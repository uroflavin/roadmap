# Development Guide

## Prerequisites

- **Python** >= 3.9
- **graphviz** system package (optional, for DOT to PNG conversion)

## Setup

```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate   # Unix/macOS
# .venv\Scripts\activate    # Windows

# Install package with dev dependencies in editable mode
pip install -e ".[dev]"
```

## Project Structure

```
src/roadmap_app/     Python package (cli, model, rendering, utils)
templates/           Jinja2 templates by output type (html/, markdown/, dot/, csv/, html-kanban/)
schema/              JSON Schema + generated markdown docs
config/              roadmap.env (dotenv configuration)
tests/               pytest tests + fixtures
docs/                CHANGELOG, developer docs, WSJF documentation
examples/            sample roadmap YAML + assets
.github/             CI workflow, release workflow, pre-commit hook
```

## Architecture

### Module Overview

| Module | Purpose |
|---|---|
| `cli.py` | Entry point: CLI arg parsing, logging setup, `main()` orchestration |
| `model.py` | Data enrichment: hierarchical IDs, WSJF/CoD calculation, `remove_element()`, `enrich_project()` |
| `rendering.py` | Template discovery, Jinja2 rendering, JSON Schema validation |
| `utils.py` | I/O helpers: YAML reading, key-value lists, versioning, base64 encoding |

### Data Pipeline

```
CLI args + config/roadmap.env
        |
        v
    YAML einlesen (utils.py)
        |
        v
    Schema-Validierung (rendering.py + schema/roadmap.json)
        |
        v
    Datenanreicherung (model.py)
    - Hierarchische IDs (_id, _parent_id, _previous_id)
    - WSJF/CoD-Berechnung
    - Gruppierung nach Datum
    - Skip-Items entfernen
    - Flache Key-Value-Liste (project["as_list"])
        |
        v
    Template-Discovery (rendering.py + templates/templates.yml)
        |
        v
    Jinja2-Rendering pro Template
        |
        v
    Output: HTML, Markdown, CSV, DOT (+ PNG via graphviz)
```

`roadmap.py` at the project root is a thin shim that imports and calls `main()` from the package.

### Domain Model

```
project
  +-- meta (version, rendertime)
  +-- logo (filename, base64)
  +-- authors[]
  +-- timeline[]
  +-- objectives[]
  |     +-- keyresults[] (with quantifiers, todos)
  |     +-- milestones[] -> deliverables[]
  +-- milestones[]
  |     +-- deliverables[] (with quantifiers, todos)
  +-- releases[]
  +-- group (precomputed groupings by date)
  +-- as_list (flat key-value representation)
```

**States:** Milestones use `IDEA | PLANNED | COMMITTED | REACHED | SKIP`. Objectives use `IDEA | ACHIEVED`. Deliverables and keyresults have `state` and `requirement` (`MUST | SHOULD | NICE_TO_HAVE`).

**ID generation:** All elements get `id` (human-readable), `_id` (sanitized, globally unique via parent chaining), `_parent_id`, and `_previous_id`. Internal computed fields are prefixed with `_`.

## CLI Usage

```bash
# After pip install -e .:
roadmap --roadmap-file examples/roadmap.yml --output-dir dist

# Or directly:
python roadmap.py --roadmap-file examples/roadmap.yml --output-dir dist
```

### Arguments

| Argument | Description | Default |
|---|---|---|
| `--roadmap-file` | Path to the roadmap YAML file | `examples/roadmap.yml` |
| `--output-dir` | Path to rendered output directory | `OUTPUT_PATH` from `roadmap.env` |
| `--skip-items` | Comma-separated dotted paths of elements to skip | (none) |
| `--environment` | Path to environment file | `config/roadmap.env` |

See [README.md](../README.md) for detailed `--skip-items` examples.

## Configuration

Configuration is loaded from `config/roadmap.env` (dotenv format). CLI arguments override these defaults.

| Variable | Purpose | Default |
|---|---|---|
| `SCHEMA` | Path to JSON Schema for validation | `schema/roadmap.json` |
| `TEMPLATE_PATH` | Root directory for Jinja2 templates | `templates/` |
| `TEMPLATE_KNOWN_SUFFIXES` | Allowed template file suffixes (JSON list) | `["md","html","dot","csv"]` |
| `OUTPUT_PATH` | Default output directory | `roadmap/` |
| `LOGFILE` | Log file path | `roadmap.log` |

## Template System

Templates are Jinja2 files organized by output type in subdirectories of `templates/`.

### Manifest (`templates/templates.yml`)

The template manifest defines which templates to render:

```yaml
- name: Full Roadmap as HTML
  input: html/roadmap.html
  output: roadmap.html
```

Currently 6 templates are configured: HTML, CSV, DOT, Markdown, and two HTML-Kanban boards (milestones, deliverables).

Each entry requires `input` (template path relative to `templates/`) and `output` (output filename relative to `--output-dir`). Invalid entries are logged and skipped.

### Fallback

If `templates.yml` is absent, the renderer falls back to walking the template directory for files matching `roadmap.<suffix>` where suffix is in `TEMPLATE_KNOWN_SUFFIXES`.

### Jinja2 Features

- `MarkdownExtension` for Markdown processing within templates
- HTML templates use deep `{% include %}` composition with ~22 partials
- `html-kanban/` shares CSS/JS with `html/` via symlinks (no duplication)
- Per-template error handling: one failing template does not block others

## Schema & Validation

- `schema/roadmap.json` defines the structure and constraints for roadmap YAML files
- Input YAML is validated against this schema before enrichment
- Pre-commit hook (`.github/pre-commit.sh`) regenerates `schema/roadmap.md` from the JSON Schema via `jsonschema2md`

## Testing

```bash
# Run all tests
pytest tests/

# Run a single test
pytest tests/test_roadmap.py::TestRoadmapFunctions::test_method_name
```

See [tests/README.md](../tests/README.md) for test structure, fixture details, and per-test descriptions.

## Linting

```bash
# Matches CI settings
flake8 src/ --count --max-complexity=34 --max-line-length=127 --statistics
```

## CI

### Test Workflow (`.github/workflows/python-app.yml`)

Runs on push/PR to `main`:
- Ubuntu + Python 3.10
- Installs `graphviz` system package
- `pip install -e ".[dev]"`
- flake8 lint check
- `pytest tests/`

### Release Workflow (`.github/workflows/release.yml`)

Triggered by pushing a tag matching `v*`:
1. Extracts version from the tag
2. Finalizes `docs/CHANGELOG.md` (replaces `[Unreleased]` header with version + date)
3. Commits the CHANGELOG update to `main`
4. Creates a GitHub Release with notes extracted from the CHANGELOG

## Versioning

- **Package version:** Derived from Git tags via `setuptools-scm` (configured in `pyproject.toml`)
- **`__version__` access:** `importlib.metadata.version("roadmap")` in the package
- **Roadmap file version:** MD5-based -- first 4 + last 4 hex characters of the MD5 hash of the YAML file content

## Pre-Commit Hooks

The pre-commit hook at `.github/pre-commit.sh` regenerates schema documentation:

```bash
jsonschema2md --examples-as-yaml --show-examples all schema/roadmap.json schema/roadmap.md
git add schema/roadmap.md
```

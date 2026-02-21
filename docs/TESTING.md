# Testing

## Running Tests

```bash
# Run all tests
pytest tests/

# Run a single test file
pytest tests/test_model.py

# Run a specific test
pytest tests/test_model.py::TestModel::test_calculate_cost_of_delay

# Verbose output
pytest tests/ -v
```

## Test Structure

Tests are organized into three files, each mirroring a module in the `src/roadmap_app/` package:

| Test file | Module under test | Tests |
|---|---|---|
| `tests/test_utils.py` | `roadmap_app.utils` | 5 |
| `tests/test_model.py` | `roadmap_app.model` | 25 |
| `tests/test_rendering.py` | `roadmap_app.rendering` | 11 |

All test classes inherit from `unittest.TestCase`.

### Test Fixture

Most tests rely on `tests/roadmap.yml`, a sample roadmap file with known properties. Changes to this file will break the hardcoded version assertion (`880a29cf`). If you modify the fixture, update the expected version accordingly (first 4 + last 4 hex chars of the MD5 hash).

## test_utils.py -- TestUtils (5 tests)

Tests for I/O helpers and data transformation utilities.

| Test | Function | Description |
|---|---|---|
| `test_create_output_folder` | `create_output_folder` | Creates a new folder and verifies idempotent re-creation |
| `test_read_roadmap_definition` | `read_roadmap_definition` | Reads a YAML file; raises `OSError` for missing files |
| `test_roadmap_yml_version_id` | `calculate_roadmap_version` | MD5-based version ID; `None` for missing files |
| `test_get_key_value_list` | `get_key_value_list` | Flattens a dict to key-value pairs with optional prefix and index |
| `test_get_filtered_key_value_list` | `get_filtered_key_value_list` | Filters a key-value list by key; raises `ValueError` without arguments |

## test_model.py -- TestModel (25 tests)

Tests for the data enrichment layer: ID generation, element removal, WSJF/CoD calculations, date grouping, and the full enrichment pipeline.

### Fixture validation (1 test)

| Test | Description |
|---|---|
| `test_preconditions_in_test_exciting_file` | Asserts the test fixture contains the expected structure (milestones, objectives, quantifiers) so that subsequent WSJF tests have a valid baseline |

### remove_element (8 tests)

| Test | Description |
|---|---|
| `test_is_level0_element_removed_from_project` | Removes a top-level key (`milestones`) |
| `test_is_level1_element_removed_from_project` | Removes a nested list key (`milestones.deliverables`) |
| `test_is_level2_element_removed_from_project` | Removes a deeply nested key (`milestones.deliverables.todos`) |
| `test_is_level1_description_removed_from_project` | Removes a scalar field (`milestones.description`) |
| `test_is_level3_removed_from_project` | Removes at depth 4 (`milestones.deliverables.todos.description`); verifies sibling branches are untouched |
| `test_is_level3_string_element_removal_is_set_to_none` | Removes a leaf scalar (`quantifiers.jobsize`) -- value is set to `None` |
| `test_correct_error_handling_for_unsupported_remove_string` | Raises `ValueError` for invalid pattern (`.`) |
| `test_remove_handles_multiple_levels_to_multiple_times` | Applies multiple comma-separated skip patterns in two rounds; verifies idempotent behavior |

### Cost of Delay / WSJF calculation (9 tests)

| Test | Description |
|---|---|
| `test_calculate_cost_of_delay` | Valid inputs: 0/0/0 = 0, 1/1/1 = 3, 10/10/10 = 30 |
| `test_calculate_cost_of_delay_non_valid_inputs` | `ValueError` for out-of-range, `None`, string, and float inputs |
| `test_calculate_weighted_shortest_job_first` | Valid inputs: min, max, floating-point rounding, jobsize 30 |
| `test_calculate_weighted_shortest_job_first_non_valid_inputs` | `ValueError` for strings, missing args, out-of-range, and `None` |
| `test_calculate_wsjf_quantifiers_if_weighted_shortest_job_is_set` | Pre-set WSJF is preserved; CoD is still calculated |
| `test_calculate_wsjf_quantifiers_if_weighted_shortest_job_is_not_set` | `None` or missing `user_business_value` causes graceful skip |
| `test_calculate_wsjf_quantifiers_if_cost_of_delay_is_set` | Pre-set CoD is preserved; WSJF remains `None` |
| `test_calculate_wsjf_quantifiers_for_milestones_deliverables` | End-to-end quantifier calculation on milestone deliverables |
| `test_calculate_wsjf_quantifiers_for_objectives_keyresult` | End-to-end quantifier calculation on objective key results |

### make_id_from (3 tests)

| Test | Description |
|---|---|
| `test_make_id_from_basic` | Spaces, dots, hyphens, and special characters become underscores; lowercased |
| `test_make_id_from_umlauts` | German umlauts and sharp-s are transliterated (e.g. `oe`, `ue`, `ss`) |
| `test_make_id_from_empty` | Empty string and no-argument call both return `""` |

### get_items_grouped_by_date (3 tests)

| Test | Description |
|---|---|
| `test_get_items_grouped_by_date` | Groups items by their `date` field |
| `test_get_items_grouped_by_date_without_date` | Items without `date` are grouped under `"None"` |
| `test_get_items_grouped_by_date_empty` | `None` and `[]` both return `{}` |

### enrich_project (1 test)

| Test | Description |
|---|---|
| `test_enrich_project` | Full enrichment pipeline: verifies `meta`, IDs on milestones/objectives, `group`, and `as_list` |

## test_rendering.py -- TestRendering (11 tests)

Tests for template discovery, YAML schema validation, and Graphviz detection.

### is_graphviz_installed (1 test)

| Test | Description |
|---|---|
| `test_is_graphviz_installed` | Skipped if `dot` binary is not on `PATH`; otherwise asserts `True` |

### validate_yaml (2 tests)

| Test | Description |
|---|---|
| `test_validate_yaml_valid` | Validates the test fixture against `schema/roadmap.json` |
| `test_validate_yaml_invalid` | Invalid data returns an error message and `is_valid=False` |

### find_templates (8 tests)

| Test | Description |
|---|---|
| `test_find_templates_with_manifest` | Manifest-based discovery: verifies returned dict keys and values |
| `test_find_templates_with_manifest_subdirectory_output` | Output path with subdirectory (e.g. `kanban/milestones.html`) |
| `test_find_templates_with_manifest_filters_unknown_suffix` | Templates with unsupported suffixes are excluded |
| `test_find_templates_with_manifest_skips_invalid_entries` | Entries missing `input` or `output` are skipped |
| `test_find_templates_with_manifest_non_list` | Non-list `templates.yml` content returns empty list |
| `test_find_templates_without_manifest` | Directory-walk fallback discovers `roadmap.<suffix>` files |
| `test_find_templates_without_manifest_filters_unknown_suffix` | Directory-walk also filters by known suffixes |
| `test_find_templates_with_real_templates` | Integration test using the actual `templates/` directory (expects 6 entries) |

## Linting

```bash
flake8 tests/ --count --max-complexity=34 --max-line-length=127 --statistics
```

## CI

Tests run automatically on push/PR to `main` via GitHub Actions (Ubuntu, Python 3.10). The CI pipeline installs the `graphviz` system package so the Graphviz-dependent test is not skipped.

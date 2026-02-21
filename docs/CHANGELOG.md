# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Breaking Changes
- fix(schema)!: correct typo "COMMITED" -> "COMMITTED" in ObjectiveState and MilestoneState
  Existing projects must update `state: COMMITED` to `state: COMMITTED` (double t).
  Affected: Objectives and Milestones. Schema validation will fail otherwise.

### Changed
- ref: split monolithic roadmap.py into src/roadmap_app/ package (cli, model, rendering, utils)
- ref: rewrite remove_element() as recursive implementation
- ref: deduplicate html-kanban CSS/JS via symlinks to html/
- ref: reorganize project structure (tests/, docs/, config/, .github/)
- ref: replace string concatenation with f-strings in model.py and cli.py
- ref: simplify `enrich_project()` -- remove duplicate skip pass, skip once after all enrichment
- ref: split `find_templates()` into manifest-based and directory-walk functions, extract shared output path logic
- ref: move `create_output_folder()` from `cli.py` to `utils.py` (I/O helper belongs with other I/O utilities)
- ref: extract `setup_logging()` and `render_templates()` from `main()`, flatten nesting via early returns

### Fixed
- fix: add validation for `templates.yml` manifest (must be list, entries require `input` and `output`)
- doc: add usage documentation to `templates.yml`
- fix: remove misleading unary plus operator in `calculate_weighted_shortest_job_first`
- fix: replace bare `except Exception` with specific exception types (KeyError, TypeError, ValueError, TemplateError, OSError)
- fix: correct typo "shure" -> "sure" in utils.py
- fix: use `with`-statement for file handle in `convert_image_to_html_base64`

### Tests
- test: fix `assertRaises` blocks -- each invalid call gets its own block
- test: make graphviz test conditional with `@skipUnless`
- test: add tests for `make_id_from()`, `get_items_grouped_by_date()`, `validate_yaml()`, `enrich_project()`
- test: add tests for `find_templates()` -- manifest-based, directory-walk fallback, suffix filtering, invalid entries, real templates
- test: split `test_roadmap.py` into `test_utils.py`, `test_model.py`, `test_rendering.py` matching package module structure
- doc: add `docs/TESTING.md` with test structure, fixture notes, and per-test descriptions

## [0.1.12] - 2025-05-28
- fix(html): #107 display date for deliverables in roadmap view left if milestone number is even
  date of deliverable is currently displayed right of deliverable, which breaks layout.

- fix(doc): Remove sponsorship by jetbrains, because sponsorship is over

## [0.1.11] - 2024-10-27
- feat(core): support project-specific templates and kanban-boards for progress-tracking #91
  This feature implements #91 and supports project-specific templates

  Every known template is stored in a ```templates.yml``` file
  
  To make use of the feature, put your ```templates.yml``` into the root of your templates-directory.
  
  The location of your templates-directory is defined in ```roadmap.env ``` as ```TEMPLATE_PATH```
  
  **This feature is backwards-compatible**: If no ```templates.yml```is found, the template-path is searched for any template starting with *roadmap* and having a suffix, given in ```TEMPLATE_KNOWN_SUFFIXES```, e.g. *roadmap.html*

  Be aware: kanban-boards are only rendered if you make use of templates.yml

## [0.1.10] - 2024-10-27
- ref: reorganize prototypes
- ref: reorganize html-template-structure

## [0.1.9] - 2024-08-18
- fix(html): accordion arrow breaks layout: arrow is displayed only if container closed

## [0.1.8] - 2024-08-18
- fix(html): accordion text-align justify breaks layout 
- fix: change accordion to dblclick to prevent accidential open or close

## [0.1.7] - 2024-06-16
- fix: tooltip is not visible (caused by accordion)

## [0.1.6] - 2024-06-16
- feat(core+html): embed logo as base64 in roadmap html template

## [0.1.5] - 2024-06-16
- ref: fix some flake error and adjust complexity level to 34
- doc: reformating examples

## [0.1.4] - 2024-06-16
- feat(html):  #39 - add foldable accordion to objective results and milestone deliverables
- doc: added html preview

## [0.1.3] - 2024-06-11
- feat(core):  Jobsize should be greater 0 - fix for #94

## [0.1.2] - 2024-06-11
- fix: Don't render "r-state" for milestones.deliverables if state is empty #95
- ref: typos in code comments

## [0.1.1] - 2024-03-02
### Fix
ref: make it more pep and fixed a bunch of typos
this was possible due to support from jetbrains :)

## [0.1.0] - 2024-02-26

BREAKING CHANGE: csv file structure changed from element structure to a key-value list

### Added

#### Feature #85: add WSJF parameters to reflect planned value and work and to enable prioritization

- documentation: added description for wsjf into docs/wsjf.md
- feat(schema): added wsjf to schema/roadmap.json
- feat(tests): put some fake data to tests/roadmap.yml
  calculated md5 and modified test_roadmap.py
- ref: ignore SameFileError while copy logo file 
- ref: add some debug info for args
- fix: allow jobsize range from 1...10 to prevent division by zero
- feat(tests): add testcase for calculate_cost_of_delay
- feat(core): add calculate_cost_of_delay
- feat(tests): add testcase for calculate_weighted_shortest_job_first
- feat(core): add calculate_weighted_shortest_job_first
- feat(tests): add testcase for calculate_wsjf_quantifiers_for_element_items
- feat(core): add calculate_wsjf_quantifiers_for_element_items
- feat(html): create a prototype for displaying wsjf and quantifier information in html template
  used icons from https://www.streamlinehq.com/ licenced under CC 4.0
- feat(core): changed wsjf into a more generall approach of using quantifiers in schema.roadmap.json
  changed documentation
  changed tests
  changed implementation
  changed html-prototype
- feat(html): base64 encode referenced icons in html template for offline use
  used https://www.base64-image.de/ as encoder
  only in html-prototype
- documentation: add wjsf and quantifiers to README and link to docs/wsjf.md
- feat(html): css variables and some more mods in prototype for quantifiers for better look
- fix(core): wrong function call during processing
- feat(core): do some postprocessing to enable skipping calculated elements
  postprocessing is using skip-items from preprocessing, we just do it twice
- feat(example): put some data to examples/roadmap.yml to display feature in the examples
- ref(test): put precondition check in separate testcase
- feat(core): support skip-items for quantifiers
- feat(html): add quantifiers to html template
  put some documentation and skip-item examples
- feat(core): added logic to make a key-value list from roadmap structure
  ref(test/core): function behaviours were refactored to be more compliant with the raise error concept

  there are two functions added to core: 
  - get_key_value_list() is capable of creating a key value list, having keys with optional index identifier
  - get_filtered_key_value_list() is capable to filter the list using key identifiers like in skip_items, just for the opposite
  
  get_key_value_list() will be used to refactor csv-export. 
  csv export will become a breaking change, because i re-arrange to just use key-value
  the advantage is, that every roadmap item could be exported, even the currently unknown items
  and the export will be much more future proof

  In addition test_roadmap.py and some function behavoiurs were refactored to be more compliant with raising error.
- fix(core): remove_element() failed with KeyError
  added a test to covers this problem
- feat(csv/core)!: add quantifiers to csv template and put project as a key-value-list under project['as_list]' for use in templates
  BREAKING CHANGE: csv file structure changed from element structure to a key-value list
- feat(markdown): add quantifiers to markdown template
- ref(prototype): got css from html template for compatibiltiy
- ref(prototype): moved css in separete file
- documentation(tech): known bug in pipreqs
- feat(dev): added rebuild of requirements as pre-commit
- feat(dev): removed rebuild of requirements as pre-commit
  needs more research work, pip must run in venv
- documentation: make a review to docs and roadmap examples

## [0.0.21] - 2024-02-21
### Added
integrate pr #87 into main: Learnings from daily usage
- feat(helloworld): removed helloworld.py including test suite
- feat(roadmap): added new command line argument for environment file
- feat(roadmap): extracted command line parsing into separate method
- feat(roadmap): adjusted requirements.txt
- doc: incorporated new findings into the technical documentation.

## [0.0.20] - 2024-02-20
### Fix
fix(html): timeline item should display date in one line

## [0.0.19] - 2024-02-18
### Added
Make the version of a roadmap unique and visible #74
Introduced project.meta.version and project.meta.rendertime

- fixes #74

## [0.0.18] - 2024-02-17
### Added
Allow project-controlled templates #79

- fixes Allow project-controlled templates #79
- feat (core): skip elements for rendering
- fix (markdown): add conditional templating for skip mechanism
- feat (tests): added roadmap.yml to tests
- feat (tests): testcoverage for remove_element()
- doc: documentation for skip mechanism
- ref+doc: some more refactorings and documentation

## [0.0.17] - 2024-02-09
### Added

- check for graphviz installed
- use logging for stdout messaging instead of print()

### Fix

- README commandline options
- a bunch of logging for commandline
- optimized: copy logo to output path moved to main

## [0.0.16] - 2024-02-06
integrated from https://github.com/rogerbackes/roadmap

### Added
minor enhancements and simply test whether it works
feat: added Dockerfile to create images
feat: added main function main function

This conditional statement if name == "main": ensures that the main function is only called when the script is executed directly, not when it's imported as a module elsewhere (e.g. in unit tests).

some more refactorings

### Fix
fixed(requirements.txt): regenerated file

## [0.0.15] - 2024-02-06
### Added
- csv-template for roadmap milestones, deliverables, objectives, keyresults and todos

## [0.0.14] - 2024-02-04
### Added
- csv-template for roadmap milestones and deliverables

## [0.0.13] - 2024-02-04
### Added
- #29: README must explain all structural elements

## [0.0.12] - 2024-02-04
### Added
- slightly modified css color of done, may and should
- #61: calculate id's: _id, id and _previous_id
- #62: add _parent_id
### Fix
- removed testing data

## [0.0.11] - 2024-02-02
### Added
- Add TODO
A Todo is something which could be used to clarify a roadmap item, e.g. a open point to discuss a milestone.
The intend of the todo is something around the roadmap process, not to do something to achieve an roadmap item
Todo is possible for objectives, milestones, deliverables and keyresults 
it is rendered in html and markdown templates

## [0.0.10] - 2024-01-27
### Fix
- html-template: Add missing objectve/milestones

## [0.0.9] - 2024-01-27
BREAKING CHANGE
### Fix
- Fix: Milestones need a date
- Fix: #14 - add a date to keyresults
- Fix: Render deliverables date

### Added
- roadmap.json
  - add date for objectives
  - add date for milestones
- re-engineered markdown template
  - add a rendered date in the template results
  - removed shitty layout ideas
- re-engineered html template
  - make html and css W3C Konform
  - add a rendered date in the template results



## [0.0.8] - 2024-01-07

### Fix
- missing title for deliverable in html-template

## [0.0.7] - 2024-01-07

### Added
- Change Order: Milestones before Objectives in HTML Template
  - this is a **breaking change**. it is affecting only html-template


## [0.0.6] - 2024-01-07

### Added
- add some stylish screen-optimized roadmap layout
    - milestones are something like a timeline 
    the deliverables of a milestone are then something like a list (each item must be done to reach milestone, no matter how)
    - objectives are something like a list
    and keyresults of an objective are something like a timeline (order matter: each keyresult follows another)

## [0.0.5] - 2023-12-30

###  Added
- [CHANGELOG.md](CHANGELOG.md) added to keep track of changes

## [0.0.4] - 2023-12-30

###  Added

- Prototype for graphviz template (see [roadmap_template.dot](roadmap/roadmap_template.dot))

## [0.0.3] - 2023-12-30

###  Fixed

- Some refactorings: Mainly function name conventions, documentation improvements
## [0.0.2] - 2023-12-27
### Added
- render roadmap as dot, and also as png for later use
  - you can use roadmap.dot.png in your project description to render it as part of your description

## [0.0.1] - 2023-12-23

###  Added

- #10 - output and roadmap.yml should be in separate outside roadmap-folders 
  - if there are some arguments, then they will take precedence over static config


[unreleased]: https://github.com/uroflavin/roadmap/tree/master
[0.0.1]: https://github.com/uroflavin/roadmap/pull/24
[0.0.2]: https://github.com/uroflavin/roadmap/pull/30
[0.0.3]: https://github.com/uroflavin/roadmap/pull/33
[0.0.4]: https://github.com/uroflavin/roadmap/pull/34
[0.0.5]: https://github.com/uroflavin/roadmap/pull/36
[0.0.6]: https://github.com/uroflavin/roadmap/pull/40
[0.0.7]: https://github.com/uroflavin/roadmap/pull/41
[0.0.8]: https://github.com/uroflavin/roadmap/pull/43
[0.0.9]: https://github.com/uroflavin/roadmap/pull/49
[0.0.10]: https://github.com/uroflavin/roadmap/pull/52
[0.0.11]: https://github.com/uroflavin/roadmap/pull/57
[0.0.12]: https://github.com/uroflavin/roadmap/pull/63
[0.0.13]: https://github.com/uroflavin/roadmap/pull/65
[0.0.14]: https://github.com/uroflavin/roadmap/pull/66
[0.0.15]: https://github.com/uroflavin/roadmap/pull/67
[0.0.16]: https://github.com/uroflavin/roadmap/pull/69
[0.0.17]: https://github.com/uroflavin/roadmap/pull/81
[0.0.18]: https://github.com/uroflavin/roadmap/pull/83
[0.0.19]: https://github.com/uroflavin/roadmap/pull/84
[0.0.20]: https://github.com/uroflavin/roadmap/pull/86
[0.0.21]: https://github.com/uroflavin/roadmap/pull/88
[0.1.0]: https://github.com/uroflavin/roadmap/pull/90
[0.1.1]: https://github.com/uroflavin/roadmap/pull/92
[0.1.2]: https://github.com/uroflavin/roadmap/pull/96
[0.1.3]: https://github.com/uroflavin/roadmap/pull/97
[0.1.4]: https://github.com/uroflavin/roadmap/pull/98
[0.1.5]: https://github.com/uroflavin/roadmap/pull/99
[0.1.6]: https://github.com/uroflavin/roadmap/pull/100
[0.1.7]: https://github.com/uroflavin/roadmap/pull/101
[0.1.8]: https://github.com/uroflavin/roadmap/pull/102
[0.1.9]: https://github.com/uroflavin/roadmap/pull/104
[0.1.10]: https://github.com/uroflavin/roadmap/pull/105
[0.1.11]: https://github.com/uroflavin/roadmap/pull/106
[0.1.12]: https://github.com/uroflavin/roadmap/pull/108
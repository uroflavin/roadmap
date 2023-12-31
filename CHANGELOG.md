# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
-  see [TODO.md](TODO.md)

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
# roadmap
Manage your project and team road maps in YAML

This project is heavyly inspired by https://github.com/SierraSoftworks/roadmap, with some key-differences:
 - roadmap is a clone, implemented in python
 - the roadmap-structure is slightly different

My development approach is to implement the main functions of https://github.com/SierraSoftworks/roadmap. This concerns the creation of a view as HTML and PDF.

I mainly focus on mapping the following structure:
 - A project has any number of objectives
    - An objective has any number of milestones
        - A milestone has any number of results
            - a result can be assigned to a release.
- timeline and the project metadata are unchanged
- The whole thing is supplemented by release assignments

Objectives, milestones, results and releases can have any number of references.

The main structure of a roadmap is as follows:
- title
- description
- authors
- timeline
- releases
- objectives


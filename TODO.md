# This is a list of todos and ideas

This list is a scratchpad during development of a new features to break down some work into smaller parts.

### TODOS
- [ ] add hillcharts for visual progress 
      you can enable hillchart-tracking by applying "progress"-tag to a deliverable
      every tagged item from a milestone will then be tracked as a hillchart-item 

- [ ] add involved teams
      involved teams are identified by their tag

- [x] feat(core): support project-specific templates and kanban-boards for progress-tracking #91
  This feature implements #91 and supports project-specific templates

  Every known template is stored in a ```templates.yml``` file
  
  To make use of the feature, put your ```templates.yml``` into the root of your templates-directory.
  
  The location of your templates-directory is defined in ```roadmap.env ``` as ```TEMPLATE_PATH```
  
  **This feature is backwards-compatible**: If no ```templates.yml```is found, the template-path is searched for any template starting with *roadmap* and having a suffix, given in ```TEMPLATE_KNOWN_SUFFIXES```, e.g. *roadmap.html*

  Be aware: kanban-boards are only rendered if you make use of templates.yml
  

- [x] reorganize html-template-structure

## Reminder Notes
The function get_key_value_list() contains a lot of the logic to refactor remove_element().

Markdown Template needs refactoring. There are a bunch of empty lines. looks terrible in the md file, but renders okayish.
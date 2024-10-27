# This is a list of todos and ideas

This list is a scratchpad during development of a new features to break down some work into smaller parts.

### TODOS
- [ ] add hillcharts for visual progress 
      you can enable hillchart-tracking by applying "progress"-tag to a deliverable
      every tagged item from a milestone will then be tracked as a hillchart-item 

- [ ] add involved teams
      involved teams are identified by their tag

- [ ] enable different templates from same type
      it is not possible to render two files with the same name
      so if we like to render various html-pages of diffenernt types this is not possible
      the reason lives mainly in the static entry-point for the templates
      so make the templates more project-specific
      for this, we have some options to decide:
      - add template structure to roadmap.yml
      - add template structure as a separate .env file
      - build some guessing-machine
        - e.g use  folder-names instead of file-names to render the output
      however, every design is bundled to a project, so best idea might be to put it in roadmap.yml
      - templates
        - template:
          name: HTML-Index
          input: html/roadmap.html
          output: 
          - file: html/index.html
          - displayname: Übersicht
        - template:
          name: HTML-Kanbanboard for Milestones
          input: html/roadmap.kanban.milestones.html
          output: 
          - file: html/kanbanboard.milestones.html
          - displayname: Kanban-Board für Meilensteine

- [x] reorganize html-template-structure

## Reminder Notes
The function get_key_value_list() contains a lot of the logic to refactor remove_element().

Markdown Template needs refactoring. There are a bunch of empty lines. looks terrible in the md file, but renders okayish.
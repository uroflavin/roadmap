# This is a list of todos and ideas

This list is a scratchpad during development of a new features to break down some work into smaller parts.

## Feature #85: add WSJF parameters to reflect planned value and work and to enable prioritization

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
### TODOS
- [x] added description for wsjf into docs/wsjf.md
- [x] added wsjf to schema/roadmap.json
  for deliverables and keyresults only
  with examples
  with full template for autocompletion in vscode
- [x] updated schema/roadmap.md documentation
- [x] put some fake data to tests/roadmap.yml
  calculated md5 and modified test_roadmap.py
- [x] add testcases to calculate quantifiers
- [x] implement calculation of quantifiers (before rendering)
- [x] create a prototype for displaying wsjf and quantifier information in html template
- [x] changed wsjf into a more generall approach of using quantifiers in schema.roadmap.json
- [X] base64 encode referenced icons in html template for offline use
- [x] add wjsf and quantifiers to README
- [x] put some data to examples/roadmap.yml to display feature in the examples
- [x] add quantifiers to html template
- [x] add quantifiers to csv template
- [x] add quantifiers to markdown template
- [x] check requirements.txt for any new requirements
- [x] enable calculation of cod and wsjf but hide details using skip mechanics
  skip_items is possible by design
  html template is keept clean
- [x] make a review to docs (readme, schema, wsjf) 
- [x] make a review to rendered roadmap examples
- [ ] merge into master
- [ ] update changelog
- [ ] merge into main



## Reminder Notes
The function get_key_value_list() contains a lot of the logic to refactor remove_element().

Markdown Template needs refactoring. There are a bunch of empty lines. looks terrible in the md file, but renders okayish.
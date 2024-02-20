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
- [ ] create a prototype for displaying wsjf and quantifier information in html template
- [ ] put some data to examples/roadmap.yml to display feature in the examples
- [ ] add wsjf and quantifiers to html template
- [ ] add wsjf and quantifiers to csv template
- [ ] add wsjf and quantifiers to markdown template
- [ ] add wjsf to README / see also part --skip-items
- [ ] check requirements.txt for any new requirements
- [ ] merge into master
- [ ] update changelog
- [ ] merge into main


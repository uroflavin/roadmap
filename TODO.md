# This is a list of todos and ideas

- [ ] #18 - timeline: group by same dates
    Sometimes you have two important activities with the same date
    it would be nicer to read to have them grouped by date

- [ ] #16 - make a connection between keyresults and milestones

- [ ] #14 - add a date to keyresults

- [ ] #13 - add involved teams for keyresults

- [ ] #29 - README must explain all structural elements
    - [ ] first step is to check and add roadmap.json for any missing description and example
    - [ ] second is to find something which is capable to render some nice documentation out of the json-schema
    - [ ] then produce a separate file (e.g. DOCUMENTATION.md), which holds the rendered documentation
    - [ ] improve README for better access for newbies, e.g. some pictures and better newbie-explanation
    - [ ] lastly find a way to render the documentation automatically for each commit

- [ ] add missing parts to the templates
    - involved teams
    - releases
    - ...some more?? (see #29)

- [ ] use gitpages for demonstration of roadmap.py capabilities
    - use roadmap.html and maybe the readme or some more stuff

- [ ] write a documentation on howto install roadmap.py
    - check requirements.txt for completenes
    - maybe use some cr/cd pipeline magic to test all the stuff and to make shure no parts are missing during further development

- [ ] render roadmap as pdf

- [ ] render roadmap as xls

- [ ] add a rendered date in the template results
      this is helpful for readers to know, which roadmap-version they are looking at

- [ ] Milestones: make deliverables foldable (SHOULD)

- [ ] Objectives: make keyresults foldable (MAY)

- [ ] HTML Template: Add Timeline-Ruler if screen < 600px
    just now, the timeline-ruler is display:none if screensize < 600px
    it would be nice, if we can see the marker but only leftside...
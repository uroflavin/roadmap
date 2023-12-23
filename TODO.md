# This is a list of todos and ideas

- [x] #10 - output and roadmap.yml should be in separate outside roadmap-folders 
    - [x] As a good first stept it would be helpfull to read some directories in a given template-path
        - Read every folder/roadmap.* as a starting point for a given template
        - the type is the templates-folder-name
        - then render the found template and output in given output-path
        - the final suffix is derived from template suffix
    - [x] A second good step would be to pack everything in roadmap.py in functional parts
    - [x] Third step would be to add some logic for argument handling
        - if there are some arguments, then they will take precedence over static config
- [ ] #18 - timeline: group by same dates
    Sometimes you have two important activities with the same date
    it would be nicer to read to have them grouped by date
- [ ] #16 - make a connection between keyresults and milestones
- [ ] #14 - add a date to keyresults
- [ ] #13 - add involved teams for keyresults
- [x] #4 - Support for project logo
    Logo must be placed where roadmap.yml lives
    it is copied during template processing
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

- [ ] add some stylish screen-optimized roadmap layout

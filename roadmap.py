import yaml

from dotenv import dotenv_values # Environment

import os
import logging

from jinja2 import Template


LOGFILE= os. getcwd() + "/roadmap.log"
logging.basicConfig(filename=LOGFILE, encoding='utf-8', level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

# No need already
# config = dotenv_values(".env") 

## Read Example
with open('examples/roadmap.full.yml') as f:
    project = yaml.load(f, Loader=yaml.FullLoader)
    logging.debug("%s", project)

## Read Markdown Template
with open('roadmap.template.md') as f:
    tmpl = Template(f.read())
    output_from_parsed_template = tmpl.render(project = project)

## Render Markdown
with open("roadmap.md", "w") as f:
    f.write(output_from_parsed_template)

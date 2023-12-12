import yaml

from dotenv import dotenv_values # Environment

import os
from pathlib import Path

import logging

from jinja2 import FileSystemLoader, Environment, Template

# Load Config from .env
config = dotenv_values("roadmap.env") 

LOGFILE= config["LOGFILE"]
logging.basicConfig(filename=LOGFILE, encoding='utf-8', level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

# Init
try:
    os.mkdir(config["OUTPUT_PATH"])
except:
    pass

## Read Roadmap-Definition
# TOOD: roadmap definition should be commandline-argument
roadmap_definition_file="examples/roadmap.yml"
with open(roadmap_definition_file) as f:
    project = yaml.load(f, Loader=yaml.FullLoader)
    logging.debug("%s", project)

## Read Markdown Template
env = Environment()
env.loader = FileSystemLoader( os.path.dirname(config["TEMPLATE_PATH_MARKDOWN"]) )
template_markdown = env.get_template(os.path.basename(config["TEMPLATE_PATH_MARKDOWN"]))
output_from_parsed_markdown_template = template_markdown.render(project = project)

## Render Markdown
# output-name is derived from roadmap_definition_file
output_basename=Path(roadmap_definition_file).stem
output_file_markdown = config["OUTPUT_PATH"] + output_basename + ".md"
with open(output_file_markdown, "w") as f:
    f.write(output_from_parsed_markdown_template)

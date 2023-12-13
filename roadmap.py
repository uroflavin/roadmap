import yaml
import json
import jsonschema
from jsonschema import validate

from dotenv import dotenv_values # Environment

import os
from pathlib import Path

import logging

from jinja2 import FileSystemLoader, Environment, Template
from jinja_markdown import MarkdownExtension
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


# validate yml
def validateYaml(roadmapData, jsonSchema):
    try:
        # Read Schema from File
        with open(jsonSchema,"r") as f:
            schema = f.read()
        # Convert Schema to Python Dict
        schema = json.loads(schema)
        logging.debug("%s", schema)

        # Convert ymlData to Python Dict
        instance = json.loads(json.dumps(roadmapData, indent=4, sort_keys=True, default=str))
        logging.debug("%s", instance)
        validate(instance=instance, schema=schema)
    except jsonschema.exceptions.ValidationError as err:
        logging.error("schema")
        logging.error("%s", schema)
        logging.error("instance")
        logging.error("%s", instance)
        logging.error("ValidationError")
        logging.error("%s", err)
        return err, False
    return None, True

validation_error, is_valid_yaml = validateYaml(project, jsonSchema="schema/roadmap.json")

if is_valid_yaml:
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

## Read HTML Template
    env = Environment()
    env.loader = FileSystemLoader( os.path.dirname(config["TEMPLATE_PATH_HTML"]) )
    env.add_extension(MarkdownExtension)
    template_html = env.get_template(os.path.basename(config["TEMPLATE_PATH_HTML"]))
    output_from_parsed_html_template = template_html.render(project = project)

    ## Render HTML
    # output-name is derived from roadmap_definition_file
    output_basename=Path(roadmap_definition_file).stem
    output_file_html = config["OUTPUT_PATH"] + output_basename + ".html"
    with open(output_file_html, "w") as f:
        f.write(output_from_parsed_html_template)
    print("roadmap-conversion successful")


else:
    print(roadmap_definition_file + " contains no valid YAML-data")
    print(validation_error)
    print("See logfile for details")
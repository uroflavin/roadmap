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
logging.debug("config: %s", config)

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
    logging.debug("project: %s",project)


# validate yml
def validateYaml(roadmapData, jsonSchema):
    try:
        # Read Schema from File
        with open(jsonSchema,"r") as f:
            schema = f.read()
        # Convert Schema to Python Dict
        schema = json.loads(schema)
        logging.debug("schema: %s", schema)

        # Convert ymlData to Python Dict
        instance = json.loads(json.dumps(roadmapData, indent=4, sort_keys=True, default=str))
        logging.debug("instance: %s", instance)
        validate(instance=instance, schema=schema)
        return None, True
    except jsonschema.exceptions.ValidationError as err:
        logging.error("schema: %s", schema)
        logging.error("instance: %s", instance)
        logging.error("ValidationError: %s", err)
        return err, False

validation_error, is_valid_yaml = validateYaml(project, jsonSchema=config["SCHEMA"])

if is_valid_yaml:
    # Find all templates
    templates = []
    for dirname, dirnames, filenames in os.walk(config["TEMPLATE_PATH"]):
        for file in filenames:
            file_parts = file.split(".")

            if len(file_parts) == 2 and file_parts[0] == "roadmap":
                file_suffix = file_parts[1]
                if file_suffix in config["TEMPLATE_KNOWN_SUFFIXES"]:
                    templates.append({
                        "path" : dirname + os.sep, 
                        "file": file,
                        "suffix": file_suffix,
                        "type": dirname.split("/")[1]
                        })
    logging.debug("templates: %s", templates)
    # process templates with jinja
    # Load Jinja Environment
    env = Environment()
    # Add some extensions for jinja
    env.add_extension(MarkdownExtension)
    
    for template in templates:
 #       try:
            env.loader = FileSystemLoader( template["path"]) 
            template_file = env.get_template(template["file"])   
            rendered_template = template_file.render(project = project)

            output_basename=Path(roadmap_definition_file).stem
            output_file = config["OUTPUT_PATH"] + output_basename + "." + template["suffix"]
            with open(output_file, "w") as f:
                f.write(rendered_template)
            logging.info("processed '%s' with template '%s' to '%s'", roadmap_definition_file, template["path"] + template["file"], output_file)
 #       except Exception as err:
 #           logging.error("processing template %s failed with error %s", template["path"] + "/" + template["file"], err)

    print("roadmap-conversion successful")


else:
    print(roadmap_definition_file + " contains no valid YAML-data")
    print(validation_error)
    print("See logfile for details")
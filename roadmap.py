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


def createOutputFolder(path_to_folder: str = ""):
    """
    Create Folder for the roadmap.py output
    If path_to_folder exist, nothing happens

    Return True: if folder is writeable
    Return False: if folder is not writeable

    :param str path_to_folder: Target folder
    :return: True on Success, False on Error
    :rtype: bool
    """
    # check if path exist
    output_folder = Path(path_to_folder)
    if( not output_folder.exists() ):
        try:
            output_folder.mkdir(parents=False, exist_ok=True)
        # FileNotFoundError is thrown if some parts of path are not present
        except FileNotFoundError as err:
            logging.error("some folders for output_folder '%s' did not exist", path_to_folder)
            logging.error(err)
            return False
    
    # write-access?
    if output_folder.stat().st_mode & 0o200:
        logging.debug("output_folder '%s' is writeable", path_to_folder)
        return True
    else:
        logging.error("output_folder '%s' is not writeable", path_to_folder)
        return False


def readRoadmapDefinition(path_to_roadmap_yml: str = ""):
    """
    Read the Roadmap-Defintion-YML
    
    Return Dict: if conversion to dict was successfull
    Return None: if conversion failed

    :param str path_to_roadmap_yml: path/to/roadmap.yml
    :return: dict on Success, None on Error
    :rtype: dict
    """
    try:
        with open(path_to_roadmap_yml,"r") as f:
            project = yaml.load(f, Loader=yaml.FullLoader)
            logging.debug("project: %s",project)
            return project
    except OSError as err:
        logging.error("roadmap-definition-file '%s' not readable")
        return None

def validateYaml(roadmap_data: dict = {}, path_to_json_schema: str = ""):
    """
    Validate roadmap-dictionary under the given jsonSchema
    
    Return tuple, True: if conversion to dict was successfull
    Return None, False: if conversion failed

    :param dict roadmap_data: dictionary containing roadmap-data
    :param str path_to_json_schema: path/to/schema/roadmap.json
    :return: None/Error, validationResult as boolean
    :rtype: tuple
    """
    try:
        # Read Schema from File
        with open(path_to_json_schema,"r") as f:
            schema = f.read()
        # Convert Schema to Python Dict
        schema = json.loads(schema)
        logging.debug("schema: %s", schema)

        # Convert ymlData to Python Dict
        instance = json.loads(json.dumps(roadmap_data, indent=4, sort_keys=True, default=str))
        logging.debug("instance: %s", instance)
        validate(instance=instance, schema=schema)
        return None, True
    except jsonschema.exceptions.ValidationError as err:
        logging.error("schema: %s", schema)
        logging.error("instance: %s", instance)
        logging.error("ValidationError: %s", err)
        return err, False

def findTemplates(template_path: str = "", template_known_suffixes: list = [] ):
    """
    find all templates in given template_path
    
    Return list of templates
    :param str template_path: directory containing templates 
    :param list template_known_suffixes: list of know-suffixes for templates, e.g. html, md, txt
    :return: templates
    :rtype: list
    """
    templates = []
    for dirname, dirnames, filenames in os.walk(template_path):
        for file in filenames:
            file_parts = file.split(".")

            if len(file_parts) == 2 and file_parts[0] == "roadmap":
                file_suffix = file_parts[1]
                if file_suffix in template_known_suffixes:
                    templates.append({
                        "path" : dirname + os.sep, 
                        "file": file,
                        "suffix": file_suffix,
                        "type": dirname.split("/")[1]
                        })
    logging.debug("templates: %s", templates)
    
    return templates

def processTemplate(environment: Environment = Environment(), template: dict = {"path": "", "file": "", "suffix": "", "type": ""}, roadmap_definition_file: str = "", project=None, output_path: str = ""):
    """
    process the template and write rendered output-data to filesystem
    
    filename of roadmap.yml without suffix is used as output name
    
    :param Environment environment: this is the jinja-template-environment
    :param dict template: contain the template data
    :param str roadmap_definition_file: filename of roadmap.yml
    :param dict project: roadmap data as dict
    :param str output_path: path for the rendered templates
    :return: Nothing
    :rtype: None
    """
    try:
        environment.loader = FileSystemLoader( template["path"]) 
        template_file = environment.get_template(template["file"])   
        rendered_template = template_file.render(project = project)

        output_basename=Path(roadmap_definition_file).stem
        output_file = output_path + output_basename + "." + template["suffix"]

        with open(output_file, "w") as f:
            f.write(rendered_template)
        logging.info("processed '%s' with template '%s' to '%s'", roadmap_definition_file, template["path"] + template["file"], output_file)
    except Exception as err:
        logging.error("processing template %s failed with error %s", template["path"] + "/" + template["file"], err)


# Init
# Load Config from roadmap.env
config = dotenv_values("roadmap.env") 

LOGFILE= config["LOGFILE"]
logging.basicConfig(filename=LOGFILE, encoding='utf-8', level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logging.debug("config: %s", config)

if createOutputFolder(config["OUTPUT_PATH"]):
    ## Read Roadmap-Definition
    # TOOD: roadmap definition should be commandline-argument
    roadmap_definition_file="examples/roadmap.yml"
    project = readRoadmapDefinition(path_to_roadmap_yml=roadmap_definition_file)


    validation_error, is_valid_yaml = validateYaml(roadmap_data=project, path_to_json_schema=config["SCHEMA"])


    if is_valid_yaml:
        # Find all templates
        templates = findTemplates(template_path=config["TEMPLATE_PATH"], template_known_suffixes=config["TEMPLATE_KNOWN_SUFFIXES"])
        # process templates with jinja
        # Load Jinja Environment
        env = Environment()
        # Add some extensions for jinja
        env.add_extension(MarkdownExtension)
        
        for template in templates:
            processTemplate(environment=env, template=template, roadmap_definition_file=roadmap_definition_file, project=project, output_path=config["OUTPUT_PATH"])
    
        print("roadmap-conversion successful")


    else:
        print(roadmap_definition_file + " contains no valid YAML-data")
        print(validation_error)
        print("See logfile for details")
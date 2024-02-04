import yaml
import json
import jsonschema
from jsonschema import validate

from dotenv import dotenv_values  # Environment

import os
from pathlib import Path

import logging

from jinja2 import FileSystemLoader, Environment
from jinja_markdown import MarkdownExtension

import argparse
import shutil

import subprocess

from pprint import pprint

def create_output_folder(path_to_folder: str = ""):
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
    if not output_folder.exists():
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


def read_roadmap_definition(path_to_roadmap_yml: str = ""):
    """
    Read the Roadmap-Defintion-YML
    
    Return Dict: if conversion to dict was successfull
    Return None: if conversion failed

    :param str path_to_roadmap_yml: path/to/roadmap.yml
    :return: dict on Success, None on Error
    :rtype: dict
    """
    try:
        with open(path_to_roadmap_yml, "r") as f:
            project = yaml.load(f, Loader=yaml.FullLoader)
            logging.debug("project: %s", project)
            return project
    except OSError as err:
        logging.error("roadmap-definition-file '%s' not readable")
        logging.error("'%s'", err)
        return None


def validate_yaml(roadmap_data: dict = None, path_to_json_schema: str = ""):
    """
    Validate roadmap-dictionary under the given jsonSchema
    
    Return tuple, True: if conversion to dict was successfull
    Return None, False: if conversion failed

    :param dict roadmap_data: dictionary containing roadmap-data
    :param str path_to_json_schema: path/to/schema/roadmap.json
    :return: None/Error, validationResult as boolean
    :rtype: tuple
    """
    schema = None
    instance = None

    try:
        # Read Schema from File
        with open(path_to_json_schema, "r") as f:
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


def find_templates(template_path: str = "", template_known_suffixes: list = None):
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
                        "path": dirname + os.sep,
                        "file": file,
                        "suffix": file_suffix,
                        "type": dirname.split("/")[1]
                    })
    logging.debug("templates: %s", templates)

    return templates


def process_template(environment: Environment = Environment(),
                     template: dict = None,
                     roadmap_definition_file: str = "", project=None, output_path: str = ""):
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
    if template is None:
        template = {"path": "", "file": "", "suffix": "", "type": ""}

    try:
        environment.loader = FileSystemLoader(template["path"])
        template_file = environment.get_template(template["file"])
        rendered_template = template_file.render(project=project)

        output_basename = Path(roadmap_definition_file).stem
        output_file = output_path + output_basename + "." + template["suffix"]

        with open(output_file, "w") as f:
            f.write(rendered_template)

        # copy logo to output path
        if "logo" in project:
            logo_src_path = str(Path(roadmap_definition_file).parent.absolute().resolve()) + "/" + project["logo"][
                "filename"]
            shutil.copy(logo_src_path, output_folder)
        # if dot file, try converting it to png, 
        # log error but continue
        try:
            if template["suffix"] == "dot":
                output_png = output_path + output_basename + ".dot.png"
                subprocess.check_call(['dot', '-Tpng', output_file, '-o', output_png])
        except Exception as err:
            logging.error("dot-converting failed '%s'", err)
            logging.error("make shure to install graphiv properly")

        logging.info("processed '%s' with template '%s' to '%s'", roadmap_definition_file,
                     template["path"] + template["file"], output_file)
    except Exception as err:
        logging.error("processing template %s failed with error %s", template["path"] + "/" + template["file"], err)

def get_items_grouped_by_date(elements=None):
    """
    group timeline by similar dates, keeps order from original
    if element-item has no date attribute, we use "None" to get a group
    :param dict element: roadmap element data as dict, e.g. timeline, objectives...
    :return: dict project with added ["group"]["timeline_by"]["date"] 
    """
    
    grouped_items = {}
    if len(elements) > 0:
        for item in elements:
            # make shure we have a date
            if "date" in item:
                # deside to init or append group
                if item["date"] in grouped_items:
                    grouped_items[item["date"]].append(item.copy())
                else:
                    grouped_items[item["date"]] = [item.copy()]
            # if we have no date, we use "None" for this group
            else:
                if "None" in grouped_items:
                    grouped_items["None"].append(item.copy())
                else:
                    grouped_items["None"] = [item.copy()]
    return grouped_items.copy()

def make_id_from(input: str = ""):
    """
    generate id for given input
    strips whitespace, dots etc. from input and make it lowercase
    :param str input: input element
    :return: str generated id
    """
    # make input lower
    _id = str(input).lower()
    # this list contains every non valid characters, which are replaced by #replacestring
    non_valid_id_characters = [" ", ".", "-", "#", "+", "*"]
    # this is the replacement character
    replacement_character = "_"
    for char in non_valid_id_characters:
        _id = _id.replace(char, replacement_character)
    # replace umlaute
    special_char_map = {ord('ä'):'ae', ord('ü'):'ue', ord('ö'):'oe', ord('ß'):'ss'}
    _id = _id.translate(special_char_map)
    return _id

def calculate_ids_for_element_items(elements: dict = None, prefix: str ="", parent_id: str = ""):
    """
    calculate ids for todos, objectives, keyresults, milestones and deliverables
    add _id field which is cleaned version from id
    add id if id is not present in elements items
    :param dict element: roadmap element data as dict, e.g. timeline, objectives...
    :param str prefix: prefix for id, used only if id is not set
    :return: dict new project with added ["_id"] and ["id] 
    """
    # lets iterate over each element and add "id", "_id" and "_parent_id"
    # because we like to have a human-readable id, we start at 1
    _previous_id = ""
    _next_id = ""

    for count, item in enumerate(elements, start=1):
        # item.id will get prefix and count, if unset
        if "id" not in item or item["id"] == "":
            item["id"] = prefix + str(count)
            #item["id"] = make_id_from(item["title"]) # this is, if we  like to use the title as id - which makes possibly no sense ;)
        
        # # parent_id is set from function call
        if "_parent_id" not in item or item["_parent_id"] == "":
            item["_parent_id"] = make_id_from(parent_id)
       
        # if parent_id is empty, we create id without parent_id
        if parent_id == "":
            item["_id"] = make_id_from(item["id"])
        # if parent_id is not empty, we add it before _id to make it unique
        else: 
            item["_id"] = parent_id + "_" + make_id_from(item["id"])
        # for later use, we store _id in _parent_id
        _parent_id = item["_id"]

        # add previous
        item["_previous_id"] = _previous_id
        # set _previous to current _id for next round
        _previous_id = item["_id"]

        # check each dict-object and calculate the id's
        if "keyresults" in item:
            item["keyresults"] = calculate_ids_for_element_items(item["keyresults"], "R", parent_id=_parent_id)
        if "deliverables" in item:
            item["deliverables"] = calculate_ids_for_element_items(item["deliverables"], "D", parent_id=_parent_id)
        if "objectives" in item:
            item["objectives"] = calculate_ids_for_element_items(item["objectives"], "O", parent_id=_parent_id)
        if "milestones" in item:
            item["milestones"] = calculate_ids_for_element_items(item["milestones"], "M", parent_id=_parent_id)
        if "todos" in item:
            item["todos"] = calculate_ids_for_element_items(item["todos"], "TODO", parent_id=_parent_id)
        if "timeline" in item:
            item["timeline"] = calculate_ids_for_element_items(item["timeline"], "timeline", parent_id=_parent_id)
        if "releases" in item:
            item["releases"] = calculate_ids_for_element_items(item["releases"], "Release", parent_id=_parent_id)

    return elements.copy()

# Init
# Load Config from roadmap.env
config = dotenv_values("roadmap.env")

LOGFILE = config["LOGFILE"]
logging.basicConfig(filename=LOGFILE, encoding='utf-8', level=logging.DEBUG,
                    format='%(asctime)s [%(levelname)s] %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logging.debug("config: %s", config)

parser = argparse.ArgumentParser()
parser.add_argument("--roadmap-file", type=str,
                    help="path to roadmap.yml", nargs="?", default="examples/roadmap.yml")

parser.add_argument("--output-dir", type=str,
                    help="path to rendered output", nargs="?", default=config["OUTPUT_PATH"])

args = parser.parse_args()

roadmap_definition_file = args.roadmap_file
output_folder = args.output_dir

if output_folder[-1] != os.sep:
    output_folder = output_folder + os.sep


if create_output_folder(output_folder):
    # Read Roadmap-Definition
    project = read_roadmap_definition(path_to_roadmap_yml=roadmap_definition_file)

    validation_error, is_valid_yaml = validate_yaml(roadmap_data=project, path_to_json_schema=config["SCHEMA"])

    if is_valid_yaml:
        # Find all templates
        templates = find_templates(template_path=config["TEMPLATE_PATH"],
                                   template_known_suffixes=config["TEMPLATE_KNOWN_SUFFIXES"])
        # Calculate some information to project
        # add _id, id, _parent_id and _previous_id
        if "timeline" in project:
            project['timeline'] = calculate_ids_for_element_items(project['timeline'], prefix="Timeline")
        if "objectives" in project:
            project['objectives'] = calculate_ids_for_element_items(project['objectives'], prefix="O")
        if "milestones" in project:
            project['milestones'] = calculate_ids_for_element_items(project['milestones'], prefix="M")
        if "releases" in project:
            project['releases'] = calculate_ids_for_element_items(project['releases'], prefix="Release")
        
        # get items groupedy by date
        project["group"] = {
            "timeline_by" : {
                "date": get_items_grouped_by_date(project["timeline"])
            },
            "objectives_by" : {
                "date": get_items_grouped_by_date(project["objectives"])
            }
        }
        # process templates with jinja
        # Load Jinja Environment
        env = Environment()
        # Add some extensions for jinja
        env.add_extension(MarkdownExtension)

        for template in templates:
            print("processing " + template["file"])
            process_template(environment=env, template=template, roadmap_definition_file=roadmap_definition_file,
                             project=project, output_path=output_folder)

        print("roadmap-conversion successful")

    else:
        print(roadmap_definition_file + " contains no valid YAML-data")
        print(validation_error)
        print("See logfile for details")
else:
    print("Could not create '" + output_folder + "'")
    print("See logfile for details")

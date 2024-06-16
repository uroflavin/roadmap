# Used for reading and writing YAML files.
import yaml

# Used for reading and writing JSON files.
import json

# Used for validating JSON data against a schema.
import jsonschema

# Provides functions for interacting with the operating system.
import os

# Used for writing user-friendly command-line interfaces.
import argparse

# Used for high-level file operations.
import shutil

# Used for running new applications or commands in new processes.
import subprocess

# Used for logging events that happen while the application is running.
import logging

# Used for loading templates from the file system and creating
# a Jinja2 environment.
from jinja2 import FileSystemLoader, Environment

# A function to validate a given JSON data with a given JSON schema.
from jsonschema import validate

# Used for reading key-value pairs from a .env file and returning them as a dictionary.
from dotenv import dotenv_values

# Provides various classes representing file system paths with semantics appropriate for different operating systems.
from pathlib import Path

# A Jinja2 extension to add Markdown support to Jinja2 templates.
from jinja_markdown import MarkdownExtension

# A dictionary subclass that calls a factory function to supply missing values.
from collections import defaultdict

# need sys.stdout as logging handler for stdout
import sys

# need to calculate hash of roadmap.yml for project.version
import hashlib

# time is used to output rendering timestamp
import time

# base64 is used to convert image to html embeddable string
import base64

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
            logging.error(
                "some folders for output_folder '%s' did not exist", path_to_folder)
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
    Read the Roadmap-Definition-YML

    Return Dict: if conversion to dict was successfully
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
        # in case of an error log file name and error message
        logging.debug("roadmap-definition-file '%s' not readable", path_to_roadmap_yml)
        logging.debug("Error: %s", err.strerror)
        raise err


def validate_yaml(roadmap_data: dict = None, path_to_json_schema: str = ""):
    """
    Validate roadmap-dictionary under the given jsonSchema

    Return tuple, True: if conversion to dict was successfully
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
        instance = json.loads(json.dumps(
            roadmap_data, indent=4, sort_keys=True, default=str))
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
    for dirname, dir_names, filenames in os.walk(template_path):
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


def is_graphviz_installed():
    """
    Check if graphviz is installed in current environment

    uses 'dot -V' and check for 'graphviz version' string in output

    :return: True if dot is installed, False if dot is not installed
    :rtype: bool
    """
    graphviz_version = subprocess.check_output(['dot', '-V'], stderr=subprocess.STDOUT)
    if "graphviz version" in str(graphviz_version):
        return True

    return False


def process_template(
        environment: Environment = None,
        template: dict = None,
        roadmap_definition_file: str = "",
        project=None,
        output_path: str = ""
):
    """
    Process the template and write rendered output-data to filesystem.

    :param environment: Jinja2 Environment object for template rendering.
    :type environment: Environment, optional
    :param template: Dictionary containing the template data.
    :type template: dict, optional
    :param roadmap_definition_file: Filename of the roadmap.yml file.
    :type roadmap_definition_file: str, optional
    :param project: Roadmap data as a dictionary.
    :type project: dict, optional
    :param output_path: Path for the rendered templates.
    :type output_path: str, optional
    :return: None
    """
    # Set default template and environment if not provided
    if environment is None:
        environment = Environment()
    if template is None:
        template = {"path": "", "file": "", "suffix": "", "type": ""}

    try:
        # Render the template and write the output file.
        environment.loader = FileSystemLoader(template["path"])
        template_file = environment.get_template(template["file"])
        rendered_template = template_file.render(project=project)
        output_basename = Path(roadmap_definition_file).stem
        output_file = os.path.join(
            output_path, f"{output_basename}.{template['suffix']}")
        with open(output_file, "w") as f:
            f.write(rendered_template)

        # If the template is a dot file, try converting it to png
        if template["suffix"] == "dot":
            # first check if we have graphviz installed
            if is_graphviz_installed():
                output_png = os.path.join(
                    output_path, f"{output_basename}.dot.png")
                # log info about converting
                logging.info("rendering '%s' to '%s'", output_file, output_png)
                subprocess.check_call(
                    ['dot', '-Tpng', output_file, '-o', output_png])
            # if 'dot -V' failed, we assume that graphviz is not installed
            else:
                raise EnvironmentError(
                    "graphviz not installed \n"
                    "   dot-template processed\n"
                    "   png rendering skipped \n"
                    "   follow https://www.graphviz.org/ for install instructions")

        logging.info("processed '%s' with template '%s' to '%s'", roadmap_definition_file,
                     os.path.join(template["path"], template["file"]), output_file)

    except Exception as err:
        logging.error("processing template '%s' failed: %s",
                      os.path.join(template["path"], template["file"]), err)


def get_items_grouped_by_date(elements=None):
    """
    Groups items by similar dates, maintaining the original order. If an item has no date attribute,
    it is grouped under "None".

    :param elements: List of items where each item is a dictionary that may contain a "date" key.
    :type elements: list, optional
    :return: A dictionary where keys are dates (or "None") and values are lists of items with those dates.
    :rtype: dict
    """

    # Use default dict to automatically handle the case where a key is not already in the dictionary
    grouped_items = defaultdict(list)

    if elements:
        for item in elements:
            # Use the item's date if it exists, otherwise use "None" and add it to the group
            date = item.get("date", "None")
            grouped_items[date].append(item.copy())

    return dict(grouped_items)


def make_id_from(input_element: str = ""):
    """
    generate id for given input
    strips whitespace, dots etc. from input and make it lowercase
    :param str input_element: input element from which we want to make an id
    :return: str generated id
    """
    # make input lower
    _id = str(input_element).lower()
    # this list contains every non-valid characters, which are replaced by #replacestring
    non_valid_id_characters = [" ", ".", "-", "#", "+", "*"]
    # this is the replacement character
    replacement_character = "_"
    for char in non_valid_id_characters:
        _id = _id.replace(char, replacement_character)
    # replace umlaut
    special_char_map = {
        ord('ä'): 'ae',
        ord('ü'): 'ue',
        ord('ö'): 'oe',
        ord('ß'): 'ss'
    }
    _id = _id.translate(special_char_map)
    return _id


def calculate_cost_of_delay(
        user_business_value: int = None,
        time_criticality: int = None,
        opportunity_enablement_or_risk_reduction: int = None):
    """
    calculate cost of delay for given values according to docs/wsjf.md

    :param int user_business_value: A value between 0 (lowest) and 10 (highest)
    describing, how much the customer (user value) or the company (business value) benefits from the result.
    :param int time_criticality: A value between 0 (lowest) and 10 (highest),
    describing, how time-critical the item ist.
    :param int opportunity_enablement_or_risk_reduction: A value between 0 (lowest) and 10 (highest),
    describing if there is any opportunity enablement or risk reduction by achieving this item.
    :return: cod as integer or None in case of error
    """
    # check if we got integers
    if not isinstance(user_business_value, int):
        raise ValueError("user_business_value is type '" + str(type(user_business_value)) + "' expect int")
    if not isinstance(time_criticality, int):
        raise ValueError("time_criticality is type '" + str(type(time_criticality)) + "' expect int")
    if not isinstance(opportunity_enablement_or_risk_reduction, int):
        raise ValueError("opportunity_enablement_or_risk_reduction is type '" + str(
            type(opportunity_enablement_or_risk_reduction)) + "' expect int")
    # value between 0 (lowest) and 10 (highest)
    if not (0 <= user_business_value <= 10):
        raise ValueError("user_business_value is not value between 0 (lowest) and 10 (highest)")
    # value between 0 (lowest) and 10 (highest)
    if not (0 <= time_criticality <= 10):
        raise ValueError("time_criticality is not value between 0 (lowest) and 10 (highest)")
    # value between 0 (lowest) and 10 (highest)
    if not (0 <= opportunity_enablement_or_risk_reduction <= 10):
        raise ValueError("opportunity_enablement_or_risk_reduction is not value between 0 (lowest) and 10 (highest)")

    return user_business_value + time_criticality + opportunity_enablement_or_risk_reduction


def calculate_weighted_shortest_job_first(
        cost_of_delay: int = None,
        jobsize: int = None):
    """
    calculate wsjf (weighted shortest job first) for given values according to docs/wsjf.md

    wsjf is rounded to 2 digits

    :param int cost_of_delay:
    A value between 0 (lowest) and 30 (highest)
    a measure of the economic value of a job over time
    :param int jobsize:
    value between 1 (shortest) and 10 (longest)
    describing, the approximation of the expected effort
    or statement about how long it takes to deliver the value for a delivery or result
    :return: wsjf as integer or None in case of error
    """
    # check if we got integers
    if not isinstance(cost_of_delay, int):
        raise ValueError("cost_of_delay is type '" + str(type(cost_of_delay)) + "' expect int")
    if not isinstance(jobsize, int):
        raise ValueError("jobsize is type '" + str(type(jobsize)) + "' expect int")
    # value between 0 (lowest) and 30 (highest)
    if not (0 <= cost_of_delay <= 30):
        raise ValueError("cost_of_delay is not value between 0 (lowest) and 30 (highest)")
    # value between 1 (lowest) and 10 (highest)
    if not (1 <= jobsize):
        raise ValueError("jobsize is not value greater 1 (shortest)")

    return round((cost_of_delay / + jobsize), 2)


def calculate_wsjf_quantifiers_for_element_items(elements: dict = None):
    """
    calculate quantifiers for given keyresults or deliverables according to docs/wsjf.md

    add quantifiers.cost_of_delay to element items
    add quantifiers.jobsize to element items
    add quantifiers.wsjf to element items

    weighted_shortest_job_first and cost_of_delay is only added if all values for wsjf are present and valid
    this is jobsize, user_business_value, time_criticality, opportunity_enablement_or_risk_reduction
    in addition: cost_of_delay is only calculated if not set
    in addition: weighted_shortest_job_first is only calculated if not set

    :param dict elements: roadmap element data as dict, e.g. timeline, objectives...
    :return: dict new project with added ["quantifiers"]
    """
    # iterate over each item
    for count, item in enumerate(elements):
        # check if we have quantifiers present in item
        if "quantifiers" in item:
            # try calculating
            try:
                # cost_of_delay is only calculated if not set
                if item["quantifiers"]["cost_of_delay"] is None:
                    item["quantifiers"]["cost_of_delay"] = calculate_cost_of_delay(
                        user_business_value=item["quantifiers"]["user_business_value"],
                        time_criticality=item["quantifiers"]["time_criticality"],
                        opportunity_enablement_or_risk_reduction=item["quantifiers"][
                            "opportunity_enablement_or_risk_reduction"])
            except Exception as err:
                # ignore error - we simply don't add quantifiers to item
                logging.debug("cost_of_delay: calculating failed %s", err)

            try:
                # weighted_shortest_job_first is only calculated if not set
                if item["quantifiers"]["weighted_shortest_job_first"] is None:
                    item["quantifiers"]["weighted_shortest_job_first"] = calculate_weighted_shortest_job_first(
                        cost_of_delay=item["quantifiers"]["cost_of_delay"],
                        jobsize=item["quantifiers"]["jobsize"])
            except Exception as err:
                # ignore error - we simply don't add quantifiers to item
                logging.debug("weighted_shortest_job_first; calculating failed: %s", err)
    return elements.copy()


def calculate_ids_for_element_items(elements: dict = None, prefix: str = "", parent_id: str = ""):
    """
    calculate ids for todos, objectives, keyresults, milestones and deliverables
    add _id field which is cleaned version from id
    add id if id is not present in elements items
    :param dict elements: roadmap element data as dict, e.g. timeline, objectives...
    :param str prefix: prefix for id, used only if id is not set
    :param str parent_id: id of parent element,
    used to make id unique
    it is used to make a prefix before _id
    :return: dict new project with added ["_id"] and ["id]
    """

    # this is the id of the element before current element in a list - already used during dot-processing
    _previous_id = ""

    # this should be the id of the element after current element in a list - it is not used nor calculated
    # _next_id = ""

    # let's iterate over each element and add "id", "_id" and "_parent_id"
    # because we like to have a human-readable id, we start at 1
    for count, item in enumerate(elements, start=1):
        # item.id will get prefix and count, if unset
        if "id" not in item or item["id"] == "":
            item["id"] = prefix + str(count)

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
            item["keyresults"] = calculate_wsjf_quantifiers_for_element_items(item["keyresults"])
        if "deliverables" in item:
            item["deliverables"] = calculate_ids_for_element_items(item["deliverables"], "D", parent_id=_parent_id)
            item["deliverables"] = calculate_wsjf_quantifiers_for_element_items(item["deliverables"])
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


def remove_element(element_name: str = "", project: dict = None):
    """
    Remove given element from project - we are working with project by reference

    TODO: this function is working but need refactoring - is way to much redundancy in the code base

    element can be any kind of object or attribute

    support 5 levels, which is the maximum number in our supported schema

    the deepest level is e.g. 'objectives.milestones.deliverables.todos.description'

    :param str element_name: roadmap element name as dotted path,
    e.g. 'objectives.milestones.deliverables.todos.description'

    :param dict project: reference of project

    :return: Nothing
    """
    # first, we remove whitespaces and make everything lowercase
    element_name = element_name.replace(" ", "").lower()
    # element_name has to contain a minimum of xx characters / based on elements of roadmap.schema 'logo' is minimum
    if len(element_name) >= 4:
        # level is the number of dots as indicator for skipping based on roadmap.schema hierarchy
        remove_level = element_name.count(".") - 0
        if remove_level == 0:
            # example element_name is: milestones
            level0_element = element_name
            if level0_element in project:
                logging.info("skip level %s (project.%s)", remove_level, element_name)
                del project[level0_element]
        elif remove_level == 1:
            # example element_name is: milestones.deliverables
            level0_element = element_name.split(".")[0]
            level1_element = element_name.split(".")[1]
            logging.info("skip level %s (project.%s)", remove_level, element_name)

            if level0_element in project:
                for project_level0_element in project[level0_element]:
                    if level1_element in project_level0_element:
                        del project_level0_element[level1_element]
        elif remove_level == 2:
            # example element_name is: milestones.deliverables.todos
            level0_element = element_name.split(".")[0]
            level1_element = element_name.split(".")[1]
            level2_element = element_name.split(".")[2]

            if level0_element in project:
                for project_level0_element in project[level0_element]:
                    if level1_element in project_level0_element:
                        for project_level1_element in project_level0_element[level1_element]:
                            if level2_element in project_level1_element:
                                logging.info("skip level %s (project.%s)", remove_level, element_name)
                                del project_level1_element[level2_element]
        elif remove_level == 3:
            # example element_name is: milestones.deliverables.todos.description
            level0_element = element_name.split(".")[0]
            level1_element = element_name.split(".")[1]
            level2_element = element_name.split(".")[2]
            level3_element = element_name.split(".")[3]
            if level0_element in project:
                for project_level0_element in project[level0_element]:
                    if level1_element in project_level0_element:
                        for project_level1_element in project_level0_element[level1_element]:
                            if level2_element in project_level1_element:
                                for project_level2_element in project_level1_element[level2_element]:
                                    if level3_element in project_level2_element:
                                        logging.info("skip level %s (project.%s)", remove_level, element_name)
                                        # if element is string, we could not easy del, so we just set it to none
                                        if isinstance(project_level2_element, str):
                                            project_level1_element[level2_element][level3_element] = None
                                        else:
                                            del project_level2_element[level3_element]
        elif remove_level == 4:
            # example element_name is: objectives.milestones.deliverables.todos.description
            level0_element = element_name.split(".")[0]
            level1_element = element_name.split(".")[1]
            level2_element = element_name.split(".")[2]
            level3_element = element_name.split(".")[3]
            level4_element = element_name.split(".")[4]

            if level0_element in project:
                for project_level0_element in project[level0_element]:
                    if level1_element in project_level0_element:
                        for project_level1_element in project_level0_element[level1_element]:
                            if level2_element in project_level1_element:
                                for project_level2_element in project_level1_element[level2_element]:
                                    if level3_element in project_level2_element:
                                        for project_level3_element in project_level2_element[level3_element]:
                                            if level4_element in project_level3_element:
                                                logging.info("skip level %s (project.%s)", remove_level, element_name)
                                                del project_level3_element[level4_element]

        else:
            logging.warning("skip level %s (project.%s) is not supported", remove_level, element_name)
    else:
        raise ValueError("element_name is to short for removing")


def calculate_roadmap_version(path_to_roadmap_yml: str = ""):
    """
    Calculate a version of roadmap.yml

    version is calculated using md5 of the roadmap.yml and
    id contains the first and last 4 characters of md5 hash as a version

    note: part of this code is from https://stackoverflow.com/questions/1131220/get-the-md5-hash-of-big-files-in-python

    :param str path_to_roadmap_yml: path/to/roadmap.yml
    :return: md5sum of roadmap.yml
    :rtype: string of md5 or None in case of error
    """
    try:
        # we use the whole file and open in binary
        with open(path_to_roadmap_yml, "rb") as f:
            # init hashlib for md5 hashing
            file_hash = hashlib.md5()
            # we only read chunks of the file to fill in the MD5 128-byte digest blocks
            # chunk mechanic prevent us from using too much memory
            while chunk := f.read(8192):
                # update the hash with chunk data
                file_hash.update(chunk)
            # get the hash as string
            version_hash = file_hash.hexdigest()
        # version uses first and last 4 characters from hash
        version = version_hash[0:4] + version_hash[-4:]
        return version
    except Exception:
        return None


def get_key_value_list(element=None, key_value_list: list = None, prefix_for_key: str = None, keep_index=False):
    """
    iterate over all given elements and make a key value list containing each element key and value

    the key is build in form of the elements:
    - milestones.title
    - milestones.description
    - milestones.deliverables.title
    - milestones.deliverables.title
    and so on

    if you set keep_index to True, the keys are build like
    - milestones.0.title
    - milestones.0.description
    - milestones.0.deliverables.0.title
    - milestones.0.deliverables.1.title

    the ordering from element is kept

    :param Any element: anything you like to make a flat list
    :param list key_value_list: an optional list, we have to append our key value pairs
    :param str prefix_for_key: prefix_for_key is used to prefix the key in the result list
    :param bool keep_index: if true, key contains loop index of all dict and list elements

    :return: list with key/value pairs as dict for given elements
    """
    # add dot to prefix if prefix is given and there is no dot present
    if prefix_for_key is None:
        prefix_for_key = ""
    elif prefix_for_key is not None and prefix_for_key[-1] != ".":
        prefix_for_key += "."

    # make shure to have a list
    if key_value_list is None:
        key_value_list = list()

    # if we get a list
    if isinstance(element, list):
        # iterate over list
        for index, item in enumerate(element):
            if isinstance(item, dict):
                # should we add index to prefix?
                if keep_index:
                    sub_prefix = prefix_for_key + str(index)
                else:
                    sub_prefix = prefix_for_key
                # if we got a dict we recall this function
                get_key_value_list(element=item,
                                   prefix_for_key=sub_prefix,
                                   key_value_list=key_value_list,
                                   keep_index=keep_index)
    elif isinstance(element, dict):
        # iterate over dict
        for index, key in enumerate(element.keys()):
            # make a sub-prefix for this element
            sub_prefix = prefix_for_key + str(key)

            # we got an element
            if not isinstance(element[key], (list, dict, tuple)):
                key_value_list.append({'key': sub_prefix,
                                       'value': element[key]})
            # we got a list,dict or tuple, so we have to go further into the element
            else:
                get_key_value_list(element=element[key],
                                   prefix_for_key=sub_prefix,
                                   key_value_list=key_value_list,
                                   keep_index=keep_index)
                # we got our value
    else:
        # remove the dot from prefix
        if len(prefix_for_key) >= 1 and prefix_for_key[-1] == ".":
            prefix_for_key = prefix_for_key[:-1]
        # we need SOME key, so we use none if prefix is not present
        # this is, because we set prefix = "" if it is none
        if prefix_for_key == "":
            prefix_for_key = None
        # add element to the list
        key_value_list.append({'key': prefix_for_key, 'value': element})

    # return a copy of our list
    return key_value_list.copy()


def get_filtered_key_value_list(element=None, key_value_list: list = None, prefix_for_key: str = None,
                                filter_for_keys: str = "", precise_search: bool = True):
    """
    filter elements by filter_for_keys

    you can use this, to filter the key_value list using certain criteria
    e.g. to get all todos
    - set filter_for_keys = ".todos."
    - set precise_search = False

    the ordering from element is kept

    :param Any element: anything you like to make a flat list
    :param list key_value_list: an optional list, we have used as our list,
    if not given, we build list for ourselves from element
    it is not useful to have a list which is build with keep_index!
    :param str prefix_for_key: prefix_for_key is used to prefix the key in the result list if key_value_list is None,
     and we have to build the list ourselves from element
    :param str filter_for_keys: a string separated by comma like "skip_items", to filter items,
    e.g. milestones.todos,milestones.deliverables.todos
    :param bool precise_search: if true, the exact strings from filter_keys are searched,
    if false, we look if any filter_key is part of key

    :return: list with key/value pairs as dict for given elements
    """
    # we need a key_value list without index
    if key_value_list is None and element is not None:
        key_value_list = get_key_value_list(element=element, key_value_list=None, prefix_for_key=prefix_for_key,
                                            keep_index=False)
    elif key_value_list is None and element is None:
        raise ValueError("neither 'key_value_list' nor 'element' is present")

    # our result list
    filtered_key_value_list = list()
    # we iterate over the filter_keys
    for filter_item in filter_for_keys.split(","):
        # let's remove any whitespaces just for convenience
        filter_key = filter_item.strip(" ")
        # we iterate over our original list
        for item in key_value_list:
            # make shure we have 'key' in our list
            if 'key' in item:
                if precise_search:
                    # check the exact key
                    if item["key"] == filter_key:
                        filtered_key_value_list.append(item)
                else:
                    if filter_key in item["key"]:
                        filtered_key_value_list.append(item)

    return filtered_key_value_list.copy()


# This function parses command-line arguments using the argparse module.
def parse_commandline_args(parser):
    # Add optional argument for specifying the path to the roadmap YAML file:
    parser.add_argument("--roadmap-file", "-rf", type=str,
                        help="path to roadmap.yml", nargs="?", default="examples/roadmap.yml")
    # Add optional argument for specifying the output directory for rendered results:
    parser.add_argument("--output-dir", "-out", type=str,
                        help="path to rendered output", nargs="?", default="roadmap/")
    # Add optional argument for skipping specific roadmap elements during rendering:
    parser.add_argument("--skip-items", "-skip",
                        type=str,
                        help="object path of roadmap-elements which should be skipped for rendering, separated by comma"
                             " e.g.: milestones.todos,milestones.deliverables.todos ",
                        nargs="?",
                        default=None)
    # Add optional argument for specifying an environment file containing paths to schema definitions, logfile, etc.:
    parser.add_argument("--environment", "-env",
                        type=str,
                        help="environment file containing paths to the schema definitions, logfile, etc.",
                        nargs="?",
                        default="roadmap.env")
    # Parse the arguments and return the parsed argument object:
    args = parser.parse_args()
    return args


def convert_image_to_html_base64(image_filename:str = ""):
    """
    Converts an image file in the given path to html compatible base64 string

    :param image_filename: full path to image file
    :return: string as html base64 string usable in img-src-tag
    """
    try:
        data = open(image_filename, 'rb').read()  # read bytes from file
        data_base64 = base64.b64encode(data)  # encode to base64 (bytes)
        data_base64 = data_base64.decode()  # convert bytes to string
        image_type = Path(image_filename).suffix[1:]
        return "data:image/" + image_type + ";base64," + data_base64
    except FileNotFoundError:
        logging.error("Could not open image" + image_filename)
        return ""


def main():
    # Init
    parser = argparse.ArgumentParser(description="Process command line arguments.")
    args = parse_commandline_args(parser)

    roadmap_definition_file = args.roadmap_file
    output_folder = args.output_dir
    skip_items = args.skip_items
    environment_definition_file = args.environment

    if not os.path.exists(roadmap_definition_file):
        raise ValueError("Roadmap file not found!")
    if not os.path.exists(environment_definition_file):
        raise ValueError("Environment file not found!")

    # Load Config from environment definition
    config = dotenv_values(environment_definition_file)

    # basic logging is file-based with level DEBUG and above and with timestamp
    logging.basicConfig(filename=config["LOGFILE"], encoding='utf-8', level=logging.DEBUG,
                        format='%(asctime)s [%(levelname)s] %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

    # handler for stdout
    console_log_handler = logging.StreamHandler(sys.stdout)
    # console format
    console_log_format = logging.Formatter('%(levelname)s: %(message)s')
    console_log_handler.setFormatter(console_log_format)
    # stdout logging is level INFO or above, without timestamp
    console_log_handler.setLevel(logging.INFO)
    logging.getLogger().addHandler(console_log_handler)

    # log config
    logging.debug("config: %s", config)

    if output_folder[-1] != os.sep:
        output_folder = output_folder + os.sep

    if create_output_folder(output_folder):
        # Read Roadmap-Definition
        project = read_roadmap_definition(
            path_to_roadmap_yml=roadmap_definition_file)

        validation_error, is_valid_yaml = validate_yaml(
            roadmap_data=project, path_to_json_schema=config["SCHEMA"])

        if is_valid_yaml:
            # add some version
            project['meta'] = {
                "version": calculate_roadmap_version(path_to_roadmap_yml=roadmap_definition_file),
                "rendertime": time.strftime("%Y%m%d%H%M%S")
            }
            logging.info("version of roadmap.yml is '%s'", project['meta']["version"])
            logging.info("rendering time '%s'", project['meta']["rendertime"])

            # Find all templates
            templates = find_templates(template_path=config["TEMPLATE_PATH"],
                                       template_known_suffixes=config["TEMPLATE_KNOWN_SUFFIXES"])
            # do some preprocessing
            if skip_items is not None:
                for skip in skip_items.replace(" ", "").split(","):
                    remove_element(skip, project=project)

            # add same placeholder for grouping - will be removed if not needed
            project["group"] = {
                "timeline_by": {
                    "date": None
                },
                "objectives_by": {
                    "date": None
                }
            }
            # Calculate some information to project
            # add _id, id, _parent_id and _previous_id
            if "timeline" in project:
                project['timeline'] = calculate_ids_for_element_items(project['timeline'], prefix="Timeline")
                # add items grouped by date
                project["group"]['timeline_by']['date'] = get_items_grouped_by_date(project["timeline"])
            # remove placeholder for grouping
            else:
                del project["group"]['timeline_by']

            if "objectives" in project:
                project['objectives'] = calculate_ids_for_element_items(project['objectives'], prefix="O")
                # add items grouped by date
                project["group"]['objectives_by']['date'] = get_items_grouped_by_date(project["objectives"])
            # remove placeholder for grouping
            else:
                del project["group"]['objectives_by']

            if "milestones" in project:
                project['milestones'] = calculate_ids_for_element_items(project['milestones'], prefix="M")
            if "releases" in project:
                project['releases'] = calculate_ids_for_element_items(project['releases'], prefix="Release")

            # do some postprocessing to enable skipping calculated elements
            # we use the same skip_items from preprocessing
            if skip_items is not None:
                for skip in skip_items.replace(" ", "").split(","):
                    remove_element(skip, project=project)

            # add our project as a key_value list
            project["as_list"] = get_key_value_list(element=project)

            # process templates with jinja
            # Load Jinja Environment
            env = Environment()
            # Add some extensions for jinja
            env.add_extension(MarkdownExtension)
            # convert logo to make it embeddable in the html template
            if "logo" in project:
                # create path
                logo_src_path = os.path.join(Path(roadmap_definition_file).parent.absolute(
                ).resolve(), project["logo"]["filename"])
                project["logo"]["base64"] = convert_image_to_html_base64(logo_src_path)

            for template in templates:
                logging.info("processing '%s'", os.path.join(template["path"], template["file"]))
                process_template(environment=env, template=template, roadmap_definition_file=roadmap_definition_file,
                                 project=project, output_path=output_folder)

            # Copy logo to output path if it exists in the project
            if "logo" in project:
                # create path
                logo_src_path = os.path.join(Path(roadmap_definition_file).parent.absolute(
                ).resolve(), project["logo"]["filename"])
                # log info
                logging.info("copy project.logo '%s' to '%s'", logo_src_path, output_folder)
                # copy
                try:
                    shutil.copy(logo_src_path, output_folder)
                except shutil.SameFileError:
                    logging.debug("copy logo file '%s' failed",
                                  logo_src_path)

            logging.info("roadmap conversion finished")

        else:
            logging.error(roadmap_definition_file + " contains no valid YAML-data - see logfile for details")
    else:
        logging.error("could not create '" + output_folder + "' - see logfile for details")


if __name__ == "__main__":
    main()

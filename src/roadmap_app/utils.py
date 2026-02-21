import yaml
import logging
import hashlib
import base64
from pathlib import Path


def read_yml_to_dict(path_to_yml: str = ""):
    """
    Read some yml file and return this as a dict

    Return Dict: if conversion to dict was successfully
    Return None: if conversion failed

    :param str path_to_yml: path/to/your.yml
    :return: dict on Success, None on Error
    :rtype: dict
    """
    try:
        with open(path_to_yml, "r") as f:
            yml_content = yaml.load(f, Loader=yaml.FullLoader)
            logging.debug("yml_content: %s", yml_content)
            return yml_content
    except OSError as err:
        # in case of an error log file name and error message
        logging.debug("yml-definition-file '%s' not readable", path_to_yml)
        logging.debug("Error: %s", err.strerror)
        raise err


def read_roadmap_definition(path_to_roadmap_yml: str = ""):
    """
    Read the Roadmap-Definition-YML

    Return Dict: if conversion to dict was successfully
    Return None: if conversion failed

    :param str path_to_roadmap_yml: path/to/roadmap.yml
    :return: dict on Success, None on Error
    :rtype: dict
    """
    return read_yml_to_dict(path_to_yml=path_to_roadmap_yml)


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

    # make sure to have a list
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
            # make sure we have 'key' in our list
            if 'key' in item:
                if precise_search:
                    # check the exact key
                    if item["key"] == filter_key:
                        filtered_key_value_list.append(item)
                else:
                    if filter_key in item["key"]:
                        filtered_key_value_list.append(item)

    return filtered_key_value_list.copy()


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
    except OSError:
        return None


def convert_image_to_html_base64(image_filename: str = ""):
    """
    Converts an image file in the given path to html compatible base64 string

    :param image_filename: full path to image file
    :return: string as html base64 string usable in img-src-tag
    """
    try:
        with open(image_filename, 'rb') as f:
            data = f.read()
        data_base64 = base64.b64encode(data).decode()
        image_type = Path(image_filename).suffix[1:]
        return f"data:image/{image_type};base64,{data_base64}"
    except FileNotFoundError:
        logging.error(f"Could not open image {image_filename}")
        return ""


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

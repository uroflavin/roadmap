import logging
import time
from collections import defaultdict

from .utils import calculate_roadmap_version, get_key_value_list


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
        raise ValueError(f"user_business_value is type '{type(user_business_value)}' expect int")
    if not isinstance(time_criticality, int):
        raise ValueError(f"time_criticality is type '{type(time_criticality)}' expect int")
    if not isinstance(opportunity_enablement_or_risk_reduction, int):
        raise ValueError(f"opportunity_enablement_or_risk_reduction is type '{type(opportunity_enablement_or_risk_reduction)}' expect int")
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
        raise ValueError(f"cost_of_delay is type '{type(cost_of_delay)}' expect int")
    if not isinstance(jobsize, int):
        raise ValueError(f"jobsize is type '{type(jobsize)}' expect int")
    # value between 0 (lowest) and 30 (highest)
    if not (0 <= cost_of_delay <= 30):
        raise ValueError("cost_of_delay is not value between 0 (lowest) and 30 (highest)")
    # value between 1 (lowest) and 10 (highest)
    if not (1 <= jobsize):
        raise ValueError("jobsize is not value greater 1 (shortest)")

    return round((cost_of_delay / jobsize), 2)


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
            except (KeyError, TypeError, ValueError) as err:
                # ignore error - we simply don't add quantifiers to item
                logging.debug("cost_of_delay: calculating failed %s", err)

            try:
                # weighted_shortest_job_first is only calculated if not set
                if item["quantifiers"]["weighted_shortest_job_first"] is None:
                    item["quantifiers"]["weighted_shortest_job_first"] = calculate_weighted_shortest_job_first(
                        cost_of_delay=item["quantifiers"]["cost_of_delay"],
                        jobsize=item["quantifiers"]["jobsize"])
            except (KeyError, TypeError, ValueError) as err:
                # ignore error - we simply don't add quantifiers to item
                logging.debug("weighted_shortest_job_first; calculating failed: %s", err)
    return elements.copy()


# Mapping of child element keys to their ID prefixes
_CHILD_ELEMENT_PREFIXES = {
    "keyresults": "R",
    "deliverables": "D",
    "objectives": "O",
    "milestones": "M",
    "todos": "TODO",
    "timeline": "timeline",
    "releases": "Release",
}

# Elements that get WSJF quantifiers calculated
_WSJF_ELEMENTS = {"keyresults", "deliverables"}


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

        # check each dict-object and calculate the id's and quantifiers
        for key, child_prefix in _CHILD_ELEMENT_PREFIXES.items():
            if key in item:
                item[key] = calculate_ids_for_element_items(item[key], child_prefix, parent_id=_parent_id)
                if key in _WSJF_ELEMENTS:
                    item[key] = calculate_wsjf_quantifiers_for_element_items(item[key])

    return elements.copy()


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


def remove_element(element_name: str = "", project: dict = None):
    """
    Remove given element from project - we are working with project by reference

    element can be any kind of object or attribute

    supports arbitrary nesting depth

    the deepest level is e.g. 'objectives.milestones.deliverables.todos.description'

    :param str element_name: roadmap element name as dotted path,
    e.g. 'objectives.milestones.deliverables.todos.description'

    :param dict project: reference of project

    :return: Nothing
    """
    # first, we remove whitespaces and make everything lowercase
    element_name = element_name.replace(" ", "").lower()
    # element_name has to contain a minimum of xx characters / based on elements of roadmap.schema 'logo' is minimum
    if len(element_name) < 4:
        raise ValueError("element_name is to short for removing")

    parts = element_name.split(".")

    def _remove(data, keys):
        if len(keys) == 1:
            # direct removal from a dict (reached via list iteration or top level)
            if isinstance(data, dict) and keys[0] in data:
                logging.info("skip (project.%s)", element_name)
                del data[keys[0]]
            return

        if not isinstance(data, dict) or keys[0] not in data:
            return

        child = data[keys[0]]
        if isinstance(child, list):
            for item in child:
                _remove(item, keys[1:])
        elif isinstance(child, dict):
            # when the parent is a dict (not a list), set leaf values to None
            if len(keys) == 2:
                if keys[1] in child:
                    logging.info("skip (project.%s)", element_name)
                    child[keys[1]] = None
            else:
                _remove(child, keys[1:])

    _remove(project, parts)


def enrich_project(project, skip_items, roadmap_definition_file):
    """
    Enrich the project dict with computed fields:
    - meta (version, rendertime)
    - IDs for all elements
    - WSJF quantifiers
    - grouped items by date
    - flattened key-value list

    :param dict project: roadmap data as dict
    :param str skip_items: comma-separated dotted paths of elements to skip
    :param str roadmap_definition_file: path to roadmap.yml (for version calculation)
    """
    # add version and rendertime
    project['meta'] = {
        "version": calculate_roadmap_version(path_to_roadmap_yml=roadmap_definition_file),
        "rendertime": time.strftime("%Y%m%d%H%M%S")
    }
    logging.info("version of roadmap.yml is '%s'", project['meta']["version"])
    logging.info("rendering time '%s'", project['meta']["rendertime"])

    # placeholders for grouping - will be removed if section is absent
    project["group"] = {
        "timeline_by": {"date": None},
        "objectives_by": {"date": None}
    }

    # calculate IDs and group by date
    if "timeline" in project:
        project['timeline'] = calculate_ids_for_element_items(project['timeline'], prefix="Timeline")
        project["group"]['timeline_by']['date'] = get_items_grouped_by_date(project["timeline"])
    else:
        del project["group"]['timeline_by']

    if "objectives" in project:
        project['objectives'] = calculate_ids_for_element_items(project['objectives'], prefix="O")
        project["group"]['objectives_by']['date'] = get_items_grouped_by_date(project["objectives"])
    else:
        del project["group"]['objectives_by']

    if "milestones" in project:
        project['milestones'] = calculate_ids_for_element_items(project['milestones'], prefix="M")
    if "releases" in project:
        project['releases'] = calculate_ids_for_element_items(project['releases'], prefix="Release")

    # remove skipped elements after all enrichment is complete
    if skip_items is not None:
        for skip in skip_items.replace(" ", "").split(","):
            remove_element(skip, project=project)

    # flatten project to key-value list
    project["as_list"] = get_key_value_list(element=project)

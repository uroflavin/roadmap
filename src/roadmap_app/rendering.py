import json
import os
import logging
import subprocess
import jsonschema
from jsonschema import validate
from jinja2 import FileSystemLoader, Environment, TemplateError
from pathlib import Path

from .utils import read_yml_to_dict


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


def _resolve_output_paths(output_name: str, global_output_path: str):
    """
    Resolve output file path and directory from an output name.

    :param str output_name: output filename, may contain subdirectories (e.g. 'kanban/milestones.html')
    :param str global_output_path: global directory for template-rendering-output
    :return: tuple of (output_file, output_file_path, output_file_basename)
    :rtype: tuple
    """
    if os.sep in output_name:
        output_parts = output_name.split(os.sep)
        output_file_path = (Path(global_output_path + os.sep + os.sep.join(output_parts[0:-1]))
                            .resolve().absolute().as_posix())
        output_file = (Path(output_file_path + os.sep + output_parts[-1])
                       .resolve().absolute().as_posix())
    else:
        output_file_path = Path(global_output_path).absolute().as_posix()
        output_file = (Path(output_file_path + os.sep + output_name)
                       .resolve().absolute().as_posix())
    output_file_basename = Path(output_name).stem
    return output_file, output_file_path, output_file_basename


def _find_templates_from_manifest(template_path, template_known_suffixes, global_output_path):
    """
    Load templates from a templates.yml manifest file.

    :param str template_path: directory containing templates
    :param list template_known_suffixes: list of known suffixes for templates
    :param str global_output_path: global directory for template-rendering-output
    :return: list of template dicts
    :rtype: list
    """
    templates = []
    template_yml = Path(template_path + os.sep + "templates.yml")

    templates_from_yml = read_yml_to_dict(template_yml.absolute())

    if not isinstance(templates_from_yml, list):
        logging.error("templates.yml must be a list of template entries")
        return templates

    for template in templates_from_yml:
        if not isinstance(template, dict) or "input" not in template or "output" not in template:
            logging.warning("skipping invalid template entry (missing 'input' or 'output'): %s", template)
            continue

        input_file = Path(template_path + os.sep + template["input"]).absolute().resolve()
        input_file_suffix = input_file.suffix.replace(".", "")
        input_file_type = input_file.parts[-2]
        input_file_path = Path(template_path + os.sep + input_file_type).absolute().resolve().as_posix()

        output_file, output_file_path, output_file_basename = _resolve_output_paths(
            template["output"], global_output_path)

        if input_file_suffix in template_known_suffixes:
            templates.append({
                "path": input_file_path,
                "file": input_file.name,
                "output_file": output_file,
                "output_file_basename": output_file_basename,
                "output_path": output_file_path,
                "suffix": input_file_suffix,
                "type": input_file_type
            })

    return templates


def _find_templates_from_directory(template_path, template_known_suffixes, global_output_path):
    """
    Find templates by walking the template directory (backward compatibility fallback).

    Looks for files matching 'roadmap.<suffix>' pattern.

    :param str template_path: directory containing templates
    :param list template_known_suffixes: list of known suffixes for templates
    :param str global_output_path: global directory for template-rendering-output
    :return: list of template dicts
    :rtype: list
    """
    templates = []

    for dirname, dir_names, filenames in os.walk(template_path):
        for file in filenames:
            file_parts = file.split(".")

            input_file = Path(file).absolute().resolve()
            input_file_suffix = input_file.suffix.replace(".", "")

            output_file, output_file_path, output_file_basename = _resolve_output_paths(
                file, global_output_path)

            if len(file_parts) == 2 and file_parts[0] == "roadmap":
                file_suffix = file_parts[1]
                if file_suffix in template_known_suffixes:
                    templates.append({
                        "path": dirname + os.sep,
                        "file": file,
                        "output_file": output_file,
                        "output_file_basename": output_file_basename,
                        "output_path": output_file_path,
                        "suffix": input_file_suffix,
                        "type": dirname.split("/")[1]
                    })

    return templates


def find_templates(template_path: str = "", template_known_suffixes: list = None, global_output_path: str = ""):
    """
    Find all templates in given template_path.

    If a templates.yml manifest exists, it is validated and used as the
    source of template definitions. Each entry must be a dict with at least
    'input' and 'output' keys. Invalid entries are logged and skipped.
    If no manifest exists, the template_path is walked for backward compatibility.

    :param str template_path: directory containing templates
    :param list template_known_suffixes: list of known suffixes for templates, e.g. html, md, txt
    :param str global_output_path: global directory for template-rendering-output
    :return: templates
    :rtype: list
    """
    template_yml = Path(template_path + os.sep + "templates.yml")

    if template_yml.is_file():
        templates = _find_templates_from_manifest(template_path, template_known_suffixes, global_output_path)
    else:
        templates = _find_templates_from_directory(template_path, template_known_suffixes, global_output_path)

    logging.debug("templates: %s", templates)
    return templates


def process_template(
        environment: Environment = None,
        template: dict = None,
        roadmap_definition_file: str = "",
        project=None
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
    :return: None
    """
    # Set default template and environment if not provided
    if environment is None:
        environment = Environment()
    if template is None:
        raise ValueError("Template file not given!")

    try:
        # Render the template and write the output file.
        search_paths = [template["path"]]
        # Add html/ sibling directory as fallback for shared assets (CSS, JS)
        html_path = str(Path(template["path"]).parent / "html")
        if html_path != template["path"] and Path(html_path).is_dir():
            search_paths.append(html_path)
        environment.loader = FileSystemLoader(search_paths)
        template_file = environment.get_template(template["file"])
        rendered_template = template_file.render(project=project)
        output_basename = template["output_file_basename"]
        output_file = template["output_file"]
        output_path = template["output_path"]

        # create directory
        if not Path(output_path).exists():
            Path(output_path).mkdir(parents=True, exist_ok=True)

        with open(output_file, "w") as f:
            f.write(rendered_template)

        # If the template is a dot file, try converting it to png
        if template["suffix"] == "dot":
            # first check if we have graphviz installed
            if is_graphviz_installed():
                output_png = os.path.join(
                    template["output_path"], f"{output_basename}.dot.png")
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

    except (TemplateError, OSError, subprocess.CalledProcessError) as err:
        logging.error("processing template '%s' failed: %s",
                      os.path.join(template["path"], template["file"]), err)

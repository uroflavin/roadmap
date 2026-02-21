import json
import os
import sys
import logging
import argparse
import shutil

from jinja2 import Environment
from jinja_markdown import MarkdownExtension
from dotenv import dotenv_values
from pathlib import Path

from .utils import read_roadmap_definition, convert_image_to_html_base64, create_output_folder
from .model import enrich_project
from .rendering import validate_yaml, find_templates, process_template


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
                        default="config/roadmap.env")
    # Parse the arguments and return the parsed argument object:
    args = parser.parse_args()
    return args


def setup_logging(config):
    """
    Configure file-based and console logging.

    File logging: DEBUG level with timestamps.
    Console logging: INFO level without timestamps.

    :param dict config: configuration dictionary containing LOGFILE path
    """
    logging.basicConfig(filename=config["LOGFILE"], encoding='utf-8', level=logging.DEBUG,
                        format='%(asctime)s [%(levelname)s] %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

    console_log_handler = logging.StreamHandler(sys.stdout)
    console_log_format = logging.Formatter('%(levelname)s: %(message)s')
    console_log_handler.setFormatter(console_log_format)
    console_log_handler.setLevel(logging.INFO)
    logging.getLogger().addHandler(console_log_handler)


def render_templates(project, config, output_folder, roadmap_definition_file):
    """
    Discover templates, render them with Jinja2, and handle logo embedding/copying.

    :param dict project: enriched roadmap project data
    :param dict config: configuration dictionary with TEMPLATE_PATH and TEMPLATE_KNOWN_SUFFIXES
    :param str output_folder: path to output directory
    :param str roadmap_definition_file: path to the roadmap YAML file
    """
    template_known_suffixes = json.loads(config["TEMPLATE_KNOWN_SUFFIXES"])
    templates = find_templates(template_path=config["TEMPLATE_PATH"],
                               template_known_suffixes=template_known_suffixes,
                               global_output_path=output_folder)

    env = Environment()
    env.add_extension(MarkdownExtension)

    # convert logo to make it embeddable in the html template
    logo_src_path = None
    if "logo" in project:
        logo_src_path = os.path.join(Path(roadmap_definition_file).parent.absolute(
        ).resolve(), project["logo"]["filename"])
        project["logo"]["base64"] = convert_image_to_html_base64(logo_src_path)

    for template in templates:
        logging.info(f"processing '{os.path.join(template['path'], template['file'])}'")
        process_template(environment=env, template=template, roadmap_definition_file=roadmap_definition_file,
                         project=project)

    # Copy logo to output path if it exists in the project
    if logo_src_path:
        logging.info(f"copy project.logo '{logo_src_path}' to '{output_folder}'")
        try:
            shutil.copy(logo_src_path, output_folder)
        except shutil.SameFileError:
            logging.debug(f"copy logo file '{logo_src_path}' failed")


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

    setup_logging(config)
    logging.debug(f"config: {config}")

    if output_folder[-1] != os.sep:
        output_folder = f"{output_folder}{os.sep}"

    if not create_output_folder(output_folder):
        logging.error(f"could not create '{output_folder}' - see logfile for details")
        return

    # Read Roadmap-Definition
    project = read_roadmap_definition(path_to_roadmap_yml=roadmap_definition_file)

    validation_error, is_valid_yaml = validate_yaml(
        roadmap_data=project, path_to_json_schema=config["SCHEMA"])

    if not is_valid_yaml:
        logging.error(f"{roadmap_definition_file} contains no valid YAML-data - see logfile for details")
        return

    # Enrich project data (IDs, WSJF, grouping, flat list)
    enrich_project(project, skip_items, roadmap_definition_file)

    render_templates(project, config, output_folder, roadmap_definition_file)
    logging.info("roadmap conversion finished")

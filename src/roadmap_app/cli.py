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
            # Enrich project data (IDs, WSJF, grouping, flat list)
            enrich_project(project, skip_items, roadmap_definition_file)

            # Find all templates
            templates = find_templates(template_path=config["TEMPLATE_PATH"],
                                       template_known_suffixes=config["TEMPLATE_KNOWN_SUFFIXES"],
                                       global_output_path=output_folder)

            # process templates with jinja
            env = Environment()
            env.add_extension(MarkdownExtension)

            # convert logo to make it embeddable in the html template
            logo_src_path = None
            if "logo" in project:
                logo_src_path = os.path.join(Path(roadmap_definition_file).parent.absolute(
                ).resolve(), project["logo"]["filename"])
                project["logo"]["base64"] = convert_image_to_html_base64(logo_src_path)

            for template in templates:
                logging.info("processing '%s'", os.path.join(template["path"], template["file"]))
                process_template(environment=env, template=template, roadmap_definition_file=roadmap_definition_file,
                                 project=project)

            # Copy logo to output path if it exists in the project
            if logo_src_path:
                logging.info("copy project.logo '%s' to '%s'", logo_src_path, output_folder)
                try:
                    shutil.copy(logo_src_path, output_folder)
                except shutil.SameFileError:
                    logging.debug("copy logo file '%s' failed",
                                  logo_src_path)

            logging.info("roadmap conversion finished")

        else:
            logging.error(f"{roadmap_definition_file} contains no valid YAML-data - see logfile for details")
    else:
        logging.error(f"could not create '{output_folder}' - see logfile for details")

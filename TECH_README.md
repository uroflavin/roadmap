# Roadmap Script

This script is used for creating and validating roadmap files. It uses YAML for reading and writing roadmap files, JSON for reading and writing JSON files, and jsonschema for validating JSON data against a schema. It also uses the os module for interacting with the operating system, argparse for writing user-friendly command-line interfaces, and shutil for high-level file operations.

## Setting Up a Virtual Environment

Before running the script, you should set up a virtual environment. This helps to keep the dependencies required by different projects separate by creating isolated python environments for them. Here's how you can do it:

1. Install the `virtualenv` package:
    ```bash
    pip install virtualenv
    ```

2. Navigate to the project directory and create a virtual environment. You can name the environment anything you like. Here we name it `env`:
    ```bash
    cd path/to/project/directory
    virtualenv env
    ```

3. Activate the virtual environment:
    - On Windows, run: `env\Scripts\activate`
    - On Unix or MacOS, run: `source env/bin/activate`

4. Once the virtual environment is activated, the name of your virtual environment will appear on left side of terminal.

## Installing Dependencies

The dependencies of the script are listed in the `requirements.txt` file. After activating the virtual environment, you can use the following command to install these dependencies:

```bash
pip install -r requirements.txt
```

## Parameters
--roadmap-file: This parameter is used to specify the path to the roadmap YAML file that you want to read. The function read_roadmap_definition is used to read this file. If the file is not readable, an error will be logged and None will be returned.

--output-dir: This parameter is used to specify the path to the folder where the output of the roadmap.py script will be stored. The function create_output_folder is used to create this folder if it does not exist. If the folder is not writable, an error will be logged and False will be returned.

## Usage
You can run the script from the command line as follows:

```bash
python script.py --roadmap-file path/to/roadmap.yml --output-dir path/to/output/folder
```

Please replace path/to/roadmap.yml with the path to your roadmap YAML file and path/to/output/folder with the path to your output folder.
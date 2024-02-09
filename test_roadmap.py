import unittest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch
from io import StringIO
from roadmap import create_output_folder, read_roadmap_definition, validate_yaml, find_templates, process_template, calculate_ids_for_element_items, is_graphviz_installed
import os

class TestRoadmapFunctions(unittest.TestCase):
    def setUp(self):
        self.test_folder = "test_folder"
        self.test_file = "test_file.yml"

    def test_create_output_folder(self):
        # Test when the folder does not exist
        if os.path.exists(self.test_folder):
            os.rmdir(self.test_folder)
        self.assertTrue(create_output_folder(self.test_folder))

        # Test when the folder already exists
        self.assertTrue(create_output_folder(self.test_folder))

        # Clean up after testing
        if os.path.exists(self.test_folder):
            os.rmdir(self.test_folder)

    def test_read_roadmap_definition(self):
        # Test with a non-existing file
        self.assertIsNone(read_roadmap_definition("non_existing_file.yml"))

        # Test with an existing file
        with open(self.test_file, 'w') as f:
            f.write("key: value")
        self.assertEqual(read_roadmap_definition(self.test_file), {"key": "value"})

        # Clean up after testing
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
           
    def test_is_graphviz_installed(self):
#       disabled test
#       TODO: find a way to install graphviz plattform independent and automatically and enable test afterwards
        # test if graphviz is installed
        self.assertTrue(is_graphviz_installed())

if __name__ == '__main__':
    unittest.main()
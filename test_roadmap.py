import unittest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch
from io import StringIO
from roadmap import create_output_folder, read_roadmap_definition, validate_yaml, find_templates, process_template, calculate_ids_for_element_items, is_graphviz_installed, remove_element
import os

class TestRoadmapFunctions(unittest.TestCase):
    def setUp(self):
        self.test_folder = "tests/test_folder"
        self.test_file = "test_file.yml"
        self.test_excisting_file = "tests/roadmap.yml"

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
        # test if graphviz is installed
        self.assertTrue(is_graphviz_installed())
    
    def test_is_level0_element_removed_from_project(self):
        remove_pattern = "milestones"
        # test if a element from project is scipped during operation
        project = read_roadmap_definition(self.test_excisting_file)
        
        self.assertIn("milestones", project)
        remove_element(remove_pattern, project=project)
        self.assertNotIn("milestones", project)
        self.assertIn("objectives", project)
    
    def test_is_level1_element_removed_from_project(self):
        remove_pattern = "milestones.deliverables"
        # test if a element from project is scipped during operation
        project = dict(read_roadmap_definition(self.test_excisting_file))
        # check if milestones in project
        self.assertIn("milestones", project)
        # check if first milestone contains deliverables
        self.assertIn("deliverables", project["milestones"][0])
        # remove milestones deliverables
        remove_element(remove_pattern, project=project)
        # check if deliverables from first milestone is removed
        self.assertNotIn("deliverables", project["milestones"][0])
        # check if project contains still milestones
        self.assertIn("milestones", project)
        # check if project contains still objectives
        self.assertIn("objectives", project)
    
    def test_is_level2_element_removed_from_project(self):
        remove_pattern = "milestones.deliverables.todos"
        # test if a element from project is scipped during operation
        project = dict(read_roadmap_definition(self.test_excisting_file))
        # check if milestones are in project
        self.assertIn("milestones", project)
        # check if objectives are in project
        self.assertIn("objectives", project)
        # check if milestones first element contains deliverables
        self.assertIn("deliverables", project["milestones"][0])
        # check if milestones first deliverable contains todos
        self.assertIn("todos", project["milestones"][0]["deliverables"][0])
        # remove milestones.deliverables.todos
        remove_element(remove_pattern, project=project)
        # check if objectives are still present
        self.assertIn("objectives", project)
        # check if milestones are still present
        self.assertIn("milestones", project)
        # check if milestones first deliverable is still present
        self.assertIn("deliverables", project["milestones"][0])
        # check if milestones first deliverable todos is removed
        self.assertNotIn("todos", project["milestones"][0]["deliverables"][0])
    
    def test_is_level1_description_removed_from_project(self):
        remove_pattern = "milestones.description"
        # test if a element from project is scipped during operation
        project = dict(read_roadmap_definition(self.test_excisting_file))
        # check if milestones are in project
        self.assertIn("milestones", project)
        # check if objectives are in project
        self.assertIn("objectives", project)
        # check if milestones first element contains description
        self.assertIn("description", project["milestones"][0])
        # remove milestones.description
        remove_element(remove_pattern, project=project)
        # check if objectives are still present
        self.assertIn("objectives", project)
        # check if milestones are still present
        self.assertIn("milestones", project)
        # check if milestones first deliverable is still present
        self.assertNotIn("description", project["milestones"][0])

    def test_is_level3_removed_from_project(self):
        remove_pattern = "milestones.deliverables.todos.description"
        # test if a element from project is scipped during operation
        project = dict(read_roadmap_definition(self.test_excisting_file))
        # check if milestones are in project
        self.assertIn("milestones", project)
        # check if objectives are in project
        self.assertIn("objectives", project)
        # check if objectives first keyresult todo element contains description
        self.assertIn("description", project["objectives"][0]['keyresults'][0]['todos'][0])
        # check if milestones first deliverables todo element contains description
        self.assertIn("description", project["milestones"][0]['deliverables'][0]['todos'][0])
        # remove milestones.description
        remove_element(remove_pattern, project=project)
        # check if objectives are still present
        self.assertIn("objectives", project)
        # check if milestones are still present
        self.assertIn("milestones", project)
        # check if milestones first deliverable is removed
        self.assertNotIn("description", project["milestones"][0]['deliverables'][0]['todos'][0])
        # check if objectives first keyresult todo element contains still description
        self.assertIn("description", project["objectives"][0]['keyresults'][0]['todos'][0])
    
    def test_correct_errorhandling_for_unsupported_remove_string(self):
        # test if we handle all errors correctly
        remove_pattern = "."
        project = dict(read_roadmap_definition(self.test_excisting_file))
        remove_element(remove_pattern, project=project)
        # check if objectives are still present
        self.assertIn("objectives", project)
        # check if milestones are still present
        self.assertIn("milestones", project)
        
        
                                                                 
if __name__ == '__main__':
    unittest.main()
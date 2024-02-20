import unittest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch
from io import StringIO
from roadmap import create_output_folder, read_roadmap_definition, validate_yaml, find_templates, process_template, calculate_ids_for_element_items, is_graphviz_installed, remove_element,calculate_roadmap_version,calculate_cost_of_delay,calculate_weighted_shortest_job_first,calculate_wsjf_quantifiers_for_element_items
import os

class TestRoadmapFunctions(unittest.TestCase):
    def setUp(self):
        # this folder is used for storing data during test
        self.test_folder = "tests/test_folder"
        # this file did not excist
        self.test_file = "test_file.yml"
        # this is a excisting roadmap
        self.test_excisting_file = "tests/roadmap.yml"
        # this is the version of the excisting roadmap
        # if you modifiy this file, make shure to modifiy his version
        # version is calculated using md5 and take the first and last 4 characters as version
        self.version_excisting_roadmap = "61a5ff21"

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
    
    def test_roadmap_yml_version_id(self):
        # test if we get none for non-existing file
        self.assertIsNone(calculate_roadmap_version(self.test_file))
        # test if the version id of roadmap fullfills our expectations
        self.assertEqual(calculate_roadmap_version(self.test_excisting_file),self.version_excisting_roadmap)
    
    def test_calculate_cost_of_delay(self):
        # this test covers the calculating part of Cost of Delay
        # check for valid input with zero
        self.assertEqual(calculate_cost_of_delay(user_business_value=0,time_criticality=0,opportunity_enablement_or_risk_reduction=0),0)
        # check for valid input with 1 for each value should give 3
        self.assertEqual(calculate_cost_of_delay(user_business_value=1,time_criticality=1,opportunity_enablement_or_risk_reduction=1),3)
        # check for valid input with 10 for each value should give 30
        self.assertEqual(calculate_cost_of_delay(user_business_value=10,time_criticality=10,opportunity_enablement_or_risk_reduction=10),30)
        # check for handling non valid input
        self.assertIsNone(calculate_cost_of_delay(user_business_value="1",time_criticality="1",opportunity_enablement_or_risk_reduction="1"))
        self.assertIsNone(calculate_cost_of_delay(user_business_value=1.0,time_criticality=1.0,opportunity_enablement_or_risk_reduction=1.0))
        self.assertIsNone(calculate_cost_of_delay(user_business_value=11,time_criticality=-1,opportunity_enablement_or_risk_reduction=100))
        self.assertIsNone(calculate_cost_of_delay(user_business_value=11,time_criticality=0,opportunity_enablement_or_risk_reduction=0))
        self.assertIsNone(calculate_cost_of_delay(user_business_value=0,time_criticality=11,opportunity_enablement_or_risk_reduction=0))
        self.assertIsNone(calculate_cost_of_delay(user_business_value=0,time_criticality=0,opportunity_enablement_or_risk_reduction=11))

    def test_calculate_weighted_shortest_job_first(self):
        # this test covers the calculating part of WSJF
        # check for valid input with min values
        self.assertEqual(calculate_weighted_shortest_job_first(cost_of_delay=0,jobsize=1),0.00)
        # check for valid input with max values
        self.assertEqual(calculate_weighted_shortest_job_first(cost_of_delay=30,jobsize=10),3.00)
        # check for valid input with floating result 
        self.assertEqual(calculate_weighted_shortest_job_first(cost_of_delay=16,jobsize=3),5.33)
        # check for handling non valid input
        self.assertIsNone(calculate_weighted_shortest_job_first(cost_of_delay="16",jobsize="3"))
        self.assertIsNone(calculate_weighted_shortest_job_first(cost_of_delay=19))
        self.assertIsNone(calculate_weighted_shortest_job_first(cost_of_delay=100,jobsize=100))
    
    def test_calculate_wsjf_quantifiers_for_milestones_deliverables(self):
        # test if we calculate correctly and quantifier will be added to project
        project = dict(read_roadmap_definition(self.test_excisting_file))
        # check if first milestone contains deliverables
        self.assertIn("deliverables", project["milestones"][0])
        # check if first milestone first deliverable contains wsjf
        self.assertIn("wsjf", project["milestones"][0]['deliverables'][0])
        self.assertEqual(project["milestones"][0]['deliverables'][0]['wsjf']['user_business_value'],1)
        self.assertEqual(project["milestones"][0]['deliverables'][0]['wsjf']['time_criticality'],1)
        self.assertEqual(project["milestones"][0]['deliverables'][0]['wsjf']['opportunity_enablement_or_risk_reduction'],1)
        self.assertEqual(project["milestones"][0]['deliverables'][0]['wsjf']['jobsize'],1)
        project["milestones"][0]['deliverables'] = calculate_wsjf_quantifiers_for_element_items(project["milestones"][0]['deliverables'])
        # did we still have wsjf?
        self.assertIn("wsjf", project["milestones"][0]['deliverables'][0])
        self.assertEqual(project["milestones"][0]['deliverables'][0]['wsjf']['user_business_value'],1)
        self.assertEqual(project["milestones"][0]['deliverables'][0]['wsjf']['time_criticality'],1)
        self.assertEqual(project["milestones"][0]['deliverables'][0]['wsjf']['opportunity_enablement_or_risk_reduction'],1)
        self.assertEqual(project["milestones"][0]['deliverables'][0]['wsjf']['jobsize'],1)
        # did we get quantifiers
        self.assertIn("quantifiers", project["milestones"][0]['deliverables'][0])
        # is cost of delay correct?
        self.assertEqual(project["milestones"][0]['deliverables'][0]['quantifiers']['cost_of_delay'],3)
        # is wsjf correct
        self.assertEqual(project["milestones"][0]['deliverables'][0]['quantifiers']['wsjf'],3)
        # is jobsize correct from wjs copied
        self.assertEqual(project["milestones"][0]['deliverables'][0]['wsjf']['jobsize'],project["milestones"][0]['deliverables'][0]['quantifiers']['jobsize'])
    
    def test_calculate_wsjf_quantifiers_for_objectives_keyresult(self):
        # test if we calculate correctly and quantifier will be added to project
        project = dict(read_roadmap_definition(self.test_excisting_file))
        # check if first objecttive contains keyresults
        self.assertIn("keyresults", project["objectives"][0])
        # check if first objecttive first keyresult contains wsjf
        self.assertIn("wsjf", project["objectives"][0]['keyresults'][0])
        self.assertEqual(project["objectives"][0]['keyresults'][0]['wsjf']['user_business_value'],1)
        self.assertEqual(project["objectives"][0]['keyresults'][0]['wsjf']['time_criticality'],1)
        self.assertEqual(project["objectives"][0]['keyresults'][0]['wsjf']['opportunity_enablement_or_risk_reduction'],1)
        self.assertEqual(project["objectives"][0]['keyresults'][0]['wsjf']['jobsize'],1)
        project["milestones"][0]['deliverables'] = calculate_wsjf_quantifiers_for_element_items(project["objectives"][0]['keyresults'])
        # did we still have wsjf?
        self.assertIn("wsjf", project["objectives"][0]['keyresults'][0])
        self.assertEqual(project["objectives"][0]['keyresults'][0]['wsjf']['user_business_value'],1)
        self.assertEqual(project["objectives"][0]['keyresults'][0]['wsjf']['time_criticality'],1)
        self.assertEqual(project["objectives"][0]['keyresults'][0]['wsjf']['opportunity_enablement_or_risk_reduction'],1)
        self.assertEqual(project["objectives"][0]['keyresults'][0]['wsjf']['jobsize'],1)
        # did we get quantifiers
        self.assertIn("quantifiers", project["objectives"][0]['keyresults'][0])
        # is cost of delay correct?
        self.assertEqual(project["objectives"][0]['keyresults'][0]['quantifiers']['cost_of_delay'],3)
        # is wsjf correct
        self.assertEqual(project["objectives"][0]['keyresults'][0]['quantifiers']['wsjf'],3)
        # is jobsize correct from wjs copied
        self.assertEqual(project["objectives"][0]['keyresults'][0]['wsjf']['jobsize'],project["objectives"][0]['keyresults'][0]['quantifiers']['jobsize'])
        
        

if __name__ == '__main__':
    unittest.main()
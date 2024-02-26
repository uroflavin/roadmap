import unittest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch
from io import StringIO
from roadmap import create_output_folder, read_roadmap_definition, validate_yaml, find_templates, process_template, calculate_ids_for_element_items, is_graphviz_installed, remove_element,calculate_roadmap_version,calculate_cost_of_delay,calculate_weighted_shortest_job_first,calculate_wsjf_quantifiers_for_element_items, get_key_value_list,get_filtered_key_value_list
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
        self.version_excisting_roadmap = "880a29cf"

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
        with self.assertRaises(OSError):
            read_roadmap_definition("non_existing_file.yml")

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
    
    def test_roadmap_yml_version_id(self):
        # test if we get none for non-existing file
        self.assertIsNone(calculate_roadmap_version(self.test_file))
        # test if the version id of roadmap fullfills our expectations
        self.assertEqual(calculate_roadmap_version(self.test_excisting_file),self.version_excisting_roadmap)

    def test_preconditions_in_test_excisting_file(self):
        # this test is to check if your test.yml has some predefined conditions for testing
        #
        #   the conditions are checked twice: once for version id, which is md5sum of file
        #   and second for the condtions here
        project = dict(read_roadmap_definition(self.test_excisting_file))
        # did we have milestones
        self.assertIn("milestones", project)
        # check if objectives are in project
        self.assertIn("objectives", project)
        # check if milestones first deliverable contains todos
        self.assertIn("todos", project["milestones"][0]["deliverables"][0])
        
        # check if first milestone contains deliverables
        self.assertIn("deliverables", project["milestones"][0])
        # check if first objecttive contains keyresults
        self.assertIn("keyresults", project["objectives"][0])
        
        # check if first milestone first deliverables contains well known quantifiers
        self.assertIn("quantifiers", project["milestones"][0]['deliverables'][0])
        # check if first objecttive first keyresult contains well known quantifiers
        self.assertIn("quantifiers", project["objectives"][0]['keyresults'][0])
        
        # check conditions for cost of delay and wsjf calculation
        self.assertEqual(project["objectives"][0]['keyresults'][0]['quantifiers']['user_business_value'],1)
        self.assertEqual(project["objectives"][0]['keyresults'][0]['quantifiers']['time_criticality'],1)
        self.assertEqual(project["objectives"][0]['keyresults'][0]['quantifiers']['opportunity_enablement_or_risk_reduction'],1)
        self.assertEqual(project["objectives"][0]['keyresults'][0]['quantifiers']['jobsize'],1)
        self.assertIsNone(project["objectives"][0]['keyresults'][0]['quantifiers']['weighted_shortest_job_first'])

        self.assertEqual(project["milestones"][0]['deliverables'][0]['quantifiers']['user_business_value'],1)
        self.assertEqual(project["milestones"][0]['deliverables'][0]['quantifiers']['time_criticality'],1)
        self.assertEqual(project["milestones"][0]['deliverables'][0]['quantifiers']['opportunity_enablement_or_risk_reduction'],1)
        self.assertEqual(project["milestones"][0]['deliverables'][0]['quantifiers']['jobsize'],1)
        self.assertIsNone(project["milestones"][0]['deliverables'][0]['quantifiers']['weighted_shortest_job_first'])

    def test_is_level0_element_removed_from_project(self):
        remove_pattern = "milestones"
        # test if a element from project is scipped during operation
        project = read_roadmap_definition(self.test_excisting_file)
        remove_element(remove_pattern, project=project)
        self.assertNotIn("milestones", project)
        self.assertIn("objectives", project)
    
    def test_is_level1_element_removed_from_project(self):
        remove_pattern = "milestones.deliverables"
        # test if a element from project is scipped during operation
        project = dict(read_roadmap_definition(self.test_excisting_file))
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

    def test_is_level3_string_element_removal_is_set_to_none(self):
        remove_pattern = "milestones.deliverables.quantifiers.jobsize"
        # test if a element from project is scipped during operation
        project = dict(read_roadmap_definition(self.test_excisting_file))
        # check if milestones first deliverables quantifiers element contains jobsize
        self.assertIn("jobsize", project["milestones"][0]['deliverables'][0]['quantifiers'])
        # remove quantifiers.jobsize
        remove_element(remove_pattern, project=project)
        # check if milestones first deliverable is None
        self.assertIsNone(project["milestones"][0]['deliverables'][0]['quantifiers']['jobsize'])
        
    def test_correct_errorhandling_for_unsupported_remove_string(self):
        # test if we handle all errors correctly
        remove_pattern = "."
        project = dict(read_roadmap_definition(self.test_excisting_file))
        with self.assertRaises(ValueError):
            remove_element(remove_pattern, project=project)
        # check if objectives are still present
        self.assertIn("objectives", project)
        # check if milestones are still present
        self.assertIn("milestones", project)

    def test_calculate_cost_of_delay(self):
        # this test covers the calculating part of Cost of Delay
        # check for valid input with zero
        self.assertEqual(calculate_cost_of_delay(user_business_value=0,time_criticality=0,opportunity_enablement_or_risk_reduction=0),0)
        # check for valid input with 1 for each value should give 3
        self.assertEqual(calculate_cost_of_delay(user_business_value=1,time_criticality=1,opportunity_enablement_or_risk_reduction=1),3)
        # check for valid input with 10 for each value should give 30
        self.assertEqual(calculate_cost_of_delay(user_business_value=10,time_criticality=10,opportunity_enablement_or_risk_reduction=10),30)
        # check for handling non valid input
    
    def test_calculate_cost_of_delay_non_valid_inputs(self):
        # test for correct handling non valid inputs during calculation of cost_of_delay
        with self.assertRaises(ValueError):
            calculate_cost_of_delay(user_business_value=0,time_criticality=0,opportunity_enablement_or_risk_reduction=11)
            calculate_cost_of_delay(user_business_value=None,time_criticality=1,opportunity_enablement_or_risk_reduction=1)
            calculate_cost_of_delay(user_business_value="1",time_criticality="1",opportunity_enablement_or_risk_reduction="1")
            calculate_cost_of_delay(user_business_value=1.0,time_criticality=1.0,opportunity_enablement_or_risk_reduction=1.0)
            calculate_cost_of_delay(user_business_value=11,time_criticality=-1,opportunity_enablement_or_risk_reduction=100)
            calculate_cost_of_delay(user_business_value=11,time_criticality=0,opportunity_enablement_or_risk_reduction=0)
            calculate_cost_of_delay(user_business_value=0,time_criticality=11,opportunity_enablement_or_risk_reduction=0)
            calculate_cost_of_delay(user_business_value=0,time_criticality=0,opportunity_enablement_or_risk_reduction=11)

        

    def test_calculate_weighted_shortest_job_first(self):
        # this test covers the calculating part of WSJF
        # check for valid input with min values
        self.assertEqual(calculate_weighted_shortest_job_first(cost_of_delay=0,jobsize=1),0.00)
        # check for valid input with max values
        self.assertEqual(calculate_weighted_shortest_job_first(cost_of_delay=30,jobsize=10),3.00)
        # check for valid input with floating result 
        self.assertEqual(calculate_weighted_shortest_job_first(cost_of_delay=16,jobsize=3),5.33)
        # check for handling non valid input
    
    def test_calculate_weighted_shortest_job_first_non_valid_inputs(self):
        # test for correct handling non valid inputs during calculation of wsjf
        with self.assertRaises(ValueError):
            calculate_weighted_shortest_job_first(cost_of_delay="16",jobsize="3")
            calculate_weighted_shortest_job_first(cost_of_delay=19)
            calculate_weighted_shortest_job_first(cost_of_delay=100,jobsize=100)
            calculate_weighted_shortest_job_first(cost_of_delay=None,jobsize=None)
            calculate_weighted_shortest_job_first(cost_of_delay=None,jobsize=1)
            calculate_weighted_shortest_job_first(cost_of_delay=1,jobsize=None)
    
    def test_calculate_wsjf_quantifiers_if_weighted_shortest_job_is_set(self):
        # test if we calculate correctly and quantifier will be added to project
        project = dict(read_roadmap_definition(self.test_excisting_file))
        # set some weird WSJF
        weird_wsjf = 100.01
        # store in project
        project["objectives"][0]['keyresults'][0]['quantifiers']['weighted_shortest_job_first'] = weird_wsjf
        # calculate
        project["milestones"][0]['deliverables'] = calculate_wsjf_quantifiers_for_element_items(project["objectives"][0]['keyresults'])
        # did we still have our weird wsjf?
        self.assertEqual(project["objectives"][0]['keyresults'][0]['quantifiers']['weighted_shortest_job_first'],weird_wsjf)
         # cost_of_delay should be calculated
        self.assertEqual(project["objectives"][0]['keyresults'][0]['quantifiers']['cost_of_delay'],3)

    def test_calculate_wsjf_quantifiers_if_weighted_shortest_job_is_not_set(self):
        # test if we calculate correctly and quantifier will be added to project
        project = dict(read_roadmap_definition(self.test_excisting_file))
        # set user_business_value to None
        project["objectives"][0]['keyresults'][0]['quantifiers']['user_business_value'] = None
        # calculate
        project["milestones"][0]['deliverables'] = calculate_wsjf_quantifiers_for_element_items(project["objectives"][0]['keyresults'])
         # cost_of_delay should not be calculated
        self.assertIsNone(project["objectives"][0]['keyresults'][0]['quantifiers']['cost_of_delay'])
        # delete quantifier user_business_value
        del project["objectives"][0]['keyresults'][0]['quantifiers']['user_business_value']
        # calculate with missing user_business_value
        project["milestones"][0]['deliverables'] = calculate_wsjf_quantifiers_for_element_items(project["objectives"][0]['keyresults'])
         # cost_of_delay should not be calculated
        self.assertIsNone(project["objectives"][0]['keyresults'][0]['quantifiers']['cost_of_delay'])
        # weighted_shortest_job_first should not be calculated
        self.assertIsNone(project["objectives"][0]['keyresults'][0]['quantifiers']['weighted_shortest_job_first'])

    def test_calculate_wsjf_quantifiers_if_cost_of_delay_is_set(self):
        # test if we calculate correctly and quantifier will be added to project
        project = dict(read_roadmap_definition(self.test_excisting_file))
        # set some weird cost_of_delay
        weird_cost_of_delay = 100
        project["objectives"][0]['keyresults'][0]['quantifiers']['cost_of_delay'] = weird_cost_of_delay
        # calculate
        project["milestones"][0]['deliverables'] = calculate_wsjf_quantifiers_for_element_items(project["objectives"][0]['keyresults'])
        
        # cost of delay should be untouched
        self.assertEqual(project["objectives"][0]['keyresults'][0]['quantifiers']['cost_of_delay'],weird_cost_of_delay)
        # wsjf should not be calculated
        self.assertIsNone(project["objectives"][0]['keyresults'][0]['quantifiers']['weighted_shortest_job_first'])

    def test_calculate_wsjf_quantifiers_for_milestones_deliverables(self):
        # test if we calculate correctly and quantifier will be added to project
        project = dict(read_roadmap_definition(self.test_excisting_file))
        project["milestones"][0]['deliverables'] = calculate_wsjf_quantifiers_for_element_items(project["milestones"][0]['deliverables'])
        # did we still have wsjf?
        self.assertIn("quantifiers", project["milestones"][0]['deliverables'][0])
        self.assertEqual(project["milestones"][0]['deliverables'][0]['quantifiers']['user_business_value'],1)
        self.assertEqual(project["milestones"][0]['deliverables'][0]['quantifiers']['time_criticality'],1)
        self.assertEqual(project["milestones"][0]['deliverables'][0]['quantifiers']['opportunity_enablement_or_risk_reduction'],1)
        self.assertEqual(project["milestones"][0]['deliverables'][0]['quantifiers']['jobsize'],1)
        # did we get quantifiers
        self.assertIn("quantifiers", project["milestones"][0]['deliverables'][0])
        # is cost of delay correct?
        self.assertEqual(project["milestones"][0]['deliverables'][0]['quantifiers']['cost_of_delay'],3)
        # is wsjf correct
        self.assertEqual(project["milestones"][0]['deliverables'][0]['quantifiers']['weighted_shortest_job_first'],3)
        # is jobsize correct from wjs copied
        self.assertEqual(project["milestones"][0]['deliverables'][0]['quantifiers']['jobsize'],project["milestones"][0]['deliverables'][0]['quantifiers']['jobsize'])
    
    def test_calculate_wsjf_quantifiers_for_objectives_keyresult(self):
        # test if we calculate correctly and quantifier will be added to project
        project = dict(read_roadmap_definition(self.test_excisting_file))
        project["milestones"][0]['deliverables'] = calculate_wsjf_quantifiers_for_element_items(project["objectives"][0]['keyresults'])
        # did we still have wsjf?
        self.assertIn("quantifiers", project["objectives"][0]['keyresults'][0])
        self.assertEqual(project["objectives"][0]['keyresults'][0]['quantifiers']['user_business_value'],1)
        self.assertEqual(project["objectives"][0]['keyresults'][0]['quantifiers']['time_criticality'],1)
        self.assertEqual(project["objectives"][0]['keyresults'][0]['quantifiers']['opportunity_enablement_or_risk_reduction'],1)
        self.assertEqual(project["objectives"][0]['keyresults'][0]['quantifiers']['jobsize'],1)
        # did we get quantifiers
        self.assertIn("quantifiers", project["objectives"][0]['keyresults'][0])
        # is cost of delay correct?
        self.assertEqual(project["objectives"][0]['keyresults'][0]['quantifiers']['cost_of_delay'],3)
        # is wsjf correct
        self.assertEqual(project["objectives"][0]['keyresults'][0]['quantifiers']['weighted_shortest_job_first'],3)
    
    def test_get_key_value_list(self):
         # test if we build a key-value list correctly
        project = dict(read_roadmap_definition(self.test_excisting_file))
        project_as_list = get_key_value_list(element=project)
        # project_as_list is list?
        self.assertIsInstance(project_as_list, list)
        # first key is 'title'
        self.assertEqual(project_as_list[0]['key'],"title")
        # second key is 'description'
        self.assertEqual(project_as_list[1]['key'],"description")
        # now test with prefix
        prefix = "project"
        project_as_list = get_key_value_list(element=project, prefix_for_key=prefix)
        # first key is 'title'
        self.assertEqual(project_as_list[0]['key'],prefix + ".title")
        # second key is 'description'
        self.assertEqual(project_as_list[1]['key'],prefix + ".description")
        # check for keeping index properly
        project_as_list = get_key_value_list(element=project['milestones'], prefix_for_key='milestones', keep_index=True)
        # our testdata first information for milestone is id
        self.assertEqual(project_as_list[0]['key'],"milestones.0.id")
        # our testdata first milestone id is M1
        self.assertEqual(project_as_list[0]['value'],"M1")
        # check for error handling
        project_as_list = get_key_value_list()
        # we always get a empty key, value list
        self.assertIsNone(project_as_list[0]['key'])
        self.assertIsNone(project_as_list[0]['value'])

    def test_get_filtered_key_value_list(self):
         # test if we filter a key-value list correctly
        project = dict(read_roadmap_definition(self.test_excisting_file))
        # first, test with a known list
        project_as_list = get_key_value_list(element=project)
        filtered_list = get_filtered_key_value_list(key_value_list=project_as_list,filter_for_keys="milestones.title",precise_search=True)

        # filtered_list is list?
        self.assertIsInstance(filtered_list, list)
        # first and second key are milestones.title
        self.assertEqual(filtered_list[0]['key'],"milestones.title")
        self.assertEqual(filtered_list[1]['key'],"milestones.title")
        # check for error handling
        with self.assertRaises(ValueError):
            get_filtered_key_value_list()
        
        
if __name__ == '__main__':
    unittest.main()
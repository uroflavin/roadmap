import unittest
import os
from roadmap_app.utils import read_roadmap_definition
from roadmap_app.model import (remove_element, calculate_cost_of_delay,
                               calculate_weighted_shortest_job_first, calculate_wsjf_quantifiers_for_element_items,
                               make_id_from, get_items_grouped_by_date, enrich_project)


class TestModel(unittest.TestCase):
    def setUp(self):
        # this is an existing roadmap
        self.test_existing_file = os.path.join(os.path.dirname(__file__), "roadmap.yml")

    def test_preconditions_in_test_exciting_file(self):
        # this test is to check if your test.yml has some predefined conditions for testing
        #
        #   the conditions are checked twice: once for version id, which is md5sum of file
        #   and second for the conditions here
        project = dict(read_roadmap_definition(self.test_existing_file))
        # did we have milestones
        self.assertIn("milestones", project)
        # check if objectives are in project
        self.assertIn("objectives", project)
        # check if milestones first deliverable contains todos
        self.assertIn("todos", project["milestones"][0]["deliverables"][0])

        # check if first milestone contains deliverables
        self.assertIn("deliverables", project["milestones"][0])
        # check if first objective contains keyresults
        self.assertIn("keyresults", project["objectives"][0])

        # check if first milestone first deliverables contains well known quantifiers
        self.assertIn("quantifiers", project["milestones"][0]['deliverables'][0])
        # check if first objective first keyresult contains well known quantifiers
        self.assertIn("quantifiers", project["objectives"][0]['keyresults'][0])

        # check conditions for cost of delay and wsjf calculation
        self.assertEqual(project["objectives"][0]['keyresults'][0]['quantifiers']['user_business_value'], 1)
        self.assertEqual(project["objectives"][0]['keyresults'][0]['quantifiers']['time_criticality'], 1)
        self.assertEqual(
            project["objectives"][0]['keyresults'][0]['quantifiers']['opportunity_enablement_or_risk_reduction'], 1)
        self.assertEqual(project["objectives"][0]['keyresults'][0]['quantifiers']['jobsize'], 1)
        self.assertIsNone(project["objectives"][0]['keyresults'][0]['quantifiers']['weighted_shortest_job_first'])

        self.assertEqual(project["milestones"][0]['deliverables'][0]['quantifiers']['user_business_value'], 1)
        self.assertEqual(project["milestones"][0]['deliverables'][0]['quantifiers']['time_criticality'], 1)
        self.assertEqual(
            project["milestones"][0]['deliverables'][0]['quantifiers']['opportunity_enablement_or_risk_reduction'], 1)
        self.assertEqual(project["milestones"][0]['deliverables'][0]['quantifiers']['jobsize'], 1)
        self.assertIsNone(project["milestones"][0]['deliverables'][0]['quantifiers']['weighted_shortest_job_first'])

    def test_is_level0_element_removed_from_project(self):
        remove_pattern = "milestones"
        # test if an element from project is skipped during operation
        project = read_roadmap_definition(self.test_existing_file)
        remove_element(remove_pattern, project=project)
        self.assertNotIn("milestones", project)
        self.assertIn("objectives", project)

    def test_is_level1_element_removed_from_project(self):
        remove_pattern = "milestones.deliverables"
        # test if an element from project is skipped during operation
        project = dict(read_roadmap_definition(self.test_existing_file))
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
        # test if an element from project is skipped during operation
        project = dict(read_roadmap_definition(self.test_existing_file))
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
        # test if an element from project is skipped during operation
        project = dict(read_roadmap_definition(self.test_existing_file))
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
        # test if an element from project is skipped during operation
        project = dict(read_roadmap_definition(self.test_existing_file))
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
        # check if objectives first keyresult todos-element contains still description
        self.assertIn("description", project["objectives"][0]['keyresults'][0]['todos'][0])

    def test_is_level3_string_element_removal_is_set_to_none(self):
        remove_pattern = "milestones.deliverables.quantifiers.jobsize"
        # test if an element from project is skipped during operation
        project = dict(read_roadmap_definition(self.test_existing_file))
        # check if milestones first deliverables quantifiers element contains jobsize
        self.assertIn("jobsize", project["milestones"][0]['deliverables'][0]['quantifiers'])
        # remove quantifiers.jobsize
        remove_element(remove_pattern, project=project)
        # check if milestones first deliverable is None
        self.assertIsNone(project["milestones"][0]['deliverables'][0]['quantifiers']['jobsize'])

    def test_correct_error_handling_for_unsupported_remove_string(self):
        # test if we handle all errors correctly
        remove_pattern = "."
        project = dict(read_roadmap_definition(self.test_existing_file))
        with self.assertRaises(ValueError):
            remove_element(remove_pattern, project=project)
        # check if objectives are still present
        self.assertIn("objectives", project)
        # check if milestones are still present
        self.assertIn("milestones", project)

    def test_remove_handles_multiple_levels_to_multiple_times(self):
        skip_items = ("milestones.deliverables.quantifiers.weighted_shortest_job_first,"
                      "objectives.keyresults.todos,"
                      "objectives.keyresults,milestones")
        project = dict(read_roadmap_definition(self.test_existing_file))
        # check if milestones are present
        self.assertIn("milestones", project)
        # first round
        for skip in skip_items.replace(" ", "").split(","):
            remove_element(skip, project=project)
        # second round
        for skip in skip_items.replace(" ", "").split(","):
            remove_element(skip, project=project)
        # check if objectives are still present
        self.assertIn("objectives", project)
        # check if milestones are removed
        self.assertNotIn("milestones", project)
        # check if first keyresult of first objective is removed
        self.assertNotIn('keyresults', project['objectives'][0])

    def test_calculate_cost_of_delay(self):
        # this test covers the calculating part of Cost of Delay
        # check for valid input with zero
        self.assertEqual(calculate_cost_of_delay(user_business_value=0, time_criticality=0,
                                                 opportunity_enablement_or_risk_reduction=0), 0)
        # check for valid input with 1 for each value should give 3
        self.assertEqual(calculate_cost_of_delay(user_business_value=1, time_criticality=1,
                                                 opportunity_enablement_or_risk_reduction=1), 3)
        # check for valid input with 10 for each value should give 30
        self.assertEqual(calculate_cost_of_delay(user_business_value=10, time_criticality=10,
                                                 opportunity_enablement_or_risk_reduction=10), 30)
        # check for handling non-valid input

    def test_calculate_cost_of_delay_non_valid_inputs(self):
        # test for correct handling non-valid inputs during calculation of cost_of_delay
        with self.assertRaises(ValueError):
            calculate_cost_of_delay(user_business_value=0, time_criticality=0,
                                    opportunity_enablement_or_risk_reduction=11)
        with self.assertRaises(ValueError):
            calculate_cost_of_delay(user_business_value=None, time_criticality=1,
                                    opportunity_enablement_or_risk_reduction=1)
        with self.assertRaises(ValueError):
            calculate_cost_of_delay(user_business_value="1", time_criticality="1",
                                    opportunity_enablement_or_risk_reduction="1")
        with self.assertRaises(ValueError):
            calculate_cost_of_delay(user_business_value=1.0, time_criticality=1.0,
                                    opportunity_enablement_or_risk_reduction=1.0)
        with self.assertRaises(ValueError):
            calculate_cost_of_delay(user_business_value=11, time_criticality=-1,
                                    opportunity_enablement_or_risk_reduction=100)
        with self.assertRaises(ValueError):
            calculate_cost_of_delay(user_business_value=11, time_criticality=0,
                                    opportunity_enablement_or_risk_reduction=0)
        with self.assertRaises(ValueError):
            calculate_cost_of_delay(user_business_value=0, time_criticality=11,
                                    opportunity_enablement_or_risk_reduction=0)
        with self.assertRaises(ValueError):
            calculate_cost_of_delay(user_business_value=0, time_criticality=0,
                                    opportunity_enablement_or_risk_reduction=11)

    def test_calculate_weighted_shortest_job_first(self):
        # this test covers the calculating part of WSJF
        # check for valid input with min values
        self.assertEqual(calculate_weighted_shortest_job_first(cost_of_delay=0, jobsize=1), 0.00)
        # check for valid input with max values
        self.assertEqual(calculate_weighted_shortest_job_first(cost_of_delay=30, jobsize=10), 3.00)
        # check for valid input with floating result
        self.assertEqual(calculate_weighted_shortest_job_first(cost_of_delay=16, jobsize=3), 5.33)
        # Check for Jobsize 30 (implementing #94)
        self.assertEqual(calculate_weighted_shortest_job_first(cost_of_delay=16, jobsize=30), 0.53)

    def test_calculate_weighted_shortest_job_first_non_valid_inputs(self):
        # test for correct handling non-valid inputs during calculation of wsjf
        with self.assertRaises(ValueError):
            calculate_weighted_shortest_job_first(cost_of_delay="16", jobsize="3")
        with self.assertRaises(ValueError):
            calculate_weighted_shortest_job_first(cost_of_delay=19)
        with self.assertRaises(ValueError):
            calculate_weighted_shortest_job_first(cost_of_delay=100, jobsize=100)
        with self.assertRaises(ValueError):
            calculate_weighted_shortest_job_first(cost_of_delay=None, jobsize=None)
        with self.assertRaises(ValueError):
            calculate_weighted_shortest_job_first(cost_of_delay=None, jobsize=1)
        with self.assertRaises(ValueError):
            calculate_weighted_shortest_job_first(cost_of_delay=1, jobsize=None)

    def test_calculate_wsjf_quantifiers_if_weighted_shortest_job_is_set(self):
        # test if we calculate correctly and quantifier will be added to project
        project = dict(read_roadmap_definition(self.test_existing_file))
        # set some weird WSJF
        weird_wsjf = 100.01
        # store in project
        project["objectives"][0]['keyresults'][0]['quantifiers']['weighted_shortest_job_first'] = weird_wsjf
        # calculate
        project["milestones"][0]['deliverables'] = calculate_wsjf_quantifiers_for_element_items(
            project["objectives"][0]['keyresults'])
        # did we still have our weird wsjf?
        self.assertEqual(project["objectives"][0]['keyresults'][0]['quantifiers']['weighted_shortest_job_first'],
                         weird_wsjf)
        # cost_of_delay should be calculated
        self.assertEqual(project["objectives"][0]['keyresults'][0]['quantifiers']['cost_of_delay'], 3)

    def test_calculate_wsjf_quantifiers_if_weighted_shortest_job_is_not_set(self):
        # test if we calculate correctly and quantifier will be added to project
        project = dict(read_roadmap_definition(self.test_existing_file))
        # set user_business_value to None
        project["objectives"][0]['keyresults'][0]['quantifiers']['user_business_value'] = None
        # calculate
        project["milestones"][0]['deliverables'] = calculate_wsjf_quantifiers_for_element_items(
            project["objectives"][0]['keyresults'])
        # cost_of_delay should not be calculated
        self.assertIsNone(project["objectives"][0]['keyresults'][0]['quantifiers']['cost_of_delay'])
        # delete quantifier user_business_value
        del project["objectives"][0]['keyresults'][0]['quantifiers']['user_business_value']
        # calculate with missing user_business_value
        project["milestones"][0]['deliverables'] = calculate_wsjf_quantifiers_for_element_items(
            project["objectives"][0]['keyresults'])
        # cost_of_delay should not be calculated
        self.assertIsNone(project["objectives"][0]['keyresults'][0]['quantifiers']['cost_of_delay'])
        # weighted_shortest_job_first should not be calculated
        self.assertIsNone(project["objectives"][0]['keyresults'][0]['quantifiers']['weighted_shortest_job_first'])

    def test_calculate_wsjf_quantifiers_if_cost_of_delay_is_set(self):
        # test if we calculate correctly and quantifier will be added to project
        project = dict(read_roadmap_definition(self.test_existing_file))
        # set some weird cost_of_delay
        weird_cost_of_delay = 100
        project["objectives"][0]['keyresults'][0]['quantifiers']['cost_of_delay'] = weird_cost_of_delay
        # calculate
        project["milestones"][0]['deliverables'] = calculate_wsjf_quantifiers_for_element_items(
            project["objectives"][0]['keyresults'])

        # cost of delay should be untouched
        self.assertEqual(project["objectives"][0]['keyresults'][0]['quantifiers']['cost_of_delay'], weird_cost_of_delay)
        # wsjf should not be calculated
        self.assertIsNone(project["objectives"][0]['keyresults'][0]['quantifiers']['weighted_shortest_job_first'])

    def test_calculate_wsjf_quantifiers_for_milestones_deliverables(self):
        # test if we calculate correctly and quantifier will be added to project
        project = dict(read_roadmap_definition(self.test_existing_file))
        project["milestones"][0]['deliverables'] = calculate_wsjf_quantifiers_for_element_items(
            project["milestones"][0]['deliverables'])
        # did we still have wsjf?
        self.assertIn("quantifiers", project["milestones"][0]['deliverables'][0])
        self.assertEqual(project["milestones"][0]['deliverables'][0]['quantifiers']['user_business_value'], 1)
        self.assertEqual(project["milestones"][0]['deliverables'][0]['quantifiers']['time_criticality'], 1)
        self.assertEqual(
            project["milestones"][0]['deliverables'][0]['quantifiers']['opportunity_enablement_or_risk_reduction'], 1)
        self.assertEqual(project["milestones"][0]['deliverables'][0]['quantifiers']['jobsize'], 1)
        # did we get quantifiers
        self.assertIn("quantifiers", project["milestones"][0]['deliverables'][0])
        # is cost of delay correct?
        self.assertEqual(project["milestones"][0]['deliverables'][0]['quantifiers']['cost_of_delay'], 3)
        # is wsjf correct
        self.assertEqual(project["milestones"][0]['deliverables'][0]['quantifiers']['weighted_shortest_job_first'], 3)
        # is jobsize correct from wjs copied
        self.assertEqual(project["milestones"][0]['deliverables'][0]['quantifiers']['jobsize'],
                         project["milestones"][0]['deliverables'][0]['quantifiers']['jobsize'])

    def test_calculate_wsjf_quantifiers_for_objectives_keyresult(self):
        # test if we calculate correctly and quantifier will be added to project
        project = dict(read_roadmap_definition(self.test_existing_file))
        project["milestones"][0]['deliverables'] = calculate_wsjf_quantifiers_for_element_items(
            project["objectives"][0]['keyresults'])
        # did we still have wsjf?
        self.assertIn("quantifiers", project["objectives"][0]['keyresults'][0])
        self.assertEqual(project["objectives"][0]['keyresults'][0]['quantifiers']['user_business_value'], 1)
        self.assertEqual(project["objectives"][0]['keyresults'][0]['quantifiers']['time_criticality'], 1)
        self.assertEqual(
            project["objectives"][0]['keyresults'][0]['quantifiers']['opportunity_enablement_or_risk_reduction'], 1)
        self.assertEqual(project["objectives"][0]['keyresults'][0]['quantifiers']['jobsize'], 1)
        # did we get quantifiers
        self.assertIn("quantifiers", project["objectives"][0]['keyresults'][0])
        # is cost of delay correct?
        self.assertEqual(project["objectives"][0]['keyresults'][0]['quantifiers']['cost_of_delay'], 3)
        # is wsjf correct
        self.assertEqual(project["objectives"][0]['keyresults'][0]['quantifiers']['weighted_shortest_job_first'], 3)

    def test_make_id_from_basic(self):
        # test basic id generation
        self.assertEqual(make_id_from("Hello World"), "hello_world")
        self.assertEqual(make_id_from("test.value"), "test_value")
        self.assertEqual(make_id_from("my-item"), "my_item")
        self.assertEqual(make_id_from("item#1"), "item_1")
        self.assertEqual(make_id_from("a+b*c"), "a_b_c")

    def test_make_id_from_umlauts(self):
        # test umlaut replacement
        self.assertEqual(make_id_from("Ueberblick"), "ueberblick")
        self.assertEqual(make_id_from("aerger"), "aerger")
        self.assertEqual(make_id_from("Größe"), "groesse")
        self.assertEqual(make_id_from("Übung"), "uebung")
        self.assertEqual(make_id_from("Straße"), "strasse")
        self.assertEqual(make_id_from("schön"), "schoen")

    def test_make_id_from_empty(self):
        # test empty input
        self.assertEqual(make_id_from(""), "")
        self.assertEqual(make_id_from(), "")

    def test_get_items_grouped_by_date(self):
        # test grouping items by date
        items = [
            {"title": "A", "date": "2024-01"},
            {"title": "B", "date": "2024-01"},
            {"title": "C", "date": "2024-02"},
        ]
        grouped = get_items_grouped_by_date(items)
        self.assertIn("2024-01", grouped)
        self.assertIn("2024-02", grouped)
        self.assertEqual(len(grouped["2024-01"]), 2)
        self.assertEqual(len(grouped["2024-02"]), 1)

    def test_get_items_grouped_by_date_without_date(self):
        # test items without date attribute are grouped under "None"
        items = [{"title": "no date"}, {"title": "also no date"}]
        grouped = get_items_grouped_by_date(items)
        self.assertIn("None", grouped)
        self.assertEqual(len(grouped["None"]), 2)

    def test_get_items_grouped_by_date_empty(self):
        # test empty and None input
        self.assertEqual(get_items_grouped_by_date(None), {})
        self.assertEqual(get_items_grouped_by_date([]), {})

    def test_enrich_project(self):
        # test that enrich_project adds all expected computed fields
        project = dict(read_roadmap_definition(self.test_existing_file))
        enrich_project(project, skip_items=None, roadmap_definition_file=self.test_existing_file)
        # meta should be added
        self.assertIn("meta", project)
        self.assertIn("version", project["meta"])
        self.assertIn("rendertime", project["meta"])
        self.assertEqual(project["meta"]["version"], self.version_existing_roadmap)
        # IDs should be calculated for milestones
        self.assertIn("_id", project["milestones"][0])
        self.assertIn("id", project["milestones"][0])
        self.assertIn("_parent_id", project["milestones"][0])
        # IDs should be calculated for objectives
        self.assertIn("_id", project["objectives"][0])
        # group should be present
        self.assertIn("group", project)
        # as_list should be present
        self.assertIn("as_list", project)
        self.assertIsInstance(project["as_list"], list)
        self.assertGreater(len(project["as_list"]), 0)


if __name__ == '__main__':
    unittest.main()

import unittest
import os
from roadmap_app.utils import (read_roadmap_definition, calculate_roadmap_version, get_key_value_list,
                               get_filtered_key_value_list, create_output_folder)


class TestUtils(unittest.TestCase):
    def setUp(self):
        # this folder is used for storing data during test
        self.test_folder = os.path.join(os.path.dirname(__file__), "test_folder")
        # this file did not exist
        self.test_file = os.path.join(os.path.dirname(__file__), "test_file.yml")
        # this is an existing roadmap
        self.test_existing_file = os.path.join(os.path.dirname(__file__), "roadmap.yml")

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

    def test_roadmap_yml_version_id(self):
        # test if we get none for non-existing file
        self.assertIsNone(calculate_roadmap_version(self.test_file))
        # test if the version id of roadmap fulfills our expectations
        self.assertEqual(calculate_roadmap_version(self.test_existing_file), self.version_existing_roadmap)

    def test_get_key_value_list(self):
        # test if we build a key-value list correctly
        project = dict(read_roadmap_definition(self.test_existing_file))
        project_as_list = get_key_value_list(element=project)
        # project_as_list is list?
        self.assertIsInstance(project_as_list, list)
        # first key is 'title'
        self.assertEqual(project_as_list[0]['key'], "title")
        # second key is 'description'
        self.assertEqual(project_as_list[1]['key'], "description")
        # now test with prefix
        prefix = "project"
        project_as_list = get_key_value_list(element=project, prefix_for_key=prefix)
        # first key is 'title'
        self.assertEqual(project_as_list[0]['key'], prefix + ".title")
        # second key is 'description'
        self.assertEqual(project_as_list[1]['key'], prefix + ".description")
        # check for keeping index properly
        project_as_list = get_key_value_list(element=project['milestones'], prefix_for_key='milestones',
                                             keep_index=True)
        # our testdata first information for milestone is id
        self.assertEqual(project_as_list[0]['key'], "milestones.0.id")
        # our testdata first milestone id is M1
        self.assertEqual(project_as_list[0]['value'], "M1")
        # check for error handling
        project_as_list = get_key_value_list()
        # we always get an empty key, value list
        self.assertIsNone(project_as_list[0]['key'])
        self.assertIsNone(project_as_list[0]['value'])

    def test_get_filtered_key_value_list(self):
        # test if we filter a key-value list correctly
        project = dict(read_roadmap_definition(self.test_existing_file))
        # first, test with a known list
        project_as_list = get_key_value_list(element=project)
        filtered_list = get_filtered_key_value_list(key_value_list=project_as_list, filter_for_keys="milestones.title",
                                                    precise_search=True)

        # filtered_list is list?
        self.assertIsInstance(filtered_list, list)
        # first and second key are milestones.title
        self.assertEqual(filtered_list[0]['key'], "milestones.title")
        self.assertEqual(filtered_list[1]['key'], "milestones.title")
        # check for error handling
        with self.assertRaises(ValueError):
            get_filtered_key_value_list()


if __name__ == '__main__':
    unittest.main()

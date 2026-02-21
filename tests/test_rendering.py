import unittest
import tempfile
import shutil
import os
from jinja2 import Environment
from roadmap_app.utils import read_roadmap_definition
from roadmap_app.rendering import validate_yaml, find_templates, is_graphviz_installed, process_template


class TestRendering(unittest.TestCase):
    def setUp(self):
        # this is an existing roadmap
        self.test_existing_file = os.path.join(os.path.dirname(__file__), "roadmap.yml")

    @unittest.skipUnless(shutil.which("dot"), "graphviz not installed")
    def test_is_graphviz_installed(self):
        # test if graphviz is installed
        self.assertTrue(is_graphviz_installed())

    def test_validate_yaml_valid(self):
        # test validation with valid roadmap data
        project = dict(read_roadmap_definition(self.test_existing_file))
        schema_path = os.path.join(os.path.dirname(__file__), "..", "schema", "roadmap.json")
        error, is_valid = validate_yaml(roadmap_data=project, path_to_json_schema=schema_path)
        self.assertIsNone(error)
        self.assertTrue(is_valid)

    def test_validate_yaml_invalid(self):
        # test validation with invalid data (missing required fields)
        invalid_data = {"not_a_valid_key": "value"}
        schema_path = os.path.join(os.path.dirname(__file__), "..", "schema", "roadmap.json")
        error, is_valid = validate_yaml(roadmap_data=invalid_data, path_to_json_schema=schema_path)
        self.assertIsNotNone(error)
        self.assertFalse(is_valid)

    def test_find_templates_with_manifest(self):
        # test manifest-based template discovery (templates.yml present)
        with tempfile.TemporaryDirectory() as tmpdir:
            template_path = tmpdir
            output_path = os.path.join(tmpdir, "output")
            os.makedirs(output_path)

            # create subdirectory and template file
            html_dir = os.path.join(template_path, "html")
            os.makedirs(html_dir)
            with open(os.path.join(html_dir, "roadmap.html"), "w") as f:
                f.write("<html>{{ project.title }}</html>")

            # create templates.yml manifest
            with open(os.path.join(template_path, "templates.yml"), "w") as f:
                f.write("- name: Test HTML\n  input: html/roadmap.html\n  output: roadmap.html\n")

            suffixes = ["html", "md", "dot", "csv"]
            templates = find_templates(template_path, suffixes, output_path)

            self.assertIsInstance(templates, list)
            self.assertEqual(len(templates), 1)
            t = templates[0]
            # check all expected keys are present
            for key in ["path", "file", "output_file", "output_file_basename", "output_path", "suffix", "type"]:
                self.assertIn(key, t)
            self.assertEqual(t["file"], "roadmap.html")
            self.assertEqual(t["suffix"], "html")
            self.assertEqual(t["type"], "html")
            self.assertEqual(t["output_file_basename"], "roadmap")
            self.assertTrue(t["output_file"].endswith("roadmap.html"))

    def test_find_templates_with_manifest_subdirectory_output(self):
        # test manifest-based discovery with subdirectory in output path (e.g. kanban/milestones.html)
        with tempfile.TemporaryDirectory() as tmpdir:
            template_path = tmpdir
            output_path = os.path.join(tmpdir, "output")
            os.makedirs(output_path)

            html_dir = os.path.join(template_path, "html-kanban")
            os.makedirs(html_dir)
            with open(os.path.join(html_dir, "roadmap.kanban.milestones.html"), "w") as f:
                f.write("<html>kanban</html>")

            with open(os.path.join(template_path, "templates.yml"), "w") as f:
                f.write("- input: html-kanban/roadmap.kanban.milestones.html\n"
                        "  output: kanban/milestones.html\n")

            templates = find_templates(template_path, ["html"], output_path)

            self.assertEqual(len(templates), 1)
            t = templates[0]
            self.assertEqual(t["file"], "roadmap.kanban.milestones.html")
            self.assertEqual(t["output_file_basename"], "milestones")
            self.assertTrue(t["output_path"].endswith("kanban"))
            self.assertTrue(t["output_file"].endswith("milestones.html"))

    def test_find_templates_with_manifest_filters_unknown_suffix(self):
        # test that templates with unknown suffixes are excluded
        with tempfile.TemporaryDirectory() as tmpdir:
            template_path = tmpdir
            output_path = os.path.join(tmpdir, "output")
            os.makedirs(output_path)

            txt_dir = os.path.join(template_path, "txt")
            os.makedirs(txt_dir)
            with open(os.path.join(txt_dir, "roadmap.txt"), "w") as f:
                f.write("plain text")

            with open(os.path.join(template_path, "templates.yml"), "w") as f:
                f.write("- input: txt/roadmap.txt\n  output: roadmap.txt\n")

            # "txt" is not in known suffixes
            templates = find_templates(template_path, ["html", "md"], output_path)
            self.assertEqual(len(templates), 0)

    def test_find_templates_with_manifest_skips_invalid_entries(self):
        # test that invalid manifest entries (missing input/output) are skipped
        with tempfile.TemporaryDirectory() as tmpdir:
            template_path = tmpdir
            output_path = os.path.join(tmpdir, "output")
            os.makedirs(output_path)

            html_dir = os.path.join(template_path, "html")
            os.makedirs(html_dir)
            with open(os.path.join(html_dir, "roadmap.html"), "w") as f:
                f.write("<html></html>")

            with open(os.path.join(template_path, "templates.yml"), "w") as f:
                f.write("- input: html/roadmap.html\n  output: roadmap.html\n"
                        "- name: missing output\n  input: html/roadmap.html\n"
                        "- name: missing input\n  output: roadmap.html\n"
                        "- just a string\n")

            templates = find_templates(template_path, ["html"], output_path)
            # only the first valid entry should be returned
            self.assertEqual(len(templates), 1)

    def test_find_templates_with_manifest_non_list(self):
        # test that a non-list templates.yml returns empty list
        with tempfile.TemporaryDirectory() as tmpdir:
            template_path = tmpdir
            output_path = os.path.join(tmpdir, "output")
            os.makedirs(output_path)

            with open(os.path.join(template_path, "templates.yml"), "w") as f:
                f.write("key: value\n")

            templates = find_templates(template_path, ["html"], output_path)
            self.assertEqual(templates, [])

    def test_find_templates_without_manifest(self):
        # test directory-walk fallback (no templates.yml)
        with tempfile.TemporaryDirectory() as tmpdir:
            template_path = tmpdir
            output_path = os.path.join(tmpdir, "output")
            os.makedirs(output_path)

            # create files matching roadmap.<suffix> pattern
            with open(os.path.join(template_path, "roadmap.html"), "w") as f:
                f.write("<html></html>")
            with open(os.path.join(template_path, "roadmap.md"), "w") as f:
                f.write("# markdown")
            # this file should NOT be found (not matching roadmap.<suffix>)
            with open(os.path.join(template_path, "other.html"), "w") as f:
                f.write("<html></html>")

            suffixes = ["html", "md"]
            templates = find_templates(template_path, suffixes, output_path)

            self.assertIsInstance(templates, list)
            self.assertEqual(len(templates), 2)
            found_files = {t["file"] for t in templates}
            self.assertIn("roadmap.html", found_files)
            self.assertIn("roadmap.md", found_files)
            self.assertNotIn("other.html", found_files)
            # check structure of returned dicts
            for t in templates:
                for key in ["path", "file", "output_file", "output_file_basename", "output_path", "suffix", "type"]:
                    self.assertIn(key, t)
                self.assertEqual(t["output_file_basename"], "roadmap")

    def test_find_templates_without_manifest_filters_unknown_suffix(self):
        # test that directory-walk also filters by known suffixes
        with tempfile.TemporaryDirectory() as tmpdir:
            template_path = tmpdir
            output_path = os.path.join(tmpdir, "output")
            os.makedirs(output_path)

            with open(os.path.join(template_path, "roadmap.txt"), "w") as f:
                f.write("text")

            templates = find_templates(template_path, ["html", "md"], output_path)
            self.assertEqual(len(templates), 0)

    def test_find_templates_with_real_templates(self):
        # test with the actual templates/ directory from the project
        template_path = os.path.join(os.path.dirname(__file__), "..", "templates")
        if not os.path.isdir(template_path):
            self.skipTest("templates/ directory not found")

        with tempfile.TemporaryDirectory() as output_path:
            suffixes = ["html", "md", "dot", "csv"]
            templates = find_templates(template_path, suffixes, output_path)

            self.assertIsInstance(templates, list)
            # the real templates.yml has 6 entries
            self.assertEqual(len(templates), 6)
            found_suffixes = {t["suffix"] for t in templates}
            self.assertIn("html", found_suffixes)
            self.assertIn("csv", found_suffixes)
            self.assertIn("dot", found_suffixes)
            self.assertIn("md", found_suffixes)


class TestProcessTemplate(unittest.TestCase):

    def _make_template(self, tmpdir, content="Hello {{ project.title }}", suffix="html"):
        """Helper: create a template file and return the template dict expected by process_template."""
        template_dir = os.path.join(tmpdir, "templates", suffix)
        os.makedirs(template_dir, exist_ok=True)
        template_file = f"roadmap.{suffix}"
        with open(os.path.join(template_dir, template_file), "w") as f:
            f.write(content)

        output_dir = os.path.join(tmpdir, "output")
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, f"roadmap.{suffix}")

        return {
            "path": template_dir,
            "file": template_file,
            "output_file": output_file,
            "output_file_basename": "roadmap",
            "output_path": output_dir,
            "suffix": suffix,
            "type": suffix,
        }

    def test_renders_template_to_output_file(self):
        # basic success case: template is rendered and written to disk
        with tempfile.TemporaryDirectory() as tmpdir:
            template = self._make_template(tmpdir, content="Title: {{ project.title }}")
            process_template(
                template=template,
                project={"title": "My Roadmap"},
            )
            with open(template["output_file"]) as f:
                self.assertEqual(f.read(), "Title: My Roadmap")

    def test_raises_value_error_when_template_is_none(self):
        # process_template must raise ValueError if template is None
        with self.assertRaises(ValueError):
            process_template(template=None, project={})

    def test_handles_missing_variable_gracefully(self):
        # Jinja2 undefined variables render as empty string by default (no error)
        with tempfile.TemporaryDirectory() as tmpdir:
            template = self._make_template(tmpdir, content="Value: {{ project.nonexistent }}")
            process_template(template=template, project={})
            with open(template["output_file"]) as f:
                content = f.read()
            self.assertIn("Value:", content)

    def test_handles_syntax_error_in_template(self):
        # a Jinja2 syntax error should be caught, not crash the process
        with tempfile.TemporaryDirectory() as tmpdir:
            template = self._make_template(tmpdir, content="{% if %}broken{% endif %}")
            # should not raise -- error is caught internally
            process_template(template=template, project={"title": "test"})
            # output file should NOT be created since rendering failed
            self.assertFalse(os.path.exists(template["output_file"]))

    def test_creates_output_subdirectory(self):
        # process_template should create missing output directories
        with tempfile.TemporaryDirectory() as tmpdir:
            template = self._make_template(tmpdir, content="ok")
            # point output to a nested path that doesn't exist yet
            nested_output = os.path.join(tmpdir, "deep", "nested", "dir")
            template["output_path"] = nested_output
            template["output_file"] = os.path.join(nested_output, "roadmap.html")

            process_template(template=template, project={})
            self.assertTrue(os.path.isdir(nested_output))
            self.assertTrue(os.path.isfile(template["output_file"]))

    def test_uses_default_environment_when_none(self):
        # when environment=None, a default Environment is created
        with tempfile.TemporaryDirectory() as tmpdir:
            template = self._make_template(tmpdir, content="default env: {{ project.x }}")
            process_template(environment=None, template=template, project={"x": "42"})
            with open(template["output_file"]) as f:
                self.assertEqual(f.read(), "default env: 42")

    def test_uses_provided_environment(self):
        # a custom Jinja2 Environment should be used if provided
        with tempfile.TemporaryDirectory() as tmpdir:
            template = self._make_template(tmpdir, content="<{{ project.v }}>")
            env = Environment()
            process_template(environment=env, template=template, project={"v": "yes"})
            with open(template["output_file"]) as f:
                self.assertEqual(f.read(), "<yes>")

    def test_template_with_none_project(self):
        # project=None -- template can still render (project is just None in context)
        with tempfile.TemporaryDirectory() as tmpdir:
            template = self._make_template(tmpdir, content="static content only")
            process_template(template=template, project=None)
            with open(template["output_file"]) as f:
                self.assertEqual(f.read(), "static content only")


if __name__ == '__main__':
    unittest.main()

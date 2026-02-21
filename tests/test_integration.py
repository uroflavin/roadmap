import unittest
import tempfile
import shutil
import os
import logging
from unittest.mock import patch

from roadmap_app.cli import main, render_templates
from roadmap_app.utils import read_roadmap_definition
from roadmap_app.rendering import validate_yaml
from roadmap_app.model import enrich_project


class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.test_existing_file = os.path.join(os.path.dirname(__file__), "roadmap.yml")
        self.schema_path = os.path.join(os.path.dirname(__file__), "..", "schema", "roadmap.json")
        self.env_file = os.path.join(os.path.dirname(__file__), "..", "config", "roadmap.env")
        self.template_path = os.path.join(os.path.dirname(__file__), "..", "templates")
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)
        # Reset logging handlers to prevent cross-test interference
        root_logger = logging.getLogger()
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
            handler.close()

    def _create_test_env_file(self, tmpdir):
        """Create a temporary .env file with logfile in the temp directory."""
        env_content = (
            f"SCHEMA=schema/roadmap.json\n"
            f"TEMPLATE_PATH=templates/\n"
            f'TEMPLATE_KNOWN_SUFFIXES=["md","html","dot","csv"]\n'
            f"OUTPUT_PATH={tmpdir}{os.sep}\n"
            f"LOGFILE={os.path.join(tmpdir, 'roadmap.log')}\n"
        )
        env_path = os.path.join(tmpdir, "roadmap.env")
        with open(env_path, "w") as f:
            f.write(env_content)
        return env_path

    def _run_main(self, extra_args=None):
        """Run main() with test fixture, temp output, and temp logfile."""
        env_path = self._create_test_env_file(self.tmpdir)
        output_dir = os.path.join(self.tmpdir, "output")
        argv = [
            "roadmap",
            "--roadmap-file", self.test_existing_file,
            "--output-dir", output_dir,
            "--environment", env_path,
        ]
        if extra_args:
            argv.extend(extra_args)
        with patch("sys.argv", argv):
            main()
        return output_dir

    # ── Group 1: Full pipeline via main() ──

    def test_main_produces_all_output_files(self):
        output_dir = self._run_main()
        expected_files = [
            "roadmap.html",
            "roadmap.csv",
            "roadmap.dot",
            "roadmap.md",
            os.path.join("kanban", "milestones.html"),
            os.path.join("kanban", "deliverables.html"),
        ]
        for filename in expected_files:
            filepath = os.path.join(output_dir, filename)
            self.assertTrue(os.path.exists(filepath), f"Missing output file: {filename}")
            self.assertGreater(os.path.getsize(filepath), 0, f"Empty output file: {filename}")

    def test_main_html_output_contains_project_data(self):
        output_dir = self._run_main()
        with open(os.path.join(output_dir, "roadmap.html"), "r") as f:
            html = f.read()
        # project title
        self.assertIn("Roadmap Unit-Test for roadmap.py", html)
        # author
        self.assertIn("Uroflavin", html)
        # milestone titles
        self.assertIn("Milestone 1 - title", html)
        self.assertIn("Milestone 2 - title", html)
        # objective titles
        self.assertIn("Objective 1 - title", html)
        self.assertIn("Objective 2 - title", html)
        # version
        self.assertIn(self.version_existing_roadmap, html)

    def test_main_markdown_output_contains_project_data(self):
        output_dir = self._run_main()
        with open(os.path.join(output_dir, "roadmap.md"), "r") as f:
            md = f.read()
        # project title
        self.assertIn("Roadmap Unit-Test for roadmap.py", md)
        # author
        self.assertIn("Uroflavin", md)
        # milestone titles
        self.assertIn("Milestone 1 - title", md)
        self.assertIn("Milestone 2 - title", md)
        # version
        self.assertIn(self.version_existing_roadmap, md)

    def test_main_csv_output_contains_key_value_pairs(self):
        output_dir = self._run_main()
        with open(os.path.join(output_dir, "roadmap.csv"), "r") as f:
            csv = f.read()
        # header
        self.assertIn("key", csv)
        self.assertIn("value", csv)
        # project title
        self.assertIn("Roadmap Unit-Test for roadmap.py", csv)
        # milestone data
        self.assertIn("Milestone 1 - title", csv)
        # objective data
        self.assertIn("Objective 1 - title", csv)

    def test_main_dot_output_contains_graph_structure(self):
        output_dir = self._run_main()
        with open(os.path.join(output_dir, "roadmap.dot"), "r") as f:
            dot = f.read()
        # graph declaration
        self.assertIn("digraph", dot)
        # version
        self.assertIn(self.version_existing_roadmap, dot)

    def test_main_kanban_outputs_contain_state_columns(self):
        output_dir = self._run_main()
        # milestones kanban
        with open(os.path.join(output_dir, "kanban", "milestones.html"), "r") as f:
            kanban_ms = f.read()
        self.assertIn("REACHED", kanban_ms)
        self.assertIn("PLANNED", kanban_ms)
        self.assertIn("Milestone 1 - title", kanban_ms)
        self.assertIn("Milestone 2 - title", kanban_ms)

        # deliverables kanban
        with open(os.path.join(output_dir, "kanban", "deliverables.html"), "r") as f:
            kanban_del = f.read()
        self.assertIn("Milestone 1 - Deliverable 1 - title", kanban_del)

    # ── Group 2: CLI argument variations ──

    def test_main_skip_items_removes_todos_from_output(self):
        output_dir = self._run_main(extra_args=["--skip-items", "milestones.todos"])
        with open(os.path.join(output_dir, "roadmap.html"), "r") as f:
            html = f.read()
        # milestone titles should still be there
        self.assertIn("Milestone 1 - title", html)
        self.assertIn("Milestone 2 - title", html)
        # milestone-level todos should be gone
        self.assertNotIn("M1 - Todo 1 - title", html)
        self.assertNotIn("M2 - Todo 1 - title", html)

    def test_main_skip_items_removes_milestones_section(self):
        output_dir = self._run_main(extra_args=["--skip-items", "milestones"])
        with open(os.path.join(output_dir, "roadmap.html"), "r") as f:
            html = f.read()
        # milestone content should be gone
        self.assertNotIn("Milestone 1 - title", html)
        self.assertNotIn("Milestone 2 - title", html)
        # objectives should remain
        self.assertIn("Objective 1 - title", html)

    # ── Group 3: Cross-module data flow (without main()) ──

    def test_validation_enrichment_pipeline(self):
        project = dict(read_roadmap_definition(self.test_existing_file))
        error, is_valid = validate_yaml(roadmap_data=project, path_to_json_schema=self.schema_path)
        self.assertTrue(is_valid, f"Schema validation failed: {error}")

        enrich_project(project, skip_items=None, roadmap_definition_file=self.test_existing_file)

        # IDs should be assigned
        self.assertIn("_id", project["milestones"][0])
        self.assertIn("_id", project["objectives"][0])
        # WSJF should be computed for deliverables with complete quantifiers
        self.assertIsNotNone(project["milestones"][0]["deliverables"][0]["quantifiers"]["weighted_shortest_job_first"])
        # meta should be present
        self.assertIn("meta", project)
        self.assertEqual(project["meta"]["version"], self.version_existing_roadmap)
        # grouping should be present
        self.assertIn("group", project)
        self.assertIn("timeline_by", project["group"])

    def test_enrichment_rendering_pipeline(self):
        from dotenv import dotenv_values
        project = dict(read_roadmap_definition(self.test_existing_file))
        enrich_project(project, skip_items=None, roadmap_definition_file=self.test_existing_file)

        config = dotenv_values(self.env_file)
        # override logfile to temp dir
        config["LOGFILE"] = os.path.join(self.tmpdir, "roadmap.log")
        output_folder = os.path.join(self.tmpdir, "output") + os.sep

        os.makedirs(output_folder, exist_ok=True)
        render_templates(project, config, output_folder, self.test_existing_file)

        # all output files should exist
        expected = ["roadmap.html", "roadmap.csv", "roadmap.dot", "roadmap.md"]
        for filename in expected:
            filepath = os.path.join(output_folder, filename)
            self.assertTrue(os.path.exists(filepath), f"Missing: {filename}")
            self.assertGreater(os.path.getsize(filepath), 0, f"Empty: {filename}")

    def test_hierarchical_ids_propagate_correctly(self):
        project = dict(read_roadmap_definition(self.test_existing_file))
        enrich_project(project, skip_items=None, roadmap_definition_file=self.test_existing_file)

        m1 = project["milestones"][0]
        # milestone ID
        self.assertEqual(m1["id"], "M1")
        self.assertEqual(m1["_id"], "m1")
        self.assertEqual(m1["_parent_id"], "")

        # first deliverable of M1
        d1 = m1["deliverables"][0]
        self.assertEqual(d1["id"], "D1")
        self.assertEqual(d1["_id"], "m1_d1")
        self.assertEqual(d1["_parent_id"], "m1")

        # first todo of first deliverable of M1
        todo1 = d1["todos"][0]
        self.assertEqual(todo1["id"], "TODO1")
        self.assertEqual(todo1["_id"], "m1_d1_todo1")
        self.assertEqual(todo1["_parent_id"], "m1_d1")

        # _previous_id: first element has empty, second element has first's _id
        self.assertEqual(m1["_previous_id"], "")
        m2 = project["milestones"][1]
        self.assertEqual(m2["_previous_id"], "m1")

    def test_wsjf_computed_for_all_elements(self):
        project = dict(read_roadmap_definition(self.test_existing_file))
        enrich_project(project, skip_items=None, roadmap_definition_file=self.test_existing_file)

        # check all deliverables across all milestones
        for m_idx, milestone in enumerate(project["milestones"]):
            for d_idx, deliverable in enumerate(milestone["deliverables"]):
                if "quantifiers" in deliverable:
                    q = deliverable["quantifiers"]
                    self.assertIsNotNone(
                        q.get("cost_of_delay"),
                        f"milestones[{m_idx}].deliverables[{d_idx}] missing cost_of_delay"
                    )
                    self.assertIsNotNone(
                        q.get("weighted_shortest_job_first"),
                        f"milestones[{m_idx}].deliverables[{d_idx}] missing wsjf"
                    )

        # check all keyresults across all objectives
        for o_idx, objective in enumerate(project["objectives"]):
            for k_idx, keyresult in enumerate(objective["keyresults"]):
                if "quantifiers" in keyresult:
                    q = keyresult["quantifiers"]
                    self.assertIsNotNone(
                        q.get("cost_of_delay"),
                        f"objectives[{o_idx}].keyresults[{k_idx}] missing cost_of_delay"
                    )
                    self.assertIsNotNone(
                        q.get("weighted_shortest_job_first"),
                        f"objectives[{o_idx}].keyresults[{k_idx}] missing wsjf"
                    )

    # ── Group 3b: Logo processing pipeline ──

    def test_logo_base64_embedding_and_copy(self):
        """Integration test for the full logo pipeline:
        base64 conversion into project dict, embedding in HTML, and file copy to output."""
        # Create a minimal 1x1 red PNG in a temp directory alongside a roadmap YAML
        import struct
        import zlib

        logo_dir = os.path.join(self.tmpdir, "logo_project")
        os.makedirs(logo_dir)

        # Minimal valid PNG: 1x1 pixel, red
        def _make_minimal_png():
            signature = b'\x89PNG\r\n\x1a\n'
            # IHDR: width=1, height=1, bit_depth=8, color_type=2 (RGB)
            ihdr_data = struct.pack('>IIBBBBB', 1, 1, 8, 2, 0, 0, 0)
            ihdr = _make_chunk(b'IHDR', ihdr_data)
            # IDAT: single row, filter byte 0, then R G B
            raw = b'\x00\xff\x00\x00'
            idat = _make_chunk(b'IDAT', zlib.compress(raw))
            iend = _make_chunk(b'IEND', b'')
            return signature + ihdr + idat + iend

        def _make_chunk(chunk_type, data):
            chunk = chunk_type + data
            return struct.pack('>I', len(data)) + chunk + struct.pack('>I', zlib.crc32(chunk) & 0xffffffff)

        logo_path = os.path.join(logo_dir, "test_logo.png")
        with open(logo_path, "wb") as f:
            f.write(_make_minimal_png())

        # Create a roadmap YAML with logo reference
        roadmap_path = os.path.join(logo_dir, "roadmap.yml")
        with open(roadmap_path, "w") as f:
            f.write(
                "title: Logo Test Project\n"
                "description: Testing logo pipeline\n"
                "logo:\n"
                "  filename: test_logo.png\n"
                "  copyright_notice: Test Copyright\n"
                "authors:\n"
                "  - name: Tester\n"
                "milestones:\n"
                "  - title: M1\n"
                "    description: Milestone 1\n"
                "    state: REACHED\n"
                "    deliverables:\n"
                "      - title: D1\n"
                "        state: DONE\n"
                "        requirement: MUST\n"
                "objectives:\n"
                "  - title: O1\n"
                "    description: Objective 1\n"
                "    state: ACTIVE\n"
                "    keyresults:\n"
                "      - title: KR1\n"
                "        state: DONE\n"
            )

        # Run the pipeline
        from dotenv import dotenv_values
        project = dict(read_roadmap_definition(roadmap_path))
        enrich_project(project, skip_items=None, roadmap_definition_file=roadmap_path)

        config = dotenv_values(self.env_file)
        config["LOGFILE"] = os.path.join(self.tmpdir, "roadmap.log")
        output_folder = os.path.join(self.tmpdir, "output") + os.sep
        os.makedirs(output_folder, exist_ok=True)

        render_templates(project, config, output_folder, roadmap_path)

        # 1. Base64 was injected into the project dict
        self.assertIn("base64", project["logo"])
        self.assertTrue(project["logo"]["base64"].startswith("data:image/png;base64,"))

        # 2. HTML output contains the base64 logo
        html_path = os.path.join(output_folder, "roadmap.html")
        with open(html_path, "r") as f:
            html = f.read()
        self.assertIn("data:image/png;base64,", html)
        self.assertIn("Test Copyright", html)

        # 3. Logo file was copied to output directory
        copied_logo = os.path.join(output_folder, "test_logo.png")
        self.assertTrue(os.path.exists(copied_logo), "Logo was not copied to output directory")
        # Verify it's a valid PNG (magic bytes)
        with open(copied_logo, "rb") as f:
            magic = f.read(4)
        self.assertEqual(magic, b'\x89PNG')

    # ── Group 4: Error scenarios ──

    def test_main_nonexistent_roadmap_file_raises_error(self):
        env_path = self._create_test_env_file(self.tmpdir)
        argv = [
            "roadmap",
            "--roadmap-file", "/nonexistent/roadmap.yml",
            "--output-dir", self.tmpdir,
            "--environment", env_path,
        ]
        with patch("sys.argv", argv):
            with self.assertRaises(ValueError):
                main()

    def test_main_nonexistent_env_file_raises_error(self):
        argv = [
            "roadmap",
            "--roadmap-file", self.test_existing_file,
            "--output-dir", self.tmpdir,
            "--environment", "/nonexistent/roadmap.env",
        ]
        with patch("sys.argv", argv):
            with self.assertRaises(ValueError):
                main()

    def test_main_invalid_yaml_returns_gracefully(self):
        # create an invalid YAML file (valid YAML but not a valid roadmap)
        invalid_yml = os.path.join(self.tmpdir, "invalid.yml")
        with open(invalid_yml, "w") as f:
            f.write("not_a_valid_key: value\n")
        env_path = self._create_test_env_file(self.tmpdir)
        output_dir = os.path.join(self.tmpdir, "output")
        argv = [
            "roadmap",
            "--roadmap-file", invalid_yml,
            "--output-dir", output_dir,
            "--environment", env_path,
        ]
        with patch("sys.argv", argv):
            main()
        # output directory may or may not exist, but no rendered files
        if os.path.exists(output_dir):
            rendered = [f for f in os.listdir(output_dir)
                        if f.endswith((".html", ".md", ".csv", ".dot"))]
            self.assertEqual(rendered, [], "Invalid YAML should produce no output files")

    # ── Group 5: Graphviz (conditional) ──

    @unittest.skipUnless(shutil.which("dot"), "graphviz not installed")
    def test_dot_to_png_conversion(self):
        output_dir = self._run_main()
        png_path = os.path.join(output_dir, "roadmap.dot.png")
        self.assertTrue(os.path.exists(png_path), "DOT-to-PNG file not created")
        # verify PNG magic bytes
        with open(png_path, "rb") as f:
            magic = f.read(8)
        self.assertEqual(magic[:4], b'\x89PNG', "File does not have valid PNG magic bytes")


if __name__ == '__main__':
    unittest.main()

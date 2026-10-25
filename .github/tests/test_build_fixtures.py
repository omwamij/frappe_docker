import importlib.util
import subprocess
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location(
    "minio_fixture", ROOT / "tests/minio_fixture.py"
)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class Fixtures(unittest.TestCase):
    def test_existing_fixture_not_rebuilt(self):
        with patch.object(
            m.subprocess, "run", return_value=subprocess.CompletedProcess([], 0)
        ), patch.object(m.subprocess, "check_call") as build:
            self.assertEqual(m.ensure_minio_fixture(), m.MINIO_IMAGE)
            build.assert_not_called()

    def test_missing_fixture_built_from_local_pinned_recipe(self):
        with patch.object(
            m.subprocess, "run", return_value=subprocess.CompletedProcess([], 1)
        ), patch.object(m.subprocess, "check_call") as build:
            m.ensure_minio_fixture()
            command = build.call_args.args[0]
            self.assertEqual(command[:2], ("docker", "build"))
            self.assertIn(m.MINIO_IMAGE, command)
            self.assertTrue(Path(command[-1]).parts[-2:] == ("tests", "minio"))

    def test_build_failure_propagates(self):
        with patch.object(
            m.subprocess, "run", return_value=subprocess.CompletedProcess([], 1)
        ), patch.object(
            m.subprocess,
            "check_call",
            side_effect=subprocess.CalledProcessError(1, ["docker", "build"]),
        ):
            with self.assertRaises(subprocess.CalledProcessError):
                m.ensure_minio_fixture()

    def test_v16_runtime_and_source_pin(self):
        source = (ROOT / ".github/workflows/build_stable.yml").read_text()
        v16 = source.split("  v16:")[1].split("  update_versions:")[0]
        self.assertIn("python_version: 3.14.9", v16)
        self.assertIn("node_version: 24.20.0", v16)
        recipe = (ROOT / "tests/minio/Dockerfile").read_text()
        self.assertIn(m.MINIO_SOURCE_COMMIT, recipe)
        self.assertIn("CGO_ENABLED=0", recipe)
        self.assertNotIn("minio/minio:latest", recipe)


if __name__ == "__main__":
    unittest.main()

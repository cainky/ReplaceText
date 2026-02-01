"""Tests for textswap."""

import json
import os
import stat
import unittest

from click.testing import CliRunner

from replace_text.replace_text import replace_text


class TestReplaceText(unittest.TestCase):
    """Core functionality tests."""

    def setUp(self):
        self.runner = CliRunner()
        self.test_folder = "test_folder"
        self.config_file = "config.json"

        os.makedirs(self.test_folder, exist_ok=True)
        with open(os.path.join(self.test_folder, "test1.txt"), "w") as f:
            f.write("Hello world")
        with open(os.path.join(self.test_folder, "test2.txt"), "w") as f:
            f.write("Python is awesome")

        config = {
            "dictionaries": {"test_dict": {"Hello": "Bonjour", "world": "monde", "Python": "Java"}},
            "ignore_extensions": [".ignore"],
            "ignore_directories": ["ignore_dir"],
            "ignore_file_prefixes": ["ignore_"],
        }
        with open(self.config_file, "w") as f:
            json.dump(config, f)

    def tearDown(self):
        for root, dirs, files in os.walk(self.test_folder, topdown=False):
            for name in files:
                file_path = os.path.join(root, name)
                # Reset permissions in case we made files read-only
                try:
                    os.chmod(file_path, stat.S_IRUSR | stat.S_IWUSR)
                except OSError:
                    pass
                os.remove(file_path)
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.test_folder)
        if os.path.exists(self.config_file):
            os.remove(self.config_file)

    def test_replace_text_keys_to_values(self):
        result = self.runner.invoke(
            replace_text,
            [
                "--direction",
                "1",
                "--folder",
                self.test_folder,
                "--dict-name",
                "test_dict",
            ],
        )
        self.assertEqual(result.exit_code, 0)

        with open(os.path.join(self.test_folder, "test1.txt")) as f:
            content = f.read()
        self.assertEqual(content, "Bonjour monde")

        with open(os.path.join(self.test_folder, "test2.txt")) as f:
            content = f.read()
        self.assertEqual(content, "Java is awesome")

    def test_replace_text_values_to_keys(self):
        self.runner.invoke(
            replace_text,
            [
                "--direction",
                "1",
                "--folder",
                self.test_folder,
                "--dict-name",
                "test_dict",
            ],
        )

        result = self.runner.invoke(
            replace_text,
            [
                "--direction",
                "2",
                "--folder",
                self.test_folder,
                "--dict-name",
                "test_dict",
            ],
        )
        self.assertEqual(result.exit_code, 0)

        with open(os.path.join(self.test_folder, "test1.txt")) as f:
            content = f.read()
        self.assertEqual(content, "Hello world")

        with open(os.path.join(self.test_folder, "test2.txt")) as f:
            content = f.read()
        self.assertEqual(content, "Python is awesome")

    def test_ignore_extensions(self):
        with open(os.path.join(self.test_folder, "test.ignore"), "w") as f:
            f.write("Hello world")

        result = self.runner.invoke(
            replace_text,
            [
                "--direction",
                "1",
                "--folder",
                self.test_folder,
                "--dict-name",
                "test_dict",
            ],
        )
        self.assertEqual(result.exit_code, 0)

        with open(os.path.join(self.test_folder, "test.ignore")) as f:
            content = f.read()
        self.assertEqual(content, "Hello world")

    def test_ignore_directories(self):
        os.makedirs(os.path.join(self.test_folder, "ignore_dir"), exist_ok=True)
        with open(os.path.join(self.test_folder, "ignore_dir", "test.txt"), "w") as f:
            f.write("Hello world")

        result = self.runner.invoke(
            replace_text,
            [
                "--direction",
                "1",
                "--folder",
                self.test_folder,
                "--dict-name",
                "test_dict",
            ],
        )
        self.assertEqual(result.exit_code, 0)

        with open(os.path.join(self.test_folder, "ignore_dir", "test.txt")) as f:
            content = f.read()
        self.assertEqual(content, "Hello world")

    def test_ignore_file_prefixes(self):
        with open(os.path.join(self.test_folder, "ignore_test.txt"), "w") as f:
            f.write("Hello world")

        result = self.runner.invoke(
            replace_text,
            [
                "--direction",
                "1",
                "--folder",
                self.test_folder,
                "--dict-name",
                "test_dict",
            ],
        )
        self.assertEqual(result.exit_code, 0)

        with open(os.path.join(self.test_folder, "ignore_test.txt")) as f:
            content = f.read()
        self.assertEqual(content, "Hello world")


class TestErrorHandling(unittest.TestCase):
    """Tests for error conditions."""

    def setUp(self):
        self.runner = CliRunner()
        self.test_folder = "test_folder_errors"
        self.config_file = "config_errors.json"
        os.makedirs(self.test_folder, exist_ok=True)

    def tearDown(self):
        for root, dirs, files in os.walk(self.test_folder, topdown=False):
            for name in files:
                file_path = os.path.join(root, name)
                try:
                    os.chmod(file_path, stat.S_IRUSR | stat.S_IWUSR)
                except OSError:
                    pass
                try:
                    os.remove(file_path)
                except OSError:
                    pass
            for name in dirs:
                try:
                    os.rmdir(os.path.join(root, name))
                except OSError:
                    pass
        try:
            os.rmdir(self.test_folder)
        except OSError:
            pass
        if os.path.exists(self.config_file):
            os.remove(self.config_file)

    def test_invalid_json_config(self):
        """Test handling of malformed JSON config."""
        with open(self.config_file, "w") as f:
            f.write("{ invalid json }")

        result = self.runner.invoke(
            replace_text,
            [
                "--config",
                self.config_file,
                "--direction",
                "1",
                "--folder",
                self.test_folder,
            ],
        )
        self.assertEqual(result.exit_code, 1)
        self.assertIn("Invalid JSON", result.output)

    def test_missing_dictionaries_key(self):
        """Test handling of config without dictionaries."""
        with open(self.config_file, "w") as f:
            json.dump({"other_key": "value"}, f)

        result = self.runner.invoke(
            replace_text,
            [
                "--config",
                self.config_file,
                "--direction",
                "1",
                "--folder",
                self.test_folder,
            ],
        )
        self.assertEqual(result.exit_code, 1)
        self.assertIn("dictionaries", result.output.lower())

    def test_empty_dictionaries(self):
        """Test handling of empty dictionaries object."""
        with open(self.config_file, "w") as f:
            json.dump({"dictionaries": {}}, f)

        result = self.runner.invoke(
            replace_text,
            [
                "--config",
                self.config_file,
                "--direction",
                "1",
                "--folder",
                self.test_folder,
            ],
        )
        self.assertEqual(result.exit_code, 1)
        self.assertIn("No dictionaries found", result.output)

    def test_nonexistent_dictionary_name(self):
        """Test handling of non-existent dictionary name."""
        with open(self.config_file, "w") as f:
            json.dump({"dictionaries": {"real_dict": {"a": "b"}}}, f)

        result = self.runner.invoke(
            replace_text,
            [
                "--config",
                self.config_file,
                "--direction",
                "1",
                "--folder",
                self.test_folder,
                "--dict-name",
                "fake_dict",
            ],
        )
        self.assertEqual(result.exit_code, 1)
        self.assertIn("not found", result.output)

    def test_empty_folder(self):
        """Test processing an empty folder."""
        with open(self.config_file, "w") as f:
            json.dump({"dictionaries": {"test": {"a": "b"}}}, f)

        result = self.runner.invoke(
            replace_text,
            [
                "--config",
                self.config_file,
                "--direction",
                "1",
                "--folder",
                self.test_folder,
                "--dict-name",
                "test",
            ],
        )
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Processed 0 files", result.output)

    def test_non_utf8_file_skipped(self):
        """Test that non-UTF8 files are skipped with warning."""
        with open(self.config_file, "w") as f:
            json.dump({"dictionaries": {"test": {"Hello": "World"}}}, f)

        # Create a file with invalid UTF-8 bytes
        binary_file = os.path.join(self.test_folder, "binary.txt")
        with open(binary_file, "wb") as f:
            f.write(b"\x80\x81\x82\x83 invalid utf8")

        result = self.runner.invoke(
            replace_text,
            [
                "--config",
                self.config_file,
                "--direction",
                "1",
                "--folder",
                self.test_folder,
                "--dict-name",
                "test",
            ],
        )
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Skipped", result.output)
        self.assertIn("UTF-8", result.output)


class TestDryRun(unittest.TestCase):
    """Tests for dry-run functionality."""

    def setUp(self):
        self.runner = CliRunner()
        self.test_folder = "test_folder_dryrun"
        self.config_file = "config_dryrun.json"

        os.makedirs(self.test_folder, exist_ok=True)
        with open(os.path.join(self.test_folder, "test.txt"), "w") as f:
            f.write("Hello world")

        config = {"dictionaries": {"test": {"Hello": "Goodbye"}}}
        with open(self.config_file, "w") as f:
            json.dump(config, f)

    def tearDown(self):
        for root, dirs, files in os.walk(self.test_folder, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.test_folder)
        os.remove(self.config_file)

    def test_dry_run_does_not_modify_files(self):
        """Test that dry-run doesn't actually change files."""
        result = self.runner.invoke(
            replace_text,
            [
                "--config",
                self.config_file,
                "--direction",
                "1",
                "--folder",
                self.test_folder,
                "--dict-name",
                "test",
                "--dry-run",
            ],
        )
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Dry run mode", result.output)
        self.assertIn("Would modify", result.output)

        # Verify file was NOT modified
        with open(os.path.join(self.test_folder, "test.txt")) as f:
            content = f.read()
        self.assertEqual(content, "Hello world")

    def test_dry_run_shows_diff(self):
        """Test that dry-run shows the diff of changes."""
        result = self.runner.invoke(
            replace_text,
            [
                "--config",
                self.config_file,
                "--direction",
                "1",
                "--folder",
                self.test_folder,
                "--dict-name",
                "test",
                "--dry-run",
            ],
        )
        self.assertEqual(result.exit_code, 0)
        # Diff should show the change
        self.assertIn("-Hello world", result.output)
        self.assertIn("+Goodbye world", result.output)


class TestEdgeCases(unittest.TestCase):
    """Tests for edge cases."""

    def setUp(self):
        self.runner = CliRunner()
        self.test_folder = "test_folder_edge"
        self.config_file = "config_edge.json"
        os.makedirs(self.test_folder, exist_ok=True)

    def tearDown(self):
        for root, dirs, files in os.walk(self.test_folder, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.test_folder)
        if os.path.exists(self.config_file):
            os.remove(self.config_file)

    def test_overlapping_keys(self):
        """Test behavior with overlapping replacement keys."""
        with open(os.path.join(self.test_folder, "test.txt"), "w") as f:
            f.write("hello hello world")

        # Note: replacements are applied in dict order
        config = {"dictionaries": {"test": {"hello": "hi", "hello world": "goodbye"}}}
        with open(self.config_file, "w") as f:
            json.dump(config, f)

        result = self.runner.invoke(
            replace_text,
            [
                "--config",
                self.config_file,
                "--direction",
                "1",
                "--folder",
                self.test_folder,
                "--dict-name",
                "test",
            ],
        )
        self.assertEqual(result.exit_code, 0)

        # Both 'hello' occurrences get replaced first, then 'hello world' can't match
        with open(os.path.join(self.test_folder, "test.txt")) as f:
            content = f.read()
        self.assertEqual(content, "hi hi world")

    def test_empty_replacement_value(self):
        """Test replacement with empty string (deletion)."""
        with open(os.path.join(self.test_folder, "test.txt"), "w") as f:
            f.write("remove this word please")

        config = {"dictionaries": {"test": {"this ": ""}}}
        with open(self.config_file, "w") as f:
            json.dump(config, f)

        result = self.runner.invoke(
            replace_text,
            [
                "--config",
                self.config_file,
                "--direction",
                "1",
                "--folder",
                self.test_folder,
                "--dict-name",
                "test",
            ],
        )
        self.assertEqual(result.exit_code, 0)

        with open(os.path.join(self.test_folder, "test.txt")) as f:
            content = f.read()
        self.assertEqual(content, "remove word please")

    def test_nested_directories(self):
        """Test processing nested directory structures."""
        nested_path = os.path.join(self.test_folder, "level1", "level2", "level3")
        os.makedirs(nested_path, exist_ok=True)

        with open(os.path.join(nested_path, "deep.txt"), "w") as f:
            f.write("Hello from deep")

        config = {"dictionaries": {"test": {"Hello": "Hi"}}}
        with open(self.config_file, "w") as f:
            json.dump(config, f)

        result = self.runner.invoke(
            replace_text,
            [
                "--config",
                self.config_file,
                "--direction",
                "1",
                "--folder",
                self.test_folder,
                "--dict-name",
                "test",
            ],
        )
        self.assertEqual(result.exit_code, 0)

        with open(os.path.join(nested_path, "deep.txt")) as f:
            content = f.read()
        self.assertEqual(content, "Hi from deep")

    def test_file_with_no_matches(self):
        """Test file that has no matching patterns."""
        with open(os.path.join(self.test_folder, "nomatch.txt"), "w") as f:
            f.write("Nothing to replace here")

        config = {"dictionaries": {"test": {"xyz": "abc"}}}
        with open(self.config_file, "w") as f:
            json.dump(config, f)

        result = self.runner.invoke(
            replace_text,
            [
                "--config",
                self.config_file,
                "--direction",
                "1",
                "--folder",
                self.test_folder,
                "--dict-name",
                "test",
            ],
        )
        self.assertEqual(result.exit_code, 0)
        self.assertIn("0 modified", result.output)

        # File should be unchanged
        with open(os.path.join(self.test_folder, "nomatch.txt")) as f:
            content = f.read()
        self.assertEqual(content, "Nothing to replace here")

    def test_auto_select_single_dictionary(self):
        """Test automatic dictionary selection when only one exists."""
        with open(os.path.join(self.test_folder, "test.txt"), "w") as f:
            f.write("Hello")

        config = {"dictionaries": {"only_one": {"Hello": "Hi"}}}
        with open(self.config_file, "w") as f:
            json.dump(config, f)

        result = self.runner.invoke(
            replace_text,
            [
                "--config",
                self.config_file,
                "--direction",
                "1",
                "--folder",
                self.test_folder,
                # Note: no --dict-name provided
            ],
        )
        self.assertEqual(result.exit_code, 0)
        self.assertIn("Using dictionary: only_one", result.output)


if __name__ == "__main__":
    unittest.main()

import os
import unittest
from unittest.mock import patch, mock_open, call
from click.testing import CliRunner
from replace_text.replace_text import replace_text


class TestReplaceText(unittest.TestCase):
    def assert_path_any_call(self, mock_obj, expected_path, mode, encoding):
        normalized_expected_path = os.path.normpath(expected_path)
        for mock_call in mock_obj.call_args_list:
            args, kwargs = mock_call
            if len(args) >= 1:
                normalized_actual_path = os.path.normpath(args[0])
                if (
                    normalized_actual_path == normalized_expected_path
                    and args[1] == mode
                    and kwargs.get("encoding") == encoding
                ):
                    return
        raise AssertionError(
            f"Expected call not found: open('{normalized_expected_path}', '{mode}', encoding='{encoding}')"
        )

    @patch("builtins.open", new_callable=mock_open, read_data="key1 content key2")
    @patch("os.walk")
    @patch("json.load")
    def test_replace_text_keys_to_values_single_dict(
        self, mock_json_load, mock_os_walk, mock_file
    ):
        mock_json_load.return_value = {
            "dictionaries": {
                "example1": {"key1": "value1", "key2": "value2", "key3": "value3"}
            },
            "ignore_extensions": [".png", ".jpg"],
        }
        mock_os_walk.return_value = [
            ("/mocked/path", ("subdir",), ("file1.txt", "file2.jpg"))
        ]

        runner = CliRunner()
        result = runner.invoke(
            replace_text,
            ["--direction", "1", "--folder", "/mocked/path", "--dict-name", "example1"],
        )

        self.assert_path_any_call(mock_file, "/mocked/path/file1.txt", "r", "utf-8")
        self.assert_path_any_call(mock_file, "/mocked/path/file1.txt", "w", "utf-8")
        mock_file().write.assert_called_with("value1 content value2")
        self.assertEqual(result.exit_code, 0)

    @patch("builtins.open", new_callable=mock_open, read_data="value1 content value2")
    @patch("os.walk")
    @patch("json.load")
    def test_replace_text_values_to_keys_multiple_dicts(
        self, mock_json_load, mock_os_walk, mock_file
    ):
        mock_json_load.return_value = {
            "dictionaries": {
                "example1": {"key1": "value1", "key2": "value2", "key3": "value3"},
                "example2": {"hello": "world", "foo": "bar", "python": "rocks"},
            },
            "ignore_extensions": [".png", ".jpg"],
        }
        mock_os_walk.return_value = [
            ("/mocked/path", ("subdir",), ("file1.txt", "file2.jpg"))
        ]

        runner = CliRunner()
        result = runner.invoke(
            replace_text,
            ["--direction", "2", "--folder", "/mocked/path", "--dict-name", "example1"],
        )

        self.assert_path_any_call(mock_file, "/mocked/path/file1.txt", "r", "utf-8")
        self.assert_path_any_call(mock_file, "/mocked/path/file1.txt", "w", "utf-8")
        mock_file().write.assert_called_with("key1 content key2")
        self.assertEqual(result.exit_code, 0)

    @patch("builtins.open", new_callable=mock_open, read_data="hello content foo")
    @patch("os.walk")
    @patch("json.load")
    def test_replace_text_with_dict_name_flag(
        self, mock_json_load, mock_os_walk, mock_file
    ):
        mock_json_load.return_value = {
            "dictionaries": {
                "example1": {"key1": "value1", "key2": "value2", "key3": "value3"},
                "example2": {"hello": "world", "foo": "bar", "python": "rocks"},
            },
            "ignore_extensions": [".png", ".jpg"],
        }
        mock_os_walk.return_value = [
            ("/mocked/path", ("subdir",), ("file1.txt", "file2.jpg"))
        ]

        runner = CliRunner()
        result = runner.invoke(
            replace_text,
            ["--direction", "1", "--folder", "/mocked/path", "--dict-name", "example2"],
        )

        self.assert_path_any_call(mock_file, "/mocked/path/file1.txt", "r", "utf-8")
        self.assert_path_any_call(mock_file, "/mocked/path/file1.txt", "w", "utf-8")
        mock_file().write.assert_called_with("world content bar")
        self.assertEqual(result.exit_code, 0)


if __name__ == "__main__":
    unittest.main()

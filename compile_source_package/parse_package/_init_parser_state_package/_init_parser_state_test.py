#!/usr/bin/env python3
"""Unit tests for _init_parser_state function."""

import unittest

from ._init_parser_state_src import _init_parser_state


class TestInitParserState(unittest.TestCase):
    """Test cases for _init_parser_state function."""

    def test_basic_initialization(self):
        """Test basic initialization with simple tokens."""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            {"type": "OPERATOR", "value": "=", "line": 1, "column": 3},
            {"type": "NUMBER", "value": "42", "line": 1, "column": 5},
        ]
        filename = "test.py"

        result = _init_parser_state(tokens, filename)

        self.assertEqual(result["tokens"], tokens)
        self.assertEqual(result["pos"], 0)
        self.assertEqual(result["filename"], filename)

    def test_empty_tokens_list(self):
        """Test initialization with empty tokens list."""
        tokens = []
        filename = "empty.py"

        result = _init_parser_state(tokens, filename)

        self.assertEqual(result["tokens"], [])
        self.assertEqual(result["pos"], 0)
        self.assertEqual(result["filename"], filename)
        self.assertEqual(len(result), 3)

    def test_single_token(self):
        """Test initialization with single token."""
        tokens = [{"type": "KEYWORD", "value": "if", "line": 10, "column": 1}]
        filename = "single.py"

        result = _init_parser_state(tokens, filename)

        self.assertEqual(len(result["tokens"]), 1)
        self.assertEqual(result["tokens"][0]["type"], "KEYWORD")
        self.assertEqual(result["tokens"][0]["value"], "if")
        self.assertEqual(result["pos"], 0)
        self.assertEqual(result["filename"], filename)

    def test_tokens_with_special_characters(self):
        """Test tokens containing special characters in values."""
        tokens = [
            {"type": "STRING", "value": "hello\nworld", "line": 1, "column": 1},
            {"type": "STRING", "value": "tab\there", "line": 2, "column": 1},
        ]
        filename = "special.py"

        result = _init_parser_state(tokens, filename)

        self.assertEqual(result["tokens"], tokens)
        self.assertEqual(result["pos"], 0)

    def test_filename_with_path(self):
        """Test with filename containing path separators."""
        tokens = [{"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}]
        filename = "/path/to/nested/file.py"

        result = _init_parser_state(tokens, filename)

        self.assertEqual(result["filename"], "/path/to/nested/file.py")
        self.assertEqual(result["pos"], 0)

    def test_unicode_filename(self):
        """Test with unicode characters in filename."""
        tokens = []
        filename = "测试文件.py"

        result = _init_parser_state(tokens, filename)

        self.assertEqual(result["filename"], "测试文件.py")
        self.assertEqual(result["tokens"], [])

    def test_pos_always_zero(self):
        """Verify pos is always initialized to 0 regardless of input."""
        tokens = [{"type": "X", "value": "x", "line": 1, "column": 1}]

        result = _init_parser_state(tokens, "test.py")

        self.assertEqual(result["pos"], 0)
        self.assertIsInstance(result["pos"], int)

    def test_returns_new_dict(self):
        """Verify function returns a new dictionary (not reference to input)."""
        tokens = [{"type": "X", "value": "x", "line": 1, "column": 1}]
        filename = "test.py"

        result1 = _init_parser_state(tokens, filename)
        result2 = _init_parser_state(tokens, filename)

        self.assertIsNot(result1, result2)
        result1["pos"] = 999
        self.assertEqual(result2["pos"], 0)

    def test_tokens_reference_preserved(self):
        """Verify tokens list reference is preserved (shallow copy behavior)."""
        tokens = [{"type": "X", "value": "x", "line": 1, "column": 1}]
        filename = "test.py"

        result = _init_parser_state(tokens, filename)

        self.assertIs(result["tokens"], tokens)

    def test_multiple_tokens_various_types(self):
        """Test with many tokens of various types."""
        tokens = [
            {"type": f"TYPE_{i}", "value": f"val_{i}", "line": i, "column": i * 2}
            for i in range(50)
        ]
        filename = "multi.py"

        result = _init_parser_state(tokens, filename)

        self.assertEqual(len(result["tokens"]), 50)
        self.assertEqual(result["pos"], 0)
        self.assertEqual(result["filename"], filename)
        self.assertEqual(result["tokens"][0]["type"], "TYPE_0")
        self.assertEqual(result["tokens"][49]["type"], "TYPE_49")

    def test_return_type_is_dict(self):
        """Verify return type is dictionary."""
        tokens = []
        filename = "test.py"

        result = _init_parser_state(tokens, filename)

        self.assertIsInstance(result, dict)

    def test_all_required_keys_present(self):
        """Verify all required keys are present in returned dict."""
        tokens = [{"type": "X", "value": "x", "line": 1, "column": 1}]
        filename = "test.py"

        result = _init_parser_state(tokens, filename)

        self.assertIn("tokens", result)
        self.assertIn("pos", result)
        self.assertIn("filename", result)
        self.assertEqual(len(result), 3)


if __name__ == "__main__":
    unittest.main()

# -*- coding: utf-8 -*-
"""
Unit tests for _build_error_node function.
Tests ERROR AST node creation and parser_state mutation.
"""

import unittest
from typing import Dict, Any

# Relative import from the same package
from ._build_error_node_src import _build_error_node


class TestBuildErrorNode(unittest.TestCase):
    """Test cases for _build_error_node function."""

    def test_build_error_node_basic(self):
        """Test basic ERROR node creation with standard inputs."""
        parser_state: Dict[str, Any] = {
            "tokens": [],
            "pos": 0,
            "filename": "test.cc"
        }
        message = "Unexpected token"
        line = 10
        column = 5

        result = _build_error_node(parser_state, message, line, column)

        # Verify return value
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], message)
        self.assertEqual(result["line"], line)
        self.assertEqual(result["column"], column)

        # Verify side effect: parser_state mutation
        self.assertEqual(parser_state["error"], "解析失败")

    def test_build_error_node_empty_message(self):
        """Test ERROR node creation with empty message."""
        parser_state: Dict[str, Any] = {"pos": 0}
        message = ""
        line = 1
        column = 1

        result = _build_error_node(parser_state, message, line, column)

        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], "")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["error"], "解析失败")

    def test_build_error_node_special_characters_in_message(self):
        """Test ERROR node creation with special characters in message."""
        parser_state: Dict[str, Any] = {"pos": 0}
        message = "Error: expected ';' but found ':' at line 10"
        line = 10
        column = 20

        result = _build_error_node(parser_state, message, line, column)

        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], message)
        self.assertEqual(result["line"], line)
        self.assertEqual(result["column"], column)
        self.assertEqual(parser_state["error"], "解析失败")

    def test_build_error_node_unicode_message(self):
        """Test ERROR node creation with unicode characters in message."""
        parser_state: Dict[str, Any] = {"pos": 0}
        message = "错误：无效的语法"
        line = 5
        column = 3

        result = _build_error_node(parser_state, message, line, column)

        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], message)
        self.assertEqual(result["line"], line)
        self.assertEqual(result["column"], column)
        self.assertEqual(parser_state["error"], "解析失败")

    def test_build_error_node_zero_line_column(self):
        """Test ERROR node creation with zero line and column values."""
        parser_state: Dict[str, Any] = {"pos": 0}
        message = "Error at start"
        line = 0
        column = 0

        result = _build_error_node(parser_state, message, line, column)

        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], message)
        self.assertEqual(result["line"], 0)
        self.assertEqual(result["column"], 0)
        self.assertEqual(parser_state["error"], "解析失败")

    def test_build_error_node_large_line_column(self):
        """Test ERROR node creation with large line and column values."""
        parser_state: Dict[str, Any] = {"pos": 0}
        message = "Error"
        line = 99999
        column = 88888

        result = _build_error_node(parser_state, message, line, column)

        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], message)
        self.assertEqual(result["line"], line)
        self.assertEqual(result["column"], column)
        self.assertEqual(parser_state["error"], "解析失败")

    def test_build_error_node_preserves_other_parser_state_fields(self):
        """Test that other parser_state fields are preserved after mutation."""
        parser_state: Dict[str, Any] = {
            "tokens": [{"type": "ID", "value": "x"}],
            "pos": 5,
            "filename": "main.cc",
            "existing_field": "existing_value"
        }

        result = _build_error_node(parser_state, "Error", 1, 1)

        # Verify error field was added
        self.assertEqual(parser_state["error"], "解析失败")

        # Verify other fields are preserved
        self.assertEqual(parser_state["tokens"], [{"type": "ID", "value": "x"}])
        self.assertEqual(parser_state["pos"], 5)
        self.assertEqual(parser_state["filename"], "main.cc")
        self.assertEqual(parser_state["existing_field"], "existing_value")

    def test_build_error_node_overwrites_existing_error_field(self):
        """Test that existing error field in parser_state is overwritten."""
        parser_state: Dict[str, Any] = {
            "pos": 0,
            "error": "Previous error"
        }

        result = _build_error_node(parser_state, "New error", 1, 1)

        # Verify error field was overwritten
        self.assertEqual(parser_state["error"], "解析失败")

    def test_build_error_node_multiple_calls(self):
        """Test multiple calls to _build_error_node on same parser_state."""
        parser_state: Dict[str, Any] = {"pos": 0}

        result1 = _build_error_node(parser_state, "First error", 1, 1)
        result2 = _build_error_node(parser_state, "Second error", 2, 2)

        # Verify both results are correct
        self.assertEqual(result1["type"], "ERROR")
        self.assertEqual(result1["value"], "First error")
        self.assertEqual(result1["line"], 1)
        self.assertEqual(result1["column"], 1)

        self.assertEqual(result2["type"], "ERROR")
        self.assertEqual(result2["value"], "Second error")
        self.assertEqual(result2["line"], 2)
        self.assertEqual(result2["column"], 2)

        # Verify parser_state error is set (to last call's effect)
        self.assertEqual(parser_state["error"], "解析失败")

    def test_build_error_node_returns_new_dict_each_call(self):
        """Test that each call returns a new dict object."""
        parser_state: Dict[str, Any] = {"pos": 0}

        result1 = _build_error_node(parser_state, "Error 1", 1, 1)
        result2 = _build_error_node(parser_state, "Error 2", 2, 2)

        # Verify they are different objects
        self.assertIsNot(result1, result2)

        # Verify modifying one doesn't affect the other
        result1["value"] = "Modified"
        self.assertEqual(result2["value"], "Error 2")

    def test_build_error_node_negative_line_column(self):
        """Test ERROR node creation with negative line and column values."""
        parser_state: Dict[str, Any] = {"pos": 0}
        message = "Error"
        line = -1
        column = -5

        result = _build_error_node(parser_state, message, line, column)

        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], message)
        self.assertEqual(result["line"], line)
        self.assertEqual(result["column"], column)
        self.assertEqual(parser_state["error"], "解析失败")

    def test_build_error_node_parser_state_initially_empty(self):
        """Test ERROR node creation with initially empty parser_state."""
        parser_state: Dict[str, Any] = {}

        result = _build_error_node(parser_state, "Error", 1, 1)

        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(parser_state["error"], "解析失败")
        self.assertEqual(len(parser_state), 1)  # Only error field added


if __name__ == "__main__":
    unittest.main()

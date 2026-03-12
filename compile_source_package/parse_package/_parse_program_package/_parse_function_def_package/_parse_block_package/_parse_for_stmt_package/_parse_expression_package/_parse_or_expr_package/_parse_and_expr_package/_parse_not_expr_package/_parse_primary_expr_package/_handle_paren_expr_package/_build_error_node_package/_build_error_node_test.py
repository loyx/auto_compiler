# -*- coding: utf-8 -*-
"""Unit tests for _build_error_node function."""

import unittest
from typing import Any, Dict

# Relative import from the same package
from ._build_error_node_src import _build_error_node


class TestBuildErrorNode(unittest.TestCase):
    """Test cases for _build_error_node function."""

    def test_build_error_node_basic(self):
        """Test basic error node creation with normal inputs."""
        parser_state: Dict[str, Any] = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }
        message = "Unexpected token"
        line = 10
        column = 5

        result = _build_error_node(parser_state, message, line, column)

        # Verify return structure
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], message)
        self.assertEqual(result["line"], line)
        self.assertEqual(result["column"], column)
        self.assertEqual(result["children"], [])

        # Verify parser_state mutation
        self.assertEqual(parser_state["error"], "解析失败")

    def test_build_error_node_mutates_parser_state(self):
        """Test that parser_state['error'] is set correctly."""
        parser_state: Dict[str, Any] = {
            "tokens": [{"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}],
            "pos": 1,
            "filename": "main.py"
        }

        _build_error_node(parser_state, "Some error", 1, 1)

        self.assertIn("error", parser_state)
        self.assertEqual(parser_state["error"], "解析失败")

    def test_build_error_node_empty_message(self):
        """Test error node with empty message."""
        parser_state: Dict[str, Any] = {}
        message = ""
        line = 1
        column = 1

        result = _build_error_node(parser_state, message, line, column)

        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], "")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["error"], "解析失败")

    def test_build_error_node_long_message(self):
        """Test error node with very long error message."""
        parser_state: Dict[str, Any] = {}
        message = "Error: " + "x" * 1000
        line = 999
        column = 999

        result = _build_error_node(parser_state, message, line, column)

        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], message)
        self.assertEqual(result["line"], 999)
        self.assertEqual(result["column"], 999)
        self.assertEqual(parser_state["error"], "解析失败")

    def test_build_error_node_zero_line_column(self):
        """Test error node with zero line and column numbers."""
        parser_state: Dict[str, Any] = {}

        result = _build_error_node(parser_state, "Error", 0, 0)

        self.assertEqual(result["line"], 0)
        self.assertEqual(result["column"], 0)
        self.assertEqual(parser_state["error"], "解析失败")

    def test_build_error_node_negative_line_column(self):
        """Test error node with negative line and column numbers."""
        parser_state: Dict[str, Any] = {}

        result = _build_error_node(parser_state, "Error", -1, -5)

        self.assertEqual(result["line"], -1)
        self.assertEqual(result["column"], -5)
        self.assertEqual(parser_state["error"], "解析失败")

    def test_build_error_node_unicode_message(self):
        """Test error node with unicode characters in message."""
        parser_state: Dict[str, Any] = {}
        message = "语法错误：意外的符号 'αβγ'"

        result = _build_error_node(parser_state, message, 5, 10)

        self.assertEqual(result["value"], message)
        self.assertEqual(parser_state["error"], "解析失败")

    def test_build_error_node_preserves_other_parser_state_fields(self):
        """Test that other parser_state fields are preserved."""
        parser_state: Dict[str, Any] = {
            "tokens": [{"type": "NUMBER", "value": "42", "line": 1, "column": 1}],
            "pos": 5,
            "filename": "test.py",
            "existing_field": "should_remain"
        }

        _build_error_node(parser_state, "Error", 1, 1)

        self.assertEqual(parser_state["tokens"][0]["type"], "NUMBER")
        self.assertEqual(parser_state["pos"], 5)
        self.assertEqual(parser_state["filename"], "test.py")
        self.assertEqual(parser_state["existing_field"], "should_remain")
        self.assertEqual(parser_state["error"], "解析失败")

    def test_build_error_node_returns_new_dict(self):
        """Test that returned error node is independent from parser_state."""
        parser_state: Dict[str, Any] = {"tokens": []}

        result = _build_error_node(parser_state, "Error", 1, 1)

        # Modifying result should not affect parser_state
        result["type"] = "MODIFIED"
        self.assertEqual(parser_state.get("error"), "解析失败")
        self.assertNotIn("type", parser_state)

    def test_build_error_node_children_is_empty_list(self):
        """Test that children field is an empty list, not None or other falsy value."""
        parser_state: Dict[str, Any] = {}

        result = _build_error_node(parser_state, "Error", 1, 1)

        self.assertIsInstance(result["children"], list)
        self.assertEqual(len(result["children"]), 0)
        self.assertIsNotNone(result["children"])


if __name__ == "__main__":
    unittest.main()

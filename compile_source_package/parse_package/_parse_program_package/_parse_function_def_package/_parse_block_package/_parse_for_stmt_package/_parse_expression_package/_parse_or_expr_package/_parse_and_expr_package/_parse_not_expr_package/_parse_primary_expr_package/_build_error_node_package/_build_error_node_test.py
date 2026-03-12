# -*- coding: utf-8 -*-
"""
Unit tests for _build_error_node function.
"""

import unittest
from typing import Dict, Any

# Relative import from the same package
from ._build_error_node_src import _build_error_node


class TestBuildErrorNode(unittest.TestCase):
    """Test cases for _build_error_node function."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.parser_state: Dict[str, Any] = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }

    def tearDown(self) -> None:
        """Clean up after tests."""
        pass

    def test_build_error_node_basic(self) -> None:
        """Test basic ERROR node creation with standard inputs."""
        message = "Unexpected token"
        line = 10
        column = 5

        result = _build_error_node(self.parser_state, message, line, column)

        # Verify returned node structure
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], message)
        self.assertEqual(result["line"], line)
        self.assertEqual(result["column"], column)

        # Verify side effect: parser_state error flag is set
        self.assertEqual(self.parser_state["error"], "解析失败")

    def test_build_error_node_empty_message(self) -> None:
        """Test ERROR node creation with empty message."""
        message = ""
        line = 1
        column = 1

        result = _build_error_node(self.parser_state, message, line, column)

        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], "")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(self.parser_state["error"], "解析失败")

    def test_build_error_node_unicode_message(self) -> None:
        """Test ERROR node creation with Unicode message."""
        message = "语法错误：意外的符号"
        line = 25
        column = 12

        result = _build_error_node(self.parser_state, message, line, column)

        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], message)
        self.assertEqual(result["line"], 25)
        self.assertEqual(result["column"], 12)
        self.assertEqual(self.parser_state["error"], "解析失败")

    def test_build_error_node_large_line_column(self) -> None:
        """Test ERROR node creation with large line and column numbers."""
        message = "Error at end of file"
        line = 99999
        column = 88888

        result = _build_error_node(self.parser_state, message, line, column)

        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], message)
        self.assertEqual(result["line"], 99999)
        self.assertEqual(result["column"], 88888)
        self.assertEqual(self.parser_state["error"], "解析失败")

    def test_build_error_node_zero_line_column(self) -> None:
        """Test ERROR node creation with zero line and column."""
        message = "Initial error"
        line = 0
        column = 0

        result = _build_error_node(self.parser_state, message, line, column)

        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], message)
        self.assertEqual(result["line"], 0)
        self.assertEqual(result["column"], 0)
        self.assertEqual(self.parser_state["error"], "解析失败")

    def test_build_error_node_negative_line_column(self) -> None:
        """Test ERROR node creation with negative line and column."""
        message = "Invalid position"
        line = -1
        column = -5

        result = _build_error_node(self.parser_state, message, line, column)

        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], message)
        self.assertEqual(result["line"], -1)
        self.assertEqual(result["column"], -5)
        self.assertEqual(self.parser_state["error"], "解析失败")

    def test_build_error_node_parser_state_modified(self) -> None:
        """Test that parser_state is modified in place."""
        original_state = self.parser_state.copy()
        message = "Test error"
        line = 5
        column = 3

        _build_error_node(self.parser_state, message, line, column)

        # Verify parser_state was modified
        self.assertIn("error", self.parser_state)
        self.assertEqual(self.parser_state["error"], "解析失败")
        # Verify other fields remain unchanged
        self.assertEqual(self.parser_state["tokens"], original_state["tokens"])
        self.assertEqual(self.parser_state["pos"], original_state["pos"])
        self.assertEqual(self.parser_state["filename"], original_state["filename"])

    def test_build_error_node_multiple_calls(self) -> None:
        """Test multiple calls to _build_error_node."""
        message1 = "First error"
        message2 = "Second error"

        result1 = _build_error_node(self.parser_state, message1, 1, 1)
        result2 = _build_error_node(self.parser_state, message2, 2, 2)

        # Both results should be independent
        self.assertEqual(result1["value"], message1)
        self.assertEqual(result2["value"], message2)
        self.assertEqual(result1["line"], 1)
        self.assertEqual(result2["line"], 2)

        # parser_state error flag should still be set
        self.assertEqual(self.parser_state["error"], "解析失败")

    def test_build_error_node_returns_dict(self) -> None:
        """Test that _build_error_node returns a dictionary."""
        result = _build_error_node(self.parser_state, "error", 1, 1)

        self.assertIsInstance(result, dict)
        self.assertIn("type", result)
        self.assertIn("value", result)
        self.assertIn("line", result)
        self.assertIn("column", result)

    def test_build_error_node_no_children_field(self) -> None:
        """Test that ERROR node does not have children field."""
        result = _build_error_node(self.parser_state, "error", 1, 1)

        # ERROR nodes should not have children
        self.assertNotIn("children", result)


if __name__ == "__main__":
    unittest.main()

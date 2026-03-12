# -*- coding: utf-8 -*-
"""Unit tests for _handle_if function."""

import unittest
from unittest.mock import patch
from typing import Any, Dict

# Relative import for the function under test
from ._handle_if_src import _handle_if

# Type aliases (matching source file)
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleIf(unittest.TestCase):
    """Test cases for _handle_if function."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_traverse_node_patcher = patch(
            '._handle_if_src._traverse_node'
        )
        self.mock_traverse_node = self.mock_traverse_node_patcher.start()
        self.addCleanup(self.mock_traverse_node_patcher.stop)

    def test_handle_if_normal_flow_with_children(self):
        """Test normal if statement processing with children nodes."""
        node: AST = {
            "type": "if",
            "children": [
                {"type": "condition", "value": "x > 0"},
                {"type": "block", "children": []},
            ],
            "line": 10,
            "column": 5,
        }
        symbol_table: SymbolTable = {
            "current_scope": 0,
            "scope_stack": [],
            "variables": {},
            "functions": {},
            "errors": [],
        }

        _handle_if(node, symbol_table)

        # Verify scope was entered
        self.assertEqual(symbol_table["current_scope"], 1)
        # Verify old scope was pushed to stack
        self.assertEqual(symbol_table["scope_stack"], [0])
        # Verify _traverse_node was called for each child
        self.assertEqual(self.mock_traverse_node.call_count, 2)
        # Verify scope was exited (restored)
        self.assertEqual(symbol_table["current_scope"], 0)
        # Verify scope_stack was popped
        self.assertEqual(symbol_table["scope_stack"], [])

    def test_handle_if_empty_children(self):
        """Test if statement with no children."""
        node: AST = {
            "type": "if",
            "children": [],
            "line": 5,
            "column": 1,
        }
        symbol_table: SymbolTable = {
            "current_scope": 2,
            "scope_stack": [0, 1],
        }

        _handle_if(node, symbol_table)

        # Verify scope was entered
        self.assertEqual(symbol_table["current_scope"], 3)
        # Verify old scope was pushed
        self.assertEqual(symbol_table["scope_stack"], [0, 1, 2])
        # No children, so _traverse_node should not be called
        self.mock_traverse_node.assert_not_called()
        # Verify scope was exited
        self.assertEqual(symbol_table["current_scope"], 2)
        self.assertEqual(symbol_table["scope_stack"], [0, 1])

    def test_handle_if_missing_symbol_table_keys(self):
        """Test if statement with minimal symbol_table (missing keys)."""
        node: AST = {
            "type": "if",
            "children": [{"type": "condition"}],
        }
        symbol_table: SymbolTable = {}

        _handle_if(node, symbol_table)

        # Verify defaults were used
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])
        # _traverse_node should have been called once
        self.assertEqual(self.mock_traverse_node.call_count, 1)

    def test_handle_if_exception_during_traversal(self):
        """Test error handling when _traverse_node raises exception."""
        node: AST = {
            "type": "if",
            "children": [{"type": "condition"}, {"type": "block"}],
            "line": 15,
            "column": 3,
        }
        symbol_table: SymbolTable = {
            "current_scope": 1,
            "scope_stack": [0],
        }

        # Make _traverse_node raise an exception on second call
        self.mock_traverse_node.side_effect = ValueError("Test error")

        _handle_if(node, symbol_table)

        # Verify error was recorded
        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["type"], "if_handling_error")
        self.assertEqual(error["message"], "Test error")
        self.assertEqual(error["line"], 15)
        self.assertEqual(error["column"], 3)
        # Verify scope was still exited despite exception
        self.assertEqual(symbol_table["current_scope"], 1)
        self.assertEqual(symbol_table["scope_stack"], [0])

    def test_handle_if_nested_scope_levels(self):
        """Test if statement at deeper nesting level."""
        node: AST = {
            "type": "if",
            "children": [{"type": "block"}],
        }
        symbol_table: SymbolTable = {
            "current_scope": 5,
            "scope_stack": [0, 1, 2, 3, 4],
        }

        _handle_if(node, symbol_table)

        # Verify scope increment
        self.assertEqual(symbol_table["current_scope"], 6)
        # Verify stack push
        self.assertEqual(symbol_table["scope_stack"], [0, 1, 2, 3, 4, 5])
        # Verify scope restoration
        self.assertEqual(symbol_table["current_scope"], 5)
        self.assertEqual(symbol_table["scope_stack"], [0, 1, 2, 3, 4])

    def test_handle_if_multiple_children_processing_order(self):
        """Test that children are processed in order."""
        node: AST = {
            "type": "if",
            "children": [
                {"type": "condition", "id": "cond"},
                {"type": "then_block", "id": "then"},
                {"type": "else_block", "id": "else"},
            ],
        }
        symbol_table: SymbolTable = {"current_scope": 0}

        _handle_if(node, symbol_table)

        # Verify all children were processed in order
        self.assertEqual(self.mock_traverse_node.call_count, 3)
        calls = self.mock_traverse_node.call_args_list
        self.assertEqual(calls[0][0][0]["id"], "cond")
        self.assertEqual(calls[1][0][0]["id"], "then")
        self.assertEqual(calls[2][0][0]["id"], "else")

    def test_handle_if_no_line_column_info(self):
        """Test error recording when node lacks line/column info."""
        node: AST = {
            "type": "if",
            "children": [{"type": "block"}],
        }
        symbol_table: SymbolTable = {"current_scope": 0}

        self.mock_traverse_node.side_effect = RuntimeError("No location info")

        _handle_if(node, symbol_table)

        # Verify error was recorded with None for line/column
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertIsNone(error["line"])
        self.assertIsNone(error["column"])

    def test_handle_if_scope_stack_initially_empty(self):
        """Test if statement when scope_stack doesn't exist initially."""
        node: AST = {
            "type": "if",
            "children": [],
        }
        symbol_table: SymbolTable = {
            "current_scope": 0,
        }

        _handle_if(node, symbol_table)

        # Verify scope_stack was created and used
        self.assertIn("scope_stack", symbol_table)
        self.assertEqual(symbol_table["scope_stack"], [])
        self.assertEqual(symbol_table["current_scope"], 0)

    def test_handle_if_preserves_other_symbol_table_fields(self):
        """Test that other symbol_table fields are not modified."""
        node: AST = {
            "type": "if",
            "children": [],
        }
        symbol_table: SymbolTable = {
            "current_scope": 1,
            "scope_stack": [0],
            "variables": {"x": {"type": "int", "scope": 0}},
            "functions": {"main": {"params": []}},
            "current_function": "main",
            "errors": [],
        }

        _handle_if(node, symbol_table)

        # Verify other fields are preserved
        self.assertEqual(symbol_table["variables"]["x"]["type"], "int")
        self.assertEqual(symbol_table["functions"]["main"]["params"], [])
        self.assertEqual(symbol_table["current_function"], "main")


if __name__ == "__main__":
    unittest.main()

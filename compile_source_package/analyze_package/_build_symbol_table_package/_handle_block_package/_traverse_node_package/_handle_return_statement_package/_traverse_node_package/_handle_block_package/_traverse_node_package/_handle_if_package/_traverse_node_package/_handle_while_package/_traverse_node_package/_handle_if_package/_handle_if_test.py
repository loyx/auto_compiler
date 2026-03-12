# -*- coding: utf-8 -*-
"""
Unit tests for _handle_if function.
Tests the if statement handler that traverses condition, then_block, and else_block.
"""

import unittest
from unittest.mock import patch, MagicMock
from typing import Any, Dict

# Relative import from the same package
from ._handle_if_src import _handle_if

# Type aliases matching the source
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleIf(unittest.TestCase):
    """Test cases for _handle_if function."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
            "errors": []
        }

    @patch("_handle_if_package._traverse_node_src._traverse_node")
    def test_handle_if_with_all_components(self, mock_traverse: MagicMock) -> None:
        """Test if node with condition, then_block, and else_block."""
        condition_node: AST = {"type": "binary_op", "value": ">", "line": 1, "column": 5}
        then_block_node: AST = {"type": "block", "children": [], "line": 1, "column": 10}
        else_block_node: AST = {"type": "block", "children": [], "line": 2, "column": 5}
        
        node: AST = {
            "type": "if",
            "condition": condition_node,
            "then_block": then_block_node,
            "else_block": else_block_node,
            "line": 1,
            "column": 1
        }
        
        _handle_if(node, self.symbol_table)
        
        # Verify _traverse_node was called for all three components in order
        self.assertEqual(mock_traverse.call_count, 3)
        mock_traverse.assert_any_call(condition_node, self.symbol_table)
        mock_traverse.assert_any_call(then_block_node, self.symbol_table)
        mock_traverse.assert_any_call(else_block_node, self.symbol_table)

    @patch("_handle_if_package._traverse_node_src._traverse_node")
    def test_handle_if_without_else_block(self, mock_traverse: MagicMock) -> None:
        """Test if node without else_block (else_block is None or missing)."""
        condition_node: AST = {"type": "binary_op", "value": "==", "line": 1, "column": 5}
        then_block_node: AST = {"type": "block", "children": [], "line": 1, "column": 10}
        
        # Test with else_block explicitly None
        node_with_none: AST = {
            "type": "if",
            "condition": condition_node,
            "then_block": then_block_node,
            "else_block": None,
            "line": 1,
            "column": 1
        }
        
        _handle_if(node_with_none, self.symbol_table)
        
        # Should only traverse condition and then_block
        self.assertEqual(mock_traverse.call_count, 2)
        mock_traverse.assert_any_call(condition_node, self.symbol_table)
        mock_traverse.assert_any_call(then_block_node, self.symbol_table)
        
        # Reset mock for next test
        mock_traverse.reset_mock()
        
        # Test with else_block missing from dict
        node_without_else: AST = {
            "type": "if",
            "condition": condition_node,
            "then_block": then_block_node,
            "line": 1,
            "column": 1
        }
        
        _handle_if(node_without_else, self.symbol_table)
        
        # Should only traverse condition and then_block
        self.assertEqual(mock_traverse.call_count, 2)

    @patch("_handle_if_package._traverse_node_src._traverse_node")
    def test_handle_if_with_none_condition(self, mock_traverse: MagicMock) -> None:
        """Test if node with None condition."""
        then_block_node: AST = {"type": "block", "children": [], "line": 1, "column": 10}
        
        node: AST = {
            "type": "if",
            "condition": None,
            "then_block": then_block_node,
            "else_block": None,
            "line": 1,
            "column": 1
        }
        
        _handle_if(node, self.symbol_table)
        
        # Should only traverse then_block
        self.assertEqual(mock_traverse.call_count, 1)
        mock_traverse.assert_called_once_with(then_block_node, self.symbol_table)

    @patch("_handle_if_package._traverse_node_src._traverse_node")
    def test_handle_if_with_none_then_block(self, mock_traverse: MagicMock) -> None:
        """Test if node with None then_block."""
        condition_node: AST = {"type": "binary_op", "value": "<", "line": 1, "column": 5}
        else_block_node: AST = {"type": "block", "children": [], "line": 2, "column": 5}
        
        node: AST = {
            "type": "if",
            "condition": condition_node,
            "then_block": None,
            "else_block": else_block_node,
            "line": 1,
            "column": 1
        }
        
        _handle_if(node, self.symbol_table)
        
        # Should traverse condition and else_block, but not then_block
        self.assertEqual(mock_traverse.call_count, 2)
        mock_traverse.assert_any_call(condition_node, self.symbol_table)
        mock_traverse.assert_any_call(else_block_node, self.symbol_table)

    @patch("_handle_if_package._traverse_node_src._traverse_node")
    def test_handle_if_with_all_none_components(self, mock_traverse: MagicMock) -> None:
        """Test if node with all components None."""
        node: AST = {
            "type": "if",
            "condition": None,
            "then_block": None,
            "else_block": None,
            "line": 1,
            "column": 1
        }
        
        _handle_if(node, self.symbol_table)
        
        # Should not call _traverse_node at all
        self.assertEqual(mock_traverse.call_count, 0)

    @patch("_handle_if_package._traverse_node_src._traverse_node")
    def test_handle_if_with_empty_node(self, mock_traverse: MagicMock) -> None:
        """Test if node with missing keys (using .get() returns None)."""
        node: AST = {
            "type": "if",
            "line": 1,
            "column": 1
        }
        
        _handle_if(node, self.symbol_table)
        
        # Should not call _traverse_node at all (all .get() return None)
        self.assertEqual(mock_traverse.call_count, 0)

    @patch("_handle_if_package._traverse_node_src._traverse_node")
    def test_handle_if_traversal_order(self, mock_traverse: MagicMock) -> None:
        """Test that components are traversed in correct order: condition, then_block, else_block."""
        condition_node: AST = {"type": "condition", "line": 1, "column": 5}
        then_block_node: AST = {"type": "then", "line": 1, "column": 10}
        else_block_node: AST = {"type": "else", "line": 2, "column": 5}
        
        node: AST = {
            "type": "if",
            "condition": condition_node,
            "then_block": then_block_node,
            "else_block": else_block_node,
            "line": 1,
            "column": 1
        }
        
        _handle_if(node, self.symbol_table)
        
        # Verify call order
        calls = mock_traverse.call_args_list
        self.assertEqual(len(calls), 3)
        self.assertEqual(calls[0][0][0], condition_node)
        self.assertEqual(calls[1][0][0], then_block_node)
        self.assertEqual(calls[2][0][0], else_block_node)

    @patch("_handle_if_package._traverse_node_src._traverse_node")
    def test_handle_if_symbol_table_passed_unchanged(self, mock_traverse: MagicMock) -> None:
        """Test that the same symbol_table instance is passed to _traverse_node."""
        condition_node: AST = {"type": "binary_op", "line": 1, "column": 5}
        
        node: AST = {
            "type": "if",
            "condition": condition_node,
            "then_block": None,
            "else_block": None,
            "line": 1,
            "column": 1
        }
        
        _handle_if(node, self.symbol_table)
        
        # Verify the exact same symbol_table object was passed
        mock_traverse.assert_called_once()
        _, passed_symbol_table = mock_traverse.call_args[0]
        self.assertIs(passed_symbol_table, self.symbol_table)

    @patch("_handle_if_package._traverse_node_src._traverse_node")
    def test_handle_if_with_nested_if(self, mock_traverse: MagicMock) -> None:
        """Test if node containing nested if in then_block."""
        condition_node: AST = {"type": "binary_op", "value": ">", "line": 1, "column": 5}
        nested_if_node: AST = {"type": "if", "line": 1, "column": 10}
        then_block_node: AST = {"type": "block", "children": [nested_if_node], "line": 1, "column": 10}
        
        node: AST = {
            "type": "if",
            "condition": condition_node,
            "then_block": then_block_node,
            "else_block": None,
            "line": 1,
            "column": 1
        }
        
        _handle_if(node, self.symbol_table)
        
        # Should traverse condition and then_block (nested if handled by recursive call)
        self.assertEqual(mock_traverse.call_count, 2)
        mock_traverse.assert_any_call(condition_node, self.symbol_table)
        mock_traverse.assert_any_call(then_block_node, self.symbol_table)


if __name__ == "__main__":
    unittest.main()

# -*- coding: utf-8 -*-
"""
Unit tests for _verify_children function.
Tests the recursive verification of node['children'] list.
"""

import unittest
from unittest.mock import patch, MagicMock
from typing import Any, Dict, List

# Relative import from the same package
from ._verify_children_src import _verify_children


class TestVerifyChildren(unittest.TestCase):
    """Test cases for _verify_children function."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.symbol_table: Dict[str, Any] = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
        }
        self.context_stack: List[Dict[str, Any]] = []
        self.filename: str = "test_file.py"

    def test_children_empty_list_returns_early(self) -> None:
        """Test that function returns early when children is empty list."""
        node: Dict[str, Any] = {
            "type": "test_node",
            "children": [],
            "line": 1,
            "column": 0,
        }
        
        # Should not raise any exception
        _verify_children(node, self.symbol_table, self.context_stack, self.filename)

    def test_children_key_missing_returns_early(self) -> None:
        """Test that function returns early when 'children' key is missing."""
        node: Dict[str, Any] = {
            "type": "test_node",
            "line": 1,
            "column": 0,
        }
        
        # Should not raise any exception
        _verify_children(node, self.symbol_table, self.context_stack, self.filename)

    @patch('main_package.compile_source_package.analyze_package._verify_ast_package._verify_node_package._verify_children_package._verify_node_package._verify_node_src._verify_node')
    def test_single_child_calls_verify_node(self, mock_verify_node: MagicMock) -> None:
        """Test that _verify_node is called for a single child."""
        child_node: Dict[str, Any] = {
            "type": "child_node",
            "line": 2,
            "column": 4,
        }
        node: Dict[str, Any] = {
            "type": "parent_node",
            "children": [child_node],
            "line": 1,
            "column": 0,
        }
        
        _verify_children(node, self.symbol_table, self.context_stack, self.filename)
        
        mock_verify_node.assert_called_once_with(
            child_node,
            self.symbol_table,
            self.context_stack,
            self.filename
        )

    @patch('main_package.compile_source_package.analyze_package._verify_ast_package._verify_node_package._verify_children_package._verify_node_package._verify_node_src._verify_node')
    def test_multiple_children_calls_verify_node_for_each(self, mock_verify_node: MagicMock) -> None:
        """Test that _verify_node is called for each child in order."""
        child1: Dict[str, Any] = {"type": "child1", "line": 2, "column": 4}
        child2: Dict[str, Any] = {"type": "child2", "line": 3, "column": 4}
        child3: Dict[str, Any] = {"type": "child3", "line": 4, "column": 4}
        
        node: Dict[str, Any] = {
            "type": "parent_node",
            "children": [child1, child2, child3],
            "line": 1,
            "column": 0,
        }
        
        _verify_children(node, self.symbol_table, self.context_stack, self.filename)
        
        self.assertEqual(mock_verify_node.call_count, 3)
        
        # Verify calls in order
        expected_calls = [
            unittest.mock.call(child1, self.symbol_table, self.context_stack, self.filename),
            unittest.mock.call(child2, self.symbol_table, self.context_stack, self.filename),
            unittest.mock.call(child3, self.symbol_table, self.context_stack, self.filename),
        ]
        mock_verify_node.assert_has_calls(expected_calls)

    @patch('main_package.compile_source_package.analyze_package._verify_ast_package._verify_node_package._verify_children_package._verify_node_package._verify_node_src._verify_node')
    def test_verify_node_exception_propagates(self, mock_verify_node: MagicMock) -> None:
        """Test that exceptions from _verify_node propagate correctly."""
        child_node: Dict[str, Any] = {
            "type": "child_node",
            "line": 2,
            "column": 4,
        }
        node: Dict[str, Any] = {
            "type": "parent_node",
            "children": [child_node],
            "line": 1,
            "column": 0,
        }
        
        test_exception = ValueError("Test verification error")
        mock_verify_node.side_effect = test_exception
        
        with self.assertRaises(ValueError) as context:
            _verify_children(node, self.symbol_table, self.context_stack, self.filename)
        
        self.assertEqual(str(context.exception), "Test verification error")
        mock_verify_node.assert_called_once()

    @patch('main_package.compile_source_package.analyze_package._verify_ast_package._verify_node_package._verify_children_package._verify_node_package._verify_node_src._verify_node')
    def test_children_with_none_values(self, mock_verify_node: MagicMock) -> None:
        """Test handling of None values in children list."""
        node: Dict[str, Any] = {
            "type": "parent_node",
            "children": [None],
            "line": 1,
            "column": 0,
        }
        
        _verify_children(node, self.symbol_table, self.context_stack, self.filename)
        
        mock_verify_node.assert_called_once_with(
            None,
            self.symbol_table,
            self.context_stack,
            self.filename
        )

    @patch('main_package.compile_source_package.analyze_package._verify_ast_package._verify_node_package._verify_children_package._verify_node_package._verify_node_src._verify_node')
    def test_complex_context_stack_passed_correctly(self, mock_verify_node: MagicMock) -> None:
        """Test that complex context stack is passed correctly to _verify_node."""
        child_node: Dict[str, Any] = {
            "type": "child_node",
            "line": 2,
            "column": 4,
        }
        node: Dict[str, Any] = {
            "type": "parent_node",
            "children": [child_node],
            "line": 1,
            "column": 0,
        }
        
        complex_context_stack: List[Dict[str, Any]] = [
            {"type": "function", "name": "main", "return_type": "int"},
            {"type": "loop", "stmt_type": "for"},
        ]
        
        complex_symbol_table: Dict[str, Any] = {
            "variables": {"x": {"type": "int", "scope": 0}},
            "functions": {"main": {"return_type": "int", "params": []}},
            "current_scope": 1,
        }
        
        _verify_children(node, complex_symbol_table, complex_context_stack, self.filename)
        
        mock_verify_node.assert_called_once_with(
            child_node,
            complex_symbol_table,
            complex_context_stack,
            self.filename
        )


if __name__ == "__main__":
    unittest.main()

# -*- coding: utf-8 -*-
"""
Unit tests for _handle_expression function.
Tests the expression node handler that traverses children for semantic analysis.
"""

import unittest
from unittest.mock import patch, MagicMock, call
from typing import Any, Dict
import sys

# Type aliases matching the source
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


# Mock _traverse_node before importing to avoid circular import issues
_mock_traverse_node = MagicMock()

# Create a mock module for _traverse_node_src
_mock_module = MagicMock()
_mock_module._traverse_node = _mock_traverse_node

# Register the mock module in sys.modules to intercept imports
sys.modules['main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_program_package._traverse_node_package._handle_block_package._traverse_node_package._handle_expression_package._traverse_node_package._traverse_node_src'] = _mock_module

# Also register shorter paths that might be used
sys.modules['_handle_expression_package._traverse_node_package._traverse_node_src'] = _mock_module

# Now import the function under test
from ._handle_expression_src import _handle_expression


class TestHandleExpression(unittest.TestCase):
    """Test cases for _handle_expression function."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
            "errors": []
        }
        # Reset mock for each test
        _mock_traverse_node.reset_mock()

    def test_handle_expression_with_single_child(self) -> None:
        """Test handling expression node with a single child."""
        child_node: AST = {
            "type": "identifier",
            "value": "x",
            "children": [],
            "line": 1,
            "column": 5
        }
        node: AST = {
            "type": "expression",
            "children": [child_node],
            "line": 1,
            "column": 1
        }

        _handle_expression(node, self.symbol_table)

        _mock_traverse_node.assert_called_once_with(child_node, self.symbol_table)

    def test_handle_expression_with_multiple_children(self) -> None:
        """Test handling expression node with multiple children."""
        child1: AST = {
            "type": "identifier",
            "value": "x",
            "children": [],
            "line": 1,
            "column": 5
        }
        child2: AST = {
            "type": "operator",
            "value": "+",
            "children": [],
            "line": 1,
            "column": 7
        }
        child3: AST = {
            "type": "literal",
            "value": 10,
            "data_type": "int",
            "children": [],
            "line": 1,
            "column": 9
        }
        node: AST = {
            "type": "expression",
            "children": [child1, child2, child3],
            "line": 1,
            "column": 1
        }

        _handle_expression(node, self.symbol_table)

        self.assertEqual(_mock_traverse_node.call_count, 3)
        _mock_traverse_node.assert_has_calls([
            call(child1, self.symbol_table),
            call(child2, self.symbol_table),
            call(child3, self.symbol_table)
        ])

    def test_handle_expression_with_nested_expression(self) -> None:
        """Test handling expression node with nested expression child."""
        nested_child: AST = {
            "type": "expression",
            "children": [
                {"type": "identifier", "value": "y", "children": [], "line": 1, "column": 6}
            ],
            "line": 1,
            "column": 5
        }
        node: AST = {
            "type": "expression",
            "children": [nested_child],
            "line": 1,
            "column": 1
        }

        _handle_expression(node, self.symbol_table)

        _mock_traverse_node.assert_called_once_with(nested_child, self.symbol_table)

    def test_handle_expression_with_empty_children(self) -> None:
        """Test handling expression node with empty children list."""
        node: AST = {
            "type": "expression",
            "children": [],
            "line": 1,
            "column": 1
        }

        _handle_expression(node, self.symbol_table)

        _mock_traverse_node.assert_not_called()

    def test_handle_expression_without_children_field(self) -> None:
        """Test handling expression node without children field (uses default)."""
        node: AST = {
            "type": "expression",
            "line": 1,
            "column": 1
        }

        _handle_expression(node, self.symbol_table)

        _mock_traverse_node.assert_not_called()

    def test_handle_expression_preserves_symbol_table(self) -> None:
        """Test that symbol_table is passed correctly to _traverse_node."""
        child_node: AST = {
            "type": "identifier",
            "value": "var",
            "children": [],
            "line": 1,
            "column": 5
        }
        node: AST = {
            "type": "expression",
            "children": [child_node],
            "line": 1,
            "column": 1
        }

        _handle_expression(node, self.symbol_table)

        # Verify the same symbol_table instance is passed
        call_args = _mock_traverse_node.call_args
        self.assertEqual(call_args[0][0], child_node)
        self.assertIs(call_args[0][1], self.symbol_table)

    def test_handle_expression_with_complex_ast(self) -> None:
        """Test handling complex expression with various node types."""
        children = [
            {"type": "identifier", "value": "a", "children": [], "line": 2, "column": 1},
            {"type": "operator", "value": "*", "children": [], "line": 2, "column": 3},
            {"type": "literal", "value": 5, "data_type": "int", "children": [], "line": 2, "column": 5},
            {"type": "operator", "value": "+", "children": [], "line": 2, "column": 7},
            {"type": "identifier", "value": "b", "children": [], "line": 2, "column": 9},
        ]
        node: AST = {
            "type": "expression",
            "children": children,
            "line": 2,
            "column": 1
        }

        _handle_expression(node, self.symbol_table)

        self.assertEqual(_mock_traverse_node.call_count, 5)
        for child in children:
            _mock_traverse_node.assert_any_call(child, self.symbol_table)

    def test_handle_expression_calls_traverse_in_order(self) -> None:
        """Test that children are traversed in order."""
        children = [
            {"type": "identifier", "value": "first", "children": [], "line": 1, "column": 1},
            {"type": "identifier", "value": "second", "children": [], "line": 1, "column": 2},
            {"type": "identifier", "value": "third", "children": [], "line": 1, "column": 3},
        ]
        node: AST = {
            "type": "expression",
            "children": children,
            "line": 1,
            "column": 1
        }

        _handle_expression(node, self.symbol_table)

        expected_calls = [call(child, self.symbol_table) for child in children]
        _mock_traverse_node.assert_has_calls(expected_calls, any_order=False)

    def test_handle_expression_with_none_children(self) -> None:
        """Test handling expression node with None as children value."""
        node: AST = {
            "type": "expression",
            "children": None,
            "line": 1,
            "column": 1
        }

        # Should handle None gracefully (get returns None, iteration fails)
        # The function uses node.get("children", []) which returns None if children is explicitly None
        # This will cause TypeError when iterating, which is expected behavior
        with self.assertRaises(TypeError):
            _handle_expression(node, self.symbol_table)

    def test_handle_expression_does_not_modify_node(self) -> None:
        """Test that the function does not modify the input node."""
        import copy
        child_node: AST = {
            "type": "identifier",
            "value": "x",
            "children": [],
            "line": 1,
            "column": 5
        }
        node: AST = {
            "type": "expression",
            "children": [child_node],
            "line": 1,
            "column": 1
        }
        node_copy = copy.deepcopy(node)

        _handle_expression(node, self.symbol_table)

        self.assertEqual(node, node_copy)


if __name__ == "__main__":
    unittest.main()
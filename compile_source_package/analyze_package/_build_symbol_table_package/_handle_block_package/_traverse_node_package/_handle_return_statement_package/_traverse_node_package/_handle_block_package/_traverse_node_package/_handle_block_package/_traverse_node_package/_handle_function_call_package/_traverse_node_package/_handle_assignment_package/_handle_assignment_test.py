# -*- coding: utf-8 -*-
"""
Unit tests for _handle_assignment function.
Tests assignment node handling: variable declaration validation and expression traversal.
"""

import unittest
from unittest.mock import patch
from typing import Any, Dict

# Relative import for the function under test
from ._handle_assignment_src import _handle_assignment


AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleAssignment(unittest.TestCase):
    """Test cases for _handle_assignment function."""

    def test_happy_path_variable_declared_with_expression(self):
        """Test assignment when variable is declared and has right-side expression."""
        node: AST = {
            "type": "assignment",
            "children": [
                {"type": "identifier", "value": "x", "line": 5, "column": 10},
                {"type": "literal", "value": 42, "line": 5, "column": 14}
            ],
            "line": 5,
            "column": 10
        }
        symbol_table: SymbolTable = {
            "variables": {
                "x": {"data_type": "int", "is_declared": True, "line": 1, "column": 1, "scope_level": 0}
            },
            "errors": []
        }

        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_assignment(node, symbol_table)

        # Should traverse the right-side expression
        mock_traverse.assert_called_once_with(
            {"type": "literal", "value": 42, "line": 5, "column": 14},
            symbol_table
        )
        # Should not record any errors
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_happy_path_variable_declared_no_expression(self):
        """Test assignment when variable is declared but no right-side expression."""
        node: AST = {
            "type": "assignment",
            "children": [
                {"type": "identifier", "value": "x", "line": 5, "column": 10}
            ],
            "line": 5,
            "column": 10
        }
        symbol_table: SymbolTable = {
            "variables": {
                "x": {"data_type": "int", "is_declared": True, "line": 1, "column": 1, "scope_level": 0}
            },
            "errors": []
        }

        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_assignment(node, symbol_table)

        # Should not traverse (no expression)
        mock_traverse.assert_not_called()
        # Should not record any errors
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_undeclared_variable_records_error(self):
        """Test assignment when variable is not declared - should record error."""
        node: AST = {
            "type": "assignment",
            "children": [
                {"type": "identifier", "value": "y", "line": 10, "column": 5}
            ],
            "line": 10,
            "column": 5
        }
        symbol_table: SymbolTable = {
            "variables": {
                "x": {"data_type": "int", "is_declared": True, "line": 1, "column": 1, "scope_level": 0}
            },
            "errors": []
        }

        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_assignment(node, symbol_table)

        # Should not traverse expression
        mock_traverse.assert_not_called()
        # Should record exactly one error
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["error_type"], "undeclared_variable")
        self.assertEqual(error["message"], "Variable 'y' is not declared")
        self.assertEqual(error["line"], 10)
        self.assertEqual(error["column"], 5)
        self.assertEqual(error["var_name"], "y")

    def test_variable_not_in_variables_dict_records_error(self):
        """Test assignment when variable is not in variables dict at all."""
        node: AST = {
            "type": "assignment",
            "children": [
                {"type": "identifier", "value": "z", "line": 15, "column": 8}
            ],
            "line": 15,
            "column": 8
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "errors": []
        }

        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_assignment(node, symbol_table)

        # Should not traverse expression
        mock_traverse.assert_not_called()
        # Should record error
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertEqual(symbol_table["errors"][0]["error_type"], "undeclared_variable")
        self.assertEqual(symbol_table["errors"][0]["var_name"], "z")

    def test_variable_is_declared_false_records_error(self):
        """Test assignment when variable exists but is_declared is False."""
        node: AST = {
            "type": "assignment",
            "children": [
                {"type": "identifier", "value": "w", "line": 20, "column": 3}
            ],
            "line": 20,
            "column": 3
        }
        symbol_table: SymbolTable = {
            "variables": {
                "w": {"data_type": "char", "is_declared": False, "line": 18, "column": 1, "scope_level": 0}
            },
            "errors": []
        }

        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_assignment(node, symbol_table)

        # Should not traverse expression
        mock_traverse.assert_not_called()
        # Should record error
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertEqual(symbol_table["errors"][0]["error_type"], "undeclared_variable")
        self.assertEqual(symbol_table["errors"][0]["var_name"], "w")

    def test_no_children_returns_early(self):
        """Test assignment node with no children - should return early without error."""
        node: AST = {
            "type": "assignment",
            "children": [],
            "line": 25,
            "column": 1
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "errors": []
        }

        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_assignment(node, symbol_table)

        # Should not traverse
        mock_traverse.assert_not_called()
        # Should not record any errors
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_missing_children_key_returns_early(self):
        """Test assignment node without 'children' key - should return early."""
        node: AST = {
            "type": "assignment",
            "line": 30,
            "column": 1
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "errors": []
        }

        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_assignment(node, symbol_table)

        # Should not traverse
        mock_traverse.assert_not_called()
        # Should not record any errors
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_creates_errors_list_if_not_exists(self):
        """Test that function creates errors list if it doesn't exist in symbol_table."""
        node: AST = {
            "type": "assignment",
            "children": [
                {"type": "identifier", "value": "missing_var", "line": 35, "column": 2}
            ],
            "line": 35,
            "column": 2
        }
        symbol_table: SymbolTable = {
            "variables": {}
            # No 'errors' key
        }

        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_assignment(node, symbol_table)

        # Should create errors list
        self.assertIn("errors", symbol_table)
        self.assertIsInstance(symbol_table["errors"], list)
        # Should record error
        self.assertEqual(len(symbol_table["errors"]), 1)

    def test_identifier_without_value_key(self):
        """Test assignment when identifier node has no 'value' key."""
        node: AST = {
            "type": "assignment",
            "children": [
                {"type": "identifier", "line": 40, "column": 5}
                # No 'value' key
            ],
            "line": 40,
            "column": 5
        }
        symbol_table: SymbolTable = {
            "variables": {
                "x": {"data_type": "int", "is_declared": True, "line": 1, "column": 1, "scope_level": 0}
            },
            "errors": []
        }

        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_assignment(node, symbol_table)

        # var_name will be None, which won't be in variables
        # Should record error for None variable
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertEqual(symbol_table["errors"][0]["var_name"], None)

    def test_multiple_assignments_accumulate_errors(self):
        """Test that multiple assignment errors accumulate in errors list."""
        symbol_table: SymbolTable = {
            "variables": {
                "x": {"data_type": "int", "is_declared": True, "line": 1, "column": 1, "scope_level": 0}
            },
            "errors": []
        }

        # First assignment - undeclared variable
        node1: AST = {
            "type": "assignment",
            "children": [
                {"type": "identifier", "value": "a", "line": 45, "column": 1}
            ],
            "line": 45,
            "column": 1
        }

        # Second assignment - another undeclared variable
        node2: AST = {
            "type": "assignment",
            "children": [
                {"type": "identifier", "value": "b", "line": 46, "column": 1}
            ],
            "line": 46,
            "column": 1
        }

        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_assignment(node1, symbol_table)
            _handle_assignment(node2, symbol_table)

        # Should have 2 errors
        self.assertEqual(len(symbol_table["errors"]), 2)
        self.assertEqual(symbol_table["errors"][0]["var_name"], "a")
        self.assertEqual(symbol_table["errors"][1]["var_name"], "b")
        # Should not traverse any expressions
        self.assertEqual(mock_traverse.call_count, 0)


if __name__ == "__main__":
    unittest.main()

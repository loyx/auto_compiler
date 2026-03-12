#!/usr/bin/env python3
"""Unit tests for _handle_assignment function."""

import unittest
from unittest.mock import patch

# Relative import from the same package
from ._handle_assignment_src import _handle_assignment, AST, SymbolTable


class TestHandleAssignment(unittest.TestCase):
    """Test cases for _handle_assignment function."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.base_node: AST = {
            "type": "assignment",
            "value": "x",
            "line": 10,
            "column": 5,
            "children": []
        }
        self.base_symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 1,
            "scope_stack": [],
            "errors": []
        }

    def test_variable_declared_success(self) -> None:
        """Happy path: variable is declared, should traverse children[0]."""
        node: AST = {
            "type": "assignment",
            "value": "x",
            "line": 10,
            "column": 5,
            "children": [{"type": "literal", "value": 42}]
        }
        symbol_table: SymbolTable = {
            "variables": {
                "x": {"data_type": "int", "is_declared": True, "line": 5, "column": 1, "scope_level": 1}
            },
            "functions": {},
            "current_scope": 1,
            "scope_stack": [],
            "errors": []
        }

        with patch("._handle_assignment_src._traverse_node") as mock_traverse:
            _handle_assignment(node, symbol_table)

        # Should call _traverse_node with children[0]
        mock_traverse.assert_called_once_with({"type": "literal", "value": 42}, symbol_table)
        # Should not record any errors
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_variable_not_declared_records_error(self) -> None:
        """Variable not declared: should record error and return early."""
        node: AST = {
            "type": "assignment",
            "value": "undefined_var",
            "line": 10,
            "column": 5,
            "children": [{"type": "literal", "value": 42}]
        }
        symbol_table: SymbolTable = {
            "variables": {
                "x": {"data_type": "int", "is_declared": True, "line": 5, "column": 1, "scope_level": 1}
            },
            "functions": {},
            "current_scope": 1,
            "scope_stack": [],
            "errors": []
        }

        with patch("._handle_assignment_src._traverse_node") as mock_traverse:
            _handle_assignment(node, symbol_table)

        # Should NOT call _traverse_node (early return)
        mock_traverse.assert_not_called()
        # Should record exactly one error
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["type"], "error")
        self.assertEqual(error["message"], "Undefined variable: undefined_var")
        self.assertEqual(error["line"], 10)
        self.assertEqual(error["column"], 5)

    def test_missing_errors_list_in_symbol_table(self) -> None:
        """Edge case: symbol_table missing 'errors' key."""
        node: AST = {
            "type": "assignment",
            "value": "undefined_var",
            "line": 10,
            "column": 5,
            "children": []
        }
        symbol_table: SymbolTable = {
            "variables": {}
        }

        with patch("._handle_assignment_src._traverse_node") as mock_traverse:
            _handle_assignment(node, symbol_table)

        # Should create errors list
        self.assertIn("errors", symbol_table)
        self.assertIsInstance(symbol_table["errors"], list)
        self.assertEqual(len(symbol_table["errors"]), 1)
        mock_traverse.assert_not_called()

    def test_missing_variables_dict_in_symbol_table(self) -> None:
        """Edge case: symbol_table missing 'variables' key."""
        node: AST = {
            "type": "assignment",
            "value": "x",
            "line": 10,
            "column": 5,
            "children": []
        }
        symbol_table: SymbolTable = {
            "errors": []
        }

        with patch("._handle_assignment_src._traverse_node") as mock_traverse:
            _handle_assignment(node, symbol_table)

        # Should create variables dict
        self.assertIn("variables", symbol_table)
        self.assertIsInstance(symbol_table["variables"], dict)
        # Variable not found, should record error
        self.assertEqual(len(symbol_table["errors"]), 1)
        mock_traverse.assert_not_called()

    def test_missing_node_value_field(self) -> None:
        """Edge case: node missing 'value' field."""
        node: AST = {
            "type": "assignment",
            "line": 10,
            "column": 5,
            "children": []
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "errors": []
        }

        with patch("._handle_assignment_src._traverse_node") as mock_traverse:
            _handle_assignment(node, symbol_table)

        # Empty string value won't be in variables, should record error
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["message"], "Undefined variable: ")
        mock_traverse.assert_not_called()

    def test_missing_node_line_column_fields(self) -> None:
        """Edge case: node missing 'line' and 'column' fields."""
        node: AST = {
            "type": "assignment",
            "value": "undefined_var",
            "children": []
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "errors": []
        }

        with patch("._handle_assignment_src._traverse_node") as mock_traverse:
            _handle_assignment(node, symbol_table)

        # Should use default values -1 for line/column
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["line"], -1)
        self.assertEqual(error["column"], -1)
        mock_traverse.assert_not_called()

    def test_no_children_does_not_traverse(self) -> None:
        """Edge case: variable declared but no children to traverse."""
        node: AST = {
            "type": "assignment",
            "value": "x",
            "line": 10,
            "column": 5,
            "children": []
        }
        symbol_table: SymbolTable = {
            "variables": {
                "x": {"data_type": "int", "is_declared": True, "line": 5, "column": 1, "scope_level": 1}
            },
            "functions": {},
            "current_scope": 1,
            "scope_stack": [],
            "errors": []
        }

        with patch("._handle_assignment_src._traverse_node") as mock_traverse:
            _handle_assignment(node, symbol_table)

        # Should NOT call _traverse_node (no children)
        mock_traverse.assert_not_called()
        # Should not record any errors
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_multiple_errors_accumulation(self) -> None:
        """Multiple undefined variables should accumulate errors."""
        symbol_table: SymbolTable = {
            "variables": {
                "x": {"data_type": "int", "is_declared": True, "line": 5, "column": 1, "scope_level": 1}
            },
            "functions": {},
            "current_scope": 1,
            "scope_stack": [],
            "errors": []
        }

        # First undefined variable
        node1: AST = {
            "type": "assignment",
            "value": "undefined1",
            "line": 10,
            "column": 5,
            "children": []
        }
        _handle_assignment(node1, symbol_table)

        # Second undefined variable
        node2: AST = {
            "type": "assignment",
            "value": "undefined2",
            "line": 20,
            "column": 15,
            "children": []
        }
        _handle_assignment(node2, symbol_table)

        # Should have 2 errors
        self.assertEqual(len(symbol_table["errors"]), 2)
        self.assertEqual(symbol_table["errors"][0]["message"], "Undefined variable: undefined1")
        self.assertEqual(symbol_table["errors"][1]["message"], "Undefined variable: undefined2")

    def test_declared_variable_with_complex_children(self) -> None:
        """Variable declared with complex expression children."""
        node: AST = {
            "type": "assignment",
            "value": "x",
            "line": 10,
            "column": 5,
            "children": [
                {
                    "type": "binary_op",
                    "operator": "+",
                    "children": [
                        {"type": "literal", "value": 1},
                        {"type": "literal", "value": 2}
                    ]
                }
            ]
        }
        symbol_table: SymbolTable = {
            "variables": {
                "x": {"data_type": "int", "is_declared": True, "line": 5, "column": 1, "scope_level": 1}
            },
            "functions": {},
            "current_scope": 1,
            "scope_stack": [],
            "errors": []
        }

        with patch("._handle_assignment_src._traverse_node") as mock_traverse:
            _handle_assignment(node, symbol_table)

        # Should call _traverse_node with the first child (binary_op node)
        mock_traverse.assert_called_once()
        called_args = mock_traverse.call_args
        self.assertEqual(called_args[0][0]["type"], "binary_op")
        self.assertEqual(called_args[0][0]["operator"], "+")
        self.assertEqual(called_args[0][1], symbol_table)


if __name__ == "__main__":
    unittest.main()

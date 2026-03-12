"""
Unit tests for _handle_assignment function.
"""
import unittest
from unittest.mock import patch

from ._handle_assignment_src import _handle_assignment


class TestHandleAssignment(unittest.TestCase):
    """Test cases for _handle_assignment function."""

    def test_variable_declared_traverses_expression(self):
        """Happy path: variable is declared, should traverse expression."""
        node = {
            "type": "assignment",
            "children": ["x", {"type": "literal", "value": 42}],
            "line": 10,
            "column": 5
        }
        symbol_table = {
            "variables": {
                "x": {
                    "data_type": "int",
                    "is_declared": True,
                    "line": 5,
                    "column": 1,
                    "scope_level": 0
                }
            },
            "errors": []
        }

        with patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_while_package._traverse_node_package._handle_assignment_package._handle_assignment_src._traverse_node") as mock_traverse:
            _handle_assignment(node, symbol_table)

            mock_traverse.assert_called_once_with({"type": "literal", "value": 42}, symbol_table)
            self.assertEqual(len(symbol_table["errors"]), 0)

    def test_variable_not_in_symbol_table_records_error(self):
        """Error path: variable not in symbol_table, should record error."""
        node = {
            "type": "assignment",
            "children": ["y", {"type": "literal", "value": 10}],
            "line": 15,
            "column": 8
        }
        symbol_table = {
            "variables": {
                "x": {
                    "data_type": "int",
                    "is_declared": True,
                    "line": 5,
                    "column": 1,
                    "scope_level": 0
                }
            },
            "errors": []
        }

        _handle_assignment(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["type"], "undeclared_variable")
        self.assertEqual(error["var_name"], "y")
        self.assertEqual(error["message"], "Variable 'y' is not declared before assignment")
        self.assertEqual(error["line"], 15)
        self.assertEqual(error["column"], 8)

    def test_variable_exists_but_not_declared_records_error(self):
        """Error path: variable exists but is_declared is False."""
        node = {
            "type": "assignment",
            "children": ["z", {"type": "literal", "value": 20}],
            "line": 20,
            "column": 3
        }
        symbol_table = {
            "variables": {
                "z": {
                    "data_type": "int",
                    "is_declared": False,
                    "line": 18,
                    "column": 1,
                    "scope_level": 0
                }
            },
            "errors": []
        }

        _handle_assignment(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["type"], "undeclared_variable")
        self.assertEqual(error["var_name"], "z")
        self.assertEqual(error["message"], "Variable 'z' is not declared before assignment")
        self.assertEqual(error["line"], 20)
        self.assertEqual(error["column"], 3)

    def test_missing_line_column_defaults_to_zero(self):
        """Edge case: node missing line/column should default to 0."""
        node = {
            "type": "assignment",
            "children": ["a", {"type": "literal", "value": 5}]
        }
        symbol_table = {
            "variables": {},
            "errors": []
        }

        _handle_assignment(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["line"], 0)
        self.assertEqual(error["column"], 0)

    def test_empty_variables_dict_records_error(self):
        """Edge case: empty variables dict should record error."""
        node = {
            "type": "assignment",
            "children": ["b", {"type": "literal", "value": 100}],
            "line": 25,
            "column": 10
        }
        symbol_table = {
            "variables": {},
            "errors": []
        }

        _handle_assignment(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["var_name"], "b")

    def test_multiple_errors_accumulated(self):
        """Verify errors accumulate in symbol_table."""
        node1 = {
            "type": "assignment",
            "children": ["undeclared1", {"type": "literal", "value": 1}],
            "line": 1,
            "column": 1
        }
        node2 = {
            "type": "assignment",
            "children": ["undeclared2", {"type": "literal", "value": 2}],
            "line": 2,
            "column": 2
        }
        symbol_table = {
            "variables": {},
            "errors": []
        }

        _handle_assignment(node1, symbol_table)
        _handle_assignment(node2, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 2)
        self.assertEqual(symbol_table["errors"][0]["var_name"], "undeclared1")
        self.assertEqual(symbol_table["errors"][1]["var_name"], "undeclared2")

    def test_declared_variable_does_not_call_traverse_on_error_path(self):
        """Verify _traverse_node is NOT called when variable is undeclared."""
        node = {
            "type": "assignment",
            "children": ["missing_var", {"type": "literal", "value": 999}],
            "line": 30,
            "column": 15
        }
        symbol_table = {
            "variables": {},
            "errors": []
        }

        with patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_while_package._traverse_node_package._handle_assignment_package._handle_assignment_src._traverse_node") as mock_traverse:
            _handle_assignment(node, symbol_table)

            mock_traverse.assert_not_called()
            self.assertEqual(len(symbol_table["errors"]), 1)

    def test_var_entry_missing_is_declared_key_treats_as_false(self):
        """Edge case: var_entry exists but missing is_declared key."""
        node = {
            "type": "assignment",
            "children": ["partial_var", {"type": "literal", "value": 7}],
            "line": 35,
            "column": 20
        }
        symbol_table = {
            "variables": {
                "partial_var": {
                    "data_type": "int",
                    "line": 33,
                    "column": 1,
                    "scope_level": 0
                }
            },
            "errors": []
        }

        _handle_assignment(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["var_name"], "partial_var")


if __name__ == "__main__":
    unittest.main()

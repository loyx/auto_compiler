# -*- coding: utf-8 -*-
"""
Unit tests for _handle_assignment function.
Tests variable declaration validation in assignment statements.
"""

import unittest
from typing import Any, Dict

from ._handle_assignment_src import _handle_assignment

# Type aliases matching the source
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleAssignment(unittest.TestCase):
    """Test cases for _handle_assignment function."""

    def test_declared_variable_assignment_success(self):
        """Happy path: Assignment to declared variable succeeds and updates position."""
        node: AST = {
            "type": "assignment",
            "value": "x",
            "line": 10,
            "column": 5
        }
        symbol_table: SymbolTable = {
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

        # No errors should be recorded
        self.assertEqual(len(symbol_table["errors"]), 0)
        # Last assignment position should be updated
        self.assertEqual(symbol_table["variables"]["x"]["last_assignment_line"], 10)
        self.assertEqual(symbol_table["variables"]["x"]["last_assignment_column"], 5)

    def test_undeclared_variable_records_error(self):
        """Error path: Assignment to undeclared variable records error."""
        node: AST = {
            "type": "assignment",
            "value": "y",
            "line": 15,
            "column": 8
        }
        symbol_table: SymbolTable = {
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

        # Error should be recorded
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["type"], "error")
        self.assertEqual(error["message"], "Variable 'y' used before declaration")
        self.assertEqual(error["line"], 15)
        self.assertEqual(error["column"], 8)
        # Variable should not be added to variables dict
        self.assertNotIn("y", symbol_table["variables"])

    def test_missing_variables_dict_creates_it(self):
        """Edge case: Missing variables dict in symbol_table is created."""
        node: AST = {
            "type": "assignment",
            "value": "z",
            "line": 20,
            "column": 3
        }
        symbol_table: SymbolTable = {
            "errors": []
        }

        _handle_assignment(node, symbol_table)

        # variables dict should be created
        self.assertIn("variables", symbol_table)
        self.assertIsInstance(symbol_table["variables"], dict)
        # Error should still be recorded for undeclared variable
        self.assertEqual(len(symbol_table["errors"]), 1)

    def test_missing_errors_dict_creates_it(self):
        """Edge case: Missing errors dict in symbol_table is created."""
        node: AST = {
            "type": "assignment",
            "value": "a",
            "line": 25,
            "column": 10
        }
        symbol_table: SymbolTable = {
            "variables": {
                "a": {
                    "data_type": "char",
                    "is_declared": True,
                    "line": 1,
                    "column": 1,
                    "scope_level": 0
                }
            }
        }

        _handle_assignment(node, symbol_table)

        # errors dict should be created
        self.assertIn("errors", symbol_table)
        self.assertIsInstance(symbol_table["errors"], list)
        # No errors for declared variable
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_missing_line_column_defaults_to_negative_one(self):
        """Edge case: Missing line/column in node defaults to -1."""
        node: AST = {
            "type": "assignment",
            "value": "b"
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "errors": []
        }

        _handle_assignment(node, symbol_table)

        # Error should be recorded with default line/column
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["line"], -1)
        self.assertEqual(error["column"], -1)

    def test_multiple_undeclared_variables_record_multiple_errors(self):
        """Multiple assignments to undeclared variables record multiple errors."""
        symbol_table: SymbolTable = {
            "variables": {},
            "errors": []
        }

        node1: AST = {"type": "assignment", "value": "x", "line": 1, "column": 1}
        node2: AST = {"type": "assignment", "value": "y", "line": 2, "column": 2}
        node3: AST = {"type": "assignment", "value": "x", "line": 3, "column": 3}

        _handle_assignment(node1, symbol_table)
        _handle_assignment(node2, symbol_table)
        _handle_assignment(node3, symbol_table)

        # Three errors should be recorded
        self.assertEqual(len(symbol_table["errors"]), 3)
        self.assertEqual(symbol_table["errors"][0]["message"], "Variable 'x' used before declaration")
        self.assertEqual(symbol_table["errors"][1]["message"], "Variable 'y' used before declaration")
        self.assertEqual(symbol_table["errors"][2]["message"], "Variable 'x' used before declaration")

    def test_declared_variable_preserves_existing_metadata(self):
        """Assignment to declared variable preserves existing metadata."""
        node: AST = {
            "type": "assignment",
            "value": "counter",
            "line": 50,
            "column": 12
        }
        symbol_table: SymbolTable = {
            "variables": {
                "counter": {
                    "data_type": "int",
                    "is_declared": True,
                    "line": 10,
                    "column": 5,
                    "scope_level": 1,
                    "custom_field": "preserved"
                }
            },
            "errors": []
        }

        _handle_assignment(node, symbol_table)

        # Existing metadata should be preserved
        self.assertEqual(symbol_table["variables"]["counter"]["data_type"], "int")
        self.assertEqual(symbol_table["variables"]["counter"]["line"], 10)
        self.assertEqual(symbol_table["variables"]["counter"]["column"], 5)
        self.assertEqual(symbol_table["variables"]["counter"]["scope_level"], 1)
        self.assertEqual(symbol_table["variables"]["counter"]["custom_field"], "preserved")
        # Only assignment position should be updated
        self.assertEqual(symbol_table["variables"]["counter"]["last_assignment_line"], 50)
        self.assertEqual(symbol_table["variables"]["counter"]["last_assignment_column"], 12)

    def test_empty_symbol_table_initializes_both_dicts(self):
        """Edge case: Completely empty symbol_table initializes both variables and errors."""
        node: AST = {
            "type": "assignment",
            "value": "test_var",
            "line": 100,
            "column": 50
        }
        symbol_table: SymbolTable = {}

        _handle_assignment(node, symbol_table)

        # Both dicts should be created
        self.assertIn("variables", symbol_table)
        self.assertIn("errors", symbol_table)
        # Error should be recorded for undeclared variable
        self.assertEqual(len(symbol_table["errors"]), 1)


if __name__ == "__main__":
    unittest.main()

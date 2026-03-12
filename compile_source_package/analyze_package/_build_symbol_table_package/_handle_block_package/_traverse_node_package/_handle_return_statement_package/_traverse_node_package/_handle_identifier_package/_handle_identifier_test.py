# -*- coding: utf-8 -*-
"""
Unit tests for _handle_identifier function.
Tests variable declaration validation and scope visibility checking.
"""

import unittest
from typing import Any, Dict

from ._handle_identifier_src import _handle_identifier

AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleIdentifier(unittest.TestCase):
    """Test cases for _handle_identifier function."""

    def test_happy_path_variable_declared_and_in_scope(self):
        """Test: variable is declared and visible in current scope - no error."""
        node: AST = {
            "type": "identifier",
            "value": "x",
            "line": 10,
            "column": 5,
        }
        symbol_table: SymbolTable = {
            "variables": {
                "x": {
                    "data_type": "int",
                    "is_declared": True,
                    "line": 5,
                    "column": 1,
                    "scope_level": 0,
                }
            },
            "current_scope": 0,
        }

        _handle_identifier(node, symbol_table)

        errors = symbol_table.get("errors", [])
        self.assertEqual(len(errors), 0)

    def test_variable_not_declared(self):
        """Test: variable not in symbol_table - error recorded."""
        node: AST = {
            "type": "identifier",
            "value": "undefined_var",
            "line": 15,
            "column": 8,
        }
        symbol_table: SymbolTable = {
            "variables": {
                "x": {
                    "data_type": "int",
                    "is_declared": True,
                    "line": 5,
                    "column": 1,
                    "scope_level": 0,
                }
            },
            "current_scope": 0,
        }

        _handle_identifier(node, symbol_table)

        errors = symbol_table.get("errors", [])
        self.assertEqual(len(errors), 1)
        self.assertIn("undefined_var", errors[0])
        self.assertIn("not declared", errors[0])
        self.assertIn("line 15", errors[0])
        self.assertIn("column 8", errors[0])

    def test_variable_out_of_scope(self):
        """Test: variable declared but scope_level > current_scope - error recorded."""
        node: AST = {
            "type": "identifier",
            "value": "outer_var",
            "line": 20,
            "column": 3,
        }
        symbol_table: SymbolTable = {
            "variables": {
                "outer_var": {
                    "data_type": "char",
                    "is_declared": True,
                    "line": 2,
                    "column": 1,
                    "scope_level": 2,
                }
            },
            "current_scope": 1,
        }

        _handle_identifier(node, symbol_table)

        errors = symbol_table.get("errors", [])
        self.assertEqual(len(errors), 1)
        self.assertIn("outer_var", errors[0])
        self.assertIn("out of scope", errors[0])
        self.assertIn("line 20", errors[0])
        self.assertIn("column 3", errors[0])

    def test_missing_value_field(self):
        """Test: identifier node missing 'value' field - error recorded."""
        node: AST = {
            "type": "identifier",
            "line": 25,
            "column": 10,
        }
        symbol_table: SymbolTable = {
            "variables": {
                "x": {
                    "data_type": "int",
                    "is_declared": True,
                    "line": 5,
                    "column": 1,
                    "scope_level": 0,
                }
            },
            "current_scope": 0,
        }

        _handle_identifier(node, symbol_table)

        errors = symbol_table.get("errors", [])
        self.assertEqual(len(errors), 1)
        self.assertIn("missing 'value' field", errors[0])
        self.assertIn("line 25", errors[0])
        self.assertIn("column 10", errors[0])

    def test_no_variables_table(self):
        """Test: symbol_table has no 'variables' key - error recorded."""
        node: AST = {
            "type": "identifier",
            "value": "any_var",
            "line": 30,
            "column": 7,
        }
        symbol_table: SymbolTable = {
            "current_scope": 0,
        }

        _handle_identifier(node, symbol_table)

        errors = symbol_table.get("errors", [])
        self.assertEqual(len(errors), 1)
        self.assertIn("any_var", errors[0])
        self.assertIn("not declared", errors[0])
        self.assertIn("no variable table", errors[0])

    def test_empty_variables_table(self):
        """Test: symbol_table['variables'] is empty - error recorded."""
        node: AST = {
            "type": "identifier",
            "value": "missing_var",
            "line": 35,
            "column": 12,
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "current_scope": 0,
        }

        _handle_identifier(node, symbol_table)

        errors = symbol_table.get("errors", [])
        self.assertEqual(len(errors), 1)
        self.assertIn("missing_var", errors[0])
        self.assertIn("not declared", errors[0])

    def test_line_column_from_node(self):
        """Test: line and column extracted from node directly."""
        node: AST = {
            "type": "identifier",
            "value": "test_var",
            "line": 100,
            "column": 50,
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "current_scope": 0,
        }

        _handle_identifier(node, symbol_table)

        errors = symbol_table.get("errors", [])
        self.assertEqual(len(errors), 1)
        self.assertIn("line 100", errors[0])
        self.assertIn("column 50", errors[0])

    def test_line_column_from_children_fallback(self):
        """Test: line and column extracted from children[0] when not in node."""
        node: AST = {
            "type": "identifier",
            "value": "child_var",
            "children": [
                {
                    "line": 200,
                    "column": 75,
                }
            ],
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "current_scope": 0,
        }

        _handle_identifier(node, symbol_table)

        errors = symbol_table.get("errors", [])
        self.assertEqual(len(errors), 1)
        self.assertIn("line 200", errors[0])
        self.assertIn("column 75", errors[0])

    def test_line_column_question_mark_fallback(self):
        """Test: line and column use '?' when unavailable from node or children."""
        node: AST = {
            "type": "identifier",
            "value": "unknown_loc",
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "current_scope": 0,
        }

        _handle_identifier(node, symbol_table)

        errors = symbol_table.get("errors", [])
        self.assertEqual(len(errors), 1)
        self.assertIn("line ?", errors[0])
        self.assertIn("column ?", errors[0])

    def test_line_from_node_column_from_children(self):
        """Test: line from node, column from children[0] (mixed fallback)."""
        node: AST = {
            "type": "identifier",
            "value": "mixed_var",
            "line": 300,
            "children": [
                {
                    "column": 99,
                }
            ],
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "current_scope": 0,
        }

        _handle_identifier(node, symbol_table)

        errors = symbol_table.get("errors", [])
        self.assertEqual(len(errors), 1)
        self.assertIn("line 300", errors[0])
        self.assertIn("column 99", errors[0])

    def test_errors_list_created_if_not_exists(self):
        """Test: errors list is created via setdefault if not present."""
        node: AST = {
            "type": "identifier",
            "value": "new_error_var",
            "line": 400,
            "column": 1,
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "current_scope": 0,
        }
        # Ensure 'errors' key does not exist initially
        self.assertNotIn("errors", symbol_table)

        _handle_identifier(node, symbol_table)

        self.assertIn("errors", symbol_table)
        self.assertIsInstance(symbol_table["errors"], list)
        self.assertEqual(len(symbol_table["errors"]), 1)

    def test_multiple_errors_accumulated(self):
        """Test: multiple calls accumulate errors in the list."""
        symbol_table: SymbolTable = {
            "variables": {
                "valid": {
                    "data_type": "int",
                    "is_declared": True,
                    "line": 1,
                    "column": 1,
                    "scope_level": 0,
                }
            },
            "current_scope": 0,
        }

        node1: AST = {"type": "identifier", "value": "invalid1", "line": 1, "column": 1}
        node2: AST = {"type": "identifier", "value": "invalid2", "line": 2, "column": 2}
        node3: AST = {"type": "identifier", "value": "valid", "line": 3, "column": 3}

        _handle_identifier(node1, symbol_table)
        _handle_identifier(node2, symbol_table)
        _handle_identifier(node3, symbol_table)

        errors = symbol_table.get("errors", [])
        self.assertEqual(len(errors), 2)
        self.assertIn("invalid1", errors[0])
        self.assertIn("invalid2", errors[1])

    def test_scope_level_equal_to_current_scope(self):
        """Test: variable with scope_level == current_scope is visible (no error)."""
        node: AST = {
            "type": "identifier",
            "value": "same_scope_var",
            "line": 500,
            "column": 10,
        }
        symbol_table: SymbolTable = {
            "variables": {
                "same_scope_var": {
                    "data_type": "int",
                    "is_declared": True,
                    "line": 100,
                    "column": 5,
                    "scope_level": 2,
                }
            },
            "current_scope": 2,
        }

        _handle_identifier(node, symbol_table)

        errors = symbol_table.get("errors", [])
        self.assertEqual(len(errors), 0)

    def test_scope_level_less_than_current_scope(self):
        """Test: variable with scope_level < current_scope is visible (no error)."""
        node: AST = {
            "type": "identifier",
            "value": "outer_visible_var",
            "line": 600,
            "column": 15,
        }
        symbol_table: SymbolTable = {
            "variables": {
                "outer_visible_var": {
                    "data_type": "char",
                    "is_declared": True,
                    "line": 50,
                    "column": 2,
                    "scope_level": 0,
                }
            },
            "current_scope": 3,
        }

        _handle_identifier(node, symbol_table)

        errors = symbol_table.get("errors", [])
        self.assertEqual(len(errors), 0)

    def test_children_empty_list(self):
        """Test: children is empty list - line/column fallback to '?'."""
        node: AST = {
            "type": "identifier",
            "value": "empty_children_var",
            "children": [],
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "current_scope": 0,
        }

        _handle_identifier(node, symbol_table)

        errors = symbol_table.get("errors", [])
        self.assertEqual(len(errors), 1)
        self.assertIn("line ?", errors[0])
        self.assertIn("column ?", errors[0])

    def test_children_first_not_dict(self):
        """Test: children[0] is not a dict - line/column fallback to '?'."""
        node: AST = {
            "type": "identifier",
            "value": "non_dict_child_var",
            "children": ["not_a_dict"],
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "current_scope": 0,
        }

        _handle_identifier(node, symbol_table)

        errors = symbol_table.get("errors", [])
        self.assertEqual(len(errors), 1)
        self.assertIn("line ?", errors[0])
        self.assertIn("column ?", errors[0])


if __name__ == "__main__":
    unittest.main()

# -*- coding: utf-8 -*-
"""Unit tests for _handle_if_statement function."""

import unittest
from typing import Any, Dict

from ._handle_if_statement_src import _handle_if_statement


AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleIfStatement(unittest.TestCase):
    """Test cases for _handle_if_statement function."""

    def test_condition_is_int_type_no_error(self):
        """Happy path: condition expression is int type, no error recorded."""
        node: AST = {
            "type": "if_statement",
            "children": [
                {"type": "expression", "data_type": "int", "line": 10, "column": 5},
                {"type": "block", "data_type": "void", "line": 10, "column": 20},
            ],
            "data_type": "void",
            "line": 10,
            "column": 1,
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 1,
            "scope_stack": [1],
            "errors": [],
        }

        _handle_if_statement(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_condition_is_char_type_records_error(self):
        """Error path: condition expression is char type, error recorded."""
        node: AST = {
            "type": "if_statement",
            "children": [
                {"type": "expression", "data_type": "char", "line": 15, "column": 8},
                {"type": "block", "data_type": "void", "line": 15, "column": 25},
            ],
            "data_type": "void",
            "line": 15,
            "column": 1,
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 1,
            "scope_stack": [1],
            "errors": [],
        }

        _handle_if_statement(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("Condition expression must be int type", symbol_table["errors"][0])
        self.assertIn("line 15", symbol_table["errors"][0])
        self.assertIn("column 1", symbol_table["errors"][0])

    def test_condition_is_void_type_records_error(self):
        """Error path: condition expression is void type, error recorded."""
        node: AST = {
            "type": "if_statement",
            "children": [
                {"type": "expression", "data_type": "void", "line": 20, "column": 3},
                {"type": "block", "data_type": "void", "line": 20, "column": 18},
            ],
            "data_type": "void",
            "line": 20,
            "column": 2,
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 1,
            "scope_stack": [1],
            "errors": [],
        }

        _handle_if_statement(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("Condition expression must be int type", symbol_table["errors"][0])

    def test_no_children_does_not_crash(self):
        """Edge case: node has no children key, function does not crash."""
        node: AST = {
            "type": "if_statement",
            "data_type": "void",
            "line": 25,
            "column": 1,
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 1,
            "scope_stack": [1],
            "errors": [],
        }

        _handle_if_statement(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_empty_children_list_does_not_crash(self):
        """Edge case: node has empty children list, function does not crash."""
        node: AST = {
            "type": "if_statement",
            "children": [],
            "data_type": "void",
            "line": 30,
            "column": 1,
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 1,
            "scope_stack": [1],
            "errors": [],
        }

        _handle_if_statement(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_condition_missing_data_type_records_error(self):
        """Edge case: condition node missing data_type, treated as non-int."""
        node: AST = {
            "type": "if_statement",
            "children": [
                {"type": "expression", "line": 35, "column": 10},
                {"type": "block", "data_type": "void", "line": 35, "column": 25},
            ],
            "data_type": "void",
            "line": 35,
            "column": 1,
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 1,
            "scope_stack": [1],
            "errors": [],
        }

        _handle_if_statement(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("Condition expression must be int type", symbol_table["errors"][0])

    def test_symbol_table_without_errors_key_creates_it(self):
        """Edge case: symbol_table without 'errors' key, function creates it."""
        node: AST = {
            "type": "if_statement",
            "children": [
                {"type": "expression", "data_type": "char", "line": 40, "column": 5},
                {"type": "block", "data_type": "void", "line": 40, "column": 20},
            ],
            "data_type": "void",
            "line": 40,
            "column": 1,
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 1,
            "scope_stack": [1],
        }

        _handle_if_statement(node, symbol_table)

        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)

    def test_multiple_if_statements_accumulate_errors(self):
        """Verify errors accumulate when processing multiple if statements."""
        node1: AST = {
            "type": "if_statement",
            "children": [
                {"type": "expression", "data_type": "char", "line": 45, "column": 1},
                {"type": "block", "data_type": "void", "line": 45, "column": 15},
            ],
            "data_type": "void",
            "line": 45,
            "column": 1,
        }
        node2: AST = {
            "type": "if_statement",
            "children": [
                {"type": "expression", "data_type": "void", "line": 50, "column": 2},
                {"type": "block", "data_type": "void", "line": 50, "column": 16},
            ],
            "data_type": "void",
            "line": 50,
            "column": 2,
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 1,
            "scope_stack": [1],
            "errors": [],
        }

        _handle_if_statement(node1, symbol_table)
        _handle_if_statement(node2, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 2)

    def test_condition_none_data_type_records_error(self):
        """Edge case: condition node has None as data_type."""
        node: AST = {
            "type": "if_statement",
            "children": [
                {"type": "expression", "data_type": None, "line": 55, "column": 7},
                {"type": "block", "data_type": "void", "line": 55, "column": 22},
            ],
            "data_type": "void",
            "line": 55,
            "column": 1,
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 1,
            "scope_stack": [1],
            "errors": [],
        }

        _handle_if_statement(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("Condition expression must be int type", symbol_table["errors"][0])

    def test_node_missing_line_column_uses_defaults(self):
        """Edge case: node missing line/column, error message uses defaults."""
        node: AST = {
            "type": "if_statement",
            "children": [
                {"type": "expression", "data_type": "char"},
                {"type": "block", "data_type": "void"},
            ],
            "data_type": "void",
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 1,
            "scope_stack": [1],
            "errors": [],
        }

        _handle_if_statement(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("line ?", symbol_table["errors"][0])
        self.assertIn("column ?", symbol_table["errors"][0])


if __name__ == "__main__":
    unittest.main()

# -*- coding: utf-8 -*-
"""
Unit tests for _handle_var_decl function.
Tests variable declaration handling, duplicate detection, and symbol table updates.
"""

import unittest
from typing import Any, Dict

from ._handle_var_decl_src import _handle_var_decl


AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleVarDecl(unittest.TestCase):
    """Test cases for _handle_var_decl function."""

    def test_new_variable_declaration(self):
        """Happy path: declaring a new variable should add it to symbol table."""
        node: AST = {
            "type": "var_decl",
            "value": "x",
            "data_type": "int",
            "line": 10,
            "column": 5
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "current_scope": 0,
            "errors": []
        }

        _handle_var_decl(node, symbol_table)

        self.assertIn("x", symbol_table["variables"])
        self.assertEqual(symbol_table["variables"]["x"]["data_type"], "int")
        self.assertTrue(symbol_table["variables"]["x"]["is_declared"])
        self.assertEqual(symbol_table["variables"]["x"]["line"], 10)
        self.assertEqual(symbol_table["variables"]["x"]["column"], 5)
        self.assertEqual(symbol_table["variables"]["x"]["scope_level"], 0)
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_char_variable_declaration(self):
        """Test declaring a char type variable."""
        node: AST = {
            "type": "var_decl",
            "value": "ch",
            "data_type": "char",
            "line": 15,
            "column": 3
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "current_scope": 0,
            "errors": []
        }

        _handle_var_decl(node, symbol_table)

        self.assertEqual(symbol_table["variables"]["ch"]["data_type"], "char")
        self.assertTrue(symbol_table["variables"]["ch"]["is_declared"])

    def test_same_scope_duplicate_declaration(self):
        """Duplicate declaration in same scope should record an error."""
        node1: AST = {
            "type": "var_decl",
            "value": "x",
            "data_type": "int",
            "line": 10,
            "column": 5
        }
        node2: AST = {
            "type": "var_decl",
            "value": "x",
            "data_type": "int",
            "line": 20,
            "column": 8
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "current_scope": 0,
            "errors": []
        }

        # First declaration
        _handle_var_decl(node1, symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 0)

        # Second declaration (duplicate in same scope)
        _handle_var_decl(node2, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertIn("already declared", error["message"])
        self.assertEqual(error["line"], 20)
        self.assertEqual(error["column"], 8)
        self.assertEqual(error["var_name"], "x")

    def test_different_scope_allows_shadowing(self):
        """Declaration in different scope should allow shadowing without error."""
        node1: AST = {
            "type": "var_decl",
            "value": "x",
            "data_type": "int",
            "line": 10,
            "column": 5
        }
        node2: AST = {
            "type": "var_decl",
            "value": "x",
            "data_type": "char",
            "line": 25,
            "column": 10
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "current_scope": 0,
            "errors": []
        }

        # First declaration at scope 0
        _handle_var_decl(node1, symbol_table)
        self.assertEqual(symbol_table["variables"]["x"]["scope_level"], 0)
        self.assertEqual(symbol_table["variables"]["x"]["data_type"], "int")

        # Change to scope 1
        symbol_table["current_scope"] = 1

        # Second declaration at scope 1 (shadowing)
        _handle_var_decl(node2, symbol_table)

        # Should not produce error
        self.assertEqual(len(symbol_table["errors"]), 0)
        # Should update to new scope's variable info
        self.assertEqual(symbol_table["variables"]["x"]["scope_level"], 1)
        self.assertEqual(symbol_table["variables"]["x"]["data_type"], "char")
        self.assertEqual(symbol_table["variables"]["x"]["line"], 25)

    def test_undeclared_variable_not_treated_as_duplicate(self):
        """Variable exists but is_declared=False should allow declaration."""
        symbol_table: SymbolTable = {
            "variables": {
                "x": {
                    "data_type": "int",
                    "is_declared": False,
                    "line": 5,
                    "column": 2,
                    "scope_level": 0
                }
            },
            "current_scope": 0,
            "errors": []
        }
        node: AST = {
            "type": "var_decl",
            "value": "x",
            "data_type": "int",
            "line": 10,
            "column": 5
        }

        _handle_var_decl(node, symbol_table)

        # Should not produce error
        self.assertEqual(len(symbol_table["errors"]), 0)
        # Should update is_declared to True
        self.assertTrue(symbol_table["variables"]["x"]["is_declared"])

    def test_initializes_errors_list_if_missing(self):
        """Should initialize errors list if not present in symbol_table."""
        node: AST = {
            "type": "var_decl",
            "value": "x",
            "data_type": "int",
            "line": 10,
            "column": 5
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "current_scope": 0
        }

        _handle_var_decl(node, symbol_table)

        self.assertIn("errors", symbol_table)
        self.assertIsInstance(symbol_table["errors"], list)

    def test_initializes_variables_dict_if_missing(self):
        """Should initialize variables dict if not present in symbol_table."""
        node: AST = {
            "type": "var_decl",
            "value": "x",
            "data_type": "int",
            "line": 10,
            "column": 5
        }
        symbol_table: SymbolTable = {
            "current_scope": 0,
            "errors": []
        }

        _handle_var_decl(node, symbol_table)

        self.assertIn("variables", symbol_table)
        self.assertIn("x", symbol_table["variables"])

    def test_default_current_scope_is_zero(self):
        """Should use 0 as default current_scope if not present."""
        node: AST = {
            "type": "var_decl",
            "value": "x",
            "data_type": "int",
            "line": 10,
            "column": 5
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "errors": []
        }

        _handle_var_decl(node, symbol_table)

        self.assertEqual(symbol_table["variables"]["x"]["scope_level"], 0)

    def test_multiple_variables_in_sequence(self):
        """Test declaring multiple different variables in sequence."""
        symbol_table: SymbolTable = {
            "variables": {},
            "current_scope": 0,
            "errors": []
        }

        for i, var_info in enumerate([
            ("a", "int", 10),
            ("b", "char", 20),
            ("c", "int", 30)
        ]):
            node: AST = {
                "type": "var_decl",
                "value": var_info[0],
                "data_type": var_info[1],
                "line": var_info[2],
                "column": 5
            }
            _handle_var_decl(node, symbol_table)

        self.assertEqual(len(symbol_table["variables"]), 3)
        self.assertIn("a", symbol_table["variables"])
        self.assertIn("b", symbol_table["variables"])
        self.assertIn("c", symbol_table["variables"])
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_multiple_duplicates_produce_multiple_errors(self):
        """Multiple duplicate declarations should produce multiple errors."""
        symbol_table: SymbolTable = {
            "variables": {},
            "current_scope": 0,
            "errors": []
        }

        # First declaration
        node1: AST = {
            "type": "var_decl",
            "value": "x",
            "data_type": "int",
            "line": 10,
            "column": 5
        }
        _handle_var_decl(node1, symbol_table)

        # Two duplicate declarations
        for line_num in [20, 30]:
            node: AST = {
                "type": "var_decl",
                "value": "x",
                "data_type": "int",
                "line": line_num,
                "column": 5
            }
            _handle_var_decl(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 2)
        self.assertEqual(symbol_table["errors"][0]["line"], 20)
        self.assertEqual(symbol_table["errors"][1]["line"], 30)

    def test_node_with_missing_fields(self):
        """Test handling node with missing optional fields (uses .get())."""
        node: AST = {
            "type": "var_decl",
            "value": "x"
            # Missing data_type, line, column
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "current_scope": 0,
            "errors": []
        }

        _handle_var_decl(node, symbol_table)

        # Should still add variable with None values for missing fields
        self.assertIn("x", symbol_table["variables"])
        self.assertIsNone(symbol_table["variables"]["x"]["data_type"])
        self.assertIsNone(symbol_table["variables"]["x"]["line"])
        self.assertIsNone(symbol_table["variables"]["x"]["column"])


if __name__ == "__main__":
    unittest.main()

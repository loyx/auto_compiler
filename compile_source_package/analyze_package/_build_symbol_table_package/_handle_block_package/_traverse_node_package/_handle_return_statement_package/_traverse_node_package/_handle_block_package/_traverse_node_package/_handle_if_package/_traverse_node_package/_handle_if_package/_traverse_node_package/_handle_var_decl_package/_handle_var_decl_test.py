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

    def test_happy_path_first_declaration(self):
        """Test normal variable declaration (first time)."""
        node: AST = {
            "type": "var_decl",
            "value": "x",
            "data_type": "int",
            "line": 10,
            "column": 5
        }
        symbol_table: SymbolTable = {
            "current_scope": 0,
            "variables": {}
        }

        _handle_var_decl(node, symbol_table)

        self.assertIn("x", symbol_table["variables"])
        var_info = symbol_table["variables"]["x"]
        self.assertEqual(var_info["data_type"], "int")
        self.assertTrue(var_info["is_declared"])
        self.assertEqual(var_info["line"], 10)
        self.assertEqual(var_info["column"], 5)
        self.assertEqual(var_info["scope_level"], 0)

    def test_happy_path_default_data_type(self):
        """Test variable declaration with default data_type (int)."""
        node: AST = {
            "type": "var_decl",
            "value": "y",
            "line": 15,
            "column": 3
        }
        symbol_table: SymbolTable = {
            "current_scope": 0,
            "variables": {}
        }

        _handle_var_decl(node, symbol_table)

        self.assertIn("y", symbol_table["variables"])
        self.assertEqual(symbol_table["variables"]["y"]["data_type"], "int")

    def test_happy_path_char_data_type(self):
        """Test variable declaration with char data_type."""
        node: AST = {
            "type": "var_decl",
            "value": "c",
            "data_type": "char",
            "line": 20,
            "column": 8
        }
        symbol_table: SymbolTable = {
            "current_scope": 0,
            "variables": {}
        }

        _handle_var_decl(node, symbol_table)

        self.assertEqual(symbol_table["variables"]["c"]["data_type"], "char")

    def test_duplicate_declaration_same_scope(self):
        """Test duplicate variable declaration at same scope level."""
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
            "line": 12,
            "column": 7
        }
        symbol_table: SymbolTable = {
            "current_scope": 0,
            "variables": {}
        }

        _handle_var_decl(node1, symbol_table)
        _handle_var_decl(node2, symbol_table)

        # Should have error recorded
        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["type"], "duplicate_declaration")
        self.assertIn("变量 'x' 重复声明", error["message"])
        self.assertEqual(error["line"], 12)
        self.assertEqual(error["column"], 7)

        # Original variable info should remain unchanged
        self.assertEqual(symbol_table["variables"]["x"]["line"], 10)

    def test_same_variable_different_scope(self):
        """Test same variable name at different scope levels (should NOT be error)."""
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
            "line": 20,
            "column": 3
        }
        symbol_table: SymbolTable = {
            "current_scope": 0,
            "variables": {}
        }

        # First declaration at scope 0
        _handle_var_decl(node1, symbol_table)

        # Change scope and declare again
        symbol_table["current_scope"] = 1
        _handle_var_decl(node2, symbol_table)

        # Should NOT have error
        self.assertNotIn("errors", symbol_table)

        # Variable info should be updated to new scope
        self.assertEqual(symbol_table["variables"]["x"]["data_type"], "char")
        self.assertEqual(symbol_table["variables"]["x"]["scope_level"], 1)
        self.assertEqual(symbol_table["variables"]["x"]["line"], 20)

    def test_boundary_empty_symbol_table(self):
        """Test with empty symbol_table (should initialize variables dict)."""
        node: AST = {
            "type": "var_decl",
            "value": "z",
            "data_type": "int",
            "line": 5,
            "column": 2
        }
        symbol_table: SymbolTable = {}

        _handle_var_decl(node, symbol_table)

        self.assertIn("variables", symbol_table)
        self.assertIn("z", symbol_table["variables"])
        self.assertEqual(symbol_table["variables"]["z"]["scope_level"], 0)

    def test_boundary_missing_node_fields(self):
        """Test with missing node fields (should use defaults)."""
        node: AST = {
            "type": "var_decl",
            "value": "a"
        }
        symbol_table: SymbolTable = {}

        _handle_var_decl(node, symbol_table)

        var_info = symbol_table["variables"]["a"]
        self.assertEqual(var_info["data_type"], "int")
        self.assertEqual(var_info["line"], 0)
        self.assertEqual(var_info["column"], 0)
        self.assertEqual(var_info["scope_level"], 0)

    def test_boundary_missing_current_scope(self):
        """Test when symbol_table missing current_scope (should default to 0)."""
        node: AST = {
            "type": "var_decl",
            "value": "b",
            "line": 8,
            "column": 4
        }
        symbol_table: SymbolTable = {
            "variables": {}
        }

        _handle_var_decl(node, symbol_table)

        self.assertEqual(symbol_table["variables"]["b"]["scope_level"], 0)

    def test_multiple_variables_different_names(self):
        """Test multiple variable declarations with different names."""
        symbol_table: SymbolTable = {
            "current_scope": 0,
            "variables": {}
        }

        for i, var_name in enumerate(["x", "y", "z"]):
            node: AST = {
                "type": "var_decl",
                "value": var_name,
                "data_type": "int",
                "line": 10 + i,
                "column": 5
            }
            _handle_var_decl(node, symbol_table)

        self.assertEqual(len(symbol_table["variables"]), 3)
        self.assertIn("x", symbol_table["variables"])
        self.assertIn("y", symbol_table["variables"])
        self.assertIn("z", symbol_table["variables"])

    def test_error_preserves_existing_errors(self):
        """Test that duplicate declaration error preserves existing errors."""
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
            "line": 12,
            "column": 7
        }
        symbol_table: SymbolTable = {
            "current_scope": 0,
            "variables": {},
            "errors": [
                {"type": "other_error", "message": "Pre-existing error", "line": 1}
            ]
        }

        _handle_var_decl(node1, symbol_table)
        _handle_var_decl(node2, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 2)
        self.assertEqual(symbol_table["errors"][0]["type"], "other_error")
        self.assertEqual(symbol_table["errors"][1]["type"], "duplicate_declaration")


if __name__ == "__main__":
    unittest.main()

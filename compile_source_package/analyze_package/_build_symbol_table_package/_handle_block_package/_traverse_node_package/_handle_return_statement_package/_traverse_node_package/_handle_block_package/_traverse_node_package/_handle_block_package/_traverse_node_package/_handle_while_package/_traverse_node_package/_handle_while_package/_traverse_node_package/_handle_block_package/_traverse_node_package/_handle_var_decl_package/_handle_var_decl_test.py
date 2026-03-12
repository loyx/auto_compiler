# -*- coding: utf-8 -*-
"""
Unit tests for _handle_var_decl function.
"""

import unittest
from typing import Any, Dict

from ._handle_var_decl_src import _handle_var_decl


class TestHandleVarDecl(unittest.TestCase):
    """Test cases for _handle_var_decl function."""

    def test_new_variable_declaration_var_name_field(self):
        """Test declaring a new variable using 'var_name' field."""
        node: Dict[str, Any] = {
            "type": "var_decl",
            "var_name": "x",
            "data_type": "int",
            "line": 10,
            "column": 5
        }
        symbol_table: Dict[str, Any] = {
            "current_scope": 0,
            "variables": {},
            "errors": []
        }

        _handle_var_decl(node, symbol_table)

        self.assertIn("x", symbol_table["variables"])
        var_info = symbol_table["variables"]["x"]
        self.assertEqual(var_info["data_type"], "int")
        self.assertTrue(var_info["is_declared"])
        self.assertEqual(var_info["line"], 10)
        self.assertEqual(var_info["column"], 5)
        self.assertEqual(var_info["scope_level"], 0)
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_new_variable_declaration_name_field(self):
        """Test declaring a new variable using 'name' field (fallback)."""
        node: Dict[str, Any] = {
            "type": "var_decl",
            "name": "y",
            "data_type": "char",
            "line": 20,
            "column": 3
        }
        symbol_table: Dict[str, Any] = {
            "current_scope": 0,
            "variables": {},
            "errors": []
        }

        _handle_var_decl(node, symbol_table)

        self.assertIn("y", symbol_table["variables"])
        var_info = symbol_table["variables"]["y"]
        self.assertEqual(var_info["data_type"], "char")
        self.assertEqual(var_info["line"], 20)
        self.assertEqual(var_info["column"], 3)

    def test_duplicate_declaration_same_scope(self):
        """Test duplicate variable declaration in the same scope."""
        node1: Dict[str, Any] = {
            "type": "var_decl",
            "var_name": "x",
            "data_type": "int",
            "line": 10,
            "column": 5
        }
        node2: Dict[str, Any] = {
            "type": "var_decl",
            "var_name": "x",
            "data_type": "char",
            "line": 15,
            "column": 8
        }
        symbol_table: Dict[str, Any] = {
            "current_scope": 0,
            "variables": {},
            "errors": []
        }

        _handle_var_decl(node1, symbol_table)
        _handle_var_decl(node2, symbol_table)

        # Variable info should remain from first declaration
        var_info = symbol_table["variables"]["x"]
        self.assertEqual(var_info["data_type"], "int")
        self.assertEqual(var_info["line"], 10)
        # Error should be recorded
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("already declared at line 10", symbol_table["errors"][0])

    def test_same_name_different_scope(self):
        """Test variable with same name in different scope (should be allowed)."""
        node1: Dict[str, Any] = {
            "type": "var_decl",
            "var_name": "x",
            "data_type": "int",
            "line": 10,
            "column": 5
        }
        node2: Dict[str, Any] = {
            "type": "var_decl",
            "var_name": "x",
            "data_type": "char",
            "line": 20,
            "column": 3
        }
        symbol_table: Dict[str, Any] = {
            "current_scope": 0,
            "variables": {},
            "errors": []
        }

        _handle_var_decl(node1, symbol_table)
        # Change scope
        symbol_table["current_scope"] = 1
        _handle_var_decl(node2, symbol_table)

        # Second declaration should overwrite (different scope)
        var_info = symbol_table["variables"]["x"]
        self.assertEqual(var_info["data_type"], "char")
        self.assertEqual(var_info["line"], 20)
        self.assertEqual(var_info["scope_level"], 1)
        # No error for different scope
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_default_data_type(self):
        """Test default data_type when not specified."""
        node: Dict[str, Any] = {
            "type": "var_decl",
            "var_name": "z",
            "line": 5,
            "column": 1
        }
        symbol_table: Dict[str, Any] = {
            "current_scope": 0,
            "variables": {},
            "errors": []
        }

        _handle_var_decl(node, symbol_table)

        var_info = symbol_table["variables"]["z"]
        self.assertEqual(var_info["data_type"], "int")

    def test_default_line_column(self):
        """Test default line and column when not specified."""
        node: Dict[str, Any] = {
            "type": "var_decl",
            "var_name": "w",
            "data_type": "char"
        }
        symbol_table: Dict[str, Any] = {
            "current_scope": 0,
            "variables": {},
            "errors": []
        }

        _handle_var_decl(node, symbol_table)

        var_info = symbol_table["variables"]["w"]
        self.assertEqual(var_info["line"], 0)
        self.assertEqual(var_info["column"], 0)

    def test_symbol_table_without_variables_key(self):
        """Test when symbol_table doesn't have 'variables' key."""
        node: Dict[str, Any] = {
            "type": "var_decl",
            "var_name": "a",
            "data_type": "int",
            "line": 1,
            "column": 1
        }
        symbol_table: Dict[str, Any] = {
            "current_scope": 0,
            "errors": []
        }

        _handle_var_decl(node, symbol_table)

        self.assertIn("variables", symbol_table)
        self.assertIn("a", symbol_table["variables"])

    def test_symbol_table_without_errors_key(self):
        """Test when symbol_table doesn't have 'errors' key."""
        node: Dict[str, Any] = {
            "type": "var_decl",
            "var_name": "b",
            "data_type": "int",
            "line": 1,
            "column": 1
        }
        symbol_table: Dict[str, Any] = {
            "current_scope": 0,
            "variables": {}
        }

        _handle_var_decl(node, symbol_table)

        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_symbol_table_without_current_scope(self):
        """Test when symbol_table doesn't have 'current_scope' key."""
        node: Dict[str, Any] = {
            "type": "var_decl",
            "var_name": "c",
            "data_type": "int",
            "line": 1,
            "column": 1
        }
        symbol_table: Dict[str, Any] = {
            "variables": {},
            "errors": []
        }

        _handle_var_decl(node, symbol_table)

        var_info = symbol_table["variables"]["c"]
        self.assertEqual(var_info["scope_level"], 0)

    def test_empty_symbol_table(self):
        """Test with completely empty symbol_table."""
        node: Dict[str, Any] = {
            "type": "var_decl",
            "var_name": "d",
            "data_type": "char",
            "line": 100,
            "column": 50
        }
        symbol_table: Dict[str, Any] = {}

        _handle_var_decl(node, symbol_table)

        self.assertIn("variables", symbol_table)
        self.assertIn("errors", symbol_table)
        self.assertIn("d", symbol_table["variables"])
        var_info = symbol_table["variables"]["d"]
        self.assertEqual(var_info["data_type"], "char")
        self.assertEqual(var_info["scope_level"], 0)

    def test_var_name_takes_precedence_over_name(self):
        """Test that 'var_name' field takes precedence over 'name' field."""
        node: Dict[str, Any] = {
            "type": "var_decl",
            "var_name": "priority",
            "name": "fallback",
            "data_type": "int",
            "line": 1,
            "column": 1
        }
        symbol_table: Dict[str, Any] = {
            "current_scope": 0,
            "variables": {},
            "errors": []
        }

        _handle_var_decl(node, symbol_table)

        self.assertIn("priority", symbol_table["variables"])
        self.assertNotIn("fallback", symbol_table["variables"])

    def test_multiple_variables_different_names(self):
        """Test declaring multiple variables with different names."""
        nodes: list = [
            {"type": "var_decl", "var_name": "x", "data_type": "int", "line": 1, "column": 1},
            {"type": "var_decl", "var_name": "y", "data_type": "char", "line": 2, "column": 2},
            {"type": "var_decl", "var_name": "z", "data_type": "int", "line": 3, "column": 3},
        ]
        symbol_table: Dict[str, Any] = {
            "current_scope": 0,
            "variables": {},
            "errors": []
        }

        for node in nodes:
            _handle_var_decl(node, symbol_table)

        self.assertEqual(len(symbol_table["variables"]), 3)
        self.assertIn("x", symbol_table["variables"])
        self.assertIn("y", symbol_table["variables"])
        self.assertIn("z", symbol_table["variables"])
        self.assertEqual(len(symbol_table["errors"]), 0)


if __name__ == "__main__":
    unittest.main()

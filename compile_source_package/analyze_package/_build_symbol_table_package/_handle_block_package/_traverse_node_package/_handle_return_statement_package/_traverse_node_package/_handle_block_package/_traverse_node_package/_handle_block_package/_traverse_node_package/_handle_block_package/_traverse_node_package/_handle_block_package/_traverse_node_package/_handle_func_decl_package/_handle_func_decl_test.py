#!/usr/bin/env python3
"""
Unit tests for _handle_func_decl function.
Tests function declaration node handling, symbol table registration, and duplicate detection.
"""

import unittest
from typing import Any, Dict

from ._handle_func_decl_src import _handle_func_decl


AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleFuncDecl(unittest.TestCase):
    """Test cases for _handle_func_decl function."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.symbol_table: SymbolTable = {
            "functions": {},
            "errors": [],
            "current_scope": 0,
            "scope_stack": []
        }

    def test_register_simple_function(self) -> None:
        """Test registering a simple function without parameters."""
        node: AST = {
            "type": "func_decl",
            "value": "main",
            "data_type": "int",
            "line": 1,
            "column": 0,
            "children": []
        }

        _handle_func_decl(node, self.symbol_table)

        self.assertIn("main", self.symbol_table["functions"])
        func_info = self.symbol_table["functions"]["main"]
        self.assertEqual(func_info["return_type"], "int")
        self.assertEqual(func_info["params"], [])
        self.assertEqual(func_info["line"], 1)
        self.assertEqual(func_info["column"], 0)
        self.assertEqual(len(self.symbol_table["errors"]), 0)

    def test_register_function_with_parameters(self) -> None:
        """Test registering a function with parameters."""
        node: AST = {
            "type": "func_decl",
            "value": "add",
            "data_type": "int",
            "line": 5,
            "column": 10,
            "children": [
                {
                    "type": "param_list",
                    "children": [
                        {
                            "type": "param",
                            "value": "a",
                            "data_type": "int"
                        },
                        {
                            "type": "param",
                            "value": "b",
                            "data_type": "int"
                        }
                    ]
                },
                {
                    "type": "block",
                    "children": []
                }
            ]
        }

        _handle_func_decl(node, self.symbol_table)

        self.assertIn("add", self.symbol_table["functions"])
        func_info = self.symbol_table["functions"]["add"]
        self.assertEqual(func_info["return_type"], "int")
        self.assertEqual(len(func_info["params"]), 2)
        self.assertEqual(func_info["params"][0]["name"], "a")
        self.assertEqual(func_info["params"][0]["data_type"], "int")
        self.assertEqual(func_info["params"][1]["name"], "b")
        self.assertEqual(func_info["params"][1]["data_type"], "int")
        self.assertEqual(func_info["line"], 5)
        self.assertEqual(func_info["column"], 10)

    def test_duplicate_function_declaration(self) -> None:
        """Test detecting duplicate function declaration."""
        node1: AST = {
            "type": "func_decl",
            "value": "foo",
            "data_type": "int",
            "line": 1,
            "column": 0,
            "children": []
        }

        node2: AST = {
            "type": "func_decl",
            "value": "foo",
            "data_type": "char",
            "line": 10,
            "column": 5,
            "children": []
        }

        _handle_func_decl(node1, self.symbol_table)
        _handle_func_decl(node2, self.symbol_table)

        self.assertEqual(len(self.symbol_table["errors"]), 1)
        error = self.symbol_table["errors"][0]
        self.assertEqual(error["type"], "duplicate_function_declaration")
        self.assertIn("foo", error["message"])
        self.assertEqual(error["line"], 10)
        self.assertEqual(error["column"], 5)
        self.assertEqual(error["function_name"], "foo")

        self.assertIn("foo", self.symbol_table["functions"])
        func_info = self.symbol_table["functions"]["foo"]
        self.assertEqual(func_info["return_type"], "int")

    def test_multiple_duplicate_declarations(self) -> None:
        """Test multiple duplicate declarations of the same function."""
        node1: AST = {
            "type": "func_decl",
            "value": "bar",
            "data_type": "int",
            "line": 1,
            "column": 0,
            "children": []
        }

        node2: AST = {
            "type": "func_decl",
            "value": "bar",
            "data_type": "int",
            "line": 5,
            "column": 0,
            "children": []
        }

        node3: AST = {
            "type": "func_decl",
            "value": "bar",
            "data_type": "int",
            "line": 10,
            "column": 0,
            "children": []
        }

        _handle_func_decl(node1, self.symbol_table)
        _handle_func_decl(node2, self.symbol_table)
        _handle_func_decl(node3, self.symbol_table)

        self.assertEqual(len(self.symbol_table["errors"]), 2)
        self.assertEqual(self.symbol_table["errors"][0]["line"], 5)
        self.assertEqual(self.symbol_table["errors"][1]["line"], 10)

    def test_function_with_char_return_type(self) -> None:
        """Test registering a function with char return type."""
        node: AST = {
            "type": "func_decl",
            "value": "get_char",
            "data_type": "char",
            "line": 3,
            "column": 2,
            "children": []
        }

        _handle_func_decl(node, self.symbol_table)

        self.assertIn("get_char", self.symbol_table["functions"])
        func_info = self.symbol_table["functions"]["get_char"]
        self.assertEqual(func_info["return_type"], "char")

    def test_default_return_type_when_missing(self) -> None:
        """Test default return type when data_type is missing."""
        node: AST = {
            "type": "func_decl",
            "value": "no_type",
            "line": 1,
            "column": 0,
            "children": []
        }

        _handle_func_decl(node, self.symbol_table)

        self.assertIn("no_type", self.symbol_table["functions"])
        func_info = self.symbol_table["functions"]["no_type"]
        self.assertEqual(func_info["return_type"], "int")

    def test_missing_line_column_defaults_to_zero(self) -> None:
        """Test default line and column when missing."""
        node: AST = {
            "type": "func_decl",
            "value": "no_pos",
            "data_type": "int",
            "children": []
        }

        _handle_func_decl(node, self.symbol_table)

        self.assertIn("no_pos", self.symbol_table["functions"])
        func_info = self.symbol_table["functions"]["no_pos"]
        self.assertEqual(func_info["line"], 0)
        self.assertEqual(func_info["column"], 0)

    def test_missing_children_defaults_to_empty(self) -> None:
        """Test default children when missing."""
        node: AST = {
            "type": "func_decl",
            "value": "no_children",
            "data_type": "int",
            "line": 1,
            "column": 0
        }

        _handle_func_decl(node, self.symbol_table)

        self.assertIn("no_children", self.symbol_table["functions"])
        func_info = self.symbol_table["functions"]["no_children"]
        self.assertEqual(func_info["params"], [])

    def test_param_list_not_first_child(self) -> None:
        """Test extracting param_list when it's not the first child."""
        node: AST = {
            "type": "func_decl",
            "value": "delayed_params",
            "data_type": "int",
            "line": 1,
            "column": 0,
            "children": [
                {
                    "type": "block",
                    "children": []
                },
                {
                    "type": "param_list",
                    "children": [
                        {
                            "type": "param",
                            "value": "x",
                            "data_type": "int"
                        }
                    ]
                }
            ]
        }

        _handle_func_decl(node, self.symbol_table)

        self.assertIn("delayed_params", self.symbol_table["functions"])
        func_info = self.symbol_table["functions"]["delayed_params"]
        self.assertEqual(len(func_info["params"]), 1)
        self.assertEqual(func_info["params"][0]["name"], "x")

    def test_param_list_with_non_param_children(self) -> None:
        """Test param_list with non-param children are ignored."""
        node: AST = {
            "type": "func_decl",
            "value": "mixed_params",
            "data_type": "int",
            "line": 1,
            "column": 0,
            "children": [
                {
                    "type": "param_list",
                    "children": [
                        {
                            "type": "param",
                            "value": "valid",
                            "data_type": "int"
                        },
                        {
                            "type": "other",
                            "value": "invalid"
                        },
                        {
                            "type": "param",
                            "value": "also_valid",
                            "data_type": "char"
                        }
                    ]
                }
            ]
        }

        _handle_func_decl(node, self.symbol_table)

        func_info = self.symbol_table["functions"]["mixed_params"]
        self.assertEqual(len(func_info["params"]), 2)
        self.assertEqual(func_info["params"][0]["name"], "valid")
        self.assertEqual(func_info["params"][1]["name"], "also_valid")

    def test_initializes_functions_dict_if_missing(self) -> None:
        """Test that functions dict is initialized if missing from symbol_table."""
        symbol_table: SymbolTable = {
            "errors": [],
            "current_scope": 0
        }

        node: AST = {
            "type": "func_decl",
            "value": "new_func",
            "data_type": "int",
            "line": 1,
            "column": 0,
            "children": []
        }

        _handle_func_decl(node, symbol_table)

        self.assertIn("functions", symbol_table)
        self.assertIn("new_func", symbol_table["functions"])

    def test_initializes_errors_list_if_missing(self) -> None:
        """Test that errors list is initialized if missing from symbol_table."""
        symbol_table: SymbolTable = {
            "functions": {}
        }

        node1: AST = {
            "type": "func_decl",
            "value": "dup",
            "data_type": "int",
            "line": 1,
            "column": 0,
            "children": []
        }

        node2: AST = {
            "type": "func_decl",
            "value": "dup",
            "data_type": "int",
            "line": 2,
            "column": 0,
            "children": []
        }

        _handle_func_decl(node1, symbol_table)
        _handle_func_decl(node2, symbol_table)

        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)

    def test_empty_symbol_table(self) -> None:
        """Test handling completely empty symbol table."""
        symbol_table: SymbolTable = {}

        node: AST = {
            "type": "func_decl",
            "value": "empty_test",
            "data_type": "int",
            "line": 1,
            "column": 0,
            "children": []
        }

        _handle_func_decl(node, symbol_table)

        self.assertIn("functions", symbol_table)
        self.assertIn("errors", symbol_table)
        self.assertIn("empty_test", symbol_table["functions"])

    def test_param_with_missing_data_type_defaults_to_int(self) -> None:
        """Test parameter with missing data_type defaults to int."""
        node: AST = {
            "type": "func_decl",
            "value": "param_no_type",
            "data_type": "int",
            "line": 1,
            "column": 0,
            "children": [
                {
                    "type": "param_list",
                    "children": [
                        {
                            "type": "param",
                            "value": "no_type_param"
                        }
                    ]
                }
            ]
        }

        _handle_func_decl(node, self.symbol_table)

        func_info = self.symbol_table["functions"]["param_no_type"]
        self.assertEqual(len(func_info["params"]), 1)
        self.assertEqual(func_info["params"][0]["data_type"], "int")

    def test_different_functions_do_not_conflict(self) -> None:
        """Test that different function names do not conflict."""
        node1: AST = {
            "type": "func_decl",
            "value": "func_a",
            "data_type": "int",
            "line": 1,
            "column": 0,
            "children": []
        }

        node2: AST = {
            "type": "func_decl",
            "value": "func_b",
            "data_type": "char",
            "line": 2,
            "column": 0,
            "children": []
        }

        _handle_func_decl(node1, self.symbol_table)
        _handle_func_decl(node2, self.symbol_table)

        self.assertEqual(len(self.symbol_table["functions"]), 2)
        self.assertIn("func_a", self.symbol_table["functions"])
        self.assertIn("func_b", self.symbol_table["functions"])
        self.assertEqual(len(self.symbol_table["errors"]), 0)


if __name__ == "__main__":
    unittest.main()

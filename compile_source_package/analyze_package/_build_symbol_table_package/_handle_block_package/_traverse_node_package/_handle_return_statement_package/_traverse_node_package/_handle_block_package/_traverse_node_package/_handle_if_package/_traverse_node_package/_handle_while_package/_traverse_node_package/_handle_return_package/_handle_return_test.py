# -*- coding: utf-8 -*-
"""
Unit tests for _handle_return function.
Tests return statement handling, scope validation, and type matching.
"""

import unittest
from typing import Any, Dict

from ._handle_return_src import _handle_return


AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleReturn(unittest.TestCase):
    """Test cases for _handle_return function."""

    def test_return_outside_function_records_error(self):
        """Test that return statement outside function records an error."""
        node: AST = {
            "type": "return",
            "line": 10,
            "column": 5
        }
        symbol_table: SymbolTable = {
            "current_function": None,
            "errors": []
        }

        _handle_return(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertEqual(symbol_table["errors"][0]["line"], 10)
        self.assertEqual(symbol_table["errors"][0]["column"], 5)
        self.assertEqual(
            symbol_table["errors"][0]["message"],
            "return statement outside of function"
        )

    def test_return_outside_function_without_errors_list(self):
        """Test that errors list is created if not present."""
        node: AST = {
            "type": "return",
            "line": 10,
            "column": 5
        }
        symbol_table: SymbolTable = {
            "current_function": None
        }

        _handle_return(node, symbol_table)

        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertEqual(
            symbol_table["errors"][0]["message"],
            "return statement outside of function"
        )

    def test_return_inside_function_no_type_check(self):
        """Test return inside function with no type info skips type check."""
        node: AST = {
            "type": "return",
            "line": 10,
            "column": 5
        }
        symbol_table: SymbolTable = {
            "current_function": "main",
            "functions": {
                "main": {
                    "return_type": "int",
                    "params": [],
                    "line": 1,
                    "column": 0
                }
            },
            "errors": []
        }

        _handle_return(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_return_type_match_no_error(self):
        """Test that matching return type produces no error."""
        node: AST = {
            "type": "return",
            "line": 10,
            "column": 5,
            "data_type": "int",
            "value": 42
        }
        symbol_table: SymbolTable = {
            "current_function": "main",
            "functions": {
                "main": {
                    "return_type": "int",
                    "params": [],
                    "line": 1,
                    "column": 0
                }
            },
            "errors": []
        }

        _handle_return(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_return_type_mismatch_records_error(self):
        """Test that mismatched return type records an error."""
        node: AST = {
            "type": "return",
            "line": 15,
            "column": 8,
            "data_type": "char",
            "value": "'a'"
        }
        symbol_table: SymbolTable = {
            "current_function": "getValue",
            "functions": {
                "getValue": {
                    "return_type": "int",
                    "params": [],
                    "line": 1,
                    "column": 0
                }
            },
            "errors": []
        }

        _handle_return(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertEqual(symbol_table["errors"][0]["line"], 15)
        self.assertEqual(symbol_table["errors"][0]["column"], 8)
        self.assertIn("return type mismatch", symbol_table["errors"][0]["message"])
        self.assertIn("expected int", symbol_table["errors"][0]["message"])
        self.assertIn("got char", symbol_table["errors"][0]["message"])

    def test_return_type_from_child_node(self):
        """Test that return type is extracted from child node if not on parent."""
        node: AST = {
            "type": "return",
            "line": 20,
            "column": 3,
            "children": [
                {
                    "type": "literal",
                    "data_type": "int",
                    "value": 100
                }
            ]
        }
        symbol_table: SymbolTable = {
            "current_function": "compute",
            "functions": {
                "compute": {
                    "return_type": "char",
                    "params": [],
                    "line": 1,
                    "column": 0
                }
            },
            "errors": []
        }

        _handle_return(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("expected char", symbol_table["errors"][0]["message"])
        self.assertIn("got int", symbol_table["errors"][0]["message"])

    def test_void_return_no_error(self):
        """Test that void return (no value) produces no error."""
        node: AST = {
            "type": "return",
            "line": 25,
            "column": 1,
            "children": []
        }
        symbol_table: SymbolTable = {
            "current_function": "voidFunc",
            "functions": {
                "voidFunc": {
                    "return_type": "void",
                    "params": [],
                    "line": 1,
                    "column": 0
                }
            },
            "errors": []
        }

        _handle_return(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_function_not_in_symbol_table_skips_check(self):
        """Test that missing function in symbol table skips type check."""
        node: AST = {
            "type": "return",
            "line": 30,
            "column": 2,
            "data_type": "int",
            "value": 5
        }
        symbol_table: SymbolTable = {
            "current_function": "unknownFunc",
            "functions": {
                "otherFunc": {
                    "return_type": "int",
                    "params": [],
                    "line": 1,
                    "column": 0
                }
            },
            "errors": []
        }

        _handle_return(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_node_without_line_column_uses_defaults(self):
        """Test that node without line/column uses default values."""
        node: AST = {
            "type": "return"
        }
        symbol_table: SymbolTable = {
            "current_function": None,
            "errors": []
        }

        _handle_return(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertEqual(symbol_table["errors"][0]["line"], 0)
        self.assertEqual(symbol_table["errors"][0]["column"], 0)

    def test_expected_type_none_skips_check(self):
        """Test that None expected type skips type check."""
        node: AST = {
            "type": "return",
            "line": 35,
            "column": 4,
            "data_type": "int",
            "value": 10
        }
        symbol_table: SymbolTable = {
            "current_function": "noReturnType",
            "functions": {
                "noReturnType": {
                    "params": [],
                    "line": 1,
                    "column": 0
                }
            },
            "errors": []
        }

        _handle_return(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_actual_type_none_skips_check(self):
        """Test that None actual type skips type check."""
        node: AST = {
            "type": "return",
            "line": 40,
            "column": 6,
            "value": "something"
        }
        symbol_table: SymbolTable = {
            "current_function": "someFunc",
            "functions": {
                "someFunc": {
                    "return_type": "int",
                    "params": [],
                    "line": 1,
                    "column": 0
                }
            },
            "errors": []
        }

        _handle_return(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_child_not_dict_skips_type_extraction(self):
        """Test that non-dict child nodes are skipped for type extraction."""
        node: AST = {
            "type": "return",
            "line": 45,
            "column": 7,
            "children": ["not_a_dict"]
        }
        symbol_table: SymbolTable = {
            "current_function": "testFunc",
            "functions": {
                "testFunc": {
                    "return_type": "int",
                    "params": [],
                    "line": 1,
                    "column": 0
                }
            },
            "errors": []
        }

        _handle_return(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 0)


if __name__ == "__main__":
    unittest.main()

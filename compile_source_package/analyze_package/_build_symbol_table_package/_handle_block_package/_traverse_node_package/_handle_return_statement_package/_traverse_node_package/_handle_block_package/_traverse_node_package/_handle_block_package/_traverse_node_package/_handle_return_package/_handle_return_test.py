# -*- coding: utf-8 -*-
"""Unit tests for _handle_return function."""

import unittest
from typing import Any, Dict

from ._handle_return_src import _handle_return


AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleReturn(unittest.TestCase):
    """Test cases for _handle_return function."""

    def test_return_inside_function_matching_type(self):
        """Happy path: return inside function with matching return type."""
        node: AST = {
            "type": "return",
            "data_type": "int",
            "line": 10,
            "column": 5
        }
        symbol_table: SymbolTable = {
            "current_function": "foo",
            "functions": {
                "foo": {"return_type": "int", "params": [], "line": 1, "column": 1}
            },
            "errors": []
        }
        
        _handle_return(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_return_inside_function_mismatched_type(self):
        """Return type mismatch should record error."""
        node: AST = {
            "type": "return",
            "data_type": "char",
            "line": 10,
            "column": 5
        }
        symbol_table: SymbolTable = {
            "current_function": "foo",
            "functions": {
                "foo": {"return_type": "int", "params": [], "line": 1, "column": 1}
            },
            "errors": []
        }
        
        _handle_return(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertEqual(symbol_table["errors"][0]["type"], "error")
        self.assertIn("Return type mismatch", symbol_table["errors"][0]["message"])
        self.assertEqual(symbol_table["errors"][0]["line"], 10)
        self.assertEqual(symbol_table["errors"][0]["column"], 5)

    def test_return_outside_function(self):
        """Return outside function should record error."""
        node: AST = {
            "type": "return",
            "data_type": "int",
            "line": 10,
            "column": 5
        }
        symbol_table: SymbolTable = {
            "current_function": None,
            "functions": {},
            "errors": []
        }
        
        _handle_return(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertEqual(symbol_table["errors"][0]["type"], "error")
        self.assertEqual(symbol_table["errors"][0]["message"], "Return statement outside function")
        self.assertEqual(symbol_table["errors"][0]["line"], 10)
        self.assertEqual(symbol_table["errors"][0]["column"], 5)

    def test_return_missing_errors_list(self):
        """Should create errors list if not present."""
        node: AST = {
            "type": "return",
            "data_type": "int",
            "line": 10,
            "column": 5
        }
        symbol_table: SymbolTable = {
            "current_function": None,
            "functions": {}
        }
        
        _handle_return(node, symbol_table)
        
        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)

    def test_return_missing_functions_dict(self):
        """Should handle missing functions dict gracefully."""
        node: AST = {
            "type": "return",
            "data_type": "int",
            "line": 10,
            "column": 5
        }
        symbol_table: SymbolTable = {
            "current_function": "foo",
            "errors": []
        }
        
        _handle_return(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_return_function_not_in_functions_dict(self):
        """Should handle current_function not in functions dict."""
        node: AST = {
            "type": "return",
            "data_type": "int",
            "line": 10,
            "column": 5
        }
        symbol_table: SymbolTable = {
            "current_function": "unknown_func",
            "functions": {
                "foo": {"return_type": "int", "params": [], "line": 1, "column": 1}
            },
            "errors": []
        }
        
        _handle_return(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_return_none_declared_return_type(self):
        """Should skip type check when declared return_type is None."""
        node: AST = {
            "type": "return",
            "data_type": "int",
            "line": 10,
            "column": 5
        }
        symbol_table: SymbolTable = {
            "current_function": "foo",
            "functions": {
                "foo": {"return_type": None, "params": [], "line": 1, "column": 1}
            },
            "errors": []
        }
        
        _handle_return(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_return_none_node_return_type(self):
        """Should skip type check when node data_type is None."""
        node: AST = {
            "type": "return",
            "data_type": None,
            "line": 10,
            "column": 5
        }
        symbol_table: SymbolTable = {
            "current_function": "foo",
            "functions": {
                "foo": {"return_type": "int", "params": [], "line": 1, "column": 1}
            },
            "errors": []
        }
        
        _handle_return(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_return_missing_line_column(self):
        """Should handle missing line/column with default -1."""
        node: AST = {
            "type": "return",
            "data_type": "int"
        }
        symbol_table: SymbolTable = {
            "current_function": None,
            "functions": {},
            "errors": []
        }
        
        _handle_return(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertEqual(symbol_table["errors"][0]["line"], -1)
        self.assertEqual(symbol_table["errors"][0]["column"], -1)


if __name__ == "__main__":
    unittest.main()

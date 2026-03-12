#!/usr/bin/env python3
"""
Unit tests for _handle_return_statement function.
Tests validation of return statement types against function signatures.
"""

import unittest
from typing import Any, Dict

from ._handle_return_statement_src import _handle_return_statement


class TestHandleReturnStatement(unittest.TestCase):
    """Test cases for _handle_return_statement function."""

    def test_return_type_matches_function_signature(self):
        """Happy path: return type matches function signature, no error."""
        node: Dict[str, Any] = {
            "type": "return_statement",
            "data_type": "int",
            "line": 10,
            "column": 5
        }
        symbol_table: Dict[str, Any] = {
            "variables": {},
            "functions": {
                "main": {
                    "return_type": "int",
                    "params": [],
                    "scope": 1
                }
            },
            "current_scope": 1,
            "scope_stack": [1],
            "current_function": "main",
            "errors": []
        }

        _handle_return_statement(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_return_type_mismatch(self):
        """Return type does not match function signature, error appended."""
        node: Dict[str, Any] = {
            "type": "return_statement",
            "data_type": "char",
            "line": 15,
            "column": 8
        }
        symbol_table: Dict[str, Any] = {
            "variables": {},
            "functions": {
                "calculate": {
                    "return_type": "int",
                    "params": [],
                    "scope": 1
                }
            },
            "current_scope": 1,
            "scope_stack": [1],
            "current_function": "calculate",
            "errors": []
        }

        _handle_return_statement(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("Return type 'char' does not match function 'calculate' return type 'int'",
                      symbol_table["errors"][0])
        self.assertIn("line 15", symbol_table["errors"][0])
        self.assertIn("column 8", symbol_table["errors"][0])

    def test_return_statement_outside_function_context(self):
        """Return statement when current_function is None."""
        node: Dict[str, Any] = {
            "type": "return_statement",
            "data_type": "int",
            "line": 5,
            "column": 3
        }
        symbol_table: Dict[str, Any] = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [0],
            "current_function": None,
            "errors": []
        }

        _handle_return_statement(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("Return statement outside function", symbol_table["errors"][0])
        self.assertIn("line 5", symbol_table["errors"][0])

    def test_function_not_found_in_symbol_table(self):
        """Current function not found in functions dict."""
        node: Dict[str, Any] = {
            "type": "return_statement",
            "data_type": "int",
            "line": 20,
            "column": 10
        }
        symbol_table: Dict[str, Any] = {
            "variables": {},
            "functions": {
                "other_func": {
                    "return_type": "int",
                    "params": [],
                    "scope": 1
                }
            },
            "current_scope": 1,
            "scope_stack": [1],
            "current_function": "nonexistent_func",
            "errors": []
        }

        _handle_return_statement(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("Return statement outside function", symbol_table["errors"][0])

    def test_node_without_data_type(self):
        """Node without data_type field, no error when types match or expected_type is None."""
        node: Dict[str, Any] = {
            "type": "return_statement",
            "line": 12,
            "column": 6
        }
        symbol_table: Dict[str, Any] = {
            "variables": {},
            "functions": {
                "test_func": {
                    "return_type": "int",
                    "params": [],
                    "scope": 1
                }
            },
            "current_scope": 1,
            "scope_stack": [1],
            "current_function": "test_func",
            "errors": []
        }

        _handle_return_statement(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_function_without_return_type(self):
        """Function signature without return_type, no comparison performed."""
        node: Dict[str, Any] = {
            "type": "return_statement",
            "data_type": "int",
            "line": 18,
            "column": 7
        }
        symbol_table: Dict[str, Any] = {
            "variables": {},
            "functions": {
                "void_func": {
                    "params": [],
                    "scope": 1
                }
            },
            "current_scope": 1,
            "scope_stack": [1],
            "current_function": "void_func",
            "errors": []
        }

        _handle_return_statement(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_symbol_table_without_errors_list(self):
        """Symbol table without errors list, function handles gracefully."""
        node: Dict[str, Any] = {
            "type": "return_statement",
            "data_type": "char",
            "line": 25,
            "column": 12
        }
        symbol_table: Dict[str, Any] = {
            "variables": {},
            "functions": {
                "main": {
                    "return_type": "int",
                    "params": [],
                    "scope": 1
                }
            },
            "current_scope": 1,
            "scope_stack": [1],
            "current_function": "main"
        }

        _handle_return_statement(node, symbol_table)

        self.assertNotIn("errors", symbol_table)

    def test_symbol_table_without_functions_dict(self):
        """Symbol table without functions dict, function handles gracefully."""
        node: Dict[str, Any] = {
            "type": "return_statement",
            "data_type": "int",
            "line": 30,
            "column": 15
        }
        symbol_table: Dict[str, Any] = {
            "variables": {},
            "current_scope": 1,
            "scope_stack": [1],
            "current_function": "main",
            "errors": []
        }

        _handle_return_statement(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_functions_dict_is_not_dict(self):
        """Functions field is not a dict, function handles gracefully."""
        node: Dict[str, Any] = {
            "type": "return_statement",
            "data_type": "int",
            "line": 35,
            "column": 18
        }
        symbol_table: Dict[str, Any] = {
            "variables": {},
            "functions": "not_a_dict",
            "current_scope": 1,
            "scope_stack": [1],
            "current_function": "main",
            "errors": []
        }

        _handle_return_statement(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_errors_list_is_not_list(self):
        """Errors field is not a list, function handles gracefully."""
        node: Dict[str, Any] = {
            "type": "return_statement",
            "data_type": "char",
            "line": 40,
            "column": 20
        }
        symbol_table: Dict[str, Any] = {
            "variables": {},
            "functions": {
                "main": {
                    "return_type": "int",
                    "params": [],
                    "scope": 1
                }
            },
            "current_scope": 1,
            "scope_stack": [1],
            "current_function": "main",
            "errors": "not_a_list"
        }

        _handle_return_statement(node, symbol_table)

        self.assertEqual(symbol_table["errors"], "not_a_list")

    def test_multiple_return_type_mismatches(self):
        """Multiple return type mismatches accumulate errors."""
        symbol_table: Dict[str, Any] = {
            "variables": {},
            "functions": {
                "func1": {
                    "return_type": "int",
                    "params": [],
                    "scope": 1
                }
            },
            "current_scope": 1,
            "scope_stack": [1],
            "current_function": "func1",
            "errors": []
        }

        node1: Dict[str, Any] = {
            "type": "return_statement",
            "data_type": "char",
            "line": 50,
            "column": 5
        }
        node2: Dict[str, Any] = {
            "type": "return_statement",
            "data_type": "char",
            "line": 55,
            "column": 10
        }

        _handle_return_statement(node1, symbol_table)
        _handle_return_statement(node2, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 2)

    def test_node_without_line_column(self):
        """Node without line/column uses default values."""
        node: Dict[str, Any] = {
            "type": "return_statement",
            "data_type": "char"
        }
        symbol_table: Dict[str, Any] = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [0],
            "current_function": None,
            "errors": []
        }

        _handle_return_statement(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("line 0", symbol_table["errors"][0])
        self.assertIn("column 0", symbol_table["errors"][0])


if __name__ == "__main__":
    unittest.main()

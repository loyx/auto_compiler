#!/usr/bin/env python3
"""
Unit tests for _handle_function_call function.
"""

import unittest
from unittest.mock import patch, MagicMock
from typing import Any, Dict

from ._handle_function_call_src import _handle_function_call


class TestHandleFunctionCall(unittest.TestCase):
    """Test cases for _handle_function_call function."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_traverse_node = MagicMock()

    def _create_node(
        self,
        node_type: str = "function_call",
        value: str = "",
        children: list = None,
        line: int = 1,
        column: int = 1
    ) -> Dict[str, Any]:
        """Helper to create AST nodes."""
        return {
            "type": node_type,
            "value": value,
            "children": children if children is not None else [],
            "line": line,
            "column": column
        }

    def _create_symbol_table(
        self,
        functions: Dict[str, Any] = None,
        variables: Dict[str, Any] = None,
        errors: list = None
    ) -> Dict[str, Any]:
        """Helper to create symbol tables."""
        return {
            "functions": functions if functions is not None else {},
            "variables": variables if variables is not None else {},
            "current_scope": 1,
            "scope_stack": [],
            "errors": errors if errors is not None else []
        }

    @patch('._handle_function_call_src._traverse_node')
    def test_function_declared_correct_params(self, mock_traverse):
        """Happy path: function is declared with correct parameter count."""
        node = self._create_node(value="my_func", children=[
            self._create_node(node_type="literal", value=1),
            self._create_node(node_type="literal", value=2)
        ], line=5, column=10)

        symbol_table = self._create_symbol_table(
            functions={
                "my_func": {
                    "return_type": "int",
                    "params": ["a", "b"],
                    "line": 1,
                    "column": 1
                }
            },
            errors=[]
        )

        _handle_function_call(node, symbol_table)

        # No errors should be added
        self.assertEqual(len(symbol_table["errors"]), 0)
        # _traverse_node should be called for each argument
        self.assertEqual(mock_traverse.call_count, 2)

    @patch('._handle_function_call_src._traverse_node')
    def test_function_not_declared(self, mock_traverse):
        """Function not declared should add error but still traverse parameters."""
        node = self._create_node(value="undefined_func", children=[
            self._create_node(node_type="literal", value=42)
        ], line=10, column=5)

        symbol_table = self._create_symbol_table(
            functions={"other_func": {"return_type": "void", "params": []}},
            errors=[]
        )

        _handle_function_call(node, symbol_table)

        # Error should be added
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["type"], "error")
        self.assertIn("Undefined function: undefined_func", error["message"])
        self.assertEqual(error["line"], 10)
        self.assertEqual(error["column"], 5)
        # Parameters should still be traversed
        mock_traverse.assert_called_once()

    @patch('._handle_function_call_src._traverse_node')
    def test_parameter_count_mismatch_too_many(self, mock_traverse):
        """Too many parameters should add error."""
        node = self._create_node(value="my_func", children=[
            self._create_node(node_type="literal", value=1),
            self._create_node(node_type="literal", value=2),
            self._create_node(node_type="literal", value=3)
        ], line=7, column=3)

        symbol_table = self._create_symbol_table(
            functions={
                "my_func": {
                    "return_type": "int",
                    "params": ["a", "b"],
                    "line": 1,
                    "column": 1
                }
            },
            errors=[]
        )

        _handle_function_call(node, symbol_table)

        # Error should be added
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertIn("expects 2 arguments, got 3", error["message"])
        self.assertEqual(error["line"], 7)
        self.assertEqual(error["column"], 3)
        # All parameters should still be traversed
        self.assertEqual(mock_traverse.call_count, 3)

    @patch('._handle_function_call_src._traverse_node')
    def test_parameter_count_mismatch_too_few(self, mock_traverse):
        """Too few parameters should add error."""
        node = self._create_node(value="my_func", children=[
            self._create_node(node_type="literal", value=1)
        ], line=8, column=4)

        symbol_table = self._create_symbol_table(
            functions={
                "my_func": {
                    "return_type": "int",
                    "params": ["a", "b", "c"],
                    "line": 1,
                    "column": 1
                }
            },
            errors=[]
        )

        _handle_function_call(node, symbol_table)

        # Error should be added
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertIn("expects 3 arguments, got 1", error["message"])

    @patch('._handle_function_call_src._traverse_node')
    def test_no_parameters(self, mock_traverse):
        """Function call with no parameters."""
        node = self._create_node(value="no_args_func", children=[], line=3, column=2)

        symbol_table = self._create_symbol_table(
            functions={
                "no_args_func": {
                    "return_type": "void",
                    "params": [],
                    "line": 1,
                    "column": 1
                }
            },
            errors=[]
        )

        _handle_function_call(node, symbol_table)

        # No errors
        self.assertEqual(len(symbol_table["errors"]), 0)
        # No traversals needed
        mock_traverse.assert_not_called()

    @patch('._handle_function_call_src._traverse_node')
    def test_no_parameters_but_function_expects_some(self, mock_traverse):
        """Function expects parameters but none provided."""
        node = self._create_node(value="expects_args", children=[], line=4, column=1)

        symbol_table = self._create_symbol_table(
            functions={
                "expects_args": {
                    "return_type": "int",
                    "params": ["x"],
                    "line": 1,
                    "column": 1
                }
            },
            errors=[]
        )

        _handle_function_call(node, symbol_table)

        # Error should be added
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertIn("expects 1 arguments, got 0", error["message"])

    def test_errors_list_initialized_if_missing(self):
        """Errors list should be initialized if not present in symbol_table."""
        node = self._create_node(value="test_func", children=[], line=1, column=1)

        symbol_table = {
            "functions": {},
            "variables": {},
            "current_scope": 1
        }

        _handle_function_call(node, symbol_table)

        # errors list should be created
        self.assertIn("errors", symbol_table)
        self.assertIsInstance(symbol_table["errors"], list)
        # Error should be added for undefined function
        self.assertEqual(len(symbol_table["errors"]), 1)

    @patch('._handle_function_call_src._traverse_node')
    def test_functions_key_missing_in_symbol_table(self, mock_traverse):
        """Functions key missing should be treated as undefined function."""
        node = self._create_node(value="any_func", children=[
            self._create_node(node_type="literal", value=1)
        ], line=6, column=7)

        symbol_table = {
            "variables": {},
            "current_scope": 1,
            "errors": []
        }

        _handle_function_call(node, symbol_table)

        # Error should be added
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertIn("Undefined function: any_func", error["message"])
        # Parameters should still be traversed
        mock_traverse.assert_called_once()

    @patch('._handle_function_call_src._traverse_node')
    def test_multiple_function_calls_accumulate_errors(self, mock_traverse):
        """Multiple issues should accumulate errors."""
        node = self._create_node(value="bad_func", children=[
            self._create_node(node_type="literal", value=1),
            self._create_node(node_type="literal", value=2)
        ], line=9, column=8)

        symbol_table = self._create_symbol_table(
            functions={
                "bad_func": {
                    "return_type": "int",
                    "params": ["x"],
                    "line": 1,
                    "column": 1
                }
            },
            errors=[{"type": "error", "message": "pre-existing error"}]
        )

        _handle_function_call(node, symbol_table)

        # Should have 2 errors (pre-existing + parameter mismatch)
        self.assertEqual(len(symbol_table["errors"]), 2)
        self.assertEqual(symbol_table["errors"][0]["message"], "pre-existing error")
        self.assertIn("expects 1 arguments, got 2", symbol_table["errors"][1]["message"])

    @patch('._handle_function_call_src._traverse_node')
    def test_node_missing_value_field(self, mock_traverse):
        """Node missing value field should handle gracefully."""
        node = {
            "type": "function_call",
            "children": [],
            "line": 1,
            "column": 1
        }

        symbol_table = self._create_symbol_table(errors=[])

        _handle_function_call(node, symbol_table)

        # Should add error for empty function name
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertIn("Undefined function: ", error["message"])

    @patch('._handle_function_call_src._traverse_node')
    def test_node_missing_position_fields(self, mock_traverse):
        """Node missing line/column should use defaults."""
        node = {
            "type": "function_call",
            "value": "test_func",
            "children": []
        }

        symbol_table = self._create_symbol_table(errors=[])

        _handle_function_call(node, symbol_table)

        # Error should use default position
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["line"], -1)
        self.assertEqual(error["column"], -1)

    @patch('._handle_function_call_src._traverse_node')
    def test_traverse_node_called_with_correct_args(self, mock_traverse):
        """Verify _traverse_node is called with correct arguments."""
        arg_node = self._create_node(node_type="identifier", value="x")
        node = self._create_node(value="my_func", children=[arg_node], line=1, column=1)

        symbol_table = self._create_symbol_table(
            functions={
                "my_func": {
                    "return_type": "void",
                    "params": ["x"],
                    "line": 1,
                    "column": 1
                }
            },
            errors=[]
        )

        _handle_function_call(node, symbol_table)

        mock_traverse.assert_called_once_with(arg_node, symbol_table)

    @patch('._handle_function_call_src._traverse_node')
    def test_function_with_no_params_field(self, mock_traverse):
        """Function declaration missing params field should be handled."""
        node = self._create_node(value="my_func", children=[
            self._create_node(node_type="literal", value=1)
        ], line=1, column=1)

        symbol_table = self._create_symbol_table(
            functions={
                "my_func": {
                    "return_type": "void",
                    "line": 1,
                    "column": 1
                }
            },
            errors=[]
        )

        _handle_function_call(node, symbol_table)

        # Should treat missing params as empty list
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertIn("expects 0 arguments, got 1", error["message"])


if __name__ == "__main__":
    unittest.main()

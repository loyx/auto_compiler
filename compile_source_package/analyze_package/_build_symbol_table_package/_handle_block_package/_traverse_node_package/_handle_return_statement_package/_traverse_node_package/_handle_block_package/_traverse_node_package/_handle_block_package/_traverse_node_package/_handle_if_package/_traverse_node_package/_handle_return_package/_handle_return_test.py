#!/usr/bin/env python3
"""Unit tests for _handle_return function."""

import unittest
from typing import Any, Dict

from ._handle_return_src import _handle_return

AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleReturn(unittest.TestCase):
    """Test cases for _handle_return function."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 1,
            "scope_stack": [1],
            "current_function": None,
            "errors": []
        }

    def _create_return_node(
        self,
        data_type: str | None = None,
        line: int = 1,
        column: int = 1
    ) -> AST:
        """Helper to create a return statement node."""
        node: AST = {
            "type": "return",
            "children": [],
            "line": line,
            "column": column
        }
        if data_type is not None:
            node["data_type"] = data_type
        return node

    def _create_function_decl(
        self,
        return_type: str | None = None,
        line: int = 0,
        column: int = 0
    ) -> Dict[str, Any]:
        """Helper to create a function declaration."""
        return {
            "return_type": return_type,
            "params": [],
            "line": line,
            "column": column
        }

    def test_return_inside_function_with_matching_type(self) -> None:
        """Happy path: return inside function with matching return type."""
        self.symbol_table["current_function"] = "main"
        self.symbol_table["functions"]["main"] = self._create_function_decl(
            return_type="int"
        )
        node = self._create_return_node(data_type="int", line=5, column=10)

        _handle_return(node, self.symbol_table)

        self.assertEqual(len(self.symbol_table["errors"]), 0)

    def test_return_outside_function(self) -> None:
        """Error: return statement when not inside any function."""
        self.symbol_table["current_function"] = None
        node = self._create_return_node(data_type="int", line=3, column=5)

        _handle_return(node, self.symbol_table)

        self.assertEqual(len(self.symbol_table["errors"]), 1)
        error = self.symbol_table["errors"][0]
        self.assertEqual(error["type"], "error")
        self.assertEqual(error["message"], "return statement outside function")
        self.assertEqual(error["line"], 3)
        self.assertEqual(error["column"], 5)

    def test_return_function_declaration_missing(self) -> None:
        """Error: current_function set but function not in symbol table."""
        self.symbol_table["current_function"] = "nonexistent"
        self.symbol_table["functions"] = {}
        node = self._create_return_node(data_type="int", line=7, column=2)

        _handle_return(node, self.symbol_table)

        self.assertEqual(len(self.symbol_table["errors"]), 1)
        error = self.symbol_table["errors"][0]
        self.assertEqual(error["type"], "error")
        self.assertEqual(error["message"], "return statement outside function")
        self.assertEqual(error["line"], 7)
        self.assertEqual(error["column"], 2)

    def test_return_type_mismatch(self) -> None:
        """Error: return type does not match function declaration."""
        self.symbol_table["current_function"] = "calculate"
        self.symbol_table["functions"]["calculate"] = self._create_function_decl(
            return_type="int"
        )
        node = self._create_return_node(data_type="string", line=12, column=8)

        _handle_return(node, self.symbol_table)

        self.assertEqual(len(self.symbol_table["errors"]), 1)
        error = self.symbol_table["errors"][0]
        self.assertEqual(error["type"], "error")
        self.assertEqual(error["message"], "Return type mismatch")
        self.assertEqual(error["line"], 12)
        self.assertEqual(error["column"], 8)

    def test_return_no_data_type(self) -> None:
        """Edge case: return node without data_type field."""
        self.symbol_table["current_function"] = "void_func"
        self.symbol_table["functions"]["void_func"] = self._create_function_decl(
            return_type="void"
        )
        node = self._create_return_node(data_type=None, line=4, column=1)

        _handle_return(node, self.symbol_table)

        self.assertEqual(len(self.symbol_table["errors"]), 0)

    def test_return_no_declared_return_type(self) -> None:
        """Edge case: function without declared return type."""
        self.symbol_table["current_function"] = "unknown_func"
        self.symbol_table["functions"]["unknown_func"] = self._create_function_decl(
            return_type=None
        )
        node = self._create_return_node(data_type="int", line=6, column=3)

        _handle_return(node, self.symbol_table)

        self.assertEqual(len(self.symbol_table["errors"]), 0)

    def test_return_both_types_none(self) -> None:
        """Edge case: both return_type and declared_return_type are None."""
        self.symbol_table["current_function"] = "void_func"
        self.symbol_table["functions"]["void_func"] = self._create_function_decl(
            return_type=None
        )
        node = self._create_return_node(data_type=None, line=8, column=4)

        _handle_return(node, self.symbol_table)

        self.assertEqual(len(self.symbol_table["errors"]), 0)

    def test_return_preserves_existing_errors(self) -> None:
        """Verify that new errors are appended, not replacing existing ones."""
        self.symbol_table["current_function"] = None
        self.symbol_table["errors"].append({
            "type": "error",
            "message": "pre-existing error",
            "line": 1,
            "column": 1
        })
        node = self._create_return_node(data_type="int", line=2, column=2)

        _handle_return(node, self.symbol_table)

        self.assertEqual(len(self.symbol_table["errors"]), 2)
        self.assertEqual(
            self.symbol_table["errors"][0]["message"],
            "pre-existing error"
        )
        self.assertEqual(
            self.symbol_table["errors"][1]["message"],
            "return statement outside function"
        )

    def test_return_default_line_column(self) -> None:
        """Verify default line/column values when not provided."""
        self.symbol_table["current_function"] = None
        node: AST = {
            "type": "return",
            "children": []
        }

        _handle_return(node, self.symbol_table)

        self.assertEqual(len(self.symbol_table["errors"]), 1)
        error = self.symbol_table["errors"][0]
        self.assertEqual(error["line"], 0)
        self.assertEqual(error["column"], 0)

    def test_return_empty_functions_dict(self) -> None:
        """Edge case: functions dict exists but is empty."""
        self.symbol_table["current_function"] = "missing_func"
        self.symbol_table["functions"] = {}
        node = self._create_return_node(data_type="int", line=10, column=5)

        _handle_return(node, self.symbol_table)

        self.assertEqual(len(self.symbol_table["errors"]), 1)
        self.assertEqual(
            self.symbol_table["errors"][0]["message"],
            "return statement outside function"
        )

    def test_return_multiple_type_mismatches(self) -> None:
        """Verify multiple type mismatches are all recorded."""
        self.symbol_table["current_function"] = "func"
        self.symbol_table["functions"]["func"] = self._create_function_decl(
            return_type="int"
        )
        node1 = self._create_return_node(data_type="string", line=1, column=1)
        node2 = self._create_return_node(data_type="float", line=2, column=2)

        _handle_return(node1, self.symbol_table)
        _handle_return(node2, self.symbol_table)

        self.assertEqual(len(self.symbol_table["errors"]), 2)
        self.assertEqual(
            self.symbol_table["errors"][0]["message"],
            "Return type mismatch"
        )
        self.assertEqual(
            self.symbol_table["errors"][1]["message"],
            "Return type mismatch"
        )


if __name__ == "__main__":
    unittest.main()

# -*- coding: utf-8 -*-
"""
Unit tests for _verify_return_stmt function.
"""

import unittest
from typing import Any, Dict, List

from ._verify_return_stmt_src import _verify_return_stmt


class TestVerifyReturnStmt(unittest.TestCase):
    """Test cases for _verify_return_stmt function."""

    def setUp(self) -> None:
        """Set up common test fixtures."""
        self.filename = "test.c"
        self.default_symbol_table: Dict[str, Any] = {
            "variables": {},
            "functions": {},
            "current_scope": 1,
        }

    # ==================== Happy Path Tests ====================

    def test_void_function_no_return_value(self) -> None:
        """Test void function with no return value - should pass."""
        node: Dict[str, Any] = {
            "type": "return_stmt",
            "value": None,
            "line": 10,
            "column": 5,
        }
        context_stack: List[Dict[str, Any]] = [
            {"type": "function", "name": "main", "return_type": "void"}
        ]

        # Should not raise
        _verify_return_stmt(node, self.default_symbol_table, context_stack, self.filename)

    def test_int_function_with_int_literal(self) -> None:
        """Test int function returning int literal - should pass."""
        node: Dict[str, Any] = {
            "type": "return_stmt",
            "value": {
                "type": "int_literal",
                "data_type": "int",
                "line": 10,
                "column": 12,
            },
            "line": 10,
            "column": 5,
        }
        context_stack: List[Dict[str, Any]] = [
            {"type": "function", "name": "foo", "return_type": "int"}
        ]

        # Should not raise
        _verify_return_stmt(node, self.default_symbol_table, context_stack, self.filename)

    def test_char_function_with_char_literal(self) -> None:
        """Test char function returning char literal - should pass."""
        node: Dict[str, Any] = {
            "type": "return_stmt",
            "value": {
                "type": "char_literal",
                "data_type": "char",
                "line": 15,
                "column": 8,
            },
            "line": 15,
            "column": 5,
        }
        context_stack: List[Dict[str, Any]] = [
            {"type": "function", "name": "get_char", "return_type": "char"}
        ]

        # Should not raise
        _verify_return_stmt(node, self.default_symbol_table, context_stack, self.filename)

    def test_int_function_returning_variable_of_int_type(self) -> None:
        """Test int function returning variable of int type - should pass."""
        symbol_table: Dict[str, Any] = {
            "variables": {
                "x": {"data_type": "int", "scope": 1},
            },
            "functions": {},
            "current_scope": 1,
        }
        node: Dict[str, Any] = {
            "type": "return_stmt",
            "value": {
                "type": "variable_ref",
                "name": "x",
                "line": 20,
                "column": 10,
            },
            "line": 20,
            "column": 5,
        }
        context_stack: List[Dict[str, Any]] = [
            {"type": "function", "name": "get_value", "return_type": "int"}
        ]

        # Should not raise
        _verify_return_stmt(node, symbol_table, context_stack, self.filename)

    def test_int_function_with_binary_op_return(self) -> None:
        """Test int function returning binary operation - should pass."""
        node: Dict[str, Any] = {
            "type": "return_stmt",
            "value": {
                "type": "binary_op",
                "data_type": "int",
                "line": 25,
                "column": 12,
            },
            "line": 25,
            "column": 5,
        }
        context_stack: List[Dict[str, Any]] = [
            {"type": "function", "name": "compute", "return_type": "int"}
        ]

        # Should not raise
        _verify_return_stmt(node, self.default_symbol_table, context_stack, self.filename)

    # ==================== Error Cases: Return Outside Function ====================

    def test_return_outside_function_empty_context(self) -> None:
        """Test return statement with empty context stack - should raise ValueError."""
        node: Dict[str, Any] = {
            "type": "return_stmt",
            "value": None,
            "line": 5,
            "column": 1,
        }
        context_stack: List[Dict[str, Any]] = []

        with self.assertRaises(ValueError) as ctx:
            _verify_return_stmt(node, self.default_symbol_table, context_stack, self.filename)

        self.assertIn("return statement outside of function", str(ctx.exception))
        self.assertIn("test.c:5:1", str(ctx.exception))

    def test_return_outside_function_loop_context(self) -> None:
        """Test return statement in loop context only - should raise ValueError."""
        node: Dict[str, Any] = {
            "type": "return_stmt",
            "value": None,
            "line": 8,
            "column": 3,
        }
        context_stack: List[Dict[str, Any]] = [
            {"type": "loop", "stmt_type": "for"}
        ]

        with self.assertRaises(ValueError) as ctx:
            _verify_return_stmt(node, self.default_symbol_table, context_stack, self.filename)

        self.assertIn("return statement outside of function", str(ctx.exception))

    def test_return_outside_function_nested_loop_context(self) -> None:
        """Test return in nested loop without function context - should raise ValueError."""
        node: Dict[str, Any] = {
            "type": "return_stmt",
            "value": None,
            "line": 12,
            "column": 5,
        }
        context_stack: List[Dict[str, Any]] = [
            {"type": "loop", "stmt_type": "while"},
            {"type": "loop", "stmt_type": "for"},
        ]

        with self.assertRaises(ValueError) as ctx:
            _verify_return_stmt(node, self.default_symbol_table, context_stack, self.filename)

        self.assertIn("return statement outside of function", str(ctx.exception))

    # ==================== Error Cases: Missing Return Value ====================

    def test_non_void_function_expects_return_but_none(self) -> None:
        """Test int function with no return value - should raise ValueError."""
        node: Dict[str, Any] = {
            "type": "return_stmt",
            "value": None,
            "line": 18,
            "column": 5,
        }
        context_stack: List[Dict[str, Any]] = [
            {"type": "function", "name": "get_int", "return_type": "int"}
        ]

        with self.assertRaises(ValueError) as ctx:
            _verify_return_stmt(node, self.default_symbol_table, context_stack, self.filename)

        self.assertIn("function expects return value of type 'int'", str(ctx.exception))
        self.assertIn("test.c:18:5", str(ctx.exception))

    def test_char_function_expects_return_but_none(self) -> None:
        """Test char function with no return value - should raise ValueError."""
        node: Dict[str, Any] = {
            "type": "return_stmt",
            "value": None,
            "line": 22,
            "column": 7,
        }
        context_stack: List[Dict[str, Any]] = [
            {"type": "function", "name": "get_char", "return_type": "char"}
        ]

        with self.assertRaises(ValueError) as ctx:
            _verify_return_stmt(node, self.default_symbol_table, context_stack, self.filename)

        self.assertIn("function expects return value of type 'char'", str(ctx.exception))

    # ==================== Error Cases: Type Mismatch ====================

    def test_int_function_returns_char_literal(self) -> None:
        """Test int function returning char literal - should raise ValueError."""
        node: Dict[str, Any] = {
            "type": "return_stmt",
            "value": {
                "type": "char_literal",
                "data_type": "char",
                "line": 30,
                "column": 12,
            },
            "line": 30,
            "column": 5,
        }
        context_stack: List[Dict[str, Any]] = [
            {"type": "function", "name": "get_int", "return_type": "int"}
        ]

        with self.assertRaises(ValueError) as ctx:
            _verify_return_stmt(node, self.default_symbol_table, context_stack, self.filename)

        self.assertIn("return type mismatch", str(ctx.exception))
        self.assertIn("expected 'int', got 'char'", str(ctx.exception))

    def test_char_function_returns_int_literal(self) -> None:
        """Test char function returning int literal - should raise ValueError."""
        node: Dict[str, Any] = {
            "type": "return_stmt",
            "value": {
                "type": "int_literal",
                "data_type": "int",
                "line": 35,
                "column": 10,
            },
            "line": 35,
            "column": 5,
        }
        context_stack: List[Dict[str, Any]] = [
            {"type": "function", "name": "get_char", "return_type": "char"}
        ]

        with self.assertRaises(ValueError) as ctx:
            _verify_return_stmt(node, self.default_symbol_table, context_stack, self.filename)

        self.assertIn("return type mismatch", str(ctx.exception))
        self.assertIn("expected 'char', got 'int'", str(ctx.exception))

    def test_int_function_returns_variable_of_char_type(self) -> None:
        """Test int function returning char variable - should raise ValueError."""
        symbol_table: Dict[str, Any] = {
            "variables": {
                "c": {"data_type": "char", "scope": 1},
            },
            "functions": {},
            "current_scope": 1,
        }
        node: Dict[str, Any] = {
            "type": "return_stmt",
            "value": {
                "type": "variable_ref",
                "name": "c",
                "line": 40,
                "column": 10,
            },
            "line": 40,
            "column": 5,
        }
        context_stack: List[Dict[str, Any]] = [
            {"type": "function", "name": "get_int", "return_type": "int"}
        ]

        with self.assertRaises(ValueError) as ctx:
            _verify_return_stmt(node, symbol_table, context_stack, self.filename)

        self.assertIn("return type mismatch", str(ctx.exception))
        self.assertIn("expected 'int', got 'char'", str(ctx.exception))

    # ==================== Error Cases: Unable to Determine Type ====================

    def test_unknown_node_type_without_data_type(self) -> None:
        """Test return with unknown node type and no data_type - should raise ValueError."""
        node: Dict[str, Any] = {
            "type": "return_stmt",
            "value": {
                "type": "unknown_type",
                "line": 45,
                "column": 10,
            },
            "line": 45,
            "column": 5,
        }
        context_stack: List[Dict[str, Any]] = [
            {"type": "function", "name": "foo", "return_type": "int"}
        ]

        with self.assertRaises(ValueError) as ctx:
            _verify_return_stmt(node, self.default_symbol_table, context_stack, self.filename)

        self.assertIn("unable to determine return value type", str(ctx.exception))

    def test_variable_ref_not_in_symbol_table(self) -> None:
        """Test return variable not in symbol table - should raise ValueError."""
        node: Dict[str, Any] = {
            "type": "return_stmt",
            "value": {
                "type": "variable_ref",
                "name": "undefined_var",
                "line": 50,
                "column": 10,
            },
            "line": 50,
            "column": 5,
        }
        context_stack: List[Dict[str, Any]] = [
            {"type": "function", "name": "foo", "return_type": "int"}
        ]

        with self.assertRaises(ValueError) as ctx:
            _verify_return_stmt(node, self.default_symbol_table, context_stack, self.filename)

        self.assertIn("unable to determine return value type", str(ctx.exception))

    def test_variable_ref_with_no_name(self) -> None:
        """Test variable_ref without name field - should raise ValueError."""
        node: Dict[str, Any] = {
            "type": "return_stmt",
            "value": {
                "type": "variable_ref",
                "line": 55,
                "column": 10,
            },
            "line": 55,
            "column": 5,
        }
        context_stack: List[Dict[str, Any]] = [
            {"type": "function", "name": "foo", "return_type": "int"}
        ]

        with self.assertRaises(ValueError) as ctx:
            _verify_return_stmt(node, self.default_symbol_table, context_stack, self.filename)

        self.assertIn("unable to determine return value type", str(ctx.exception))

    # ==================== Edge Cases ====================

    def test_nested_function_context_uses_top_frame(self) -> None:
        """Test that nested context uses top frame for return type check."""
        node: Dict[str, Any] = {
            "type": "return_stmt",
            "value": {
                "type": "int_literal",
                "data_type": "int",
                "line": 60,
                "column": 12,
            },
            "line": 60,
            "column": 5,
        }
        # Inner function is int, outer is void - should use inner (top)
        context_stack: List[Dict[str, Any]] = [
            {"type": "function", "name": "outer", "return_type": "void"},
            {"type": "function", "name": "inner", "return_type": "int"},
        ]

        # Should not raise - uses inner function's return type
        _verify_return_stmt(node, self.default_symbol_table, context_stack, self.filename)

    def test_missing_line_column_defaults_to_zero(self) -> None:
        """Test that missing line/column defaults to 0 in error message."""
        node: Dict[str, Any] = {
            "type": "return_stmt",
            "value": None,
        }
        context_stack: List[Dict[str, Any]] = []

        with self.assertRaises(ValueError) as ctx:
            _verify_return_stmt(node, self.default_symbol_table, context_stack, self.filename)

        self.assertIn("test.c:0:0", str(ctx.exception))

    def test_int_literal_inferred_type_without_data_type(self) -> None:
        """Test int_literal type inference when data_type is not set."""
        node: Dict[str, Any] = {
            "type": "return_stmt",
            "value": {
                "type": "int_literal",
                # No data_type field - should be inferred as "int"
                "line": 70,
                "column": 12,
            },
            "line": 70,
            "column": 5,
        }
        context_stack: List[Dict[str, Any]] = [
            {"type": "function", "name": "foo", "return_type": "int"}
        ]

        # Should not raise - infers int from int_literal type
        _verify_return_stmt(node, self.default_symbol_table, context_stack, self.filename)

    def test_char_literal_inferred_type_without_data_type(self) -> None:
        """Test char_literal type inference when data_type is not set."""
        node: Dict[str, Any] = {
            "type": "return_stmt",
            "value": {
                "type": "char_literal",
                # No data_type field - should be inferred as "char"
                "line": 75,
                "column": 10,
            },
            "line": 75,
            "column": 5,
        }
        context_stack: List[Dict[str, Any]] = [
            {"type": "function", "name": "foo", "return_type": "char"}
        ]

        # Should not raise - infers char from char_literal type
        _verify_return_stmt(node, self.default_symbol_table, context_stack, self.filename)

    def test_binary_op_inferred_type_without_data_type(self) -> None:
        """Test binary_op type inference when data_type is not set."""
        node: Dict[str, Any] = {
            "type": "return_stmt",
            "value": {
                "type": "binary_op",
                # No data_type field - should be inferred as "int"
                "line": 80,
                "column": 12,
            },
            "line": 80,
            "column": 5,
        }
        context_stack: List[Dict[str, Any]] = [
            {"type": "function", "name": "foo", "return_type": "int"}
        ]

        # Should not raise - infers int from binary_op type
        _verify_return_stmt(node, self.default_symbol_table, context_stack, self.filename)


if __name__ == "__main__":
    unittest.main()

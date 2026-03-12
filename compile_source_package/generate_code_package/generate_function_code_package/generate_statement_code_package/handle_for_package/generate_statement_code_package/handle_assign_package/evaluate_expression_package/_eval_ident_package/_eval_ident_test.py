#!/usr/bin/env python3
"""Unit tests for _eval_ident function."""

import unittest
from typing import Dict, Any

from ._eval_ident_src import _eval_ident


class TestEvalIdent(unittest.TestCase):
    """Test cases for _eval_ident function."""

    def test_valid_ident_expression(self) -> None:
        """Test happy path: valid IDENT expression with defined variable."""
        expr: Dict[str, Any] = {"type": "IDENT", "name": "x"}
        var_offsets: Dict[str, int] = {"x": 8, "y": 16}
        
        code, temp_count, reg = _eval_ident(expr, var_offsets)
        
        self.assertEqual(code, "    LDR R0, [SP, #8]")
        self.assertEqual(temp_count, 0)
        self.assertEqual(reg, "R0")

    def test_valid_ident_with_different_offset(self) -> None:
        """Test IDENT expression with different stack offset."""
        expr: Dict[str, Any] = {"type": "IDENT", "name": "counter"}
        var_offsets: Dict[str, int] = {"counter": 24}
        
        code, temp_count, reg = _eval_ident(expr, var_offsets)
        
        self.assertEqual(code, "    LDR R0, [SP, #24]")
        self.assertEqual(temp_count, 0)
        self.assertEqual(reg, "R0")

    def test_missing_name_field_raises_value_error(self) -> None:
        """Test that missing 'name' field raises ValueError."""
        expr: Dict[str, Any] = {"type": "IDENT"}
        var_offsets: Dict[str, int] = {"x": 8}
        
        with self.assertRaises(ValueError) as context:
            _eval_ident(expr, var_offsets)
        
        self.assertIn("Missing required field 'name'", str(context.exception))

    def test_empty_expr_raises_value_error(self) -> None:
        """Test that empty expr dict raises ValueError."""
        expr: Dict[str, Any] = {}
        var_offsets: Dict[str, int] = {"x": 8}
        
        with self.assertRaises(ValueError) as context:
            _eval_ident(expr, var_offsets)
        
        self.assertIn("Missing required field 'name'", str(context.exception))

    def test_undefined_variable_raises_value_error(self) -> None:
        """Test that undefined variable raises ValueError."""
        expr: Dict[str, Any] = {"type": "IDENT", "name": "undefined_var"}
        var_offsets: Dict[str, int] = {"x": 8, "y": 16}
        
        with self.assertRaises(ValueError) as context:
            _eval_ident(expr, var_offsets)
        
        self.assertIn("Undefined variable: undefined_var", str(context.exception))

    def test_empty_var_offsets_raises_value_error(self) -> None:
        """Test that empty var_offsets with any variable raises ValueError."""
        expr: Dict[str, Any] = {"type": "IDENT", "name": "any_var"}
        var_offsets: Dict[str, int] = {}
        
        with self.assertRaises(ValueError) as context:
            _eval_ident(expr, var_offsets)
        
        self.assertIn("Undefined variable: any_var", str(context.exception))

    def test_zero_offset(self) -> None:
        """Test IDENT expression with zero stack offset."""
        expr: Dict[str, Any] = {"type": "IDENT", "name": "zero_var"}
        var_offsets: Dict[str, int] = {"zero_var": 0}
        
        code, temp_count, reg = _eval_ident(expr, var_offsets)
        
        self.assertEqual(code, "    LDR R0, [SP, #0]")
        self.assertEqual(temp_count, 0)
        self.assertEqual(reg, "R0")

    def test_large_offset(self) -> None:
        """Test IDENT expression with large stack offset."""
        expr: Dict[str, Any] = {"type": "IDENT", "name": "large_var"}
        var_offsets: Dict[str, int] = {"large_var": 1024}
        
        code, temp_count, reg = _eval_ident(expr, var_offsets)
        
        self.assertEqual(code, "    LDR R0, [SP, #1024]")
        self.assertEqual(temp_count, 0)
        self.assertEqual(reg, "R0")

    def test_variable_name_with_underscore(self) -> None:
        """Test IDENT expression with variable name containing underscore."""
        expr: Dict[str, Any] = {"type": "IDENT", "name": "my_variable"}
        var_offsets: Dict[str, int] = {"my_variable": 32}
        
        code, temp_count, reg = _eval_ident(expr, var_offsets)
        
        self.assertEqual(code, "    LDR R0, [SP, #32]")
        self.assertEqual(temp_count, 0)
        self.assertEqual(reg, "R0")

    def test_extra_fields_in_expr_ignored(self) -> None:
        """Test that extra fields in expr are ignored."""
        expr: Dict[str, Any] = {"type": "IDENT", "name": "x", "extra": "ignored", "line": 42}
        var_offsets: Dict[str, int] = {"x": 8}
        
        code, temp_count, reg = _eval_ident(expr, var_offsets)
        
        self.assertEqual(code, "    LDR R0, [SP, #8]")
        self.assertEqual(temp_count, 0)
        self.assertEqual(reg, "R0")


if __name__ == "__main__":
    unittest.main()

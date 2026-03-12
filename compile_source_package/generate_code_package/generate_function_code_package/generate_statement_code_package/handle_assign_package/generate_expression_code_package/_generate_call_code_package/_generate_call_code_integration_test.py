#!/usr/bin/env python3
"""Integration tests for _generate_call_code function.

Tests verify behavior through real module boundaries with generate_expression_code,
only mocking external infrastructure dependencies.
"""

import pytest
from _generate_call_code_package._generate_call_code_src import _generate_call_code


class TestGenerateCallCodeIntegration:
    """Integration tests for _generate_call_code through real call chain."""

    def test_call_no_args_integration(self):
        """Integration test: CALL with no arguments."""
        expr = {"type": "CALL", "name": "getchar", "args": []}
        var_offsets = {}
        
        result = _generate_call_code(expr, "main", var_offsets)
        
        assert result == "bl getchar"

    def test_call_single_const_arg_integration(self):
        """Integration test: CALL with single CONST argument."""
        expr = {
            "type": "CALL",
            "name": "putchar",
            "args": [{"type": "CONST", "value": 65}]
        }
        var_offsets = {}
        
        result = _generate_call_code(expr, "main", var_offsets)
        
        lines = result.strip().split("\n")
        assert len(lines) == 2
        assert "mov x0, #65" in lines[0]
        assert "bl putchar" in lines[1]

    def test_call_two_args_integration(self):
        """Integration test: CALL with two CONST arguments."""
        expr = {
            "type": "CALL",
            "name": "add",
            "args": [
                {"type": "CONST", "value": 1},
                {"type": "CONST", "value": 2}
            ]
        }
        var_offsets = {}
        
        result = _generate_call_code(expr, "main", var_offsets)
        
        lines = result.strip().split("\n")
        assert len(lines) == 3
        assert "mov x0, #1" in lines[0]
        assert "mov x1, x0" in lines[1]
        assert "bl add" in lines[2]

    def test_call_three_args_integration(self):
        """Integration test: CALL with three CONST arguments."""
        expr = {
            "type": "CALL",
            "name": "sum3",
            "args": [
                {"type": "CONST", "value": 1},
                {"type": "CONST", "value": 2},
                {"type": "CONST", "value": 3}
            ]
        }
        var_offsets = {}
        
        result = _generate_call_code(expr, "main", var_offsets)
        
        lines = result.strip().split("\n")
        assert len(lines) == 5
        assert "mov x0, #1" in lines[0]
        assert "mov x1, x0" in lines[1]
        assert "mov x0, #2" in lines[2]
        assert "mov x2, x0" in lines[3]
        assert "bl sum3" in lines[4]

    def test_call_eight_args_max_integration(self):
        """Integration test: CALL with maximum 8 CONST arguments."""
        expr = {
            "type": "CALL",
            "name": "func8",
            "args": [{"type": "CONST", "value": i} for i in range(8)]
        }
        var_offsets = {}
        
        result = _generate_call_code(expr, "main", var_offsets)
        
        lines = result.strip().split("\n")
        assert len(lines) == 15
        assert "bl func8" in lines[-1]

    def test_call_nine_args_raises_error_integration(self):
        """Integration test: CALL with 9 arguments raises ValueError."""
        expr = {
            "type": "CALL",
            "name": "too_many",
            "args": [{"type": "CONST", "value": i} for i in range(9)]
        }
        var_offsets = {}
        
        with pytest.raises(ValueError, match="Too many arguments"):
            _generate_call_code(expr, "main", var_offsets)

    def test_call_with_var_arg_integration(self):
        """Integration test: CALL with VAR argument (reads from stack)."""
        expr = {
            "type": "CALL",
            "name": "print_val",
            "args": [{"type": "VAR", "name": "x"}]
        }
        var_offsets = {"x": -16}
        
        result = _generate_call_code(expr, "main", var_offsets)
        
        lines = result.strip().split("\n")
        assert len(lines) == 3
        assert "ldr x0, [sp, #-16]" in lines[0]
        assert "bl print_val" in lines[1]

    def test_call_with_binop_arg_integration(self):
        """Integration test: CALL with BINOP argument."""
        expr = {
            "type": "CALL",
            "name": "print_sum",
            "args": [{
                "type": "BINOP",
                "op": "+",
                "left": {"type": "CONST", "value": 10},
                "right": {"type": "CONST", "value": 20}
            }]
        }
        var_offsets = {}
        
        result = _generate_call_code(expr, "main", var_offsets)
        
        lines = result.strip().split("\n")
        assert "mov x0, #10" in lines[0]
        assert "mov x1, #20" in lines[1]
        assert "add x0, x0, x1" in lines[2]
        assert "bl print_sum" in lines[3]

    def test_call_missing_name_defaults_integration(self):
        """Integration test: CALL with missing name field defaults to empty."""
        expr = {"type": "CALL", "args": []}
        var_offsets = {}
        
        result = _generate_call_code(expr, "main", var_offsets)
        
        assert result == "bl "

    def test_call_missing_args_defaults_integration(self):
        """Integration test: CALL with missing args field defaults to empty list."""
        expr = {"type": "CALL", "name": "test_func"}
        var_offsets = {}
        
        result = _generate_call_code(expr, "main", var_offsets)
        
        assert result == "bl test_func"

    def test_call_nested_call_arg_integration(self):
        """Integration test: CALL with nested CALL as argument."""
        expr = {
            "type": "CALL",
            "name": "outer",
            "args": [{
                "type": "CALL",
                "name": "inner",
                "args": []
            }]
        }
        var_offsets = {}
        
        result = _generate_call_code(expr, "main", var_offsets)
        
        lines = result.strip().split("\n")
        assert "bl inner" in lines[0]
        assert "mov x0, x0" not in result
        assert "bl outer" in lines[-1]

    def test_call_mixed_arg_types_integration(self):
        """Integration test: CALL with mixed CONST, VAR, and BINOP arguments."""
        expr = {
            "type": "CALL",
            "name": "mixed",
            "args": [
                {"type": "CONST", "value": 42},
                {"type": "VAR", "name": "y"},
                {
                    "type": "BINOP",
                    "op": "*",
                    "left": {"type": "CONST", "value": 2},
                    "right": {"type": "CONST", "value": 3}
                }
            ]
        }
        var_offsets = {"y": -24}
        
        result = _generate_call_code(expr, "main", var_offsets)
        
        lines = result.strip().split("\n")
        assert len(lines) == 8
        assert "mov x0, #42" in lines[0]
        assert "ldr x0, [sp, #-24]" in lines[2]
        assert "mov x1, x0" in lines[3]
        assert "bl mixed" in lines[-1]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

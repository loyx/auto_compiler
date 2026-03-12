# -*- coding: utf-8 -*-
"""Unit tests for handle_return function."""

from typing import Dict, Any
import unittest
from .handle_return_src import handle_return, _evaluate_expression


class TestHandleReturn(unittest.TestCase):
    """Test cases for handle_return function."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.func_name = "test_func"
        self.label_counter: Dict[str, int] = {"for_cond": 0, "for_end": 0, "for_update": 0}
        self.var_offsets: Dict[str, int] = {"x": 8, "y": 12, "result": 16}
        self.next_offset = 20

    def test_return_void_none_value(self) -> None:
        """Test return statement with None value (void return)."""
        stmt: Dict[str, Any] = {"type": "RETURN", "value": None}
        code, offset = handle_return(stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset)
        
        self.assertEqual(offset, self.next_offset)
        self.assertEqual(code, "    B test_func_epilogue")

    def test_return_void_empty_dict_value(self) -> None:
        """Test return statement with empty dict value (void return)."""
        stmt: Dict[str, Any] = {"type": "RETURN", "value": {}}
        code, offset = handle_return(stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset)
        
        self.assertEqual(offset, self.next_offset)
        self.assertEqual(code, "    B test_func_epilogue")

    def test_return_const_int(self) -> None:
        """Test return statement with CONST_INT value."""
        stmt: Dict[str, Any] = {
            "type": "RETURN",
            "value": {"type": "CONST_INT", "value": 42}
        }
        code, offset = handle_return(stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset)
        
        self.assertEqual(offset, self.next_offset)
        expected_code = "    MOV R0, #42\n    B test_func_epilogue"
        self.assertEqual(code, expected_code)

    def test_return_const_int_zero(self) -> None:
        """Test return statement with CONST_INT value of zero."""
        stmt: Dict[str, Any] = {
            "type": "RETURN",
            "value": {"type": "CONST_INT", "value": 0}
        }
        code, offset = handle_return(stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset)
        
        self.assertEqual(offset, self.next_offset)
        expected_code = "    MOV R0, #0\n    B test_func_epilogue"
        self.assertEqual(code, expected_code)

    def test_return_const_float(self) -> None:
        """Test return statement with CONST_FLOAT value."""
        stmt: Dict[str, Any] = {
            "type": "RETURN",
            "value": {"type": "CONST_FLOAT", "value": 3.14}
        }
        code, offset = handle_return(stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset)
        
        self.assertEqual(offset, self.next_offset)
        expected_code = "    MOV R0, #3\n    B test_func_epilogue"
        self.assertEqual(code, expected_code)

    def test_return_var_ref_existing(self) -> None:
        """Test return statement with VAR_REF to existing variable."""
        stmt: Dict[str, Any] = {
            "type": "RETURN",
            "value": {"type": "VAR_REF", "var_name": "x"}
        }
        code, offset = handle_return(stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset)
        
        self.assertEqual(offset, self.next_offset)
        expected_code = "    LDR R0, [FP, #8]\n    B test_func_epilogue"
        self.assertEqual(code, expected_code)

    def test_return_var_ref_non_existing(self) -> None:
        """Test return statement with VAR_REF to non-existing variable."""
        stmt: Dict[str, Any] = {
            "type": "RETURN",
            "value": {"type": "VAR_REF", "var_name": "unknown_var"}
        }
        code, offset = handle_return(stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset)
        
        self.assertEqual(offset, self.next_offset)
        expected_code = "    MOV R0, #0\n    B test_func_epilogue"
        self.assertEqual(code, expected_code)

    def test_return_add_operation(self) -> None:
        """Test return statement with ADD binary operation."""
        stmt: Dict[str, Any] = {
            "type": "RETURN",
            "value": {
                "type": "ADD",
                "left": {"type": "CONST_INT", "value": 5},
                "right": {"type": "CONST_INT", "value": 3}
            }
        }
        code, offset = handle_return(stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset)
        
        self.assertEqual(offset, self.next_offset)
        expected_code = "    MOV R0, #5\n    MOV R1, #3\n    ADD R0, R0, R1\n    B test_func_epilogue"
        self.assertEqual(code, expected_code)

    def test_return_sub_operation(self) -> None:
        """Test return statement with SUB binary operation."""
        stmt: Dict[str, Any] = {
            "type": "RETURN",
            "value": {
                "type": "SUB",
                "left": {"type": "CONST_INT", "value": 10},
                "right": {"type": "CONST_INT", "value": 4}
            }
        }
        code, offset = handle_return(stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset)
        
        self.assertEqual(offset, self.next_offset)
        expected_code = "    MOV R0, #10\n    MOV R1, #4\n    SUB R0, R0, R1\n    B test_func_epilogue"
        self.assertEqual(code, expected_code)

    def test_return_mul_operation(self) -> None:
        """Test return statement with MUL binary operation."""
        stmt: Dict[str, Any] = {
            "type": "RETURN",
            "value": {
                "type": "MUL",
                "left": {"type": "CONST_INT", "value": 6},
                "right": {"type": "CONST_INT", "value": 7}
            }
        }
        code, offset = handle_return(stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset)
        
        self.assertEqual(offset, self.next_offset)
        expected_code = "    MOV R0, #6\n    MOV R1, #7\n    MUL R0, R0, R1\n    B test_func_epilogue"
        self.assertEqual(code, expected_code)

    def test_return_div_operation(self) -> None:
        """Test return statement with DIV binary operation."""
        stmt: Dict[str, Any] = {
            "type": "RETURN",
            "value": {
                "type": "DIV",
                "left": {"type": "CONST_INT", "value": 20},
                "right": {"type": "CONST_INT", "value": 4}
            }
        }
        code, offset = handle_return(stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset)
        
        self.assertEqual(offset, self.next_offset)
        expected_code = "    MOV R0, #20\n    MOV R1, #4\n    SDIV R0, R0, R1\n    B test_func_epilogue"
        self.assertEqual(code, expected_code)

    def test_return_nested_binary_operation(self) -> None:
        """Test return statement with nested binary operation."""
        stmt: Dict[str, Any] = {
            "type": "RETURN",
            "value": {
                "type": "ADD",
                "left": {
                    "type": "MUL",
                    "left": {"type": "CONST_INT", "value": 2},
                    "right": {"type": "CONST_INT", "value": 3}
                },
                "right": {"type": "CONST_INT", "value": 4}
            }
        }
        code, offset = handle_return(stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset)
        
        self.assertEqual(offset, self.next_offset)
        # (2 * 3) + 4
        expected_code = "    MOV R0, #2\n    MOV R1, #3\n    MUL R0, R0, R1\n    MOV R1, #4\n    ADD R0, R0, R1\n    B test_func_epilogue"
        self.assertEqual(code, expected_code)

    def test_return_var_ref_in_binary_op(self) -> None:
        """Test return statement with VAR_REF in binary operation."""
        stmt: Dict[str, Any] = {
            "type": "RETURN",
            "value": {
                "type": "ADD",
                "left": {"type": "VAR_REF", "var_name": "x"},
                "right": {"type": "VAR_REF", "var_name": "y"}
            }
        }
        code, offset = handle_return(stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset)
        
        self.assertEqual(offset, self.next_offset)
        expected_code = "    LDR R0, [FP, #8]\n    LDR R1, [FP, #12]\n    ADD R0, R0, R1\n    B test_func_epilogue"
        self.assertEqual(code, expected_code)

    def test_return_unknown_expression_type(self) -> None:
        """Test return statement with unknown expression type."""
        stmt: Dict[str, Any] = {
            "type": "RETURN",
            "value": {"type": "UNKNOWN_TYPE", "data": "something"}
        }
        code, offset = handle_return(stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset)
        
        self.assertEqual(offset, self.next_offset)
        expected_code = "    MOV R0, #0\n    B test_func_epilogue"
        self.assertEqual(code, expected_code)

    def test_return_different_func_name(self) -> None:
        """Test return statement with different function name."""
        stmt: Dict[str, Any] = {
            "type": "RETURN",
            "value": {"type": "CONST_INT", "value": 100}
        }
        code, offset = handle_return(stmt, "another_func", self.label_counter, self.var_offsets, self.next_offset)
        
        self.assertEqual(offset, self.next_offset)
        expected_code = "    MOV R0, #100\n    B another_func_epilogue"
        self.assertEqual(code, expected_code)

    def test_return_offset_unchanged(self) -> None:
        """Test that next_offset is returned unchanged."""
        stmt: Dict[str, Any] = {
            "type": "RETURN",
            "value": {"type": "CONST_INT", "value": 1}
        }
        _, offset = handle_return(stmt, self.func_name, self.label_counter, self.var_offsets, 999)
        self.assertEqual(offset, 999)

    def test_return_label_counter_unchanged(self) -> None:
        """Test that label_counter is not modified."""
        stmt: Dict[str, Any] = {
            "type": "RETURN",
            "value": {"type": "CONST_INT", "value": 1}
        }
        original_counter = self.label_counter.copy()
        handle_return(stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset)
        self.assertEqual(self.label_counter, original_counter)

    def test_return_var_offsets_unchanged(self) -> None:
        """Test that var_offsets is not modified."""
        stmt: Dict[str, Any] = {
            "type": "RETURN",
            "value": {"type": "CONST_INT", "value": 1}
        }
        original_offsets = self.var_offsets.copy()
        handle_return(stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset)
        self.assertEqual(self.var_offsets, original_offsets)


class TestEvaluateExpression(unittest.TestCase):
    """Test cases for _evaluate_expression helper function."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.var_offsets: Dict[str, int] = {"a": 4, "b": 8, "c": 12}
        self.func_name = "test_func"

    def test_evaluate_const_int(self) -> None:
        """Test evaluating CONST_INT expression."""
        expr = {"type": "CONST_INT", "value": 123}
        code = _evaluate_expression(expr, self.var_offsets, self.func_name)
        self.assertEqual(code, "    MOV R0, #123")

    def test_evaluate_const_int_negative(self) -> None:
        """Test evaluating negative CONST_INT expression."""
        expr = {"type": "CONST_INT", "value": -5}
        code = _evaluate_expression(expr, self.var_offsets, self.func_name)
        self.assertEqual(code, "    MOV R0, #-5")

    def test_evaluate_const_float(self) -> None:
        """Test evaluating CONST_FLOAT expression."""
        expr = {"type": "CONST_FLOAT", "value": 2.71}
        code = _evaluate_expression(expr, self.var_offsets, self.func_name)
        self.assertEqual(code, "    MOV R0, #2")

    def test_evaluate_const_float_zero(self) -> None:
        """Test evaluating CONST_FLOAT with zero value."""
        expr = {"type": "CONST_FLOAT", "value": 0.0}
        code = _evaluate_expression(expr, self.var_offsets, self.func_name)
        self.assertEqual(code, "    MOV R0, #0")

    def test_evaluate_var_ref_existing(self) -> None:
        """Test evaluating VAR_REF to existing variable."""
        expr = {"type": "VAR_REF", "var_name": "b"}
        code = _evaluate_expression(expr, self.var_offsets, self.func_name)
        self.assertEqual(code, "    LDR R0, [FP, #8]")

    def test_evaluate_var_ref_non_existing(self) -> None:
        """Test evaluating VAR_REF to non-existing variable."""
        expr = {"type": "VAR_REF", "var_name": "not_found"}
        code = _evaluate_expression(expr, self.var_offsets, self.func_name)
        self.assertEqual(code, "    MOV R0, #0")

    def test_evaluate_add(self) -> None:
        """Test evaluating ADD expression."""
        expr = {
            "type": "ADD",
            "left": {"type": "CONST_INT", "value": 10},
            "right": {"type": "CONST_INT", "value": 5}
        }
        code = _evaluate_expression(expr, self.var_offsets, self.func_name)
        expected = "    MOV R0, #10\n    MOV R1, #5\n    ADD R0, R0, R1"
        self.assertEqual(code, expected)

    def test_evaluate_sub(self) -> None:
        """Test evaluating SUB expression."""
        expr = {
            "type": "SUB",
            "left": {"type": "CONST_INT", "value": 15},
            "right": {"type": "CONST_INT", "value": 7}
        }
        code = _evaluate_expression(expr, self.var_offsets, self.func_name)
        expected = "    MOV R0, #15\n    MOV R1, #7\n    SUB R0, R0, R1"
        self.assertEqual(code, expected)

    def test_evaluate_mul(self) -> None:
        """Test evaluating MUL expression."""
        expr = {
            "type": "MUL",
            "left": {"type": "CONST_INT", "value": 3},
            "right": {"type": "CONST_INT", "value": 4}
        }
        code = _evaluate_expression(expr, self.var_offsets, self.func_name)
        expected = "    MOV R0, #3\n    MOV R1, #4\n    MUL R0, R0, R1"
        self.assertEqual(code, expected)

    def test_evaluate_div(self) -> None:
        """Test evaluating DIV expression."""
        expr = {
            "type": "DIV",
            "left": {"type": "CONST_INT", "value": 24},
            "right": {"type": "CONST_INT", "value": 6}
        }
        code = _evaluate_expression(expr, self.var_offsets, self.func_name)
        expected = "    MOV R0, #24\n    MOV R1, #6\n    SDIV R0, R0, R1"
        self.assertEqual(code, expected)

    def test_evaluate_unknown_type(self) -> None:
        """Test evaluating unknown expression type."""
        expr = {"type": "UNKNOWN", "data": "test"}
        code = _evaluate_expression(expr, self.var_offsets, self.func_name)
        self.assertEqual(code, "    MOV R0, #0")

    def test_evaluate_empty_dict(self) -> None:
        """Test evaluating empty dict expression."""
        expr: Dict[str, Any] = {}
        code = _evaluate_expression(expr, self.var_offsets, self.func_name)
        self.assertEqual(code, "    MOV R0, #0")

    def test_evaluate_var_ref_in_binary_op(self) -> None:
        """Test evaluating binary op with VAR_REF operands."""
        expr = {
            "type": "ADD",
            "left": {"type": "VAR_REF", "var_name": "a"},
            "right": {"type": "VAR_REF", "var_name": "c"}
        }
        code = _evaluate_expression(expr, self.var_offsets, self.func_name)
        expected = "    LDR R0, [FP, #4]\n    LDR R1, [FP, #12]\n    ADD R0, R0, R1"
        self.assertEqual(code, expected)


if __name__ == "__main__":
    unittest.main()

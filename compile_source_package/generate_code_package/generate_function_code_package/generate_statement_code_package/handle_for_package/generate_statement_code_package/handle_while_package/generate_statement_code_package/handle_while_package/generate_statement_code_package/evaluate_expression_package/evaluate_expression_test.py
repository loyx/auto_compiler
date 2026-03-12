# -*- coding: utf-8 -*-
"""Unit tests for evaluate_expression function."""

from unittest.mock import patch
import pytest

from .evaluate_expression_src import evaluate_expression


class TestEvaluateExpressionConst:
    """Tests for CONST expression type."""

    def test_const_integer(self):
        """Test CONST with integer value."""
        expr = {"type": "CONST", "value": 42}
        label_counter = {}
        var_offsets = {}
        next_offset = 0

        code, offset = evaluate_expression(expr, "main", label_counter, var_offsets, next_offset)

        assert code == "ldr r0, =42\n"
        assert offset == 0

    def test_const_negative(self):
        """Test CONST with negative value."""
        expr = {"type": "CONST", "value": -10}
        label_counter = {}
        var_offsets = {}
        next_offset = 0

        code, offset = evaluate_expression(expr, "main", label_counter, var_offsets, next_offset)

        assert code == "ldr r0, =-10\n"
        assert offset == 0

    def test_const_zero(self):
        """Test CONST with zero value."""
        expr = {"type": "CONST", "value": 0}
        label_counter = {}
        var_offsets = {}
        next_offset = 0

        code, offset = evaluate_expression(expr, "main", label_counter, var_offsets, next_offset)

        assert code == "ldr r0, =0\n"
        assert offset == 0


class TestEvaluateExpressionVar:
    """Tests for VAR expression type."""

    def test_var_simple(self):
        """Test VAR with simple variable."""
        expr = {"type": "VAR", "var_name": "x"}
        label_counter = {}
        var_offsets = {"x": 8}
        next_offset = 12

        code, offset = evaluate_expression(expr, "main", label_counter, var_offsets, next_offset)

        assert code == "ldr r0, [sp, #8]\n"
        assert offset == 12

    def test_var_offset_zero(self):
        """Test VAR with zero offset."""
        expr = {"type": "VAR", "var_name": "y"}
        label_counter = {}
        var_offsets = {"y": 0}
        next_offset = 4

        code, offset = evaluate_expression(expr, "main", label_counter, var_offsets, next_offset)

        assert code == "ldr r0, [sp, #0]\n"
        assert offset == 4


class TestEvaluateExpressionBinop:
    """Tests for BINOP expression type."""

    @patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.evaluate_expression_package.evaluate_expression_src.generate_binop")
    def test_binop_addition(self, mock_generate_binop):
        """Test BINOP with addition operator."""
        mock_generate_binop.return_value = "add r0, r1, r0\n"

        expr = {
            "type": "BINOP",
            "op": "+",
            "left": {"type": "CONST", "value": 5},
            "right": {"type": "CONST", "value": 3}
        }
        label_counter = {}
        var_offsets = {}
        next_offset = 0

        code, offset = evaluate_expression(expr, "main", label_counter, var_offsets, next_offset)

        expected = "ldr r0, =5\n"
        expected += "push {r0}\n"
        expected += "ldr r0, =3\n"
        expected += "pop {r1}\n"
        expected += "add r0, r1, r0\n"

        assert code == expected
        assert offset == 0
        mock_generate_binop.assert_called_once_with("+", label_counter)

    @patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.evaluate_expression_package.evaluate_expression_src.generate_binop")
    def test_binop_nested(self, mock_generate_binop):
        """Test BINOP with nested expressions."""
        mock_generate_binop.return_value = "mul r0, r1, r0\n"

        expr = {
            "type": "BINOP",
            "op": "*",
            "left": {
                "type": "BINOP",
                "op": "+",
                "left": {"type": "CONST", "value": 2},
                "right": {"type": "CONST", "value": 3}
            },
            "right": {"type": "CONST", "value": 4}
        }
        label_counter = {}
        var_offsets = {}
        next_offset = 0

        code, offset = evaluate_expression(expr, "main", label_counter, var_offsets, next_offset)

        assert "ldr r0, =2\n" in code
        assert "ldr r0, =3\n" in code
        assert "ldr r0, =4\n" in code
        assert code.count("push {r0}\n") == 2
        assert code.count("pop {r1}\n") == 2
        assert offset == 0
        assert mock_generate_binop.call_count == 2

    @patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.evaluate_expression_package.evaluate_expression_src.generate_binop")
    def test_binop_with_vars(self, mock_generate_binop):
        """Test BINOP with variable operands."""
        mock_generate_binop.return_value = "sub r0, r1, r0\n"

        expr = {
            "type": "BINOP",
            "op": "-",
            "left": {"type": "VAR", "var_name": "a"},
            "right": {"type": "VAR", "var_name": "b"}
        }
        label_counter = {}
        var_offsets = {"a": 8, "b": 12}
        next_offset = 16

        code, offset = evaluate_expression(expr, "main", label_counter, var_offsets, next_offset)

        expected = "ldr r0, [sp, #8]\n"
        expected += "push {r0}\n"
        expected += "ldr r0, [sp, #12]\n"
        expected += "pop {r1}\n"
        expected += "sub r0, r1, r0\n"

        assert code == expected
        assert offset == 16


class TestEvaluateExpressionUnop:
    """Tests for UNOP expression type."""

    @patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.evaluate_expression_package.evaluate_expression_src.generate_unop")
    def test_unop_negation(self, mock_generate_unop):
        """Test UNOP with negation operator."""
        mock_generate_unop.return_value = "neg r0, r0\n"

        expr = {
            "type": "UNOP",
            "op": "-",
            "operand": {"type": "CONST", "value": 10}
        }
        label_counter = {}
        var_offsets = {}
        next_offset = 0

        code, offset = evaluate_expression(expr, "main", label_counter, var_offsets, next_offset)

        expected = "ldr r0, =10\n"
        expected += "neg r0, r0\n"

        assert code == expected
        assert offset == 0
        mock_generate_unop.assert_called_once_with("-")

    @patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.evaluate_expression_package.evaluate_expression_src.generate_unop")
    def test_unop_not(self, mock_generate_unop):
        """Test UNOP with not operator."""
        mock_generate_unop.return_value = "not_op_code\n"

        expr = {
            "type": "UNOP",
            "op": "not",
            "operand": {"type": "VAR", "var_name": "flag"}
        }
        label_counter = {}
        var_offsets = {"flag": 0}
        next_offset = 4

        code, offset = evaluate_expression(expr, "main", label_counter, var_offsets, next_offset)

        assert "ldr r0, [sp, #0]\n" in code
        assert offset == 4
        mock_generate_unop.assert_called_once_with("not")

    @patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.evaluate_expression_package.evaluate_expression_src.generate_unop")
    def test_unop_nested(self, mock_generate_unop):
        """Test UNOP with nested operand."""
        mock_generate_unop.return_value = "neg r0, r0\n"

        expr = {
            "type": "UNOP",
            "op": "-",
            "operand": {
                "type": "BINOP",
                "op": "+",
                "left": {"type": "CONST", "value": 1},
                "right": {"type": "CONST", "value": 2}
            }
        }
        label_counter = {}
        var_offsets = {}
        next_offset = 0

        code, offset = evaluate_expression(expr, "main", label_counter, var_offsets, next_offset)

        assert "ldr r0, =1\n" in code
        assert "ldr r0, =2\n" in code
        assert offset == 0


class TestEvaluateExpressionCall:
    """Tests for CALL expression type."""

    def test_call_no_args(self):
        """Test CALL with no arguments."""
        expr = {
            "type": "CALL",
            "func_name": "get_value",
            "args": []
        }
        label_counter = {}
        var_offsets = {}
        next_offset = 0

        code, offset = evaluate_expression(expr, "main", label_counter, var_offsets, next_offset)

        expected = "bl get_value\n"
        assert code == expected
        assert offset == 0

    def test_call_single_arg(self):
        """Test CALL with single argument."""
        expr = {
            "type": "CALL",
            "func_name": "print",
            "args": [{"type": "CONST", "value": 42}]
        }
        label_counter = {}
        var_offsets = {}
        next_offset = 0

        code, offset = evaluate_expression(expr, "main", label_counter, var_offsets, next_offset)

        expected = "ldr r0, =42\n"
        expected += "push {r0}\n"
        expected += "bl print\n"
        expected += "add sp, sp, #4\n"

        assert code == expected
        assert offset == 0

    def test_call_multiple_args(self):
        """Test CALL with multiple arguments (reverse order evaluation)."""
        expr = {
            "type": "CALL",
            "func_name": "add",
            "args": [
                {"type": "CONST", "value": 1},
                {"type": "CONST", "value": 2},
                {"type": "CONST", "value": 3}
            ]
        }
        label_counter = {}
        var_offsets = {}
        next_offset = 0

        code, offset = evaluate_expression(expr, "main", label_counter, var_offsets, next_offset)

        expected = "ldr r0, =3\n"
        expected += "push {r0}\n"
        expected += "ldr r0, =2\n"
        expected += "push {r0}\n"
        expected += "ldr r0, =1\n"
        expected += "push {r0}\n"
        expected += "bl add\n"
        expected += "add sp, sp, #12\n"

        assert code == expected
        assert offset == 0

    def test_call_with_var_args(self):
        """Test CALL with variable arguments."""
        expr = {
            "type": "CALL",
            "func_name": "compute",
            "args": [
                {"type": "VAR", "var_name": "x"},
                {"type": "VAR", "var_name": "y"}
            ]
        }
        label_counter = {}
        var_offsets = {"x": 8, "y": 12}
        next_offset = 16

        code, offset = evaluate_expression(expr, "main", label_counter, var_offsets, next_offset)

        assert "ldr r0, [sp, #12]\n" in code
        assert "ldr r0, [sp, #8]\n" in code
        assert "bl compute\n" in code
        assert "add sp, sp, #8\n" in code
        assert offset == 16

    @patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.evaluate_expression_package.evaluate_expression_src.evaluate_expression")
    def test_call_nested_expression_args(self, mock_eval):
        """Test CALL with nested expression arguments."""
        mock_eval.side_effect = [
            ("ldr r0, =5\n", 0),
            ("ldr r0, =10\n", 0),
        ]

        expr = {
            "type": "CALL",
            "func_name": "func",
            "args": [
                {"type": "BINOP", "op": "+", "left": {"type": "CONST", "value": 2}, "right": {"type": "CONST", "value": 3}},
                {"type": "CONST", "value": 10}
            ]
        }
        label_counter = {}
        var_offsets = {}
        next_offset = 0

        code, offset = evaluate_expression(expr, "main", label_counter, var_offsets, next_offset)

        assert "bl func\n" in code
        assert "add sp, sp, #8\n" in code


class TestEvaluateExpressionUnknown:
    """Tests for unknown expression types."""

    def test_unknown_type_raises(self):
        """Test that unknown expression type raises ValueError."""
        expr = {"type": "UNKNOWN_TYPE"}
        label_counter = {}
        var_offsets = {}
        next_offset = 0

        with pytest.raises(ValueError) as exc_info:
            evaluate_expression(expr, "main", label_counter, var_offsets, next_offset)

        assert "Unknown expression type: UNKNOWN_TYPE" in str(exc_info.value)

    def test_missing_type_raises(self):
        """Test that missing type key raises appropriate error."""
        expr = {"value": 42}
        label_counter = {}
        var_offsets = {}
        next_offset = 0

        with pytest.raises(ValueError) as exc_info:
            evaluate_expression(expr, "main", label_counter, var_offsets, next_offset)

        assert "Unknown expression type: None" in str(exc_info.value)


class TestEvaluateExpressionOffsetPropagation:
    """Tests for offset propagation through nested expressions."""

    @patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.evaluate_expression_package.evaluate_expression_src.generate_binop")
    def test_offset_propagation_binop(self, mock_generate_binop):
        """Test that offset is properly propagated through BINOP."""
        mock_generate_binop.return_value = "add r0, r1, r0\n"

        expr = {
            "type": "BINOP",
            "op": "+",
            "left": {"type": "CONST", "value": 1},
            "right": {"type": "CONST", "value": 2}
        }
        label_counter = {}
        var_offsets = {}
        next_offset = 100

        code, offset = evaluate_expression(expr, "main", label_counter, var_offsets, next_offset)

        assert offset == 100

    @patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.evaluate_expression_package.evaluate_expression_src.generate_unop")
    def test_offset_propagation_unop(self, mock_generate_unop):
        """Test that offset is properly propagated through UNOP."""
        mock_generate_unop.return_value = "neg r0, r0\n"

        expr = {
            "type": "UNOP",
            "op": "-",
            "operand": {"type": "CONST", "value": 5}
        }
        label_counter = {}
        var_offsets = {}
        next_offset = 50

        code, offset = evaluate_expression(expr, "main", label_counter, var_offsets, next_offset)

        assert offset == 50


class TestEvaluateExpressionComplex:
    """Tests for complex nested expressions."""

    @patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.evaluate_expression_package.evaluate_expression_src.generate_binop")
    @patch("evaluate_expression_package.evaluate_expression_src.generate_unop")
    def test_complex_expression(self, mock_generate_unop, mock_generate_binop):
        """Test complex nested expression: -(a + b) * c."""
        mock_generate_binop.side_effect = ["add r0, r1, r0\n", "mul r0, r1, r0\n"]
        mock_generate_unop.return_value = "neg r0, r0\n"

        expr = {
            "type": "BINOP",
            "op": "*",
            "left": {
                "type": "UNOP",
                "op": "-",
                "operand": {
                    "type": "BINOP",
                    "op": "+",
                    "left": {"type": "VAR", "var_name": "a"},
                    "right": {"type": "VAR", "var_name": "b"}
                }
            },
            "right": {"type": "VAR", "var_name": "c"}
        }
        label_counter = {}
        var_offsets = {"a": 0, "b": 4, "c": 8}
        next_offset = 12

        code, offset = evaluate_expression(expr, "main", label_counter, var_offsets, next_offset)

        assert "ldr r0, [sp, #0]\n" in code
        assert "ldr r0, [sp, #4]\n" in code
        assert "ldr r0, [sp, #8]\n" in code
        assert mock_generate_binop.call_count == 2
        assert mock_generate_unop.call_count == 1
        assert offset == 12

    @patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.evaluate_expression_package.evaluate_expression_src.generate_binop")
    def test_chained_binop(self, mock_generate_binop):
        """Test chained binary operations: a + b + c."""
        mock_generate_binop.return_value = "add r0, r1, r0\n"

        expr = {
            "type": "BINOP",
            "op": "+",
            "left": {
                "type": "BINOP",
                "op": "+",
                "left": {"type": "VAR", "var_name": "a"},
                "right": {"type": "VAR", "var_name": "b"}
            },
            "right": {"type": "VAR", "var_name": "c"}
        }
        label_counter = {}
        var_offsets = {"a": 0, "b": 4, "c": 8}
        next_offset = 12

        code, offset = evaluate_expression(expr, "main", label_counter, var_offsets, next_offset)

        assert mock_generate_binop.call_count == 2
        assert offset == 12

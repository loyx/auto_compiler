# -*- coding: utf-8 -*-
"""Unit tests for _handle_binary_op function."""

from typing import Dict
from unittest.mock import patch
import pytest

from ._handle_binary_op_src import _handle_binary_op, BINARY_OP_MAP


class TestHandleBinaryOp:
    """Test cases for _handle_binary_op function."""

    def test_add_operator(self):
        """Test binary addition operator."""
        left_expr = {"type": "literal", "value": 5}
        right_expr = {"type": "literal", "value": 3}
        var_offsets: Dict[str, int] = {}
        next_offset = 0

        with patch("..generate_expression_code_src.generate_expression_code") as mock_gen:
            mock_gen.side_effect = [
                ("LOAD_CONST 5\n", 0, 1),
                ("LOAD_CONST 3\n", 1, 2),
            ]

            code, result_offset, updated_offset = _handle_binary_op(
                "+", left_expr, right_expr, var_offsets, next_offset
            )

            assert "LOAD_CONST 5\n" in code
            assert "LOAD_CONST 3\n" in code
            assert "BINARY_ADD\n" in code
            assert result_offset == 0
            assert updated_offset == 2
            assert mock_gen.call_count == 2

    def test_subtract_operator(self):
        """Test binary subtraction operator."""
        left_expr = {"type": "variable", "name": "x"}
        right_expr = {"type": "literal", "value": 10}
        var_offsets = {"x": 0}
        next_offset = 1

        with patch("..generate_expression_code_src.generate_expression_code") as mock_gen:
            mock_gen.side_effect = [
                ("LOAD_VAR x\n", 0, 1),
                ("LOAD_CONST 10\n", 1, 2),
            ]

            code, result_offset, updated_offset = _handle_binary_op(
                "-", left_expr, right_expr, var_offsets, next_offset
            )

            assert "BINARY_SUBTRACT\n" in code
            assert result_offset == 0

    def test_multiply_operator(self):
        """Test binary multiplication operator."""
        left_expr = {"type": "literal", "value": 4}
        right_expr = {"type": "literal", "value": 5}
        var_offsets: Dict[str, int] = {}
        next_offset = 0

        with patch("..generate_expression_code_src.generate_expression_code") as mock_gen:
            mock_gen.side_effect = [
                ("LOAD_CONST 4\n", 0, 1),
                ("LOAD_CONST 5\n", 1, 2),
            ]

            code, result_offset, updated_offset = _handle_binary_op(
                "*", left_expr, right_expr, var_offsets, next_offset
            )

            assert "BINARY_MULTIPLY\n" in code

    def test_divide_operator(self):
        """Test binary division operator."""
        left_expr = {"type": "literal", "value": 20}
        right_expr = {"type": "literal", "value": 4}
        var_offsets: Dict[str, int] = {}
        next_offset = 0

        with patch("..generate_expression_code_src.generate_expression_code") as mock_gen:
            mock_gen.side_effect = [
                ("LOAD_CONST 20\n", 0, 1),
                ("LOAD_CONST 4\n", 1, 2),
            ]

            code, result_offset, updated_offset = _handle_binary_op(
                "/", left_expr, right_expr, var_offsets, next_offset
            )

            assert "BINARY_DIVIDE\n" in code

    def test_floor_divide_operator(self):
        """Test binary floor division operator."""
        left_expr = {"type": "literal", "value": 7}
        right_expr = {"type": "literal", "value": 2}
        var_offsets: Dict[str, int] = {}
        next_offset = 0

        with patch("..generate_expression_code_src.generate_expression_code") as mock_gen:
            mock_gen.side_effect = [
                ("LOAD_CONST 7\n", 0, 1),
                ("LOAD_CONST 2\n", 1, 2),
            ]

            code, result_offset, updated_offset = _handle_binary_op(
                "//", left_expr, right_expr, var_offsets, next_offset
            )

            assert "BINARY_FLOOR_DIVIDE\n" in code

    def test_modulo_operator(self):
        """Test binary modulo operator."""
        left_expr = {"type": "literal", "value": 17}
        right_expr = {"type": "literal", "value": 5}
        var_offsets: Dict[str, int] = {}
        next_offset = 0

        with patch("..generate_expression_code_src.generate_expression_code") as mock_gen:
            mock_gen.side_effect = [
                ("LOAD_CONST 17\n", 0, 1),
                ("LOAD_CONST 5\n", 1, 2),
            ]

            code, result_offset, updated_offset = _handle_binary_op(
                "%", left_expr, right_expr, var_offsets, next_offset
            )

            assert "BINARY_MODULO\n" in code

    def test_power_operator(self):
        """Test binary power operator."""
        left_expr = {"type": "literal", "value": 2}
        right_expr = {"type": "literal", "value": 3}
        var_offsets: Dict[str, int] = {}
        next_offset = 0

        with patch("..generate_expression_code_src.generate_expression_code") as mock_gen:
            mock_gen.side_effect = [
                ("LOAD_CONST 2\n", 0, 1),
                ("LOAD_CONST 3\n", 1, 2),
            ]

            code, result_offset, updated_offset = _handle_binary_op(
                "**", left_expr, right_expr, var_offsets, next_offset
            )

            assert "BINARY_POWER\n" in code

    def test_comparison_operators(self):
        """Test all comparison operators."""
        comparison_ops = [
            ("==", "BINARY_EQUAL"),
            ("!=", "BINARY_NOT_EQUAL"),
            ("<", "BINARY_LESS_THAN"),
            ("<=", "BINARY_LESS_EQUAL"),
            (">", "BINARY_GREATER_THAN"),
            (">=", "BINARY_GREATER_EQUAL"),
        ]

        for op, expected_instruction in comparison_ops:
            left_expr = {"type": "literal", "value": 1}
            right_expr = {"type": "literal", "value": 2}
            var_offsets: Dict[str, int] = {}
            next_offset = 0

            with patch("..generate_expression_code_src.generate_expression_code") as mock_gen:
                mock_gen.side_effect = [
                    ("LOAD_CONST 1\n", 0, 1),
                    ("LOAD_CONST 2\n", 1, 2),
                ]

                code, result_offset, updated_offset = _handle_binary_op(
                    op, left_expr, right_expr, var_offsets, next_offset
                )

                assert expected_instruction in code, f"Failed for operator: {op}"

    def test_bitwise_operators(self):
        """Test all bitwise operators."""
        bitwise_ops = [
            ("&", "BINARY_AND"),
            ("|", "BINARY_OR"),
            ("^", "BINARY_XOR"),
            ("<<", "BINARY_LSHIFT"),
            (">>", "BINARY_RSHIFT"),
        ]

        for op, expected_instruction in bitwise_ops:
            left_expr = {"type": "literal", "value": 5}
            right_expr = {"type": "literal", "value": 3}
            var_offsets: Dict[str, int] = {}
            next_offset = 0

            with patch("..generate_expression_code_src.generate_expression_code") as mock_gen:
                mock_gen.side_effect = [
                    ("LOAD_CONST 5\n", 0, 1),
                    ("LOAD_CONST 3\n", 1, 2),
                ]

                code, result_offset, updated_offset = _handle_binary_op(
                    op, left_expr, right_expr, var_offsets, next_offset
                )

                assert expected_instruction in code, f"Failed for operator: {op}"

    def test_unsupported_operator_raises_error(self):
        """Test that unsupported operator raises ValueError."""
        left_expr = {"type": "literal", "value": 1}
        right_expr = {"type": "literal", "value": 2}
        var_offsets: Dict[str, int] = {}
        next_offset = 0

        with patch("..generate_expression_code_src.generate_expression_code") as mock_gen:
            mock_gen.side_effect = [
                ("LOAD_CONST 1\n", 0, 1),
                ("LOAD_CONST 2\n", 1, 2),
            ]

            with pytest.raises(ValueError) as exc_info:
                _handle_binary_op("???", left_expr, right_expr, var_offsets, next_offset)

            assert "Unsupported binary operator: ???" in str(exc_info.value)

    def test_code_assembly_order(self):
        """Test that code is assembled in correct order: left, right, instruction."""
        left_expr = {"type": "literal", "value": 10}
        right_expr = {"type": "literal", "value": 20}
        var_offsets: Dict[str, int] = {}
        next_offset = 0

        with patch("..generate_expression_code_src.generate_expression_code") as mock_gen:
            mock_gen.side_effect = [
                ("LEFT_CODE\n", 0, 1),
                ("RIGHT_CODE\n", 1, 2),
            ]

            code, result_offset, updated_offset = _handle_binary_op(
                "+", left_expr, right_expr, var_offsets, next_offset
            )

            lines = code.strip().split("\n")
            assert lines[0] == "LEFT_CODE"
            assert lines[1] == "RIGHT_CODE"
            assert lines[2] == "BINARY_ADD"

    def test_result_offset_is_left_offset(self):
        """Test that result offset is the left operand's offset."""
        left_expr = {"type": "literal", "value": 1}
        right_expr = {"type": "literal", "value": 2}
        var_offsets: Dict[str, int] = {}
        next_offset = 0

        with patch("..generate_expression_code_src.generate_expression_code") as mock_gen:
            mock_gen.side_effect = [
                ("LOAD_CONST 1\n", 5, 1),  # left_offset = 5
                ("LOAD_CONST 2\n", 6, 2),  # right_offset = 6
            ]

            code, result_offset, updated_offset = _handle_binary_op(
                "+", left_expr, right_expr, var_offsets, next_offset
            )

            assert result_offset == 5

    def test_next_offset_propagation(self):
        """Test that next_offset is properly propagated through calls."""
        left_expr = {"type": "literal", "value": 1}
        right_expr = {"type": "literal", "value": 2}
        var_offsets: Dict[str, int] = {}
        next_offset = 10

        with patch("..generate_expression_code_src.generate_expression_code") as mock_gen:
            mock_gen.side_effect = [
                ("LOAD_CONST 1\n", 0, 11),  # next_offset becomes 11
                ("LOAD_CONST 2\n", 1, 12),  # next_offset becomes 12
            ]

            code, result_offset, updated_offset = _handle_binary_op(
                "+", left_expr, right_expr, var_offsets, next_offset
            )

            assert updated_offset == 12

    def test_nested_binary_operations(self):
        """Test handling of nested binary operations (expression trees)."""
        # (a + b) * c
        left_expr = {
            "type": "binary_op",
            "operator": "+",
            "left": {"type": "variable", "name": "a"},
            "right": {"type": "variable", "name": "b"},
        }
        right_expr = {"type": "variable", "name": "c"}
        var_offsets = {"a": 0, "b": 1, "c": 2}
        next_offset = 3

        with patch("..generate_expression_code_src.generate_expression_code") as mock_gen:
            mock_gen.side_effect = [
                ("LOAD_VAR a\nLOAD_VAR b\nBINARY_ADD\n", 0, 4),
                ("LOAD_VAR c\n", 4, 5),
            ]

            code, result_offset, updated_offset = _handle_binary_op(
                "*", left_expr, right_expr, var_offsets, next_offset
            )

            assert "BINARY_MULTIPLY\n" in code
            assert result_offset == 0
            assert updated_offset == 5

    def test_generate_expression_code_called_twice(self):
        """Test that generate_expression_code is called exactly twice."""
        left_expr = {"type": "literal", "value": 1}
        right_expr = {"type": "literal", "value": 2}
        var_offsets: Dict[str, int] = {}
        next_offset = 0

        with patch("..generate_expression_code_src.generate_expression_code") as mock_gen:
            mock_gen.side_effect = [
                ("LOAD_CONST 1\n", 0, 1),
                ("LOAD_CONST 2\n", 1, 2),
            ]

            _handle_binary_op("+", left_expr, right_expr, var_offsets, next_offset)

            assert mock_gen.call_count == 2

    def test_generate_expression_code_call_order(self):
        """Test that generate_expression_code is called left first, then right."""
        left_expr = {"type": "literal", "value": 1}
        right_expr = {"type": "literal", "value": 2}
        var_offsets: Dict[str, int] = {}
        next_offset = 0

        with patch("..generate_expression_code_src.generate_expression_code") as mock_gen:
            mock_gen.side_effect = [
                ("LOAD_CONST 1\n", 0, 1),
                ("LOAD_CONST 2\n", 1, 2),
            ]

            _handle_binary_op("+", left_expr, right_expr, var_offsets, next_offset)

            calls = mock_gen.call_args_list
            assert calls[0][0][0] == left_expr
            assert calls[1][0][0] == right_expr

    def test_var_offsets_passed_to_generate_expression_code(self):
        """Test that var_offsets is passed correctly to generate_expression_code."""
        left_expr = {"type": "variable", "name": "x"}
        right_expr = {"type": "variable", "name": "y"}
        var_offsets = {"x": 0, "y": 1}
        next_offset = 2

        with patch("..generate_expression_code_src.generate_expression_code") as mock_gen:
            mock_gen.side_effect = [
                ("LOAD_VAR x\n", 0, 2),
                ("LOAD_VAR y\n", 1, 2),
            ]

            _handle_binary_op("+", left_expr, right_expr, var_offsets, next_offset)

            for call in mock_gen.call_args_list:
                assert call[0][1] == var_offsets

    def test_empty_string_operator_raises_error(self):
        """Test that empty string operator raises ValueError."""
        left_expr = {"type": "literal", "value": 1}
        right_expr = {"type": "literal", "value": 2}
        var_offsets: Dict[str, int] = {}
        next_offset = 0

        with patch("..generate_expression_code_src.generate_expression_code") as mock_gen:
            mock_gen.side_effect = [
                ("LOAD_CONST 1\n", 0, 1),
                ("LOAD_CONST 2\n", 1, 2),
            ]

            with pytest.raises(ValueError):
                _handle_binary_op("", left_expr, right_expr, var_offsets, next_offset)

    def test_complex_expression_with_call(self):
        """Test binary op with function call as operand."""
        left_expr = {
            "type": "call",
            "function": "get_value",
            "args": [],
        }
        right_expr = {"type": "literal", "value": 10}
        var_offsets: Dict[str, int] = {}
        next_offset = 0

        with patch("..generate_expression_code_src.generate_expression_code") as mock_gen:
            mock_gen.side_effect = [
                ("CALL get_value\n", 0, 1),
                ("LOAD_CONST 10\n", 1, 2),
            ]

            code, result_offset, updated_offset = _handle_binary_op(
                "+", left_expr, right_expr, var_offsets, next_offset
            )

            assert "CALL get_value\n" in code
            assert "LOAD_CONST 10\n" in code
            assert "BINARY_ADD\n" in code

    def test_all_operators_in_map_are_supported(self):
        """Test that all operators in BINARY_OP_MAP are supported."""
        left_expr = {"type": "literal", "value": 1}
        right_expr = {"type": "literal", "value": 2}
        var_offsets: Dict[str, int] = {}
        next_offset = 0

        for operator in BINARY_OP_MAP.keys():
            with patch("..generate_expression_code_src.generate_expression_code") as mock_gen:
                mock_gen.side_effect = [
                    ("LOAD_CONST 1\n", 0, 1),
                    ("LOAD_CONST 2\n", 1, 2),
                ]

                code, result_offset, updated_offset = _handle_binary_op(
                    operator, left_expr, right_expr, var_offsets, next_offset
                )

                expected_instruction = BINARY_OP_MAP[operator]
                assert expected_instruction in code, f"Failed for operator: {operator}"

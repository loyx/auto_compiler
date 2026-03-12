# -*- coding: utf-8 -*-
"""Unit tests for generate_short_circuit_and function."""

from unittest.mock import patch
import pytest

from .generate_short_circuit_and_src import generate_short_circuit_and


class TestGenerateShortCircuitAnd:
    """Test cases for generate_short_circuit_and function."""

    def test_happy_path_basic_and_expression(self):
        """Test basic AND expression with simple left and right operands."""
        expr = {
            "type": "AND",
            "left": {"type": "CONST", "value": 1},
            "right": {"type": "CONST", "value": 2}
        }
        func_name = "test_func"
        label_counter = {"skip": 0}
        var_offsets = {}
        next_offset = 0

        with patch(
            "generate_short_circuit_and_package.generate_short_circuit_and_src.generate_expr_code"
        ) as mock_generate_expr_code:
            # First call for left operand
            # Second call for right operand
            mock_generate_expr_code.side_effect = [
                ("    mov x0, #1\n", 0),
                ("    mov x0, #2\n", 0)
            ]

            result_code, result_offset = generate_short_circuit_and(
                expr, func_name, label_counter, var_offsets, next_offset
            )

            # Verify label counter was incremented
            assert label_counter["skip"] == 1

            # Verify generate_expr_code was called twice
            assert mock_generate_expr_code.call_count == 2

            # Verify the code structure
            expected_skip_label = "test_func_and_skip_0"
            assert expected_skip_label in result_code
            assert f"    cbz x0, {expected_skip_label}\n" in result_code
            assert "    mov x0, #1\n" in result_code
            assert "    mov x0, #2\n" in result_code
            assert f"{expected_skip_label}:\n" in result_code

            # Verify code order: left_code + branch_code + right_code + label_code
            left_pos = result_code.find("    mov x0, #1\n")
            branch_pos = result_code.find(f"    cbz x0, {expected_skip_label}\n")
            right_pos = result_code.find("    mov x0, #2\n")
            label_pos = result_code.find(f"{expected_skip_label}:\n")

            assert left_pos < branch_pos < right_pos < label_pos

    def test_label_counter_increment(self):
        """Test that label_counter['skip'] is incremented after use."""
        expr = {
            "type": "AND",
            "left": {"type": "CONST", "value": 1},
            "right": {"type": "CONST", "value": 2}
        }
        func_name = "test_func"
        label_counter = {"skip": 5}
        var_offsets = {}
        next_offset = 0

        with patch(
            "generate_short_circuit_and_package.generate_short_circuit_and_src.generate_expr_code"
        ) as mock_generate_expr_code:
            mock_generate_expr_code.side_effect = [
                ("    mov x0, #1\n", 0),
                ("    mov x0, #2\n", 0)
            ]

            generate_short_circuit_and(
                expr, func_name, label_counter, var_offsets, next_offset
            )

            # Verify label counter was incremented from 5 to 6
            assert label_counter["skip"] == 6

    def test_label_naming_with_different_func_name(self):
        """Test that skip label uses correct func_name prefix."""
        expr = {
            "type": "AND",
            "left": {"type": "CONST", "value": 1},
            "right": {"type": "CONST", "value": 2}
        }
        func_name = "my_function"
        label_counter = {"skip": 3}
        var_offsets = {}
        next_offset = 0

        with patch(
            "generate_short_circuit_and_package.generate_short_circuit_and_src.generate_expr_code"
        ) as mock_generate_expr_code:
            mock_generate_expr_code.side_effect = [
                ("    mov x0, #1\n", 0),
                ("    mov x0, #2\n", 0)
            ]

            result_code, _ = generate_short_circuit_and(
                expr, func_name, label_counter, var_offsets, next_offset
            )

            # Verify label uses correct func_name and counter value (before increment)
            assert "my_function_and_skip_3" in result_code
            assert "    cbz x0, my_function_and_skip_3\n" in result_code
            assert "my_function_and_skip_3:\n" in result_code

    def test_next_offset_propagation(self):
        """Test that next_offset is properly propagated through generate_expr_code calls."""
        expr = {
            "type": "AND",
            "left": {"type": "CONST", "value": 1},
            "right": {"type": "CONST", "value": 2}
        }
        func_name = "test_func"
        label_counter = {"skip": 0}
        var_offsets = {}
        next_offset = 10

        with patch(
            "generate_short_circuit_and_package.generate_short_circuit_and_src.generate_expr_code"
        ) as mock_generate_expr_code:
            # First call returns offset 15, second call returns offset 20
            mock_generate_expr_code.side_effect = [
                ("    mov x0, #1\n", 15),
                ("    mov x0, #2\n", 20)
            ]

            _, result_offset = generate_short_circuit_and(
                expr, func_name, label_counter, var_offsets, next_offset
            )

            # Verify final offset is from the last generate_expr_code call
            assert result_offset == 20

            # Verify generate_expr_code was called with correct offsets
            calls = mock_generate_expr_code.call_args_list
            assert len(calls) == 2
            # First call should use initial next_offset (10)
            assert calls[0][0][4] == 10
            # Second call should use offset from first call (15)
            assert calls[1][0][4] == 15

    def test_complex_nested_expressions(self):
        """Test AND expression with nested operands."""
        expr = {
            "type": "AND",
            "left": {
                "type": "AND",
                "left": {"type": "CONST", "value": 1},
                "right": {"type": "CONST", "value": 2}
            },
            "right": {
                "type": "OR",
                "left": {"type": "CONST", "value": 3},
                "right": {"type": "CONST", "value": 4}
            }
        }
        func_name = "test_func"
        label_counter = {"skip": 0}
        var_offsets = {}
        next_offset = 0

        with patch(
            "generate_short_circuit_and_package.generate_short_circuit_and_src.generate_expr_code"
        ) as mock_generate_expr_code:
            mock_generate_expr_code.side_effect = [
                ("    ; left nested code\n", 5),
                ("    ; right nested code\n", 10)
            ]

            result_code, result_offset = generate_short_circuit_and(
                expr, func_name, label_counter, var_offsets, next_offset
            )

            assert label_counter["skip"] == 1
            assert result_offset == 10
            assert "    ; left nested code\n" in result_code
            assert "    ; right nested code\n" in result_code
            assert "    cbz x0, test_func_and_skip_0\n" in result_code
            assert "test_func_and_skip_0:\n" in result_code

    def test_var_offsets_passed_through(self):
        """Test that var_offsets is passed to generate_expr_code calls."""
        expr = {
            "type": "AND",
            "left": {"type": "VAR", "name": "x"},
            "right": {"type": "VAR", "name": "y"}
        }
        func_name = "test_func"
        label_counter = {"skip": 0}
        var_offsets = {"x": 0, "y": 8}
        next_offset = 16

        with patch(
            "generate_short_circuit_and_package.generate_short_circuit_and_src.generate_expr_code"
        ) as mock_generate_expr_code:
            mock_generate_expr_code.side_effect = [
                ("    ldr x0, [sp, #0]\n", 16),
                ("    ldr x0, [sp, #8]\n", 16)
            ]

            generate_short_circuit_and(
                expr, func_name, label_counter, var_offsets, next_offset
            )

            # Verify var_offsets was passed to both calls
            calls = mock_generate_expr_code.call_args_list
            assert calls[0][0][3] == var_offsets
            assert calls[1][0][3] == var_offsets

    def test_empty_label_counter(self):
        """Test behavior when label_counter starts at 0."""
        expr = {
            "type": "AND",
            "left": {"type": "CONST", "value": 1},
            "right": {"type": "CONST", "value": 2}
        }
        func_name = "func"
        label_counter = {"skip": 0}
        var_offsets = {}
        next_offset = 0

        with patch(
            "generate_short_circuit_and_package.generate_short_circuit_and_src.generate_expr_code"
        ) as mock_generate_expr_code:
            mock_generate_expr_code.side_effect = [
                ("    mov x0, #1\n", 0),
                ("    mov x0, #2\n", 0)
            ]

            result_code, _ = generate_short_circuit_and(
                expr, func_name, label_counter, var_offsets, next_offset
            )

            assert "func_and_skip_0" in result_code
            assert label_counter["skip"] == 1

    def test_multiple_and_expressions_sequential(self):
        """Test multiple AND expressions generating unique labels."""
        expr = {
            "type": "AND",
            "left": {"type": "CONST", "value": 1},
            "right": {"type": "CONST", "value": 2}
        }
        func_name = "test_func"
        label_counter = {"skip": 0}
        var_offsets = {}
        next_offset = 0

        with patch(
            "generate_short_circuit_and_package.generate_short_circuit_and_src.generate_expr_code"
        ) as mock_generate_expr_code:
            mock_generate_expr_code.side_effect = [
                ("    mov x0, #1\n", 0),
                ("    mov x0, #2\n", 0),
                ("    mov x0, #3\n", 0),
                ("    mov x0, #4\n", 0)
            ]

            # First AND expression
            result_code1, _ = generate_short_circuit_and(
                expr, func_name, label_counter, var_offsets, next_offset
            )
            assert label_counter["skip"] == 1
            assert "test_func_and_skip_0" in result_code1
            assert "test_func_and_skip_1" not in result_code1

            # Second AND expression
            result_code2, _ = generate_short_circuit_and(
                expr, func_name, label_counter, var_offsets, next_offset
            )
            assert label_counter["skip"] == 2
            assert "test_func_and_skip_1" in result_code2
            assert "test_func_and_skip_0" not in result_code2

    def test_code_structure_exact_format(self):
        """Test that generated code follows exact expected format."""
        expr = {
            "type": "AND",
            "left": {"type": "CONST", "value": 1},
            "right": {"type": "CONST", "value": 2}
        }
        func_name = "test"
        label_counter = {"skip": 0}
        var_offsets = {}
        next_offset = 0

        with patch(
            "generate_short_circuit_and_package.generate_short_circuit_and_src.generate_expr_code"
        ) as mock_generate_expr_code:
            mock_generate_expr_code.side_effect = [
                ("LEFT_CODE\n", 0),
                ("RIGHT_CODE\n", 0)
            ]

            result_code, _ = generate_short_circuit_and(
                expr, func_name, label_counter, var_offsets, next_offset
            )

            # Expected exact structure
            expected = "LEFT_CODE\n    cbz x0, test_and_skip_0\nRIGHT_CODE\ntest_and_skip_0:\n"
            assert result_code == expected

    def test_return_type_tuple(self):
        """Test that function returns a tuple of (str, int)."""
        expr = {
            "type": "AND",
            "left": {"type": "CONST", "value": 1},
            "right": {"type": "CONST", "value": 2}
        }
        func_name = "test_func"
        label_counter = {"skip": 0}
        var_offsets = {}
        next_offset = 0

        with patch(
            "generate_short_circuit_and_package.generate_short_circuit_and_src.generate_expr_code"
        ) as mock_generate_expr_code:
            mock_generate_expr_code.side_effect = [
                ("    mov x0, #1\n", 0),
                ("    mov x0, #2\n", 0)
            ]

            result = generate_short_circuit_and(
                expr, func_name, label_counter, var_offsets, next_offset
            )

            assert isinstance(result, tuple)
            assert len(result) == 2
            assert isinstance(result[0], str)
            assert isinstance(result[1], int)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

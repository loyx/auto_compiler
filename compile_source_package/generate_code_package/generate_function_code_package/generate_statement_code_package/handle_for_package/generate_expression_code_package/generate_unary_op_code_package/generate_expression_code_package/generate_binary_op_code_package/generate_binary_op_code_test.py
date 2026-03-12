# -*- coding: utf-8 -*-
"""Unit tests for generate_binary_op_code function."""

from unittest.mock import patch

from .generate_binary_op_code_src import (
    generate_binary_op_code,
    _generate_logical_and,
    _generate_logical_or,
    _generate_binary_instruction,
)


class TestGenerateBinaryOpCode:
    """Test suite for generate_binary_op_code function."""

    def setup_method(self):
        """Set up test fixtures."""
        self.func_name = "test_func"
        self.label_counter = {"counter": 0}
        self.var_offsets = {"x": 0, "y": 8}
        self.next_offset = 16

    def test_arithmetic_addition(self):
        """Test + operator generates ADD instruction."""
        expr = {
            "type": "BINARY_OP",
            "operator": "+",
            "left": {"type": "NUMBER", "value": 5},
            "right": {"type": "NUMBER", "value": 3},
        }
        label_counter = {"counter": 0}

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_unary_op_code_package.generate_expression_code_package.generate_binary_op_code_package.generate_expression_code_src.generate_expression_code"
        ) as mock_gen_expr:
            mock_gen_expr.side_effect = [
                ("MOV x0, #5\n", 16),
                ("MOV x0, #3\n", 16),
            ]

            code, next_offset = generate_binary_op_code(
                expr, self.func_name, label_counter, self.var_offsets, self.next_offset
            )

            assert "MOV x1, x0" in code
            assert "ADD x0, x1, x0" in code
            assert next_offset == 16

    def test_arithmetic_subtraction(self):
        """Test - operator generates SUB instruction."""
        expr = {
            "type": "BINARY_OP",
            "operator": "-",
            "left": {"type": "NUMBER", "value": 10},
            "right": {"type": "NUMBER", "value": 4},
        }
        label_counter = {"counter": 0}

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_unary_op_code_package.generate_expression_code_package.generate_binary_op_code_package.generate_expression_code_src.generate_expression_code"
        ) as mock_gen_expr:
            mock_gen_expr.side_effect = [
                ("MOV x0, #10\n", 16),
                ("MOV x0, #4\n", 16),
            ]

            code, _ = generate_binary_op_code(
                expr, self.func_name, label_counter, self.var_offsets, self.next_offset
            )

            assert "SUB x0, x1, x0" in code

    def test_arithmetic_multiplication(self):
        """Test * operator generates MUL instruction."""
        expr = {
            "type": "BINARY_OP",
            "operator": "*",
            "left": {"type": "NUMBER", "value": 6},
            "right": {"type": "NUMBER", "value": 7},
        }
        label_counter = {"counter": 0}

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_unary_op_code_package.generate_expression_code_package.generate_binary_op_code_package.generate_expression_code_src.generate_expression_code"
        ) as mock_gen_expr:
            mock_gen_expr.side_effect = [
                ("MOV x0, #6\n", 16),
                ("MOV x0, #7\n", 16),
            ]

            code, _ = generate_binary_op_code(
                expr, self.func_name, label_counter, self.var_offsets, self.next_offset
            )

            assert "MUL x0, x1, x0" in code

    def test_arithmetic_division(self):
        """Test / operator generates SDIV instruction."""
        expr = {
            "type": "BINARY_OP",
            "operator": "/",
            "left": {"type": "NUMBER", "value": 20},
            "right": {"type": "NUMBER", "value": 4},
        }
        label_counter = {"counter": 0}

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_unary_op_code_package.generate_expression_code_package.generate_binary_op_code_package.generate_expression_code_src.generate_expression_code"
        ) as mock_gen_expr:
            mock_gen_expr.side_effect = [
                ("MOV x0, #20\n", 16),
                ("MOV x0, #4\n", 16),
            ]

            code, _ = generate_binary_op_code(
                expr, self.func_name, label_counter, self.var_offsets, self.next_offset
            )

            assert "SDIV x0, x1, x0" in code

    def test_comparison_equal(self):
        """Test == operator generates CMP and CSET EQ."""
        expr = {
            "type": "BINARY_OP",
            "operator": "==",
            "left": {"type": "NUMBER", "value": 5},
            "right": {"type": "NUMBER", "value": 5},
        }
        label_counter = {"counter": 0}

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_unary_op_code_package.generate_expression_code_package.generate_binary_op_code_package.generate_expression_code_src.generate_expression_code"
        ) as mock_gen_expr:
            mock_gen_expr.side_effect = [
                ("MOV x0, #5\n", 16),
                ("MOV x0, #5\n", 16),
            ]

            code, _ = generate_binary_op_code(
                expr, self.func_name, label_counter, self.var_offsets, self.next_offset
            )

            assert "CMP x1, x0" in code
            assert "CSET x0, EQ" in code

    def test_comparison_not_equal(self):
        """Test != operator generates CMP and CSET NE."""
        expr = {
            "type": "BINARY_OP",
            "operator": "!=",
            "left": {"type": "NUMBER", "value": 5},
            "right": {"type": "NUMBER", "value": 3},
        }
        label_counter = {"counter": 0}

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_unary_op_code_package.generate_expression_code_package.generate_binary_op_code_package.generate_expression_code_src.generate_expression_code"
        ) as mock_gen_expr:
            mock_gen_expr.side_effect = [
                ("MOV x0, #5\n", 16),
                ("MOV x0, #3\n", 16),
            ]

            code, _ = generate_binary_op_code(
                expr, self.func_name, label_counter, self.var_offsets, self.next_offset
            )

            assert "CSET x0, NE" in code

    def test_comparison_less_than(self):
        """Test < operator generates CMP and CSET LT."""
        expr = {
            "type": "BINARY_OP",
            "operator": "<",
            "left": {"type": "NUMBER", "value": 3},
            "right": {"type": "NUMBER", "value": 5},
        }
        label_counter = {"counter": 0}

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_unary_op_code_package.generate_expression_code_package.generate_binary_op_code_package.generate_expression_code_src.generate_expression_code"
        ) as mock_gen_expr:
            mock_gen_expr.side_effect = [
                ("MOV x0, #3\n", 16),
                ("MOV x0, #5\n", 16),
            ]

            code, _ = generate_binary_op_code(
                expr, self.func_name, label_counter, self.var_offsets, self.next_offset
            )

            assert "CSET x0, LT" in code

    def test_comparison_greater_than(self):
        """Test > operator generates CMP and CSET GT."""
        expr = {
            "type": "BINARY_OP",
            "operator": ">",
            "left": {"type": "NUMBER", "value": 10},
            "right": {"type": "NUMBER", "value": 5},
        }
        label_counter = {"counter": 0}

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_unary_op_code_package.generate_expression_code_package.generate_binary_op_code_package.generate_expression_code_src.generate_expression_code"
        ) as mock_gen_expr:
            mock_gen_expr.side_effect = [
                ("MOV x0, #10\n", 16),
                ("MOV x0, #5\n", 16),
            ]

            code, _ = generate_binary_op_code(
                expr, self.func_name, label_counter, self.var_offsets, self.next_offset
            )

            assert "CSET x0, GT" in code

    def test_comparison_less_equal(self):
        """Test <= operator generates CMP and CSET LE."""
        expr = {
            "type": "BINARY_OP",
            "operator": "<=",
            "left": {"type": "NUMBER", "value": 5},
            "right": {"type": "NUMBER", "value": 5},
        }
        label_counter = {"counter": 0}

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_unary_op_code_package.generate_expression_code_package.generate_binary_op_code_package.generate_expression_code_src.generate_expression_code"
        ) as mock_gen_expr:
            mock_gen_expr.side_effect = [
                ("MOV x0, #5\n", 16),
                ("MOV x0, #5\n", 16),
            ]

            code, _ = generate_binary_op_code(
                expr, self.func_name, label_counter, self.var_offsets, self.next_offset
            )

            assert "CSET x0, LE" in code

    def test_comparison_greater_equal(self):
        """Test >= operator generates CMP and CSET GE."""
        expr = {
            "type": "BINARY_OP",
            "operator": ">=",
            "left": {"type": "NUMBER", "value": 10},
            "right": {"type": "NUMBER", "value": 5},
        }
        label_counter = {"counter": 0}

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_unary_op_code_package.generate_expression_code_package.generate_binary_op_code_package.generate_expression_code_src.generate_expression_code"
        ) as mock_gen_expr:
            mock_gen_expr.side_effect = [
                ("MOV x0, #10\n", 16),
                ("MOV x0, #5\n", 16),
            ]

            code, _ = generate_binary_op_code(
                expr, self.func_name, label_counter, self.var_offsets, self.next_offset
            )

            assert "CSET x0, GE" in code

    def test_bitwise_and(self):
        """Test & operator generates AND instruction."""
        expr = {
            "type": "BINARY_OP",
            "operator": "&",
            "left": {"type": "NUMBER", "value": 5},
            "right": {"type": "NUMBER", "value": 3},
        }
        label_counter = {"counter": 0}

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_unary_op_code_package.generate_expression_code_package.generate_binary_op_code_package.generate_expression_code_src.generate_expression_code"
        ) as mock_gen_expr:
            mock_gen_expr.side_effect = [
                ("MOV x0, #5\n", 16),
                ("MOV x0, #3\n", 16),
            ]

            code, _ = generate_binary_op_code(
                expr, self.func_name, label_counter, self.var_offsets, self.next_offset
            )

            assert "AND x0, x1, x0" in code

    def test_bitwise_or(self):
        """Test | operator generates ORR instruction."""
        expr = {
            "type": "BINARY_OP",
            "operator": "|",
            "left": {"type": "NUMBER", "value": 5},
            "right": {"type": "NUMBER", "value": 3},
        }
        label_counter = {"counter": 0}

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_unary_op_code_package.generate_expression_code_package.generate_binary_op_code_package.generate_expression_code_src.generate_expression_code"
        ) as mock_gen_expr:
            mock_gen_expr.side_effect = [
                ("MOV x0, #5\n", 16),
                ("MOV x0, #3\n", 16),
            ]

            code, _ = generate_binary_op_code(
                expr, self.func_name, label_counter, self.var_offsets, self.next_offset
            )

            assert "ORR x0, x1, x0" in code

    def test_bitwise_xor(self):
        """Test ^ operator generates EOR instruction."""
        expr = {
            "type": "BINARY_OP",
            "operator": "^",
            "left": {"type": "NUMBER", "value": 5},
            "right": {"type": "NUMBER", "value": 3},
        }
        label_counter = {"counter": 0}

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_unary_op_code_package.generate_expression_code_package.generate_binary_op_code_package.generate_expression_code_src.generate_expression_code"
        ) as mock_gen_expr:
            mock_gen_expr.side_effect = [
                ("MOV x0, #5\n", 16),
                ("MOV x0, #3\n", 16),
            ]

            code, _ = generate_binary_op_code(
                expr, self.func_name, label_counter, self.var_offsets, self.next_offset
            )

            assert "EOR x0, x1, x0" in code

    def test_bitwise_left_shift(self):
        """Test << operator generates LSL instruction."""
        expr = {
            "type": "BINARY_OP",
            "operator": "<<",
            "left": {"type": "NUMBER", "value": 1},
            "right": {"type": "NUMBER", "value": 3},
        }
        label_counter = {"counter": 0}

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_unary_op_code_package.generate_expression_code_package.generate_binary_op_code_package.generate_expression_code_src.generate_expression_code"
        ) as mock_gen_expr:
            mock_gen_expr.side_effect = [
                ("MOV x0, #1\n", 16),
                ("MOV x0, #3\n", 16),
            ]

            code, _ = generate_binary_op_code(
                expr, self.func_name, label_counter, self.var_offsets, self.next_offset
            )

            assert "LSL x0, x1, x0" in code

    def test_bitwise_right_shift(self):
        """Test >> operator generates ASR instruction."""
        expr = {
            "type": "BINARY_OP",
            "operator": ">>",
            "left": {"type": "NUMBER", "value": 8},
            "right": {"type": "NUMBER", "value": 2},
        }
        label_counter = {"counter": 0}

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_unary_op_code_package.generate_expression_code_package.generate_binary_op_code_package.generate_expression_code_src.generate_expression_code"
        ) as mock_gen_expr:
            mock_gen_expr.side_effect = [
                ("MOV x0, #8\n", 16),
                ("MOV x0, #2\n", 16),
            ]

            code, _ = generate_binary_op_code(
                expr, self.func_name, label_counter, self.var_offsets, self.next_offset
            )

            assert "ASR x0, x1, x0" in code

    def test_logical_and_short_circuit_when_left_zero(self):
        """Test && short-circuits when left operand is zero."""
        expr = {
            "type": "BINARY_OP",
            "operator": "&&",
            "left": {"type": "NUMBER", "value": 0},
            "right": {"type": "NUMBER", "value": 5},
        }
        label_counter = {"counter": 5}

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_unary_op_code_package.generate_expression_code_package.generate_binary_op_code_package.generate_expression_code_src.generate_expression_code"
        ) as mock_gen_expr:
            mock_gen_expr.side_effect = [
                ("MOV x0, #0\n", 16),
                ("MOV x0, #5\n", 16),
            ]

            code, _ = generate_binary_op_code(
                expr, self.func_name, label_counter, self.var_offsets, self.next_offset
            )

            assert "CMP x0, #0" in code
            assert "BEQ L_test_func_end_5" in code
            assert "L_test_func_end_5:" in code
            assert label_counter["counter"] == 6

    def test_logical_and_evaluates_right_when_left_nonzero(self):
        """Test && evaluates right operand when left is non-zero."""
        expr = {
            "type": "BINARY_OP",
            "operator": "&&",
            "left": {"type": "NUMBER", "value": 1},
            "right": {"type": "NUMBER", "value": 5},
        }
        label_counter = {"counter": 3}

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_unary_op_code_package.generate_expression_code_package.generate_binary_op_code_package.generate_expression_code_src.generate_expression_code"
        ) as mock_gen_expr:
            mock_gen_expr.side_effect = [
                ("MOV x0, #1\n", 16),
                ("MOV x0, #5\n", 16),
            ]

            code, _ = generate_binary_op_code(
                expr, self.func_name, label_counter, self.var_offsets, self.next_offset
            )

            assert "BEQ L_test_func_end_3" in code
            assert "MOV x0, #5" in code
            assert "L_test_func_end_3:" in code
            assert label_counter["counter"] == 4

    def test_logical_or_short_circuit_when_left_nonzero(self):
        """Test || short-circuits when left operand is non-zero."""
        expr = {
            "type": "BINARY_OP",
            "operator": "||",
            "left": {"type": "NUMBER", "value": 1},
            "right": {"type": "NUMBER", "value": 5},
        }
        label_counter = {"counter": 7}

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_unary_op_code_package.generate_expression_code_package.generate_binary_op_code_package.generate_expression_code_src.generate_expression_code"
        ) as mock_gen_expr:
            mock_gen_expr.side_effect = [
                ("MOV x0, #1\n", 16),
                ("MOV x0, #5\n", 16),
            ]

            code, _ = generate_binary_op_code(
                expr, self.func_name, label_counter, self.var_offsets, self.next_offset
            )

            assert "CMP x0, #0" in code
            assert "BNE L_test_func_end_7" in code
            assert "L_test_func_end_7:" in code
            assert label_counter["counter"] == 8

    def test_logical_or_evaluates_right_when_left_zero(self):
        """Test || evaluates right operand when left is zero."""
        expr = {
            "type": "BINARY_OP",
            "operator": "||",
            "left": {"type": "NUMBER", "value": 0},
            "right": {"type": "NUMBER", "value": 5},
        }
        label_counter = {"counter": 2}

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_unary_op_code_package.generate_expression_code_package.generate_binary_op_code_package.generate_expression_code_src.generate_expression_code"
        ) as mock_gen_expr:
            mock_gen_expr.side_effect = [
                ("MOV x0, #0\n", 16),
                ("MOV x0, #5\n", 16),
            ]

            code, _ = generate_binary_op_code(
                expr, self.func_name, label_counter, self.var_offsets, self.next_offset
            )

            assert "BNE L_test_func_end_2" in code
            assert "MOV x0, #5" in code
            assert "L_test_func_end_2:" in code
            assert label_counter["counter"] == 3

    def test_unsupported_operator(self):
        """Test unsupported operator generates comment."""
        expr = {
            "type": "BINARY_OP",
            "operator": "**",
            "left": {"type": "NUMBER", "value": 2},
            "right": {"type": "NUMBER", "value": 3},
        }
        label_counter = {"counter": 0}

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_unary_op_code_package.generate_expression_code_package.generate_binary_op_code_package.generate_expression_code_src.generate_expression_code"
        ) as mock_gen_expr:
            mock_gen_expr.side_effect = [
                ("MOV x0, #2\n", 16),
                ("MOV x0, #3\n", 16),
            ]

            code, _ = generate_binary_op_code(
                expr, self.func_name, label_counter, self.var_offsets, self.next_offset
            )

            assert "// Unsupported operator: **" in code

    def test_nested_binary_operations(self):
        """Test nested binary operations are handled correctly."""
        expr = {
            "type": "BINARY_OP",
            "operator": "+",
            "left": {
                "type": "BINARY_OP",
                "operator": "*",
                "left": {"type": "NUMBER", "value": 2},
                "right": {"type": "NUMBER", "value": 3},
            },
            "right": {"type": "NUMBER", "value": 4},
        }
        label_counter = {"counter": 0}

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_unary_op_code_package.generate_expression_code_package.generate_binary_op_code_package.generate_expression_code_src.generate_expression_code"
        ) as mock_gen_expr:
            mock_gen_expr.side_effect = [
                ("MOV x0, #2\nMOV x1, x0\nMOV x0, #3\nMUL x0, x1, x0\n", 16),
                ("MOV x0, #4\n", 16),
            ]

            code, next_offset = generate_binary_op_code(
                expr, self.func_name, label_counter, self.var_offsets, self.next_offset
            )

            assert "MUL x0, x1, x0" in code
            assert "ADD x0, x1, x0" in code
            assert next_offset == 16

    def test_offset_propagation(self):
        """Test that next_offset is properly propagated through calls."""
        expr = {
            "type": "BINARY_OP",
            "operator": "+",
            "left": {"type": "NUMBER", "value": 1},
            "right": {"type": "NUMBER", "value": 2},
        }
        label_counter = {"counter": 0}

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_unary_op_code_package.generate_expression_code_package.generate_binary_op_code_package.generate_expression_code_src.generate_expression_code"
        ) as mock_gen_expr:
            mock_gen_expr.side_effect = [
                ("MOV x0, #1\n", 24),
                ("MOV x0, #2\n", 32),
            ]

            code, next_offset = generate_binary_op_code(
                expr, self.func_name, label_counter, self.var_offsets, self.next_offset
            )

            assert next_offset == 32


class TestGenerateBinaryInstruction:
    """Test suite for _generate_binary_instruction helper function."""

    def test_all_supported_operators(self):
        """Test all supported operators map to correct instructions."""
        operator_map = {
            "+": "ADD x0, x1, x0\n",
            "-": "SUB x0, x1, x0\n",
            "*": "MUL x0, x1, x0\n",
            "/": "SDIV x0, x1, x0\n",
            "==": "CMP x1, x0\nCSET x0, EQ\n",
            "!=": "CMP x1, x0\nCSET x0, NE\n",
            "<": "CMP x1, x0\nCSET x0, LT\n",
            ">": "CMP x1, x0\nCSET x0, GT\n",
            "<=": "CMP x1, x0\nCSET x0, LE\n",
            ">=": "CMP x1, x0\nCSET x0, GE\n",
            "&": "AND x0, x1, x0\n",
            "|": "ORR x0, x1, x0\n",
            "^": "EOR x0, x1, x0\n",
            "<<": "LSL x0, x1, x0\n",
            ">>": "ASR x0, x1, x0\n",
        }

        for operator, expected in operator_map.items():
            result = _generate_binary_instruction(operator)
            assert result == expected, f"Failed for operator: {operator}"

    def test_unsupported_operator_returns_comment(self):
        """Test unsupported operator returns comment string."""
        result = _generate_binary_instruction("**")
        assert "// Unsupported operator: **" in result

    def test_unknown_operator_returns_comment(self):
        """Test unknown operator returns comment with operator name."""
        result = _generate_binary_instruction("%%")
        assert "// Unsupported operator: %%" in result


class TestGenerateLogicalAnd:
    """Test suite for _generate_logical_and helper function."""

    def test_generates_correct_labels(self):
        """Test logical and generates unique labels."""
        label_counter = {"counter": 10}

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_unary_op_code_package.generate_expression_code_package.generate_binary_op_code_package.generate_expression_code_src.generate_expression_code"
        ) as mock_gen_expr:
            mock_gen_expr.side_effect = [
                ("MOV x0, #1\n", 16),
                ("MOV x0, #1\n", 16),
            ]

            code, _ = _generate_logical_and(
                {"type": "NUMBER", "value": 1},
                {"type": "NUMBER", "value": 1},
                "my_func",
                label_counter,
                {},
                16,
            )

            assert "L_my_func_end_10" in code
            assert label_counter["counter"] == 11


class TestGenerateLogicalOr:
    """Test suite for _generate_logical_or helper function."""

    def test_generates_correct_labels(self):
        """Test logical or generates unique labels."""
        label_counter = {"counter": 20}

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_unary_op_code_package.generate_expression_code_package.generate_binary_op_code_package.generate_expression_code_src.generate_expression_code"
        ) as mock_gen_expr:
            mock_gen_expr.side_effect = [
                ("MOV x0, #0\n", 16),
                ("MOV x0, #1\n", 16),
            ]

            code, _ = _generate_logical_or(
                {"type": "NUMBER", "value": 0},
                {"type": "NUMBER", "value": 1},
                "my_func",
                label_counter,
                {},
                16,
            )

            assert "L_my_func_end_20" in code
            assert label_counter["counter"] == 21

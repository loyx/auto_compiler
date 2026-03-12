"""Unit tests for generate_binop_code function."""
import pytest
from unittest.mock import patch

# Relative import from the same package
from .generate_binop_code_src import generate_binop_code


class TestGenerateBinopCode:
    """Test cases for generate_binop_code function."""

    def test_arithmetic_add(self):
        """Test addition operator."""
        expr = {
            "op": "+",
            "left": {"type": "LITERAL", "value": 5},
            "right": {"type": "LITERAL", "value": 3}
        }

        with patch('generate_expression_code_package.generate_expression_code_src.generate_expression_code') as mock_gen:
            mock_gen.side_effect = ["    mov x0, #5", "    mov x0, #3"]

            result = generate_binop_code(expr, "test_func", {})

            assert "    mov x0, #5" in result
            assert "    mov x1, x0" in result
            assert "    mov x0, #3" in result
            assert "    mov x2, x0" in result
            assert "    mov x0, x1" in result
            assert "    add x0, x0, x2" in result

    def test_arithmetic_subtract(self):
        """Test subtraction operator."""
        expr = {
            "op": "-",
            "left": {"type": "LITERAL", "value": 10},
            "right": {"type": "LITERAL", "value": 4}
        }

        with patch('generate_expression_code_package.generate_expression_code_src.generate_expression_code') as mock_gen:
            mock_gen.side_effect = ["    mov x0, #10", "    mov x0, #4"]

            result = generate_binop_code(expr, "test_func", {})

            assert "    sub x0, x0, x2" in result

    def test_arithmetic_multiply(self):
        """Test multiplication operator."""
        expr = {
            "op": "*",
            "left": {"type": "LITERAL", "value": 6},
            "right": {"type": "LITERAL", "value": 7}
        }

        with patch('generate_expression_code_package.generate_expression_code_src.generate_expression_code') as mock_gen:
            mock_gen.side_effect = ["    mov x0, #6", "    mov x0, #7"]

            result = generate_binop_code(expr, "test_func", {})

            assert "    mul x0, x0, x2" in result

    def test_arithmetic_divide(self):
        """Test division operator."""
        expr = {
            "op": "/",
            "left": {"type": "LITERAL", "value": 20},
            "right": {"type": "LITERAL", "value": 4}
        }

        with patch('generate_expression_code_package.generate_expression_code_src.generate_expression_code') as mock_gen:
            mock_gen.side_effect = ["    mov x0, #20", "    mov x0, #4"]

            result = generate_binop_code(expr, "test_func", {})

            assert "    sdiv x0, x0, x2" in result

    def test_comparison_equal(self):
        """Test equality operator."""
        expr = {
            "op": "==",
            "left": {"type": "LITERAL", "value": 5},
            "right": {"type": "LITERAL", "value": 5}
        }

        with patch('generate_expression_code_package.generate_expression_code_src.generate_expression_code') as mock_gen:
            mock_gen.side_effect = ["    mov x0, #5", "    mov x0, #5"]

            result = generate_binop_code(expr, "test_func", {})

            assert "    cmp x0, x2" in result
            assert "    cset x0, eq" in result

    def test_comparison_not_equal(self):
        """Test inequality operator."""
        expr = {
            "op": "!=",
            "left": {"type": "LITERAL", "value": 5},
            "right": {"type": "LITERAL", "value": 3}
        }

        with patch('generate_expression_code_package.generate_expression_code_src.generate_expression_code') as mock_gen:
            mock_gen.side_effect = ["    mov x0, #5", "    mov x0, #3"]

            result = generate_binop_code(expr, "test_func", {})

            assert "    cmp x0, x2" in result
            assert "    cset x0, ne" in result

    def test_comparison_less_than(self):
        """Test less than operator."""
        expr = {
            "op": "<",
            "left": {"type": "LITERAL", "value": 3},
            "right": {"type": "LITERAL", "value": 5}
        }

        with patch('generate_expression_code_package.generate_expression_code_src.generate_expression_code') as mock_gen:
            mock_gen.side_effect = ["    mov x0, #3", "    mov x0, #5"]

            result = generate_binop_code(expr, "test_func", {})

            assert "    cmp x0, x2" in result
            assert "    cset x0, lt" in result

    def test_comparison_greater_than(self):
        """Test greater than operator."""
        expr = {
            "op": ">",
            "left": {"type": "LITERAL", "value": 7},
            "right": {"type": "LITERAL", "value": 3}
        }

        with patch('generate_expression_code_package.generate_expression_code_src.generate_expression_code') as mock_gen:
            mock_gen.side_effect = ["    mov x0, #7", "    mov x0, #3"]

            result = generate_binop_code(expr, "test_func", {})

            assert "    cmp x0, x2" in result
            assert "    cset x0, gt" in result

    def test_comparison_less_equal(self):
        """Test less than or equal operator."""
        expr = {
            "op": "<=",
            "left": {"type": "LITERAL", "value": 5},
            "right": {"type": "LITERAL", "value": 5}
        }

        with patch('generate_expression_code_package.generate_expression_code_src.generate_expression_code') as mock_gen:
            mock_gen.side_effect = ["    mov x0, #5", "    mov x0, #5"]

            result = generate_binop_code(expr, "test_func", {})

            assert "    cmp x0, x2" in result
            assert "    cset x0, le" in result

    def test_comparison_greater_equal(self):
        """Test greater than or equal operator."""
        expr = {
            "op": ">=",
            "left": {"type": "LITERAL", "value": 7},
            "right": {"type": "LITERAL", "value": 5}
        }

        with patch('generate_expression_code_package.generate_expression_code_src.generate_expression_code') as mock_gen:
            mock_gen.side_effect = ["    mov x0, #7", "    mov x0, #5"]

            result = generate_binop_code(expr, "test_func", {})

            assert "    cmp x0, x2" in result
            assert "    cset x0, ge" in result

    def test_missing_op_field(self):
        """Test error when 'op' field is missing."""
        expr = {
            "left": {"type": "LITERAL", "value": 5},
            "right": {"type": "LITERAL", "value": 3}
        }

        with pytest.raises(ValueError) as exc_info:
            generate_binop_code(expr, "test_func", {})

        assert "Missing 'op' field" in str(exc_info.value)
        assert "test_func" in str(exc_info.value)

    def test_missing_left_field(self):
        """Test error when 'left' field is missing."""
        expr = {
            "op": "+",
            "right": {"type": "LITERAL", "value": 3}
        }

        with pytest.raises(ValueError) as exc_info:
            generate_binop_code(expr, "test_func", {})

        assert "Missing 'left' field" in str(exc_info.value)
        assert "test_func" in str(exc_info.value)

    def test_missing_right_field(self):
        """Test error when 'right' field is missing."""
        expr = {
            "op": "+",
            "left": {"type": "LITERAL", "value": 5}
        }

        with pytest.raises(ValueError) as exc_info:
            generate_binop_code(expr, "test_func", {})

        assert "Missing 'right' field" in str(exc_info.value)
        assert "test_func" in str(exc_info.value)

    def test_unsupported_operator(self):
        """Test error for unsupported operator."""
        expr = {
            "op": "%",
            "left": {"type": "LITERAL", "value": 5},
            "right": {"type": "LITERAL", "value": 3}
        }

        with patch('generate_expression_code_package.generate_expression_code_src.generate_expression_code') as mock_gen:
            mock_gen.side_effect = ["    mov x0, #5", "    mov x0, #3"]

            with pytest.raises(ValueError) as exc_info:
                generate_binop_code(expr, "test_func", {})

            assert "Unsupported operator '%'" in str(exc_info.value)
            assert "test_func" in str(exc_info.value)

    def test_nested_expressions(self):
        """Test with nested binary operations."""
        expr = {
            "op": "+",
            "left": {
                "op": "*",
                "left": {"type": "LITERAL", "value": 2},
                "right": {"type": "LITERAL", "value": 3}
            },
            "right": {"type": "LITERAL", "value": 4}
        }

        with patch('generate_expression_code_package.generate_expression_code_src.generate_expression_code') as mock_gen:
            mock_gen.side_effect = [
                "    mov x0, #2\n    mov x1, x0\n    mov x0, #3\n    mov x2, x0\n    mov x0, x1\n    mul x0, x0, x2",
                "    mov x0, #4"
            ]

            result = generate_binop_code(expr, "test_func", {})

            assert mock_gen.call_count == 2
            assert "    mul x0, x0, x2" in result
            assert "    add x0, x0, x2" in result

    def test_var_operands(self):
        """Test with variable operands."""
        expr = {
            "op": "+",
            "left": {"type": "VAR", "name": "x"},
            "right": {"type": "VAR", "name": "y"}
        }

        var_offsets = {"x": 0, "y": 1}

        with patch('generate_expression_code_package.generate_expression_code_src.generate_expression_code') as mock_gen:
            mock_gen.side_effect = ["    ldr x0, [sp, #0]", "    ldr x0, [sp, #8]"]

            result = generate_binop_code(expr, "test_func", var_offsets)

            assert "    ldr x0, [sp, #0]" in result
            assert "    ldr x0, [sp, #8]" in result
            assert "    add x0, x0, x2" in result

    def test_mixed_operands(self):
        """Test with mixed literal and variable operands."""
        expr = {
            "op": "-",
            "left": {"type": "VAR", "name": "count"},
            "right": {"type": "LITERAL", "value": 1}
        }

        var_offsets = {"count": 0}

        with patch('generate_expression_code_package.generate_expression_code_src.generate_expression_code') as mock_gen:
            mock_gen.side_effect = ["    ldr x0, [sp, #0]", "    mov x0, #1"]

            result = generate_binop_code(expr, "test_func", var_offsets)

            assert "    ldr x0, [sp, #0]" in result
            assert "    mov x0, #1" in result
            assert "    sub x0, x0, x2" in result

    def test_code_order(self):
        """Test that assembly code is in correct order."""
        expr = {
            "op": "+",
            "left": {"type": "LITERAL", "value": 1},
            "right": {"type": "LITERAL", "value": 2}
        }

        with patch('generate_expression_code_package.generate_expression_code_src.generate_expression_code') as mock_gen:
            mock_gen.side_effect = ["    LEFT_CODE", "    RIGHT_CODE"]

            result = generate_binop_code(expr, "test_func", {})

            lines = result.split('\n')
            assert lines[0] == "    LEFT_CODE"
            assert lines[1] == "    mov x1, x0"
            assert lines[2] == "    RIGHT_CODE"
            assert lines[3] == "    mov x2, x0"
            assert lines[4] == "    mov x0, x1"
            assert lines[5] == "    add x0, x0, x2"

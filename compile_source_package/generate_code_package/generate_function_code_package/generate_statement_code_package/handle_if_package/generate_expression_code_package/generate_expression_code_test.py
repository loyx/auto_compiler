# -*- coding: utf-8 -*-
"""Unit tests for generate_expression_code function."""

import pytest
from .generate_expression_code_src import generate_expression_code


class TestGenerateExpressionCode:
    """Test cases for generate_expression_code function."""

    def test_literal_positive_value(self):
        """Test LITERAL expression with positive integer value."""
        expr = {"type": "LITERAL", "value": 42}
        var_offsets = {}
        next_offset = 0
        
        code, updated_offset, result_reg = generate_expression_code(expr, var_offsets, next_offset)
        
        assert code == "    mov w0, #42\n"
        assert updated_offset == 0
        assert result_reg == "w0"

    def test_literal_zero_value(self):
        """Test LITERAL expression with zero value."""
        expr = {"type": "LITERAL", "value": 0}
        var_offsets = {}
        next_offset = 0
        
        code, updated_offset, result_reg = generate_expression_code(expr, var_offsets, next_offset)
        
        assert code == "    mov w0, #0\n"
        assert updated_offset == 0
        assert result_reg == "w0"

    def test_literal_negative_value(self):
        """Test LITERAL expression with negative integer value."""
        expr = {"type": "LITERAL", "value": -100}
        var_offsets = {}
        next_offset = 0
        
        code, updated_offset, result_reg = generate_expression_code(expr, var_offsets, next_offset)
        
        assert code == "    mov w0, #-100\n"
        assert updated_offset == 0
        assert result_reg == "w0"

    def test_ident_defined_variable(self):
        """Test IDENT expression with defined variable."""
        expr = {"type": "IDENT", "name": "x"}
        var_offsets = {"x": 8}
        next_offset = 16
        
        code, updated_offset, result_reg = generate_expression_code(expr, var_offsets, next_offset)
        
        assert code == "    ldr w0, [sp, #8]\n"
        assert updated_offset == 16
        assert result_reg == "w0"

    def test_ident_undefined_variable_raises_keyerror(self):
        """Test IDENT expression with undefined variable raises KeyError."""
        expr = {"type": "IDENT", "name": "undefined_var"}
        var_offsets = {"x": 8}
        next_offset = 0
        
        with pytest.raises(KeyError, match="Undefined variable: undefined_var"):
            generate_expression_code(expr, var_offsets, next_offset)

    def test_binary_addition(self):
        """Test BINARY expression with addition operator."""
        expr = {
            "type": "BINARY",
            "operator": "+",
            "left": {"type": "LITERAL", "value": 5},
            "right": {"type": "LITERAL", "value": 3}
        }
        var_offsets = {}
        next_offset = 0
        
        code, updated_offset, result_reg = generate_expression_code(expr, var_offsets, next_offset)
        
        assert "mov w0, #5" in code
        assert "mov w0, #3" in code
        assert "add w0, w0, w0" in code
        assert updated_offset == 0
        assert result_reg == "w0"

    def test_binary_subtraction(self):
        """Test BINARY expression with subtraction operator."""
        expr = {
            "type": "BINARY",
            "operator": "-",
            "left": {"type": "LITERAL", "value": 10},
            "right": {"type": "LITERAL", "value": 4}
        }
        var_offsets = {}
        next_offset = 0
        
        code, updated_offset, result_reg = generate_expression_code(expr, var_offsets, next_offset)
        
        assert "sub w0, w0, w0" in code
        assert result_reg == "w0"

    def test_binary_multiplication(self):
        """Test BINARY expression with multiplication operator."""
        expr = {
            "type": "BINARY",
            "operator": "*",
            "left": {"type": "LITERAL", "value": 6},
            "right": {"type": "LITERAL", "value": 7}
        }
        var_offsets = {}
        next_offset = 0
        
        code, updated_offset, result_reg = generate_expression_code(expr, var_offsets, next_offset)
        
        assert "mul w0, w0, w0" in code
        assert result_reg == "w0"

    def test_binary_division(self):
        """Test BINARY expression with division operator."""
        expr = {
            "type": "BINARY",
            "operator": "/",
            "left": {"type": "LITERAL", "value": 20},
            "right": {"type": "LITERAL", "value": 4}
        }
        var_offsets = {}
        next_offset = 0
        
        code, updated_offset, result_reg = generate_expression_code(expr, var_offsets, next_offset)
        
        assert "sdiv w0, w0, w0" in code
        assert result_reg == "w0"

    def test_binary_bitwise_and(self):
        """Test BINARY expression with bitwise AND operator."""
        expr = {
            "type": "BINARY",
            "operator": "&",
            "left": {"type": "LITERAL", "value": 12},
            "right": {"type": "LITERAL", "value": 5}
        }
        var_offsets = {}
        next_offset = 0
        
        code, updated_offset, result_reg = generate_expression_code(expr, var_offsets, next_offset)
        
        assert "and w0, w0, w0" in code
        assert result_reg == "w0"

    def test_binary_bitwise_or(self):
        """Test BINARY expression with bitwise OR operator."""
        expr = {
            "type": "BINARY",
            "operator": "|",
            "left": {"type": "LITERAL", "value": 8},
            "right": {"type": "LITERAL", "value": 4}
        }
        var_offsets = {}
        next_offset = 0
        
        code, updated_offset, result_reg = generate_expression_code(expr, var_offsets, next_offset)
        
        assert "orr w0, w0, w0" in code
        assert result_reg == "w0"

    def test_binary_bitwise_xor(self):
        """Test BINARY expression with bitwise XOR operator."""
        expr = {
            "type": "BINARY",
            "operator": "^",
            "left": {"type": "LITERAL", "value": 15},
            "right": {"type": "LITERAL", "value": 7}
        }
        var_offsets = {}
        next_offset = 0
        
        code, updated_offset, result_reg = generate_expression_code(expr, var_offsets, next_offset)
        
        assert "eor w0, w0, w0" in code
        assert result_reg == "w0"

    def test_binary_comparison_equal(self):
        """Test BINARY expression with equality comparison."""
        expr = {
            "type": "BINARY",
            "operator": "==",
            "left": {"type": "LITERAL", "value": 5},
            "right": {"type": "LITERAL", "value": 5}
        }
        var_offsets = {}
        next_offset = 0
        
        code, updated_offset, result_reg = generate_expression_code(expr, var_offsets, next_offset)
        
        assert "cmp w0, w0" in code
        assert "cset w0, eq" in code
        assert result_reg == "w0"

    def test_binary_comparison_not_equal(self):
        """Test BINARY expression with not equal comparison."""
        expr = {
            "type": "BINARY",
            "operator": "!=",
            "left": {"type": "LITERAL", "value": 5},
            "right": {"type": "LITERAL", "value": 3}
        }
        var_offsets = {}
        next_offset = 0
        
        code, updated_offset, result_reg = generate_expression_code(expr, var_offsets, next_offset)
        
        assert "cset w0, ne" in code
        assert result_reg == "w0"

    def test_binary_comparison_less_than(self):
        """Test BINARY expression with less than comparison."""
        expr = {
            "type": "BINARY",
            "operator": "<",
            "left": {"type": "LITERAL", "value": 3},
            "right": {"type": "LITERAL", "value": 5}
        }
        var_offsets = {}
        next_offset = 0
        
        code, updated_offset, result_reg = generate_expression_code(expr, var_offsets, next_offset)
        
        assert "cset w0, lt" in code
        assert result_reg == "w0"

    def test_binary_comparison_less_equal(self):
        """Test BINARY expression with less than or equal comparison."""
        expr = {
            "type": "BINARY",
            "operator": "<=",
            "left": {"type": "LITERAL", "value": 5},
            "right": {"type": "LITERAL", "value": 5}
        }
        var_offsets = {}
        next_offset = 0
        
        code, updated_offset, result_reg = generate_expression_code(expr, var_offsets, next_offset)
        
        assert "cset w0, le" in code
        assert result_reg == "w0"

    def test_binary_comparison_greater_than(self):
        """Test BINARY expression with greater than comparison."""
        expr = {
            "type": "BINARY",
            "operator": ">",
            "left": {"type": "LITERAL", "value": 10},
            "right": {"type": "LITERAL", "value": 5}
        }
        var_offsets = {}
        next_offset = 0
        
        code, updated_offset, result_reg = generate_expression_code(expr, var_offsets, next_offset)
        
        assert "cset w0, gt" in code
        assert result_reg == "w0"

    def test_binary_comparison_greater_equal(self):
        """Test BINARY expression with greater than or equal comparison."""
        expr = {
            "type": "BINARY",
            "operator": ">=",
            "left": {"type": "LITERAL", "value": 5},
            "right": {"type": "LITERAL", "value": 5}
        }
        var_offsets = {}
        next_offset = 0
        
        code, updated_offset, result_reg = generate_expression_code(expr, var_offsets, next_offset)
        
        assert "cset w0, ge" in code
        assert result_reg == "w0"

    def test_binary_logical_and(self):
        """Test BINARY expression with logical AND operator."""
        expr = {
            "type": "BINARY",
            "operator": "&&",
            "left": {"type": "LITERAL", "value": 1},
            "right": {"type": "LITERAL", "value": 1}
        }
        var_offsets = {}
        next_offset = 0
        
        code, updated_offset, result_reg = generate_expression_code(expr, var_offsets, next_offset)
        
        assert "and w0, w0, w0" in code
        assert result_reg == "w0"

    def test_binary_logical_or(self):
        """Test BINARY expression with logical OR operator."""
        expr = {
            "type": "BINARY",
            "operator": "||",
            "left": {"type": "LITERAL", "value": 0},
            "right": {"type": "LITERAL", "value": 1}
        }
        var_offsets = {}
        next_offset = 0
        
        code, updated_offset, result_reg = generate_expression_code(expr, var_offsets, next_offset)
        
        assert "orr w0, w0, w0" in code
        assert result_reg == "w0"

    def test_binary_with_ident_operands(self):
        """Test BINARY expression with identifier operands."""
        expr = {
            "type": "BINARY",
            "operator": "+",
            "left": {"type": "IDENT", "name": "a"},
            "right": {"type": "IDENT", "name": "b"}
        }
        var_offsets = {"a": 0, "b": 4}
        next_offset = 8
        
        code, updated_offset, result_reg = generate_expression_code(expr, var_offsets, next_offset)
        
        assert "ldr w0, [sp, #0]" in code
        assert "ldr w0, [sp, #4]" in code
        assert "add w0, w0, w0" in code
        assert updated_offset == 8
        assert result_reg == "w0"

    def test_binary_unknown_operator_raises_valueerror(self):
        """Test BINARY expression with unknown operator raises ValueError."""
        expr = {
            "type": "BINARY",
            "operator": "**",
            "left": {"type": "LITERAL", "value": 2},
            "right": {"type": "LITERAL", "value": 3}
        }
        var_offsets = {}
        next_offset = 0
        
        with pytest.raises(ValueError, match="Unknown binary operator: \\*\\*"):
            generate_expression_code(expr, var_offsets, next_offset)

    def test_unary_negation(self):
        """Test UNARY expression with negation operator."""
        expr = {
            "type": "UNARY",
            "operator": "-",
            "operand": {"type": "LITERAL", "value": 42}
        }
        var_offsets = {}
        next_offset = 0
        
        code, updated_offset, result_reg = generate_expression_code(expr, var_offsets, next_offset)
        
        assert "mov w0, #42" in code
        assert "neg w0, w0" in code
        assert updated_offset == 0
        assert result_reg == "w0"

    def test_unary_logical_not(self):
        """Test UNARY expression with logical NOT operator."""
        expr = {
            "type": "UNARY",
            "operator": "!",
            "operand": {"type": "LITERAL", "value": 0}
        }
        var_offsets = {}
        next_offset = 0
        
        code, updated_offset, result_reg = generate_expression_code(expr, var_offsets, next_offset)
        
        assert "cmp w0, #0" in code
        assert "cset w0, eq" in code
        assert result_reg == "w0"

    def test_unary_bitwise_not(self):
        """Test UNARY expression with bitwise NOT operator."""
        expr = {
            "type": "UNARY",
            "operator": "~",
            "operand": {"type": "LITERAL", "value": 5}
        }
        var_offsets = {}
        next_offset = 0
        
        code, updated_offset, result_reg = generate_expression_code(expr, var_offsets, next_offset)
        
        assert "mvn w0, w0" in code
        assert result_reg == "w0"

    def test_unary_with_ident_operand(self):
        """Test UNARY expression with identifier operand."""
        expr = {
            "type": "UNARY",
            "operator": "-",
            "operand": {"type": "IDENT", "name": "x"}
        }
        var_offsets = {"x": 12}
        next_offset = 16
        
        code, updated_offset, result_reg = generate_expression_code(expr, var_offsets, next_offset)
        
        assert "ldr w0, [sp, #12]" in code
        assert "neg w0, w0" in code
        assert updated_offset == 16
        assert result_reg == "w0"

    def test_unary_unknown_operator_raises_valueerror(self):
        """Test UNARY expression with unknown operator raises ValueError."""
        expr = {
            "type": "UNARY",
            "operator": "++",
            "operand": {"type": "LITERAL", "value": 5}
        }
        var_offsets = {}
        next_offset = 0
        
        with pytest.raises(ValueError, match="Unknown unary operator: \\+\\+"):
            generate_expression_code(expr, var_offsets, next_offset)

    def test_unknown_expression_type_raises_valueerror(self):
        """Test unknown expression type raises ValueError."""
        expr = {"type": "UNKNOWN", "value": 42}
        var_offsets = {}
        next_offset = 0
        
        with pytest.raises(ValueError, match="Unknown expression type: UNKNOWN"):
            generate_expression_code(expr, var_offsets, next_offset)

    def test_nested_binary_expression(self):
        """Test nested BINARY expression."""
        expr = {
            "type": "BINARY",
            "operator": "+",
            "left": {
                "type": "BINARY",
                "operator": "*",
                "left": {"type": "LITERAL", "value": 2},
                "right": {"type": "LITERAL", "value": 3}
            },
            "right": {"type": "LITERAL", "value": 4}
        }
        var_offsets = {}
        next_offset = 0
        
        code, updated_offset, result_reg = generate_expression_code(expr, var_offsets, next_offset)
        
        assert "mul w0, w0, w0" in code
        assert "add w0, w0, w0" in code
        assert updated_offset == 0
        assert result_reg == "w0"

    def test_nested_unary_expression(self):
        """Test nested UNARY expression."""
        expr = {
            "type": "UNARY",
            "operator": "-",
            "operand": {
                "type": "UNARY",
                "operator": "-",
                "operand": {"type": "LITERAL", "value": 5}
            }
        }
        var_offsets = {}
        next_offset = 0
        
        code, updated_offset, result_reg = generate_expression_code(expr, var_offsets, next_offset)
        
        assert code.count("neg w0, w0") == 2
        assert updated_offset == 0
        assert result_reg == "w0"

    def test_mixed_nested_expression(self):
        """Test mixed nested expression with binary and unary."""
        expr = {
            "type": "BINARY",
            "operator": "+",
            "left": {
                "type": "UNARY",
                "operator": "-",
                "operand": {"type": "LITERAL", "value": 10}
            },
            "right": {"type": "LITERAL", "value": 5}
        }
        var_offsets = {}
        next_offset = 0
        
        code, updated_offset, result_reg = generate_expression_code(expr, var_offsets, next_offset)
        
        assert "neg w0, w0" in code
        assert "add w0, w0, w0" in code
        assert updated_offset == 0
        assert result_reg == "w0"

    def test_comparison_with_ident_operands(self):
        """Test comparison operation with identifier operands."""
        expr = {
            "type": "BINARY",
            "operator": "==",
            "left": {"type": "IDENT", "name": "x"},
            "right": {"type": "IDENT", "name": "y"}
        }
        var_offsets = {"x": 0, "y": 4}
        next_offset = 8
        
        code, updated_offset, result_reg = generate_expression_code(expr, var_offsets, next_offset)
        
        assert "ldr w0, [sp, #0]" in code
        assert "ldr w0, [sp, #4]" in code
        assert "cmp w0, w0" in code
        assert "cset w0, eq" in code
        assert updated_offset == 8
        assert result_reg == "w0"

    def test_complex_expression_tree(self):
        """Test complex expression tree with multiple levels."""
        expr = {
            "type": "BINARY",
            "operator": "&&",
            "left": {
                "type": "BINARY",
                "operator": ">",
                "left": {"type": "IDENT", "name": "a"},
                "right": {"type": "LITERAL", "value": 0}
            },
            "right": {
                "type": "BINARY",
                "operator": "<",
                "left": {"type": "IDENT", "name": "a"},
                "right": {"type": "LITERAL", "value": 100}
            }
        }
        var_offsets = {"a": 0}
        next_offset = 4
        
        code, updated_offset, result_reg = generate_expression_code(expr, var_offsets, next_offset)
        
        assert "ldr w0, [sp, #0]" in code
        assert "cset w0, gt" in code
        assert "cset w0, lt" in code
        assert "and w0, w0, w0" in code
        assert updated_offset == 4
        assert result_reg == "w0"

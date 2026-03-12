# -*- coding: utf-8 -*-
"""Unit tests for generate_expression_code function."""

import pytest
from .generate_expression_code_src import generate_expression_code


class TestGenerateLiteralCode:
    """Tests for LITERAL expression type."""

    def test_literal_int_positive(self):
        """Test positive integer literal."""
        expr = {"type": "LITERAL", "value": 42}
        result = generate_expression_code(expr, "main", {})
        assert result == "    mov x0, #42"

    def test_literal_int_zero(self):
        """Test zero integer literal."""
        expr = {"type": "LITERAL", "value": 0}
        result = generate_expression_code(expr, "main", {})
        assert result == "    mov x0, #0"

    def test_literal_int_negative(self):
        """Test negative integer literal."""
        expr = {"type": "LITERAL", "value": -10}
        result = generate_expression_code(expr, "main", {})
        assert result == "    mov x0, #-10"

    def test_literal_bool_true(self):
        """Test boolean True literal (converts to 1)."""
        expr = {"type": "LITERAL", "value": True}
        result = generate_expression_code(expr, "main", {})
        assert result == "    mov x0, #1"

    def test_literal_bool_false(self):
        """Test boolean False literal (converts to 0)."""
        expr = {"type": "LITERAL", "value": False}
        result = generate_expression_code(expr, "main", {})
        assert result == "    mov x0, #0"

    def test_literal_none_value(self):
        """Test None literal value raises ValueError."""
        expr = {"type": "LITERAL", "value": None}
        with pytest.raises(ValueError, match="Literal value cannot be None"):
            generate_expression_code(expr, "main", {})

    def test_literal_string_value(self):
        """Test string literal raises ValueError."""
        expr = {"type": "LITERAL", "value": "hello"}
        with pytest.raises(ValueError, match="String literals not supported"):
            generate_expression_code(expr, "main", {})

    def test_literal_float_value(self):
        """Test float literal raises ValueError."""
        expr = {"type": "LITERAL", "value": 3.14}
        with pytest.raises(ValueError, match="Float literals not supported"):
            generate_expression_code(expr, "main", {})

    def test_literal_unsupported_type(self):
        """Test unsupported literal type raises ValueError."""
        expr = {"type": "LITERAL", "value": [1, 2, 3]}
        with pytest.raises(ValueError, match="Unsupported literal type"):
            generate_expression_code(expr, "main", {})


class TestGenerateIdentifierCode:
    """Tests for IDENTIFIER expression type."""

    def test_identifier_defined_variable(self):
        """Test identifier with defined variable in var_offsets."""
        expr = {"type": "IDENTIFIER", "var_name": "x"}
        var_offsets = {"x": 16, "y": 24}
        result = generate_expression_code(expr, "main", var_offsets)
        assert result == "    ldr x0, [sp, #16]"

    def test_identifier_defined_variable_offset_zero(self):
        """Test identifier with offset 0."""
        expr = {"type": "IDENTIFIER", "var_name": "param"}
        var_offsets = {"param": 0}
        result = generate_expression_code(expr, "main", var_offsets)
        assert result == "    ldr x0, [sp, #0]"

    def test_identifier_undefined_variable(self):
        """Test undefined variable generates error comment and mov x0,#0."""
        expr = {"type": "IDENTIFIER", "var_name": "undefined_var"}
        var_offsets = {"x": 16}
        result = generate_expression_code(expr, "main", var_offsets)
        lines = result.split("\n")
        assert len(lines) == 2
        assert "ERROR: undefined variable 'undefined_var'" in lines[0]
        assert lines[1] == "    mov x0, #0"

    def test_identifier_empty_var_offsets(self):
        """Test identifier with empty var_offsets."""
        expr = {"type": "IDENTIFIER", "var_name": "any_var"}
        result = generate_expression_code(expr, "main", {})
        lines = result.split("\n")
        assert len(lines) == 2
        assert "ERROR: undefined variable 'any_var'" in lines[0]


class TestGenerateBinaryOpCode:
    """Tests for BINARY_OP expression type."""

    def test_binary_op_add(self):
        """Test ADD binary operation."""
        expr = {
            "type": "BINARY_OP",
            "op": "ADD",
            "left": {"type": "LITERAL", "value": 5},
            "right": {"type": "LITERAL", "value": 3},
        }
        result = generate_expression_code(expr, "main", {})
        lines = result.split("\n")
        assert "    mov x0, #5" in lines
        assert "    mov x1, x0" in lines
        assert "    mov x0, #3" in lines
        assert "    add x0, x1, x0" in lines

    def test_binary_op_sub(self):
        """Test SUB binary operation."""
        expr = {
            "type": "BINARY_OP",
            "op": "SUB",
            "left": {"type": "LITERAL", "value": 10},
            "right": {"type": "LITERAL", "value": 4},
        }
        result = generate_expression_code(expr, "main", {})
        assert "    sub x0, x1, x0" in result

    def test_binary_op_mul(self):
        """Test MUL binary operation."""
        expr = {
            "type": "BINARY_OP",
            "op": "MUL",
            "left": {"type": "LITERAL", "value": 6},
            "right": {"type": "LITERAL", "value": 7},
        }
        result = generate_expression_code(expr, "main", {})
        assert "    mul x0, x1, x0" in result

    def test_binary_op_div(self):
        """Test DIV binary operation."""
        expr = {
            "type": "BINARY_OP",
            "op": "DIV",
            "left": {"type": "LITERAL", "value": 20},
            "right": {"type": "LITERAL", "value": 4},
        }
        result = generate_expression_code(expr, "main", {})
        assert "    udiv x0, x1, x0" in result

    def test_binary_op_mod(self):
        """Test MOD binary operation (udiv + msub)."""
        expr = {
            "type": "BINARY_OP",
            "op": "MOD",
            "left": {"type": "LITERAL", "value": 17},
            "right": {"type": "LITERAL", "value": 5},
        }
        result = generate_expression_code(expr, "main", {})
        lines = result.split("\n")
        assert "    udiv x0, x1, x0" in lines
        assert "    msub x0, x0, x0, x1" in lines

    def test_binary_op_and(self):
        """Test AND binary operation."""
        expr = {
            "type": "BINARY_OP",
            "op": "AND",
            "left": {"type": "LITERAL", "value": 0xFF},
            "right": {"type": "LITERAL", "value": 0x0F},
        }
        result = generate_expression_code(expr, "main", {})
        assert "    and x0, x1, x0" in result

    def test_binary_op_or(self):
        """Test ORR binary operation."""
        expr = {
            "type": "BINARY_OP",
            "op": "ORR",
            "left": {"type": "LITERAL", "value": 0xF0},
            "right": {"type": "LITERAL", "value": 0x0F},
        }
        result = generate_expression_code(expr, "main", {})
        assert "    orr x0, x1, x0" in result

    def test_binary_op_eor(self):
        """Test EOR binary operation."""
        expr = {
            "type": "BINARY_OP",
            "op": "EOR",
            "left": {"type": "LITERAL", "value": 0xAA},
            "right": {"type": "LITERAL", "value": 0x55},
        }
        result = generate_expression_code(expr, "main", {})
        assert "    eor x0, x1, x0" in result

    def test_binary_op_unsupported_operator(self):
        """Test unsupported binary operator raises ValueError."""
        expr = {
            "type": "BINARY_OP",
            "op": "UNKNOWN_OP",
            "left": {"type": "LITERAL", "value": 1},
            "right": {"type": "LITERAL", "value": 2},
        }
        with pytest.raises(ValueError, match="Unsupported binary operator"):
            generate_expression_code(expr, "main", {})

    def test_binary_op_nested_expression(self):
        """Test binary op with nested binary op as operand."""
        expr = {
            "type": "BINARY_OP",
            "op": "ADD",
            "left": {
                "type": "BINARY_OP",
                "op": "MUL",
                "left": {"type": "LITERAL", "value": 2},
                "right": {"type": "LITERAL", "value": 3},
            },
            "right": {"type": "LITERAL", "value": 4},
        }
        result = generate_expression_code(expr, "main", {})
        lines = result.split("\n")
        # Should contain nested mul operation
        assert "    mul x0, x1, x0" in lines
        assert "    add x0, x1, x0" in lines

    def test_binary_op_with_identifier(self):
        """Test binary op with identifier operands."""
        expr = {
            "type": "BINARY_OP",
            "op": "ADD",
            "left": {"type": "IDENTIFIER", "var_name": "x"},
            "right": {"type": "IDENTIFIER", "var_name": "y"},
        }
        var_offsets = {"x": 16, "y": 24}
        result = generate_expression_code(expr, "main", var_offsets)
        lines = result.split("\n")
        assert "    ldr x0, [sp, #16]" in lines
        assert "    ldr x0, [sp, #24]" in lines
        assert "    add x0, x1, x0" in lines


class TestGenerateFunctionCallCode:
    """Tests for FUNCTION_CALL expression type."""

    def test_function_call_no_args(self):
        """Test function call with no arguments."""
        expr = {"type": "FUNCTION_CALL", "func_name": "get_value", "args": []}
        result = generate_expression_code(expr, "main", {})
        lines = result.split("\n")
        assert "    bl get_value" in lines

    def test_function_call_one_arg(self):
        """Test function call with one argument."""
        expr = {
            "type": "FUNCTION_CALL",
            "func_name": "print_num",
            "args": [{"type": "LITERAL", "value": 42}],
        }
        result = generate_expression_code(expr, "main", {})
        lines = result.split("\n")
        assert "    mov x0, #42" in lines
        assert "    mov x1, x0" in lines
        assert "    bl print_num" in lines

    def test_function_call_two_args(self):
        """Test function call with two arguments."""
        expr = {
            "type": "FUNCTION_CALL",
            "func_name": "add",
            "args": [
                {"type": "LITERAL", "value": 5},
                {"type": "LITERAL", "value": 3},
            ],
        }
        result = generate_expression_code(expr, "main", {})
        lines = result.split("\n")
        assert "    mov x0, #5" in lines
        assert "    mov x1, x0" in lines
        assert "    mov x0, #3" in lines
        assert "    mov x2, x0" in lines
        assert "    bl add" in lines

    def test_function_call_eight_args(self):
        """Test function call with maximum 8 arguments."""
        expr = {
            "type": "FUNCTION_CALL",
            "func_name": "multi_arg_func",
            "args": [{"type": "LITERAL", "value": i} for i in range(8)],
        }
        result = generate_expression_code(expr, "main", {})
        lines = result.split("\n")
        # Should have bl instruction
        assert "    bl multi_arg_func" in lines
        # Should not raise error
        assert result is not None

    def test_function_call_nine_args(self):
        """Test function call with more than 8 arguments raises ValueError."""
        expr = {
            "type": "FUNCTION_CALL",
            "func_name": "too_many_args",
            "args": [{"type": "LITERAL", "value": i} for i in range(9)],
        }
        with pytest.raises(ValueError, match="exceeds maximum 8 arguments"):
            generate_expression_code(expr, "main", {})

    def test_function_call_with_identifier_args(self):
        """Test function call with identifier arguments."""
        expr = {
            "type": "FUNCTION_CALL",
            "func_name": "process",
            "args": [
                {"type": "IDENTIFIER", "var_name": "x"},
                {"type": "IDENTIFIER", "var_name": "y"},
            ],
        }
        var_offsets = {"x": 16, "y": 24}
        result = generate_expression_code(expr, "main", var_offsets)
        lines = result.split("\n")
        assert "    ldr x0, [sp, #16]" in lines
        assert "    ldr x0, [sp, #24]" in lines
        assert "    bl process" in lines

    def test_function_call_nested_function_call(self):
        """Test function call with nested function call as argument."""
        expr = {
            "type": "FUNCTION_CALL",
            "func_name": "outer",
            "args": [
                {
                    "type": "FUNCTION_CALL",
                    "func_name": "inner",
                    "args": [{"type": "LITERAL", "value": 10}],
                }
            ],
        }
        result = generate_expression_code(expr, "main", {})
        lines = result.split("\n")
        assert "    bl inner" in lines
        assert "    bl outer" in lines


class TestUnknownExpressionType:
    """Tests for unknown expression type error handling."""

    def test_unknown_expression_type(self):
        """Test unknown expression type raises ValueError."""
        expr = {"type": "UNKNOWN_TYPE", "data": "some_data"}
        with pytest.raises(ValueError, match="Unknown expression type"):
            generate_expression_code(expr, "main", {})

    def test_missing_type_field(self):
        """Test missing type field raises ValueError (treated as None)."""
        expr = {"value": 42}
        with pytest.raises(ValueError, match="Unknown expression type"):
            generate_expression_code(expr, "main", {})

    def test_empty_expression_dict(self):
        """Test empty expression dict raises ValueError."""
        expr = {}
        with pytest.raises(ValueError, match="Unknown expression type"):
            generate_expression_code(expr, "main", {})


class TestEdgeCases:
    """Tests for edge cases and boundary conditions."""

    def test_complex_nested_expression(self):
        """Test complex nested expression with multiple levels."""
        expr = {
            "type": "BINARY_OP",
            "op": "ADD",
            "left": {
                "type": "BINARY_OP",
                "op": "MUL",
                "left": {"type": "LITERAL", "value": 2},
                "right": {
                    "type": "FUNCTION_CALL",
                    "func_name": "get_factor",
                    "args": [{"type": "LITERAL", "value": 5}],
                },
            },
            "right": {"type": "IDENTIFIER", "var_name": "offset"},
        }
        var_offsets = {"offset": 32}
        result = generate_expression_code(expr, "main", var_offsets)
        lines = result.split("\n")
        # Should contain all operations
        assert "    bl get_factor" in lines
        assert "    mul x0, x1, x0" in lines
        assert "    ldr x0, [sp, #32]" in lines
        assert "    add x0, x1, x0" in lines

    def test_function_name_parameter_ignored_for_literals(self):
        """Test func_name parameter doesn't affect literal generation."""
        expr = {"type": "LITERAL", "value": 100}
        result1 = generate_expression_code(expr, "func_a", {})
        result2 = generate_expression_code(expr, "func_b", {})
        assert result1 == result2

    def test_var_offsets_ignored_for_literals(self):
        """Test var_offsets doesn't affect literal generation."""
        expr = {"type": "LITERAL", "value": 50}
        result1 = generate_expression_code(expr, "main", {})
        result2 = generate_expression_code(expr, "main", {"x": 16, "y": 24})
        assert result1 == result2

    def test_boolean_in_binary_op(self):
        """Test boolean literals in binary operations."""
        expr = {
            "type": "BINARY_OP",
            "op": "AND",
            "left": {"type": "LITERAL", "value": True},
            "right": {"type": "LITERAL", "value": False},
        }
        result = generate_expression_code(expr, "main", {})
        lines = result.split("\n")
        assert "    mov x0, #1" in lines
        assert "    mov x0, #0" in lines
        assert "    and x0, x1, x0" in lines

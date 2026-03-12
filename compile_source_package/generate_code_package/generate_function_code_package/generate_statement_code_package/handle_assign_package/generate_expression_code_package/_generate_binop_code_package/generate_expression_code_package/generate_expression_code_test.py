import pytest
from unittest.mock import patch

from .generate_expression_code_src import generate_expression_code


class TestGenerateExpressionCode:
    """Test cases for generate_expression_code dispatcher function."""

    def test_binop_expression_routing(self):
        """Test that BINOP expressions are routed to _generate_binop_code."""
        expr = {
            "type": "BINOP",
            "op": "+",
            "left": {"type": "LITERAL", "value": 1, "literal_type": "int"},
            "right": {"type": "LITERAL", "value": 2, "literal_type": "int"},
        }
        func_name = "test_func"
        var_offsets = {"x": 0}

        with patch("generate_expression_code_package._generate_binop_code_package._generate_binop_code_src._generate_binop_code") as mock_binop:
            mock_binop.return_value = "add x0, x1, x2"

            result = generate_expression_code(expr, func_name, var_offsets)

            mock_binop.assert_called_once_with(expr, func_name, var_offsets)
            assert result == "add x0, x1, x2"

    def test_literal_expression_routing(self):
        """Test that LITERAL expressions are routed to _generate_literal_code."""
        expr = {
            "type": "LITERAL",
            "value": 42,
            "literal_type": "int",
        }
        func_name = "test_func"
        var_offsets = {}

        with patch("._generate_literal_code_package._generate_literal_code_src._generate_literal_code") as mock_literal:
            mock_literal.return_value = "mov x0, #42"

            result = generate_expression_code(expr, func_name, var_offsets)

            mock_literal.assert_called_once_with(expr, func_name, var_offsets)
            assert result == "mov x0, #42"

    def test_var_expression_routing(self):
        """Test that VAR expressions are routed to _generate_var_code."""
        expr = {
            "type": "VAR",
            "name": "x",
        }
        func_name = "test_func"
        var_offsets = {"x": 8}

        with patch("._generate_var_code_package._generate_var_code_src._generate_var_code") as mock_var:
            mock_var.return_value = "ldr x0, [sp, #8]"

            result = generate_expression_code(expr, func_name, var_offsets)

            mock_var.assert_called_once_with(expr, func_name, var_offsets)
            assert result == "ldr x0, [sp, #8]"

    def test_call_expression_routing(self):
        """Test that CALL expressions are routed to _generate_call_code."""
        expr = {
            "type": "CALL",
            "function": "foo",
            "arguments": [],
        }
        func_name = "test_func"
        var_offsets = {}

        with patch("._generate_call_code_package._generate_call_code_src._generate_call_code") as mock_call:
            mock_call.return_value = "bl foo"

            result = generate_expression_code(expr, func_name, var_offsets)

            mock_call.assert_called_once_with(expr, func_name, var_offsets)
            assert result == "bl foo"

    def test_unop_expression_routing(self):
        """Test that UNOP expressions are routed to _generate_unop_code."""
        expr = {
            "type": "UNOP",
            "op": "-",
            "operand": {"type": "VAR", "name": "x"},
        }
        func_name = "test_func"
        var_offsets = {"x": 0}

        with patch("._generate_unop_code_package._generate_unop_code_src._generate_unop_code") as mock_unop:
            mock_unop.return_value = "neg x0, x0"

            result = generate_expression_code(expr, func_name, var_offsets)

            mock_unop.assert_called_once_with(expr, func_name, var_offsets)
            assert result == "neg x0, x0"

    def test_unknown_expression_type_raises_valueerror(self):
        """Test that unknown expression types raise ValueError."""
        expr = {
            "type": "UNKNOWN_TYPE",
        }
        func_name = "test_func"
        var_offsets = {}

        with pytest.raises(ValueError) as exc_info:
            generate_expression_code(expr, func_name, var_offsets)

        assert "Unknown expression type: 'UNKNOWN_TYPE'" in str(exc_info.value)

    def test_empty_expr_dict_raises_keyerror(self):
        """Test that empty expression dict raises KeyError when accessing 'type'."""
        expr = {}
        func_name = "test_func"
        var_offsets = {}

        with pytest.raises(KeyError):
            generate_expression_code(expr, func_name, var_offsets)

    def test_binop_with_nested_expressions(self):
        """Test BINOP with nested expressions to verify recursive structure handling."""
        expr = {
            "type": "BINOP",
            "op": "*",
            "left": {
                "type": "BINOP",
                "op": "+",
                "left": {"type": "LITERAL", "value": 1, "literal_type": "int"},
                "right": {"type": "LITERAL", "value": 2, "literal_type": "int"},
            },
            "right": {"type": "VAR", "name": "x"},
        }
        func_name = "test_func"
        var_offsets = {"x": 16}

        with patch("._generate_binop_code_package._generate_binop_code_src._generate_binop_code") as mock_binop:
            mock_binop.return_value = "mul x0, x1, x2"

            result = generate_expression_code(expr, func_name, var_offsets)

            mock_binop.assert_called_once_with(expr, func_name, var_offsets)
            assert result == "mul x0, x1, x2"

    def test_call_with_arguments(self):
        """Test CALL expression with multiple arguments."""
        expr = {
            "type": "CALL",
            "function": "add",
            "arguments": [
                {"type": "LITERAL", "value": 1, "literal_type": "int"},
                {"type": "LITERAL", "value": 2, "literal_type": "int"},
            ],
        }
        func_name = "test_func"
        var_offsets = {}

        with patch("._generate_call_code_package._generate_call_code_src._generate_call_code") as mock_call:
            mock_call.return_value = "mov x0, #1\nmov x1, #2\nbl add"

            result = generate_expression_code(expr, func_name, var_offsets)

            mock_call.assert_called_once_with(expr, func_name, var_offsets)
            assert result == "mov x0, #1\nmov x1, #2\nbl add"

    def test_unop_logical_not(self):
        """Test UNOP with logical not operator."""
        expr = {
            "type": "UNOP",
            "op": "!",
            "operand": {"type": "VAR", "name": "flag"},
        }
        func_name = "test_func"
        var_offsets = {"flag": 24}

        with patch("._generate_unop_code_package._generate_unop_code_src._generate_unop_code") as mock_unop:
            mock_unop.return_value = "mvn x0, x0"

            result = generate_expression_code(expr, func_name, var_offsets)

            mock_unop.assert_called_once_with(expr, func_name, var_offsets)
            assert result == "mvn x0, x0"

    def test_literal_bool_true(self):
        """Test LITERAL expression with boolean true value."""
        expr = {
            "type": "LITERAL",
            "value": True,
            "literal_type": "bool",
        }
        func_name = "test_func"
        var_offsets = {}

        with patch("._generate_literal_code_package._generate_literal_code_src._generate_literal_code") as mock_literal:
            mock_literal.return_value = "mov x0, #1"

            result = generate_expression_code(expr, func_name, var_offsets)

            mock_literal.assert_called_once_with(expr, func_name, var_offsets)
            assert result == "mov x0, #1"

    def test_literal_bool_false(self):
        """Test LITERAL expression with boolean false value."""
        expr = {
            "type": "LITERAL",
            "value": False,
            "literal_type": "bool",
        }
        func_name = "test_func"
        var_offsets = {}

        with patch("._generate_literal_code_package._generate_literal_code_src._generate_literal_code") as mock_literal:
            mock_literal.return_value = "mov x0, #0"

            result = generate_expression_code(expr, func_name, var_offsets)

            mock_literal.assert_called_once_with(expr, func_name, var_offsets)
            assert result == "mov x0, #0"

    def test_var_offsets_passed_correctly(self):
        """Test that var_offsets dictionary is passed correctly to handlers."""
        expr = {
            "type": "VAR",
            "name": "y",
        }
        func_name = "main"
        var_offsets = {"x": 0, "y": 8, "z": 16}

        with patch("._generate_var_code_package._generate_var_code_src._generate_var_code") as mock_var:
            mock_var.return_value = "ldr x0, [sp, #8]"

            result = generate_expression_code(expr, func_name, var_offsets)

            mock_var.assert_called_once_with(expr, func_name, var_offsets)
            assert result == "ldr x0, [sp, #8]"

    def test_all_expression_types_covered(self):
        """Test that all 5 supported expression types can be dispatched."""
        func_name = "test"
        var_offsets = {}

        expression_types = [
            ("BINOP", {"type": "BINOP", "op": "+", "left": {}, "right": {}}),
            ("LITERAL", {"type": "LITERAL", "value": 0, "literal_type": "int"}),
            ("VAR", {"type": "VAR", "name": "x"}),
            ("CALL", {"type": "CALL", "function": "foo", "arguments": []}),
            ("UNOP", {"type": "UNOP", "op": "-", "operand": {}}),
        ]

        for expr_type, expr in expression_types:
            with patch("._generate_binop_code_package._generate_binop_code_src._generate_binop_code") as mock_binop, \
                 patch("._generate_literal_code_package._generate_literal_code_src._generate_literal_code") as mock_literal, \
                 patch("._generate_var_code_package._generate_var_code_src._generate_var_code") as mock_var, \
                 patch("._generate_call_code_package._generate_call_code_src._generate_call_code") as mock_call, \
                 patch("._generate_unop_code_package._generate_unop_code_src._generate_unop_code") as mock_unop:

                mock_binop.return_value = "binop_code"
                mock_literal.return_value = "literal_code"
                mock_var.return_value = "var_code"
                mock_call.return_value = "call_code"
                mock_unop.return_value = "unop_code"

                result = generate_expression_code(expr, func_name, var_offsets)

                if expr_type == "BINOP":
                    mock_binop.assert_called_once()
                    assert result == "binop_code"
                elif expr_type == "LITERAL":
                    mock_literal.assert_called_once()
                    assert result == "literal_code"
                elif expr_type == "VAR":
                    mock_var.assert_called_once()
                    assert result == "var_code"
                elif expr_type == "CALL":
                    mock_call.assert_called_once()
                    assert result == "call_code"
                elif expr_type == "UNOP":
                    mock_unop.assert_called_once()
                    assert result == "unop_code"

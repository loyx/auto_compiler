"""Unit tests for _handle_binary function."""

from unittest.mock import patch, MagicMock
import pytest

# Import the function under test using relative import
from ._handle_binary_src import _handle_binary


class TestHandleBinaryArithmetic:
    """Test arithmetic binary operators."""

    @patch("._handle_binary_src.generate_expression_code")
    def test_add_operator(self, mock_gen_expr: MagicMock) -> None:
        """Test addition operator generates correct assembly."""
        # Setup: left operand returns x1, right operand returns x2
        mock_gen_expr.side_effect = [
            ("    mov x1, #5\n", 1, "x1"),
            ("    mov x2, #3\n", 1, "x2"),
        ]
        
        expr = {
            "type": "BINARY",
            "op": "+",
            "left": {"type": "LITERAL", "value": 5},
            "right": {"type": "LITERAL", "value": 3},
        }
        
        code, next_offset, result_reg = _handle_binary(expr, {}, 1)
        
        assert "add x0, x1, x2" in code
        assert next_offset == 1
        assert result_reg == "x0"

    @patch("._handle_binary_src.generate_expression_code")
    def test_subtract_operator(self, mock_gen_expr: MagicMock) -> None:
        """Test subtraction operator generates correct assembly."""
        mock_gen_expr.side_effect = [
            ("    mov x1, #10\n", 1, "x1"),
            ("    mov x2, #4\n", 1, "x2"),
        ]
        
        expr = {"type": "BINARY", "op": "-", "left": {"type": "LITERAL", "value": 10}, "right": {"type": "LITERAL", "value": 4}}
        
        code, next_offset, result_reg = _handle_binary(expr, {}, 1)
        
        assert "sub x0, x1, x2" in code
        assert result_reg == "x0"

    @patch("._handle_binary_src.generate_expression_code")
    def test_multiply_operator(self, mock_gen_expr: MagicMock) -> None:
        """Test multiplication operator generates correct assembly."""
        mock_gen_expr.side_effect = [
            ("    mov x1, #6\n", 1, "x1"),
            ("    mov x2, #7\n", 1, "x2"),
        ]
        
        expr = {"type": "BINARY", "op": "*", "left": {"type": "LITERAL", "value": 6}, "right": {"type": "LITERAL", "value": 7}}
        
        code, next_offset, result_reg = _handle_binary(expr, {}, 1)
        
        assert "mul x0, x1, x2" in code
        assert result_reg == "x0"

    @patch("._handle_binary_src.generate_expression_code")
    def test_divide_operator(self, mock_gen_expr: MagicMock) -> None:
        """Test division operator generates correct assembly."""
        mock_gen_expr.side_effect = [
            ("    mov x1, #20\n", 1, "x1"),
            ("    mov x2, #4\n", 1, "x2"),
        ]
        
        expr = {"type": "BINARY", "op": "/", "left": {"type": "LITERAL", "value": 20}, "right": {"type": "LITERAL", "value": 4}}
        
        code, next_offset, result_reg = _handle_binary(expr, {}, 1)
        
        assert "sdiv x0, x1, x2" in code
        assert result_reg == "x0"

    @patch("._handle_binary_src.generate_expression_code")
    def test_left_operand_not_in_x1(self, mock_gen_expr: MagicMock) -> None:
        """Test mov instruction when left result is not in x1."""
        mock_gen_expr.side_effect = [
            ("    ldr x3, [sp, #0]\n", 1, "x3"),
            ("    mov x2, #5\n", 1, "x2"),
        ]
        
        expr = {"type": "BINARY", "op": "+", "left": {"type": "IDENT", "name": "a"}, "right": {"type": "LITERAL", "value": 5}}
        
        code, next_offset, result_reg = _handle_binary(expr, {"a": 0}, 1)
        
        assert "mov x1, x3" in code
        assert "add x0, x1, x2" in code


class TestHandleBinaryComparison:
    """Test comparison binary operators."""

    @patch("._handle_binary_src.generate_expression_code")
    def test_equal_operator(self, mock_gen_expr: MagicMock) -> None:
        """Test equality operator generates cmp and cset eq."""
        mock_gen_expr.side_effect = [
            ("    mov x1, #5\n", 1, "x1"),
            ("    mov x2, #5\n", 1, "x2"),
        ]
        
        expr = {"type": "BINARY", "op": "==", "left": {"type": "LITERAL", "value": 5}, "right": {"type": "LITERAL", "value": 5}}
        
        code, next_offset, result_reg = _handle_binary(expr, {}, 1)
        
        assert "cmp x1, x2" in code
        assert "cset x0, eq" in code
        assert result_reg == "x0"

    @patch("._handle_binary_src.generate_expression_code")
    def test_not_equal_operator(self, mock_gen_expr: MagicMock) -> None:
        """Test inequality operator generates cmp and cset ne."""
        mock_gen_expr.side_effect = [
            ("    mov x1, #5\n", 1, "x1"),
            ("    mov x2, #3\n", 1, "x2"),
        ]
        
        expr = {"type": "BINARY", "op": "!=", "left": {"type": "LITERAL", "value": 5}, "right": {"type": "LITERAL", "value": 3}}
        
        code, next_offset, result_reg = _handle_binary(expr, {}, 1)
        
        assert "cmp x1, x2" in code
        assert "cset x0, ne" in code

    @patch("._handle_binary_src.generate_expression_code")
    def test_less_than_operator(self, mock_gen_expr: MagicMock) -> None:
        """Test less than operator generates cmp and cset lt."""
        mock_gen_expr.side_effect = [
            ("    mov x1, #3\n", 1, "x1"),
            ("    mov x2, #5\n", 1, "x2"),
        ]
        
        expr = {"type": "BINARY", "op": "<", "left": {"type": "LITERAL", "value": 3}, "right": {"type": "LITERAL", "value": 5}}
        
        code, next_offset, result_reg = _handle_binary(expr, {}, 1)
        
        assert "cmp x1, x2" in code
        assert "cset x0, lt" in code

    @patch("._handle_binary_src.generate_expression_code")
    def test_greater_than_operator(self, mock_gen_expr: MagicMock) -> None:
        """Test greater than operator generates cmp and cset gt."""
        mock_gen_expr.side_effect = [
            ("    mov x1, #7\n", 1, "x1"),
            ("    mov x2, #5\n", 1, "x2"),
        ]
        
        expr = {"type": "BINARY", "op": ">", "left": {"type": "LITERAL", "value": 7}, "right": {"type": "LITERAL", "value": 5}}
        
        code, next_offset, result_reg = _handle_binary(expr, {}, 1)
        
        assert "cmp x1, x2" in code
        assert "cset x0, gt" in code

    @patch("._handle_binary_src.generate_expression_code")
    def test_less_than_or_equal_operator(self, mock_gen_expr: MagicMock) -> None:
        """Test <= operator generates cmp and cset le."""
        mock_gen_expr.side_effect = [
            ("    mov x1, #5\n", 1, "x1"),
            ("    mov x2, #5\n", 1, "x2"),
        ]
        
        expr = {"type": "BINARY", "op": "<=", "left": {"type": "LITERAL", "value": 5}, "right": {"type": "LITERAL", "value": 5}}
        
        code, next_offset, result_reg = _handle_binary(expr, {}, 1)
        
        assert "cmp x1, x2" in code
        assert "cset x0, le" in code

    @patch("._handle_binary_src.generate_expression_code")
    def test_greater_than_or_equal_operator(self, mock_gen_expr: MagicMock) -> None:
        """Test >= operator generates cmp and cset ge."""
        mock_gen_expr.side_effect = [
            ("    mov x1, #7\n", 1, "x1"),
            ("    mov x2, #5\n", 1, "x2"),
        ]
        
        expr = {"type": "BINARY", "op": ">=", "left": {"type": "LITERAL", "value": 7}, "right": {"type": "LITERAL", "value": 5}}
        
        code, next_offset, result_reg = _handle_binary(expr, {}, 1)
        
        assert "cmp x1, x2" in code
        assert "cset x0, ge" in code


class TestHandleBinaryLogical:
    """Test logical binary operators with short-circuit evaluation."""

    @patch("._handle_binary_src.generate_expression_code")
    def test_logical_and_shortcircuit_false(self, mock_gen_expr: MagicMock) -> None:
        """Test && short-circuits when left is false (0)."""
        # Left evaluates to 0, right should not be evaluated in short-circuit
        # But in our implementation, both are evaluated - we test the structure
        mock_gen_expr.side_effect = [
            ("    mov x1, #0\n", 1, "x1"),
            ("    mov x2, #1\n", 1, "x2"),
        ]
        
        expr = {"type": "BINARY", "op": "&&", "left": {"type": "LITERAL", "value": 0}, "right": {"type": "LITERAL", "value": 1}}
        
        code, next_offset, result_reg = _handle_binary(expr, {}, 1)
        
        assert "cbz x1, __and_end_1" in code
        assert "__and_end_1:" in code
        assert result_reg == "x0"

    @patch("._handle_binary_src.generate_expression_code")
    def test_logical_and_both_true(self, mock_gen_expr: MagicMock) -> None:
        """Test && when both operands are true."""
        mock_gen_expr.side_effect = [
            ("    mov x1, #1\n", 1, "x1"),
            ("    mov x2, #1\n", 1, "x2"),
        ]
        
        expr = {"type": "BINARY", "op": "&&", "left": {"type": "LITERAL", "value": 1}, "right": {"type": "LITERAL", "value": 1}}
        
        code, next_offset, result_reg = _handle_binary(expr, {}, 1)
        
        assert "cbz x1, __and_end_1" in code
        assert "__and_end_1:" in code
        # Should have mov to x0 if right_reg is not x0
        assert "mov x0, x2" in code

    @patch("._handle_binary_src.generate_expression_code")
    def test_logical_or_shortcircuit_true(self, mock_gen_expr: MagicMock) -> None:
        """Test || short-circuits when left is true (non-zero)."""
        mock_gen_expr.side_effect = [
            ("    mov x1, #1\n", 1, "x1"),
            ("    mov x2, #0\n", 1, "x2"),
        ]
        
        expr = {"type": "BINARY", "op": "||", "left": {"type": "LITERAL", "value": 1}, "right": {"type": "LITERAL", "value": 0}}
        
        code, next_offset, result_reg = _handle_binary(expr, {}, 1)
        
        assert "cbnz x1, __or_end_1" in code
        assert "__or_end_1:" in code
        assert result_reg == "x0"

    @patch("._handle_binary_src.generate_expression_code")
    def test_logical_or_both_false(self, mock_gen_expr: MagicMock) -> None:
        """Test || when both operands are false."""
        mock_gen_expr.side_effect = [
            ("    mov x1, #0\n", 1, "x1"),
            ("    mov x2, #0\n", 1, "x2"),
        ]
        
        expr = {"type": "BINARY", "op": "||", "left": {"type": "LITERAL", "value": 0}, "right": {"type": "LITERAL", "value": 0}}
        
        code, next_offset, result_reg = _handle_binary(expr, {}, 1)
        
        assert "cbnz x1, __or_end_1" in code
        assert "__or_end_1:" in code
        assert "mov x0, x2" in code


class TestHandleBinaryErrors:
    """Test error handling for unsupported operators."""

    @patch("._handle_binary_src.generate_expression_code")
    def test_unsupported_operator_raises_valueerror(self, mock_gen_expr: MagicMock) -> None:
        """Test that unsupported operator raises ValueError."""
        mock_gen_expr.side_effect = [
            ("    mov x1, #5\n", 1, "x1"),
            ("    mov x2, #3\n", 1, "x2"),
        ]
        
        expr = {"type": "BINARY", "op": "**", "left": {"type": "LITERAL", "value": 5}, "right": {"type": "LITERAL", "value": 3}}
        
        with pytest.raises(ValueError, match="Unsupported binary operator: \\*\\*"):
            _handle_binary(expr, {}, 1)

    @patch("._handle_binary_src.generate_expression_code")
    def test_unknown_operator_raises_valueerror(self, mock_gen_expr: MagicMock) -> None:
        """Test that unknown operator raises ValueError with operator name."""
        mock_gen_expr.side_effect = [
            ("    mov x1, #1\n", 1, "x1"),
            ("    mov x2, #1\n", 1, "x2"),
        ]
        
        expr = {"type": "BINARY", "op": "%", "left": {"type": "LITERAL", "value": 1}, "right": {"type": "LITERAL", "value": 1}}
        
        with pytest.raises(ValueError, match="Unsupported binary operator: %"):
            _handle_binary(expr, {}, 1)


class TestHandleBinaryEdgeCases:
    """Test edge cases and boundary conditions."""

    @patch("._handle_binary_src.generate_expression_code")
    def test_nested_binary_expression(self, mock_gen_expr: MagicMock) -> None:
        """Test nested binary expressions are handled via recursive calls."""
        # Simulate nested expression: (5 + 3) * 2
        mock_gen_expr.side_effect = [
            ("    mov x1, #5\n    mov x2, #3\n    add x0, x1, x2\n", 1, "x0"),
            ("    mov x2, #2\n", 1, "x2"),
        ]
        
        expr = {
            "type": "BINARY",
            "op": "*",
            "left": {"type": "BINARY", "op": "+", "left": {"type": "LITERAL", "value": 5}, "right": {"type": "LITERAL", "value": 3}},
            "right": {"type": "LITERAL", "value": 2},
        }
        
        code, next_offset, result_reg = _handle_binary(expr, {}, 1)
        
        assert "mul x0, x1, x2" in code
        assert result_reg == "x0"

    @patch("._handle_binary_src.generate_expression_code")
    def test_empty_code_from_operands(self, mock_gen_expr: MagicMock) -> None:
        """Test handling when operand code is empty."""
        mock_gen_expr.side_effect = [
            ("", 1, "x1"),
            ("", 1, "x2"),
        ]
        
        expr = {"type": "BINARY", "op": "+", "left": {"type": "LITERAL", "value": 1}, "right": {"type": "LITERAL", "value": 2}}
        
        code, next_offset, result_reg = _handle_binary(expr, {}, 1)
        
        # Should still have the add instruction
        assert "add x0, x1, x2" in code

    @patch("._handle_binary_src.generate_expression_code")
    def test_right_operand_in_x0_no_mov_needed(self, mock_gen_expr: MagicMock) -> None:
        """Test no mov needed when right operand already in x0 for logical ops."""
        mock_gen_expr.side_effect = [
            ("    mov x1, #1\n", 1, "x1"),
            ("    mov x0, #1\n", 1, "x0"),
        ]
        
        expr = {"type": "BINARY", "op": "&&", "left": {"type": "LITERAL", "value": 1}, "right": {"type": "LITERAL", "value": 1}}
        
        code, next_offset, result_reg = _handle_binary(expr, {}, 1)
        
        # Should not have unnecessary mov x0, x0
        assert "mov x0, x0" not in code
        assert "__and_end_1:" in code

    @patch("._handle_binary_src.generate_expression_code")
    def test_var_offsets_passed_to_recursive_calls(self, mock_gen_expr: MagicMock) -> None:
        """Test that var_offsets are correctly passed to generate_expression_code."""
        var_offsets = {"x": 0, "y": 1}
        mock_gen_expr.side_effect = [
            ("    ldr x1, [sp, #0]\n", 1, "x1"),
            ("    ldr x2, [sp, #8]\n", 1, "x2"),
        ]
        
        expr = {"type": "BINARY", "op": "+", "left": {"type": "IDENT", "name": "x"}, "right": {"type": "IDENT", "name": "y"}}
        
        _handle_binary(expr, var_offsets, 1)
        
        # Verify generate_expression_code was called with correct var_offsets
        assert mock_gen_expr.call_count == 2
        call_args_list = mock_gen_expr.call_args_list
        assert call_args_list[0][0][1] == var_offsets
        assert call_args_list[1][0][1] == var_offsets

    @patch("._handle_binary_src.generate_expression_code")
    def test_next_offset_propagated_correctly(self, mock_gen_expr: MagicMock) -> None:
        """Test that next_offset is correctly propagated through recursive calls."""
        mock_gen_expr.side_effect = [
            ("    mov x1, #5\n", 2, "x1"),  # left increments offset to 2
            ("    mov x2, #3\n", 3, "x2"),  # right increments offset to 3
        ]
        
        expr = {"type": "BINARY", "op": "+", "left": {"type": "LITERAL", "value": 5}, "right": {"type": "LITERAL", "value": 3}}
        
        code, next_offset, result_reg = _handle_binary(expr, {}, 1)
        
        # next_offset should be 3 (final value from right operand)
        assert next_offset == 3

    @patch("._handle_binary_src.generate_expression_code")
    def test_assembly_code_has_proper_indentation(self, mock_gen_expr: MagicMock) -> None:
        """Test that all assembly lines have 4-space indentation."""
        mock_gen_expr.side_effect = [
            ("    ldr x1, [sp, #0]\n", 1, "x1"),
            ("    mov x2, #5\n", 1, "x2"),
        ]
        
        expr = {"type": "BINARY", "op": "+", "left": {"type": "IDENT", "name": "a"}, "right": {"type": "LITERAL", "value": 5}}
        
        code, next_offset, result_reg = _handle_binary(expr, {"a": 0}, 1)
        
        # Check all non-empty lines have 4-space indent (except labels)
        lines = code.strip().split("\n")
        for line in lines:
            if line and not line.endswith(":"):
                assert line.startswith("    "), f"Line not properly indented: {line}"

# === std / third-party imports ===
import unittest
from unittest.mock import patch
from typing import Dict

# === sub function imports ===
from .handle_return_stmt_src import handle_return_stmt


class TestHandleReturnStmt(unittest.TestCase):
    """Test cases for handle_return_stmt function."""

    def test_return_stmt_with_value_field(self):
        """Test RETURN statement with 'value' field."""
        stmt = {
            "type": "return",
            "value": {"type": "literal", "value": 42}
        }
        var_offsets: Dict[str, int] = {"x": 0}
        next_offset = 5

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_return_stmt_package.handle_return_stmt_src.generate_expression_code"
        ) as mock_gen_expr:
            mock_gen_expr.return_value = ("mov x0, #42", 6)

            code, updated_offset = handle_return_stmt(stmt, var_offsets, next_offset)

            mock_gen_expr.assert_called_once_with(
                {"type": "literal", "value": 42}, var_offsets, next_offset
            )
            self.assertEqual(code, "mov x0, #42\nret")
            self.assertEqual(updated_offset, 6)

    def test_return_stmt_with_expression_field(self):
        """Test RETURN statement with 'expression' field (alias for value)."""
        stmt = {
            "type": "return",
            "expression": {"type": "binary", "op": "+", "left": 1, "right": 2}
        }
        var_offsets: Dict[str, int] = {}
        next_offset = 3

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_return_stmt_package.handle_return_stmt_src.generate_expression_code"
        ) as mock_gen_expr:
            mock_gen_expr.return_value = ("add x0, x1, x2", 4)

            code, updated_offset = handle_return_stmt(stmt, var_offsets, next_offset)

            mock_gen_expr.assert_called_once_with(
                {"type": "binary", "op": "+", "left": 1, "right": 2}, var_offsets, next_offset
            )
            self.assertEqual(code, "add x0, x1, x2\nret")
            self.assertEqual(updated_offset, 4)

    def test_return_stmt_value_takes_precedence_over_expression(self):
        """Test that 'value' field takes precedence when both exist."""
        stmt = {
            "type": "return",
            "value": {"type": "literal", "value": 100},
            "expression": {"type": "literal", "value": 200}
        }
        var_offsets: Dict[str, int] = {}
        next_offset = 1

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_return_stmt_package.handle_return_stmt_src.generate_expression_code"
        ) as mock_gen_expr:
            mock_gen_expr.return_value = ("mov x0, #100", 2)

            code, updated_offset = handle_return_stmt(stmt, var_offsets, next_offset)

            mock_gen_expr.assert_called_once_with(
                {"type": "literal", "value": 100}, var_offsets, next_offset
            )
            self.assertEqual(code, "mov x0, #100\nret")
            self.assertEqual(updated_offset, 2)

    def test_return_stmt_without_value_or_expression(self):
        """Test RETURN statement without value or expression field."""
        stmt = {
            "type": "return"
        }
        var_offsets: Dict[str, int] = {"x": 0}
        next_offset = 5

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_return_stmt_package.handle_return_stmt_src.generate_expression_code"
        ) as mock_gen_expr:
            code, updated_offset = handle_return_stmt(stmt, var_offsets, next_offset)

            mock_gen_expr.assert_not_called()
            self.assertEqual(code, "ret")
            self.assertEqual(updated_offset, next_offset)

    def test_return_stmt_with_none_value(self):
        """Test RETURN statement with explicit None value."""
        stmt = {
            "type": "return",
            "value": None
        }
        var_offsets: Dict[str, int] = {}
        next_offset = 10

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_return_stmt_package.handle_return_stmt_src.generate_expression_code"
        ) as mock_gen_expr:
            code, updated_offset = handle_return_stmt(stmt, var_offsets, next_offset)

            mock_gen_expr.assert_not_called()
            self.assertEqual(code, "ret")
            self.assertEqual(updated_offset, next_offset)

    def test_return_stmt_with_empty_dict_value(self):
        """Test RETURN statement with empty dict as value."""
        stmt = {
            "type": "return",
            "value": {}
        }
        var_offsets: Dict[str, int] = {"a": 0}
        next_offset = 7

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_return_stmt_package.handle_return_stmt_src.generate_expression_code"
        ) as mock_gen_expr:
            mock_gen_expr.return_value = ("nop", 8)

            code, updated_offset = handle_return_stmt(stmt, var_offsets, next_offset)

            mock_gen_expr.assert_called_once_with({}, var_offsets, next_offset)
            self.assertEqual(code, "nop\nret")
            self.assertEqual(updated_offset, 8)

    def test_return_stmt_preserves_var_offsets(self):
        """Test that var_offsets is passed through unchanged to generate_expression_code."""
        stmt = {
            "type": "return",
            "value": {"type": "variable", "name": "result"}
        }
        var_offsets: Dict[str, int] = {"result": 0, "temp": 1, "data": 2}
        next_offset = 15

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_return_stmt_package.handle_return_stmt_src.generate_expression_code"
        ) as mock_gen_expr:
            mock_gen_expr.return_value = ("ldr x0, [sp, #0]", 16)

            handle_return_stmt(stmt, var_offsets, next_offset)

            mock_gen_expr.assert_called_once()
            call_args = mock_gen_expr.call_args
            self.assertEqual(call_args[0][1], var_offsets)

    def test_return_stmt_next_offset_updated_correctly(self):
        """Test that next_offset is updated by generate_expression_code return value."""
        stmt = {
            "type": "return",
            "value": {"type": "call", "func": "compute"}
        }
        var_offsets: Dict[str, int] = {}
        next_offset = 20

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_return_stmt_package.handle_return_stmt_src.generate_expression_code"
        ) as mock_gen_expr:
            mock_gen_expr.return_value = ("bl compute", 25)

            _, updated_offset = handle_return_stmt(stmt, var_offsets, next_offset)

            self.assertEqual(updated_offset, 25)

    def test_return_stmt_multiple_expression_lines(self):
        """Test RETURN with expression that generates multiple code lines."""
        stmt = {
            "type": "return",
            "value": {"type": "complex", "expr": "a + b * c"}
        }
        var_offsets: Dict[str, int] = {"a": 0, "b": 1, "c": 2}
        next_offset = 10

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_return_stmt_package.handle_return_stmt_src.generate_expression_code"
        ) as mock_gen_expr:
            mock_gen_expr.return_value = ("ldr x1, [sp, #0]\nldr x2, [sp, #1]\nmul x0, x1, x2", 13)

            code, updated_offset = handle_return_stmt(stmt, var_offsets, next_offset)

            expected_code = "ldr x1, [sp, #0]\nldr x2, [sp, #1]\nmul x0, x1, x2\nret"
            self.assertEqual(code, expected_code)
            self.assertEqual(updated_offset, 13)

    def test_return_stmt_empty_var_offsets(self):
        """Test RETURN statement with empty var_offsets."""
        stmt = {
            "type": "return",
            "value": {"type": "literal", "value": 0}
        }
        var_offsets: Dict[str, int] = {}
        next_offset = 0

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_return_stmt_package.handle_return_stmt_src.generate_expression_code"
        ) as mock_gen_expr:
            mock_gen_expr.return_value = ("mov x0, #0", 1)

            code, updated_offset = handle_return_stmt(stmt, var_offsets, next_offset)

            mock_gen_expr.assert_called_once_with(
                {"type": "literal", "value": 0}, {}, 0
            )
            self.assertEqual(code, "mov x0, #0\nret")
            self.assertEqual(updated_offset, 1)


if __name__ == "__main__":
    unittest.main()

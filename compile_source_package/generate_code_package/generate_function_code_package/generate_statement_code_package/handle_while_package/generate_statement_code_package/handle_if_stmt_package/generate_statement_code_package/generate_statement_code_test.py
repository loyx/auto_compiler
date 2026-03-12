import unittest
from unittest.mock import patch, MagicMock

from .generate_statement_code_src import generate_statement_code, _handle_assign, _handle_return, _handle_expr_stmt


class TestGenerateStatementCode(unittest.TestCase):
    """Test cases for generate_statement_code function."""

    @patch('generate_statement_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_if_stmt_package.generate_statement_code_package.generate_statement_code_src.generate_expression_code')
    def test_assign_statement(self, mock_gen_expr: MagicMock) -> None:
        """Test assignment statement generates correct assembly code."""
        stmt = {"type": "assign", "target": "x", "value": {"type": "literal", "value": 5}}
        var_offsets = {"x": 0}
        next_offset = 8
        
        mock_gen_expr.return_value = ("MOV x0, #5\n", 8)
        
        code, new_offset = generate_statement_code(stmt, "test_func", {}, var_offsets, next_offset)
        
        self.assertIn("MOV x0, #5", code)
        self.assertIn("STR x0, [sp, #0]", code)
        self.assertEqual(new_offset, 8)
        mock_gen_expr.assert_called_once()

    @patch('generate_statement_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_if_stmt_package.generate_statement_code_package.generate_statement_code_src.generate_expression_code')
    def test_assign_statement_multiple_vars(self, mock_gen_expr: MagicMock) -> None:
        """Test assignment with different variable offsets."""
        stmt = {"type": "assign", "target": "y", "value": {"type": "literal", "value": 10}}
        var_offsets = {"x": 0, "y": 8, "z": 16}
        next_offset = 24
        
        mock_gen_expr.return_value = ("MOV x0, #10\n", 24)
        
        code, new_offset = generate_statement_code(stmt, "test_func", {}, var_offsets, next_offset)
        
        self.assertIn("STR x0, [sp, #8]", code)
        self.assertEqual(new_offset, 24)

    @patch('generate_statement_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_if_stmt_package.generate_statement_code_package.generate_statement_code_src.generate_expression_code')
    def test_return_statement_with_value(self, mock_gen_expr: MagicMock) -> None:
        """Test return statement with a value."""
        stmt = {"type": "return", "return_value": {"type": "literal", "value": 42}}
        next_offset = 8
        
        mock_gen_expr.return_value = ("MOV x0, #42\n", 8)
        
        code, new_offset = generate_statement_code(stmt, "test_func", {}, {}, next_offset)
        
        self.assertEqual(code, "MOV x0, #42\n")
        self.assertEqual(new_offset, 8)
        mock_gen_expr.assert_called_once()

    @patch('generate_statement_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_if_stmt_package.generate_statement_code_package.generate_statement_code_src.generate_expression_code')
    def test_return_statement_with_value_key(self, mock_gen_expr: MagicMock) -> None:
        """Test return statement using 'value' key instead of 'return_value'."""
        stmt = {"type": "return", "value": {"type": "literal", "value": 99}}
        next_offset = 8
        
        mock_gen_expr.return_value = ("MOV x0, #99\n", 8)
        
        code, new_offset = generate_statement_code(stmt, "test_func", {}, {}, next_offset)
        
        self.assertEqual(code, "MOV x0, #99\n")
        self.assertEqual(new_offset, 8)

    def test_return_statement_no_value(self) -> None:
        """Test return statement without a value (void return)."""
        stmt = {"type": "return"}
        next_offset = 8
        
        code, new_offset = generate_statement_code(stmt, "test_func", {}, {}, next_offset)
        
        self.assertEqual(code, "")
        self.assertEqual(new_offset, 8)

    @patch('generate_statement_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_if_stmt_package.generate_statement_code_package.generate_statement_code_src.generate_expression_code')
    def test_expr_stmt(self, mock_gen_expr: MagicMock) -> None:
        """Test expression statement generates code and discards result."""
        stmt = {"type": "expr_stmt", "expression": {"type": "binary", "op": "+", "left": 1, "right": 2}}
        next_offset = 8
        
        mock_gen_expr.return_value = ("ADD x0, x1, x2\n", 8)
        
        code, new_offset = generate_statement_code(stmt, "test_func", {}, {}, next_offset)
        
        self.assertEqual(code, "ADD x0, x1, x2\n")
        self.assertEqual(new_offset, 8)
        mock_gen_expr.assert_called_once()

    @patch('generate_statement_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_if_stmt_package.generate_statement_code_package.generate_statement_code_src.handle_if_stmt')
    def test_if_statement(self, mock_handle_if: MagicMock) -> None:
        """Test if statement delegates to handle_if_stmt."""
        stmt = {
            "type": "if",
            "condition": {"type": "binary", "op": "==", "left": 1, "right": 2},
            "then_body": [{"type": "assign", "target": "x", "value": {"type": "literal", "value": 1}}],
            "else_body": []
        }
        label_counter = {"if_else": 0, "if_end": 0}
        var_offsets = {"x": 0}
        next_offset = 8
        
        expected_code = "cbz x0, test_func_if_else_0\n...test_func_if_else_0:\n"
        mock_handle_if.return_value = (expected_code, 16)
        
        code, new_offset = generate_statement_code(stmt, "test_func", label_counter, var_offsets, next_offset)
        
        self.assertEqual(code, expected_code)
        self.assertEqual(new_offset, 16)
        mock_handle_if.assert_called_once_with(stmt, "test_func", label_counter, var_offsets, next_offset)

    @patch('generate_statement_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_if_stmt_package.generate_statement_code_package.generate_statement_code_src.handle_while_stmt')
    def test_while_statement(self, mock_handle_while: MagicMock) -> None:
        """Test while statement delegates to handle_while_stmt."""
        stmt = {
            "type": "while",
            "condition": {"type": "binary", "op": "<", "left": 1, "right": 10},
            "body": [{"type": "assign", "target": "i", "value": {"type": "binary", "op": "+", "left": "i", "right": 1}}]
        }
        label_counter = {"while_cond": 0, "while_end": 0}
        var_offsets = {"i": 0}
        next_offset = 8
        
        expected_code = "test_func_while_cond_0:\n...cbz x0, test_func_while_end_0\n...b test_func_while_cond_0\ntest_func_while_end_0:\n"
        mock_handle_while.return_value = (expected_code, 24)
        
        code, new_offset = generate_statement_code(stmt, "test_func", label_counter, var_offsets, next_offset)
        
        self.assertEqual(code, expected_code)
        self.assertEqual(new_offset, 24)
        mock_handle_while.assert_called_once_with(stmt, "test_func", label_counter, var_offsets, next_offset)

    def test_unknown_statement_type(self) -> None:
        """Test that unknown statement type raises ValueError."""
        stmt = {"type": "unknown_type"}
        
        with self.assertRaises(ValueError) as context:
            generate_statement_code(stmt, "test_func", {}, {}, 8)
        
        self.assertIn("Unknown statement type: unknown_type", str(context.exception))

    @patch('generate_statement_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_if_stmt_package.generate_statement_code_package.generate_statement_code_src.generate_expression_code')
    def test_handle_assign_helper(self, mock_gen_expr: MagicMock) -> None:
        """Test _handle_assign helper function directly."""
        stmt = {"type": "assign", "target": "x", "value": {"type": "literal", "value": 5}}
        var_offsets = {"x": 16}
        next_offset = 24
        
        mock_gen_expr.return_value = ("MOV x0, #5\n", 24)
        
        code, new_offset = _handle_assign(stmt, var_offsets, next_offset)
        
        self.assertIn("MOV x0, #5", code)
        self.assertIn("STR x0, [sp, #16]", code)
        self.assertEqual(new_offset, 24)
        mock_gen_expr.assert_called_once_with({"type": "literal", "value": 5}, var_offsets, 24)

    def test_handle_return_helper_no_value(self) -> None:
        """Test _handle_return helper with no return value."""
        stmt = {"type": "return"}
        next_offset = 8
        
        code, new_offset = _handle_return(stmt, next_offset)
        
        self.assertEqual(code, "")
        self.assertEqual(new_offset, 8)

    @patch('generate_statement_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_if_stmt_package.generate_statement_code_package.generate_statement_code_src.generate_expression_code')
    def test_handle_return_helper_with_return_value(self, mock_gen_expr: MagicMock) -> None:
        """Test _handle_return helper with return_value key."""
        stmt = {"type": "return", "return_value": {"type": "literal", "value": 42}}
        next_offset = 8
        
        mock_gen_expr.return_value = ("MOV x0, #42\n", 8)
        
        code, new_offset = _handle_return(stmt, next_offset)
        
        self.assertEqual(code, "MOV x0, #42\n")
        self.assertEqual(new_offset, 8)
        mock_gen_expr.assert_called_once_with({"type": "literal", "value": 42}, {}, 8)

    @patch('generate_statement_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_if_stmt_package.generate_statement_code_package.generate_statement_code_src.generate_expression_code')
    def test_handle_return_helper_with_value_key(self, mock_gen_expr: MagicMock) -> None:
        """Test _handle_return helper with value key."""
        stmt = {"type": "return", "value": {"type": "literal", "value": 99}}
        next_offset = 8
        
        mock_gen_expr.return_value = ("MOV x0, #99\n", 8)
        
        code, new_offset = _handle_return(stmt, next_offset)
        
        self.assertEqual(code, "MOV x0, #99\n")
        self.assertEqual(new_offset, 8)

    @patch('generate_statement_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_if_stmt_package.generate_statement_code_package.generate_statement_code_src.generate_expression_code')
    def test_handle_expr_stmt_helper(self, mock_gen_expr: MagicMock) -> None:
        """Test _handle_expr_stmt helper function directly."""
        stmt = {"type": "expr_stmt", "expression": {"type": "literal", "value": 123}}
        next_offset = 8
        
        mock_gen_expr.return_value = ("MOV x0, #123\n", 8)
        
        code, new_offset = _handle_expr_stmt(stmt, next_offset)
        
        self.assertEqual(code, "MOV x0, #123\n")
        self.assertEqual(new_offset, 8)
        mock_gen_expr.assert_called_once_with({"type": "literal", "value": 123}, {}, 8)


if __name__ == "__main__":
    unittest.main()

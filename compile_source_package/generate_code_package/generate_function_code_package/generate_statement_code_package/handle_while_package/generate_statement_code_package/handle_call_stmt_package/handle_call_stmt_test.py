# === Test file for handle_call_stmt ===
import unittest
from unittest.mock import patch

# Import the function under test using relative import
from .handle_call_stmt_src import handle_call_stmt


class TestHandleCallStmt(unittest.TestCase):
    """Test cases for handle_call_stmt function."""

    def test_empty_function_name(self):
        """Test when function name is empty or missing."""
        stmt = {"function": "", "args": []}
        var_offsets = {}
        next_offset = 0

        code, updated_offset = handle_call_stmt(stmt, var_offsets, next_offset)

        self.assertEqual(code, "")
        self.assertEqual(updated_offset, 0)

    def test_missing_function_key(self):
        """Test when function key is missing from stmt."""
        stmt = {"args": []}
        var_offsets = {}
        next_offset = 0

        code, updated_offset = handle_call_stmt(stmt, var_offsets, next_offset)

        self.assertEqual(code, "")
        self.assertEqual(updated_offset, 0)

    def test_no_arguments(self):
        """Test CALL with no arguments."""
        stmt = {"function": "my_func", "args": []}
        var_offsets = {}
        next_offset = 100

        code, updated_offset = handle_call_stmt(stmt, var_offsets, next_offset)

        self.assertEqual(code, "bl my_func")
        self.assertEqual(updated_offset, 100)

    def test_single_argument(self):
        """Test CALL with a single argument."""
        stmt = {"function": "my_func", "args": [{"type": "LITERAL", "value": 42}]}
        var_offsets = {}
        next_offset = 100

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_call_stmt_package.handle_call_stmt_src.generate_expression_code"
        ) as mock_gen_expr:
            mock_gen_expr.return_value = ("MOV x0, #42", 108)

            code, updated_offset = handle_call_stmt(stmt, var_offsets, next_offset)

            mock_gen_expr.assert_called_once_with({"type": "LITERAL", "value": 42}, var_offsets, 100)
            self.assertIn("MOV x0, #42", code)
            self.assertIn("STORE_OFFSET 100", code)
            self.assertIn("bl my_func", code)
            self.assertEqual(updated_offset, 108)

    def test_multiple_arguments(self):
        """Test CALL with multiple arguments."""
        stmt = {
            "function": "add_func",
            "args": [
                {"type": "LITERAL", "value": 10},
                {"type": "LITERAL", "value": 20},
                {"type": "LITERAL", "value": 30},
            ],
        }
        var_offsets = {}
        next_offset = 200

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_call_stmt_package.handle_call_stmt_src.generate_expression_code"
        ) as mock_gen_expr:
            mock_gen_expr.side_effect = [
                ("MOV x0, #10", 208),
                ("MOV x0, #20", 216),
                ("MOV x0, #30", 224),
            ]

            code, updated_offset = handle_call_stmt(stmt, var_offsets, next_offset)

            self.assertEqual(mock_gen_expr.call_count, 3)
            self.assertIn("MOV x0, #10", code)
            self.assertIn("STORE_OFFSET 200", code)
            self.assertIn("MOV x0, #20", code)
            self.assertIn("STORE_OFFSET 208", code)
            self.assertIn("MOV x0, #30", code)
            self.assertIn("STORE_OFFSET 216", code)
            self.assertIn("bl add_func", code)
            self.assertEqual(updated_offset, 224)

    def test_var_offsets_passed_to_expression_generator(self):
        """Test that var_offsets is correctly passed to generate_expression_code."""
        stmt = {"function": "test_func", "args": [{"type": "VAR", "name": "x"}]}
        var_offsets = {"x": 0, "y": 8}
        next_offset = 50

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_call_stmt_package.handle_call_stmt_src.generate_expression_code"
        ) as mock_gen_expr:
            mock_gen_expr.return_value = ("LDR x0, [sp, #0]", 58)

            handle_call_stmt(stmt, var_offsets, next_offset)

            mock_gen_expr.assert_called_once_with({"type": "VAR", "name": "x"}, var_offsets, 50)

    def test_code_parts_joined_with_newlines(self):
        """Test that code parts are properly joined with newlines."""
        stmt = {
            "function": "multi_arg_func",
            "args": [{"type": "LITERAL", "value": 1}, {"type": "LITERAL", "value": 2}],
        }
        var_offsets = {}
        next_offset = 0

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_call_stmt_package.handle_call_stmt_src.generate_expression_code"
        ) as mock_gen_expr:
            mock_gen_expr.side_effect = [
                ("MOV x0, #1", 8),
                ("MOV x0, #2", 16),
            ]

            code, _ = handle_call_stmt(stmt, var_offsets, next_offset)

            lines = code.split("\n")
            self.assertEqual(len(lines), 5)
            self.assertEqual(lines[0], "MOV x0, #1")
            self.assertEqual(lines[1], "STORE_OFFSET 0")
            self.assertEqual(lines[2], "MOV x0, #2")
            self.assertEqual(lines[3], "STORE_OFFSET 8")
            self.assertEqual(lines[4], "bl multi_arg_func")

    def test_offset_calculation_for_store(self):
        """Test that STORE_OFFSET uses current_offset - 8."""
        stmt = {"function": "f", "args": [{"type": "LITERAL", "value": 5}]}
        var_offsets = {}
        next_offset = 100

        with patch(
            "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_call_stmt_package.handle_call_stmt_src.generate_expression_code"
        ) as mock_gen_expr:
            mock_gen_expr.return_value = ("MOV x0, #5", 108)

            code, _ = handle_call_stmt(stmt, var_offsets, next_offset)

            self.assertIn("STORE_OFFSET 100", code)

    def test_args_key_missing(self):
        """Test when args key is missing from stmt."""
        stmt = {"function": "no_args_func"}
        var_offsets = {}
        next_offset = 50

        code, updated_offset = handle_call_stmt(stmt, var_offsets, next_offset)

        self.assertEqual(code, "bl no_args_func")
        self.assertEqual(updated_offset, 50)


if __name__ == "__main__":
    unittest.main()

import unittest
from unittest.mock import patch

from ._generate_call_code_src import _generate_call_code


class TestGenerateCallCode(unittest.TestCase):
    """Test cases for _generate_call_code function."""

    def setUp(self):
        """Set up test fixtures."""
        self.func_name = "test_func"
        self.var_offsets = {"x": 0, "y": 8}

    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_assign_package.generate_expression_code_package._generate_call_code_package._generate_call_code_src.generate_expression_code')
    def test_call_no_args(self, mock_gen_expr):
        """Test function call with no arguments."""
        expr = {
            "type": "CALL",
            "name": "printf",
            "args": []
        }

        result = _generate_call_code(expr, self.func_name, self.var_offsets)

        # Should only generate the bl instruction
        self.assertEqual(result, "bl printf")
        # generate_expression_code should not be called for empty args
        mock_gen_expr.assert_not_called()

    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_assign_package.generate_expression_code_package._generate_call_code_package._generate_call_code_src.generate_expression_code')
    def test_call_single_arg(self, mock_gen_expr):
        """Test function call with one argument."""
        mock_gen_expr.return_value = "ldr x0, [sp, #0]"

        expr = {
            "type": "CALL",
            "name": "puts",
            "args": [{"type": "CONST", "value": 42}]
        }

        result = _generate_call_code(expr, self.func_name, self.var_offsets)

        # Should evaluate arg and call function
        expected = "ldr x0, [sp, #0]\nbl puts"
        self.assertEqual(result, expected)
        mock_gen_expr.assert_called_once()

    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_assign_package.generate_expression_code_package._generate_call_code_package._generate_call_code_src.generate_expression_code')
    def test_call_two_args(self, mock_gen_expr):
        """Test function call with two arguments."""
        mock_gen_expr.side_effect = [
            "ldr x0, [sp, #0]",  # First arg
            "ldr x0, [sp, #8]"   # Second arg
        ]

        expr = {
            "type": "CALL",
            "name": "add",
            "args": [
                {"type": "CONST", "value": 1},
                {"type": "CONST", "value": 2}
            ]
        }

        result = _generate_call_code(expr, self.func_name, self.var_offsets)

        # First arg stays in x0, second arg moved to x1
        expected_lines = [
            "ldr x0, [sp, #0]",
            "ldr x0, [sp, #8]",
            "mov x1, x0",
            "bl add"
        ]
        expected = "\n".join(expected_lines)
        self.assertEqual(result, expected)
        self.assertEqual(mock_gen_expr.call_count, 2)

    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_assign_package.generate_expression_code_package._generate_call_code_package._generate_call_code_src.generate_expression_code')
    def test_call_three_args(self, mock_gen_expr):
        """Test function call with three arguments."""
        mock_gen_expr.side_effect = [
            "arg1_code",
            "arg2_code",
            "arg3_code"
        ]

        expr = {
            "type": "CALL",
            "name": "func",
            "args": [
                {"type": "CONST", "value": 1},
                {"type": "CONST", "value": 2},
                {"type": "CONST", "value": 3}
            ]
        }

        result = _generate_call_code(expr, self.func_name, self.var_offsets)

        # Verify order: arg1 in x0, arg2 moved to x1, arg3 moved to x2
        expected_lines = [
            "arg1_code",
            "arg2_code",
            "mov x1, x0",
            "arg3_code",
            "mov x2, x0",
            "bl func"
        ]
        expected = "\n".join(expected_lines)
        self.assertEqual(result, expected)
        self.assertEqual(mock_gen_expr.call_count, 3)

    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_assign_package.generate_expression_code_package._generate_call_code_package._generate_call_code_src.generate_expression_code')
    def test_call_eight_args_max(self, mock_gen_expr):
        """Test function call with maximum 8 arguments."""
        # Mock return values for 8 args
        mock_gen_expr.side_effect = [f"ldr x0, [sp, #{i*8}]" for i in range(8)]

        expr = {
            "type": "CALL",
            "name": "multi_arg_func",
            "args": [{"type": "CONST", "value": i} for i in range(8)]
        }

        result = _generate_call_code(expr, self.func_name, self.var_offsets)

        # Should have 8 arg evaluations, 7 mov instructions (for args 1-7), and bl
        self.assertIn("bl multi_arg_func", result)
        self.assertIn("mov x1, x0", result)
        self.assertIn("mov x7, x0", result)
        self.assertEqual(mock_gen_expr.call_count, 8)

        # Count mov instructions - should be 7 (for indices 1-7)
        mov_count = result.count("mov x")
        self.assertEqual(mov_count, 7)

    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_assign_package.generate_expression_code_package._generate_call_code_package._generate_call_code_src.generate_expression_code')
    def test_call_nine_args_raises_error(self, mock_gen_expr):
        """Test function call with 9 arguments raises ValueError."""
        expr = {
            "type": "CALL",
            "name": "too_many_args",
            "args": [{"type": "CONST", "value": i} for i in range(9)]
        }

        with self.assertRaises(ValueError) as context:
            _generate_call_code(expr, self.func_name, self.var_offsets)

        self.assertIn("Too many arguments", str(context.exception))
        # generate_expression_code should not be called when validation fails
        mock_gen_expr.assert_not_called()

    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_assign_package.generate_expression_code_package._generate_call_code_package._generate_call_code_src.generate_expression_code')
    def test_call_missing_name_defaults_to_empty(self, mock_gen_expr):
        """Test function call with missing name field."""
        expr = {
            "type": "CALL",
            "args": []
        }

        result = _generate_call_code(expr, self.func_name, self.var_offsets)

        # Should use empty string for function name
        self.assertEqual(result, "bl ")
        mock_gen_expr.assert_not_called()

    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_assign_package.generate_expression_code_package._generate_call_code_package._generate_call_code_src.generate_expression_code')
    def test_call_missing_args_defaults_to_empty(self, mock_gen_expr):
        """Test function call with missing args field."""
        expr = {
            "type": "CALL",
            "name": "no_args_func"
        }

        result = _generate_call_code(expr, self.func_name, self.var_offsets)

        # Should default to empty args list
        self.assertEqual(result, "bl no_args_func")
        mock_gen_expr.assert_not_called()

    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_assign_package.generate_expression_code_package._generate_call_code_package._generate_call_code_src.generate_expression_code')
    def test_call_args_evaluated_left_to_right(self, mock_gen_expr):
        """Test that arguments are evaluated left-to-right."""
        mock_gen_expr.side_effect = [
            "arg1_code",
            "arg2_code",
            "arg3_code"
        ]

        expr = {
            "type": "CALL",
            "name": "func",
            "args": [
                {"type": "CONST", "value": 1},
                {"type": "CONST", "value": 2},
                {"type": "CONST", "value": 3}
            ]
        }

        _generate_call_code(expr, self.func_name, self.var_offsets)

        # Verify call order matches argument order
        calls = mock_gen_expr.call_args_list
        self.assertEqual(len(calls), 3)
        # Each call should receive the corresponding arg expression
        self.assertEqual(calls[0][0][0]["value"], 1)
        self.assertEqual(calls[1][0][0]["value"], 2)
        self.assertEqual(calls[2][0][0]["value"], 3)

    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_assign_package.generate_expression_code_package._generate_call_code_package._generate_call_code_src.generate_expression_code')
    def test_call_generates_code_lines_joined_by_newline(self, mock_gen_expr):
        """Test that code lines are properly joined with newlines."""
        mock_gen_expr.side_effect = ["line1", "line2"]

        expr = {
            "type": "CALL",
            "name": "test",
            "args": [{"type": "CONST", "value": 1}, {"type": "CONST", "value": 2}]
        }

        result = _generate_call_code(expr, self.func_name, self.var_offsets)

        # Verify newline separation
        lines = result.split("\n")
        self.assertEqual(len(lines), 4)  # line1, line2, mov x1, x0, bl test
        self.assertEqual(lines[0], "line1")
        self.assertEqual(lines[1], "line2")
        self.assertEqual(lines[2], "mov x1, x0")
        self.assertEqual(lines[3], "bl test")


if __name__ == '__main__':
    unittest.main()

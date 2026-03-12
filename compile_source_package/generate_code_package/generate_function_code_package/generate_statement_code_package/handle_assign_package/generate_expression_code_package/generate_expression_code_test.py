# === imports ===
import unittest
from unittest.mock import patch

# === relative import of target function ===
from .generate_expression_code_src import generate_expression_code


class TestGenerateExpressionCode(unittest.TestCase):
    """Test cases for generate_expression_code function."""

    @patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_assign_package.generate_expression_code_package.generate_expression_code_src._generate_const_code")
    def test_const_expression(self, mock_const):
        """Test CONST expression type dispatches to _generate_const_code."""
        mock_const.return_value = "mov x0, #42"
        
        expr = {"type": "CONST", "value": 42}
        result = generate_expression_code(expr, "test_func", {})
        
        mock_const.assert_called_once_with(42)
        self.assertEqual(result, "mov x0, #42")

    @patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_assign_package.generate_expression_code_package.generate_expression_code_src._generate_var_code")
    def test_var_expression(self, mock_var):
        """Test VAR expression type dispatches to _generate_var_code."""
        mock_var.return_value = "ldr x0, [sp, #8]"
        
        expr = {"type": "VAR", "name": "x"}
        var_offsets = {"x": 8}
        result = generate_expression_code(expr, "test_func", var_offsets)
        
        mock_var.assert_called_once_with("x", var_offsets)
        self.assertEqual(result, "ldr x0, [sp, #8]")

    @patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_assign_package.generate_expression_code_package.generate_expression_code_src._generate_binop_code")
    def test_binop_expression(self, mock_binop):
        """Test BINOP expression type dispatches to _generate_binop_code."""
        mock_binop.return_value = "mov x9, x0\nmov x0, #5\nadd x0, x9, x0"
        
        expr = {
            "type": "BINOP",
            "op": "+",
            "left": {"type": "VAR", "name": "a"},
            "right": {"type": "CONST", "value": 5}
        }
        var_offsets = {"a": 0}
        result = generate_expression_code(expr, "test_func", var_offsets)
        
        mock_binop.assert_called_once_with(expr, "test_func", var_offsets)
        self.assertEqual(result, "mov x9, x0\nmov x0, #5\nadd x0, x9, x0")

    @patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_assign_package.generate_expression_code_package.generate_expression_code_src._generate_call_code")
    def test_call_expression(self, mock_call):
        """Test CALL expression type dispatches to _generate_call_code."""
        mock_call.return_value = "mov x0, #1\nmov x1, #2\nbl my_func"
        
        expr = {
            "type": "CALL",
            "name": "my_func",
            "args": [
                {"type": "CONST", "value": 1},
                {"type": "CONST", "value": 2}
            ]
        }
        var_offsets = {}
        result = generate_expression_code(expr, "test_func", var_offsets)
        
        mock_call.assert_called_once_with(expr, "test_func", var_offsets)
        self.assertEqual(result, "mov x0, #1\nmov x1, #2\nbl my_func")

    def test_unsupported_expression_type(self):
        """Test that unsupported expression types raise ValueError."""
        expr = {"type": "UNKNOWN", "data": "some_data"}
        
        with self.assertRaises(ValueError) as context:
            generate_expression_code(expr, "test_func", {})
        
        self.assertIn("Unsupported expression type: UNKNOWN", str(context.exception))

    @patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_assign_package.generate_expression_code_package.generate_expression_code_src._generate_const_code")
    def test_const_with_zero_value(self, mock_const):
        """Test CONST expression with zero value (boundary case)."""
        mock_const.return_value = "mov x0, #0"
        
        expr = {"type": "CONST", "value": 0}
        result = generate_expression_code(expr, "test_func", {})
        
        mock_const.assert_called_once_with(0)
        self.assertEqual(result, "mov x0, #0")

    @patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_assign_package.generate_expression_code_package.generate_expression_code_src._generate_const_code")
    def test_const_with_negative_value(self, mock_const):
        """Test CONST expression with negative value (boundary case)."""
        mock_const.return_value = "mov x0, #-100"
        
        expr = {"type": "CONST", "value": -100}
        result = generate_expression_code(expr, "test_func", {})
        
        mock_const.assert_called_once_with(-100)
        self.assertEqual(result, "mov x0, #-100")

    @patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_assign_package.generate_expression_code_package.generate_expression_code_src._generate_var_code")
    def test_var_with_empty_offsets(self, mock_var):
        """Test VAR expression behavior (mock will handle KeyError if var not in offsets)."""
        mock_var.side_effect = KeyError("missing_var")
        
        expr = {"type": "VAR", "name": "missing_var"}
        var_offsets = {}
        
        with self.assertRaises(KeyError):
            generate_expression_code(expr, "test_func", var_offsets)
        
        mock_var.assert_called_once_with("missing_var", var_offsets)

    @patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_assign_package.generate_expression_code_package.generate_expression_code_src._generate_binop_code")
    def test_binop_with_comparison_operator(self, mock_binop):
        """Test BINOP expression with comparison operator."""
        mock_binop.return_value = "mov x9, x0\nmov x0, #10\ncmp x9, x0\ncset x0, eq"
        
        expr = {
            "type": "BINOP",
            "op": "==",
            "left": {"type": "VAR", "name": "x"},
            "right": {"type": "CONST", "value": 10}
        }
        var_offsets = {"x": 0}
        result = generate_expression_code(expr, "test_func", var_offsets)
        
        mock_binop.assert_called_once_with(expr, "test_func", var_offsets)
        self.assertEqual(result, "mov x9, x0\nmov x0, #10\ncmp x9, x0\ncset x0, eq")

    @patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_assign_package.generate_expression_code_package.generate_expression_code_src._generate_call_code")
    def test_call_with_no_args(self, mock_call):
        """Test CALL expression with no arguments."""
        mock_call.return_value = "bl no_arg_func"
        
        expr = {
            "type": "CALL",
            "name": "no_arg_func",
            "args": []
        }
        var_offsets = {}
        result = generate_expression_code(expr, "test_func", var_offsets)
        
        mock_call.assert_called_once_with(expr, "test_func", var_offsets)
        self.assertEqual(result, "bl no_arg_func")

    @patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_assign_package.generate_expression_code_package.generate_expression_code_src._generate_call_code")
    def test_call_with_multiple_args(self, mock_call):
        """Test CALL expression with multiple arguments."""
        mock_call.return_value = "mov x0, #1\nmov x1, #2\nmov x2, #3\nbl multi_arg_func"
        
        expr = {
            "type": "CALL",
            "name": "multi_arg_func",
            "args": [
                {"type": "CONST", "value": 1},
                {"type": "CONST", "value": 2},
                {"type": "CONST", "value": 3}
            ]
        }
        var_offsets = {}
        result = generate_expression_code(expr, "test_func", var_offsets)
        
        mock_call.assert_called_once_with(expr, "test_func", var_offsets)
        self.assertEqual(result, "mov x0, #1\nmov x1, #2\nmov x2, #3\nbl multi_arg_func")

    def test_missing_type_field(self):
        """Test expression without type field raises ValueError."""
        expr = {"value": 42}  # Missing "type" field
        
        with self.assertRaises(ValueError) as context:
            generate_expression_code(expr, "test_func", {})
        
        self.assertIn("Unsupported expression type: None", str(context.exception))


if __name__ == "__main__":
    unittest.main()

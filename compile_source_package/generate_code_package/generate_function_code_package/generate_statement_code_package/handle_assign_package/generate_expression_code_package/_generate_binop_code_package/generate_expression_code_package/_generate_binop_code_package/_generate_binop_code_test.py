import unittest
from unittest.mock import patch

from ._generate_binop_code_src import _generate_binop_code


class TestGenerateBinopCode(unittest.TestCase):
    """Unit tests for _generate_binop_code function."""

    def setUp(self):
        """Set up test fixtures."""
        self.func_name = "test_func"
        self.var_offsets = {"var1": 0, "var2": 8}

    @patch('_generate_binop_code_package.generate_expression_code_package._generate_binop_code_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code')
    def test_add_operator(self, mock_gen_expr):
        """Test addition operator generates correct ARM64 code."""
        mock_gen_expr.side_effect = [
            "    mov x0, #5\n",
            "    mov x0, #3\n"
        ]
        
        expr = {
            "type": "BINOP",
            "op": "+",
            "left": {"type": "LITERAL", "value": 5},
            "right": {"type": "LITERAL", "value": 3}
        }
        
        result = _generate_binop_code(expr, self.func_name, self.var_offsets)
        
        expected = "    mov x0, #5\n    mov x9, x0\n    mov x0, #3\n    add x0, x9, x0\n"
        self.assertEqual(result, expected)
        self.assertEqual(mock_gen_expr.call_count, 2)

    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_assign_package.generate_expression_code_package._generate_binop_code_package.generate_expression_code_package._generate_binop_code_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code')
    def test_sub_operator(self, mock_gen_expr):
        """Test subtraction operator generates correct ARM64 code."""
        mock_gen_expr.side_effect = [
            "    mov x0, #10\n",
            "    mov x0, #4\n"
        ]
        
        expr = {
            "type": "BINOP",
            "op": "-",
            "left": {"type": "LITERAL", "value": 10},
            "right": {"type": "LITERAL", "value": 4}
        }
        
        result = _generate_binop_code(expr, self.func_name, self.var_offsets)
        
        expected = "    mov x0, #10\n    mov x9, x0\n    mov x0, #4\n    sub x0, x9, x0\n"
        self.assertEqual(result, expected)

    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_assign_package.generate_expression_code_package._generate_binop_code_package.generate_expression_code_package._generate_binop_code_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code')
    def test_mul_operator(self, mock_gen_expr):
        """Test multiplication operator generates correct ARM64 code."""
        mock_gen_expr.side_effect = [
            "    mov x0, #6\n",
            "    mov x0, #7\n"
        ]
        
        expr = {
            "type": "BINOP",
            "op": "*",
            "left": {"type": "LITERAL", "value": 6},
            "right": {"type": "LITERAL", "value": 7}
        }
        
        result = _generate_binop_code(expr, self.func_name, self.var_offsets)
        
        expected = "    mov x0, #6\n    mov x9, x0\n    mov x0, #7\n    mul x0, x9, x0\n"
        self.assertEqual(result, expected)

    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_assign_package.generate_expression_code_package._generate_binop_code_package.generate_expression_code_package._generate_binop_code_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code')
    def test_div_operator(self, mock_gen_expr):
        """Test division operator generates correct ARM64 code (signed division)."""
        mock_gen_expr.side_effect = [
            "    mov x0, #20\n",
            "    mov x0, #4\n"
        ]
        
        expr = {
            "type": "BINOP",
            "op": "/",
            "left": {"type": "LITERAL", "value": 20},
            "right": {"type": "LITERAL", "value": 4}
        }
        
        result = _generate_binop_code(expr, self.func_name, self.var_offsets)
        
        expected = "    mov x0, #20\n    mov x9, x0\n    mov x0, #4\n    sdiv x0, x9, x0\n"
        self.assertEqual(result, expected)

    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_assign_package.generate_expression_code_package._generate_binop_code_package.generate_expression_code_package._generate_binop_code_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code')
    def test_eq_operator(self, mock_gen_expr):
        """Test equality operator generates correct ARM64 code."""
        mock_gen_expr.side_effect = [
            "    mov x0, #5\n",
            "    mov x0, #5\n"
        ]
        
        expr = {
            "type": "BINOP",
            "op": "==",
            "left": {"type": "LITERAL", "value": 5},
            "right": {"type": "LITERAL", "value": 5}
        }
        
        result = _generate_binop_code(expr, self.func_name, self.var_offsets)
        
        expected = "    mov x0, #5\n    mov x9, x0\n    mov x0, #5\n    cmp x9, x0\n    cset x0, eq\n"
        self.assertEqual(result, expected)

    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_assign_package.generate_expression_code_package._generate_binop_code_package.generate_expression_code_package._generate_binop_code_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code')
    def test_ne_operator(self, mock_gen_expr):
        """Test inequality operator generates correct ARM64 code."""
        mock_gen_expr.side_effect = [
            "    mov x0, #5\n",
            "    mov x0, #3\n"
        ]
        
        expr = {
            "type": "BINOP",
            "op": "!=",
            "left": {"type": "LITERAL", "value": 5},
            "right": {"type": "LITERAL", "value": 3}
        }
        
        result = _generate_binop_code(expr, self.func_name, self.var_offsets)
        
        expected = "    mov x0, #5\n    mov x9, x0\n    mov x0, #3\n    cmp x9, x0\n    cset x0, ne\n"
        self.assertEqual(result, expected)

    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_assign_package.generate_expression_code_package._generate_binop_code_package.generate_expression_code_package._generate_binop_code_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code')
    def test_lt_operator(self, mock_gen_expr):
        """Test less-than operator generates correct ARM64 code."""
        mock_gen_expr.side_effect = [
            "    mov x0, #3\n",
            "    mov x0, #5\n"
        ]
        
        expr = {
            "type": "BINOP",
            "op": "<",
            "left": {"type": "LITERAL", "value": 3},
            "right": {"type": "LITERAL", "value": 5}
        }
        
        result = _generate_binop_code(expr, self.func_name, self.var_offsets)
        
        expected = "    mov x0, #3\n    mov x9, x0\n    mov x0, #5\n    cmp x9, x0\n    cset x0, lt\n"
        self.assertEqual(result, expected)

    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_assign_package.generate_expression_code_package._generate_binop_code_package.generate_expression_code_package._generate_binop_code_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code')
    def test_gt_operator(self, mock_gen_expr):
        """Test greater-than operator generates correct ARM64 code."""
        mock_gen_expr.side_effect = [
            "    mov x0, #10\n",
            "    mov x0, #5\n"
        ]
        
        expr = {
            "type": "BINOP",
            "op": ">",
            "left": {"type": "LITERAL", "value": 10},
            "right": {"type": "LITERAL", "value": 5}
        }
        
        result = _generate_binop_code(expr, self.func_name, self.var_offsets)
        
        expected = "    mov x0, #10\n    mov x9, x0\n    mov x0, #5\n    cmp x9, x0\n    cset x0, gt\n"
        self.assertEqual(result, expected)

    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_assign_package.generate_expression_code_package._generate_binop_code_package.generate_expression_code_package._generate_binop_code_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code')
    def test_le_operator(self, mock_gen_expr):
        """Test less-than-or-equal operator generates correct ARM64 code."""
        mock_gen_expr.side_effect = [
            "    mov x0, #5\n",
            "    mov x0, #5\n"
        ]
        
        expr = {
            "type": "BINOP",
            "op": "<=",
            "left": {"type": "LITERAL", "value": 5},
            "right": {"type": "LITERAL", "value": 5}
        }
        
        result = _generate_binop_code(expr, self.func_name, self.var_offsets)
        
        expected = "    mov x0, #5\n    mov x9, x0\n    mov x0, #5\n    cmp x9, x0\n    cset x0, le\n"
        self.assertEqual(result, expected)

    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_assign_package.generate_expression_code_package._generate_binop_code_package.generate_expression_code_package._generate_binop_code_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code')
    def test_ge_operator(self, mock_gen_expr):
        """Test greater-than-or-equal operator generates correct ARM64 code."""
        mock_gen_expr.side_effect = [
            "    mov x0, #10\n",
            "    mov x0, #5\n"
        ]
        
        expr = {
            "type": "BINOP",
            "op": ">=",
            "left": {"type": "LITERAL", "value": 10},
            "right": {"type": "LITERAL", "value": 5}
        }
        
        result = _generate_binop_code(expr, self.func_name, self.var_offsets)
        
        expected = "    mov x0, #10\n    mov x9, x0\n    mov x0, #5\n    cmp x9, x0\n    cset x0, ge\n"
        self.assertEqual(result, expected)

    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_assign_package.generate_expression_code_package._generate_binop_code_package.generate_expression_code_package._generate_binop_code_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code')
    def test_unsupported_operator_raises_valueerror(self, mock_gen_expr):
        """Test that unsupported operator raises ValueError."""
        expr = {
            "type": "BINOP",
            "op": "%",
            "left": {"type": "LITERAL", "value": 10},
            "right": {"type": "LITERAL", "value": 3}
        }
        
        with self.assertRaises(ValueError) as context:
            _generate_binop_code(expr, self.func_name, self.var_offsets)
        
        self.assertIn("Unsupported binary operator: %", str(context.exception))
        mock_gen_expr.assert_not_called()

    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_assign_package.generate_expression_code_package._generate_binop_code_package.generate_expression_code_package._generate_binop_code_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code')
    def test_nested_expressions(self, mock_gen_expr):
        """Test nested binary expressions are handled correctly."""
        # Mock for nested left expression (itself a BINOP)
        mock_gen_expr.side_effect = [
            "    mov x0, #2\n    mov x9, x0\n    mov x0, #3\n    add x0, x9, x0\n",  # left: 2+3
            "    mov x0, #4\n"  # right: 4
        ]
        
        expr = {
            "type": "BINOP",
            "op": "*",
            "left": {
                "type": "BINOP",
                "op": "+",
                "left": {"type": "LITERAL", "value": 2},
                "right": {"type": "LITERAL", "value": 3}
            },
            "right": {"type": "LITERAL", "value": 4}
        }
        
        result = _generate_binop_code(expr, self.func_name, self.var_offsets)
        
        expected = (
            "    mov x0, #2\n    mov x9, x0\n    mov x0, #3\n    add x0, x9, x0\n"
            "    mov x9, x0\n"
            "    mov x0, #4\n"
            "    mul x0, x9, x0\n"
        )
        self.assertEqual(result, expected)
        self.assertEqual(mock_gen_expr.call_count, 2)

    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_assign_package.generate_expression_code_package._generate_binop_code_package.generate_expression_code_package._generate_binop_code_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code')
    def test_empty_var_offsets(self, mock_gen_expr):
        """Test function works with empty var_offsets."""
        mock_gen_expr.side_effect = [
            "    mov x0, #1\n",
            "    mov x0, #2\n"
        ]
        
        expr = {
            "type": "BINOP",
            "op": "+",
            "left": {"type": "LITERAL", "value": 1},
            "right": {"type": "LITERAL", "value": 2}
        }
        
        result = _generate_binop_code(expr, self.func_name, {})
        
        expected = "    mov x0, #1\n    mov x9, x0\n    mov x0, #2\n    add x0, x9, x0\n"
        self.assertEqual(result, expected)

    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_assign_package.generate_expression_code_package._generate_binop_code_package.generate_expression_code_package._generate_binop_code_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code')
    def test_generate_expression_code_called_with_correct_params(self, mock_gen_expr):
        """Test that generate_expression_code is called with correct parameters."""
        mock_gen_expr.return_value = "    mov x0, #1\n"
        
        expr = {
            "type": "BINOP",
            "op": "+",
            "left": {"type": "LITERAL", "value": 1},
            "right": {"type": "LITERAL", "value": 2}
        }
        
        _generate_binop_code(expr, self.func_name, self.var_offsets)
        
        self.assertEqual(mock_gen_expr.call_count, 2)
        # First call for left operand
        mock_gen_expr.assert_any_call({"type": "LITERAL", "value": 1}, self.func_name, self.var_offsets)
        # Second call for right operand
        mock_gen_expr.assert_any_call({"type": "LITERAL", "value": 2}, self.func_name, self.var_offsets)


if __name__ == "__main__":
    unittest.main()

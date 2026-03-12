import unittest
from unittest.mock import patch

from ._generate_binop_code_src import _generate_binop_code
from . import _generate_binop_code_src


class TestGenerateBinopCode(unittest.TestCase):
    """Test cases for _generate_binop_code function."""

    @patch.object(_generate_binop_code_src, 'generate_expression_code')
    def test_add_operator(self, mock_gen_expr):
        """Test binary addition operator."""
        mock_gen_expr.side_effect = ["mov x0, #5", "mov x0, #3"]

        expr = {
            "type": "BINOP",
            "op": "+",
            "left": {"type": "LITERAL", "value": 5},
            "right": {"type": "LITERAL", "value": 3}
        }

        result = _generate_binop_code(expr, "test_func", {})

        expected = "mov x0, #5\nmov x9, x0\nmov x0, #3\nadd x0, x9, x0"
        self.assertEqual(result, expected)

    @patch.object(_generate_binop_code_src, 'generate_expression_code')
    def test_sub_operator(self, mock_gen_expr):
        """Test binary subtraction operator."""
        mock_gen_expr.side_effect = ["mov x0, #10", "mov x0, #4"]

        expr = {
            "type": "BINOP",
            "op": "-",
            "left": {"type": "LITERAL", "value": 10},
            "right": {"type": "LITERAL", "value": 4}
        }

        result = _generate_binop_code(expr, "test_func", {})

        expected = "mov x0, #10\nmov x9, x0\nmov x0, #4\nsub x0, x9, x0"
        self.assertEqual(result, expected)

    @patch('._generate_binop_code_src.generate_expression_code')
    def test_mul_operator(self, mock_gen_expr):
        """Test binary multiplication operator."""
        mock_gen_expr.side_effect = ["mov x0, #6", "mov x0, #7"]

        expr = {
            "type": "BINOP",
            "op": "*",
            "left": {"type": "LITERAL", "value": 6},
            "right": {"type": "LITERAL", "value": 7}
        }

        result = _generate_binop_code(expr, "test_func", {})

        expected = "mov x0, #6\nmov x9, x0\nmov x0, #7\nmul x0, x9, x0"
        self.assertEqual(result, expected)

    @patch('._generate_binop_code_src.generate_expression_code')
    def test_div_operator(self, mock_gen_expr):
        """Test binary division operator."""
        mock_gen_expr.side_effect = ["mov x0, #10", "mov x0, #2"]

        expr = {
            "type": "BINOP",
            "op": "/",
            "left": {"type": "LITERAL", "value": 10},
            "right": {"type": "LITERAL", "value": 2}
        }

        result = _generate_binop_code(expr, "test_func", {})

        expected = "mov x0, #10\nmov x9, x0\nmov x0, #2\nsdiv x0, x9, x0"
        self.assertEqual(result, expected)

    @patch('._generate_binop_code_src.generate_expression_code')
    def test_eq_operator(self, mock_gen_expr):
        """Test equality comparison operator."""
        mock_gen_expr.side_effect = ["mov x0, #5", "mov x0, #5"]

        expr = {
            "type": "BINOP",
            "op": "==",
            "left": {"type": "LITERAL", "value": 5},
            "right": {"type": "LITERAL", "value": 5}
        }

        result = _generate_binop_code(expr, "test_func", {})

        expected = "mov x0, #5\nmov x9, x0\nmov x0, #5\ncmp x9, x0\ncset x0, eq"
        self.assertEqual(result, expected)

    @patch('._generate_binop_code_src.generate_expression_code')
    def test_ne_operator(self, mock_gen_expr):
        """Test not equal comparison operator."""
        mock_gen_expr.side_effect = ["mov x0, #5", "mov x0, #3"]

        expr = {
            "type": "BINOP",
            "op": "!=",
            "left": {"type": "LITERAL", "value": 5},
            "right": {"type": "LITERAL", "value": 3}
        }

        result = _generate_binop_code(expr, "test_func", {})

        expected = "mov x0, #5\nmov x9, x0\nmov x0, #3\ncmp x9, x0\ncset x0, ne"
        self.assertEqual(result, expected)

    @patch('._generate_binop_code_src.generate_expression_code')
    def test_lt_operator(self, mock_gen_expr):
        """Test less than comparison operator."""
        mock_gen_expr.side_effect = ["mov x0, #3", "mov x0, #5"]

        expr = {
            "type": "BINOP",
            "op": "<",
            "left": {"type": "LITERAL", "value": 3},
            "right": {"type": "LITERAL", "value": 5}
        }

        result = _generate_binop_code(expr, "test_func", {})

        expected = "mov x0, #3\nmov x9, x0\nmov x0, #5\ncmp x9, x0\ncset x0, lt"
        self.assertEqual(result, expected)

    @patch('._generate_binop_code_src.generate_expression_code')
    def test_gt_operator(self, mock_gen_expr):
        """Test greater than comparison operator."""
        mock_gen_expr.side_effect = ["mov x0, #10", "mov x0, #5"]

        expr = {
            "type": "BINOP",
            "op": ">",
            "left": {"type": "LITERAL", "value": 10},
            "right": {"type": "LITERAL", "value": 5}
        }

        result = _generate_binop_code(expr, "test_func", {})

        expected = "mov x0, #10\nmov x9, x0\nmov x0, #5\ncmp x9, x0\ncset x0, gt"
        self.assertEqual(result, expected)

    @patch('._generate_binop_code_src.generate_expression_code')
    def test_le_operator(self, mock_gen_expr):
        """Test less than or equal comparison operator."""
        mock_gen_expr.side_effect = ["mov x0, #5", "mov x0, #5"]

        expr = {
            "type": "BINOP",
            "op": "<=",
            "left": {"type": "LITERAL", "value": 5},
            "right": {"type": "LITERAL", "value": 5}
        }

        result = _generate_binop_code(expr, "test_func", {})

        expected = "mov x0, #5\nmov x9, x0\nmov x0, #5\ncmp x9, x0\ncset x0, le"
        self.assertEqual(result, expected)

    @patch('._generate_binop_code_src.generate_expression_code')
    def test_ge_operator(self, mock_gen_expr):
        """Test greater than or equal comparison operator."""
        mock_gen_expr.side_effect = ["mov x0, #10", "mov x0, #5"]

        expr = {
            "type": "BINOP",
            "op": ">=",
            "left": {"type": "LITERAL", "value": 10},
            "right": {"type": "LITERAL", "value": 5}
        }

        result = _generate_binop_code(expr, "test_func", {})

        expected = "mov x0, #10\nmov x9, x0\nmov x0, #5\ncmp x9, x0\ncset x0, ge"
        self.assertEqual(result, expected)

    @patch('._generate_binop_code_src.generate_expression_code')
    def test_nested_expression(self, mock_gen_expr):
        """Test nested binary operations."""
        mock_gen_expr.side_effect = [
            "mov x0, #2\nmov x9, x0\nmov x0, #3\nadd x0, x9, x0",
            "mov x0, #4"
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

        result = _generate_binop_code(expr, "test_func", {})

        expected = (
            "mov x0, #2\nmov x9, x0\nmov x0, #3\nadd x0, x9, x0\n"
            "mov x9, x0\n"
            "mov x0, #4\n"
            "mul x0, x9, x0"
        )
        self.assertEqual(result, expected)
        self.assertEqual(mock_gen_expr.call_count, 2)

    @patch('._generate_binop_code_src.generate_expression_code')
    def test_with_var_offsets(self, mock_gen_expr):
        """Test that var_offsets are passed through correctly."""
        mock_gen_expr.side_effect = ["ldr x0, [sp, #8]", "ldr x0, [sp, #16]"]

        var_offsets = {"x": 8, "y": 16}
        expr = {
            "type": "BINOP",
            "op": "+",
            "left": {"type": "VAR", "name": "x"},
            "right": {"type": "VAR", "name": "y"}
        }

        result = _generate_binop_code(expr, "my_func", var_offsets)

        expected = "ldr x0, [sp, #8]\nmov x9, x0\nldr x0, [sp, #16]\nadd x0, x9, x0"
        self.assertEqual(result, expected)

        calls = mock_gen_expr.call_args_list
        self.assertEqual(calls[0][0][0]["name"], "x")
        self.assertEqual(calls[0][0][1], "my_func")
        self.assertEqual(calls[0][0][2], var_offsets)
        self.assertEqual(calls[1][0][0]["name"], "y")
        self.assertEqual(calls[1][0][1], "my_func")
        self.assertEqual(calls[1][0][2], var_offsets)

    @patch('._generate_binop_code_src.generate_expression_code')
    def test_invalid_operator(self, mock_gen_expr):
        """Test that invalid operator raises ValueError."""
        mock_gen_expr.side_effect = ["mov x0, #1", "mov x0, #2"]

        expr = {
            "type": "BINOP",
            "op": "**",
            "left": {"type": "LITERAL", "value": 1},
            "right": {"type": "LITERAL", "value": 2}
        }

        with self.assertRaises(ValueError) as context:
            _generate_binop_code(expr, "test_func", {})

        self.assertIn("Unsupported binary operator", str(context.exception))
        self.assertIn("**", str(context.exception))

    @patch('._generate_binop_code_src.generate_expression_code')
    def test_empty_func_name(self, mock_gen_expr):
        """Test with empty function name."""
        mock_gen_expr.side_effect = ["mov x0, #1", "mov x0, #2"]

        expr = {
            "type": "BINOP",
            "op": "+",
            "left": {"type": "LITERAL", "value": 1},
            "right": {"type": "LITERAL", "value": 2}
        }

        result = _generate_binop_code(expr, "", {})

        expected = "mov x0, #1\nmov x9, x0\nmov x0, #2\nadd x0, x9, x0"
        self.assertEqual(result, expected)

    @patch('._generate_binop_code_src.generate_expression_code')
    def test_complex_nested_expression(self, mock_gen_expr):
        """Test deeply nested expression tree."""
        mock_gen_expr.side_effect = [
            "mov x0, #1\nmov x9, x0\nmov x0, #2\nadd x0, x9, x0",
            "mov x0, #3\nmov x9, x0\nmov x0, #4\nsub x0, x9, x0",
        ]

        expr = {
            "type": "BINOP",
            "op": "*",
            "left": {
                "type": "BINOP",
                "op": "+",
                "left": {"type": "LITERAL", "value": 1},
                "right": {"type": "LITERAL", "value": 2}
            },
            "right": {
                "type": "BINOP",
                "op": "-",
                "left": {"type": "LITERAL", "value": 3},
                "right": {"type": "LITERAL", "value": 4}
            }
        }

        result = _generate_binop_code(expr, "test_func", {})

        expected = (
            "mov x0, #1\nmov x9, x0\nmov x0, #2\nadd x0, x9, x0\n"
            "mov x9, x0\n"
            "mov x0, #3\nmov x9, x0\nmov x0, #4\nsub x0, x9, x0\n"
            "mul x0, x9, x0"
        )
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()

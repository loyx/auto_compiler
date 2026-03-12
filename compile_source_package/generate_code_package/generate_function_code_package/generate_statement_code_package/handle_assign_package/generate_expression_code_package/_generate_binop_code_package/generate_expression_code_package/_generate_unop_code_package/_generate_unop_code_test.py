# === std / third-party imports ===
import unittest
from unittest.mock import patch

# === sub function imports ===
from ._generate_unop_code_src import _generate_unop_code


class TestGenerateUnopCode(unittest.TestCase):
    """Test cases for _generate_unop_code function."""

    def setUp(self):
        """Set up test fixtures."""
        self.func_name = "test_func"
        self.var_offsets = {"x": 0, "y": 8}

    @patch("._generate_unop_code_package._generate_unop_code_src.generate_expression_code")
    def test_negation_operator(self, mock_gen_expr):
        """Test arithmetic negation operator '-'."""
        mock_gen_expr.return_value = "ldr x0, [sp, #0]\n"
        
        expr = {
            "type": "UNOP",
            "op": "-",
            "operand": {"type": "VAR", "name": "x"}
        }
        
        result = _generate_unop_code(expr, self.func_name, self.var_offsets)
        
        mock_gen_expr.assert_called_once_with(
            {"type": "VAR", "name": "x"},
            self.func_name,
            self.var_offsets
        )
        self.assertEqual(result, "ldr x0, [sp, #0]\nneg x0, x0\n")

    @patch("._generate_unop_code_package._generate_unop_code_src.generate_expression_code")
    def test_logical_not_operator(self, mock_gen_expr):
        """Test logical not operator '!'."""
        mock_gen_expr.return_value = "mov x0, #1\n"
        
        expr = {
            "type": "UNOP",
            "op": "!",
            "operand": {"type": "CONST", "value": 1}
        }
        
        result = _generate_unop_code(expr, self.func_name, self.var_offsets)
        
        mock_gen_expr.assert_called_once_with(
            {"type": "CONST", "value": 1},
            self.func_name,
            self.var_offsets
        )
        self.assertEqual(result, "mov x0, #1\ncmp x0, #0\ncset x0, eq\n")

    @patch("._generate_unop_code_package._generate_unop_code_src.generate_expression_code")
    def test_nested_unop_expression(self, mock_gen_expr):
        """Test unary operator with nested expression operand."""
        mock_gen_expr.return_value = "ldr x0, [sp, #8]\nneg x0, x0\n"
        
        expr = {
            "type": "UNOP",
            "op": "!",
            "operand": {
                "type": "UNOP",
                "op": "-",
                "operand": {"type": "VAR", "name": "y"}
            }
        }
        
        result = _generate_unop_code(expr, self.func_name, self.var_offsets)
        
        mock_gen_expr.assert_called_once_with(
            {
                "type": "UNOP",
                "op": "-",
                "operand": {"type": "VAR", "name": "y"}
            },
            self.func_name,
            self.var_offsets
        )
        self.assertEqual(
            result,
            "ldr x0, [sp, #8]\nneg x0, x0\ncmp x0, #0\ncset x0, eq\n"
        )

    @patch("._generate_unop_code_package._generate_unop_code_src.generate_expression_code")
    def test_unsupported_operator(self, mock_gen_expr):
        """Test ValueError for unsupported unary operator."""
        mock_gen_expr.return_value = "mov x0, #5\n"
        
        expr = {
            "type": "UNOP",
            "op": "~",
            "operand": {"type": "CONST", "value": 5}
        }
        
        with self.assertRaises(ValueError) as context:
            _generate_unop_code(expr, self.func_name, self.var_offsets)
        
        self.assertIn("Unsupported unary operator: '~'", str(context.exception))
        mock_gen_expr.assert_called_once()

    def test_missing_op_field(self):
        """Test KeyError when 'op' field is missing."""
        expr = {
            "type": "UNOP",
            "operand": {"type": "CONST", "value": 1}
        }
        
        with self.assertRaises(KeyError):
            _generate_unop_code(expr, self.func_name, self.var_offsets)

    def test_missing_operand_field(self):
        """Test KeyError when 'operand' field is missing."""
        expr = {
            "type": "UNOP",
            "op": "-"
        }
        
        with self.assertRaises(KeyError):
            _generate_unop_code(expr, self.func_name, self.var_offsets)

    @patch("._generate_unop_code_package._generate_unop_code_src.generate_expression_code")
    def test_empty_var_offsets(self, mock_gen_expr):
        """Test with empty variable offsets dictionary."""
        mock_gen_expr.return_value = "mov x0, #42\n"
        
        expr = {
            "type": "UNOP",
            "op": "-",
            "operand": {"type": "CONST", "value": 42}
        }
        
        result = _generate_unop_code(expr, self.func_name, {})
        
        mock_gen_expr.assert_called_once_with(
            {"type": "CONST", "value": 42},
            self.func_name,
            {}
        )
        self.assertEqual(result, "mov x0, #42\nneg x0, x0\n")

    @patch("._generate_unop_code_package._generate_unop_code_src.generate_expression_code")
    def test_multiple_calls_independence(self, mock_gen_expr):
        """Test that multiple calls are independent."""
        mock_gen_expr.side_effect = [
            "ldr x0, [sp, #0]\n",
            "ldr x0, [sp, #8]\n"
        ]
        
        expr1 = {"type": "UNOP", "op": "-", "operand": {"type": "VAR", "name": "x"}}
        expr2 = {"type": "UNOP", "op": "!", "operand": {"type": "VAR", "name": "y"}}
        
        result1 = _generate_unop_code(expr1, self.func_name, self.var_offsets)
        result2 = _generate_unop_code(expr2, self.func_name, self.var_offsets)
        
        self.assertEqual(result1, "ldr x0, [sp, #0]\nneg x0, x0\n")
        self.assertEqual(result2, "ldr x0, [sp, #8]\ncmp x0, #0\ncset x0, eq\n")
        self.assertEqual(mock_gen_expr.call_count, 2)


if __name__ == "__main__":
    unittest.main()

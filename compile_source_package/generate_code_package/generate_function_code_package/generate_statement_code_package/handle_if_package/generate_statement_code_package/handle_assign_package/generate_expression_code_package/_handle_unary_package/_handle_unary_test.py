import unittest
from unittest.mock import patch

# Relative import from the same package
from ._handle_unary_src import _handle_unary


class TestHandleUnary(unittest.TestCase):
    """Test cases for _handle_unary function."""

    def setUp(self):
        """Set up test fixtures."""
        self.var_offsets = {"x": 0, "y": 1}
        self.next_offset = 2

    @patch('generate_expression_code_package._handle_unary_package._handle_unary_src.generate_expression_code')
    def test_negation_operator(self, mock_gen_code):
        """Test unary negation operator '-'."""
        mock_gen_code.return_value = ("    ldr x1, [sp, #0]", 2, "x1")

        expr = {"op": "-", "operand": {"type": "IDENT", "name": "x"}}

        code, offset, reg = _handle_unary(expr, self.var_offsets, self.next_offset)

        # Verify generate_expression_code was called correctly
        mock_gen_code.assert_called_once_with(
            {"type": "IDENT", "name": "x"},
            self.var_offsets,
            self.next_offset
        )

        # Verify output
        self.assertIn("ldr x1, [sp, #0]", code)
        self.assertIn("mov x0, x1", code)
        self.assertIn("neg x0, x0", code)
        self.assertEqual(offset, 2)
        self.assertEqual(reg, "x0")

    @patch('generate_expression_code_package._handle_unary_package._handle_unary_src.generate_expression_code')
    def test_logical_not_operator(self, mock_gen_code):
        """Test unary logical not operator '!'."""
        mock_gen_code.return_value = ("    ldr x1, [sp, #0]", 3, "x1")

        expr = {"op": "!", "operand": {"type": "LITERAL", "value": 5}}

        code, offset, reg = _handle_unary(expr, self.var_offsets, self.next_offset)

        # Verify generate_expression_code was called correctly
        mock_gen_code.assert_called_once_with(
            {"type": "LITERAL", "value": 5},
            self.var_offsets,
            self.next_offset
        )

        # Verify output
        self.assertIn("ldr x1, [sp, #0]", code)
        self.assertIn("mov x0, x1", code)
        self.assertIn("cmp x0, #0", code)
        self.assertIn("cset x0, eq", code)
        self.assertEqual(offset, 3)
        self.assertEqual(reg, "x0")

    @patch('generate_expression_code_package._handle_unary_package._handle_unary_src.generate_expression_code')
    def test_operand_already_in_x0(self, mock_gen_code):
        """Test when operand is already in x0 register (no mov needed)."""
        mock_gen_code.return_value = ("    some_code", 2, "x0")

        expr = {"op": "-", "operand": {"type": "LITERAL", "value": 10}}

        code, offset, reg = _handle_unary(expr, self.var_offsets, self.next_offset)

        # Should not have mov instruction since already in x0
        self.assertNotIn("mov x0", code)
        self.assertIn("some_code", code)
        self.assertIn("neg x0, x0", code)
        self.assertEqual(offset, 2)
        self.assertEqual(reg, "x0")

    @patch('generate_expression_code_package._handle_unary_package._handle_unary_src.generate_expression_code')
    def test_unsupported_operator(self, mock_gen_code):
        """Test that unsupported operator raises ValueError."""
        mock_gen_code.return_value = ("    code", 2, "x1")

        expr = {"op": "~", "operand": {"type": "LITERAL", "value": 5}}

        with self.assertRaises(ValueError) as context:
            _handle_unary(expr, self.var_offsets, self.next_offset)

        self.assertIn("Unsupported unary operator: ~", str(context.exception))

    @patch('generate_expression_code_package._handle_unary_package._handle_unary_src.generate_expression_code')
    def test_nested_unary_expression(self, mock_gen_code):
        """Test nested unary expression handling."""
        # First call for inner operand
        # Second call for outer operand (the inner unary result)
        mock_gen_code.side_effect = [
            ("    ldr x1, [sp, #0]", 2, "x1"),  # Inner literal
            ("    neg x0, x0", 2, "x0")  # Inner unary result
        ]

        expr = {
            "op": "!",
            "operand": {
                "op": "-",
                "operand": {"type": "LITERAL", "value": 5}
            }
        }

        code, offset, reg = _handle_unary(expr, self.var_offsets, self.next_offset)

        # Verify generate_expression_code was called twice (nested)
        self.assertEqual(mock_gen_code.call_count, 2)

        # Verify output contains logical not operations
        self.assertIn("cmp x0, #0", code)
        self.assertIn("cset x0, eq", code)
        self.assertEqual(offset, 2)
        self.assertEqual(reg, "x0")

    @patch('generate_expression_code_package._handle_unary_package._handle_unary_src.generate_expression_code')
    def test_empty_operand_code(self, mock_gen_code):
        """Test when operand generates empty code."""
        mock_gen_code.return_value = ("", 2, "x1")

        expr = {"op": "-", "operand": {"type": "LITERAL", "value": 0}}

        code, offset, reg = _handle_unary(expr, self.var_offsets, self.next_offset)

        # Should still have neg instruction
        self.assertIn("mov x0, x1", code)
        self.assertIn("neg x0, x0", code)
        self.assertEqual(offset, 2)
        self.assertEqual(reg, "x0")

    @patch('generate_expression_code_package._handle_unary_package._handle_unary_src.generate_expression_code')
    def test_negation_with_x0_no_extra_mov(self, mock_gen_code):
        """Test negation when operand already returns x0, no mov needed."""
        mock_gen_code.return_value = ("    cmp x0, #5", 2, "x0")

        expr = {"op": "-", "operand": {"type": "BINARY", "op": "+", "left": {"type": "LITERAL", "value": 2}, "right": {"type": "LITERAL", "value": 3}}}

        code, offset, reg = _handle_unary(expr, self.var_offsets, self.next_offset)

        # Should not have mov since operand is already in x0
        self.assertNotIn("mov x0", code)
        self.assertIn("cmp x0, #5", code)
        self.assertIn("neg x0, x0", code)
        self.assertEqual(offset, 2)
        self.assertEqual(reg, "x0")

    @patch('generate_expression_code_package._handle_unary_package._handle_unary_src.generate_expression_code')
    def test_logical_not_with_x0_no_extra_mov(self, mock_gen_code):
        """Test logical not when operand already returns x0, no mov needed."""
        mock_gen_code.return_value = ("    ldr x0, [sp, #0]", 2, "x0")

        expr = {"op": "!", "operand": {"type": "IDENT", "name": "flag"}}

        code, offset, reg = _handle_unary(expr, self.var_offsets, self.next_offset)

        # Should not have mov since operand is already in x0
        self.assertNotIn("mov x0", code)
        self.assertIn("ldr x0, [sp, #0]", code)
        self.assertIn("cmp x0, #0", code)
        self.assertIn("cset x0, eq", code)
        self.assertEqual(offset, 2)
        self.assertEqual(reg, "x0")


if __name__ == '__main__':
    unittest.main()

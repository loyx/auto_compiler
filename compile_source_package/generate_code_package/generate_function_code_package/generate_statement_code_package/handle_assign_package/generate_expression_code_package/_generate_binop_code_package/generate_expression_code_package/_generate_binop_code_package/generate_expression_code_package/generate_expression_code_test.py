import unittest
from unittest.mock import patch

# Relative import from the same package
from .generate_expression_code_src import generate_expression_code


class TestGenerateExpressionCode(unittest.TestCase):
    """Unit tests for generate_expression_code function."""

    @patch('generate_expression_code_package._generate_binop_code_package.generate_expression_code_package._generate_binop_code_package.generate_expression_code_package.generate_binop_code_package.generate_binop_code_src.generate_binop_code')
    def test_binop_delegates_to_generate_binop_code(self, mock_generate_binop_code):
        """Test BINOP expression delegates to generate_binop_code."""
        mock_generate_binop_code.return_value = "add x0, x1, x2"
        expr = {
            "type": "BINOP",
            "op": "+",
            "left": {"type": "VAR", "name": "a"},
            "right": {"type": "VAR", "name": "b"}
        }
        var_offsets = {"a": 0, "b": 8}
        
        result = generate_expression_code(expr, "test_func", var_offsets)
        
        self.assertEqual(result, "add x0, x1, x2")
        mock_generate_binop_code.assert_called_once_with(expr, "test_func", var_offsets)

    def test_var_valid_variable(self):
        """Test VAR expression with valid variable name."""
        expr = {"type": "VAR", "name": "x"}
        var_offsets = {"x": 16}
        
        result = generate_expression_code(expr, "test_func", var_offsets)
        
        self.assertEqual(result, "ldr x0, [sp, #16]")

    def test_var_missing_name_field(self):
        """Test VAR expression missing 'name' field raises ValueError."""
        expr = {"type": "VAR"}
        var_offsets = {"x": 0}
        
        with self.assertRaises(ValueError) as context:
            generate_expression_code(expr, "test_func", var_offsets)
        
        self.assertIn("missing 'name' field", str(context.exception))

    def test_var_undefined_variable(self):
        """Test VAR expression with undefined variable raises ValueError."""
        expr = {"type": "VAR", "name": "undefined_var"}
        var_offsets = {"x": 0}
        
        with self.assertRaises(ValueError) as context:
            generate_expression_code(expr, "test_func", var_offsets)
        
        self.assertIn("Undefined variable: undefined_var", str(context.exception))

    def test_literal_positive_small(self):
        """Test literal with small positive value (<= 65535)."""
        expr = {"type": "LITERAL", "value": 100}
        result = generate_expression_code(expr, "test_func", {})
        self.assertEqual(result, "movz x0, #100")

    def test_literal_positive_large(self):
        """Test literal with large positive value (> 65535)."""
        expr = {"type": "LITERAL", "value": 70000}
        result = generate_expression_code(expr, "test_func", {})
        # 70000 = 0x11170, upper = 1, lower = 69488
        expected = "movz x0, #1, lsl #16\nmovk x0, #69488"
        self.assertEqual(result, expected)

    def test_literal_zero(self):
        """Test literal with zero value."""
        expr = {"type": "LITERAL", "value": 0}
        result = generate_expression_code(expr, "test_func", {})
        self.assertEqual(result, "movz x0, #0")

    def test_literal_negative_small(self):
        """Test literal with small negative value (>= -65536)."""
        expr = {"type": "LITERAL", "value": -100}
        result = generate_expression_code(expr, "test_func", {})
        # movn x0, #99 (movn sets bits to inverse, so -100 = ~99)
        self.assertEqual(result, "movn x0, #99")

    def test_literal_negative_large(self):
        """Test literal with large negative value (< -65536)."""
        expr = {"type": "LITERAL", "value": -70000}
        result = generate_expression_code(expr, "test_func", {})
        # For -70000: movz x0, #65535, lsl #16 then orr with lower bits
        expected = "movz x0, #65535, lsl #16\norr x0, x0, #61071"
        self.assertEqual(result, expected)

    def test_literal_missing_value_field(self):
        """Test literal expression missing 'value' field raises ValueError."""
        expr = {"type": "LITERAL"}
        
        with self.assertRaises(ValueError) as context:
            generate_expression_code(expr, "test_func", {})
        
        self.assertIn("missing 'value' field", str(context.exception))

    def test_unsupported_expression_type(self):
        """Test unsupported expression type raises ValueError."""
        expr = {"type": "UNKNOWN"}
        
        with self.assertRaises(ValueError) as context:
            generate_expression_code(expr, "test_func", {})
        
        self.assertIn("Unsupported expression type: UNKNOWN", str(context.exception))

    def test_empty_expression_type(self):
        """Test expression with empty/missing type field raises ValueError."""
        expr = {}
        
        with self.assertRaises(ValueError) as context:
            generate_expression_code(expr, "test_func", {})
        
        self.assertIn("Unsupported expression type: None", str(context.exception))


if __name__ == "__main__":
    unittest.main()

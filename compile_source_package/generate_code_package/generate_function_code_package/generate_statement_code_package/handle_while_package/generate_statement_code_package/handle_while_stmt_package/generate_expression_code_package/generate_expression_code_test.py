# -*- coding: utf-8 -*-
"""Unit tests for generate_expression_code function."""

import unittest
from unittest.mock import patch

from .generate_expression_code_src import generate_expression_code


class TestGenerateExpressionCode(unittest.TestCase):
    """Test cases for generate_expression_code function."""

    def test_literal_expression(self):
        """Test literal expression routes to generate_literal_code."""
        expr = {"type": "literal", "value": 42}
        var_offsets = {"x": 0}
        next_offset = 16
        
        with patch("generate_expression_code_package.generate_literal_code_package.generate_literal_code_src.generate_literal_code") as mock_literal:
            mock_literal.return_value = ("mov x0, #42", 16)
            
            code, offset = generate_expression_code(expr, var_offsets, next_offset)
            
            mock_literal.assert_called_once_with(42, 16)
            self.assertEqual(code, "mov x0, #42")
            self.assertEqual(offset, 16)

    def test_variable_expression(self):
        """Test variable expression routes to generate_variable_code."""
        expr = {"type": "variable", "var_name": "counter"}
        var_offsets = {"counter": 8}
        next_offset = 16
        
        with patch("generate_expression_code_package.generate_variable_code_package.generate_variable_code_src.generate_variable_code") as mock_variable:
            mock_variable.return_value = ("ldr x0, [sp, #8]", 16)
            
            code, offset = generate_expression_code(expr, var_offsets, next_offset)
            
            mock_variable.assert_called_once_with("counter", var_offsets, 16)
            self.assertEqual(code, "ldr x0, [sp, #8]")
            self.assertEqual(offset, 16)

    def test_binary_op_expression(self):
        """Test binary_op expression routes to generate_binary_op_code."""
        expr = {
            "type": "binary_op",
            "left": {"type": "literal", "value": 5},
            "right": {"type": "literal", "value": 3},
            "operator": "+"
        }
        var_offsets = {}
        next_offset = 16
        
        with patch("generate_expression_code_package.generate_binary_op_code_package.generate_binary_op_code_src.generate_binary_op_code") as mock_binary:
            mock_binary.return_value = ("mov x0, #5\nmov x1, #3\nadd x0, x0, x1", 24)
            
            code, offset = generate_expression_code(expr, var_offsets, next_offset)
            
            mock_binary.assert_called_once_with(
                {"type": "literal", "value": 5},
                {"type": "literal", "value": 3},
                "+",
                var_offsets,
                16
            )
            self.assertEqual(code, "mov x0, #5\nmov x1, #3\nadd x0, x0, x1")
            self.assertEqual(offset, 24)

    def test_unary_op_expression(self):
        """Test unary_op expression routes to generate_unary_op_code."""
        expr = {
            "type": "unary_op",
            "operand": {"type": "literal", "value": 10},
            "operator": "-"
        }
        var_offsets = {}
        next_offset = 16
        
        with patch("generate_expression_code_package.generate_unary_op_code_package.generate_unary_op_code_src.generate_unary_op_code") as mock_unary:
            mock_unary.return_value = ("mov x0, #10\nneg x0, x0", 24)
            
            code, offset = generate_expression_code(expr, var_offsets, next_offset)
            
            mock_unary.assert_called_once_with(
                {"type": "literal", "value": 10},
                "-",
                var_offsets,
                16
            )
            self.assertEqual(code, "mov x0, #10\nneg x0, x0")
            self.assertEqual(offset, 24)

    def test_comparison_expression(self):
        """Test comparison expression routes to generate_comparison_code."""
        expr = {
            "type": "comparison",
            "left": {"type": "variable", "var_name": "a"},
            "right": {"type": "variable", "var_name": "b"},
            "operator": ">"
        }
        var_offsets = {"a": 0, "b": 8}
        next_offset = 16
        
        with patch("generate_expression_code_package.generate_comparison_code_package.generate_comparison_code_src.generate_comparison_code") as mock_comparison:
            mock_comparison.return_value = ("ldr x0, [sp, #0]\nldr x1, [sp, #8]\ncmp x0, x1\ncset x0, gt", 24)
            
            code, offset = generate_expression_code(expr, var_offsets, next_offset)
            
            mock_comparison.assert_called_once_with(
                {"type": "variable", "var_name": "a"},
                {"type": "variable", "var_name": "b"},
                ">",
                var_offsets,
                16
            )
            self.assertEqual(code, "ldr x0, [sp, #0]\nldr x1, [sp, #8]\ncmp x0, x1\ncset x0, gt")
            self.assertEqual(offset, 24)

    def test_and_expression(self):
        """Test 'and' logical expression routes to generate_logical_code."""
        expr = {
            "type": "and",
            "left": {"type": "literal", "value": 1},
            "right": {"type": "literal", "value": 0}
        }
        var_offsets = {}
        next_offset = 16
        
        with patch("generate_expression_code_package.generate_logical_code_package.generate_logical_code_src.generate_logical_code") as mock_logical:
            mock_logical.return_value = ("mov x0, #1\ncbz x0, L0\nmov x0, #0", 16, 1)
            
            code, offset = generate_expression_code(expr, var_offsets, next_offset)
            
            mock_logical.assert_called_once_with(
                {"type": "literal", "value": 1},
                {"type": "literal", "value": 0},
                "and",
                var_offsets,
                16,
                0
            )
            self.assertEqual(code, "mov x0, #1\ncbz x0, L0\nmov x0, #0")
            self.assertEqual(offset, 16)

    def test_or_expression(self):
        """Test 'or' logical expression routes to generate_logical_code."""
        expr = {
            "type": "or",
            "left": {"type": "literal", "value": 0},
            "right": {"type": "literal", "value": 1}
        }
        var_offsets = {}
        next_offset = 16
        
        with patch("generate_expression_code_package.generate_logical_code_package.generate_logical_code_src.generate_logical_code") as mock_logical:
            mock_logical.return_value = ("mov x0, #0\ncbnz x0, L0\nmov x0, #1", 16, 1)
            
            code, offset = generate_expression_code(expr, var_offsets, next_offset)
            
            mock_logical.assert_called_once_with(
                {"type": "literal", "value": 0},
                {"type": "literal", "value": 1},
                "or",
                var_offsets,
                16,
                0
            )
            self.assertEqual(code, "mov x0, #0\ncbnz x0, L0\nmov x0, #1")
            self.assertEqual(offset, 16)

    def test_unknown_expression_type_raises_error(self):
        """Test unknown expression type raises ValueError."""
        expr = {"type": "unknown_type", "value": 42}
        var_offsets = {}
        next_offset = 16
        
        with self.assertRaises(ValueError) as context:
            generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertIn("Unknown expression type: unknown_type", str(context.exception))

    def test_literal_with_boolean_value(self):
        """Test literal expression with boolean value."""
        expr = {"type": "literal", "value": True}
        var_offsets = {}
        next_offset = 16
        
        with patch("generate_expression_code_package.generate_literal_code_package.generate_literal_code_src.generate_literal_code") as mock_literal:
            mock_literal.return_value = ("mov x0, #1", 16)
            
            code, offset = generate_expression_code(expr, var_offsets, next_offset)
            
            mock_literal.assert_called_once_with(True, 16)
            self.assertEqual(code, "mov x0, #1")
            self.assertEqual(offset, 16)

    def test_complex_nested_expression(self):
        """Test complex nested expression with multiple levels."""
        expr = {
            "type": "binary_op",
            "left": {
                "type": "comparison",
                "left": {"type": "variable", "var_name": "x"},
                "right": {"type": "literal", "value": 10},
                "operator": ">"
            },
            "right": {"type": "literal", "value": 5},
            "operator": "*"
        }
        var_offsets = {"x": 0}
        next_offset = 16
        
        # The function should route to generate_binary_op_code with the nested structures
        with patch("generate_expression_code_package.generate_binary_op_code_package.generate_binary_op_code_src.generate_binary_op_code") as mock_binary:
            mock_binary.return_value = ("complex code here", 32)
            
            code, offset = generate_expression_code(expr, var_offsets, next_offset)
            
            mock_binary.assert_called_once()
            # Verify the left operand is the comparison dict
            call_args = mock_binary.call_args
            self.assertEqual(call_args[0][0]["type"], "comparison")
            self.assertEqual(call_args[0][2], "*")
            self.assertEqual(code, "complex code here")
            self.assertEqual(offset, 32)


if __name__ == "__main__":
    unittest.main()

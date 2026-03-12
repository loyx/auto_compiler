# === std / third-party imports ===
import unittest
from unittest.mock import patch

# === relative import for tested module ===
from .generate_expression_code_src import generate_expression_code


class TestGenerateExpressionCode(unittest.TestCase):
    """Test cases for generate_expression_code dispatcher function."""

    def test_dispatch_literal_expression(self):
        """Test LITERAL expression type dispatches to generate_literal_code."""
        expr = {"type": "LITERAL", "value": 42, "literal_type": "int"}
        func_name = "test_func"
        label_counter = {"counter": 0}
        var_offsets = {"x": 0}
        next_offset = 5

        with patch("generate_expression_code_package.generate_unary_op_code_package.generate_expression_code_package.generate_literal_code_package.generate_literal_code_src.generate_literal_code") as mock_literal:
            mock_literal.return_value = ("mov x0, #42", 5)
            
            code, updated_offset = generate_expression_code(
                expr, func_name, label_counter, var_offsets, next_offset
            )
            
            mock_literal.assert_called_once_with(expr, next_offset)
            self.assertEqual(code, "mov x0, #42")
            self.assertEqual(updated_offset, 5)

    def test_dispatch_identifier_expression(self):
        """Test IDENTIFIER expression type dispatches to generate_identifier_code."""
        expr = {"type": "IDENTIFIER", "name": "my_var"}
        func_name = "test_func"
        label_counter = {"counter": 0}
        var_offsets = {"my_var": 0}
        next_offset = 5

        with patch("generate_expression_code_package.generate_unary_op_code_package.generate_expression_code_package.generate_literal_code_package.generate_identifier_code_package.generate_identifier_code_src.generate_identifier_code") as mock_identifier:
            mock_identifier.return_value = ("ldr x0, [sp, #0]", 5)
            
            code, updated_offset = generate_expression_code(
                expr, func_name, label_counter, var_offsets, next_offset
            )
            
            mock_identifier.assert_called_once_with(expr, var_offsets, next_offset)
            self.assertEqual(code, "ldr x0, [sp, #0]")
            self.assertEqual(updated_offset, 5)

    def test_dispatch_binary_op_expression(self):
        """Test BINARY_OP expression type dispatches to generate_binary_op_code."""
        expr = {"type": "BINARY_OP", "operator": "+", "left": {"type": "LITERAL", "value": 1}, "right": {"type": "LITERAL", "value": 2}}
        func_name = "test_func"
        label_counter = {"counter": 0}
        var_offsets = {"x": 0}
        next_offset = 5

        with patch("generate_expression_code_package.generate_unary_op_code_package.generate_expression_code_package.generate_literal_code_package.generate_identifier_code_package.generate_binary_op_code_package.generate_binary_op_code_src.generate_binary_op_code") as mock_binary:
            mock_binary.return_value = ("add x0, x1, x2", 7)
            
            code, updated_offset = generate_expression_code(
                expr, func_name, label_counter, var_offsets, next_offset
            )
            
            mock_binary.assert_called_once_with(expr, func_name, label_counter, var_offsets, next_offset)
            self.assertEqual(code, "add x0, x1, x2")
            self.assertEqual(updated_offset, 7)

    def test_dispatch_unary_op_expression(self):
        """Test UNARY_OP expression type dispatches to generate_unary_op_code."""
        expr = {"type": "UNARY_OP", "operator": "-", "operand": {"type": "LITERAL", "value": 5}}
        func_name = "test_func"
        label_counter = {"counter": 0}
        var_offsets = {"x": 0}
        next_offset = 5

        with patch("generate_expression_code_package.generate_unary_op_code_package.generate_unary_op_code_src.generate_unary_op_code") as mock_unary:
            mock_unary.return_value = ("neg x0, x1", 6)
            
            code, updated_offset = generate_expression_code(
                expr, func_name, label_counter, var_offsets, next_offset
            )
            
            mock_unary.assert_called_once_with(expr, func_name, label_counter, var_offsets, next_offset)
            self.assertEqual(code, "neg x0, x1")
            self.assertEqual(updated_offset, 6)

    def test_dispatch_call_expression(self):
        """Test CALL expression type dispatches to generate_call_code."""
        expr = {"type": "CALL", "function": {"type": "IDENTIFIER", "name": "foo"}, "arguments": []}
        func_name = "test_func"
        label_counter = {"counter": 0}
        var_offsets = {"x": 0}
        next_offset = 5

        with patch("generate_expression_code_package.generate_unary_op_code_package.generate_expression_code_package.generate_literal_code_package.generate_identifier_code_package.generate_binary_op_code_package.generate_call_code_package.generate_call_code_src.generate_call_code") as mock_call:
            mock_call.return_value = ("bl foo", 5)
            
            code, updated_offset = generate_expression_code(
                expr, func_name, label_counter, var_offsets, next_offset
            )
            
            mock_call.assert_called_once_with(expr, func_name, label_counter, var_offsets, next_offset)
            self.assertEqual(code, "bl foo")
            self.assertEqual(updated_offset, 5)

    def test_unknown_expression_type_raises_valueerror(self):
        """Test that unknown expression type raises ValueError."""
        expr = {"type": "UNKNOWN_TYPE"}
        func_name = "test_func"
        label_counter = {"counter": 0}
        var_offsets = {"x": 0}
        next_offset = 5

        with self.assertRaises(ValueError) as context:
            generate_expression_code(expr, func_name, label_counter, var_offsets, next_offset)
        
        self.assertIn("Unknown expression type: UNKNOWN_TYPE", str(context.exception))

    def test_empty_type_field_raises_valueerror(self):
        """Test that empty type field raises ValueError."""
        expr = {"type": ""}
        func_name = "test_func"
        label_counter = {"counter": 0}
        var_offsets = {"x": 0}
        next_offset = 5

        with self.assertRaises(ValueError) as context:
            generate_expression_code(expr, func_name, label_counter, var_offsets, next_offset)
        
        self.assertIn("Unknown expression type:", str(context.exception))

    def test_missing_type_field_raises_valueerror(self):
        """Test that missing type field raises ValueError."""
        expr = {"value": 42}
        func_name = "test_func"
        label_counter = {"counter": 0}
        var_offsets = {"x": 0}
        next_offset = 5

        with self.assertRaises(ValueError) as context:
            generate_expression_code(expr, func_name, label_counter, var_offsets, next_offset)
        
        self.assertIn("Unknown expression type:", str(context.exception))

    def test_label_counter_mutable_for_binary_op(self):
        """Test that label_counter can be modified in-place for BINARY_OP (short-circuit operators)."""
        expr = {"type": "BINARY_OP", "operator": "&&", "left": {"type": "LITERAL", "value": 1}, "right": {"type": "LITERAL", "value": 2}}
        func_name = "test_func"
        label_counter = {"counter": 0}
        var_offsets = {"x": 0}
        next_offset = 5

        def side_effect(e, fn, lc, vo, no):
            lc["counter"] = 2
            return ("cmp x0, #0", 5)

        with patch("generate_expression_code_package.generate_unary_op_code_package.generate_expression_code_package.generate_literal_code_package.generate_identifier_code_package.generate_binary_op_code_package.generate_binary_op_code_src.generate_binary_op_code") as mock_binary:
            mock_binary.side_effect = side_effect
            
            code, updated_offset = generate_expression_code(
                expr, func_name, label_counter, var_offsets, next_offset
            )
            
            self.assertEqual(label_counter["counter"], 2)
            self.assertEqual(code, "cmp x0, #0")

    def test_all_parameters_passed_correctly(self):
        """Test that all parameters are passed correctly to sub-functions."""
        expr = {"type": "CALL", "function": {"type": "IDENTIFIER", "name": "bar"}, "arguments": [{"type": "LITERAL", "value": 10}]}
        func_name = "caller_func"
        label_counter = {"counter": 5}
        var_offsets = {"param1": 0, "param2": 1}
        next_offset = 10

        with patch("generate_expression_code_package.generate_unary_op_code_package.generate_expression_code_package.generate_literal_code_package.generate_identifier_code_package.generate_binary_op_code_package.generate_call_code_package.generate_call_code_src.generate_call_code") as mock_call:
            mock_call.return_value = ("bl bar", 10)
            
            generate_expression_code(expr, func_name, label_counter, var_offsets, next_offset)
            
            mock_call.assert_called_once()
            call_args = mock_call.call_args
            self.assertEqual(call_args[0][0], expr)
            self.assertEqual(call_args[0][1], func_name)
            self.assertEqual(call_args[0][2], label_counter)
            self.assertEqual(call_args[0][3], var_offsets)
            self.assertEqual(call_args[0][4], next_offset)


if __name__ == "__main__":
    unittest.main()

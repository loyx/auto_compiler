# -*- coding: utf-8 -*-
"""Unit tests for generate_expression_code function."""

import unittest
from unittest.mock import patch

from .generate_expression_code_src import generate_expression_code

# Patch paths for sub-functions
PATCH_LITERAL = "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_literal_code_package.generate_literal_code_src.generate_literal_code"
PATCH_IDENTIFIER = "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_identifier_code_package.generate_identifier_code_src.generate_identifier_code"
PATCH_BINARY_OP = "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_binary_op_code_package.generate_binary_op_code_src.generate_binary_op_code"
PATCH_UNARY_OP = "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_unary_op_code_package.generate_unary_op_code_src.generate_unary_op_code"
PATCH_CALL = "main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_call_code_package.generate_call_code_src.generate_call_code"


class TestGenerateExpressionCode(unittest.TestCase):
    """Test cases for generate_expression_code function."""

    def setUp(self):
        """Set up common test fixtures."""
        self.func_name = "test_func"
        self.label_counter = {"for_cond": 0, "skip": 0}
        self.var_offsets = {"x": 0, "y": 8}
        self.next_offset = 16

    def test_literal_expression_int(self):
        """Test LITERAL expression with integer value."""
        expr = {"type": "LITERAL", "value": 42, "literal_type": "int"}
        
        with patch(PATCH_LITERAL) as mock_literal:
            mock_literal.return_value = ("mov x0, #42", 16)
            
            code, offset = generate_expression_code(expr, self.func_name, self.label_counter, self.var_offsets, self.next_offset)
            
            self.assertEqual(code, "mov x0, #42")
            self.assertEqual(offset, 16)
            mock_literal.assert_called_once_with(expr, self.next_offset)

    def test_literal_expression_bool(self):
        """Test LITERAL expression with boolean value."""
        expr = {"type": "LITERAL", "value": True, "literal_type": "bool"}
        
        with patch(PATCH_LITERAL) as mock_literal:
            mock_literal.return_value = ("mov x0, #1", 16)
            
            code, offset = generate_expression_code(expr, self.func_name, self.label_counter, self.var_offsets, self.next_offset)
            
            self.assertEqual(code, "mov x0, #1")
            mock_literal.assert_called_once()

    def test_identifier_expression(self):
        """Test IDENTIFIER expression."""
        expr = {"type": "IDENTIFIER", "name": "x"}
        
        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_expression_code_src.generate_identifier_code") as mock_identifier:
            mock_identifier.return_value = ("ldr x0, [sp, #0]", 16)
            
            code, offset = generate_expression_code(expr, self.func_name, self.label_counter, self.var_offsets, self.next_offset)
            
            self.assertEqual(code, "ldr x0, [sp, #0]")
            mock_identifier.assert_called_once_with(expr, self.var_offsets, self.next_offset)

    def test_binary_op_expression(self):
        """Test BINARY_OP expression."""
        expr = {
            "type": "BINARY_OP",
            "operator": "+",
            "left": {"type": "IDENTIFIER", "name": "x"},
            "right": {"type": "LITERAL", "value": 1, "literal_type": "int"}
        }
        
        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_expression_code_src.generate_binary_op_code") as mock_binary:
            mock_binary.return_value = ("mov x0, #1\nadd x0, x0, x1", 16)
            
            code, offset = generate_expression_code(expr, self.func_name, self.label_counter, self.var_offsets, self.next_offset)
            
            self.assertEqual(code, "mov x0, #1\nadd x0, x0, x1")
            mock_binary.assert_called_once_with(expr, self.func_name, self.label_counter, self.var_offsets, self.next_offset)

    def test_unary_op_expression(self):
        """Test UNARY_OP expression."""
        expr = {
            "type": "UNARY_OP",
            "operator": "-",
            "operand": {"type": "IDENTIFIER", "name": "x"}
        }
        
        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_expression_code_src.generate_unary_op_code") as mock_unary:
            mock_unary.return_value = ("neg x0, x0", 16)
            
            code, offset = generate_expression_code(expr, self.func_name, self.label_counter, self.var_offsets, self.next_offset)
            
            self.assertEqual(code, "neg x0, x0")
            mock_unary.assert_called_once_with(expr, self.var_offsets, self.next_offset)

    def test_call_expression(self):
        """Test CALL expression."""
        expr = {
            "type": "CALL",
            "callee": "printf",
            "args": [
                {"type": "LITERAL", "value": 42, "literal_type": "int"}
            ]
        }
        
        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_expression_code_src.generate_call_code") as mock_call:
            mock_call.return_value = ("mov x0, #42\nbl printf", 16)
            
            code, offset = generate_expression_code(expr, self.func_name, self.label_counter, self.var_offsets, self.next_offset)
            
            self.assertEqual(code, "mov x0, #42\nbl printf")
            mock_call.assert_called_once_with(expr, self.func_name, self.label_counter, self.var_offsets, self.next_offset)

    def test_unknown_expression_type(self):
        """Test that unknown expression type raises ValueError."""
        expr = {"type": "UNKNOWN_TYPE"}
        
        with self.assertRaises(ValueError) as context:
            generate_expression_code(expr, self.func_name, self.label_counter, self.var_offsets, self.next_offset)
        
        self.assertIn("Unknown expression type: UNKNOWN_TYPE", str(context.exception))

    def test_label_counter_not_modified_for_simple_exprs(self):
        """Test that label_counter is not modified for simple expressions."""
        expr = {"type": "LITERAL", "value": 10, "literal_type": "int"}
        original_counter = self.label_counter.copy()
        
        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_expression_code_src.generate_literal_code") as mock_literal:
            mock_literal.return_value = ("mov x0, #10", 16)
            
            generate_expression_code(expr, self.func_name, self.label_counter, self.var_offsets, self.next_offset)
            
            mock_literal.assert_called_once()

    def test_var_offsets_passed_correctly(self):
        """Test that var_offsets is passed correctly to sub-functions."""
        expr = {"type": "IDENTIFIER", "name": "y"}
        
        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_expression_code_src.generate_identifier_code") as mock_identifier:
            mock_identifier.return_value = ("ldr x0, [sp, #8]", 16)
            
            generate_expression_code(expr, self.func_name, self.label_counter, self.var_offsets, self.next_offset)
            
            mock_identifier.assert_called_once()
            call_args = mock_identifier.call_args
            self.assertEqual(call_args[0][1], self.var_offsets)

    def test_next_offset_passed_correctly(self):
        """Test that next_offset is passed correctly to sub-functions."""
        expr = {"type": "LITERAL", "value": 100, "literal_type": "int"}
        
        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_expression_code_src.generate_literal_code") as mock_literal:
            mock_literal.return_value = ("mov x0, #100", 20)
            
            code, offset = generate_expression_code(expr, self.func_name, self.label_counter, self.var_offsets, self.next_offset)
            
            mock_literal.assert_called_once_with(expr, self.next_offset)
            self.assertEqual(offset, 20)

    def test_func_name_passed_to_binary_and_call(self):
        """Test that func_name is passed to binary_op and call sub-functions."""
        binary_expr = {
            "type": "BINARY_OP",
            "operator": "+",
            "left": {"type": "LITERAL", "value": 1, "literal_type": "int"},
            "right": {"type": "LITERAL", "value": 2, "literal_type": "int"}
        }
        
        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_expression_code_src.generate_binary_op_code") as mock_binary:
            mock_binary.return_value = ("add x0, x0, x1", 16)
            
            generate_expression_code(binary_expr, self.func_name, self.label_counter, self.var_offsets, self.next_offset)
            
            mock_binary.assert_called_once()
            self.assertEqual(mock_binary.call_args[0][1], self.func_name)

    def test_return_type_is_tuple(self):
        """Test that return value is a tuple of (str, int)."""
        expr = {"type": "LITERAL", "value": 5, "literal_type": "int"}
        
        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_expression_code_src.generate_literal_code") as mock_literal:
            mock_literal.return_value = ("mov x0, #5", 16)
            
            result = generate_expression_code(expr, self.func_name, self.label_counter, self.var_offsets, self.next_offset)
            
            self.assertIsInstance(result, tuple)
            self.assertEqual(len(result), 2)
            self.assertIsInstance(result[0], str)
            self.assertIsInstance(result[1], int)


if __name__ == "__main__":
    unittest.main()

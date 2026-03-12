#!/usr/bin/env python3
"""Unit tests for handle_return function."""

import unittest
from unittest.mock import patch

from .handle_return_src import handle_return


class TestHandleReturn(unittest.TestCase):
    """Test cases for handle_return function."""

    def setUp(self):
        """Set up test fixtures."""
        self.func_name = "test_func"
        self.label_counter = {"if_else": 0, "if_end": 0, "expr_temp": 0}
        self.var_offsets = {"x": 0, "y": 4}
        self.next_offset = 8

    def test_void_return_no_value(self):
        """Test void return with no value key in stmt."""
        stmt = {"type": "RETURN"}
        
        asm_code, updated_offset = handle_return(
            stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
        )
        
        expected_asm = "MOV SP, FP\nPOP FP\nBX LR"
        self.assertEqual(asm_code, expected_asm)
        self.assertEqual(updated_offset, self.next_offset)

    def test_void_return_with_none_value(self):
        """Test void return with explicit None value."""
        stmt = {"type": "RETURN", "value": None}
        
        asm_code, updated_offset = handle_return(
            stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
        )
        
        expected_asm = "MOV SP, FP\nPOP FP\nBX LR"
        self.assertEqual(asm_code, expected_asm)
        self.assertEqual(updated_offset, self.next_offset)

    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_return_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code')
    def test_non_void_return_with_literal(self, mock_gen_expr):
        """Test non-void return with literal value expression."""
        return_value = {"type": "LITERAL", "value": 42}
        stmt = {"type": "RETURN", "value": return_value}
        
        mock_gen_expr.return_value = ("MOV R0, #42", 8)
        
        asm_code, updated_offset = handle_return(
            stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
        )
        
        expected_asm = "MOV R0, #42\nMOV SP, FP\nPOP FP\nBX LR"
        self.assertEqual(asm_code, expected_asm)
        self.assertEqual(updated_offset, self.next_offset)
        mock_gen_expr.assert_called_once_with(
            return_value, self.func_name, self.label_counter, self.var_offsets, self.next_offset
        )

    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_return_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code')
    def test_non_void_return_with_variable(self, mock_gen_expr):
        """Test non-void return with variable expression."""
        return_value = {"type": "VAR", "name": "x"}
        stmt = {"type": "RETURN", "value": return_value}
        
        mock_gen_expr.return_value = ("LDR R0, [FP, #0]", 8)
        
        asm_code, updated_offset = handle_return(
            stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
        )
        
        expected_asm = "LDR R0, [FP, #0]\nMOV SP, FP\nPOP FP\nBX LR"
        self.assertEqual(asm_code, expected_asm)
        self.assertEqual(updated_offset, self.next_offset)

    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_return_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code')
    def test_non_void_return_with_binary_op(self, mock_gen_expr):
        """Test non-void return with binary operation expression."""
        return_value = {
            "type": "BINOP",
            "op": "+",
            "left": {"type": "VAR", "name": "x"},
            "right": {"type": "LITERAL", "value": 1}
        }
        stmt = {"type": "RETURN", "value": return_value}
        
        mock_gen_expr.return_value = ("LDR R0, [FP, #0]\nADD R0, R0, #1", 8)
        
        asm_code, updated_offset = handle_return(
            stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
        )
        
        expected_asm = "LDR R0, [FP, #0]\nADD R0, R0, #1\nMOV SP, FP\nPOP FP\nBX LR"
        self.assertEqual(asm_code, expected_asm)
        self.assertEqual(updated_offset, self.next_offset)

    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_return_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code')
    def test_non_void_return_with_function_call(self, mock_gen_expr):
        """Test non-void return with function call expression."""
        return_value = {
            "type": "CALL",
            "func_name": "helper",
            "args": [{"type": "VAR", "name": "x"}]
        }
        stmt = {"type": "RETURN", "value": return_value}
        
        mock_gen_expr.return_value = ("BL helper", 8)
        
        asm_code, updated_offset = handle_return(
            stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
        )
        
        expected_asm = "BL helper\nMOV SP, FP\nPOP FP\nBX LR"
        self.assertEqual(asm_code, expected_asm)
        self.assertEqual(updated_offset, self.next_offset)

    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_return_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code')
    def test_non_void_return_with_unary_op(self, mock_gen_expr):
        """Test non-void return with unary operation expression."""
        return_value = {
            "type": "UNOP",
            "op": "-",
            "operand": {"type": "VAR", "name": "x"}
        }
        stmt = {"type": "RETURN", "value": return_value}
        
        mock_gen_expr.return_value = ("LDR R0, [FP, #0]\nRSB R0, R0, #0", 8)
        
        asm_code, updated_offset = handle_return(
            stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
        )
        
        expected_asm = "LDR R0, [FP, #0]\nRSB R0, R0, #0\nMOV SP, FP\nPOP FP\nBX LR"
        self.assertEqual(asm_code, expected_asm)
        self.assertEqual(updated_offset, self.next_offset)

    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_return_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code')
    def test_non_void_return_offset_propagation(self, mock_gen_expr):
        """Test that offset is properly propagated but not changed after epilogue."""
        return_value = {"type": "LITERAL", "value": 100}
        stmt = {"type": "RETURN", "value": return_value}
        
        # Simulate expression code generation that updates offset
        mock_gen_expr.return_value = ("MOV R0, #100", 16)
        
        asm_code, updated_offset = handle_return(
            stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
        )
        
        # Offset should remain as next_offset (not the updated_offset from expression)
        self.assertEqual(updated_offset, self.next_offset)
        self.assertEqual(updated_offset, 8)

    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_return_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code')
    def test_non_void_return_empty_expression_code(self, mock_gen_expr):
        """Test non-void return when expression generates empty code."""
        return_value = {"type": "LITERAL", "value": 0}
        stmt = {"type": "RETURN", "value": return_value}
        
        mock_gen_expr.return_value = ("", 8)
        
        asm_code, updated_offset = handle_return(
            stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
        )
        
        # Empty string will create a blank line before epilogue
        expected_asm = "\nMOV SP, FP\nPOP FP\nBX LR"
        self.assertEqual(asm_code, expected_asm)
        self.assertEqual(updated_offset, self.next_offset)

    def test_return_with_empty_dict_stmt(self):
        """Test return with minimal/empty statement dict."""
        stmt = {}
        
        asm_code, updated_offset = handle_return(
            stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
        )
        
        expected_asm = "MOV SP, FP\nPOP FP\nBX LR"
        self.assertEqual(asm_code, expected_asm)
        self.assertEqual(updated_offset, self.next_offset)

    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_return_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code')
    def test_return_preserves_label_counter(self, mock_gen_expr):
        """Test that label_counter is passed through but not modified by handle_return."""
        return_value = {"type": "LITERAL", "value": 5}
        stmt = {"type": "RETURN", "value": return_value}
        
        original_label_counter = self.label_counter.copy()
        mock_gen_expr.return_value = ("MOV R0, #5", 8)
        
        handle_return(
            stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
        )
        
        # handle_return itself doesn't modify label_counter
        # (generate_expression_code might, but that's tested separately)
        self.assertEqual(self.label_counter, original_label_counter)

    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_return_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code')
    def test_return_preserves_var_offsets(self, mock_gen_expr):
        """Test that var_offsets is passed through but not modified by handle_return."""
        return_value = {"type": "VAR", "name": "y"}
        stmt = {"type": "RETURN", "value": return_value}
        
        original_var_offsets = self.var_offsets.copy()
        mock_gen_expr.return_value = ("LDR R0, [FP, #4]", 8)
        
        handle_return(
            stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
        )
        
        # handle_return itself doesn't modify var_offsets
        self.assertEqual(self.var_offsets, original_var_offsets)


if __name__ == "__main__":
    unittest.main()

# === std / third-party imports ===
from typing import Dict
import unittest
from unittest.mock import patch

# === sub function imports ===
from .generate_unary_op_code_src import generate_unary_op_code


class TestGenerateUnaryOpCode(unittest.TestCase):
    """Test cases for generate_unary_op_code function."""

    def setUp(self):
        """Set up test fixtures."""
        self.var_offsets: Dict[str, int] = {"x": 0, "y": 8}
        self.next_offset = 16

    def test_negation_with_literal_operand(self):
        """Test negation operator with a literal value operand."""
        operand = {"type": "literal", "value": 42}
        
        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_stmt_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("    MOV x0, #42\n", 16)
            
            code, new_offset = generate_unary_op_code(operand, "-", self.var_offsets, self.next_offset)
            
            mock_gen_expr.assert_called_once_with(operand, self.var_offsets, self.next_offset)
            self.assertIn("NEG x0, x0", code)
            self.assertEqual(new_offset, 16)

    def test_negation_with_variable_operand(self):
        """Test negation operator with a variable operand."""
        operand = {"type": "variable", "var_name": "x"}
        
        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_stmt_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("    LDR x0, [sp, #0]\n", 16)
            
            code, new_offset = generate_unary_op_code(operand, "-", self.var_offsets, self.next_offset)
            
            mock_gen_expr.assert_called_once_with(operand, self.var_offsets, self.next_offset)
            self.assertIn("NEG x0, x0", code)
            self.assertEqual(new_offset, 16)

    def test_negation_with_binary_expression_operand(self):
        """Test negation operator with a binary expression operand."""
        operand = {
            "type": "binary_op",
            "operator": "+",
            "left": {"type": "literal", "value": 10},
            "right": {"type": "literal", "value": 20}
        }
        
        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_stmt_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("    MOV x0, #10\n    MOV x1, #20\n    ADD x0, x0, x1\n", 24)
            
            code, new_offset = generate_unary_op_code(operand, "-", self.var_offsets, self.next_offset)
            
            mock_gen_expr.assert_called_once_with(operand, self.var_offsets, self.next_offset)
            self.assertIn("NEG x0, x0", code)
            self.assertEqual(new_offset, 24)

    def test_negation_with_nested_unary_operand(self):
        """Test negation operator with a nested unary expression operand."""
        operand = {
            "type": "unary_op",
            "operator": "-",
            "operand": {"type": "literal", "value": 5}
        }
        
        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_stmt_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("    MOV x0, #5\n    NEG x0, x0\n", 16)
            
            code, new_offset = generate_unary_op_code(operand, "-", self.var_offsets, self.next_offset)
            
            mock_gen_expr.assert_called_once_with(operand, self.var_offsets, self.next_offset)
            self.assertIn("NEG x0, x0", code)
            self.assertEqual(new_offset, 16)

    def test_unsupported_operator_raises_error(self):
        """Test that unsupported unary operators raise ValueError."""
        operand = {"type": "literal", "value": 10}
        
        with self.assertRaises(ValueError) as context:
            generate_unary_op_code(operand, "+", self.var_offsets, self.next_offset)
        
        self.assertIn("Unsupported unary operator: +", str(context.exception))

    def test_not_operator_raises_error(self):
        """Test that 'not' operator raises ValueError (not yet supported)."""
        operand = {"type": "literal", "value": 1}
        
        with self.assertRaises(ValueError) as context:
            generate_unary_op_code(operand, "not", self.var_offsets, self.next_offset)
        
        self.assertIn("Unsupported unary operator: not", str(context.exception))

    def test_bitwise_not_operator_raises_error(self):
        """Test that bitwise not operator raises ValueError (not yet supported)."""
        operand = {"type": "literal", "value": 5}
        
        with self.assertRaises(ValueError) as context:
            generate_unary_op_code(operand, "~", self.var_offsets, self.next_offset)
        
        self.assertIn("Unsupported unary operator: ~", str(context.exception))

    def test_none_operand_raises_error(self):
        """Test that None operand raises ValueError."""
        with self.assertRaises(ValueError) as context:
            generate_unary_op_code(None, "-", self.var_offsets, self.next_offset)
        
        self.assertIn("Unary operand cannot be None", str(context.exception))

    def test_empty_dict_operand(self):
        """Test behavior with empty dict operand (delegated to generate_expression_code)."""
        operand = {}
        
        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_stmt_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("    MOV x0, #0\n", 16)
            
            code, new_offset = generate_unary_op_code(operand, "-", self.var_offsets, self.next_offset)
            
            mock_gen_expr.assert_called_once_with(operand, self.var_offsets, self.next_offset)
            self.assertIn("NEG x0, x0", code)

    def test_zero_literal_operand(self):
        """Test negation with zero literal operand."""
        operand = {"type": "literal", "value": 0}
        
        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_stmt_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("    MOV x0, #0\n", 16)
            
            code, new_offset = generate_unary_op_code(operand, "-", self.var_offsets, self.next_offset)
            
            mock_gen_expr.assert_called_once_with(operand, self.var_offsets, self.next_offset)
            self.assertIn("NEG x0, x0", code)
            self.assertEqual(new_offset, 16)

    def test_negative_literal_operand(self):
        """Test negation with negative literal operand."""
        operand = {"type": "literal", "value": -10}
        
        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_stmt_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("    MOV x0, #-10\n", 16)
            
            code, new_offset = generate_unary_op_code(operand, "-", self.var_offsets, self.next_offset)
            
            mock_gen_expr.assert_called_once_with(operand, self.var_offsets, self.next_offset)
            self.assertIn("NEG x0, x0", code)
            self.assertEqual(new_offset, 16)

    def test_offset_propagation(self):
        """Test that next_offset is properly propagated and returned."""
        operand = {"type": "literal", "value": 100}
        
        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_stmt_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("    MOV x0, #100\n", 32)
            
            code, new_offset = generate_unary_op_code(operand, "-", self.var_offsets, 16)
            
            self.assertEqual(new_offset, 32)

    def test_code_formatting(self):
        """Test that generated code has proper ARM64 formatting."""
        operand = {"type": "literal", "value": 5}
        
        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_stmt_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("    MOV x0, #5\n", 16)
            
            code, new_offset = generate_unary_op_code(operand, "-", self.var_offsets, self.next_offset)
            
            # Check that NEG instruction is properly formatted with indentation
            self.assertIn("    NEG x0, x0\n", code)

    def test_var_offsets_readonly_behavior(self):
        """Test that var_offsets is not modified (read-only usage)."""
        operand = {"type": "variable", "var_name": "x"}
        original_var_offsets = self.var_offsets.copy()
        
        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_stmt_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("    LDR x0, [sp, #0]\n", 16)
            
            generate_unary_op_code(operand, "-", self.var_offsets, self.next_offset)
            
            # Verify var_offsets was not modified
            self.assertEqual(self.var_offsets, original_var_offsets)

    def test_multiple_calls_independence(self):
        """Test that multiple calls are independent."""
        operand1 = {"type": "literal", "value": 10}
        operand2 = {"type": "literal", "value": 20}
        
        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_stmt_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.side_effect = [
                ("    MOV x0, #10\n", 16),
                ("    MOV x0, #20\n", 16)
            ]
            
            code1, offset1 = generate_unary_op_code(operand1, "-", self.var_offsets, self.next_offset)
            code2, offset2 = generate_unary_op_code(operand2, "-", self.var_offsets, self.next_offset)
            
            self.assertIn("NEG x0, x0", code1)
            self.assertIn("NEG x0, x0", code2)
            self.assertEqual(mock_gen_expr.call_count, 2)


if __name__ == "__main__":
    unittest.main()

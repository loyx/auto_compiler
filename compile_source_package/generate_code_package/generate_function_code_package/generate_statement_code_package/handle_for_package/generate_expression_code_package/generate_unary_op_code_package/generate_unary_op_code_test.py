import unittest
from unittest.mock import patch

# Import the function under test using relative import
from .generate_unary_op_code_src import generate_unary_op_code


class TestGenerateUnaryOpCode(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures."""
        self.var_offsets = {"x": 0, "y": 1}
        self.label_counter = {"counter": 0}
        self.func_name = "test_func"
        self.next_offset = 5
    
    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_unary_op_code_package.generate_unary_op_code_src.generate_expression_code')
    def test_negation_operator(self, mock_gen_expr):
        """Test unary negation operator (-)."""
        # Setup mock to return operand code and offset
        mock_gen_expr.return_value = ("    ldr x0, [sp, #0]\n", 6)
        
        expr = {
            "type": "UNARY_OP",
            "operator": "-",
            "operand": {"type": "LITERAL", "value": 5}
        }
        
        code, offset = generate_unary_op_code(
            expr,
            self.func_name,
            self.label_counter,
            self.var_offsets,
            self.next_offset
        )
        
        # Verify generate_expression_code was called with correct args
        mock_gen_expr.assert_called_once_with(
            {"type": "LITERAL", "value": 5},
            self.func_name,
            self.label_counter,
            self.var_offsets,
            self.next_offset
        )
        
        # Verify the generated code
        expected_code = "    ldr x0, [sp, #0]\n    neg x0, x0\n"
        self.assertEqual(code, expected_code)
        self.assertEqual(offset, 6)
    
    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_unary_op_code_package.generate_unary_op_code_src.generate_expression_code')
    def test_logical_not_operator(self, mock_gen_expr):
        """Test unary logical not operator (!)."""
        # Setup mock
        mock_gen_expr.return_value = ("    ldr x0, [sp, #0]\n", 6)
        
        expr = {
            "type": "UNARY_OP",
            "operator": "!",
            "operand": {"type": "LITERAL", "value": 0}
        }
        
        code, offset = generate_unary_op_code(
            expr,
            self.func_name,
            self.label_counter,
            self.var_offsets,
            self.next_offset
        )
        
        # Verify generate_expression_code was called
        mock_gen_expr.assert_called_once_with(
            {"type": "LITERAL", "value": 0},
            self.func_name,
            self.label_counter,
            self.var_offsets,
            self.next_offset
        )
        
        # Verify the generated code
        expected_code = "    ldr x0, [sp, #0]\n    cmp x0, #0\n    cset x0, eq\n"
        self.assertEqual(code, expected_code)
        self.assertEqual(offset, 6)
    
    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_unary_op_code_package.generate_unary_op_code_src.generate_expression_code')
    def test_bitwise_not_operator(self, mock_gen_expr):
        """Test unary bitwise not operator (~)."""
        # Setup mock
        mock_gen_expr.return_value = ("    ldr x0, [sp, #0]\n", 6)
        
        expr = {
            "type": "UNARY_OP",
            "operator": "~",
            "operand": {"type": "LITERAL", "value": 5}
        }
        
        code, offset = generate_unary_op_code(
            expr,
            self.func_name,
            self.label_counter,
            self.var_offsets,
            self.next_offset
        )
        
        # Verify generate_expression_code was called
        mock_gen_expr.assert_called_once_with(
            {"type": "LITERAL", "value": 5},
            self.func_name,
            self.label_counter,
            self.var_offsets,
            self.next_offset
        )
        
        # Verify the generated code
        expected_code = "    ldr x0, [sp, #0]\n    mvn x0, x0\n"
        self.assertEqual(code, expected_code)
        self.assertEqual(offset, 6)
    
    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_expression_code_package.generate_unary_op_code_package.generate_unary_op_code_src.generate_expression_code')
    def test_unknown_operator_raises_error(self, mock_gen_expr):
        """Test that unknown operator raises ValueError."""
        expr = {
            "type": "UNARY_OP",
            "operator": "@",
            "operand": {"type": "LITERAL", "value": 5}
        }
        
        with self.assertRaises(ValueError) as context:
            generate_unary_op_code(
                expr,
                self.func_name,
                self.label_counter,
                self.var_offsets,
                self.next_offset
            )
        
        self.assertIn("Unknown unary operator: @", str(context.exception))
        # Verify generate_expression_code was still called for the operand
        mock_gen_expr.assert_called_once()
    
    @patch('generate_unary_op_code_package.generate_unary_op_code_src.generate_expression_code')
    def test_offset_propagation(self, mock_gen_expr):
        """Test that offset from operand is correctly propagated."""
        # Test with different offset values
        test_offsets = [0, 10, 100]
        
        for test_offset in test_offsets:
            mock_gen_expr.return_value = ("    ldr x0, [sp, #0]\n", test_offset + 1)
            
            expr = {
                "type": "UNARY_OP",
                "operator": "-",
                "operand": {"type": "LITERAL", "value": 5}
            }
            
            _, offset = generate_unary_op_code(
                expr,
                self.func_name,
                self.label_counter,
                self.var_offsets,
                test_offset
            )
            
            self.assertEqual(offset, test_offset + 1)
    
    @patch('generate_unary_op_code_package.generate_unary_op_code_src.generate_expression_code')
    def test_empty_var_offsets(self, mock_gen_expr):
        """Test with empty var_offsets dict."""
        mock_gen_expr.return_value = ("    mov x0, #5\n", 5)
        
        expr = {
            "type": "UNARY_OP",
            "operator": "-",
            "operand": {"type": "LITERAL", "value": 5}
        }
        
        code, offset = generate_unary_op_code(
            expr,
            self.func_name,
            self.label_counter,
            {},
            self.next_offset
        )
        
        expected_code = "    mov x0, #5\n    neg x0, x0\n"
        self.assertEqual(code, expected_code)
        self.assertEqual(offset, 5)
    
    @patch('generate_unary_op_code_package.generate_unary_op_code_src.generate_expression_code')
    def test_complex_operand_expression(self, mock_gen_expr):
        """Test with complex operand expression (mocked)."""
        # Mock returns code for a complex expression
        mock_gen_expr.return_value = (
            "    ldr x0, [sp, #0]\n    ldr x1, [sp, #1]\n    add x0, x0, x1\n",
            7
        )
        
        expr = {
            "type": "UNARY_OP",
            "operator": "!",
            "operand": {
                "type": "BINARY_OP",
                "operator": "+",
                "left": {"type": "IDENTIFIER", "name": "a"},
                "right": {"type": "IDENTIFIER", "name": "b"}
            }
        }
        
        code, offset = generate_unary_op_code(
            expr,
            self.func_name,
            self.label_counter,
            self.var_offsets,
            self.next_offset
        )
        
        # Verify the logical not is applied after the complex operand
        self.assertIn("add x0, x0, x1", code)
        self.assertIn("cmp x0, #0", code)
        self.assertIn("cset x0, eq", code)
        self.assertEqual(offset, 7)


if __name__ == '__main__':
    unittest.main()
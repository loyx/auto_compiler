import unittest
from unittest.mock import patch
from typing import Dict

# Import using relative import from the same package
from .generate_expression_code_src import generate_expression_code


class TestGenerateExpressionCode(unittest.TestCase):
    """Test cases for generate_expression_code function."""
    
    def test_literal_int(self):
        """Test literal integer expression."""
        expr = {"type": "literal", "value_type": "int", "value": 42}
        var_offsets: Dict[str, int] = {}
        next_offset = 0
        
        code, updated_offset = generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertEqual(code, "mov x0, #42\n")
        self.assertEqual(updated_offset, 0)
    
    def test_literal_bool_true(self):
        """Test literal boolean true expression."""
        expr = {"type": "literal", "value_type": "bool", "value": 1}
        var_offsets: Dict[str, int] = {}
        next_offset = 0
        
        code, updated_offset = generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertEqual(code, "mov x0, #1\n")
        self.assertEqual(updated_offset, 0)
    
    def test_literal_bool_false(self):
        """Test literal boolean false expression."""
        expr = {"type": "literal", "value_type": "bool", "value": 0}
        var_offsets: Dict[str, int] = {}
        next_offset = 0
        
        code, updated_offset = generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertEqual(code, "mov x0, #0\n")
        self.assertEqual(updated_offset, 0)
    
    def test_literal_negative(self):
        """Test literal negative integer expression."""
        expr = {"type": "literal", "value_type": "int", "value": -10}
        var_offsets: Dict[str, int] = {}
        next_offset = 0
        
        code, updated_offset = generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertEqual(code, "mov x0, #-10\n")
        self.assertEqual(updated_offset, 0)
    
    def test_variable_existing(self):
        """Test variable expression with existing variable."""
        expr = {"type": "variable", "name": "x"}
        var_offsets: Dict[str, int] = {"x": 16}
        next_offset = 0
        
        code, updated_offset = generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertEqual(code, "ldr x0, [sp, #16]\n")
        self.assertEqual(updated_offset, 0)
    
    def test_variable_zero_offset(self):
        """Test variable expression with zero offset."""
        expr = {"type": "variable", "name": "y"}
        var_offsets: Dict[str, int] = {"y": 0}
        next_offset = 0
        
        code, updated_offset = generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertEqual(code, "ldr x0, [sp, #0]\n")
        self.assertEqual(updated_offset, 0)
    
    def test_variable_missing(self):
        """Test variable expression with missing variable raises KeyError."""
        expr = {"type": "variable", "name": "y"}
        var_offsets: Dict[str, int] = {"x": 16}
        next_offset = 0
        
        with self.assertRaises(KeyError) as context:
            generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertIn("y", str(context.exception))
    
    @patch('generate_expression_code_package.generate_expression_code_src._get_binary_op_instruction')
    def test_binary_op_add(self, mock_get_binary_op):
        """Test binary operation with add operator."""
        mock_get_binary_op.return_value = "add x0, x1, x0\n"
        
        expr = {
            "type": "binary_op",
            "op": "add",
            "left": {"type": "literal", "value_type": "int", "value": 5},
            "right": {"type": "literal", "value_type": "int", "value": 3}
        }
        var_offsets: Dict[str, int] = {}
        next_offset = 0
        
        code, updated_offset = generate_expression_code(expr, var_offsets, next_offset)
        
        expected_parts = [
            "mov x0, #5\n",
            "str x0, [sp, #0]\n",
            "mov x0, #3\n",
            "ldr x1, [sp, #0]\n",
            "add x0, x1, x0\n"
        ]
        self.assertEqual(code, "".join(expected_parts))
        self.assertEqual(updated_offset, 8)
        mock_get_binary_op.assert_called_once_with("add")
    
    @patch('generate_expression_code_package.generate_expression_code_src._get_binary_op_instruction')
    def test_binary_op_sub(self, mock_get_binary_op):
        """Test binary operation with sub operator."""
        mock_get_binary_op.return_value = "sub x0, x1, x0\n"
        
        expr = {
            "type": "binary_op",
            "op": "sub",
            "left": {"type": "literal", "value_type": "int", "value": 10},
            "right": {"type": "literal", "value_type": "int", "value": 4}
        }
        var_offsets: Dict[str, int] = {}
        next_offset = 0
        
        code, updated_offset = generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertIn("mov x0, #10\n", code)
        self.assertIn("mov x0, #4\n", code)
        self.assertIn("sub x0, x1, x0\n", code)
        self.assertEqual(updated_offset, 8)
    
    @patch('generate_expression_code_package.generate_expression_code_src._get_binary_op_instruction')
    def test_binary_op_with_variables(self, mock_get_binary_op):
        """Test binary operation with variable operands."""
        mock_get_binary_op.return_value = "add x0, x1, x0\n"
        
        expr = {
            "type": "binary_op",
            "op": "add",
            "left": {"type": "variable", "name": "a"},
            "right": {"type": "variable", "name": "b"}
        }
        var_offsets: Dict[str, int] = {"a": 16, "b": 24}
        next_offset = 0
        
        code, updated_offset = generate_expression_code(expr, var_offsets, next_offset)
        
        expected_parts = [
            "ldr x0, [sp, #16]\n",
            "str x0, [sp, #0]\n",
            "ldr x0, [sp, #24]\n",
            "ldr x1, [sp, #0]\n",
            "add x0, x1, x0\n"
        ]
        self.assertEqual(code, "".join(expected_parts))
        self.assertEqual(updated_offset, 8)
    
    @patch('generate_expression_code_package.generate_expression_code_src._get_binary_op_instruction')
    def test_binary_op_non_zero_offset(self, mock_get_binary_op):
        """Test binary operation with non-zero starting offset."""
        mock_get_binary_op.return_value = "mul x0, x1, x0\n"
        
        expr = {
            "type": "binary_op",
            "op": "mul",
            "left": {"type": "literal", "value_type": "int", "value": 2},
            "right": {"type": "literal", "value_type": "int", "value": 3}
        }
        var_offsets: Dict[str, int] = {}
        next_offset = 32
        
        code, updated_offset = generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertIn("str x0, [sp, #32]\n", code)
        self.assertIn("ldr x1, [sp, #32]\n", code)
        self.assertEqual(updated_offset, 40)
    
    @patch('generate_expression_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_if_stmt_package.generate_expression_code_package.generate_expression_code_src._get_unary_op_instruction')
    def test_unary_op_neg(self, mock_get_unary_op):
        """Test unary operation with neg operator."""
        mock_get_unary_op.return_value = "neg x0, x0\n"
        
        expr = {
            "type": "unary_op",
            "op": "neg",
            "operand": {"type": "literal", "value_type": "int", "value": 5}
        }
        var_offsets: Dict[str, int] = {}
        next_offset = 0
        
        code, updated_offset = generate_expression_code(expr, var_offsets, next_offset)
        
        expected_parts = [
            "mov x0, #5\n",
            "neg x0, x0\n"
        ]
        self.assertEqual(code, "".join(expected_parts))
        self.assertEqual(updated_offset, 0)
        mock_get_unary_op.assert_called_once_with("neg")
    
    @patch('generate_expression_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_if_stmt_package.generate_expression_code_package.generate_expression_code_src._get_unary_op_instruction')
    def test_unary_op_not(self, mock_get_unary_op):
        """Test unary operation with not operator."""
        mock_get_unary_op.return_value = "mvn x0, x0\n"
        
        expr = {
            "type": "unary_op",
            "op": "not",
            "operand": {"type": "literal", "value_type": "int", "value": 0}
        }
        var_offsets: Dict[str, int] = {}
        next_offset = 0
        
        code, updated_offset = generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertIn("mov x0, #0\n", code)
        self.assertIn("mvn x0, x0\n", code)
        self.assertEqual(updated_offset, 0)
    
    @patch('generate_expression_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_if_stmt_package.generate_expression_code_package.generate_expression_code_src._get_unary_op_instruction')
    def test_unary_op_lnot(self, mock_get_unary_op):
        """Test unary operation with lnot (logical not) operator."""
        mock_get_unary_op.return_value = "lnot x0, x0\n"
        
        expr = {
            "type": "unary_op",
            "op": "lnot",
            "operand": {"type": "variable", "name": "flag"}
        }
        var_offsets: Dict[str, int] = {"flag": 8}
        next_offset = 0
        
        code, updated_offset = generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertIn("ldr x0, [sp, #8]\n", code)
        self.assertIn("lnot x0, x0\n", code)
        self.assertEqual(updated_offset, 0)
    
    @patch('generate_expression_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_if_stmt_package.generate_expression_code_package.generate_expression_code_src._get_binary_op_instruction')
    def test_nested_binary_op(self, mock_get_binary_op):
        """Test nested binary operations."""
        mock_get_binary_op.side_effect = lambda op: f"{op} x0, x1, x0\n"
        
        expr = {
            "type": "binary_op",
            "op": "add",
            "left": {
                "type": "binary_op",
                "op": "mul",
                "left": {"type": "literal", "value_type": "int", "value": 2},
                "right": {"type": "literal", "value_type": "int", "value": 3}
            },
            "right": {"type": "literal", "value_type": "int", "value": 4}
        }
        var_offsets: Dict[str, int] = {}
        next_offset = 0
        
        code, updated_offset = generate_expression_code(expr, var_offsets, next_offset)
        
        # Should handle nested structure correctly
        self.assertIn("mov x0, #2\n", code)
        self.assertIn("mov x0, #3\n", code)
        self.assertIn("mul x0, x1, x0\n", code)
        self.assertIn("mov x0, #4\n", code)
        self.assertIn("add x0, x1, x0\n", code)
        self.assertEqual(updated_offset, 16)  # Two stack slots used
    
    @patch('generate_expression_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_if_stmt_package.generate_expression_code_package.generate_expression_code_src._get_binary_op_instruction')
    @patch('generate_expression_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_if_stmt_package.generate_expression_code_package.generate_expression_code_src._get_unary_op_instruction')
    def test_mixed_nested_ops(self, mock_get_unary_op, mock_get_binary_op):
        """Test mixed nested binary and unary operations."""
        mock_get_binary_op.return_value = "add x0, x1, x0\n"
        mock_get_unary_op.return_value = "neg x0, x0\n"
        
        expr = {
            "type": "binary_op",
            "op": "add",
            "left": {
                "type": "unary_op",
                "op": "neg",
                "operand": {"type": "literal", "value_type": "int", "value": 5}
            },
            "right": {"type": "literal", "value_type": "int", "value": 10}
        }
        var_offsets: Dict[str, int] = {}
        next_offset = 0
        
        code, updated_offset = generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertIn("mov x0, #5\n", code)
        self.assertIn("neg x0, x0\n", code)
        self.assertIn("mov x0, #10\n", code)
        self.assertIn("add x0, x1, x0\n", code)
        self.assertEqual(updated_offset, 8)
    
    def test_unknown_expression_type(self):
        """Test unknown expression type raises ValueError."""
        expr = {"type": "unknown"}  # type: ignore
        var_offsets: Dict[str, int] = {}
        next_offset = 0
        
        with self.assertRaises(ValueError) as context:
            generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertIn("unknown", str(context.exception).lower())
    
    @patch('generate_expression_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_if_stmt_package.generate_expression_code_package.generate_expression_code_src._get_binary_op_instruction')
    def test_comparison_op(self, mock_get_binary_op):
        """Test comparison operator (eq)."""
        mock_get_binary_op.return_value = "cmp x1, x0\n"
        
        expr = {
            "type": "binary_op",
            "op": "eq",
            "left": {"type": "literal", "value_type": "int", "value": 5},
            "right": {"type": "literal", "value_type": "int", "value": 5}
        }
        var_offsets: Dict[str, int] = {}
        next_offset = 0
        
        code, updated_offset = generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertIn("cmp x1, x0\n", code)
        self.assertEqual(updated_offset, 8)
    
    @patch('generate_expression_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_if_stmt_package.generate_expression_code_package.generate_expression_code_src._get_binary_op_instruction')
    def test_binary_op_offset_tracking(self, mock_get_binary_op):
        """Test that offset is properly tracked through multiple binary ops."""
        mock_get_binary_op.return_value = "add x0, x1, x0\n"
        
        # First binary op
        expr1 = {
            "type": "binary_op",
            "op": "add",
            "left": {"type": "literal", "value_type": "int", "value": 1},
            "right": {"type": "literal", "value_type": "int", "value": 2}
        }
        var_offsets: Dict[str, int] = {}
        
        code1, offset1 = generate_expression_code(expr1, var_offsets, 0)
        self.assertEqual(offset1, 8)
        
        # Second binary op starting from offset1
        expr2 = {
            "type": "binary_op",
            "op": "add",
            "left": {"type": "literal", "value_type": "int", "value": 3},
            "right": {"type": "literal", "value_type": "int", "value": 4}
        }
        
        code2, offset2 = generate_expression_code(expr2, var_offsets, offset1)
        self.assertEqual(offset2, 16)
        self.assertIn("str x0, [sp, #8]\n", code2)


if __name__ == '__main__':
    unittest.main()

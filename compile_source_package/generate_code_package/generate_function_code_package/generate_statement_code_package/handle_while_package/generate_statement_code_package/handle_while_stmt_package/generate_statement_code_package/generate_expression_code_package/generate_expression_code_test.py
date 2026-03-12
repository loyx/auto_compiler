# === std / third-party imports ===
import unittest
from unittest.mock import patch

# === relative imports ===
from .generate_expression_code_src import generate_expression_code


class TestGenerateExpressionCode(unittest.TestCase):
    """Unit tests for generate_expression_code function."""

    def test_literal_expression(self):
        """Test dispatch to _handle_literal for literal expressions."""
        expr = {"type": "literal", "value": 42}
        var_offsets = {"x": 0}
        next_offset = 5
        
        expected_code = "LOAD_CONST 42\n"
        expected_result_offset = 5
        expected_next_offset = 6
        
        with patch("._handle_literal_package._handle_literal_src._handle_literal") as mock_literal:
            mock_literal.return_value = (expected_code, expected_result_offset, expected_next_offset)
            
            code, result_offset, updated_offset = generate_expression_code(expr, var_offsets, next_offset)
            
            mock_literal.assert_called_once_with(42, next_offset)
            self.assertEqual(code, expected_code)
            self.assertEqual(result_offset, expected_result_offset)
            self.assertEqual(updated_offset, expected_next_offset)

    def test_variable_expression(self):
        """Test dispatch to _handle_variable for variable expressions."""
        expr = {"type": "variable", "name": "x"}
        var_offsets = {"x": 0, "y": 1}
        next_offset = 3
        
        expected_code = "LOAD 0\n"
        expected_result_offset = 0
        expected_next_offset = 3
        
        with patch("._handle_variable_package._handle_variable_src._handle_variable") as mock_variable:
            mock_variable.return_value = (expected_code, expected_result_offset, expected_next_offset)
            
            code, result_offset, updated_offset = generate_expression_code(expr, var_offsets, next_offset)
            
            mock_variable.assert_called_once_with("x", var_offsets, next_offset)
            self.assertEqual(code, expected_code)
            self.assertEqual(result_offset, expected_result_offset)
            self.assertEqual(updated_offset, expected_next_offset)

    def test_binary_op_expression(self):
        """Test dispatch to _handle_binary_op for binary operation expressions."""
        expr = {
            "type": "binary_op",
            "operator": "+",
            "left": {"type": "literal", "value": 1},
            "right": {"type": "literal", "value": 2}
        }
        var_offsets = {"x": 0}
        next_offset = 5
        
        expected_code = "LOAD_CONST 1\nLOAD_CONST 2\nBINARY_OP +\n"
        expected_result_offset = 7
        expected_next_offset = 8
        
        with patch("._handle_binary_op_package._handle_binary_op_src._handle_binary_op") as mock_binary:
            mock_binary.return_value = (expected_code, expected_result_offset, expected_next_offset)
            
            code, result_offset, updated_offset = generate_expression_code(expr, var_offsets, next_offset)
            
            mock_binary.assert_called_once_with("+", expr["left"], expr["right"], var_offsets, next_offset)
            self.assertEqual(code, expected_code)
            self.assertEqual(result_offset, expected_result_offset)
            self.assertEqual(updated_offset, expected_next_offset)

    def test_unary_op_expression(self):
        """Test dispatch to _handle_unary_op for unary operation expressions."""
        expr = {
            "type": "unary_op",
            "operator": "-",
            "operand": {"type": "literal", "value": 5}
        }
        var_offsets = {"x": 0}
        next_offset = 4
        
        expected_code = "LOAD_CONST 5\nUNARY_OP -\n"
        expected_result_offset = 5
        expected_next_offset = 6
        
        with patch("._handle_unary_op_package._handle_unary_op_src._handle_unary_op") as mock_unary:
            mock_unary.return_value = (expected_code, expected_result_offset, expected_next_offset)
            
            code, result_offset, updated_offset = generate_expression_code(expr, var_offsets, next_offset)
            
            mock_unary.assert_called_once_with("-", expr["operand"], var_offsets, next_offset)
            self.assertEqual(code, expected_code)
            self.assertEqual(result_offset, expected_result_offset)
            self.assertEqual(updated_offset, expected_next_offset)

    def test_call_expression(self):
        """Test dispatch to _handle_call for function call expressions."""
        expr = {
            "type": "call",
            "function": "print",
            "args": [
                {"type": "literal", "value": "hello"},
                {"type": "variable", "name": "x"}
            ]
        }
        var_offsets = {"x": 0}
        next_offset = 3
        
        expected_code = "LOAD_CONST hello\nLOAD 0\nCALL print 2\n"
        expected_result_offset = 5
        expected_next_offset = 6
        
        with patch("._handle_call_package._handle_call_src._handle_call") as mock_call:
            mock_call.return_value = (expected_code, expected_result_offset, expected_next_offset)
            
            code, result_offset, updated_offset = generate_expression_code(expr, var_offsets, next_offset)
            
            mock_call.assert_called_once_with("print", expr["args"], var_offsets, next_offset)
            self.assertEqual(code, expected_code)
            self.assertEqual(result_offset, expected_result_offset)
            self.assertEqual(updated_offset, expected_next_offset)

    def test_unknown_expression_type(self):
        """Test that unknown expression type raises ValueError."""
        expr = {"type": "unknown_type", "data": "some_data"}
        var_offsets = {"x": 0}
        next_offset = 5
        
        with self.assertRaises(ValueError) as context:
            generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertIn("Unknown expression type: unknown_type", str(context.exception))

    def test_missing_type_key(self):
        """Test that missing 'type' key raises ValueError."""
        expr = {"value": 42}  # No "type" key
        var_offsets = {"x": 0}
        next_offset = 5
        
        with self.assertRaises(ValueError) as context:
            generate_expression_code(expr, var_offsets, next_offset)
        
        self.assertIn("Unknown expression type: None", str(context.exception))

    def test_literal_with_different_value_types(self):
        """Test literal expression with various value types."""
        test_cases = [
            ("int", 42),
            ("float", 3.14),
            ("str", "hello"),
            ("bool", True),
            ("bool", False),
            ("None", None),
        ]
        
        for value_name, value in test_cases:
            with self.subTest(value_type=value_name):
                expr = {"type": "literal", "value": value}
                var_offsets = {}
                next_offset = 0
                
                expected_code = f"LOAD_CONST {value}\n"
                expected_result_offset = 0
                expected_next_offset = 1
                
                with patch("._handle_literal_package._handle_literal_src._handle_literal") as mock_literal:
                    mock_literal.return_value = (expected_code, expected_result_offset, expected_next_offset)
                    
                    code, result_offset, updated_offset = generate_expression_code(expr, var_offsets, next_offset)
                    
                    mock_literal.assert_called_once_with(value, next_offset)
                    self.assertEqual(code, expected_code)


if __name__ == "__main__":
    unittest.main()

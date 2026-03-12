import unittest
from unittest.mock import patch

from .handle_assign_src import handle_assign


class TestHandleAssign(unittest.TestCase):
    """Test cases for handle_assign function."""
    
    def setUp(self):
        """Set up common test fixtures."""
        self.func_name = "test_func"
        self.label_counter = {"for_cond": 0, "for_end": 0, "for_update": 0}
        self.var_offsets = {"x": 4, "y": 8, "z": 12}
        self.next_offset = 16
    
    def test_happy_path_with_target_field(self):
        """Test assignment using 'target' field."""
        stmt = {
            "type": "ASSIGN",
            "target": "x",
            "value": {"type": "CONST", "value": 42}
        }
        
        with patch("handle_assign_package.handle_assign_src.evaluate_expression") as mock_eval:
            mock_eval.return_value = ("    MOV R0, #42\n", 16, "R0")
            
            code, offset = handle_assign(stmt, self.func_name, self.label_counter,
                                         self.var_offsets, self.next_offset)
            
            self.assertIn("    MOV R0, #42\n", code)
            self.assertIn("    STR R0, [SP, #-4]\n", code)
            self.assertEqual(offset, 16)
            mock_eval.assert_called_once_with(
                {"type": "CONST", "value": 42},
                self.func_name,
                self.label_counter,
                self.var_offsets,
                self.next_offset
            )
    
    def test_happy_path_with_var_name_field(self):
        """Test assignment using 'var_name' field (alternative)."""
        stmt = {
            "type": "ASSIGN",
            "var_name": "y",
            "value": {"type": "CONST", "value": 100}
        }
        
        with patch("handle_assign_package.handle_assign_src.evaluate_expression") as mock_eval:
            mock_eval.return_value = ("    MOV R0, #100\n", 16, "R0")
            
            code, offset = handle_assign(stmt, self.func_name, self.label_counter,
                                         self.var_offsets, self.next_offset)
            
            self.assertIn("    STR R0, [SP, #-8]\n", code)
            self.assertEqual(offset, 16)
    
    def test_target_takes_precedence_over_var_name(self):
        """Test that 'target' field takes precedence when both are present."""
        stmt = {
            "type": "ASSIGN",
            "target": "x",
            "var_name": "y",
            "value": {"type": "CONST", "value": 5}
        }
        
        with patch("handle_assign_package.handle_assign_src.evaluate_expression") as mock_eval:
            mock_eval.return_value = ("    MOV R0, #5\n", 16, "R0")
            
            code, offset = handle_assign(stmt, self.func_name, self.label_counter,
                                         self.var_offsets, self.next_offset)
            
            self.assertIn("    STR R0, [SP, #-4]\n", code)
    
    def test_undefined_variable_raises_valueerror(self):
        """Test that undefined variable raises ValueError."""
        stmt = {
            "type": "ASSIGN",
            "target": "undefined_var",
            "value": {"type": "CONST", "value": 10}
        }
        
        with self.assertRaises(ValueError) as context:
            handle_assign(stmt, self.func_name, self.label_counter,
                         self.var_offsets, self.next_offset)
        
        self.assertIn("Undefined variable: undefined_var", str(context.exception))
    
    def test_complex_expression_delegation(self):
        """Test delegation to evaluate_expression for complex expressions."""
        stmt = {
            "type": "ASSIGN",
            "target": "z",
            "value": {
                "type": "BINOP",
                "op": "+",
                "left": {"type": "VAR", "name": "x"},
                "right": {"type": "VAR", "name": "y"}
            }
        }
        
        with patch("handle_assign_package.handle_assign_src.evaluate_expression") as mock_eval:
            mock_eval.return_value = (
                "    LDR R0, [SP, #-4]\n    LDR R1, [SP, #-8]\n    ADD R0, R0, R1\n",
                16,
                "R0"
            )
            
            code, offset = handle_assign(stmt, self.func_name, self.label_counter,
                                         self.var_offsets, self.next_offset)
            
            self.assertIn("    LDR R0, [SP, #-4]\n", code)
            self.assertIn("    LDR R1, [SP, #-8]\n", code)
            self.assertIn("    ADD R0, R0, R1\n", code)
            self.assertIn("    STR R0, [SP, #-12]\n", code)
            self.assertEqual(offset, 16)
    
    def test_different_result_register(self):
        """Test handling when evaluate_expression returns different register."""
        stmt = {
            "type": "ASSIGN",
            "target": "x",
            "value": {"type": "CONST", "value": 999}
        }
        
        with patch("handle_assign_package.handle_assign_src.evaluate_expression") as mock_eval:
            mock_eval.return_value = ("    MOV R2, #999\n", 16, "R2")
            
            code, offset = handle_assign(stmt, self.func_name, self.label_counter,
                                         self.var_offsets, self.next_offset)
            
            self.assertIn("    STR R2, [SP, #-4]\n", code)
    
    def test_offset_propagation(self):
        """Test that updated_offset from evaluate_expression is propagated."""
        stmt = {
            "type": "ASSIGN",
            "target": "x",
            "value": {"type": "CONST", "value": 1}
        }
        
        with patch("handle_assign_package.handle_assign_src.evaluate_expression") as mock_eval:
            mock_eval.return_value = ("    MOV R0, #1\n", 32, "R0")
            
            code, offset = handle_assign(stmt, self.func_name, self.label_counter,
                                         self.var_offsets, self.next_offset)
            
            self.assertEqual(offset, 32)
    
    def test_empty_expression_code(self):
        """Test handling when expression generates no code."""
        stmt = {
            "type": "ASSIGN",
            "target": "x",
            "value": {"type": "VAR", "name": "y"}
        }
        
        with patch("handle_assign_package.handle_assign_src.evaluate_expression") as mock_eval:
            mock_eval.return_value = ("", 16, "R0")
            
            code, offset = handle_assign(stmt, self.func_name, self.label_counter,
                                         self.var_offsets, self.next_offset)
            
            self.assertEqual(code, "    STR R0, [SP, #-4]\n")
            self.assertEqual(offset, 16)
    
    def test_zero_offset_variable(self):
        """Test assignment to variable at offset 0."""
        var_offsets_zero = {"a": 0, "b": 4}
        stmt = {
            "type": "ASSIGN",
            "target": "a",
            "value": {"type": "CONST", "value": 0}
        }
        
        with patch("handle_assign_package.handle_assign_src.evaluate_expression") as mock_eval:
            mock_eval.return_value = ("    MOV R0, #0\n", 8, "R0")
            
            code, offset = handle_assign(stmt, self.func_name, self.label_counter,
                                         var_offsets_zero, 8)
            
            self.assertIn("    STR R0, [SP, #-0]\n", code)
    
    def test_large_offset_variable(self):
        """Test assignment to variable at large offset."""
        var_offsets_large = {"big": 1024}
        stmt = {
            "type": "ASSIGN",
            "target": "big",
            "value": {"type": "CONST", "value": 42}
        }
        
        with patch("handle_assign_package.handle_assign_src.evaluate_expression") as mock_eval:
            mock_eval.return_value = ("    MOV R0, #42\n", 1028, "R0")
            
            code, offset = handle_assign(stmt, self.func_name, self.label_counter,
                                         var_offsets_large, 1028)
            
            self.assertIn("    STR R0, [SP, #-1024]\n", code)
    
    def test_evaluate_expression_exception_propagation(self):
        """Test that exceptions from evaluate_expression are propagated."""
        stmt = {
            "type": "ASSIGN",
            "target": "x",
            "value": {"type": "UNSUPPORTED", "data": "test"}
        }
        
        with patch("handle_assign_package.handle_assign_src.evaluate_expression") as mock_eval:
            mock_eval.side_effect = ValueError("Unsupported expression type: UNSUPPORTED")
            
            with self.assertRaises(ValueError) as context:
                handle_assign(stmt, self.func_name, self.label_counter,
                             self.var_offsets, self.next_offset)
            
            self.assertIn("Unsupported expression type: UNSUPPORTED", str(context.exception))
    
    def test_code_order_expression_before_store(self):
        """Test that expression code comes before store instruction."""
        stmt = {
            "type": "ASSIGN",
            "target": "x",
            "value": {"type": "CONST", "value": 7}
        }
        
        with patch("handle_assign_package.handle_assign_src.evaluate_expression") as mock_eval:
            mock_eval.return_value = ("    MOV R0, #7\n", 16, "R0")
            
            code, offset = handle_assign(stmt, self.func_name, self.label_counter,
                                         self.var_offsets, self.next_offset)
            
            mov_pos = code.find("    MOV R0, #7\n")
            str_pos = code.find("    STR R0, [SP, #-4]\n")
            self.assertLess(mov_pos, str_pos, "Expression code should come before store instruction")


if __name__ == "__main__":
    unittest.main()

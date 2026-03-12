# === Test file for handle_return ===
import unittest
from typing import Dict, Any
from unittest.mock import patch

# Import the function under test using relative import
from .handle_return_src import handle_return


class TestHandleReturn(unittest.TestCase):
    """Test cases for handle_return function."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.func_name = "test_func"
        self.label_counter: Dict[str, int] = {"if_else": 0, "if_end": 0}
        self.var_offsets: Dict[str, int] = {"x": 0, "y": 1}
        self.next_offset = 5

    def test_return_with_expression_result_in_x0(self) -> None:
        """Test RETURN statement with expression where result is already in x0."""
        stmt: Dict[str, Any] = {
            "type": "RETURN",
            "expression": {"type": "literal", "value": 42}
        }
        
        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_return_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("    mov x0, #42", 6, "x0")
            
            code, updated_offset = handle_return(
                stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
            )
            
            # Verify generate_expression_code was called
            mock_gen_expr.assert_called_once_with(
                stmt["expression"], self.var_offsets, self.next_offset
            )
            
            # Verify no mov instruction since result is already in x0
            self.assertEqual(code, "    mov x0, #42\n    ret")
            self.assertEqual(updated_offset, 6)

    def test_return_with_expression_result_not_in_x0(self) -> None:
        """Test RETURN statement with expression where result is in different register."""
        stmt: Dict[str, Any] = {
            "type": "RETURN",
            "expression": {"type": "binary", "op": "+", "left": {"type": "var", "name": "x"}, "right": {"type": "literal", "value": 1}}
        }
        
        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_return_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("    add x1, x0, #1", 6, "x1")
            
            code, updated_offset = handle_return(
                stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
            )
            
            # Verify generate_expression_code was called
            mock_gen_expr.assert_called_once_with(
                stmt["expression"], self.var_offsets, self.next_offset
            )
            
            # Verify mov instruction to move result to x0
            self.assertEqual(code, "    add x1, x0, #1\n    mov x0, x1\n    ret")
            self.assertEqual(updated_offset, 6)

    def test_return_without_expression(self) -> None:
        """Test RETURN statement without expression (void return)."""
        stmt: Dict[str, Any] = {
            "type": "RETURN"
        }
        
        code, updated_offset = handle_return(
            stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
        )
        
        # Verify only ret instruction is emitted
        self.assertEqual(code, "    ret")
        self.assertEqual(updated_offset, self.next_offset)

    def test_return_with_none_expression(self) -> None:
        """Test RETURN statement with None expression (treated as void return)."""
        stmt: Dict[str, Any] = {
            "type": "RETURN",
            "expression": None
        }
        
        code, updated_offset = handle_return(
            stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
        )
        
        # Verify only ret instruction is emitted
        self.assertEqual(code, "    ret")
        self.assertEqual(updated_offset, self.next_offset)

    def test_return_with_complex_expression(self) -> None:
        """Test RETURN statement with complex nested expression."""
        stmt: Dict[str, Any] = {
            "type": "RETURN",
            "expression": {
                "type": "call",
                "function": "printf",
                "args": [{"type": "literal", "value": "Hello"}]
            }
        }
        
        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_return_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("    bl printf", 5, "x0")
            
            code, updated_offset = handle_return(
                stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
            )
            
            # Verify generate_expression_code was called with correct arguments
            mock_gen_expr.assert_called_once_with(
                stmt["expression"], self.var_offsets, self.next_offset
            )
            
            # Verify no mov needed since result is in x0
            self.assertEqual(code, "    bl printf\n    ret")
            self.assertEqual(updated_offset, 5)

    def test_return_does_not_modify_label_counter(self) -> None:
        """Test that handle_return does not modify label_counter."""
        stmt: Dict[str, Any] = {
            "type": "RETURN",
            "expression": {"type": "literal", "value": 0}
        }
        
        original_label_counter = self.label_counter.copy()
        
        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_return_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("    mov x0, #0", 6, "x0")
            
            handle_return(
                stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
            )
            
            # Verify label_counter was not modified
            self.assertEqual(self.label_counter, original_label_counter)

    def test_return_does_not_modify_var_offsets(self) -> None:
        """Test that handle_return does not modify var_offsets."""
        stmt: Dict[str, Any] = {
            "type": "RETURN",
            "expression": {"type": "literal", "value": 0}
        }
        
        original_var_offsets = self.var_offsets.copy()
        
        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_return_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("    mov x0, #0", 6, "x0")
            
            handle_return(
                stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
            )
            
            # Verify var_offsets was not modified
            self.assertEqual(self.var_offsets, original_var_offsets)

    def test_return_with_zero_offset(self) -> None:
        """Test RETURN statement with zero next_offset (boundary case)."""
        stmt: Dict[str, Any] = {
            "type": "RETURN",
            "expression": {"type": "literal", "value": 0}
        }
        
        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_return_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("    mov x0, #0", 1, "x0")
            
            code, updated_offset = handle_return(
                stmt, self.func_name, self.label_counter, self.var_offsets, 0
            )
            
            self.assertEqual(code, "    mov x0, #0\n    ret")
            self.assertEqual(updated_offset, 1)

    def test_return_preserves_func_name_parameter(self) -> None:
        """Test that func_name parameter is passed but not used in RETURN handling."""
        stmt: Dict[str, Any] = {
            "type": "RETURN"
        }
        
        # func_name should not affect the output for RETURN
        code1, _ = handle_return(
            stmt, "func1", self.label_counter, self.var_offsets, self.next_offset
        )
        code2, _ = handle_return(
            stmt, "func2", self.label_counter, self.var_offsets, self.next_offset
        )
        
        # Both should produce the same output
        self.assertEqual(code1, code2)
        self.assertEqual(code1, "    ret")


if __name__ == "__main__":
    unittest.main()

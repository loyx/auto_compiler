"""Unit tests for generate_statement_code function."""

import unittest
from unittest.mock import patch

from .generate_statement_code_src import generate_statement_code


class TestGenerateStatementCode(unittest.TestCase):
    """Test cases for generate_statement_code function."""

    def setUp(self):
        """Set up test fixtures."""
        self.func_name = "test_func"
        self.label_counter = {"while_cond": 0, "while_end": 0, "if_end": 0, "if_else": 0}
        self.var_offsets = {"x": 0, "y": 4, "z": 8}
        self.next_offset = 12

    def test_assign_statement(self):
        """Test ASSIGN statement generates correct assembly code."""
        stmt = {
            "type": "ASSIGN",
            "var_name": "x",
            "value": {"type": "CONST", "value": 42}
        }
        
        with patch("compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.evaluate_expression_package.evaluate_expression_src.evaluate_expression") as mock_eval:
            mock_eval.return_value = ("    mov r0, #42", 12)
            
            code, offset = generate_statement_code(
                stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
            )
            
            mock_eval.assert_called_once_with(
                {"type": "CONST", "value": 42},
                self.func_name,
                self.label_counter,
                self.var_offsets,
                self.next_offset
            )
            self.assertIn("mov r0, #42", code)
            self.assertIn("str r0, [sp, #0]", code)
            self.assertEqual(offset, 12)

    def test_if_statement_without_else(self):
        """Test IF statement without else body."""
        stmt = {
            "type": "IF",
            "condition": {"type": "CONST", "value": 1},
            "then_body": [
                {"type": "ASSIGN", "var_name": "y", "value": {"type": "CONST", "value": 10}}
            ]
        }
        
        with patch("compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.evaluate_expression_package.evaluate_expression_src.evaluate_expression") as mock_eval:
            mock_eval.return_value = ("    mov r0, #1", 12)
            
            with patch("compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.generate_statement_code_src.generate_statement_code") as mock_gen:
                mock_gen.return_value = ("    mov r0, #10\n    str r0, [sp, #4]", 12)
                
                label_counter = {"if_end": 0}
                code, offset = generate_statement_code(
                    stmt, self.func_name, label_counter, self.var_offsets, self.next_offset
                )
                
                self.assertEqual(label_counter["if_end"], 1)
                self.assertIn("test_func_if_end_0:", code)
                self.assertIn("beq test_func_if_end_0", code)

    def test_if_statement_with_else(self):
        """Test IF statement with else body."""
        stmt = {
            "type": "IF",
            "condition": {"type": "CONST", "value": 1},
            "then_body": [
                {"type": "ASSIGN", "var_name": "y", "value": {"type": "CONST", "value": 10}}
            ],
            "else_body": [
                {"type": "ASSIGN", "var_name": "y", "value": {"type": "CONST", "value": 20}}
            ]
        }
        
        with patch("compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.evaluate_expression_package.evaluate_expression_src.evaluate_expression") as mock_eval:
            mock_eval.return_value = ("    mov r0, #1", 12)
            
            with patch("compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.generate_statement_code_src.generate_statement_code") as mock_gen:
                mock_gen.return_value = ("    mov r0, #10\n    str r0, [sp, #4]", 12)
                
                label_counter = {"if_end": 0, "if_else": 0}
                code, offset = generate_statement_code(
                    stmt, self.func_name, label_counter, self.var_offsets, self.next_offset
                )
                
                self.assertEqual(label_counter["if_end"], 1)
                self.assertEqual(label_counter["if_else"], 1)
                self.assertIn("test_func_if_end_0:", code)
                self.assertIn("test_func_if_else_0:", code)
                self.assertIn("beq test_func_if_else_0", code)
                self.assertIn("b test_func_if_end_0", code)

    def test_while_statement(self):
        """Test WHILE statement delegates to handle_while."""
        stmt = {
            "type": "WHILE",
            "condition": {"type": "CONST", "value": 1},
            "body": [
                {"type": "ASSIGN", "var_name": "x", "value": {"type": "CONST", "value": 0}}
            ]
        }
        
        expected_code = "while_loop_code"
        expected_offset = 20
        
        with patch("compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_package.handle_while_src.handle_while") as mock_handle_while:
            mock_handle_while.return_value = (expected_code, expected_offset)
            
            code, offset = generate_statement_code(
                stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
            )
            
            mock_handle_while.assert_called_once_with(
                stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
            )
            self.assertEqual(code, expected_code)
            self.assertEqual(offset, expected_offset)

    def test_return_statement_with_expression(self):
        """Test RETURN statement with expression."""
        stmt = {
            "type": "RETURN",
            "expression": {"type": "CONST", "value": 42}
        }
        
        with patch("compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.evaluate_expression_package.evaluate_expression_src.evaluate_expression") as mock_eval:
            mock_eval.return_value = ("    mov r0, #42", 12)
            
            code, offset = generate_statement_code(
                stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
            )
            
            mock_eval.assert_called_once()
            self.assertIn("mov r0, #42", code)
            self.assertIn("bx lr", code)
            self.assertEqual(offset, 12)

    def test_return_statement_without_expression(self):
        """Test RETURN statement without expression (void return)."""
        stmt = {
            "type": "RETURN"
        }
        
        code, offset = generate_statement_code(
            stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
        )
        
        self.assertNotIn("evaluate_expression", code)
        self.assertIn("bx lr", code)
        self.assertEqual(offset, self.next_offset)

    def test_expr_statement(self):
        """Test EXPR statement evaluates expression and discards result."""
        stmt = {
            "type": "EXPR",
            "expression": {"type": "CONST", "value": 99}
        }
        
        with patch("compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.evaluate_expression_package.evaluate_expression_src.evaluate_expression") as mock_eval:
            mock_eval.return_value = ("    mov r0, #99", 12)
            
            code, offset = generate_statement_code(
                stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
            )
            
            mock_eval.assert_called_once()
            self.assertIn("mov r0, #99", code)
            self.assertEqual(offset, 12)

    def test_unknown_statement_type(self):
        """Test that unknown statement type raises ValueError."""
        stmt = {
            "type": "UNKNOWN_TYPE"
        }
        
        with self.assertRaises(ValueError) as context:
            generate_statement_code(
                stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
            )
        
        self.assertIn("Unknown statement type: UNKNOWN_TYPE", str(context.exception))

    def test_assign_with_variable_reference(self):
        """Test ASSIGN statement with variable reference as value."""
        stmt = {
            "type": "ASSIGN",
            "var_name": "z",
            "value": {"type": "VAR", "name": "x"}
        }
        
        with patch("compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.evaluate_expression_package.evaluate_expression_src.evaluate_expression") as mock_eval:
            mock_eval.return_value = ("    ldr r0, [sp, #0]", 12)
            
            code, offset = generate_statement_code(
                stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
            )
            
            self.assertIn("ldr r0, [sp, #0]", code)
            self.assertIn("str r0, [sp, #8]", code)

    def test_nested_if_statements(self):
        """Test nested IF statements generate correct labels."""
        stmt = {
            "type": "IF",
            "condition": {"type": "CONST", "value": 1},
            "then_body": [
                {
                    "type": "IF",
                    "condition": {"type": "CONST", "value": 2},
                    "then_body": []
                }
            ]
        }
        
        with patch("compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.evaluate_expression_package.evaluate_expression_src.evaluate_expression") as mock_eval:
            mock_eval.return_value = ("    mov r0, #1", 12)
            
            with patch("compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.generate_statement_code_src.generate_statement_code") as mock_gen:
                mock_gen.return_value = ("", 12)
                
                label_counter = {"if_end": 0}
                code, offset = generate_statement_code(
                    stmt, self.func_name, label_counter, self.var_offsets, self.next_offset
                )
                
                self.assertEqual(label_counter["if_end"], 2)


if __name__ == "__main__":
    unittest.main()

# -*- coding: utf-8 -*-
"""Unit tests for generate_statement_code function."""

import unittest
from unittest.mock import patch, MagicMock


class TestGenerateStatementCode(unittest.TestCase):
    """Test cases for generate_statement_code function."""

    def setUp(self):
        """Set up test fixtures."""
        self.func_name = "test_func"
        self.label_counter = {
            "if_else": 0,
            "if_end": 0,
            "while_cond": 0,
            "while_end": 0,
            "for_cond": 0,
            "for_end": 0,
            "for_update": 0,
        }
        self.var_offsets = {}
        self.next_offset = 0

    def _import_uut(self):
        """Import the unit under test."""
        from .generate_statement_code_src import generate_statement_code
        return generate_statement_code

    @patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_var_decl_package.handle_var_decl_src.handle_var_decl")
    def test_var_decl_statement(self, mock_handle_var_decl: MagicMock):
        """Test VAR_DECL statement delegates to handle_var_decl."""
        generate_statement_code = self._import_uut()
        
        stmt = {
            "type": "VAR_DECL",
            "var_name": "x",
            "var_type": "int",
            "init_value": {"type": "LITERAL", "value": 42}
        }
        mock_handle_var_decl.return_value = ("    // VAR_DECL code\n", 8)
        
        code, next_offset = generate_statement_code(
            stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
        )
        
        mock_handle_var_decl.assert_called_once_with(
            stmt, self.func_name, self.var_offsets, self.next_offset
        )
        self.assertEqual(code, "    // VAR_DECL code\n")
        self.assertEqual(next_offset, 8)

    @patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_assign_package.handle_assign_src.handle_assign")
    def test_assign_statement(self, mock_handle_assign: MagicMock):
        """Test ASSIGN statement delegates to handle_assign."""
        generate_statement_code = self._import_uut()
        
        stmt = {
            "type": "ASSIGN",
            "target": "x",
            "value": {"type": "LITERAL", "value": 10}
        }
        mock_handle_assign.return_value = "    // ASSIGN code\n"
        
        code, next_offset = generate_statement_code(
            stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
        )
        
        mock_handle_assign.assert_called_once_with(
            stmt, self.func_name, self.var_offsets
        )
        self.assertEqual(code, "    // ASSIGN code\n")
        self.assertEqual(next_offset, self.next_offset)

    @patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.generate_statement_code_src.handle_if")
    def test_if_statement(self, mock_handle_if: MagicMock):
        """Test IF statement delegates to handle_if."""
        generate_statement_code = self._import_uut()
        
        stmt = {
            "type": "IF",
            "condition": {"type": "BINARY_OP", "op": ">", "left": {"type": "IDENTIFIER", "name": "x"}, "right": {"type": "LITERAL", "value": 0}},
            "then_body": [{"type": "EXPRESSION", "expr": {"type": "FUNCTION_CALL", "func_name": "print", "args": []}}],
            "else_body": []
        }
        mock_handle_if.return_value = ("    // IF code\n", 0)
        
        code, next_offset = generate_statement_code(
            stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
        )
        
        mock_handle_if.assert_called_once_with(
            stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
        )
        self.assertEqual(code, "    // IF code\n")
        self.assertEqual(next_offset, 0)

    @patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.generate_statement_code_src.handle_while")
    def test_while_statement(self, mock_handle_while: MagicMock):
        """Test WHILE statement delegates to handle_while."""
        generate_statement_code = self._import_uut()
        
        stmt = {
            "type": "WHILE",
            "condition": {"type": "BINARY_OP", "op": "<", "left": {"type": "IDENTIFIER", "name": "i"}, "right": {"type": "LITERAL", "value": 10}},
            "body": [{"type": "EXPRESSION", "expr": {"type": "FUNCTION_CALL", "func_name": "print", "args": []}}]
        }
        mock_handle_while.return_value = ("    // WHILE code\n", 0)
        
        code, next_offset = generate_statement_code(
            stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
        )
        
        mock_handle_while.assert_called_once_with(
            stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
        )
        self.assertEqual(code, "    // WHILE code\n")
        self.assertEqual(next_offset, 0)

    @patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.generate_statement_code_src.handle_for")
    def test_for_statement(self, mock_handle_for: MagicMock):
        """Test FOR statement delegates to handle_for."""
        generate_statement_code = self._import_uut()
        
        stmt = {
            "type": "FOR",
            "init": {"type": "VAR_DECL", "var_name": "i", "var_type": "int", "init_value": {"type": "LITERAL", "value": 0}},
            "condition": {"type": "BINARY_OP", "op": "<", "left": {"type": "IDENTIFIER", "name": "i"}, "right": {"type": "LITERAL", "value": 10}},
            "update": {"type": "ASSIGN", "target": "i", "value": {"type": "BINARY_OP", "op": "+", "left": {"type": "IDENTIFIER", "name": "i"}, "right": {"type": "LITERAL", "value": 1}}},
            "body": [{"type": "EXPRESSION", "expr": {"type": "FUNCTION_CALL", "func_name": "print", "args": []}}]
        }
        mock_handle_for.return_value = ("    // FOR code\n", 0)
        
        code, next_offset = generate_statement_code(
            stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
        )
        
        mock_handle_for.assert_called_once_with(
            stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
        )
        self.assertEqual(code, "    // FOR code\n")
        self.assertEqual(next_offset, 0)

    @patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.generate_statement_code_src.handle_return")
    def test_return_statement(self, mock_handle_return: MagicMock):
        """Test RETURN statement delegates to handle_return."""
        generate_statement_code = self._import_uut()
        
        stmt = {
            "type": "RETURN",
            "value": {"type": "IDENTIFIER", "name": "x"}
        }
        mock_handle_return.return_value = "    // RETURN code\n"
        
        code, next_offset = generate_statement_code(
            stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
        )
        
        mock_handle_return.assert_called_once_with(
            stmt, self.func_name, self.var_offsets
        )
        self.assertEqual(code, "    // RETURN code\n")
        self.assertEqual(next_offset, self.next_offset)

    @patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.generate_statement_code_src.handle_expression_stmt")
    def test_expression_statement(self, mock_handle_expression_stmt: MagicMock):
        """Test EXPRESSION statement delegates to handle_expression_stmt."""
        generate_statement_code = self._import_uut()
        
        stmt = {
            "type": "EXPRESSION",
            "expr": {"type": "FUNCTION_CALL", "func_name": "print", "args": [{"type": "LITERAL", "value": 42}]}
        }
        mock_handle_expression_stmt.return_value = "    // EXPRESSION code\n"
        
        code, next_offset = generate_statement_code(
            stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
        )
        
        mock_handle_expression_stmt.assert_called_once_with(
            stmt, self.func_name, self.var_offsets
        )
        self.assertEqual(code, "    // EXPRESSION code\n")
        self.assertEqual(next_offset, self.next_offset)

    def test_break_statement(self):
        """Test BREAK statement generates branch to break label."""
        generate_statement_code = self._import_uut()
        
        stmt = {"type": "BREAK"}
        
        code, next_offset = generate_statement_code(
            stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
        )
        
        self.assertEqual(code, f"    b {self.func_name}_break")
        self.assertEqual(next_offset, self.next_offset)

    def test_continue_statement(self):
        """Test CONTINUE statement generates placeholder comment."""
        generate_statement_code = self._import_uut()
        
        stmt = {"type": "CONTINUE"}
        
        code, next_offset = generate_statement_code(
            stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
        )
        
        self.assertEqual(code, "    // CONTINUE placeholder")
        self.assertEqual(next_offset, self.next_offset)

    def test_unknown_statement_type(self):
        """Test unknown statement type generates unknown type comment."""
        generate_statement_code = self._import_uut()
        
        stmt = {"type": "UNKNOWN_TYPE"}
        
        code, next_offset = generate_statement_code(
            stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
        )
        
        self.assertEqual(code, "    // Unknown statement type: UNKNOWN_TYPE")
        self.assertEqual(next_offset, self.next_offset)

    def test_missing_type_field(self):
        """Test statement with missing type field defaults to unknown."""
        generate_statement_code = self._import_uut()
        
        stmt = {}
        
        code, next_offset = generate_statement_code(
            stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
        )
        
        self.assertEqual(code, "    // Unknown statement type: ")
        self.assertEqual(next_offset, self.next_offset)

    @patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.generate_statement_code_src.handle_var_decl")
    def test_next_offset_propagation(self, mock_handle_var_decl: MagicMock):
        """Test next_offset is properly propagated to handlers and returned."""
        generate_statement_code = self._import_uut()
        
        stmt = {"type": "VAR_DECL", "var_name": "x", "var_type": "int"}
        mock_handle_var_decl.return_value = ("    code\n", 16)
        
        _, returned_offset = generate_statement_code(
            stmt, self.func_name, self.label_counter, self.var_offsets, 8
        )
        
        mock_handle_var_decl.assert_called_once()
        call_args = mock_handle_var_decl.call_args
        self.assertEqual(call_args[0][3], 8)
        self.assertEqual(returned_offset, 16)

    @patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.generate_statement_code_src.handle_if")
    def test_label_counter_passed_to_handler(self, mock_handle_if: MagicMock):
        """Test label_counter is passed to handlers that need it."""
        generate_statement_code = self._import_uut()
        
        stmt = {
            "type": "IF",
            "condition": {"type": "LITERAL", "value": 1},
            "then_body": [],
            "else_body": []
        }
        mock_handle_if.return_value = ("    code\n", 0)
        
        generate_statement_code(
            stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
        )
        
        call_args = mock_handle_if.call_args
        self.assertIs(call_args[0][2], self.label_counter)

    @patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.generate_statement_code_src.handle_var_decl")
    def test_var_offsets_passed_to_handler(self, mock_handle_var_decl: MagicMock):
        """Test var_offsets is passed to handlers."""
        generate_statement_code = self._import_uut()
        
        stmt = {"type": "VAR_DECL", "var_name": "x", "var_type": "int"}
        mock_handle_var_decl.return_value = ("    code\n", 8)
        
        generate_statement_code(
            stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset
        )
        
        call_args = mock_handle_var_decl.call_args
        self.assertIs(call_args[0][2], self.var_offsets)


if __name__ == "__main__":
    unittest.main()

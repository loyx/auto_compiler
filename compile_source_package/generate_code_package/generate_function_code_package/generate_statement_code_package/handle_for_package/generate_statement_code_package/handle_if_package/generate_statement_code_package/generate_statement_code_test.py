# === std / third-party imports ===
import unittest
from typing import Tuple
from unittest.mock import patch, MagicMock

# === relative imports ===
from .generate_statement_code_src import generate_statement_code


class TestGenerateStatementCode(unittest.TestCase):
    """Test cases for generate_statement_code dispatcher function."""

    def setUp(self):
        """Set up common test fixtures."""
        self.func_name = "test_function"
        self.label_counter = {"if_else": 0, "if_end": 0, "while_start": 0, "while_end": 0}
        self.var_offsets = {"x": 0, "y": 4}
        self.next_offset = 8

    def _create_mock_handler(self, return_value: Tuple[str, int] = ("mock_asm", 10)):
        """Helper to create a mock handler with default return value."""
        mock = MagicMock(return_value=return_value)
        return mock

    # ==================== Happy Path Tests ====================

    def test_if_statement_routes_to_handle_if(self):
        """Test IF statement type routes to handle_if handler."""
        stmt = {
            "type": "IF",
            "condition": {"type": "LITERAL", "value": True},
            "then_body": [],
            "else_body": []
        }
        mock_return = ("if_asm_code", 12)

        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_if_src.handle_if") as mock_handle_if:
            mock_handle_if.return_value = mock_return

            result = generate_statement_code(stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset)

            mock_handle_if.assert_called_once_with(stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset)
            self.assertEqual(result, mock_return)

    def test_assign_statement_routes_to_handle_assign(self):
        """Test ASSIGN statement type routes to handle_assign handler."""
        stmt = {
            "type": "ASSIGN",
            "var_name": "x",
            "expression": {"type": "LITERAL", "value": 42}
        }
        mock_return = ("assign_asm_code", 8)

        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_assign_package.handle_assign_src.handle_assign") as mock_handle_assign:
            mock_handle_assign.return_value = mock_return

            result = generate_statement_code(stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset)

            mock_handle_assign.assert_called_once_with(stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset)
            self.assertEqual(result, mock_return)

    def test_return_statement_routes_to_handle_return(self):
        """Test RETURN statement type routes to handle_return handler."""
        stmt = {
            "type": "RETURN",
            "value": {"type": "LITERAL", "value": 0}
        }
        mock_return = ("return_asm_code", 8)

        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_return_package.handle_return_src.handle_return") as mock_handle_return:
            mock_handle_return.return_value = mock_return

            result = generate_statement_code(stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset)

            mock_handle_return.assert_called_once_with(stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset)
            self.assertEqual(result, mock_return)

    def test_return_without_value_routes_to_handle_return(self):
        """Test RETURN statement without value routes to handle_return handler."""
        stmt = {
            "type": "RETURN",
            "value": None
        }
        mock_return = ("return_asm_code", 8)

        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_return_package.handle_return_src.handle_return") as mock_handle_return:
            mock_handle_return.return_value = mock_return

            result = generate_statement_code(stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset)

            mock_handle_return.assert_called_once_with(stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset)
            self.assertEqual(result, mock_return)

    def test_while_statement_routes_to_handle_while(self):
        """Test WHILE statement type routes to handle_while handler."""
        stmt = {
            "type": "WHILE",
            "condition": {"type": "LITERAL", "value": True},
            "body": []
        }
        mock_return = ("while_asm_code", 16)

        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_while_package.handle_while_src.handle_while") as mock_handle_while:
            mock_handle_while.return_value = mock_return

            result = generate_statement_code(stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset)

            mock_handle_while.assert_called_once_with(stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset)
            self.assertEqual(result, mock_return)

    def test_decl_statement_routes_to_handle_decl(self):
        """Test DECL statement type routes to handle_decl handler."""
        stmt = {
            "type": "DECL",
            "var_name": "z",
            "var_type": "int"
        }
        mock_return = ("decl_asm_code", 12)

        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_decl_package.handle_decl_src.handle_decl") as mock_handle_decl:
            mock_handle_decl.return_value = mock_return

            result = generate_statement_code(stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset)

            mock_handle_decl.assert_called_once_with(stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset)
            self.assertEqual(result, mock_return)

    def test_call_statement_routes_to_handle_call(self):
        """Test CALL statement type routes to handle_call handler."""
        stmt = {
            "type": "CALL",
            "func_name": "printf",
            "args": [{"type": "LITERAL", "value": 42}]
        }
        mock_return = ("call_asm_code", 20)

        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_call_package.handle_call_src.handle_call") as mock_handle_call:
            mock_handle_call.return_value = mock_return

            result = generate_statement_code(stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset)

            mock_handle_call.assert_called_once_with(stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset)
            self.assertEqual(result, mock_return)

    def test_block_statement_routes_to_handle_block(self):
        """Test BLOCK statement type routes to handle_block handler."""
        stmt = {
            "type": "BLOCK",
            "statements": [
                {"type": "DECL", "var_name": "a", "var_type": "int"},
                {"type": "ASSIGN", "var_name": "a", "expression": {"type": "LITERAL", "value": 10}}
            ]
        }
        mock_return = ("block_asm_code", 24)

        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_block_package.handle_block_src.handle_block") as mock_handle_block:
            mock_handle_block.return_value = mock_return

            result = generate_statement_code(stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset)

            mock_handle_block.assert_called_once_with(stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset)
            self.assertEqual(result, mock_return)

    # ==================== Boundary Value Tests ====================

    def test_empty_block_statement(self):
        """Test BLOCK statement with empty statements list."""
        stmt = {
            "type": "BLOCK",
            "statements": []
        }
        mock_return = ("", 8)

        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_block_package.handle_block_src.handle_block") as mock_handle_block:
            mock_handle_block.return_value = mock_return

            result = generate_statement_code(stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset)

            mock_handle_block.assert_called_once_with(stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset)
            self.assertEqual(result, mock_return)

    def test_if_with_empty_bodies(self):
        """Test IF statement with empty then_body and else_body."""
        stmt = {
            "type": "IF",
            "condition": {"type": "LITERAL", "value": False},
            "then_body": [],
            "else_body": []
        }
        mock_return = ("if_asm", 8)

        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_if_package.handle_if_src.handle_if") as mock_handle_if:
            mock_handle_if.return_value = mock_return

            result = generate_statement_code(stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset)

            mock_handle_if.assert_called_once()
            self.assertEqual(result, mock_return)

    def test_offset_zero(self):
        """Test with next_offset = 0."""
        stmt = {"type": "DECL", "var_name": "x", "var_type": "int"}
        mock_return = ("decl_asm", 4)

        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_decl_package.handle_decl_src.handle_decl") as mock_handle_decl:
            mock_handle_decl.return_value = mock_return

            result = generate_statement_code(stmt, self.func_name, self.label_counter, self.var_offsets, 0)

            mock_handle_decl.assert_called_once_with(stmt, self.func_name, self.label_counter, self.var_offsets, 0)
            self.assertEqual(result, mock_return)

    def test_empty_var_offsets(self):
        """Test with empty var_offsets dict."""
        stmt = {"type": "DECL", "var_name": "new_var", "var_type": "int"}
        mock_return = ("decl_asm", 4)

        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_decl_package.handle_decl_src.handle_decl") as mock_handle_decl:
            mock_handle_decl.return_value = mock_return

            result = generate_statement_code(stmt, self.func_name, self.label_counter, {}, self.next_offset)

            mock_handle_decl.assert_called_once_with(stmt, self.func_name, self.label_counter, {}, self.next_offset)
            self.assertEqual(result, mock_return)

    def test_empty_label_counter(self):
        """Test with empty label_counter dict."""
        stmt = {"type": "IF", "condition": {"type": "LITERAL", "value": True}, "then_body": [], "else_body": []}
        mock_return = ("if_asm", 8)

        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_if_package.handle_if_src.handle_if") as mock_handle_if:
            mock_handle_if.return_value = mock_return

            result = generate_statement_code(stmt, self.func_name, {}, self.var_offsets, self.next_offset)

            mock_handle_if.assert_called_once_with(stmt, self.func_name, {}, self.var_offsets, self.next_offset)
            self.assertEqual(result, mock_return)

    # ==================== Invalid Input Tests ====================

    def test_unknown_statement_type_raises_value_error(self):
        """Test that unknown statement type raises ValueError."""
        stmt = {"type": "UNKNOWN_TYPE"}

        with self.assertRaises(ValueError) as context:
            generate_statement_code(stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset)

        self.assertIn("Unknown statement type: UNKNOWN_TYPE", str(context.exception))

    def test_missing_type_field_raises_value_error(self):
        """Test that missing type field raises ValueError."""
        stmt = {"var_name": "x"}

        with self.assertRaises(ValueError) as context:
            generate_statement_code(stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset)

        self.assertIn("Unknown statement type:", str(context.exception))

    def test_empty_type_field_raises_value_error(self):
        """Test that empty type field raises ValueError."""
        stmt = {"type": ""}

        with self.assertRaises(ValueError) as context:
            generate_statement_code(stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset)

        self.assertIn("Unknown statement type:", str(context.exception))

    # ==================== Return Value Propagation Tests ====================

    def test_handler_return_value_propagated_correctly(self):
        """Test that handler return value is correctly propagated."""
        stmt = {"type": "ASSIGN", "var_name": "x", "expression": {"type": "LITERAL", "value": 5}}
        expected_code = "LDR R0, [SP, #0]\nSTR R0, [SP, #8]"
        expected_offset = 16

        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_assign_package.handle_assign_src.handle_assign") as mock_handle_assign:
            mock_handle_assign.return_value = (expected_code, expected_offset)

            code, offset = generate_statement_code(stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset)

            self.assertEqual(code, expected_code)
            self.assertEqual(offset, expected_offset)

    def test_handler_return_zero_offset(self):
        """Test handler returning zero offset is propagated."""
        stmt = {"type": "RETURN", "value": None}

        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_return_package.handle_return_src.handle_return") as mock_handle_return:
            mock_handle_return.return_value = ("", 0)

            code, offset = generate_statement_code(stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset)

            self.assertEqual(offset, 0)

    def test_handler_return_large_offset(self):
        """Test handler returning large offset is propagated."""
        stmt = {"type": "BLOCK", "statements": []}
        large_offset = 10000

        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_block_package.handle_block_src.handle_block") as mock_handle_block:
            mock_handle_block.return_value = ("block_asm", large_offset)

            code, offset = generate_statement_code(stmt, self.func_name, self.label_counter, self.var_offsets, self.next_offset)

            self.assertEqual(offset, large_offset)

    # ==================== Parameter Passing Tests ====================

    def test_all_parameters_passed_to_handler(self):
        """Test that all parameters are correctly passed to handler."""
        stmt = {"type": "CALL", "func_name": "foo", "args": []}
        custom_func_name = "custom_func"
        custom_labels = {"custom": 1}
        custom_vars = {"custom_var": 100}
        custom_offset = 999

        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_call_package.handle_call_src.handle_call") as mock_handle_call:
            mock_handle_call.return_value = ("call", 1000)

            generate_statement_code(stmt, custom_func_name, custom_labels, custom_vars, custom_offset)

            mock_handle_call.assert_called_once_with(stmt, custom_func_name, custom_labels, custom_vars, custom_offset)

    def test_mutable_label_counter_passed_by_reference(self):
        """Test that label_counter dict is passed (can be mutated by handler)."""
        stmt = {"type": "IF", "condition": {"type": "LITERAL", "value": True}, "then_body": [], "else_body": []}
        label_counter = {"if_else": 0}

        def side_effect(s, fn, lc, vo, no):
            lc["if_else"] = 5
            return ("asm", 8)

        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_if_package.handle_if_src.handle_if") as mock_handle_if:
            mock_handle_if.side_effect = side_effect

            generate_statement_code(stmt, self.func_name, label_counter, self.var_offsets, self.next_offset)

            self.assertEqual(label_counter["if_else"], 5)

    def test_mutable_var_offsets_passed_by_reference(self):
        """Test that var_offsets dict is passed (can be mutated by handler)."""
        stmt = {"type": "DECL", "var_name": "new_var", "var_type": "int"}
        var_offsets = {"x": 0}

        def side_effect(s, fn, lc, vo, no):
            vo["new_var"] = 4
            return ("asm", 4)

        with patch("main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_for_package.generate_statement_code_package.handle_if_package.generate_statement_code_package.handle_decl_package.handle_decl_src.handle_decl") as mock_handle_decl:
            mock_handle_decl.side_effect = side_effect

            generate_statement_code(stmt, self.func_name, self.label_counter, var_offsets, self.next_offset)

            self.assertEqual(var_offsets["new_var"], 4)


if __name__ == "__main__":
    unittest.main()

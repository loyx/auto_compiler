# -*- coding: utf-8 -*-
"""Unit tests for generate_statement_code function."""

import unittest
from unittest.mock import patch

from .generate_statement_code_src import generate_statement_code


class TestGenerateStatementCode(unittest.TestCase):
    """Test cases for generate_statement_code dispatcher function."""

    def test_if_statement_delegates_to_handle_if(self):
        """IF statement should delegate to handle_if handler."""
        stmt = {
            "type": "IF",
            "condition": {"type": "BINARY", "op": "==", "left": {"type": "VAR", "name": "x"}, "right": {"type": "LITERAL", "value": 0}},
            "then_body": [{"type": "RETURN", "value": {"type": "LITERAL", "value": 1}}],
            "else_body": []
        }
        func_name = "test_func"
        label_counter = {"if_else": 0, "if_end": 0}
        var_offsets = {}
        next_offset = 0

        expected_code = "    CMP R0, 0\n    JE else_label\n    RET\nelse_label:\n"
        expected_offset = 5

        with patch("generate_statement_code_src.handle_if") as mock_handle_if:
            mock_handle_if.return_value = (expected_code, expected_offset)
            
            result_code, result_offset = generate_statement_code(
                stmt, func_name, label_counter, var_offsets, next_offset
            )

            mock_handle_if.assert_called_once_with(stmt, func_name, label_counter, var_offsets, next_offset)
            self.assertEqual(result_code, expected_code)
            self.assertEqual(result_offset, expected_offset)

    def test_while_statement_delegates_to_handle_while(self):
        """WHILE statement should delegate to handle_while handler."""
        stmt = {
            "type": "WHILE",
            "condition": {"type": "BINARY", "op": "<", "left": {"type": "VAR", "name": "i"}, "right": {"type": "LITERAL", "value": 10}},
            "body": [{"type": "EXPR", "expression": {"type": "BINARY", "op": "+", "left": {"type": "VAR", "name": "i"}, "right": {"type": "LITERAL", "value": 1}}}]
        }
        func_name = "loop_func"
        label_counter = {"while_start": 0, "while_end": 0}
        var_offsets = {}
        next_offset = 0

        expected_code = "while_start_0:\n    CMP R0, 10\n    JGE while_end_0\n    ADD R0, R1\n    JMP while_start_0\nwhile_end_0:\n"
        expected_offset = 3

        with patch("generate_statement_code_src.handle_while") as mock_handle_while:
            mock_handle_while.return_value = (expected_code, expected_offset)
            
            result_code, result_offset = generate_statement_code(
                stmt, func_name, label_counter, var_offsets, next_offset
            )

            mock_handle_while.assert_called_once_with(stmt, func_name, label_counter, var_offsets, next_offset)
            self.assertEqual(result_code, expected_code)
            self.assertEqual(result_offset, expected_offset)

    def test_assign_statement(self):
        """ASSIGN statement should generate expression code and STORE_VAR."""
        stmt = {
            "type": "ASSIGN",
            "var_name": "x",
            "value": {"type": "LITERAL", "value": 42}
        }
        var_offsets = {"x": 0}
        next_offset = 1

        with patch("generate_statement_code_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("    LOAD_IMM R0, 42", 1, "R0")
            
            result_code, result_offset = generate_statement_code(
                stmt, "func", {}, var_offsets, next_offset
            )

            mock_gen_expr.assert_called_once_with({"type": "LITERAL", "value": 42}, var_offsets, next_offset)
            self.assertIn("LOAD_IMM R0, 42", result_code)
            self.assertIn("STORE_VAR x", result_code)
            self.assertEqual(result_offset, 1)

    def test_decl_statement_without_initial_value(self):
        """DECL statement without initial value should allocate slot and modify var_offsets."""
        stmt = {
            "type": "DECL",
            "var_name": "y"
        }
        var_offsets = {"x": 0}
        next_offset = 1

        result_code, result_offset = generate_statement_code(
            stmt, "func", {}, var_offsets, next_offset
        )

        self.assertEqual(var_offsets["y"], 1)
        self.assertEqual(result_offset, 2)
        self.assertEqual(result_code, "")

    def test_decl_statement_with_initial_value(self):
        """DECL statement with initial value should allocate slot, initialize, and modify var_offsets."""
        stmt = {
            "type": "DECL",
            "var_name": "z",
            "initial_value": {"type": "LITERAL", "value": 100}
        }
        var_offsets = {"x": 0}
        next_offset = 1

        with patch("generate_statement_code_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("    LOAD_IMM R0, 100", 1, "R0")
            
            result_code, result_offset = generate_statement_code(
                stmt, "func", {}, var_offsets, next_offset
            )

            self.assertEqual(var_offsets["z"], 1)
            self.assertEqual(result_offset, 2)
            self.assertIn("LOAD_IMM R0, 100", result_code)
            self.assertIn("STORE_VAR z", result_code)

    def test_return_statement_with_value(self):
        """RETURN statement with value should generate expression code and RET_VALUE."""
        stmt = {
            "type": "RETURN",
            "value": {"type": "VAR", "name": "result"}
        }
        var_offsets = {"result": 0}
        next_offset = 1

        with patch("generate_statement_code_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("    LOAD_VAR R0, [result]", 1, "R0")
            
            result_code, result_offset = generate_statement_code(
                stmt, "func", {}, var_offsets, next_offset
            )

            mock_gen_expr.assert_called_once_with({"type": "VAR", "name": "result"}, var_offsets, next_offset)
            self.assertIn("LOAD_VAR R0, [result]", result_code)
            self.assertIn("RET_VALUE", result_code)
            self.assertEqual(result_offset, 1)

    def test_return_statement_without_value(self):
        """RETURN statement without value should generate simple RET."""
        stmt = {
            "type": "RETURN"
        }
        var_offsets = {}
        next_offset = 0

        result_code, result_offset = generate_statement_code(
            stmt, "func", {}, var_offsets, next_offset
        )

        self.assertEqual(result_code, "    RET")
        self.assertEqual(result_offset, 0)

    def test_expr_statement(self):
        """EXPR statement should generate expression code and discard result."""
        stmt = {
            "type": "EXPR",
            "expression": {"type": "CALL", "func": "print", "args": [{"type": "LITERAL", "value": "hello"}]}
        }
        var_offsets = {}
        next_offset = 0

        with patch("generate_statement_code_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("    CALL print", 0, "R0")
            
            result_code, result_offset = generate_statement_code(
                stmt, "func", {}, var_offsets, next_offset
            )

            mock_gen_expr.assert_called_once_with({"type": "CALL", "func": "print", "args": [{"type": "LITERAL", "value": "hello"}]}, var_offsets, next_offset)
            self.assertEqual(result_code, "    CALL print")
            self.assertEqual(result_offset, 0)

    def test_break_statement(self):
        """BREAK statement should generate simple BREAK instruction."""
        stmt = {"type": "BREAK"}
        var_offsets = {}
        next_offset = 5

        result_code, result_offset = generate_statement_code(
            stmt, "func", {}, var_offsets, next_offset
        )

        self.assertEqual(result_code, "    BREAK")
        self.assertEqual(result_offset, 5)

    def test_continue_statement(self):
        """CONTINUE statement should generate simple CONTINUE instruction."""
        stmt = {"type": "CONTINUE"}
        var_offsets = {}
        next_offset = 3

        result_code, result_offset = generate_statement_code(
            stmt, "func", {}, var_offsets, next_offset
        )

        self.assertEqual(result_code, "    CONTINUE")
        self.assertEqual(result_offset, 3)

    def test_block_statement_with_multiple_statements(self):
        """BLOCK statement should process each statement in sequence."""
        stmt = {
            "type": "BLOCK",
            "statements": [
                {"type": "DECL", "var_name": "a"},
                {"type": "ASSIGN", "var_name": "a", "value": {"type": "LITERAL", "value": 10}},
                {"type": "RETURN", "value": {"type": "VAR", "name": "a"}}
            ]
        }
        func_name = "block_func"
        label_counter = {}
        var_offsets = {}
        next_offset = 0

        with patch("generate_statement_code_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.side_effect = [
                ("    LOAD_IMM R0, 10", 1, "R0"),
                ("    LOAD_VAR R0, [a]", 2, "R0")
            ]
            
            result_code, result_offset = generate_statement_code(
                stmt, func_name, label_counter, var_offsets, next_offset
            )

            self.assertIn("LOAD_IMM R0, 10", result_code)
            self.assertIn("STORE_VAR a", result_code)
            self.assertIn("LOAD_VAR R0, [a]", result_code)
            self.assertIn("RET_VALUE", result_code)
            self.assertEqual(var_offsets["a"], 0)
            self.assertEqual(result_offset, 2)

    def test_block_statement_with_empty_statements(self):
        """BLOCK statement with empty statements list should return empty code."""
        stmt = {
            "type": "BLOCK",
            "statements": []
        }
        var_offsets = {}
        next_offset = 0

        result_code, result_offset = generate_statement_code(
            stmt, "func", {}, var_offsets, next_offset
        )

        self.assertEqual(result_code, "")
        self.assertEqual(result_offset, 0)

    def test_block_statement_with_statements_returning_empty_code(self):
        """BLOCK statement should skip statements that return empty code."""
        stmt = {
            "type": "BLOCK",
            "statements": [
                {"type": "DECL", "var_name": "x"},
                {"type": "DECL", "var_name": "y"}
            ]
        }
        var_offsets = {}
        next_offset = 0

        result_code, result_offset = generate_statement_code(
            stmt, "func", {}, var_offsets, next_offset
        )

        self.assertEqual(result_code, "")
        self.assertEqual(result_offset, 2)
        self.assertEqual(var_offsets["x"], 0)
        self.assertEqual(var_offsets["y"], 1)

    def test_unknown_statement_type_raises_value_error(self):
        """Unknown statement type should raise ValueError."""
        stmt = {"type": "UNKNOWN_TYPE"}
        var_offsets = {}
        next_offset = 0

        with self.assertRaises(ValueError) as context:
            generate_statement_code(stmt, "func", {}, var_offsets, next_offset)

        self.assertIn("Unknown statement type: UNKNOWN_TYPE", str(context.exception))

    def test_var_offsets_modified_in_place_for_decl(self):
        """DECL statement should modify var_offsets dictionary in-place."""
        stmt = {"type": "DECL", "var_name": "new_var"}
        var_offsets = {"existing": 0}
        original_var_offsets_id = id(var_offsets)
        next_offset = 1

        generate_statement_code(stmt, "func", {}, var_offsets, next_offset)

        self.assertEqual(id(var_offsets), original_var_offsets_id)
        self.assertEqual(len(var_offsets), 2)
        self.assertEqual(var_offsets["existing"], 0)
        self.assertEqual(var_offsets["new_var"], 1)

    def test_label_counter_passed_through_to_handlers(self):
        """Label counter should be passed through to IF and WHILE handlers."""
        if_stmt = {"type": "IF", "condition": {}, "then_body": [], "else_body": []}
        while_stmt = {"type": "WHILE", "condition": {}, "body": []}
        label_counter = {"if_else": 5, "if_end": 3, "while_start": 2, "while_end": 1}
        var_offsets = {}
        next_offset = 0

        with patch("generate_statement_code_src.handle_if") as mock_handle_if:
            mock_handle_if.return_value = ("", 0)
            generate_statement_code(if_stmt, "func", label_counter, var_offsets, next_offset)
            mock_handle_if.assert_called_once()
            self.assertEqual(mock_handle_if.call_args[0][2], label_counter)

        with patch("generate_statement_code_src.handle_while") as mock_handle_while:
            mock_handle_while.return_value = ("", 0)
            generate_statement_code(while_stmt, "func", label_counter, var_offsets, next_offset)
            mock_handle_while.assert_called_once()
            self.assertEqual(mock_handle_while.call_args[0][2], label_counter)


if __name__ == "__main__":
    unittest.main()

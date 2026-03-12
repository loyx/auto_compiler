# -*- coding: utf-8 -*-
"""Unit tests for _parse_block function."""

import unittest
from unittest.mock import patch

from ._parse_block_src import _parse_block


class TestParseBlock(unittest.TestCase):
    """Test cases for _parse_block function."""

    def test_empty_block(self):
        """Test parsing an empty block: {}"""
        tokens = [
            {"type": "LBRACE", "value": "{", "line": 1, "column": 1},
            {"type": "RBRACE", "value": "}", "line": 1, "column": 2},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.c"}

        result = _parse_block(parser_state)

        self.assertEqual(result["type"], "BLOCK")
        self.assertEqual(result["children"], [])
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 2)

    def test_block_with_single_expr_stmt(self):
        """Test parsing a block with a single expression statement."""
        tokens = [
            {"type": "LBRACE", "value": "{", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 3},
            {"type": "RBRACE", "value": "}", "line": 1, "column": 5},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.c"}

        mock_expr_stmt = {"type": "EXPR_STMT", "children": [], "line": 1, "column": 3}

        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_expr_stmt_package._parse_expr_stmt_src._parse_expr_stmt",
            return_value=mock_expr_stmt,
        ):
            result = _parse_block(parser_state)

        self.assertEqual(result["type"], "BLOCK")
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0]["type"], "EXPR_STMT")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 2)

    def test_block_with_multiple_statements(self):
        """Test parsing a block with multiple statements of different types."""
        tokens = [
            {"type": "LBRACE", "value": "{", "line": 1, "column": 1},
            {"type": "VAR", "value": "var", "line": 2, "column": 2},
            {"type": "IF", "value": "if", "line": 3, "column": 2},
            {"type": "RETURN", "value": "return", "line": 4, "column": 2},
            {"type": "RBRACE", "value": "}", "line": 5, "column": 1},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.c"}

        mock_var_decl = {"type": "VAR_DECL", "children": [], "line": 2, "column": 2}
        mock_if_stmt = {"type": "IF", "children": [], "line": 3, "column": 2}
        mock_return_stmt = {"type": "RETURN", "children": [], "line": 4, "column": 2}

        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_var_decl_package._parse_var_decl_src._parse_var_decl",
            return_value=mock_var_decl,
        ), patch(
            "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_if_stmt_package._parse_if_stmt_src._parse_if_stmt",
            return_value=mock_if_stmt,
        ), patch(
            "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_return_stmt_package._parse_return_stmt_src._parse_return_stmt",
            return_value=mock_return_stmt,
        ):
            result = _parse_block(parser_state)

        self.assertEqual(result["type"], "BLOCK")
        self.assertEqual(len(result["children"]), 3)
        self.assertEqual(result["children"][0]["type"], "VAR_DECL")
        self.assertEqual(result["children"][1]["type"], "IF")
        self.assertEqual(result["children"][2]["type"], "RETURN")
        self.assertEqual(parser_state["pos"], 4)

    def test_block_with_while_stmt(self):
        """Test parsing a block with a WHILE statement."""
        tokens = [
            {"type": "LBRACE", "value": "{", "line": 1, "column": 1},
            {"type": "WHILE", "value": "while", "line": 2, "column": 2},
            {"type": "RBRACE", "value": "}", "line": 3, "column": 1},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.c"}

        mock_while_stmt = {"type": "WHILE", "children": [], "line": 2, "column": 2}

        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_while_stmt_package._parse_while_stmt_src._parse_while_stmt",
            return_value=mock_while_stmt,
        ):
            result = _parse_block(parser_state)

        self.assertEqual(result["type"], "BLOCK")
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0]["type"], "WHILE")
        self.assertEqual(parser_state["pos"], 2)

    def test_block_with_for_stmt(self):
        """Test parsing a block with a FOR statement."""
        tokens = [
            {"type": "LBRACE", "value": "{", "line": 1, "column": 1},
            {"type": "FOR", "value": "for", "line": 2, "column": 2},
            {"type": "RBRACE", "value": "}", "line": 3, "column": 1},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.c"}

        mock_for_stmt = {"type": "FOR", "children": [], "line": 2, "column": 2}

        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_for_stmt_package._parse_for_stmt_src._parse_for_stmt",
            return_value=mock_for_stmt,
        ):
            result = _parse_block(parser_state)

        self.assertEqual(result["type"], "BLOCK")
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0]["type"], "FOR")
        self.assertEqual(parser_state["pos"], 2)

    def test_block_with_break_stmt(self):
        """Test parsing a block with a BREAK statement."""
        tokens = [
            {"type": "LBRACE", "value": "{", "line": 1, "column": 1},
            {"type": "BREAK", "value": "break", "line": 2, "column": 2},
            {"type": "RBRACE", "value": "}", "line": 3, "column": 1},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.c"}

        mock_break_stmt = {"type": "BREAK", "children": [], "line": 2, "column": 2}

        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_break_stmt_package._parse_break_stmt_src._parse_break_stmt",
            return_value=mock_break_stmt,
        ):
            result = _parse_block(parser_state)

        self.assertEqual(result["type"], "BLOCK")
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0]["type"], "BREAK")
        self.assertEqual(parser_state["pos"], 2)

    def test_block_with_continue_stmt(self):
        """Test parsing a block with a CONTINUE statement."""
        tokens = [
            {"type": "LBRACE", "value": "{", "line": 1, "column": 1},
            {"type": "CONTINUE", "value": "continue", "line": 2, "column": 2},
            {"type": "RBRACE", "value": "}", "line": 3, "column": 1},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.c"}

        mock_continue_stmt = {"type": "CONTINUE", "children": [], "line": 2, "column": 2}

        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_continue_stmt_package._parse_continue_stmt_src._parse_continue_stmt",
            return_value=mock_continue_stmt,
        ):
            result = _parse_block(parser_state)

        self.assertEqual(result["type"], "BLOCK")
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0]["type"], "CONTINUE")
        self.assertEqual(parser_state["pos"], 2)

    def test_block_with_let_decl(self):
        """Test parsing a block with a LET variable declaration."""
        tokens = [
            {"type": "LBRACE", "value": "{", "line": 1, "column": 1},
            {"type": "LET", "value": "let", "line": 2, "column": 2},
            {"type": "RBRACE", "value": "}", "line": 3, "column": 1},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.c"}

        mock_var_decl = {"type": "VAR_DECL", "children": [], "line": 2, "column": 2}

        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_var_decl_package._parse_var_decl_src._parse_var_decl",
            return_value=mock_var_decl,
        ):
            result = _parse_block(parser_state)

        self.assertEqual(result["type"], "BLOCK")
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0]["type"], "VAR_DECL")
        self.assertEqual(parser_state["pos"], 2)

    def test_block_with_const_decl(self):
        """Test parsing a block with a CONST variable declaration."""
        tokens = [
            {"type": "LBRACE", "value": "{", "line": 1, "column": 1},
            {"type": "CONST", "value": "const", "line": 2, "column": 2},
            {"type": "RBRACE", "value": "}", "line": 3, "column": 1},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.c"}

        mock_var_decl = {"type": "VAR_DECL", "children": [], "line": 2, "column": 2}

        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_var_decl_package._parse_var_decl_src._parse_var_decl",
            return_value=mock_var_decl,
        ):
            result = _parse_block(parser_state)

        self.assertEqual(result["type"], "BLOCK")
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0]["type"], "VAR_DECL")
        self.assertEqual(parser_state["pos"], 2)

    def test_unexpected_eof_before_lbrace(self):
        """Test that SyntaxError is raised when EOF is reached before LBRACE."""
        tokens = []
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.c"}

        with self.assertRaises(SyntaxError) as context:
            _parse_block(parser_state)

        self.assertIn("Unexpected end of file", str(context.exception))
        self.assertIn("expected '{'", str(context.exception))

    def test_wrong_token_type_instead_of_lbrace(self):
        """Test that SyntaxError is raised when current token is not LBRACE."""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.c"}

        with self.assertRaises(SyntaxError) as context:
            _parse_block(parser_state)

        self.assertIn("Expected '{'", str(context.exception))
        self.assertIn("IDENTIFIER", str(context.exception))

    def test_block_line_column_from_lbrace(self):
        """Test that BLOCK node line/column are taken from LBRACE token."""
        tokens = [
            {"type": "LBRACE", "value": "{", "line": 10, "column": 25},
            {"type": "RBRACE", "value": "}", "line": 10, "column": 26},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.c"}

        result = _parse_block(parser_state)

        self.assertEqual(result["line"], 10)
        self.assertEqual(result["column"], 25)


if __name__ == "__main__":
    unittest.main()

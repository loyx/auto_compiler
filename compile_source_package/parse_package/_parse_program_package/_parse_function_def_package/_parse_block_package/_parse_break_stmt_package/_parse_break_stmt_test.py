# -*- coding: utf-8 -*-
"""
Unit tests for _parse_break_stmt function.
Tests the break statement parser node implementation.
"""

import unittest
from typing import Dict, Any

# Relative import from the same package
from ._parse_break_stmt_src import _parse_break_stmt


class TestParseBreakStmt(unittest.TestCase):
    """Test cases for _parse_break_stmt parser function."""

    def _create_parser_state(self, tokens: list, pos: int = 0, filename: str = "test.src") -> Dict[str, Any]:
        """Helper to create a parser state dictionary."""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename,
            "error": None
        }

    def _create_token(self, token_type: str, value: str, line: int, column: int) -> Dict[str, Any]:
        """Helper to create a token dictionary."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    # ==================== Happy Path Tests ====================

    def test_parse_break_stmt_simple(self):
        """Test parsing a simple break statement without semicolon."""
        tokens = [
            self._create_token("BREAK", "break", 5, 10)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        result = _parse_break_stmt(parser_state)

        self.assertEqual(result["type"], "BREAK_STMT")
        self.assertEqual(result["children"], [])
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 10)
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_break_stmt_with_semicolon(self):
        """Test parsing a break statement followed by semicolon."""
        tokens = [
            self._create_token("BREAK", "break", 10, 5),
            self._create_token("SEMICOLON", ";", 10, 11)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        result = _parse_break_stmt(parser_state)

        self.assertEqual(result["type"], "BREAK_STMT")
        self.assertEqual(result["children"], [])
        self.assertEqual(result["line"], 10)
        self.assertEqual(result["column"], 5)
        self.assertEqual(parser_state["pos"], 2)

    def test_parse_break_stmt_middle_of_tokens(self):
        """Test parsing break statement in the middle of token stream."""
        tokens = [
            self._create_token("IDENTIFIER", "x", 1, 1),
            self._create_token("BREAK", "break", 2, 5),
            self._create_token("SEMICOLON", ";", 2, 10),
            self._create_token("IDENTIFIER", "y", 3, 1)
        ]
        parser_state = self._create_parser_state(tokens, pos=1)

        result = _parse_break_stmt(parser_state)

        self.assertEqual(result["type"], "BREAK_STMT")
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 5)
        self.assertEqual(parser_state["pos"], 3)

    def test_parse_break_stmt_without_semicolon_next_token_exists(self):
        """Test parsing break without semicolon when next token is not semicolon."""
        tokens = [
            self._create_token("BREAK", "break", 5, 1),
            self._create_token("IDENTIFIER", "x", 5, 7)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        result = _parse_break_stmt(parser_state)

        self.assertEqual(result["type"], "BREAK_STMT")
        self.assertEqual(parser_state["pos"], 1)

    # ==================== Boundary Value Tests ====================

    def test_parse_break_stmt_at_end_of_tokens(self):
        """Test parsing break statement as the last token."""
        tokens = [
            self._create_token("BREAK", "break", 100, 1)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        result = _parse_break_stmt(parser_state)

        self.assertEqual(result["type"], "BREAK_STMT")
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_break_stmt_position_at_token_boundary(self):
        """Test parsing break when pos is exactly at the last valid index."""
        tokens = [
            self._create_token("IDENTIFIER", "x", 1, 1),
            self._create_token("BREAK", "break", 2, 1)
        ]
        parser_state = self._create_parser_state(tokens, pos=1)

        result = _parse_break_stmt(parser_state)

        self.assertEqual(result["type"], "BREAK_STMT")
        self.assertEqual(result["line"], 2)
        self.assertEqual(parser_state["pos"], 2)

    # ==================== Error Cases ====================

    def test_parse_break_stmt_position_beyond_tokens(self):
        """Test parsing when position is beyond token list length."""
        tokens = [
            self._create_token("IDENTIFIER", "x", 1, 1)
        ]
        parser_state = self._create_parser_state(tokens, pos=5)

        with self.assertRaises(SyntaxError) as context:
            _parse_break_stmt(parser_state)

        self.assertIn("Unexpected end of input", str(context.exception))

    def test_parse_break_stmt_position_at_empty_tokens(self):
        """Test parsing when token list is empty."""
        tokens = []
        parser_state = self._create_parser_state(tokens, pos=0)

        with self.assertRaises(SyntaxError) as context:
            _parse_break_stmt(parser_state)

        self.assertIn("Unexpected end of input", str(context.exception))

    def test_parse_break_stmt_wrong_token_type(self):
        """Test parsing when current token is not BREAK type."""
        tokens = [
            self._create_token("IDENTIFIER", "continue", 5, 10)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        with self.assertRaises(SyntaxError) as context:
            _parse_break_stmt(parser_state)

        self.assertIn("Expected BREAK token", str(context.exception))
        self.assertIn("IDENTIFIER", str(context.exception))

    def test_parse_break_stmt_different_token_types(self):
        """Test parsing with various non-BREAK token types."""
        non_break_types = ["IF", "WHILE", "FOR", "RETURN", "CONTINUE", "VAR", "FUNCTION"]

        for token_type in non_break_types:
            tokens = [self._create_token(token_type, "keyword", 1, 1)]
            parser_state = self._create_parser_state(tokens, pos=0)

            with self.assertRaises(SyntaxError) as context:
                _parse_break_stmt(parser_state)

            self.assertIn("Expected BREAK token", str(context.exception))

    def test_parse_break_stmt_token_missing_type_field(self):
        """Test parsing when token is missing type field."""
        tokens = [
            {"value": "break", "line": 1, "column": 1}
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        with self.assertRaises(SyntaxError) as context:
            _parse_break_stmt(parser_state)

        self.assertIn("Expected BREAK token", str(context.exception))

    def test_parse_break_stmt_token_with_none_type(self):
        """Test parsing when token type is None."""
        tokens = [
            self._create_token(None, "break", 1, 1)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        with self.assertRaises(SyntaxError) as context:
            _parse_break_stmt(parser_state)

        self.assertIn("Expected BREAK token", str(context.exception))

    # ==================== State Mutation Tests ====================

    def test_parse_break_stmt_does_not_modify_tokens(self):
        """Test that the function does not modify the tokens list."""
        tokens = [
            self._create_token("BREAK", "break", 1, 1),
            self._create_token("SEMICOLON", ";", 1, 6)
        ]
        original_tokens = [t.copy() for t in tokens]
        parser_state = self._create_parser_state(tokens, pos=0)

        _parse_break_stmt(parser_state)

        self.assertEqual(tokens, original_tokens)

    def test_parse_break_stmt_preserves_other_state_fields(self):
        """Test that other parser state fields are preserved."""
        tokens = [self._create_token("BREAK", "break", 1, 1)]
        parser_state = self._create_parser_state(tokens, pos=0, filename="my_test.src")
        parser_state["error"] = "some error"
        parser_state["custom_field"] = "custom value"

        _parse_break_stmt(parser_state)

        self.assertEqual(parser_state["filename"], "my_test.src")
        self.assertEqual(parser_state["error"], "some error")
        self.assertEqual(parser_state["custom_field"], "custom value")

    # ==================== AST Node Structure Tests ====================

    def test_parse_break_stmt_ast_node_has_required_fields(self):
        """Test that returned AST node has all required fields."""
        tokens = [self._create_token("BREAK", "break", 10, 20)]
        parser_state = self._create_parser_state(tokens, pos=0)

        result = _parse_break_stmt(parser_state)

        self.assertIn("type", result)
        self.assertIn("children", result)
        self.assertIn("line", result)
        self.assertIn("column", result)

    def test_parse_break_stmt_ast_node_no_extra_fields(self):
        """Test that returned AST node has no unexpected fields."""
        tokens = [self._create_token("BREAK", "break", 1, 1)]
        parser_state = self._create_parser_state(tokens, pos=0)

        result = _parse_break_stmt(parser_state)

        expected_keys = {"type", "children", "line", "column"}
        self.assertEqual(set(result.keys()), expected_keys)

    def test_parse_break_stmt_children_is_empty_list(self):
        """Test that children field is an empty list, not None or other type."""
        tokens = [self._create_token("BREAK", "break", 1, 1)]
        parser_state = self._create_parser_state(tokens, pos=0)

        result = _parse_break_stmt(parser_state)

        self.assertIsInstance(result["children"], list)
        self.assertEqual(len(result["children"]), 0)

    def test_parse_break_stmt_preserves_position_info(self):
        """Test that line and column information is preserved correctly."""
        test_cases = [
            (1, 1),
            (100, 50),
            (999, 999),
            (0, 0)
        ]

        for line, column in test_cases:
            tokens = [self._create_token("BREAK", "break", line, column)]
            parser_state = self._create_parser_state(tokens, pos=0)

            result = _parse_break_stmt(parser_state)

            self.assertEqual(result["line"], line, f"Failed for line={line}")
            self.assertEqual(result["column"], column, f"Failed for column={column}")


class TestParseBreakStmtIntegration(unittest.TestCase):
    """Integration tests for _parse_break_stmt in realistic scenarios."""

    def _create_token(self, token_type: str, value: str, line: int, column: int):
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def test_parse_break_stmt_in_while_loop_context(self):
        """Test break statement in a while loop context."""
        tokens = [
            self._create_token("WHILE", "while", 1, 1),
            self._create_token("LPAREN", "(", 1, 7),
            self._create_token("IDENTIFIER", "cond", 1, 8),
            self._create_token("RPAREN", ")", 1, 12),
            self._create_token("LBRACE", "{", 1, 14),
            self._create_token("BREAK", "break", 2, 5),
            self._create_token("SEMICOLON", ";", 2, 10),
            self._create_token("RBRACE", "}", 3, 1)
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 5,
            "filename": "loop.src",
            "error": None
        }

        result = _parse_break_stmt(parser_state)

        self.assertEqual(result["type"], "BREAK_STMT")
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 5)
        self.assertEqual(parser_state["pos"], 7)

    def test_parse_break_stmt_in_for_loop_context(self):
        """Test break statement in a for loop context."""
        tokens = [
            self._create_token("FOR", "for", 1, 1),
            self._create_token("LPAREN", "(", 1, 5),
            self._create_token("IDENTIFIER", "i", 1, 6),
            self._create_token("SEMICOLON", ";", 1, 7),
            self._create_token("IDENTIFIER", "i", 1, 9),
            self._create_token("LT", "<", 1, 11),
            self._create_token("NUMBER", "10", 1, 13),
            self._create_token("RPAREN", ")", 1, 15),
            self._create_token("LBRACE", "{", 1, 17),
            self._create_token("BREAK", "break", 2, 5),
            self._create_token("RBRACE", "}", 3, 1)
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 9,
            "filename": "for_loop.src",
            "error": None
        }

        result = _parse_break_stmt(parser_state)

        self.assertEqual(result["type"], "BREAK_STMT")
        self.assertEqual(result["line"], 2)
        self.assertEqual(parser_state["pos"], 10)

    def test_multiple_break_statements_sequential(self):
        """Test parsing multiple break statements sequentially."""
        tokens = [
            self._create_token("BREAK", "break", 1, 1),
            self._create_token("SEMICOLON", ";", 1, 6),
            self._create_token("BREAK", "break", 2, 1),
            self._create_token("SEMICOLON", ";", 2, 6)
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "multi.src",
            "error": None
        }

        result1 = _parse_break_stmt(parser_state)
        result2 = _parse_break_stmt(parser_state)

        self.assertEqual(result1["type"], "BREAK_STMT")
        self.assertEqual(result1["line"], 1)
        self.assertEqual(result2["type"], "BREAK_STMT")
        self.assertEqual(result2["line"], 2)
        self.assertEqual(parser_state["pos"], 4)


if __name__ == "__main__":
    unittest.main()

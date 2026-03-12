# -*- coding: utf-8 -*-
"""Unit tests for _parse_continue_statement function."""

import unittest
from typing import Any, Dict

from ._parse_continue_statement_src import _parse_continue_statement


Token = Dict[str, Any]
AST = Dict[str, Any]
ParserState = Dict[str, Any]


def _make_token(token_type: str, value: str = "", line: int = 1, column: int = 1) -> Token:
    """Helper to create a token dict."""
    return {
        "type": token_type,
        "value": value,
        "line": line,
        "column": column
    }


def _make_parser_state(tokens: list, pos: int = 0, filename: str = "test.py") -> ParserState:
    """Helper to create a parser state dict."""
    return {
        "tokens": tokens,
        "pos": pos,
        "filename": filename,
        "error": ""
    }


class TestParseContinueStatement(unittest.TestCase):
    """Test cases for _parse_continue_statement function."""

    def test_happy_path_single_continue(self):
        """Test parsing a single valid continue statement."""
        tokens = [
            _make_token("CONTINUE", "continue", line=5, column=10),
            _make_token("SEMICOLON", ";", line=5, column=18)
        ]
        parser_state = _make_parser_state(tokens, pos=0)
        
        result = _parse_continue_statement(parser_state)
        
        # Verify AST node structure
        self.assertEqual(result["type"], "CONTINUE_STMT")
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 10)
        self.assertEqual(result["children"], [])
        
        # Verify parser state was updated
        self.assertEqual(parser_state["pos"], 2)

    def test_happy_path_continue_with_other_tokens_after(self):
        """Test parsing continue when there are more tokens after."""
        tokens = [
            _make_token("CONTINUE", "continue", line=3, column=5),
            _make_token("SEMICOLON", ";", line=3, column=13),
            _make_token("RETURN", "return", line=4, column=1)
        ]
        parser_state = _make_parser_state(tokens, pos=0)
        
        result = _parse_continue_statement(parser_state)
        
        self.assertEqual(result["type"], "CONTINUE_STMT")
        self.assertEqual(result["line"], 3)
        self.assertEqual(result["column"], 5)
        self.assertEqual(parser_state["pos"], 2)

    def test_happy_path_continue_not_at_start(self):
        """Test parsing continue when pos is not at 0."""
        tokens = [
            _make_token("IF", "if", line=1, column=1),
            _make_token("LPAREN", "(", line=1, column=4),
            _make_token("CONTINUE", "continue", line=2, column=5),
            _make_token("SEMICOLON", ";", line=2, column=13)
        ]
        parser_state = _make_parser_state(tokens, pos=2)
        
        result = _parse_continue_statement(parser_state)
        
        self.assertEqual(result["type"], "CONTINUE_STMT")
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 5)
        self.assertEqual(parser_state["pos"], 4)

    def test_boundary_no_semicolon_end_of_tokens(self):
        """Test error when continue is at end with no semicolon."""
        tokens = [
            _make_token("CONTINUE", "continue", line=10, column=1)
        ]
        parser_state = _make_parser_state(tokens, pos=0)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_continue_statement(parser_state)
        
        self.assertEqual(str(context.exception), "Expected ';' after continue statement")
        # Verify pos was not updated (function should fail before updating)
        self.assertEqual(parser_state["pos"], 0)

    def test_boundary_wrong_token_after_continue(self):
        """Test error when token after continue is not semicolon."""
        tokens = [
            _make_token("CONTINUE", "continue", line=7, column=3),
            _make_token("IDENTIFIER", "x", line=7, column=11)
        ]
        parser_state = _make_parser_state(tokens, pos=0)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_continue_statement(parser_state)
        
        self.assertEqual(str(context.exception), "Expected ';' after continue statement")
        self.assertEqual(parser_state["pos"], 0)

    def test_boundary_multiple_semicolons(self):
        """Test parsing continue with multiple semicolons (only first consumed)."""
        tokens = [
            _make_token("CONTINUE", "continue", line=1, column=1),
            _make_token("SEMICOLON", ";", line=1, column=9),
            _make_token("SEMICOLON", ";", line=1, column=10)
        ]
        parser_state = _make_parser_state(tokens, pos=0)
        
        result = _parse_continue_statement(parser_state)
        
        self.assertEqual(result["type"], "CONTINUE_STMT")
        self.assertEqual(parser_state["pos"], 2)

    def test_edge_case_different_line_numbers(self):
        """Test with continue and semicolon on different lines."""
        tokens = [
            _make_token("CONTINUE", "continue", line=15, column=20),
            _make_token("SEMICOLON", ";", line=16, column=1)
        ]
        parser_state = _make_parser_state(tokens, pos=0)
        
        result = _parse_continue_statement(parser_state)
        
        # Line/column should come from CONTINUE token
        self.assertEqual(result["line"], 15)
        self.assertEqual(result["column"], 20)
        self.assertEqual(parser_state["pos"], 2)

    def test_edge_case_zero_column(self):
        """Test with zero-based column number."""
        tokens = [
            _make_token("CONTINUE", "continue", line=1, column=0),
            _make_token("SEMICOLON", ";", line=1, column=8)
        ]
        parser_state = _make_parser_state(tokens, pos=0)
        
        result = _parse_continue_statement(parser_state)
        
        self.assertEqual(result["column"], 0)
        self.assertEqual(parser_state["pos"], 2)

    def test_state_preservation_other_fields(self):
        """Test that other parser_state fields are preserved."""
        tokens = [
            _make_token("CONTINUE", "continue", line=1, column=1),
            _make_token("SEMICOLON", ";", line=1, column=9)
        ]
        parser_state = _make_parser_state(tokens, pos=0, filename="my_test.py")
        parser_state["error"] = "previous error"
        
        result = _parse_continue_statement(parser_state)
        
        # Other fields should be preserved
        self.assertEqual(parser_state["filename"], "my_test.py")
        self.assertEqual(parser_state["error"], "previous error")
        self.assertEqual(parser_state["tokens"], tokens)


if __name__ == "__main__":
    unittest.main()

# -*- coding: utf-8 -*-
"""Unit tests for _parse_for_stmt function."""

import unittest
from unittest.mock import patch
from typing import Any, Dict

from ._parse_for_stmt_src import _parse_for_stmt


def _make_token(token_type: str, value: str = "", line: int = 1, column: int = 1) -> Dict[str, Any]:
    """Helper to create a token dict."""
    return {
        "type": token_type,
        "value": value,
        "line": line,
        "column": column
    }


def _make_parser_state(tokens: list, pos: int = 0, filename: str = "test.py") -> Dict[str, Any]:
    """Helper to create a parser state dict."""
    return {
        "tokens": tokens,
        "pos": pos,
        "filename": filename
    }


class TestParseForStmt(unittest.TestCase):
    """Test cases for _parse_for_stmt function."""

    def test_happy_path_simple_for_loop(self):
        """Test parsing a simple for loop: for i in expr block"""
        tokens = [
            _make_token("FOR", "for", line=1, column=1),
            _make_token("IDENTIFIER", "i", line=1, column=5),
            _make_token("IN", "in", line=1, column=7),
            _make_token("IDENTIFIER", "range", line=1, column=10),
            _make_token("LPAREN", "(", line=1, column=15),
            _make_token("NUMBER", "10", line=1, column=16),
            _make_token("RPAREN", ")", line=1, column=18),
        ]
        parser_state = _make_parser_state(tokens)
        
        mock_expr_node = {
            "type": "CALL_EXPR",
            "children": [],
            "line": 1,
            "column": 10
        }
        mock_block_node = {
            "type": "BLOCK",
            "children": [],
            "line": 1,
            "column": 19
        }
        
        with patch("._parse_for_stmt_src._parse_expression", return_value=mock_expr_node) as mock_parse_expr:
            with patch("._parse_for_stmt_src._parse_block", return_value=mock_block_node) as mock_parse_block:
                result = _parse_for_stmt(parser_state)
        
        self.assertEqual(result["type"], "FOR_STMT")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(len(result["children"]), 3)
        
        # Check iteration variable
        iter_var = result["children"][0]
        self.assertEqual(iter_var["type"], "IDENTIFIER")
        self.assertEqual(iter_var["value"], "i")
        self.assertEqual(iter_var["line"], 1)
        self.assertEqual(iter_var["column"], 5)
        
        # Check range expression
        self.assertEqual(result["children"][1], mock_expr_node)
        
        # Check body
        self.assertEqual(result["children"][2], mock_block_node)
        
        # Verify pos was updated
        self.assertEqual(parser_state["pos"], 7)
        
        # Verify mocks were called
        mock_parse_expr.assert_called_once()
        mock_parse_block.assert_called_once()

    def test_happy_path_for_with_multiline(self):
        """Test parsing for loop spanning multiple lines."""
        tokens = [
            _make_token("FOR", "for", line=2, column=5),
            _make_token("IDENTIFIER", "item", line=2, column=9),
            _make_token("IN", "in", line=2, column=14),
            _make_token("IDENTIFIER", "items", line=2, column=17),
        ]
        parser_state = _make_parser_state(tokens)
        
        mock_expr_node = {"type": "IDENTIFIER", "value": "items", "line": 2, "column": 17}
        mock_block_node = {"type": "BLOCK", "children": [], "line": 3, "column": 5}
        
        with patch("._parse_for_stmt_src._parse_expression", return_value=mock_expr_node):
            with patch("._parse_for_stmt_src._parse_block", return_value=mock_block_node):
                result = _parse_for_stmt(parser_state)
        
        self.assertEqual(result["type"], "FOR_STMT")
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 5)
        self.assertEqual(result["children"][0]["value"], "item")

    def test_error_empty_tokens(self):
        """Test error when tokens list is empty."""
        parser_state = _make_parser_state([])
        
        with self.assertRaises(SyntaxError) as context:
            _parse_for_stmt(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))

    def test_error_pos_at_end(self):
        """Test error when pos is already at end of tokens."""
        tokens = [_make_token("FOR", "for", line=1, column=1)]
        parser_state = _make_parser_state(tokens, pos=1)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_for_stmt(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))

    def test_error_missing_identifier(self):
        """Test error when identifier is missing after FOR."""
        tokens = [
            _make_token("FOR", "for", line=1, column=1),
            _make_token("IN", "in", line=1, column=5),
        ]
        parser_state = _make_parser_state(tokens)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_for_stmt(parser_state)
        
        self.assertIn("Expected identifier", str(context.exception))
        self.assertIn("got IN", str(context.exception))

    def test_error_wrong_token_after_for(self):
        """Test error when wrong token type appears after FOR."""
        tokens = [
            _make_token("FOR", "for", line=1, column=1),
            _make_token("NUMBER", "123", line=1, column=5),
        ]
        parser_state = _make_parser_state(tokens)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_for_stmt(parser_state)
        
        self.assertIn("Expected identifier", str(context.exception))
        self.assertIn("got NUMBER", str(context.exception))

    def test_error_missing_in_keyword(self):
        """Test error when IN keyword is missing."""
        tokens = [
            _make_token("FOR", "for", line=1, column=1),
            _make_token("IDENTIFIER", "i", line=1, column=5),
            _make_token("NUMBER", "10", line=1, column=7),
        ]
        parser_state = _make_parser_state(tokens)
        
        with patch("._parse_for_stmt_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.side_effect = SyntaxError("Expected IN")
            with self.assertRaises(SyntaxError):
                _parse_for_stmt(parser_state)

    def test_error_parse_expression_raises(self):
        """Test that SyntaxError from _parse_expression is propagated."""
        tokens = [
            _make_token("FOR", "for", line=1, column=1),
            _make_token("IDENTIFIER", "i", line=1, column=5),
            _make_token("IN", "in", line=1, column=7),
        ]
        parser_state = _make_parser_state(tokens)
        
        with patch("._parse_for_stmt_src._parse_expression", side_effect=SyntaxError("Invalid expression")):
            with self.assertRaises(SyntaxError) as context:
                _parse_for_stmt(parser_state)
        
        self.assertEqual(str(context.exception), "Invalid expression")

    def test_error_parse_block_raises(self):
        """Test that SyntaxError from _parse_block is propagated."""
        tokens = [
            _make_token("FOR", "for", line=1, column=1),
            _make_token("IDENTIFIER", "i", line=1, column=5),
            _make_token("IN", "in", line=1, column=7),
        ]
        parser_state = _make_parser_state(tokens)
        
        mock_expr_node = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 9}
        
        with patch("._parse_for_stmt_src._parse_expression", return_value=mock_expr_node):
            with patch("._parse_for_stmt_src._parse_block", side_effect=SyntaxError("Invalid block")):
                with self.assertRaises(SyntaxError) as context:
                    _parse_for_stmt(parser_state)
        
        self.assertEqual(str(context.exception), "Invalid block")

    def test_pos_updated_correctly(self):
        """Test that parser_state pos is updated to correct position."""
        tokens = [
            _make_token("FOR", "for", line=1, column=1),
            _make_token("IDENTIFIER", "i", line=1, column=5),
            _make_token("IN", "in", line=1, column=7),
            _make_token("IDENTIFIER", "x", line=1, column=10),
        ]
        parser_state = _make_parser_state(tokens)
        
        mock_expr_node = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 10}
        mock_block_node = {"type": "BLOCK", "children": [], "line": 1, "column": 12}
        
        with patch("._parse_for_stmt_src._parse_expression", return_value=mock_expr_node):
            with patch("._parse_for_stmt_src._parse_block", return_value=mock_block_node):
                _parse_for_stmt(parser_state)
        
        # FOR consumed (pos=1), IDENTIFIER consumed (pos=2), IN consumed (pos=3),
        # _parse_expression consumes expr token (pos=4), _parse_block consumes remaining
        self.assertEqual(parser_state["pos"], 4)

    def test_for_keyword_at_different_position(self):
        """Test parsing for loop when FOR is not at position 0."""
        tokens = [
            _make_token("SEMICOLON", ";", line=1, column=1),
            _make_token("FOR", "for", line=1, column=3),
            _make_token("IDENTIFIER", "x", line=1, column=7),
            _make_token("IN", "in", line=1, column=9),
        ]
        parser_state = _make_parser_state(tokens, pos=1)
        
        mock_expr_node = {"type": "IDENTIFIER", "value": "y", "line": 1, "column": 12}
        mock_block_node = {"type": "BLOCK", "children": [], "line": 1, "column": 14}
        
        with patch("._parse_for_stmt_src._parse_expression", return_value=mock_expr_node):
            with patch("._parse_for_stmt_src._parse_block", return_value=mock_block_node):
                result = _parse_for_stmt(parser_state)
        
        self.assertEqual(result["type"], "FOR_STMT")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 3)
        self.assertEqual(parser_state["pos"], 4)

    def test_identifier_with_special_name(self):
        """Test for loop with various identifier names."""
        for ident_name in ["_", "x1", "_temp", "item"]:
            with self.subTest(identifier=ident_name):
                tokens = [
                    _make_token("FOR", "for", line=1, column=1),
                    _make_token("IDENTIFIER", ident_name, line=1, column=5),
                    _make_token("IN", "in", line=1, column=10),
                ]
                parser_state = _make_parser_state(tokens)
                
                mock_expr_node = {"type": "IDENTIFIER", "value": "seq", "line": 1, "column": 13}
                mock_block_node = {"type": "BLOCK", "children": [], "line": 1, "column": 17}
                
                with patch("._parse_for_stmt_src._parse_expression", return_value=mock_expr_node):
                    with patch("._parse_for_stmt_src._parse_block", return_value=mock_block_node):
                        result = _parse_for_stmt(parser_state)
                
                self.assertEqual(result["children"][0]["value"], ident_name)


if __name__ == "__main__":
    unittest.main()

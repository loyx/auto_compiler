# -*- coding: utf-8 -*-
"""Unit tests for _parse_expression function."""

import unittest
from unittest.mock import patch
from typing import Any, Dict

from ._parse_expression_package._parse_expression_src import _parse_expression


Token = Dict[str, Any]
AST = Dict[str, Any]
ParserState = Dict[str, Any]


class TestParseExpression(unittest.TestCase):
    """Test cases for _parse_expression function."""

    def test_single_term_expression(self):
        """Test parsing a single term (no operators)."""
        tokens: list[Token] = [
            {"type": "NUMBER", "value": "42", "line": 1, "column": 1}
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        mock_term_ast: AST = {
            "type": "NUMBER",
            "value": "42",
            "line": 1,
            "column": 1
        }
        
        with patch("._parse_expression_package._parse_expression_src._parse_term", return_value=mock_term_ast) as mock_parse_term:
            result = _parse_expression(parser_state)
        
        self.assertEqual(result["type"], "NUMBER")
        self.assertEqual(result["value"], "42")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 1)
        mock_parse_term.assert_called_once()

    def test_expression_with_plus_operator(self):
        """Test parsing expression with PLUS operator."""
        tokens: list[Token] = [
            {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
            {"type": "PLUS", "value": "+", "line": 1, "column": 3},
            {"type": "NUMBER", "value": "2", "line": 1, "column": 5}
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        term1_ast: AST = {"type": "NUMBER", "value": "1", "line": 1, "column": 1}
        term2_ast: AST = {"type": "NUMBER", "value": "2", "line": 1, "column": 5}
        
        with patch("._parse_expression_package._parse_expression_src._parse_term", side_effect=[term1_ast, term2_ast]) as mock_parse_term:
            result = _parse_expression(parser_state)
        
        self.assertEqual(result["type"], "BINOP")
        self.assertEqual(result["operator"], "+")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 3)
        self.assertEqual(len(result["children"]), 2)
        self.assertEqual(result["children"][0]["value"], "1")
        self.assertEqual(result["children"][1]["value"], "2")
        self.assertEqual(parser_state["pos"], 3)
        self.assertEqual(mock_parse_term.call_count, 2)

    def test_expression_with_minus_operator(self):
        """Test parsing expression with MINUS operator."""
        tokens: list[Token] = [
            {"type": "NUMBER", "value": "10", "line": 2, "column": 1},
            {"type": "MINUS", "value": "-", "line": 2, "column": 4},
            {"type": "NUMBER", "value": "5", "line": 2, "column": 6}
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        term1_ast: AST = {"type": "NUMBER", "value": "10", "line": 2, "column": 1}
        term2_ast: AST = {"type": "NUMBER", "value": "5", "line": 2, "column": 6}
        
        with patch("._parse_expression_package._parse_expression_src._parse_term", side_effect=[term1_ast, term2_ast]) as mock_parse_term:
            result = _parse_expression(parser_state)
        
        self.assertEqual(result["type"], "BINOP")
        self.assertEqual(result["operator"], "-")
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 4)
        self.assertEqual(parser_state["pos"], 3)
        self.assertEqual(mock_parse_term.call_count, 2)

    def test_multiple_operators_left_associative(self):
        """Test parsing expression with multiple operators (left-associative)."""
        tokens: list[Token] = [
            {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
            {"type": "PLUS", "value": "+", "line": 1, "column": 3},
            {"type": "NUMBER", "value": "2", "line": 1, "column": 5},
            {"type": "MINUS", "value": "-", "line": 1, "column": 7},
            {"type": "NUMBER", "value": "3", "line": 1, "column": 9}
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        term1_ast: AST = {"type": "NUMBER", "value": "1", "line": 1, "column": 1}
        term2_ast: AST = {"type": "NUMBER", "value": "2", "line": 1, "column": 5}
        term3_ast: AST = {"type": "NUMBER", "value": "3", "line": 1, "column": 9}
        
        with patch("._parse_expression_package._parse_expression_src._parse_term", side_effect=[term1_ast, term2_ast, term3_ast]) as mock_parse_term:
            result = _parse_expression(parser_state)
        
        # Should be left-associative: (1 + 2) - 3
        self.assertEqual(result["type"], "BINOP")
        self.assertEqual(result["operator"], "-")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 7)
        
        left_child = result["children"][0]
        self.assertEqual(left_child["type"], "BINOP")
        self.assertEqual(left_child["operator"], "+")
        self.assertEqual(left_child["children"][0]["value"], "1")
        self.assertEqual(left_child["children"][1]["value"], "2")
        
        self.assertEqual(result["children"][1]["value"], "3")
        self.assertEqual(parser_state["pos"], 5)
        self.assertEqual(mock_parse_term.call_count, 3)

    def test_empty_tokens_raises_syntax_error(self):
        """Test that empty tokens list raises SyntaxError."""
        parser_state: ParserState = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_expression(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))
        self.assertIn("test.py", str(context.exception))

    def test_pos_at_end_raises_syntax_error(self):
        """Test that pos at end of tokens raises SyntaxError."""
        tokens: list[Token] = [
            {"type": "NUMBER", "value": "42", "line": 1, "column": 1}
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 1,  # Already at end
            "filename": "test.py",
            "error": ""
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_expression(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))

    def test_unknown_filename_in_error(self):
        """Test error message with unknown filename."""
        parser_state: ParserState = {
            "tokens": [],
            "pos": 0,
            "filename": "",
            "error": ""
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_expression(parser_state)
        
        self.assertIn("<unknown>", str(context.exception))

    def test_stops_at_non_plus_minus_token(self):
        """Test that parsing stops when encountering non-PLUS/MINUS token."""
        tokens: list[Token] = [
            {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
            {"type": "PLUS", "value": "+", "line": 1, "column": 3},
            {"type": "NUMBER", "value": "2", "line": 1, "column": 5},
            {"type": "SEMICOLON", "value": ";", "line": 1, "column": 7},
            {"type": "NUMBER", "value": "3", "line": 1, "column": 9}
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        term1_ast: AST = {"type": "NUMBER", "value": "1", "line": 1, "column": 1}
        term2_ast: AST = {"type": "NUMBER", "value": "2", "line": 1, "column": 5}
        
        with patch("._parse_expression_package._parse_expression_src._parse_term", side_effect=[term1_ast, term2_ast]) as mock_parse_term:
            result = _parse_expression(parser_state)
        
        # Should only parse "1 + 2", stop at SEMICOLON
        self.assertEqual(result["type"], "BINOP")
        self.assertEqual(result["operator"], "+")
        self.assertEqual(parser_state["pos"], 3)  # Stopped before SEMICOLON
        self.assertEqual(mock_parse_term.call_count, 2)

    def test_preserves_line_column_from_operator(self):
        """Test that BINOP node preserves line/column from operator token."""
        tokens: list[Token] = [
            {"type": "NUMBER", "value": "1", "line": 5, "column": 10},
            {"type": "PLUS", "value": "+", "line": 6, "column": 2},
            {"type": "NUMBER", "value": "2", "line": 6, "column": 4}
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        term1_ast: AST = {"type": "NUMBER", "value": "1", "line": 5, "column": 10}
        term2_ast: AST = {"type": "NUMBER", "value": "2", "line": 6, "column": 4}
        
        with patch("._parse_expression_package._parse_expression_src._parse_term", side_effect=[term1_ast, term2_ast]) as mock_parse_term:
            result = _parse_expression(parser_state)
        
        # BINOP should use operator's line/column
        self.assertEqual(result["line"], 6)
        self.assertEqual(result["column"], 2)

    def test_mixed_plus_minus_operators(self):
        """Test parsing expression with mixed PLUS and MINUS operators."""
        tokens: list[Token] = [
            {"type": "NUMBER", "value": "10", "line": 1, "column": 1},
            {"type": "MINUS", "value": "-", "line": 1, "column": 4},
            {"type": "NUMBER", "value": "3", "line": 1, "column": 6},
            {"type": "PLUS", "value": "+", "line": 1, "column": 8},
            {"type": "NUMBER", "value": "5", "line": 1, "column": 10}
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        term1_ast: AST = {"type": "NUMBER", "value": "10", "line": 1, "column": 1}
        term2_ast: AST = {"type": "NUMBER", "value": "3", "line": 1, "column": 6}
        term3_ast: AST = {"type": "NUMBER", "value": "5", "line": 1, "column": 10}
        
        with patch("._parse_expression_package._parse_expression_src._parse_term", side_effect=[term1_ast, term2_ast, term3_ast]) as mock_parse_term:
            result = _parse_expression(parser_state)
        
        # Should be: (10 - 3) + 5
        self.assertEqual(result["type"], "BINOP")
        self.assertEqual(result["operator"], "+")
        
        left_child = result["children"][0]
        self.assertEqual(left_child["type"], "BINOP")
        self.assertEqual(left_child["operator"], "-")
        self.assertEqual(left_child["children"][0]["value"], "10")
        self.assertEqual(left_child["children"][1]["value"], "3")
        
        self.assertEqual(result["children"][1]["value"], "5")
        self.assertEqual(mock_parse_term.call_count, 3)


if __name__ == "__main__":
    unittest.main()

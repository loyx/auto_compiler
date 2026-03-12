#!/usr/bin/env python3
"""Unit tests for _parse_array_literal function."""

import unittest
from unittest.mock import patch
from typing import Any, Dict

# Relative import for the function under test
from ._parse_array_literal_src import _parse_array_literal

Token = Dict[str, Any]
AST = Dict[str, Any]
ParserState = Dict[str, Any]


class TestParseArrayLiteral(unittest.TestCase):
    """Test cases for _parse_array_literal function."""

    def test_empty_array(self):
        """Test parsing an empty array []."""
        tokens: list[Token] = [
            {"type": "LEFT_BRACKET", "value": "[", "line": 1, "column": 1},
            {"type": "RIGHT_BRACKET", "value": "]", "line": 1, "column": 2},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 1,  # Points to RIGHT_BRACKET (after LEFT_BRACKET)
            "filename": "test.src",
            "error": ""
        }
        
        result = _parse_array_literal(parser_state, start_line=1, start_column=1)
        
        self.assertEqual(result["type"], "ARRAY_LITERAL")
        self.assertEqual(result["elements"], [])
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 2)  # Consumed RIGHT_BRACKET

    def test_single_element_array(self):
        """Test parsing an array with one element [1]."""
        tokens: list[Token] = [
            {"type": "LEFT_BRACKET", "value": "[", "line": 1, "column": 1},
            {"type": "NUMBER", "value": "1", "line": 1, "column": 2},
            {"type": "RIGHT_BRACKET", "value": "]", "line": 1, "column": 3},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 1,  # Points to NUMBER (after LEFT_BRACKET)
            "filename": "test.src",
            "error": ""
        }
        
        mock_element: AST = {
            "type": "NUMBER",
            "value": "1",
            "line": 1,
            "column": 2
        }
        
        with patch("._parse_array_literal_src._parse_unary") as mock_parse_unary:
            mock_parse_unary.return_value = mock_element
            result = _parse_array_literal(parser_state, start_line=1, start_column=1)
            
            mock_parse_unary.assert_called_once()
            self.assertEqual(result["type"], "ARRAY_LITERAL")
            self.assertEqual(len(result["elements"]), 1)
            self.assertEqual(result["elements"][0]["type"], "NUMBER")
            self.assertEqual(result["elements"][0]["value"], "1")
            self.assertEqual(parser_state["pos"], 3)  # Consumed NUMBER and RIGHT_BRACKET

    def test_multiple_elements_array(self):
        """Test parsing an array with multiple elements [1, 2, 3]."""
        tokens: list[Token] = [
            {"type": "LEFT_BRACKET", "value": "[", "line": 1, "column": 1},
            {"type": "NUMBER", "value": "1", "line": 1, "column": 2},
            {"type": "COMMA", "value": ",", "line": 1, "column": 3},
            {"type": "NUMBER", "value": "2", "line": 1, "column": 4},
            {"type": "COMMA", "value": ",", "line": 1, "column": 5},
            {"type": "NUMBER", "value": "3", "line": 1, "column": 6},
            {"type": "RIGHT_BRACKET", "value": "]", "line": 1, "column": 7},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 1,  # Points to first NUMBER
            "filename": "test.src",
            "error": ""
        }
        
        mock_elements: list[AST] = [
            {"type": "NUMBER", "value": "1", "line": 1, "column": 2},
            {"type": "NUMBER", "value": "2", "line": 1, "column": 4},
            {"type": "NUMBER", "value": "3", "line": 1, "column": 6},
        ]
        
        with patch("._parse_array_literal_src._parse_unary") as mock_parse_unary:
            mock_parse_unary.side_effect = mock_elements
            result = _parse_array_literal(parser_state, start_line=1, start_column=1)
            
            self.assertEqual(mock_parse_unary.call_count, 3)
            self.assertEqual(result["type"], "ARRAY_LITERAL")
            self.assertEqual(len(result["elements"]), 3)
            self.assertEqual(result["elements"][0]["value"], "1")
            self.assertEqual(result["elements"][1]["value"], "2")
            self.assertEqual(result["elements"][2]["value"], "3")
            self.assertEqual(parser_state["pos"], 7)  # After RIGHT_BRACKET

    def test_element_parse_failure(self):
        """Test when _parse_unary returns an ERROR node."""
        tokens: list[Token] = [
            {"type": "LEFT_BRACKET", "value": "[", "line": 1, "column": 1},
            {"type": "INVALID", "value": "xyz", "line": 1, "column": 2},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 1,
            "filename": "test.src",
            "error": "Invalid token"
        }
        
        mock_error_element: AST = {
            "type": "ERROR",
            "value": "Invalid token",
            "line": 1,
            "column": 2
        }
        
        with patch("._parse_array_literal_src._parse_unary") as mock_parse_unary:
            mock_parse_unary.return_value = mock_error_element
            result = _parse_array_literal(parser_state, start_line=1, start_column=1)
            
            mock_parse_unary.assert_called_once()
            self.assertEqual(result["type"], "ERROR")
            self.assertEqual(result["value"], "Invalid token")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)

    def test_unexpected_end_of_input_after_element(self):
        """Test when input ends after an element without closing bracket."""
        tokens: list[Token] = [
            {"type": "LEFT_BRACKET", "value": "[", "line": 1, "column": 1},
            {"type": "NUMBER", "value": "1", "line": 1, "column": 2},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 1,
            "filename": "test.src",
            "error": ""
        }
        
        mock_element: AST = {
            "type": "NUMBER",
            "value": "1",
            "line": 1,
            "column": 2
        }
        
        with patch("._parse_array_literal_src._parse_unary") as mock_parse_unary:
            mock_parse_unary.return_value = mock_element
            result = _parse_array_literal(parser_state, start_line=1, start_column=1)
            
            self.assertEqual(result["type"], "ERROR")
            self.assertEqual(result["value"], "Unexpected end of input in array literal")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            self.assertIn("error", parser_state)
            self.assertEqual(parser_state["error"], "Unexpected end of input in array literal")

    def test_invalid_token_after_element(self):
        """Test when an invalid token (not COMMA or RIGHT_BRACKET) follows an element."""
        tokens: list[Token] = [
            {"type": "LEFT_BRACKET", "value": "[", "line": 1, "column": 1},
            {"type": "NUMBER", "value": "1", "line": 1, "column": 2},
            {"type": "SEMICOLON", "value": ";", "line": 1, "column": 3},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 1,
            "filename": "test.src",
            "error": ""
        }
        
        mock_element: AST = {
            "type": "NUMBER",
            "value": "1",
            "line": 1,
            "column": 2
        }
        
        with patch("._parse_array_literal_src._parse_unary") as mock_parse_unary:
            mock_parse_unary.return_value = mock_element
            result = _parse_array_literal(parser_state, start_line=1, start_column=1)
            
            self.assertEqual(result["type"], "ERROR")
            self.assertEqual(result["value"], "Expected COMMA or RIGHT_BRACKET, got SEMICOLON")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            self.assertEqual(parser_state["error"], "Expected COMMA or RIGHT_BRACKET, got SEMICOLON")

    def test_empty_tokens_list(self):
        """Test when tokens list is empty (edge case)."""
        tokens: list[Token] = []
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.src",
            "error": ""
        }
        
        result = _parse_array_literal(parser_state, start_line=1, start_column=1)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], "Unexpected end of input in array literal")

    def test_pos_beyond_tokens_length(self):
        """Test when pos is already beyond the tokens list length."""
        tokens: list[Token] = [
            {"type": "LEFT_BRACKET", "value": "[", "line": 1, "column": 1},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 5,  # Beyond list length
            "filename": "test.src",
            "error": ""
        }
        
        result = _parse_array_literal(parser_state, start_line=1, start_column=1)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], "Unexpected end of input in array literal")


if __name__ == "__main__":
    unittest.main()

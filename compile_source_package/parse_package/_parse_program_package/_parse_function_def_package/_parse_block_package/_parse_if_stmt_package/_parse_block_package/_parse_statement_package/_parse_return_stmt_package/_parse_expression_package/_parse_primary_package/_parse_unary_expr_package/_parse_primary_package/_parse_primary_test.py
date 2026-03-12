"""Unit tests for _parse_primary function."""
import unittest
from typing import Any, Dict

from ._parse_primary_src import _parse_primary


def make_token(token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
    """Helper to create a token dictionary."""
    return {
        "type": token_type,
        "value": value,
        "line": line,
        "column": column
    }


def make_parser_state(tokens: list, pos: int = 0, filename: str = "test.py") -> Dict[str, Any]:
    """Helper to create a parser state dictionary."""
    return {
        "tokens": tokens,
        "pos": pos,
        "filename": filename,
        "error": ""
    }


class TestParsePrimary(unittest.TestCase):
    """Test cases for _parse_primary function."""

    def test_parse_integer_literal(self):
        """Test parsing INTEGER token returns LITERAL AST."""
        tokens = [make_token("INTEGER", "42", line=1, column=5)]
        parser_state = make_parser_state(tokens, pos=0)
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "42")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 5)
        self.assertEqual(result["children"], [])
        self.assertEqual(parser_state["pos"], 1)
        self.assertEqual(parser_state["error"], "")

    def test_parse_float_literal(self):
        """Test parsing FLOAT token returns LITERAL AST."""
        tokens = [make_token("FLOAT", "3.14", line=2, column=10)]
        parser_state = make_parser_state(tokens, pos=0)
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "3.14")
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 10)
        self.assertEqual(result["children"], [])
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_string_literal(self):
        """Test parsing STRING token returns LITERAL AST."""
        tokens = [make_token("STRING", '"hello"', line=3, column=1)]
        parser_state = make_parser_state(tokens, pos=0)
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], '"hello"')
        self.assertEqual(result["line"], 3)
        self.assertEqual(result["column"], 1)
        self.assertEqual(result["children"], [])
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_identifier_standalone(self):
        """Test parsing IDENTIFIER not followed by LPAREN returns IDENTIFIER AST."""
        tokens = [
            make_token("IDENTIFIER", "x", line=1, column=1),
            make_token("PLUS", "+", line=1, column=2)
        ]
        parser_state = make_parser_state(tokens, pos=0)
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "x")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(result["children"], [])
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_identifier_as_function_call(self):
        """Test parsing IDENTIFIER followed by LPAREN returns CALL AST."""
        tokens = [
            make_token("IDENTIFIER", "func", line=1, column=1),
            make_token("LPAREN", "(", line=1, column=5)
        ]
        parser_state = make_parser_state(tokens, pos=0)
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "CALL")
        self.assertEqual(result["value"], "func")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(result["children"], [])
        self.assertEqual(parser_state["pos"], 2)

    def test_parse_parenthesized_expression(self):
        """Test parsing LPAREN returns PAREN AST."""
        tokens = [make_token("LPAREN", "(", line=1, column=1)]
        parser_state = make_parser_state(tokens, pos=0)
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "PAREN")
        self.assertEqual(result["value"], None)
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(result["children"], [])
        self.assertEqual(parser_state["pos"], 1)

    def test_empty_tokens_list(self):
        """Test parsing with empty tokens list returns ERROR AST."""
        tokens = []
        parser_state = make_parser_state(tokens, pos=0)
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], None)
        self.assertEqual(result["line"], 0)
        self.assertEqual(result["column"], 0)
        self.assertEqual(result["children"], [])
        self.assertEqual(parser_state["pos"], 0)
        self.assertEqual(parser_state["error"], "Unexpected end of input")

    def test_pos_at_end_of_tokens(self):
        """Test parsing when pos is at end of tokens returns ERROR AST."""
        tokens = [make_token("INTEGER", "1", line=1, column=1)]
        parser_state = make_parser_state(tokens, pos=1)
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], None)
        self.assertEqual(result["line"], 0)
        self.assertEqual(result["column"], 0)
        self.assertEqual(result["children"], [])
        self.assertEqual(parser_state["pos"], 1)
        self.assertEqual(parser_state["error"], "Unexpected end of input")

    def test_unknown_token_type(self):
        """Test parsing unknown token type returns ERROR AST."""
        tokens = [make_token("UNKNOWN", "?", line=5, column=3)]
        parser_state = make_parser_state(tokens, pos=0)
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], None)
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 3)
        self.assertEqual(result["children"], [])
        self.assertEqual(parser_state["pos"], 0)
        self.assertEqual(parser_state["error"], "Unexpected token: UNKNOWN")

    def test_identifier_at_end_is_not_call(self):
        """Test IDENTIFIER at end of tokens (no following LPAREN) returns IDENTIFIER AST."""
        tokens = [make_token("IDENTIFIER", "last", line=1, column=1)]
        parser_state = make_parser_state(tokens, pos=0)
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "last")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(result["children"], [])
        self.assertEqual(parser_state["pos"], 1)

    def test_multiple_calls_consume_correct_pos(self):
        """Test that multiple sequential calls to _parse_primary consume tokens correctly."""
        tokens = [
            make_token("INTEGER", "1", line=1, column=1),
            make_token("IDENTIFIER", "x", line=1, column=3),
            make_token("STRING", '"test"', line=1, column=5)
        ]
        parser_state = make_parser_state(tokens, pos=0)
        
        result1 = _parse_primary(parser_state)
        self.assertEqual(result1["type"], "LITERAL")
        self.assertEqual(result1["value"], "1")
        self.assertEqual(parser_state["pos"], 1)
        
        result2 = _parse_primary(parser_state)
        self.assertEqual(result2["type"], "IDENTIFIER")
        self.assertEqual(result2["value"], "x")
        self.assertEqual(parser_state["pos"], 2)
        
        result3 = _parse_primary(parser_state)
        self.assertEqual(result3["type"], "LITERAL")
        self.assertEqual(result3["value"], '"test"')
        self.assertEqual(parser_state["pos"], 3)


if __name__ == "__main__":
    unittest.main()

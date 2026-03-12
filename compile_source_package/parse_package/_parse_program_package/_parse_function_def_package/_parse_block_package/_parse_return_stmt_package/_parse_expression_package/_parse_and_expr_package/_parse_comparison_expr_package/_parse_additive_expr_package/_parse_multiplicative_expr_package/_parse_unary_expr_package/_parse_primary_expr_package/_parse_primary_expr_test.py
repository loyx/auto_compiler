#!/usr/bin/env python3
"""
Unit tests for _parse_primary_expr function.
Tests parsing of primary expressions (identifiers, literals, parenthesized expressions).
"""

import unittest

from ._parse_primary_expr_src import _parse_primary_expr


class TestParsePrimaryExpr(unittest.TestCase):
    """Test cases for _parse_primary_expr function."""

    def test_parse_identifier(self):
        """Test parsing an IDENTIFIER token."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "myVar", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "myVar")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 5)
        self.assertEqual(result["children"], [])
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_number_literal(self):
        """Test parsing a NUMBER token."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "42", "line": 2, "column": 10}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "42")
        self.assertEqual(result["literal_type"], "NUMBER")
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 10)
        self.assertEqual(result["children"], [])
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_string_literal(self):
        """Test parsing a STRING token."""
        parser_state = {
            "tokens": [
                {"type": "STRING", "value": "hello world", "line": 3, "column": 1}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "hello world")
        self.assertEqual(result["literal_type"], "STRING")
        self.assertEqual(result["line"], 3)
        self.assertEqual(result["column"], 1)
        self.assertEqual(result["children"], [])
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_boolean_literal_true(self):
        """Test parsing a BOOLEAN token with value true."""
        parser_state = {
            "tokens": [
                {"type": "BOOLEAN", "value": "true", "line": 4, "column": 8}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "true")
        self.assertEqual(result["literal_type"], "BOOLEAN")
        self.assertEqual(result["line"], 4)
        self.assertEqual(result["column"], 8)
        self.assertEqual(result["children"], [])
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_boolean_literal_false(self):
        """Test parsing a BOOLEAN token with value false."""
        parser_state = {
            "tokens": [
                {"type": "BOOLEAN", "value": "false", "line": 5, "column": 12}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "false")
        self.assertEqual(result["literal_type"], "BOOLEAN")
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 12)
        self.assertEqual(result["children"], [])
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_null_literal(self):
        """Test parsing a NULL token."""
        parser_state = {
            "tokens": [
                {"type": "NULL", "value": "null", "line": 6, "column": 3}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "null")
        self.assertEqual(result["literal_type"], "NULL")
        self.assertEqual(result["line"], 6)
        self.assertEqual(result["column"], 3)
        self.assertEqual(result["children"], [])
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_lparen_raises_syntax_error(self):
        """Test that LPAREN token raises SyntaxError for mutual recursion."""
        parser_state = {
            "tokens": [
                {"type": "LPAREN", "value": "(", "line": 7, "column": 15}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_primary_expr(parser_state)
        
        self.assertIn("Parenthesized expression requires expression parser", str(context.exception))
        self.assertEqual(parser_state["pos"], 1)

    def test_unexpected_end_of_input(self):
        """Test that empty token list raises SyntaxError."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.src"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_primary_expr(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))

    def test_position_at_end_of_tokens(self):
        """Test that pos >= len(tokens) raises SyntaxError."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 1,
            "filename": "test.src"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_primary_expr(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))

    def test_invalid_token_type_operator(self):
        """Test that operator token raises SyntaxError with details."""
        parser_state = {
            "tokens": [
                {"type": "PLUS", "value": "+", "line": 8, "column": 20}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_primary_expr(parser_state)
        
        error_msg = str(context.exception)
        self.assertIn("Unexpected token '+'", error_msg)
        self.assertIn("PLUS", error_msg)
        self.assertIn("line 8", error_msg)
        self.assertIn("column 20", error_msg)
        self.assertIn("Expected primary expression", error_msg)

    def test_invalid_token_type_keyword(self):
        """Test that keyword token raises SyntaxError."""
        parser_state = {
            "tokens": [
                {"type": "IF", "value": "if", "line": 9, "column": 1}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_primary_expr(parser_state)
        
        error_msg = str(context.exception)
        self.assertIn("Unexpected token 'if'", error_msg)
        self.assertIn("IF", error_msg)

    def test_position_advances_only_on_success_or_lparen(self):
        """Test that pos is updated correctly for valid tokens and LPAREN."""
        # Test IDENTIFIER
        state1 = {
            "tokens": [{"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test.src"
        }
        _parse_primary_expr(state1)
        self.assertEqual(state1["pos"], 1)
        
        # Test LPAREN (pos advances before raising error)
        state2 = {
            "tokens": [{"type": "LPAREN", "value": "(", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test.src"
        }
        with self.assertRaises(SyntaxError):
            _parse_primary_expr(state2)
        self.assertEqual(state2["pos"], 1)
        
        # Test invalid token (pos should NOT advance)
        state3 = {
            "tokens": [{"type": "PLUS", "value": "+", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test.src"
        }
        with self.assertRaises(SyntaxError):
            _parse_primary_expr(state3)
        self.assertEqual(state3["pos"], 0)

    def test_multiple_tokens_only_consumes_one(self):
        """Test that only the current token is consumed."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "first", "line": 1, "column": 1},
                {"type": "NUMBER", "value": "123", "line": 1, "column": 10},
                {"type": "STRING", "value": "text", "line": 1, "column": 15}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["value"], "first")
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_from_middle_position(self):
        """Test parsing from a non-zero position."""
        parser_state = {
            "tokens": [
                {"type": "PLUS", "value": "+", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "middle", "line": 1, "column": 5},
                {"type": "NUMBER", "value": "999", "line": 1, "column": 15}
            ],
            "pos": 1,
            "filename": "test.src"
        }
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["value"], "middle")
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(parser_state["pos"], 2)

    def test_float_number_literal(self):
        """Test parsing a floating point NUMBER token."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "3.14159", "line": 10, "column": 7}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "3.14159")
        self.assertEqual(result["literal_type"], "NUMBER")

    def test_negative_number_as_token(self):
        """Test parsing a negative number if tokenized as NUMBER."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "-42", "line": 11, "column": 3}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "-42")
        self.assertEqual(result["literal_type"], "NUMBER")

    def test_empty_string_literal(self):
        """Test parsing an empty string token."""
        parser_state = {
            "tokens": [
                {"type": "STRING", "value": "", "line": 12, "column": 10}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "")
        self.assertEqual(result["literal_type"], "STRING")

    def test_identifier_with_underscore(self):
        """Test parsing an identifier containing underscores."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "_private_var_123", "line": 13, "column": 5}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "_private_var_123")

    def test_error_message_contains_filename_context(self):
        """Test that error messages provide useful context."""
        parser_state = {
            "tokens": [
                {"type": "SEMICOLON", "value": ";", "line": 100, "column": 50}
            ],
            "pos": 0,
            "filename": "path/to/myfile.cc"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_primary_expr(parser_state)
        
        error_msg = str(context.exception)
        self.assertIn(";", error_msg)
        self.assertIn("SEMICOLON", error_msg)
        self.assertIn("line 100", error_msg)
        self.assertIn("column 50", error_msg)


if __name__ == "__main__":
    unittest.main()

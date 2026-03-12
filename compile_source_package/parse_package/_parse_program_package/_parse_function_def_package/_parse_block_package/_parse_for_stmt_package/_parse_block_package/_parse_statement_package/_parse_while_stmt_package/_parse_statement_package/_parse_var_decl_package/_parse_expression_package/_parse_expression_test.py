# -*- coding: utf-8 -*-
"""Unit tests for _parse_expression function."""

import unittest

from ._parse_expression_src import _parse_expression, _parse_primary, ParserState, Token


def _make_token(token_type: str, value: str, line: int = 1, column: int = 1) -> Token:
    """Helper to create a token dictionary."""
    return {
        "type": token_type,
        "value": value,
        "line": line,
        "column": column
    }


def _make_parser_state(tokens: list, pos: int = 0, filename: str = "<test>") -> ParserState:
    """Helper to create a parser state dictionary."""
    return {
        "tokens": tokens,
        "pos": pos,
        "filename": filename
    }


class TestParseExpressionLiterals(unittest.TestCase):
    """Test cases for parsing literal expressions."""

    def test_parse_number_literal(self):
        """Test parsing a simple number literal."""
        tokens = [_make_token("NUMBER", "42")]
        state = _make_parser_state(tokens)
        
        result = _parse_expression(state)
        
        self.assertEqual(result["type"], "Literal")
        self.assertEqual(result["value"], "42")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(state["pos"], 1)

    def test_parse_string_literal(self):
        """Test parsing a simple string literal."""
        tokens = [_make_token("STRING", '"hello"')]
        state = _make_parser_state(tokens)
        
        result = _parse_expression(state)
        
        self.assertEqual(result["type"], "Literal")
        self.assertEqual(result["value"], '"hello"')
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(state["pos"], 1)

    def test_parse_number_with_decimal(self):
        """Test parsing a number with decimal point."""
        tokens = [_make_token("NUMBER", "3.14")]
        state = _make_parser_state(tokens)
        
        result = _parse_expression(state)
        
        self.assertEqual(result["type"], "Literal")
        self.assertEqual(result["value"], "3.14")


class TestParseExpressionIdentifiers(unittest.TestCase):
    """Test cases for parsing identifier expressions."""

    def test_parse_simple_identifier(self):
        """Test parsing a simple identifier."""
        tokens = [_make_token("IDENTIFIER", "x")]
        state = _make_parser_state(tokens)
        
        result = _parse_expression(state)
        
        self.assertEqual(result["type"], "Identifier")
        self.assertEqual(result["value"], "x")
        self.assertEqual(state["pos"], 1)

    def test_parse_long_identifier(self):
        """Test parsing a longer identifier name."""
        tokens = [_make_token("IDENTIFIER", "myVariable")]
        state = _make_parser_state(tokens)
        
        result = _parse_expression(state)
        
        self.assertEqual(result["type"], "Identifier")
        self.assertEqual(result["value"], "myVariable")


class TestParseExpressionBinaryOperators(unittest.TestCase):
    """Test cases for parsing binary operator expressions."""

    def test_parse_addition(self):
        """Test parsing addition expression."""
        tokens = [
            _make_token("NUMBER", "1"),
            _make_token("OPERATOR", "+"),
            _make_token("NUMBER", "2")
        ]
        state = _make_parser_state(tokens)
        
        result = _parse_expression(state)
        
        self.assertEqual(result["type"], "BinaryOp")
        self.assertEqual(result["operator"], "+")
        self.assertEqual(len(result["children"]), 2)
        self.assertEqual(result["children"][0]["type"], "Literal")
        self.assertEqual(result["children"][0]["value"], "1")
        self.assertEqual(result["children"][1]["type"], "Literal")
        self.assertEqual(result["children"][1]["value"], "2")
        self.assertEqual(state["pos"], 3)

    def test_parse_subtraction(self):
        """Test parsing subtraction expression."""
        tokens = [
            _make_token("IDENTIFIER", "a"),
            _make_token("OPERATOR", "-"),
            _make_token("IDENTIFIER", "b")
        ]
        state = _make_parser_state(tokens)
        
        result = _parse_expression(state)
        
        self.assertEqual(result["type"], "BinaryOp")
        self.assertEqual(result["operator"], "-")

    def test_parse_multiplication(self):
        """Test parsing multiplication expression."""
        tokens = [
            _make_token("NUMBER", "5"),
            _make_token("OPERATOR", "*"),
            _make_token("NUMBER", "3")
        ]
        state = _make_parser_state(tokens)
        
        result = _parse_expression(state)
        
        self.assertEqual(result["type"], "BinaryOp")
        self.assertEqual(result["operator"], "*")

    def test_parse_division(self):
        """Test parsing division expression."""
        tokens = [
            _make_token("NUMBER", "10"),
            _make_token("OPERATOR", "/"),
            _make_token("NUMBER", "2")
        ]
        state = _make_parser_state(tokens)
        
        result = _parse_expression(state)
        
        self.assertEqual(result["type"], "BinaryOp")
        self.assertEqual(result["operator"], "/")

    def test_parse_chained_operations_left_associative(self):
        """Test that chained operations are left-associative."""
        tokens = [
            _make_token("NUMBER", "1"),
            _make_token("OPERATOR", "+"),
            _make_token("NUMBER", "2"),
            _make_token("OPERATOR", "+"),
            _make_token("NUMBER", "3")
        ]
        state = _make_parser_state(tokens)
        
        result = _parse_expression(state)
        
        # Should be ((1 + 2) + 3), left-associative
        self.assertEqual(result["type"], "BinaryOp")
        self.assertEqual(result["operator"], "+")
        # Right child should be the literal "3"
        self.assertEqual(result["children"][1]["type"], "Literal")
        self.assertEqual(result["children"][1]["value"], "3")
        # Left child should be another BinaryOp (1 + 2)
        self.assertEqual(result["children"][0]["type"], "BinaryOp")
        self.assertEqual(result["children"][0]["operator"], "+")
        self.assertEqual(state["pos"], 5)

    def test_parse_mixed_operators(self):
        """Test parsing expression with mixed operators."""
        tokens = [
            _make_token("NUMBER", "1"),
            _make_token("OPERATOR", "+"),
            _make_token("NUMBER", "2"),
            _make_token("OPERATOR", "*"),
            _make_token("NUMBER", "3")
        ]
        state = _make_parser_state(tokens)
        
        result = _parse_expression(state)
        
        # Simple left-to-right parsing (no precedence handling in this implementation)
        self.assertEqual(result["type"], "BinaryOp")
        self.assertEqual(result["operator"], "*")
        self.assertEqual(state["pos"], 5)


class TestParseExpressionParentheses(unittest.TestCase):
    """Test cases for parsing parenthesized expressions."""

    def test_parse_parenthesized_number(self):
        """Test parsing a number in parentheses."""
        tokens = [
            _make_token("LPAREN", "("),
            _make_token("NUMBER", "42"),
            _make_token("RPAREN", ")")
        ]
        state = _make_parser_state(tokens)
        
        result = _parse_expression(state)
        
        self.assertEqual(result["type"], "Literal")
        self.assertEqual(result["value"], "42")
        self.assertEqual(state["pos"], 3)

    def test_parse_parenthesized_expression(self):
        """Test parsing a complex expression in parentheses."""
        tokens = [
            _make_token("LPAREN", "("),
            _make_token("NUMBER", "1"),
            _make_token("OPERATOR", "+"),
            _make_token("NUMBER", "2"),
            _make_token("RPAREN", ")")
        ]
        state = _make_parser_state(tokens)
        
        result = _parse_expression(state)
        
        self.assertEqual(result["type"], "BinaryOp")
        self.assertEqual(result["operator"], "+")
        self.assertEqual(state["pos"], 5)

    def test_parse_nested_parentheses(self):
        """Test parsing nested parentheses."""
        tokens = [
            _make_token("LPAREN", "("),
            _make_token("LPAREN", "("),
            _make_token("NUMBER", "1"),
            _make_token("RPAREN", ")"),
            _make_token("RPAREN", ")")
        ]
        state = _make_parser_state(tokens)
        
        result = _parse_expression(state)
        
        self.assertEqual(result["type"], "Literal")
        self.assertEqual(result["value"], "1")
        self.assertEqual(state["pos"], 5)

    def test_parse_parenthesized_with_operator(self):
        """Test parsing (1 + 2) * 3."""
        tokens = [
            _make_token("LPAREN", "("),
            _make_token("NUMBER", "1"),
            _make_token("OPERATOR", "+"),
            _make_token("NUMBER", "2"),
            _make_token("RPAREN", ")"),
            _make_token("OPERATOR", "*"),
            _make_token("NUMBER", "3")
        ]
        state = _make_parser_state(tokens)
        
        result = _parse_expression(state)
        
        self.assertEqual(result["type"], "BinaryOp")
        self.assertEqual(result["operator"], "*")
        self.assertEqual(state["pos"], 7)


class TestParseExpressionErrors(unittest.TestCase):
    """Test cases for error handling in expression parsing."""

    def test_empty_tokens_raises_syntax_error(self):
        """Test that empty token list raises SyntaxError."""
        state = _make_parser_state([])
        
        with self.assertRaises(SyntaxError) as context:
            _parse_expression(state)
        
        self.assertIn("Unexpected end of expression", str(context.exception))

    def test_position_beyond_tokens_raises_syntax_error(self):
        """Test that position beyond token list raises SyntaxError."""
        tokens = [_make_token("NUMBER", "1")]
        state = _make_parser_state(tokens, pos=1)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_expression(state)
        
        self.assertIn("Unexpected end of expression", str(context.exception))

    def test_unclosed_parenthesis_raises_syntax_error(self):
        """Test that unclosed parenthesis raises SyntaxError."""
        tokens = [
            _make_token("LPAREN", "("),
            _make_token("NUMBER", "42")
        ]
        state = _make_parser_state(tokens)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_expression(state)
        
        self.assertIn("Unclosed parenthesis", str(context.exception))

    def test_mismatched_parenthesis_raises_syntax_error(self):
        """Test that mismatched parenthesis raises SyntaxError."""
        tokens = [
            _make_token("LPAREN", "("),
            _make_token("NUMBER", "42"),
            _make_token("NUMBER", "1")
        ]
        state = _make_parser_state(tokens)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_expression(state)
        
        self.assertIn("Expected ')'", str(context.exception))

    def test_unknown_token_type_raises_syntax_error(self):
        """Test that unknown token type raises SyntaxError."""
        tokens = [_make_token("UNKNOWN", "???")]
        state = _make_parser_state(tokens)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_expression(state)
        
        self.assertIn("Unexpected token", str(context.exception))

    def test_error_includes_filename(self):
        """Test that error messages include the filename."""
        tokens = []
        state = _make_parser_state(tokens, filename="test.src")
        
        with self.assertRaises(SyntaxError) as context:
            _parse_expression(state)
        
        self.assertIn("test.src", str(context.exception))

    def test_error_includes_line_and_column(self):
        """Test that error messages include line and column."""
        tokens = [_make_token("UNKNOWN", "???", line=5, column=10)]
        state = _make_parser_state(tokens, filename="test.src")
        
        with self.assertRaises(SyntaxError) as context:
            _parse_expression(state)
        
        error_msg = str(context.exception)
        self.assertIn("5", error_msg)
        self.assertIn("10", error_msg)


class TestParseExpressionEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""

    def test_single_identifier_followed_by_other_tokens(self):
        """Test that parsing stops at non-expression tokens."""
        tokens = [
            _make_token("IDENTIFIER", "x"),
            _make_token("OPERATOR", ";"),
            _make_token("NUMBER", "1")
        ]
        state = _make_parser_state(tokens)
        
        result = _parse_expression(state)
        
        self.assertEqual(result["type"], "Identifier")
        self.assertEqual(result["value"], "x")
        self.assertEqual(state["pos"], 1)

    def test_operator_not_in_supported_list_stops_parsing(self):
        """Test that unsupported operators stop binary expression parsing."""
        tokens = [
            _make_token("NUMBER", "1"),
            _make_token("OPERATOR", "%"),
            _make_token("NUMBER", "2")
        ]
        state = _make_parser_state(tokens)
        
        result = _parse_expression(state)
        
        self.assertEqual(result["type"], "Literal")
        self.assertEqual(result["value"], "1")
        self.assertEqual(state["pos"], 1)

    def test_expression_with_custom_filename(self):
        """Test parsing with custom filename in parser state."""
        tokens = [_make_token("NUMBER", "123")]
        state = _make_parser_state(tokens, filename="my_source.c")
        
        result = _parse_expression(state)
        
        self.assertEqual(result["value"], "123")

    def test_expression_preserves_token_positions(self):
        """Test that AST nodes preserve token line/column information."""
        tokens = [_make_token("IDENTIFIER", "var", line=10, column=5)]
        state = _make_parser_state(tokens)
        
        result = _parse_expression(state)
        
        self.assertEqual(result["line"], 10)
        self.assertEqual(result["column"], 5)

    def test_binary_op_preserves_operator_token_position(self):
        """Test that BinaryOp nodes preserve operator token position."""
        tokens = [
            _make_token("NUMBER", "1", line=1, column=1),
            _make_token("OPERATOR", "+", line=1, column=3),
            _make_token("NUMBER", "2", line=1, column=5)
        ]
        state = _make_parser_state(tokens)
        
        result = _parse_expression(state)
        
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 3)


class TestParsePrimary(unittest.TestCase):
    """Test cases for the _parse_primary helper function."""

    def test_parse_primary_number(self):
        """Test _parse_primary with number token."""
        tokens = [_make_token("NUMBER", "42")]
        state = _make_parser_state(tokens)
        
        result = _parse_primary(state)
        
        self.assertEqual(result["type"], "Literal")
        self.assertEqual(result["value"], "42")
        self.assertEqual(state["pos"], 1)

    def test_parse_primary_string(self):
        """Test _parse_primary with string token."""
        tokens = [_make_token("STRING", '"test"')]
        state = _make_parser_state(tokens)
        
        result = _parse_primary(state)
        
        self.assertEqual(result["type"], "Literal")
        self.assertEqual(result["value"], '"test"')

    def test_parse_primary_identifier(self):
        """Test _parse_primary with identifier token."""
        tokens = [_make_token("IDENTIFIER", "foo")]
        state = _make_parser_state(tokens)
        
        result = _parse_primary(state)
        
        self.assertEqual(result["type"], "Identifier")
        self.assertEqual(result["value"], "foo")

    def test_parse_primary_parenthesized(self):
        """Test _parse_primary with parenthesized expression."""
        tokens = [
            _make_token("LPAREN", "("),
            _make_token("NUMBER", "5"),
            _make_token("RPAREN", ")")
        ]
        state = _make_parser_state(tokens)
        
        result = _parse_primary(state)
        
        self.assertEqual(result["type"], "Literal")
        self.assertEqual(result["value"], "5")
        self.assertEqual(state["pos"], 3)

    def test_parse_primary_empty_raises(self):
        """Test _parse_primary with empty tokens raises SyntaxError."""
        state = _make_parser_state([])
        
        with self.assertRaises(SyntaxError):
            _parse_primary(state)

    def test_parse_primary_unknown_raises(self):
        """Test _parse_primary with unknown token raises SyntaxError."""
        tokens = [_make_token("KEYWORD", "if")]
        state = _make_parser_state(tokens)
        
        with self.assertRaises(SyntaxError):
            _parse_primary(state)


if __name__ == "__main__":
    unittest.main()

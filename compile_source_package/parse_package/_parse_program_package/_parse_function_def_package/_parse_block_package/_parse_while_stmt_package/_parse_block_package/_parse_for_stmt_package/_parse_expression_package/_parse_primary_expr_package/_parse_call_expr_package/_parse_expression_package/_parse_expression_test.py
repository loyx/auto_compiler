# -*- coding: utf-8 -*-
"""Unit tests for _parse_expression function."""

import unittest
from unittest.mock import patch
from typing import Any, Dict

# Relative import from the same package
from ._parse_expression_src import _parse_expression, _parse_primary, _parse_binary_op, _get_precedence


def make_token(ttype: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
    """Helper to create a token dict."""
    return {"type": ttype, "value": value, "line": line, "column": column}


def make_parser_state(tokens: list, pos: int = 0, filename: str = "test.py") -> Dict[str, Any]:
    """Helper to create a parser state dict."""
    return {"tokens": tokens, "pos": pos, "filename": filename, "error": ""}


class TestParseExpression(unittest.TestCase):
    """Test cases for _parse_expression function."""

    def test_parse_number_literal(self):
        """Test parsing a NUMBER literal."""
        tokens = [make_token("NUMBER", "42")]
        parser_state = make_parser_state(tokens)
        
        result = _parse_expression(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "42")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 1)
        self.assertEqual(parser_state.get("error"), "")

    def test_parse_string_literal(self):
        """Test parsing a STRING literal."""
        tokens = [make_token("STRING", '"hello"')]
        parser_state = make_parser_state(tokens)
        
        result = _parse_expression(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], '"hello"')
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_identifier(self):
        """Test parsing an IDENTIFIER."""
        tokens = [make_token("IDENTIFIER", "x")]
        parser_state = make_parser_state(tokens)
        
        result = _parse_expression(parser_state)
        
        self.assertEqual(result["type"], "IDENT")
        self.assertEqual(result["value"], "x")
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_identifier_followed_by_lparen_calls_parse_call_expr(self):
        """Test that identifier followed by LPAREN delegates to _parse_call_expr."""
        tokens = [make_token("IDENTIFIER", "foo"), make_token("LPAREN", "("), make_token("RPAREN", ")")]
        parser_state = make_parser_state(tokens)
        
        mock_call_result = {"type": "CALL", "value": "foo", "line": 1, "column": 1, "children": []}
        
        with patch("._parse_expression_src._parse_call_expr", return_value=mock_call_result) as mock_call:
            result = _parse_expression(parser_state)
            
            mock_call.assert_called_once()
            self.assertEqual(result["type"], "CALL")
            self.assertEqual(result["value"], "foo")

    def test_parse_parenthesized_expression(self):
        """Test parsing a parenthesized expression."""
        tokens = [
            make_token("LPAREN", "(", column=1),
            make_token("NUMBER", "42", column=2),
            make_token("RPAREN", ")", column=3)
        ]
        parser_state = make_parser_state(tokens)
        
        result = _parse_expression(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "42")
        self.assertEqual(parser_state["pos"], 3)

    def test_parse_parenthesized_expression_missing_rparen(self):
        """Test error when parenthesized expression is missing closing paren."""
        tokens = [
            make_token("LPAREN", "(", column=1),
            make_token("NUMBER", "42", column=2)
        ]
        parser_state = make_parser_state(tokens)
        
        result = _parse_expression(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertIn("Missing", parser_state.get("error", ""))

    def test_parse_binary_op_addition(self):
        """Test parsing addition expression."""
        tokens = [
            make_token("NUMBER", "1", column=1),
            make_token("PLUS", "+", column=2),
            make_token("NUMBER", "2", column=3)
        ]
        parser_state = make_parser_state(tokens)
        
        result = _parse_expression(parser_state)
        
        self.assertEqual(result["type"], "BINOP")
        self.assertEqual(result["value"], "+")
        self.assertEqual(len(result["children"]), 2)
        self.assertEqual(result["children"][0]["type"], "LITERAL")
        self.assertEqual(result["children"][0]["value"], "1")
        self.assertEqual(result["children"][1]["type"], "LITERAL")
        self.assertEqual(result["children"][1]["value"], "2")
        self.assertEqual(parser_state["pos"], 3)

    def test_parse_binary_op_multiplication_higher_precedence(self):
        """Test that multiplication has higher precedence than addition."""
        tokens = [
            make_token("NUMBER", "1", column=1),
            make_token("PLUS", "+", column=2),
            make_token("NUMBER", "2", column=3),
            make_token("STAR", "*", column=4),
            make_token("NUMBER", "3", column=5)
        ]
        parser_state = make_parser_state(tokens)
        
        result = _parse_expression(parser_state)
        
        # Should be: 1 + (2 * 3), so top-level is PLUS with right child being STAR
        self.assertEqual(result["type"], "BINOP")
        self.assertEqual(result["value"], "+")
        self.assertEqual(result["children"][0]["value"], "1")
        right = result["children"][1]
        self.assertEqual(right["type"], "BINOP")
        self.assertEqual(right["value"], "*")
        self.assertEqual(right["children"][0]["value"], "2")
        self.assertEqual(right["children"][1]["value"], "3")

    def test_parse_binary_op_comparison_lower_precedence(self):
        """Test that comparison operators have lower precedence than addition."""
        tokens = [
            make_token("NUMBER", "1", column=1),
            make_token("PLUS", "+", column=2),
            make_token("NUMBER", "2", column=3),
            make_token("EQ", "==", column=4),
            make_token("NUMBER", "3", column=5)
        ]
        parser_state = make_parser_state(tokens)
        
        result = _parse_expression(parser_state)
        
        # Should be: (1 + 2) == 3, so top-level is EQ
        self.assertEqual(result["type"], "BINOP")
        self.assertEqual(result["value"], "==")
        left = result["children"][0]
        self.assertEqual(left["type"], "BINOP")
        self.assertEqual(left["value"], "+")
        self.assertEqual(result["children"][1]["value"], "3")

    def test_parse_unexpected_eof(self):
        """Test error when input is empty."""
        parser_state = make_parser_state([])
        
        result = _parse_expression(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertIn("EOF", parser_state.get("error", ""))
        self.assertEqual(parser_state["pos"], 0)

    def test_parse_unexpected_token(self):
        """Test error when encountering an unexpected token type."""
        tokens = [make_token("LPAREN", "(")]
        parser_state = make_parser_state(tokens)
        
        result = _parse_expression(parser_state)
        
        # LPAREN will try to parse as parenthesized expression
        # Let's test with a standalone operator
        tokens2 = [make_token("PLUS", "+")]
        parser_state2 = make_parser_state(tokens2)
        
        result = _parse_expression(parser_state2)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertIn("Unexpected token", parser_state2.get("error", ""))


class TestParsePrimary(unittest.TestCase):
    """Test cases for _parse_primary helper function."""

    def test_parse_primary_number(self):
        """Test _parse_primary with NUMBER token."""
        tokens = [make_token("NUMBER", "123")]
        parser_state = make_parser_state(tokens)
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "123")
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_primary_string(self):
        """Test _parse_primary with STRING token."""
        tokens = [make_token("STRING", '"test"')]
        parser_state = make_parser_state(tokens)
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], '"test"')

    def test_parse_primary_identifier_no_call(self):
        """Test _parse_primary with IDENTIFIER not followed by LPAREN."""
        tokens = [make_token("IDENTIFIER", "var")]
        parser_state = make_parser_state(tokens)
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "IDENT")
        self.assertEqual(result["value"], "var")
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_primary_identifier_with_call(self):
        """Test _parse_primary with IDENTIFIER followed by LPAREN."""
        tokens = [
            make_token("IDENTIFIER", "func"),
            make_token("LPAREN", "("),
            make_token("RPAREN", ")")
        ]
        parser_state = make_parser_state(tokens)
        
        mock_call_result = {"type": "CALL", "value": "func", "line": 1, "column": 1, "children": []}
        
        with patch("._parse_expression_src._parse_call_expr", return_value=mock_call_result) as mock_call:
            result = _parse_primary(parser_state)
            
            mock_call.assert_called_once()
            self.assertEqual(result["type"], "CALL")

    def test_parse_primary_parenthesized(self):
        """Test _parse_primary with LPAREN starting parenthesized expression."""
        tokens = [
            make_token("LPAREN", "("),
            make_token("NUMBER", "5"),
            make_token("RPAREN", ")")
        ]
        parser_state = make_parser_state(tokens)
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "5")
        self.assertEqual(parser_state["pos"], 3)

    def test_parse_primary_invalid_token(self):
        """Test _parse_primary with invalid token type."""
        tokens = [make_token("PLUS", "+")]
        parser_state = make_parser_state(tokens)
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertIn("Unexpected token", parser_state.get("error", ""))


class TestGetPrecedence(unittest.TestCase):
    """Test cases for _get_precedence helper function."""

    def test_precedence_plus_minus(self):
        """Test precedence for PLUS and MINUS operators."""
        self.assertEqual(_get_precedence("PLUS"), 2)
        self.assertEqual(_get_precedence("MINUS"), 2)

    def test_precedence_star_slash(self):
        """Test precedence for STAR and SLASH operators."""
        self.assertEqual(_get_precedence("STAR"), 3)
        self.assertEqual(_get_precedence("SLASH"), 3)

    def test_precedence_comparison(self):
        """Test precedence for comparison operators."""
        self.assertEqual(_get_precedence("EQ"), 1)
        self.assertEqual(_get_precedence("NEQ"), 1)
        self.assertEqual(_get_precedence("LT"), 1)
        self.assertEqual(_get_precedence("GT"), 1)
        self.assertEqual(_get_precedence("LTE"), 1)
        self.assertEqual(_get_precedence("GTE"), 1)

    def test_precedence_unknown(self):
        """Test precedence for unknown operator types."""
        self.assertEqual(_get_precedence("UNKNOWN"), 0)
        self.assertEqual(_get_precedence("IDENTIFIER"), 0)
        self.assertEqual(_get_precedence("NUMBER"), 0)


class TestParseBinaryOp(unittest.TestCase):
    """Test cases for _parse_binary_op helper function."""

    def test_parse_binary_op_no_operator(self):
        """Test _parse_binary_op when there's no operator token."""
        tokens = [make_token("NUMBER", "1")]
        parser_state = make_parser_state(tokens, pos=1)
        left = {"type": "LITERAL", "value": "1", "line": 1, "column": 1, "children": []}
        
        result = _parse_binary_op(parser_state, left, 0)
        
        self.assertEqual(result, left)
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_binary_op_single_operator(self):
        """Test _parse_binary_op with a single operator."""
        tokens = [
            make_token("PLUS", "+"),
            make_token("NUMBER", "2")
        ]
        parser_state = make_parser_state(tokens, pos=0)
        left = {"type": "LITERAL", "value": "1", "line": 1, "column": 1, "children": []}
        
        parser_state["pos"] = 0
        
        result = _parse_binary_op(parser_state, left, 0)
        
        self.assertEqual(result["type"], "BINOP")
        self.assertEqual(result["value"], "+")


class TestParseExpressionIntegration(unittest.TestCase):
    """Integration tests for _parse_expression with complex expressions."""

    def test_complex_expression_precedence(self):
        """Test complex expression: 1 + 2 * 3 - 4."""
        tokens = [
            make_token("NUMBER", "1", column=1),
            make_token("PLUS", "+", column=2),
            make_token("NUMBER", "2", column=3),
            make_token("STAR", "*", column=4),
            make_token("NUMBER", "3", column=5),
            make_token("MINUS", "-", column=6),
            make_token("NUMBER", "4", column=7)
        ]
        parser_state = make_parser_state(tokens)
        
        result = _parse_expression(parser_state)
        
        self.assertEqual(result["type"], "BINOP")
        self.assertEqual(result["value"], "-")
        self.assertEqual(parser_state["pos"], 7)

    def test_nested_parentheses(self):
        """Test nested parentheses: ((1 + 2))."""
        tokens = [
            make_token("LPAREN", "("),
            make_token("LPAREN", "("),
            make_token("NUMBER", "1"),
            make_token("PLUS", "+"),
            make_token("NUMBER", "2"),
            make_token("RPAREN", ")"),
            make_token("RPAREN", ")")
        ]
        parser_state = make_parser_state(tokens)
        
        result = _parse_expression(parser_state)
        
        self.assertEqual(result["type"], "BINOP")
        self.assertEqual(result["value"], "+")
        self.assertEqual(parser_state["pos"], 7)

    def test_mixed_identifiers_and_literals(self):
        """Test expression with identifiers and literals: x + 1."""
        tokens = [
            make_token("IDENTIFIER", "x"),
            make_token("PLUS", "+"),
            make_token("NUMBER", "1")
        ]
        parser_state = make_parser_state(tokens)
        
        result = _parse_expression(parser_state)
        
        self.assertEqual(result["type"], "BINOP")
        self.assertEqual(result["value"], "+")
        self.assertEqual(result["children"][0]["type"], "IDENT")
        self.assertEqual(result["children"][0]["value"], "x")
        self.assertEqual(result["children"][1]["type"], "LITERAL")
        self.assertEqual(result["children"][1]["value"], "1")


if __name__ == "__main__":
    unittest.main()

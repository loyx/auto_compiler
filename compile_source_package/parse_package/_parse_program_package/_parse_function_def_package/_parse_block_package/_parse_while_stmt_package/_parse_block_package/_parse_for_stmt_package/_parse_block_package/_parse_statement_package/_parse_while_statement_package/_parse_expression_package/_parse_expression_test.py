# -*- coding: utf-8 -*-
"""Unit tests for _parse_expression function."""

import unittest
from typing import Any, Dict

from ._parse_expression_src import _parse_expression


def make_token(token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
    """Helper to create a token dict."""
    return {
        "type": token_type,
        "value": value,
        "line": line,
        "column": column
    }


def make_parser_state(tokens: list, pos: int = 0, filename: str = "") -> Dict[str, Any]:
    """Helper to create a parser_state dict."""
    return {
        "tokens": tokens,
        "pos": pos,
        "filename": filename
    }


class TestParseExpression(unittest.TestCase):
    """Test cases for _parse_expression function."""

    def test_parse_identifier(self):
        """Test parsing a simple identifier."""
        tokens = [make_token("IDENTIFIER", "x", 1, 1)]
        state = make_parser_state(tokens)
        
        result = _parse_expression(state)
        
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "x")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(state["pos"], 1)

    def test_parse_number_literal(self):
        """Test parsing a NUMBER literal."""
        tokens = [make_token("NUMBER", "42", 1, 1)]
        state = make_parser_state(tokens)
        
        result = _parse_expression(state)
        
        self.assertEqual(result["type"], "NUMBER")
        self.assertEqual(result["value"], "42")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(state["pos"], 1)

    def test_parse_string_literal(self):
        """Test parsing a STRING literal."""
        tokens = [make_token("STRING", '"hello"', 1, 1)]
        state = make_parser_state(tokens)
        
        result = _parse_expression(state)
        
        self.assertEqual(result["type"], "STRING")
        self.assertEqual(result["value"], '"hello"')
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(state["pos"], 1)

    def test_parse_binary_operation(self):
        """Test parsing a binary operation: 1 + 2."""
        tokens = [
            make_token("NUMBER", "1", 1, 1),
            make_token("PLUS", "+", 1, 3),
            make_token("NUMBER", "2", 1, 5)
        ]
        state = make_parser_state(tokens)
        
        result = _parse_expression(state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["operator"], "+")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 3)
        self.assertEqual(len(result["children"]), 2)
        
        left = result["children"][0]
        self.assertEqual(left["type"], "NUMBER")
        self.assertEqual(left["value"], "1")
        
        right = result["children"][1]
        self.assertEqual(right["type"], "NUMBER")
        self.assertEqual(right["value"], "2")
        
        self.assertEqual(state["pos"], 3)

    def test_parse_binary_operation_with_identifier(self):
        """Test parsing binary op with identifier: x + y."""
        tokens = [
            make_token("IDENTIFIER", "x", 1, 1),
            make_token("PLUS", "+", 1, 3),
            make_token("IDENTIFIER", "y", 1, 5)
        ]
        state = make_parser_state(tokens)
        
        result = _parse_expression(state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["operator"], "+")
        self.assertEqual(state["pos"], 3)

    def test_parse_parenthesized_expression(self):
        """Test parsing parenthesized expression: (x)."""
        tokens = [
            make_token("LPAREN", "(", 1, 1),
            make_token("IDENTIFIER", "x", 1, 2),
            make_token("RPAREN", ")", 1, 3)
        ]
        state = make_parser_state(tokens)
        
        result = _parse_expression(state)
        
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "x")
        self.assertEqual(state["pos"], 3)

    def test_parse_parenthesized_binary_op(self):
        """Test parsing parenthesized binary op: (1 + 2)."""
        tokens = [
            make_token("LPAREN", "(", 1, 1),
            make_token("NUMBER", "1", 1, 2),
            make_token("PLUS", "+", 1, 4),
            make_token("NUMBER", "2", 1, 6),
            make_token("RPAREN", ")", 1, 7)
        ]
        state = make_parser_state(tokens)
        
        result = _parse_expression(state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["operator"], "+")
        self.assertEqual(state["pos"], 5)

    def test_parse_nested_parentheses(self):
        """Test parsing nested parentheses: ((x))."""
        tokens = [
            make_token("LPAREN", "(", 1, 1),
            make_token("LPAREN", "(", 1, 2),
            make_token("IDENTIFIER", "x", 1, 3),
            make_token("RPAREN", ")", 1, 4),
            make_token("RPAREN", ")", 1, 5)
        ]
        state = make_parser_state(tokens)
        
        result = _parse_expression(state)
        
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "x")
        self.assertEqual(state["pos"], 5)

    def test_parse_chained_binary_operations(self):
        """Test parsing chained binary ops: 1 + 2 + 3 (left-associative)."""
        tokens = [
            make_token("NUMBER", "1", 1, 1),
            make_token("PLUS", "+", 1, 3),
            make_token("NUMBER", "2", 1, 5),
            make_token("PLUS", "+", 1, 7),
            make_token("NUMBER", "3", 1, 9)
        ]
        state = make_parser_state(tokens)
        
        result = _parse_expression(state)
        
        # First binary op consumes 1 + (2 + 3) due to recursive nature
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(state["pos"], 5)

    def test_parse_different_operators(self):
        """Test parsing with different operator types."""
        operators = [
            ("PLUS", "+"),
            ("MINUS", "-"),
            ("MULTIPLY", "*"),
            ("DIVIDE", "/"),
            ("EQUALS", "="),
            ("LESS", "<"),
            ("GREATER", ">")
        ]
        
        for op_type, op_value in operators:
            with self.subTest(operator=op_value):
                tokens = [
                    make_token("NUMBER", "1", 1, 1),
                    make_token(op_type, op_value, 1, 3),
                    make_token("NUMBER", "2", 1, 5)
                ]
                state = make_parser_state(tokens)
                
                result = _parse_expression(state)
                
                self.assertEqual(result["type"], "BINARY_OP")
                self.assertEqual(result["operator"], op_value)
                self.assertEqual(state["pos"], 3)

    def test_incomplete_expression_empty_tokens(self):
        """Test error when tokens list is empty."""
        tokens = []
        state = make_parser_state(tokens)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_expression(state)
        
        self.assertIn("Incomplete expression", str(context.exception))

    def test_incomplete_expression_pos_at_end(self):
        """Test error when pos is at end of tokens."""
        tokens = [make_token("NUMBER", "1", 1, 1)]
        state = make_parser_state(tokens, pos=1)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_expression(state)
        
        self.assertIn("Incomplete expression", str(context.exception))

    def test_invalid_expression_start(self):
        """Test error when expression starts with invalid token."""
        tokens = [make_token("LPAREN", "(", 1, 1)]
        state = make_parser_state(tokens)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_expression(state)
        
        self.assertIn("Invalid expression start", str(context.exception))

    def test_missing_closing_paren(self):
        """Test error when closing paren is missing."""
        tokens = [
            make_token("LPAREN", "(", 1, 1),
            make_token("IDENTIFIER", "x", 1, 2)
        ]
        state = make_parser_state(tokens)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_expression(state)
        
        self.assertIn("Incomplete expression", str(context.exception))

    def test_wrong_closing_token(self):
        """Test error when wrong token closes paren."""
        tokens = [
            make_token("LPAREN", "(", 1, 1),
            make_token("IDENTIFIER", "x", 1, 2),
            make_token("NUMBER", "1", 1, 3)
        ]
        state = make_parser_state(tokens)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_expression(state)
        
        self.assertIn("Expected ')'", str(context.exception))

    def test_binary_op_missing_right_operand(self):
        """Test error when binary op has no right operand."""
        tokens = [
            make_token("NUMBER", "1", 1, 1),
            make_token("PLUS", "+", 1, 3)
        ]
        state = make_parser_state(tokens)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_expression(state)
        
        self.assertIn("Incomplete expression", str(context.exception))

    def test_position_updated_correctly(self):
        """Test that parser_state pos is updated correctly after parsing."""
        tokens = [
            make_token("NUMBER", "1", 1, 1),
            make_token("PLUS", "+", 1, 3),
            make_token("NUMBER", "2", 1, 5),
            make_token("IDENTIFIER", "x", 2, 1)
        ]
        state = make_parser_state(tokens)
        
        result = _parse_expression(state)
        
        # Should consume 1 + 2, leaving pos at 3 (pointing to IDENTIFIER)
        self.assertEqual(state["pos"], 3)
        self.assertEqual(result["type"], "BINARY_OP")

    def test_line_column_preserved(self):
        """Test that line and column information is preserved in AST."""
        tokens = [
            make_token("IDENTIFIER", "var", 5, 10),
            make_token("PLUS", "+", 5, 14),
            make_token("NUMBER", "100", 5, 16)
        ]
        state = make_parser_state(tokens)
        
        result = _parse_expression(state)
        
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 14)
        self.assertEqual(result["children"][0]["line"], 5)
        self.assertEqual(result["children"][0]["column"], 10)
        self.assertEqual(result["children"][1]["line"], 5)
        self.assertEqual(result["children"][1]["column"], 16)


if __name__ == "__main__":
    unittest.main()

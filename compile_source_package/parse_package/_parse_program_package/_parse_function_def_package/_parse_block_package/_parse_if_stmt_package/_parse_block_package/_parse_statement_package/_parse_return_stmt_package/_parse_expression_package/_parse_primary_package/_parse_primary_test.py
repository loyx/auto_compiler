# -*- coding: utf-8 -*-
"""Unit tests for _parse_primary function."""

import unittest
from unittest.mock import patch
from typing import Dict, Any, List

# Relative import from the same package
from ._parse_primary_src import _parse_primary


def create_token(token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
    """Helper to create a token dict."""
    return {
        "type": token_type,
        "value": value,
        "line": line,
        "column": column
    }


def create_parser_state(tokens: List[Dict[str, Any]], pos: int = 0, filename: str = "<test>") -> Dict[str, Any]:
    """Helper to create a parser state dict."""
    return {
        "tokens": tokens,
        "pos": pos,
        "filename": filename
    }


class TestParsePrimary(unittest.TestCase):
    """Test cases for _parse_primary function."""

    def test_parse_identifier(self):
        """Test parsing a simple identifier."""
        tokens = [create_token("IDENTIFIER", "x")]
        parser_state = create_parser_state(tokens)
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "x")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(result["children"], [])
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_identifier_at_different_position(self):
        """Test parsing identifier at non-zero position."""
        tokens = [create_token("NUMBER_INT", "1"), create_token("IDENTIFIER", "y", column=5)]
        parser_state = create_parser_state(tokens, pos=1)
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "y")
        self.assertEqual(result["column"], 5)
        self.assertEqual(parser_state["pos"], 2)

    def test_parse_integer_literal(self):
        """Test parsing an integer literal."""
        tokens = [create_token("NUMBER_INT", "42")]
        parser_state = create_parser_state(tokens)
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], 42)
        self.assertIsInstance(result["value"], int)
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_negative_integer_literal(self):
        """Test parsing a negative integer literal."""
        tokens = [create_token("NUMBER_INT", "-123")]
        parser_state = create_parser_state(tokens)
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], -123)
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_float_literal(self):
        """Test parsing a float literal."""
        tokens = [create_token("NUMBER_FLOAT", "3.14")]
        parser_state = create_parser_state(tokens)
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], 3.14)
        self.assertIsInstance(result["value"], float)
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_string_literal(self):
        """Test parsing a string literal."""
        tokens = [create_token("STRING", "hello world")]
        parser_state = create_parser_state(tokens)
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "hello world")
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_string_with_quotes(self):
        """Test parsing a string literal with quotes included."""
        tokens = [create_token("STRING", '"quoted string"')]
        parser_state = create_parser_state(tokens)
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], '"quoted string"')
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_bool_true(self):
        """Test parsing boolean true literal."""
        tokens = [create_token("BOOL", "true")]
        parser_state = create_parser_state(tokens)
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], True)
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_bool_false(self):
        """Test parsing boolean false literal."""
        tokens = [create_token("BOOL", "false")]
        parser_state = create_parser_state(tokens)
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], False)
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_bool_true_uppercase(self):
        """Test parsing boolean TRUE literal (uppercase)."""
        tokens = [create_token("BOOL", "TRUE")]
        parser_state = create_parser_state(tokens)
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], True)
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_null_literal(self):
        """Test parsing null literal."""
        tokens = [create_token("NULL", "null")]
        parser_state = create_parser_state(tokens)
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertIsNone(result["value"])
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_null_uppercase(self):
        """Test parsing NULL literal (uppercase)."""
        tokens = [create_token("NULL", "NULL")]
        parser_state = create_parser_state(tokens)
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertIsNone(result["value"])
        self.assertEqual(parser_state["pos"], 1)

    @patch('._parse_primary_package._parse_unary_expr_package._parse_unary_expr_src._parse_unary_expr')
    def test_parse_unary_minus(self, mock_parse_unary):
        """Test parsing unary minus operator delegates to _parse_unary_expr."""
        tokens = [create_token("OPERATOR", "-")]
        parser_state = create_parser_state(tokens)
        
        expected_ast = {"type": "UNARY_OP", "value": "-", "children": []}
        mock_parse_unary.return_value = expected_ast
        
        result = _parse_primary(parser_state)
        
        mock_parse_unary.assert_called_once_with(parser_state)
        self.assertEqual(result, expected_ast)
        # pos should not be advanced by _parse_primary for unary ops
        self.assertEqual(parser_state["pos"], 0)

    @patch('._parse_primary_package._parse_unary_expr_package._parse_unary_expr_src._parse_unary_expr')
    def test_parse_unary_not(self, mock_parse_unary):
        """Test parsing unary not operator delegates to _parse_unary_expr."""
        tokens = [create_token("OPERATOR", "!")]
        parser_state = create_parser_state(tokens)
        
        expected_ast = {"type": "UNARY_OP", "value": "!", "children": []}
        mock_parse_unary.return_value = expected_ast
        
        result = _parse_primary(parser_state)
        
        mock_parse_unary.assert_called_once_with(parser_state)
        self.assertEqual(result, expected_ast)

    @patch('._parse_primary_package._parse_unary_expr_package._parse_unary_expr_src._parse_unary_expr')
    def test_parse_unary_bitwise_not(self, mock_parse_unary):
        """Test parsing unary bitwise not operator delegates to _parse_unary_expr."""
        tokens = [create_token("OPERATOR", "~")]
        parser_state = create_parser_state(tokens)
        
        expected_ast = {"type": "UNARY_OP", "value": "~", "children": []}
        mock_parse_unary.return_value = expected_ast
        
        result = _parse_primary(parser_state)
        
        mock_parse_unary.assert_called_once_with(parser_state)
        self.assertEqual(result, expected_ast)

    @patch('._parse_primary_package._parse_expression_package._parse_expression_src._parse_expression')
    def test_parse_parenthesized_expression(self, mock_parse_expr):
        """Test parsing parenthesized expression delegates to _parse_expression."""
        tokens = [
            create_token("LPAREN", "(", line=2, column=3),
            create_token("NUMBER_INT", "5"),
            create_token("RPAREN", ")")
        ]
        parser_state = create_parser_state(tokens)
        
        expected_ast = {"type": "LITERAL", "value": 5}
        mock_parse_expr.return_value = expected_ast
        
        result = _parse_primary(parser_state)
        
        mock_parse_expr.assert_called_once_with(parser_state)
        self.assertEqual(result, expected_ast)
        self.assertEqual(parser_state["pos"], 3)  # consumed (, expr, )

    @patch('._parse_primary_package._parse_expression_package._parse_expression_src._parse_expression')
    def test_parse_parenthesized_expression_missing_closing(self, mock_parse_expr):
        """Test parsing parenthesized expression with missing closing paren raises SyntaxError."""
        tokens = [
            create_token("LPAREN", "(", line=2, column=3),
            create_token("NUMBER_INT", "5")
        ]
        parser_state = create_parser_state(tokens)
        
        expected_ast = {"type": "LITERAL", "value": 5}
        mock_parse_expr.return_value = expected_ast
        
        with self.assertRaises(SyntaxError) as context:
            _parse_primary(parser_state)
        
        self.assertIn("Expected ')'", str(context.exception))
        self.assertIn("2:3", str(context.exception))

    @patch('._parse_primary_package._parse_expression_package._parse_expression_src._parse_expression')
    def test_parse_parenthesized_expression_wrong_closing(self, mock_parse_expr):
        """Test parsing parenthesized expression with wrong closing token raises SyntaxError."""
        tokens = [
            create_token("LPAREN", "(", line=2, column=3),
            create_token("NUMBER_INT", "5"),
            create_token("COMMA", ",")
        ]
        parser_state = create_parser_state(tokens)
        
        expected_ast = {"type": "LITERAL", "value": 5}
        mock_parse_expr.return_value = expected_ast
        
        with self.assertRaises(SyntaxError) as context:
            _parse_primary(parser_state)
        
        self.assertIn("Expected ')'", str(context.exception))

    @patch('._parse_primary_package._parse_function_call_package._parse_function_call_src._parse_function_call')
    def test_parse_function_call(self, mock_parse_func_call):
        """Test parsing function call delegates to _parse_function_call."""
        tokens = [
            create_token("IDENTIFIER", "foo", line=5, column=10),
            create_token("LPAREN", "(")
        ]
        parser_state = create_parser_state(tokens)
        
        expected_ast = {"type": "CALL", "value": "foo", "children": []}
        mock_parse_func_call.return_value = expected_ast
        
        result = _parse_primary(parser_state)
        
        mock_parse_func_call.assert_called_once_with(parser_state, "foo", 5, 10)
        self.assertEqual(result, expected_ast)

    @patch('._parse_primary_package._parse_function_call_package._parse_function_call_src._parse_function_call')
    def test_parse_function_call_with_args(self, mock_parse_func_call):
        """Test parsing function call with arguments."""
        tokens = [
            create_token("IDENTIFIER", "bar", line=1, column=1),
            create_token("LPAREN", "("),
            create_token("NUMBER_INT", "1"),
            create_token("COMMA", ","),
            create_token("NUMBER_INT", "2"),
            create_token("RPAREN", ")")
        ]
        parser_state = create_parser_state(tokens)
        
        expected_ast = {"type": "CALL", "value": "bar", "children": []}
        mock_parse_func_call.return_value = expected_ast
        
        result = _parse_primary(parser_state)
        
        mock_parse_func_call.assert_called_once_with(parser_state, "bar", 1, 1)
        self.assertEqual(result, expected_ast)

    def test_parse_empty_token_list(self):
        """Test parsing with empty token list raises SyntaxError."""
        tokens = []
        parser_state = create_parser_state(tokens)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_primary(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))
        self.assertIn("<test>:0:0", str(context.exception))

    def test_parse_pos_beyond_tokens(self):
        """Test parsing when pos is beyond token list raises SyntaxError."""
        tokens = [create_token("NUMBER_INT", "1")]
        parser_state = create_parser_state(tokens, pos=5)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_primary(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))

    def test_parse_unexpected_token(self):
        """Test parsing unexpected token type raises SyntaxError."""
        tokens = [create_token("KEYWORD", "if", line=10, column=20)]
        parser_state = create_parser_state(tokens)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_primary(parser_state)
        
        self.assertIn("Unexpected token 'if'", str(context.exception))
        self.assertIn("10:20", str(context.exception))

    def test_parse_unexpected_operator(self):
        """Test parsing unexpected operator (not unary) raises SyntaxError."""
        tokens = [create_token("OPERATOR", "+", line=3, column=5)]
        parser_state = create_parser_state(tokens)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_primary(parser_state)
        
        self.assertIn("Unexpected token '+'", str(context.exception))
        self.assertIn("3:5", str(context.exception))

    def test_parse_custom_filename_in_error(self):
        """Test that custom filename appears in error message."""
        tokens = []
        parser_state = create_parser_state(tokens, filename="my_file.cc")
        
        with self.assertRaises(SyntaxError) as context:
            _parse_primary(parser_state)
        
        self.assertIn("my_file.cc:0:0", str(context.exception))

    def test_parse_missing_token_type(self):
        """Test parsing token without type field handles gracefully."""
        tokens = [{"value": "something", "line": 1, "column": 1}]
        parser_state = create_parser_state(tokens)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_primary(parser_state)
        
        self.assertIn("Unexpected token 'something'", str(context.exception))

    def test_parse_missing_token_value(self):
        """Test parsing token without value field handles gracefully."""
        tokens = [{"type": "UNKNOWN", "line": 1, "column": 1}]
        parser_state = create_parser_state(tokens)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_primary(parser_state)
        
        self.assertIn("Unexpected token ''", str(context.exception))

    def test_parse_missing_line_column(self):
        """Test parsing token without line/column uses defaults."""
        tokens = [{"type": "UNKNOWN", "value": "test"}]
        parser_state = create_parser_state(tokens)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_primary(parser_state)
        
        self.assertIn(":0:0:", str(context.exception))


if __name__ == "__main__":
    unittest.main()

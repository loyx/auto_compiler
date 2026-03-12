"""
Unit tests for _parse_primary function.
Tests parsing of basic expression units: identifiers, literals, and parenthesized expressions.
"""

import unittest
from unittest.mock import patch

from ._parse_primary_src import _parse_primary


def _mock_consume_token_side_effect(state):
    """Side effect function for mocking _consume_token."""
    state["pos"] = state["pos"] + 1
    return state["tokens"][state["pos"] - 1]


class TestParsePrimary(unittest.TestCase):
    """Test cases for _parse_primary function."""

    def test_parse_identifier(self):
        """Test parsing an IDENTIFIER token."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.cc"
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_expr_stmt_package._parse_expression_package._parse_unary_package._parse_primary_package._consume_token_package._consume_token_src._consume_token") as mock_consume:
            mock_consume.side_effect = _mock_consume_token_side_effect
            
            result = _parse_primary(parser_state)
            
            self.assertEqual(result["type"], "IDENTIFIER")
            self.assertEqual(result["value"], "x")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 5)
            self.assertEqual(parser_state["pos"], 1)

    def test_parse_number_literal(self):
        """Test parsing a NUMBER token."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "42", "line": 2, "column": 10}
            ],
            "pos": 0,
            "filename": "test.cc"
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_expr_stmt_package._parse_expression_package._parse_unary_package._parse_primary_package._consume_token_package._consume_token_src._consume_token") as mock_consume:
            mock_consume.side_effect = _mock_consume_token_side_effect
            
            result = _parse_primary(parser_state)
            
            self.assertEqual(result["type"], "LITERAL")
            self.assertEqual(result["value"], 42)
            self.assertEqual(result["line"], 2)
            self.assertEqual(result["column"], 10)
            self.assertEqual(parser_state["pos"], 1)

    def test_parse_string_literal(self):
        """Test parsing a STRING token with quotes."""
        parser_state = {
            "tokens": [
                {"type": "STRING", "value": '"hello"', "line": 3, "column": 15}
            ],
            "pos": 0,
            "filename": "test.cc"
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_expr_stmt_package._parse_expression_package._parse_unary_package._parse_primary_package._consume_token_package._consume_token_src._consume_token") as mock_consume:
            mock_consume.side_effect = _mock_consume_token_side_effect
            
            result = _parse_primary(parser_state)
            
            self.assertEqual(result["type"], "LITERAL")
            self.assertEqual(result["value"], "hello")
            self.assertEqual(result["line"], 3)
            self.assertEqual(result["column"], 15)
            self.assertEqual(parser_state["pos"], 1)

    def test_parse_string_literal_minimal(self):
        """Test parsing a STRING token with minimal length (empty string)."""
        parser_state = {
            "tokens": [
                {"type": "STRING", "value": '""', "line": 4, "column": 20}
            ],
            "pos": 0,
            "filename": "test.cc"
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_expr_stmt_package._parse_expression_package._parse_unary_package._parse_primary_package._consume_token_package._consume_token_src._consume_token") as mock_consume:
            mock_consume.side_effect = _mock_consume_token_side_effect
            
            result = _parse_primary(parser_state)
            
            self.assertEqual(result["type"], "LITERAL")
            self.assertEqual(result["value"], "")
            self.assertEqual(result["line"], 4)
            self.assertEqual(result["column"], 20)
            self.assertEqual(parser_state["pos"], 1)

    def test_parse_string_literal_single_char(self):
        """Test parsing a STRING token with single character."""
        parser_state = {
            "tokens": [
                {"type": "STRING", "value": '"a"', "line": 5, "column": 25}
            ],
            "pos": 0,
            "filename": "test.cc"
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_expr_stmt_package._parse_expression_package._parse_unary_package._parse_primary_package._consume_token_package._consume_token_src._consume_token") as mock_consume:
            mock_consume.side_effect = _mock_consume_token_side_effect
            
            result = _parse_primary(parser_state)
            
            self.assertEqual(result["type"], "LITERAL")
            self.assertEqual(result["value"], "a")
            self.assertEqual(result["line"], 5)
            self.assertEqual(result["column"], 25)
            self.assertEqual(parser_state["pos"], 1)

    def test_parse_keyword_true(self):
        """Test parsing KEYWORD token with value 'true'."""
        parser_state = {
            "tokens": [
                {"type": "KEYWORD", "value": "true", "line": 6, "column": 30}
            ],
            "pos": 0,
            "filename": "test.cc"
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_expr_stmt_package._parse_expression_package._parse_unary_package._parse_primary_package._consume_token_package._consume_token_src._consume_token") as mock_consume:
            mock_consume.side_effect = _mock_consume_token_side_effect
            
            result = _parse_primary(parser_state)
            
            self.assertEqual(result["type"], "LITERAL")
            self.assertEqual(result["value"], True)
            self.assertEqual(result["line"], 6)
            self.assertEqual(result["column"], 30)
            self.assertEqual(parser_state["pos"], 1)

    def test_parse_keyword_false(self):
        """Test parsing KEYWORD token with value 'false'."""
        parser_state = {
            "tokens": [
                {"type": "KEYWORD", "value": "false", "line": 7, "column": 35}
            ],
            "pos": 0,
            "filename": "test.cc"
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_expr_stmt_package._parse_expression_package._parse_unary_package._parse_primary_package._consume_token_package._consume_token_src._consume_token") as mock_consume:
            mock_consume.side_effect = _mock_consume_token_side_effect
            
            result = _parse_primary(parser_state)
            
            self.assertEqual(result["type"], "LITERAL")
            self.assertEqual(result["value"], False)
            self.assertEqual(result["line"], 7)
            self.assertEqual(result["column"], 35)
            self.assertEqual(parser_state["pos"], 1)

    def test_parse_keyword_invalid(self):
        """Test parsing KEYWORD token with invalid value raises SyntaxError."""
        parser_state = {
            "tokens": [
                {"type": "KEYWORD", "value": "if", "line": 8, "column": 40}
            ],
            "pos": 0,
            "filename": "test.cc"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_primary(parser_state)
        
        self.assertIn("Unexpected token 'if'", str(context.exception))
        self.assertIn("test.cc:8:40", str(context.exception))

    def test_parse_parenthesized_expression(self):
        """Test parsing a parenthesized expression."""
        inner_ast = {"type": "IDENTIFIER", "value": "y", "line": 9, "column": 46}
        parser_state = {
            "tokens": [
                {"type": "PUNCTUATION", "value": "(", "line": 9, "column": 45},
                {"type": "IDENTIFIER", "value": "y", "line": 9, "column": 46},
                {"type": "PUNCTUATION", "value": ")", "line": 9, "column": 47}
            ],
            "pos": 0,
            "filename": "test.cc"
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_expr_stmt_package._parse_expression_package._parse_unary_package._parse_primary_package._consume_token_package._consume_token_src._consume_token") as mock_consume, \
             patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_expr_stmt_package._parse_expression_package._parse_unary_package._parse_primary_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            
            mock_consume.side_effect = _mock_consume_token_side_effect
            mock_parse_expr.return_value = inner_ast
            
            result = _parse_primary(parser_state)
            
            self.assertEqual(result, inner_ast)
            self.assertEqual(parser_state["pos"], 3)
            mock_consume.assert_called()
            mock_parse_expr.assert_called_once()

    def test_parse_empty_tokens(self):
        """Test parsing with empty tokens list raises SyntaxError."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.cc"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_primary(parser_state)
        
        self.assertIn("Unexpected end of expression", str(context.exception))
        self.assertIn("test.cc", str(context.exception))

    def test_parse_pos_out_of_range(self):
        """Test parsing with pos beyond tokens length raises SyntaxError."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 5}
            ],
            "pos": 5,
            "filename": "test.cc"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_primary(parser_state)
        
        self.assertIn("Unexpected end of expression", str(context.exception))

    def test_parse_missing_closing_parenthesis_end(self):
        """Test parsing parenthesized expression with missing closing parenthesis at end."""
        parser_state = {
            "tokens": [
                {"type": "PUNCTUATION", "value": "(", "line": 10, "column": 50},
                {"type": "IDENTIFIER", "value": "z", "line": 10, "column": 51}
            ],
            "pos": 0,
            "filename": "test.cc"
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_expr_stmt_package._parse_expression_package._parse_unary_package._parse_primary_package._consume_token_package._consume_token_src._consume_token") as mock_consume, \
             patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_expr_stmt_package._parse_expression_package._parse_unary_package._parse_primary_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            
            mock_consume.side_effect = _mock_consume_token_side_effect
            mock_parse_expr.return_value = {"type": "IDENTIFIER", "value": "z", "line": 10, "column": 51}
            
            with self.assertRaises(SyntaxError) as context:
                _parse_primary(parser_state)
            
            self.assertIn("Missing closing parenthesis", str(context.exception))

    def test_parse_missing_closing_parenthesis_wrong_token(self):
        """Test parsing parenthesized expression with wrong closing token."""
        parser_state = {
            "tokens": [
                {"type": "PUNCTUATION", "value": "(", "line": 11, "column": 55},
                {"type": "IDENTIFIER", "value": "w", "line": 11, "column": 56},
                {"type": "PUNCTUATION", "value": ";", "line": 11, "column": 57}
            ],
            "pos": 0,
            "filename": "test.cc"
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_expr_stmt_package._parse_expression_package._parse_unary_package._parse_primary_package._consume_token_package._consume_token_src._consume_token") as mock_consume, \
             patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_expr_stmt_package._parse_expression_package._parse_unary_package._parse_primary_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            
            mock_consume.side_effect = _mock_consume_token_side_effect
            mock_parse_expr.return_value = {"type": "IDENTIFIER", "value": "w", "line": 11, "column": 56}
            
            with self.assertRaises(SyntaxError) as context:
                _parse_primary(parser_state)
            
            self.assertIn("Missing closing parenthesis", str(context.exception))

    def test_parse_unexpected_token_type(self):
        """Test parsing with unexpected token type raises SyntaxError."""
        parser_state = {
            "tokens": [
                {"type": "OPERATOR", "value": "+", "line": 12, "column": 60}
            ],
            "pos": 0,
            "filename": "test.cc"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_primary(parser_state)
        
        self.assertIn("Unexpected token '+'", str(context.exception))
        self.assertIn("test.cc:12:60", str(context.exception))

    def test_parse_default_filename(self):
        """Test that default filename '<unknown>' is used when not provided."""
        parser_state = {
            "tokens": [
                {"type": "KEYWORD", "value": "invalid", "line": 1, "column": 5}
            ],
            "pos": 0
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_primary(parser_state)
        
        self.assertIn("<unknown>", str(context.exception))


if __name__ == "__main__":
    unittest.main()

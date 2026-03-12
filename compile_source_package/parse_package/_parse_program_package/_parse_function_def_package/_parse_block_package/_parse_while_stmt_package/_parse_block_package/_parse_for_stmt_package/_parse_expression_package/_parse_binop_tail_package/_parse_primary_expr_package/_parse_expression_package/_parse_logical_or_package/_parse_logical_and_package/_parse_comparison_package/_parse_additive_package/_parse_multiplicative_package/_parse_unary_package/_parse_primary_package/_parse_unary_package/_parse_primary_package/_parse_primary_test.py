# -*- coding: utf-8 -*-
"""
Unit tests for _parse_primary function.
Tests primary expression parsing: literals, identifiers, and parenthesized expressions.
"""

import unittest
from unittest.mock import patch

# Relative import from the same package
from ._parse_primary_package._parse_primary_src import _parse_primary, _make_value_node, _make_identifier_node, _make_error_node


class TestParsePrimaryLiterals(unittest.TestCase):
    """Test cases for parsing literal tokens."""
    
    def test_parse_integer_literal(self):
        """Test parsing INTEGER token."""
        parser_state = {
            "tokens": [
                {"type": "INTEGER", "value": "42", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "VALUE")
        self.assertEqual(result["value"], "42")
        self.assertEqual(result["value_type"], "INTEGER")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 1)
        self.assertNotIn("error", parser_state)
    
    def test_parse_float_literal(self):
        """Test parsing FLOAT token."""
        parser_state = {
            "tokens": [
                {"type": "FLOAT", "value": "3.14", "line": 2, "column": 5}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "VALUE")
        self.assertEqual(result["value"], "3.14")
        self.assertEqual(result["value_type"], "FLOAT")
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 5)
        self.assertEqual(parser_state["pos"], 1)
    
    def test_parse_string_literal(self):
        """Test parsing STRING token."""
        parser_state = {
            "tokens": [
                {"type": "STRING", "value": '"hello world"', "line": 3, "column": 10}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "VALUE")
        self.assertEqual(result["value"], '"hello world"')
        self.assertEqual(result["value_type"], "STRING")
        self.assertEqual(parser_state["pos"], 1)
    
    def test_parse_boolean_true_literal(self):
        """Test parsing BOOLEAN token (true)."""
        parser_state = {
            "tokens": [
                {"type": "BOOLEAN", "value": "true", "line": 4, "column": 1}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "VALUE")
        self.assertEqual(result["value"], "true")
        self.assertEqual(result["value_type"], "BOOLEAN")
        self.assertEqual(parser_state["pos"], 1)
    
    def test_parse_boolean_false_literal(self):
        """Test parsing BOOLEAN token (false)."""
        parser_state = {
            "tokens": [
                {"type": "BOOLEAN", "value": "false", "line": 5, "column": 1}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "VALUE")
        self.assertEqual(result["value"], "false")
        self.assertEqual(result["value_type"], "BOOLEAN")
        self.assertEqual(parser_state["pos"], 1)
    
    def test_parse_nil_literal(self):
        """Test parsing NIL token."""
        parser_state = {
            "tokens": [
                {"type": "NIL", "value": "nil", "line": 6, "column": 1}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "VALUE")
        self.assertEqual(result["value"], "nil")
        self.assertEqual(result["value_type"], "NIL")
        self.assertEqual(parser_state["pos"], 1)


class TestParsePrimaryIdentifier(unittest.TestCase):
    """Test cases for parsing identifier tokens."""
    
    def test_parse_simple_identifier(self):
        """Test parsing a simple IDENTIFIER token."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "myVar", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["name"], "myVar")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 1)
        self.assertNotIn("error", parser_state)
    
    def test_parse_identifier_with_underscore(self):
        """Test parsing identifier with underscore."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "_private_var", "line": 2, "column": 3}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["name"], "_private_var")
        self.assertEqual(parser_state["pos"], 1)


class TestParsePrimaryParenthesized(unittest.TestCase):
    """Test cases for parsing parenthesized expressions."""
    
    @patch('._parse_primary_package._parse_primary_src._parse_expression')
    def test_parse_parenthesized_expression_success(self, mock_parse_expr):
        """Test parsing successful parenthesized expression."""
        mock_parse_expr.return_value = {
            "type": "VALUE",
            "value": "123",
            "value_type": "INTEGER",
            "line": 1,
            "column": 2
        }
        
        parser_state = {
            "tokens": [
                {"type": "LEFT_PAREN", "value": "(", "line": 1, "column": 1},
                {"type": "INTEGER", "value": "123", "line": 1, "column": 2},
                {"type": "RIGHT_PAREN", "value": ")", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "VALUE")
        self.assertEqual(result["value"], "123")
        self.assertEqual(parser_state["pos"], 3)
        mock_parse_expr.assert_called_once()
        self.assertNotIn("error", parser_state)
    
    @patch('._parse_primary_package._parse_primary_src._parse_expression')
    def test_parse_parenthesized_expression_error_propagation(self, mock_parse_expr):
        """Test error propagation from nested expression parsing."""
        mock_parse_expr.return_value = {
            "type": "ERROR",
            "message": "Invalid expression",
            "line": 1,
            "column": 2
        }
        # Simulate error being set in parser_state by _parse_expression
        def side_effect(ps):
            ps["error"] = "Invalid expression"
            return mock_parse_expr.return_value
        
        mock_parse_expr.side_effect = side_effect
        
        parser_state = {
            "tokens": [
                {"type": "LEFT_PAREN", "value": "(", "line": 1, "column": 1},
                {"type": "INTEGER", "value": "123", "line": 1, "column": 2}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertIn("error", parser_state)
        mock_parse_expr.assert_called_once()
    
    @patch('._parse_primary_package._parse_primary_src._parse_expression')
    def test_parse_parenthesized_missing_right_paren(self, mock_parse_expr):
        """Test parsing parenthesized expression without closing parenthesis."""
        mock_parse_expr.return_value = {
            "type": "VALUE",
            "value": "42",
            "value_type": "INTEGER",
            "line": 1,
            "column": 2
        }
        
        parser_state = {
            "tokens": [
                {"type": "LEFT_PAREN", "value": "(", "line": 1, "column": 1},
                {"type": "INTEGER", "value": "42", "line": 1, "column": 2}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["message"], "Missing closing parenthesis")
        self.assertIn("error", parser_state)
        self.assertEqual(parser_state["error"], "Missing closing parenthesis")
    
    @patch('._parse_primary_package._parse_primary_src._parse_expression')
    def test_parse_parenthesized_wrong_closing_token(self, mock_parse_expr):
        """Test parsing parenthesized expression with wrong closing token."""
        mock_parse_expr.return_value = {
            "type": "VALUE",
            "value": "42",
            "value_type": "INTEGER",
            "line": 1,
            "column": 2
        }
        
        parser_state = {
            "tokens": [
                {"type": "LEFT_PAREN", "value": "(", "line": 1, "column": 1},
                {"type": "INTEGER", "value": "42", "line": 1, "column": 2},
                {"type": "COMMA", "value": ",", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertIn("Expected RIGHT_PAREN", result["message"])
        self.assertIn("COMMA", result["message"])
        self.assertIn("error", parser_state)


class TestParsePrimaryErrorCases(unittest.TestCase):
    """Test cases for error conditions."""
    
    def test_empty_token_list(self):
        """Test parsing with empty token list."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.src"
        }
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["message"], "Unexpected end of input")
        self.assertIn("error", parser_state)
        self.assertEqual(parser_state["error"], "Unexpected end of input")
    
    def test_pos_beyond_token_list(self):
        """Test parsing when pos is beyond token list length."""
        parser_state = {
            "tokens": [
                {"type": "INTEGER", "value": "42", "line": 1, "column": 1}
            ],
            "pos": 5,
            "filename": "test.src"
        }
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["message"], "Unexpected end of input")
        self.assertIn("error", parser_state)
    
    def test_unexpected_token_type(self):
        """Test parsing with unexpected token type."""
        parser_state = {
            "tokens": [
                {"type": "PLUS", "value": "+", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["message"], "Unexpected token: PLUS")
        self.assertIn("error", parser_state)
        self.assertEqual(parser_state["pos"], 0)  # pos should not advance
    
    def test_operator_token_not_primary(self):
        """Test that operator tokens are not treated as primary expressions."""
        parser_state = {
            "tokens": [
                {"type": "STAR", "value": "*", "line": 2, "column": 5}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertIn("Unexpected token: STAR", result["message"])
    
    def test_keyword_token_not_primary(self):
        """Test that keyword tokens are not treated as primary expressions."""
        parser_state = {
            "tokens": [
                {"type": "IF", "value": "if", "line": 3, "column": 1}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertIn("Unexpected token: IF", result["message"])


class TestParsePrimaryEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""
    
    def test_multiple_tokens_only_consumes_one(self):
        """Test that only one token is consumed for simple literals."""
        parser_state = {
            "tokens": [
                {"type": "INTEGER", "value": "10", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 2},
                {"type": "INTEGER", "value": "20", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "VALUE")
        self.assertEqual(result["value"], "10")
        self.assertEqual(parser_state["pos"], 1)  # Only consumed first token
    
    def test_parse_from_middle_of_token_list(self):
        """Test parsing starting from middle position."""
        parser_state = {
            "tokens": [
                {"type": "PLUS", "value": "+", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 2},
                {"type": "MINUS", "value": "-", "line": 1, "column": 3}
            ],
            "pos": 1,
            "filename": "test.src"
        }
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["name"], "x")
        self.assertEqual(parser_state["pos"], 2)
    
    def test_token_missing_type_field(self):
        """Test handling of token with missing type field."""
        parser_state = {
            "tokens": [
                {"value": "something", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertIn("Unexpected token:", result["message"])
    
    def test_token_missing_value_field(self):
        """Test handling of token with missing value field."""
        parser_state = {
            "tokens": [
                {"type": "INTEGER", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "VALUE")
        self.assertEqual(result["value"], "")  # Empty string default
        self.assertEqual(result["value_type"], "INTEGER")
    
    def test_parser_state_missing_pos_field(self):
        """Test handling of parser_state without pos field."""
        parser_state = {
            "tokens": [
                {"type": "INTEGER", "value": "99", "line": 1, "column": 1}
            ],
            "filename": "test.src"
        }
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "VALUE")
        self.assertEqual(result["value"], "99")
        self.assertEqual(parser_state["pos"], 1)
    
    def test_parser_state_missing_tokens_field(self):
        """Test handling of parser_state without tokens field."""
        parser_state = {
            "pos": 0,
            "filename": "test.src"
        }
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["message"], "Unexpected end of input")


class TestHelperFunctions(unittest.TestCase):
    """Test helper functions used by _parse_primary."""
    
    def test_make_value_node(self):
        """Test _make_value_node creates correct structure."""
        node = _make_value_node("INTEGER", "42", 1, 5)
        
        self.assertEqual(node["type"], "VALUE")
        self.assertEqual(node["value"], "42")
        self.assertEqual(node["value_type"], "INTEGER")
        self.assertEqual(node["line"], 1)
        self.assertEqual(node["column"], 5)
    
    def test_make_identifier_node(self):
        """Test _make_identifier_node creates correct structure."""
        node = _make_identifier_node("myVar", 2, 10)
        
        self.assertEqual(node["type"], "IDENTIFIER")
        self.assertEqual(node["name"], "myVar")
        self.assertEqual(node["line"], 2)
        self.assertEqual(node["column"], 10)
    
    def test_make_error_node_with_token_at_pos(self):
        """Test _make_error_node with token available at current pos."""
        parser_state = {
            "tokens": [
                {"type": "PLUS", "value": "+", "line": 3, "column": 7}
            ],
            "pos": 0
        }
        
        node = _make_error_node("Test error", parser_state)
        
        self.assertEqual(node["type"], "ERROR")
        self.assertEqual(node["message"], "Test error")
        self.assertEqual(node["line"], 3)
        self.assertEqual(node["column"], 7)
    
    def test_make_error_node_with_pos_beyond_tokens(self):
        """Test _make_error_node when pos is beyond token list."""
        parser_state = {
            "tokens": [
                {"type": "PLUS", "value": "+", "line": 1, "column": 1}
            ],
            "pos": 10
        }
        
        node = _make_error_node("Test error", parser_state)
        
        self.assertEqual(node["type"], "ERROR")
        self.assertEqual(node["message"], "Test error")
        self.assertEqual(node["line"], 0)
        self.assertEqual(node["column"], 0)
    
    def test_make_error_node_with_empty_tokens(self):
        """Test _make_error_node with empty token list."""
        parser_state = {
            "tokens": [],
            "pos": 0
        }
        
        node = _make_error_node("Test error", parser_state)
        
        self.assertEqual(node["type"], "ERROR")
        self.assertEqual(node["message"], "Test error")
        self.assertEqual(node["line"], 0)
        self.assertEqual(node["column"], 0)


if __name__ == "__main__":
    unittest.main()

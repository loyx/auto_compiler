#!/usr/bin/env python3
"""Unit tests for _parse_expression function."""

import unittest
from unittest.mock import patch

from ._parse_expression_src import _parse_expression


class TestParseExpression(unittest.TestCase):
    """Test cases for _parse_expression function."""

    def test_parse_expression_delegates_to_parse_or(self):
        """Test that _parse_expression correctly delegates to _parse_or."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        expected_ast = {
            "type": "identifier",
            "name": "x",
            "line": 1,
            "column": 1
        }
        
        with patch("._parse_expression_src._parse_or") as mock_parse_or:
            mock_parse_or.return_value = expected_ast
            
            result = _parse_expression(parser_state)
            
            mock_parse_or.assert_called_once_with(parser_state)
            self.assertEqual(result, expected_ast)

    def test_parse_expression_returns_parse_or_result(self):
        """Test that _parse_expression returns exactly what _parse_or returns."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "42", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        mock_result = {
            "type": "literal",
            "value": 42,
            "literal_type": "number",
            "line": 1,
            "column": 1
        }
        
        with patch("._parse_expression_src._parse_or") as mock_parse_or:
            mock_parse_or.return_value = mock_result
            
            result = _parse_expression(parser_state)
            
            self.assertEqual(result, mock_result)

    def test_parse_expression_with_empty_tokens(self):
        """Test _parse_expression with empty token list."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }
        
        expected_ast = {
            "type": "error",
            "value": None,
            "line": 0,
            "column": 0
        }
        
        with patch("._parse_expression_src._parse_or") as mock_parse_or:
            mock_parse_or.return_value = expected_ast
            
            result = _parse_expression(parser_state)
            
            mock_parse_or.assert_called_once_with(parser_state)
            self.assertEqual(result, expected_ast)

    def test_parse_expression_with_pos_not_at_zero(self):
        """Test _parse_expression when pos is not at the beginning."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
            ],
            "pos": 1,
            "filename": "test.py"
        }
        
        expected_ast = {
            "type": "identifier",
            "name": "b",
            "line": 1,
            "column": 5
        }
        
        with patch("._parse_expression_src._parse_or") as mock_parse_or:
            mock_parse_or.return_value = expected_ast
            
            result = _parse_expression(parser_state)
            
            mock_parse_or.assert_called_once_with(parser_state)
            self.assertEqual(result, expected_ast)

    def test_parse_expression_propagates_syntax_error(self):
        """Test that _parse_expression propagates SyntaxError from _parse_or."""
        parser_state = {
            "tokens": [
                {"type": "INVALID", "value": "@", "line": 2, "column": 5}
            ],
            "pos": 0,
            "filename": "error_test.py"
        }
        
        with patch("._parse_expression_src._parse_or") as mock_parse_or:
            mock_parse_or.side_effect = SyntaxError("error_test.py:2:5: Invalid token")
            
            with self.assertRaises(SyntaxError) as context:
                _parse_expression(parser_state)
            
            self.assertIn("Invalid token", str(context.exception))
            mock_parse_or.assert_called_once_with(parser_state)

    def test_parse_expression_with_complex_ast_result(self):
        """Test _parse_expression with a complex nested AST result."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OR", "value": "||", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "y", "line": 1, "column": 6}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        expected_ast = {
            "type": "binary_op",
            "operator": "||",
            "left": {
                "type": "identifier",
                "name": "x",
                "line": 1,
                "column": 1
            },
            "right": {
                "type": "identifier",
                "name": "y",
                "line": 1,
                "column": 6
            },
            "line": 1,
            "column": 1
        }
        
        with patch("._parse_expression_src._parse_or") as mock_parse_or:
            mock_parse_or.return_value = expected_ast
            
            result = _parse_expression(parser_state)
            
            mock_parse_or.assert_called_once_with(parser_state)
            self.assertEqual(result, expected_ast)
            self.assertEqual(result["type"], "binary_op")
            self.assertEqual(result["operator"], "||")

    def test_parse_expression_modifies_parser_state_pos(self):
        """Test that _parse_expression allows _parse_or to modify parser_state['pos']."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "123", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        def mock_parse_or_impl(state):
            state["pos"] = 1
            return {"type": "literal", "value": 123, "line": 1, "column": 1}
        
        with patch("._parse_expression_src._parse_or", side_effect=mock_parse_or_impl):
            result = _parse_expression(parser_state)
            
            self.assertEqual(parser_state["pos"], 1)
            self.assertEqual(result["type"], "literal")

    def test_parse_expression_with_function_call(self):
        """Test _parse_expression with a function call expression."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "foo", "line": 1, "column": 1},
                {"type": "LPAREN", "value": "(", "line": 1, "column": 4},
                {"type": "NUMBER", "value": "1", "line": 1, "column": 5},
                {"type": "RPAREN", "value": ")", "line": 1, "column": 6}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        expected_ast = {
            "type": "call",
            "callee": {
                "type": "identifier",
                "name": "foo",
                "line": 1,
                "column": 1
            },
            "arguments": [
                {
                    "type": "literal",
                    "value": 1,
                    "literal_type": "number",
                    "line": 1,
                    "column": 5
                }
            ],
            "line": 1,
            "column": 1
        }
        
        with patch("._parse_expression_src._parse_or") as mock_parse_or:
            mock_parse_or.return_value = expected_ast
            
            result = _parse_expression(parser_state)
            
            mock_parse_or.assert_called_once_with(parser_state)
            self.assertEqual(result, expected_ast)
            self.assertEqual(result["type"], "call")

    def test_parse_expression_with_unary_operator(self):
        """Test _parse_expression with a unary operator expression."""
        parser_state = {
            "tokens": [
                {"type": "NOT", "value": "!", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "flag", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        expected_ast = {
            "type": "unary_op",
            "operator": "!",
            "operand": {
                "type": "identifier",
                "name": "flag",
                "line": 1,
                "column": 3
            },
            "line": 1,
            "column": 1
        }
        
        with patch("._parse_expression_src._parse_or") as mock_parse_or:
            mock_parse_or.return_value = expected_ast
            
            result = _parse_expression(parser_state)
            
            mock_parse_or.assert_called_once_with(parser_state)
            self.assertEqual(result, expected_ast)
            self.assertEqual(result["type"], "unary_op")

    def test_parse_expression_preserves_parser_state_reference(self):
        """Test that _parse_expression passes the same parser_state object reference."""
        parser_state = {
            "tokens": [
                {"type": "STRING", "value": "hello", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        received_state = None
        
        def capture_state(state):
            nonlocal received_state
            received_state = state
            return {"type": "literal", "value": "hello", "line": 1, "column": 1}
        
        with patch("._parse_expression_src._parse_or", side_effect=capture_state):
            _parse_expression(parser_state)
            
            self.assertIs(received_state, parser_state)


if __name__ == "__main__":
    unittest.main()

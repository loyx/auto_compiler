# -*- coding: utf-8 -*-
"""Unit tests for _parse_expression function."""

import unittest
from unittest.mock import patch

from ._parse_expression_src import _parse_expression, _current_token, _advance, _expect


class TestParseExpression(unittest.TestCase):
    """Test cases for _parse_expression function."""

    def test_parse_expression_delegates_to_logical_or(self):
        """Test that _parse_expression delegates to _parse_logical_or."""
        mock_state = {"tokens": [], "pos": 0}
        mock_result = {"type": "IDENTIFIER", "value": "x"}
        
        with patch("._parse_expression_src._parse_logical_or") as mock_logical_or:
            mock_logical_or.return_value = mock_result
            result = _parse_expression(mock_state)
            
            mock_logical_or.assert_called_once_with(mock_state)
            self.assertEqual(result, mock_result)

    def test_parse_expression_with_complex_expression(self):
        """Test delegation with a complex expression result."""
        mock_state = {"tokens": [{"type": "NUMBER", "value": "1"}], "pos": 0}
        mock_result = {
            "type": "BINARY_OP",
            "value": "+",
            "children": [
                {"type": "LITERAL", "value": 1},
                {"type": "LITERAL", "value": 2}
            ]
        }
        
        with patch("._parse_expression_src._parse_logical_or") as mock_logical_or:
            mock_logical_or.return_value = mock_result
            result = _parse_expression(mock_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "+")


class TestCurrentToken(unittest.TestCase):
    """Test cases for _current_token helper function."""

    def test_current_token_returns_token_at_pos(self):
        """Test getting token at current position."""
        state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 2}
            ],
            "pos": 0
        }
        token = _current_token(state)
        self.assertEqual(token["type"], "NUMBER")
        self.assertEqual(token["value"], "1")

    def test_current_token_returns_token_at_middle_pos(self):
        """Test getting token at middle position."""
        state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 2},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 3}
            ],
            "pos": 1
        }
        token = _current_token(state)
        self.assertEqual(token["type"], "PLUS")
        self.assertEqual(token["value"], "+")

    def test_current_token_returns_none_at_end(self):
        """Test that None is returned when pos is at end."""
        state = {
            "tokens": [{"type": "NUMBER", "value": "1", "line": 1, "column": 1}],
            "pos": 1
        }
        token = _current_token(state)
        self.assertIsNone(token)

    def test_current_token_returns_none_with_empty_tokens(self):
        """Test that None is returned with empty token list."""
        state = {"tokens": [], "pos": 0}
        token = _current_token(state)
        self.assertIsNone(token)

    def test_current_token_with_missing_pos(self):
        """Test behavior when pos is missing from state."""
        state = {"tokens": [{"type": "NUMBER", "value": "1"}]}
        token = _current_token(state)
        self.assertEqual(token["type"], "NUMBER")


class TestAdvance(unittest.TestCase):
    """Test cases for _advance helper function."""

    def test_advance_returns_token_and_increments_pos(self):
        """Test advancing returns token and increments position."""
        state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 2}
            ],
            "pos": 0
        }
        token = _advance(state)
        
        self.assertEqual(token["type"], "NUMBER")
        self.assertEqual(state["pos"], 1)

    def test_advance_multiple_times(self):
        """Test advancing multiple times."""
        state = {
            "tokens": [
                {"type": "NUMBER", "value": "1"},
                {"type": "PLUS", "value": "+"},
                {"type": "NUMBER", "value": "2"}
            ],
            "pos": 0
        }
        
        token1 = _advance(state)
        token2 = _advance(state)
        
        self.assertEqual(token1["value"], "1")
        self.assertEqual(token2["value"], "+")
        self.assertEqual(state["pos"], 2)

    def test_advance_at_end_returns_none(self):
        """Test advancing at end returns None."""
        state = {"tokens": [{"type": "NUMBER", "value": "1"}], "pos": 1}
        token = _advance(state)
        
        self.assertIsNone(token)
        self.assertEqual(state["pos"], 2)


class TestExpect(unittest.TestCase):
    """Test cases for _expect helper function."""

    def test_expect_matches_and_advances(self):
        """Test expect matches token type and advances."""
        state = {
            "tokens": [{"type": "NUMBER", "value": "1", "line": 1, "column": 1}],
            "pos": 0
        }
        token = _expect(state, "NUMBER")
        
        self.assertEqual(token["type"], "NUMBER")
        self.assertEqual(state["pos"], 1)

    def test_expect_matches_value(self):
        """Test expect matches both type and value."""
        state = {
            "tokens": [{"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}],
            "pos": 0
        }
        token = _expect(state, "IDENTIFIER", "x")
        
        self.assertEqual(token["value"], "x")
        self.assertEqual(state["pos"], 1)

    def test_expect_raises_on_none_token(self):
        """Test expect raises SyntaxError when token is None."""
        state = {"tokens": [], "pos": 0}
        
        with self.assertRaises(SyntaxError) as context:
            _expect(state, "NUMBER")
        
        self.assertIn("Unexpected end of input", str(context.exception))

    def test_expect_raises_on_wrong_type(self):
        """Test expect raises SyntaxError on wrong token type."""
        state = {
            "tokens": [{"type": "IDENTIFIER", "value": "x"}],
            "pos": 0
        }
        
        with self.assertRaises(SyntaxError) as context:
            _expect(state, "NUMBER")
        
        self.assertIn("Expected NUMBER", str(context.exception))

    def test_expect_raises_on_wrong_value(self):
        """Test expect raises SyntaxError on wrong token value."""
        state = {
            "tokens": [{"type": "IDENTIFIER", "value": "y"}],
            "pos": 0
        }
        
        with self.assertRaises(SyntaxError) as context:
            _expect(state, "IDENTIFIER", "x")
        
        self.assertIn("Expected 'x'", str(context.exception))


if __name__ == "__main__":
    unittest.main()

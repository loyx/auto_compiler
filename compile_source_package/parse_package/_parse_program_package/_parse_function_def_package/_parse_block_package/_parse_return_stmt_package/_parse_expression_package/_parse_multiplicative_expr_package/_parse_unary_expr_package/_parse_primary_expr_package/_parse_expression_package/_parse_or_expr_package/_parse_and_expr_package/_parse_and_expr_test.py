# -*- coding: utf-8 -*-
"""Unit tests for _parse_and_expr function."""

import unittest
from unittest.mock import patch
from typing import Any, Dict

from ._parse_and_expr_src import _parse_and_expr


class TestParseAndExpr(unittest.TestCase):
    """Test cases for _parse_and_expr function."""

    def test_single_comparison_no_and(self):
        """Test parsing a single comparison expression without AND."""
        mock_comparison = {
            "type": "COMPARISON",
            "value": "x > 5",
            "line": 1,
            "column": 1
        }
        
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("._parse_and_expr_src._parse_comparison", return_value=mock_comparison):
            result = _parse_and_expr(parser_state)
        
        self.assertEqual(result, mock_comparison)
        self.assertEqual(parser_state["pos"], 0)

    def test_single_and_expression(self):
        """Test parsing a single AND expression (a AND b)."""
        left_comparison = {
            "type": "COMPARISON",
            "value": "x > 5",
            "line": 1,
            "column": 1
        }
        right_comparison = {
            "type": "COMPARISON",
            "value": "y < 10",
            "line": 1,
            "column": 10
        }
        and_token = {"type": "KEYWORD", "value": "AND", "line": 1, "column": 6}
        
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                and_token,
                {"type": "IDENTIFIER", "value": "y", "line": 1, "column": 10}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        call_count = [0]
        
        def mock_parse_comparison(state: Dict[str, Any]):
            result = left_comparison if call_count[0] == 0 else right_comparison
            call_count[0] += 1
            return result
        
        with patch("._parse_and_expr_src._parse_comparison", side_effect=mock_parse_comparison):
            with patch("._parse_and_expr_src._is_and_keyword", side_effect=[True, False]):
                with patch("._parse_and_expr_src._consume_token", return_value=and_token):
                    result = _parse_and_expr(parser_state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["operator"], "AND")
        self.assertEqual(len(result["children"]), 2)
        self.assertEqual(result["children"][0], left_comparison)
        self.assertEqual(result["children"][1], right_comparison)
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 6)
        self.assertEqual(parser_state["pos"], 2)

    def test_multiple_and_expressions_left_associative(self):
        """Test parsing multiple AND expressions (a AND b AND c) with left associativity."""
        comparison_a = {
            "type": "COMPARISON",
            "value": "a",
            "line": 1,
            "column": 1
        }
        comparison_b = {
            "type": "COMPARISON",
            "value": "b",
            "line": 1,
            "column": 6
        }
        comparison_c = {
            "type": "COMPARISON",
            "value": "c",
            "line": 1,
            "column": 11
        }
        and_token_1 = {"type": "KEYWORD", "value": "AND", "line": 1, "column": 3}
        and_token_2 = {"type": "KEYWORD", "value": "AND", "line": 1, "column": 8}
        
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                and_token_1,
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 6},
                and_token_2,
                {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 11}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        call_count = [0]
        
        def mock_parse_comparison(state: Dict[str, Any]):
            results = [comparison_a, comparison_b, comparison_c]
            result = results[call_count[0]]
            call_count[0] += 1
            return result
        
        with patch("._parse_and_expr_src._parse_comparison", side_effect=mock_parse_comparison):
            with patch("._parse_and_expr_src._is_and_keyword", side_effect=[True, True, False]):
                with patch("._parse_and_expr_src._consume_token", side_effect=[and_token_1, and_token_2]):
                    result = _parse_and_expr(parser_state)
        
        # Should be left-associative: (a AND b) AND c
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["operator"], "AND")
        self.assertEqual(len(result["children"]), 2)
        
        # Left child should be (a AND b)
        left_child = result["children"][0]
        self.assertEqual(left_child["type"], "BINARY_OP")
        self.assertEqual(left_child["operator"], "AND")
        self.assertEqual(left_child["children"][0], comparison_a)
        self.assertEqual(left_child["children"][1], comparison_b)
        
        # Right child should be c
        self.assertEqual(result["children"][1], comparison_c)
        self.assertEqual(parser_state["pos"], 4)

    def test_empty_tokens(self):
        """Test parsing with empty token list."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }
        
        mock_comparison = {
            "type": "COMPARISON",
            "value": "empty",
            "line": 0,
            "column": 0
        }
        
        with patch("._parse_and_expr_src._parse_comparison", return_value=mock_comparison):
            result = _parse_and_expr(parser_state)
        
        self.assertEqual(result, mock_comparison)
        self.assertEqual(parser_state["pos"], 0)

    def test_pos_at_end_of_tokens(self):
        """Test parsing when pos is already at end of tokens."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 1,
            "filename": "test.py"
        }
        
        mock_comparison = {
            "type": "COMPARISON",
            "value": "x",
            "line": 1,
            "column": 1
        }
        
        with patch("._parse_and_expr_src._parse_comparison", return_value=mock_comparison):
            result = _parse_and_expr(parser_state)
        
        self.assertEqual(result, mock_comparison)
        self.assertEqual(parser_state["pos"], 1)

    def test_and_keyword_not_consumed_when_false(self):
        """Test that AND keyword is not consumed when _is_and_keyword returns False."""
        mock_comparison = {
            "type": "COMPARISON",
            "value": "x",
            "line": 1,
            "column": 1
        }
        
        parser_state = {
            "tokens": [
                {"type": "KEYWORD", "value": "OR", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("._parse_and_expr_src._parse_comparison", return_value=mock_comparison):
            with patch("._parse_and_expr_src._is_and_keyword", return_value=False):
                result = _parse_and_expr(parser_state)
        
        self.assertEqual(result, mock_comparison)
        self.assertEqual(parser_state["pos"], 0)

    def test_parser_state_modified_correctly(self):
        """Test that parser_state pos is modified correctly after consuming tokens."""
        left_comparison = {
            "type": "COMPARISON",
            "value": "left",
            "line": 1,
            "column": 1
        }
        right_comparison = {
            "type": "COMPARISON",
            "value": "right",
            "line": 1,
            "column": 10
        }
        and_token = {"type": "KEYWORD", "value": "AND", "line": 1, "column": 5}
        
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                and_token,
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 10}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        call_count = [0]
        
        def mock_parse_comparison(state: Dict[str, Any]):
            result = left_comparison if call_count[0] == 0 else right_comparison
            call_count[0] += 1
            return result
        
        with patch("._parse_and_expr_src._parse_comparison", side_effect=mock_parse_comparison):
            with patch("._parse_and_expr_src._is_and_keyword", side_effect=[True, False]):
                with patch("._parse_and_expr_src._consume_token", return_value=and_token):
                    result = _parse_and_expr(parser_state)
        
        self.assertEqual(parser_state["pos"], 1)


class TestIsAndKeyword(unittest.TestCase):
    """Test cases for _is_and_keyword helper function."""

    def test_is_and_keyword_true(self):
        """Test _is_and_keyword returns True for AND keyword."""
        from ._parse_and_expr_src import _is_and_keyword
        
        parser_state = {
            "tokens": [
                {"type": "KEYWORD", "value": "AND", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _is_and_keyword(parser_state)
        self.assertTrue(result)

    def test_is_and_keyword_false_different_value(self):
        """Test _is_and_keyword returns False for non-AND keyword."""
        from ._parse_and_expr_src import _is_and_keyword
        
        parser_state = {
            "tokens": [
                {"type": "KEYWORD", "value": "OR", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _is_and_keyword(parser_state)
        self.assertFalse(result)

    def test_is_and_keyword_false_different_type(self):
        """Test _is_and_keyword returns False for non-KEYWORD type."""
        from ._parse_and_expr_src import _is_and_keyword
        
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "AND", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _is_and_keyword(parser_state)
        self.assertFalse(result)

    def test_is_and_keyword_empty_tokens(self):
        """Test _is_and_keyword returns False for empty tokens."""
        from ._parse_and_expr_src import _is_and_keyword
        
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _is_and_keyword(parser_state)
        self.assertFalse(result)

    def test_is_and_keyword_pos_at_end(self):
        """Test _is_and_keyword returns False when pos is at end."""
        from ._parse_and_expr_src import _is_and_keyword
        
        parser_state = {
            "tokens": [
                {"type": "KEYWORD", "value": "AND", "line": 1, "column": 1}
            ],
            "pos": 1,
            "filename": "test.py"
        }
        
        result = _is_and_keyword(parser_state)
        self.assertFalse(result)

    def test_is_and_keyword_pos_beyond_end(self):
        """Test _is_and_keyword returns False when pos is beyond end."""
        from ._parse_and_expr_src import _is_and_keyword
        
        parser_state = {
            "tokens": [
                {"type": "KEYWORD", "value": "AND", "line": 1, "column": 1}
            ],
            "pos": 5,
            "filename": "test.py"
        }
        
        result = _is_and_keyword(parser_state)
        self.assertFalse(result)


class TestConsumeToken(unittest.TestCase):
    """Test cases for _consume_token helper function."""

    def test_consume_token_success(self):
        """Test _consume_token successfully consumes and returns token."""
        from ._parse_and_expr_src import _consume_token
        
        token = {"type": "KEYWORD", "value": "AND", "line": 1, "column": 1}
        parser_state = {
            "tokens": [token],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _consume_token(parser_state)
        
        self.assertEqual(result, token)
        self.assertEqual(parser_state["pos"], 1)

    def test_consume_token_empty_tokens(self):
        """Test _consume_token raises SyntaxError for empty tokens."""
        from ._parse_and_expr_src import _consume_token
        
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))
        self.assertIn("test.py", str(context.exception))

    def test_consume_token_pos_at_end(self):
        """Test _consume_token raises SyntaxError when pos is at end."""
        from ._parse_and_expr_src import _consume_token
        
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 1,
            "filename": "test.py"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))

    def test_consume_token_pos_beyond_end(self):
        """Test _consume_token raises SyntaxError when pos is beyond end."""
        from ._parse_and_expr_src import _consume_token
        
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 10,
            "filename": "test.py"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))


if __name__ == "__main__":
    unittest.main()

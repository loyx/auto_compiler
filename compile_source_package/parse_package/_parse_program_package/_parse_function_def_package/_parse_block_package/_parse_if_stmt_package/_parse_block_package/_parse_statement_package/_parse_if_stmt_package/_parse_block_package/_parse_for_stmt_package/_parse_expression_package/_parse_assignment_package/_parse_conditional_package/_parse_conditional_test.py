# -*- coding: utf-8 -*-
"""Unit tests for _parse_conditional function."""

import unittest
from unittest.mock import patch

from ._parse_conditional_src import _parse_conditional


class TestParseConditional(unittest.TestCase):
    """Test cases for _parse_conditional parser function."""

    def setUp(self):
        """Set up test fixtures."""
        self.maxDiff = None

    def test_no_ternary_returns_condition(self):
        """Test when there is no '?' token, returns condition directly."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 3},
            ],
            "filename": "test.c",
            "pos": 0,
            "error": ""
        }
        
        mock_condition = {
            "type": "IDENTIFIER",
            "value": "a",
            "line": 1,
            "column": 1
        }
        
        with patch("._parse_or_package._parse_or_src._parse_or") as mock_parse_or:
            mock_parse_or.return_value = mock_condition
            
            result = _parse_conditional(parser_state)
            
            self.assertEqual(result, mock_condition)
            mock_parse_or.assert_called_once_with(parser_state)
            self.assertEqual(parser_state["pos"], 0)

    def test_ternary_expression_parsed(self):
        """Test parsing a valid ternary expression: a ? b : c"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "QUESTION", "value": "?", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
                {"type": "COLON", "value": ":", "line": 1, "column": 7},
                {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 9},
            ],
            "filename": "test.c",
            "pos": 0,
            "error": ""
        }
        
        condition_node = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        true_expr_node = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
        false_expr_node = {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 9}
        
        with patch("._parse_or_package._parse_or_src._parse_or") as mock_parse_or:
            mock_parse_or.side_effect = [condition_node, true_expr_node, false_expr_node]
            
            result = _parse_conditional(parser_state)
            
            expected = {
                "type": "CONDITIONAL",
                "condition": condition_node,
                "true_expr": true_expr_node,
                "false_expr": false_expr_node,
                "line": 1,
                "column": 3
            }
            
            self.assertEqual(result, expected)
            self.assertEqual(parser_state["pos"], 5)
            self.assertEqual(mock_parse_or.call_count, 3)

    def test_nested_ternary_right_associative(self):
        """Test nested ternary is right-associative: a ? b : c ? d : e"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "QUESTION", "value": "?", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
                {"type": "COLON", "value": ":", "line": 1, "column": 7},
                {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 9},
                {"type": "QUESTION", "value": "?", "line": 1, "column": 11},
                {"type": "IDENTIFIER", "value": "d", "line": 1, "column": 13},
                {"type": "COLON", "value": ":", "line": 1, "column": 15},
                {"type": "IDENTIFIER", "value": "e", "line": 1, "column": 17},
            ],
            "filename": "test.c",
            "pos": 0,
            "error": ""
        }
        
        a_node = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        b_node = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
        c_node = {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 9}
        d_node = {"type": "IDENTIFIER", "value": "d", "line": 1, "column": 13}
        e_node = {"type": "IDENTIFIER", "value": "e", "line": 1, "column": 17}
        
        inner_conditional = {
            "type": "CONDITIONAL",
            "condition": c_node,
            "true_expr": d_node,
            "false_expr": e_node,
            "line": 1,
            "column": 11
        }
        
        with patch("._parse_or_package._parse_or_src._parse_or") as mock_parse_or:
            mock_parse_or.side_effect = [a_node, b_node, c_node, d_node, e_node]
            
            result = _parse_conditional(parser_state)
            
            expected = {
                "type": "CONDITIONAL",
                "condition": a_node,
                "true_expr": b_node,
                "false_expr": inner_conditional,
                "line": 1,
                "column": 3
            }
            
            self.assertEqual(result, expected)
            self.assertEqual(parser_state["pos"], 10)

    def test_missing_colon_raises_error(self):
        """Test that missing ':' after true expression raises error."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "QUESTION", "value": "?", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
            ],
            "filename": "test.c",
            "pos": 0,
            "error": ""
        }
        
        condition_node = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        true_expr_node = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
        
        with patch("._parse_or_package._parse_or_src._parse_or") as mock_parse_or:
            mock_parse_or.side_effect = [condition_node, true_expr_node]
            
            with patch("._raise_error_package._raise_error_src._raise_error") as mock_raise:
                mock_raise.side_effect = SyntaxError("Expected ':' after conditional expression")
                
                with self.assertRaises(SyntaxError):
                    _parse_conditional(parser_state)
                
                mock_raise.assert_called_once()
                args, kwargs = mock_raise.call_args
                self.assertEqual(args[0], parser_state)
                self.assertEqual(args[1], "Expected ':' after conditional expression")

    def test_tokens_exhausted_after_question(self):
        """Test when tokens end after '?' without true expression."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "QUESTION", "value": "?", "line": 1, "column": 3},
            ],
            "filename": "test.c",
            "pos": 0,
            "error": ""
        }
        
        condition_node = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        
        with patch("._parse_or_package._parse_or_src._parse_or") as mock_parse_or:
            mock_parse_or.side_effect = [condition_node]
            
            with patch("._raise_error_package._raise_error_src._raise_error") as mock_raise:
                mock_raise.side_effect = SyntaxError("Expected ':' after conditional expression")
                
                with self.assertRaises(SyntaxError):
                    _parse_conditional(parser_state)

    def test_wrong_token_after_true_expr(self):
        """Test when token after true expression is not ':'."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "QUESTION", "value": "?", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
                {"type": "SEMICOLON", "value": ";", "line": 1, "column": 7},
            ],
            "filename": "test.c",
            "pos": 0,
            "error": ""
        }
        
        condition_node = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        true_expr_node = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
        
        with patch("._parse_or_package._parse_or_src._parse_or") as mock_parse_or:
            mock_parse_or.side_effect = [condition_node, true_expr_node]
            
            with patch("._raise_error_package._raise_error_src._raise_error") as mock_raise:
                mock_raise.side_effect = SyntaxError("Expected ':' after conditional expression")
                
                with self.assertRaises(SyntaxError):
                    _parse_conditional(parser_state)
                
                mock_raise.assert_called_once()

    def test_empty_tokens_returns_condition(self):
        """Test when tokens list is empty."""
        parser_state = {
            "tokens": [],
            "filename": "test.c",
            "pos": 0,
            "error": ""
        }
        
        mock_condition = {"type": "NUMBER", "value": "42", "line": 1, "column": 1}
        
        with patch("._parse_or_package._parse_or_src._parse_or") as mock_parse_or:
            mock_parse_or.return_value = mock_condition
            
            result = _parse_conditional(parser_state)
            
            self.assertEqual(result, mock_condition)
            self.assertEqual(parser_state["pos"], 0)

    def test_position_at_end_returns_condition(self):
        """Test when pos is already at end of tokens."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            ],
            "filename": "test.c",
            "pos": 1,
            "error": ""
        }
        
        mock_condition = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        
        with patch("._parse_or_package._parse_or_src._parse_or") as mock_parse_or:
            mock_parse_or.return_value = mock_condition
            
            result = _parse_conditional(parser_state)
            
            self.assertEqual(result, mock_condition)
            self.assertEqual(parser_state["pos"], 1)

    def test_complex_expression_as_condition(self):
        """Test with complex expression as condition."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "y", "line": 1, "column": 5},
                {"type": "QUESTION", "value": "?", "line": 1, "column": 7},
                {"type": "NUMBER", "value": "1", "line": 1, "column": 9},
                {"type": "COLON", "value": ":", "line": 1, "column": 11},
                {"type": "NUMBER", "value": "0", "line": 1, "column": 13},
            ],
            "filename": "test.c",
            "pos": 0,
            "error": ""
        }
        
        condition_node = {
            "type": "BINARY_OP",
            "left": {"type": "IDENTIFIER", "value": "x"},
            "right": {"type": "IDENTIFIER", "value": "y"},
            "line": 1,
            "column": 1
        }
        true_expr_node = {"type": "NUMBER", "value": "1", "line": 1, "column": 9}
        false_expr_node = {"type": "NUMBER", "value": "0", "line": 1, "column": 13}
        
        with patch("._parse_or_package._parse_or_src._parse_or") as mock_parse_or:
            mock_parse_or.side_effect = [condition_node, true_expr_node, false_expr_node]
            
            result = _parse_conditional(parser_state)
            
            expected = {
                "type": "CONDITIONAL",
                "condition": condition_node,
                "true_expr": true_expr_node,
                "false_expr": false_expr_node,
                "line": 1,
                "column": 7
            }
            
            self.assertEqual(result, expected)
            self.assertEqual(parser_state["pos"], 7)


if __name__ == "__main__":
    unittest.main()

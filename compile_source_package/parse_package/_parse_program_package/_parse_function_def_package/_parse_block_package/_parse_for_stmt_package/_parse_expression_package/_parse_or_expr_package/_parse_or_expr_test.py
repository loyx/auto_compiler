#!/usr/bin/env python3
"""Unit tests for _parse_or_expr function."""

import unittest
from unittest.mock import patch

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))))))))))
from ._parse_or_expr_src import _parse_or_expr


class TestParseOrExpr(unittest.TestCase):
    """Test cases for _parse_or_expr function."""

    def test_single_and_expr_no_or(self):
        """Test parsing a single and_expr without any 'or' operators."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        mock_and_expr_result = {
            "type": "IDENTIFIER",
            "value": "a",
            "line": 1,
            "column": 1
        }
        
        with patch('._parse_and_expr_package._parse_and_expr_src._parse_and_expr') as mock_parse_and:
            mock_parse_and.return_value = mock_and_expr_result
            
            result = _parse_or_expr(parser_state)
            
            self.assertEqual(result, mock_and_expr_result)
            self.assertEqual(parser_state["pos"], 0)
            mock_parse_and.assert_called_once_with(parser_state)

    def test_two_and_exprs_with_or(self):
        """Test parsing 'a or b' - two and_exprs connected by 'or'."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "OR", "value": "or", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        left_operand = {
            "type": "IDENTIFIER",
            "value": "a",
            "line": 1,
            "column": 1
        }
        
        right_operand = {
            "type": "IDENTIFIER",
            "value": "b",
            "line": 1,
            "column": 5
        }
        
        with patch('._parse_and_expr_package._parse_and_expr_src._parse_and_expr') as mock_parse_and:
            mock_parse_and.side_effect = [left_operand, right_operand]
            
            result = _parse_or_expr(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "or")
            self.assertEqual(len(result["children"]), 2)
            self.assertEqual(result["children"][0], left_operand)
            self.assertEqual(result["children"][1], right_operand)
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            self.assertEqual(parser_state["pos"], 2)
            self.assertEqual(mock_parse_and.call_count, 2)

    def test_multiple_or_expressions_left_associative(self):
        """Test parsing 'a or b or c' - verifies left-associativity."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "OR", "value": "or", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
                {"type": "OR", "value": "or", "line": 1, "column": 7},
                {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 9}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        call_count = [0]
        
        def side_effect(state):
            call_count[0] += 1
            if call_count[0] == 1:
                return {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
            elif call_count[0] == 2:
                return {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
            else:
                return {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 9}
        
        with patch('._parse_and_expr_package._parse_and_expr_src._parse_and_expr') as mock_parse_and:
            mock_parse_and.side_effect = side_effect
            
            result = _parse_or_expr(parser_state)
            
            # Should be left-associative: (a or b) or c
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "or")
            self.assertEqual(len(result["children"]), 2)
            
            # Right child should be 'c'
            right_child = result["children"][1]
            self.assertEqual(right_child["type"], "IDENTIFIER")
            self.assertEqual(right_child["value"], "c")
            
            # Left child should be (a or b)
            left_child = result["children"][0]
            self.assertEqual(left_child["type"], "BINARY_OP")
            self.assertEqual(left_child["value"], "or")
            self.assertEqual(len(left_child["children"]), 2)
            self.assertEqual(left_child["children"][0]["value"], "a")
            self.assertEqual(left_child["children"][1]["value"], "b")
            
            # Line/column from leftmost operand
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            
            # pos should be at 4 (consumed 5 tokens: a, or, b, or, c)
            self.assertEqual(parser_state["pos"], 4)
            self.assertEqual(mock_parse_and.call_count, 3)

    def test_empty_tokens(self):
        """Test parsing with empty token list."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }
        
        mock_result = {"type": "LITERAL", "value": None, "line": 0, "column": 0}
        
        with patch('._parse_and_expr_package._parse_and_expr_src._parse_and_expr') as mock_parse_and:
            mock_parse_and.return_value = mock_result
            
            result = _parse_or_expr(parser_state)
            
            self.assertEqual(result, mock_result)
            self.assertEqual(parser_state["pos"], 0)

    def test_pos_at_end_of_tokens(self):
        """Test parsing when position is already at end of tokens."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
            ],
            "pos": 1,
            "filename": "test.py"
        }
        
        mock_result = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        
        with patch('._parse_and_expr_package._parse_and_expr_src._parse_and_expr') as mock_parse_and:
            mock_parse_and.return_value = mock_result
            
            result = _parse_or_expr(parser_state)
            
            self.assertEqual(result, mock_result)
            self.assertEqual(parser_state["pos"], 1)

    def test_or_token_at_end(self):
        """Test parsing when OR token is at the end without right operand."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "OR", "value": "or", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        left_operand = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        right_operand = {"type": "LITERAL", "value": None, "line": 0, "column": 0}
        
        with patch('._parse_and_expr_package._parse_and_expr_src._parse_and_expr') as mock_parse_and:
            mock_parse_and.side_effect = [left_operand, right_operand]
            
            result = _parse_or_expr(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "or")
            self.assertEqual(len(result["children"]), 2)
            self.assertEqual(parser_state["pos"], 2)

    def test_line_column_preserved_from_left_operand(self):
        """Test that line and column are preserved from left operand."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 5, "column": 10},
                {"type": "OR", "value": "or", "line": 5, "column": 12},
                {"type": "IDENTIFIER", "value": "y", "line": 5, "column": 14}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        left_operand = {"type": "IDENTIFIER", "value": "x", "line": 5, "column": 10}
        right_operand = {"type": "IDENTIFIER", "value": "y", "line": 5, "column": 14}
        
        with patch('._parse_and_expr_package._parse_and_expr_src._parse_and_expr') as mock_parse_and:
            mock_parse_and.side_effect = [left_operand, right_operand]
            
            result = _parse_or_expr(parser_state)
            
            self.assertEqual(result["line"], 5)
            self.assertEqual(result["column"], 10)

    def test_pos_updated_correctly(self):
        """Test that parser_state pos is updated correctly after parsing."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "OR", "value": "or", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
                {"type": "OR", "value": "or", "line": 1, "column": 7},
                {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 9}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        call_count = [0]
        
        def side_effect(state):
            call_count[0] += 1
            if call_count[0] == 1:
                return {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
            elif call_count[0] == 2:
                return {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
            else:
                return {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 9}
        
        with patch('._parse_and_expr_package._parse_and_expr_src._parse_and_expr') as mock_parse_and:
            mock_parse_and.side_effect = side_effect
            
            result = _parse_or_expr(parser_state)
            
            # Should consume all 5 tokens: a, or, b, or, c
            # pos should be 4 (0-indexed, pointing past last token)
            self.assertEqual(parser_state["pos"], 4)


if __name__ == '__main__':
    unittest.main()

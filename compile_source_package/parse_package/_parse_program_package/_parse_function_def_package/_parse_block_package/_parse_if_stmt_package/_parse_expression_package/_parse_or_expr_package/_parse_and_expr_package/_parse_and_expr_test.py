# -*- coding: utf-8 -*-
"""Unit tests for _parse_and_expr function."""

import unittest
from unittest.mock import patch, MagicMock
from typing import Any, Dict

# Mock the entire dependency chain before importing _parse_and_expr
import sys
from unittest.mock import MagicMock

# Create mock modules for the entire dependency chain
mock_primary_expr = MagicMock()
mock_primary_expr._parse_primary_expr = MagicMock(return_value={"type": "EMPTY", "value": None, "line": 0, "column": 0})

mock_unary_expr = MagicMock()
mock_unary_expr._parse_unary_expr = MagicMock(return_value={"type": "EMPTY", "value": None, "line": 0, "column": 0})

mock_multiplicative_expr = MagicMock()
mock_multiplicative_expr._parse_multiplicative_expr = MagicMock(return_value={"type": "EMPTY", "value": None, "line": 0, "column": 0})

mock_additive_expr = MagicMock()
mock_additive_expr._parse_additive_expr = MagicMock(return_value={"type": "EMPTY", "value": None, "line": 0, "column": 0})

mock_comparison_expr = MagicMock()
mock_comparison_expr._parse_comparison_expr = MagicMock(return_value={"type": "EMPTY", "value": None, "line": 0, "column": 0})

# Register mock modules in sys.modules to prevent actual imports
base_path = "._parse_comparison_expr_package._parse_additive_expr_package._parse_multiplicative_expr_package._parse_unary_expr_package"
sys.modules[f"{base_path}._parse_primary_expr_package"] = MagicMock()
sys.modules[f"{base_path}._parse_primary_expr_package._parse_primary_expr_src"] = mock_primary_expr

sys.modules[f"{base_path}"] = MagicMock()
sys.modules[f"{base_path}._parse_unary_expr_src"] = mock_unary_expr

sys.modules[f"{base_path}._parse_multiplicative_expr_package"] = MagicMock()
sys.modules[f"{base_path}._parse_multiplicative_expr_package._parse_multiplicative_expr_src"] = mock_multiplicative_expr

sys.modules[f"._parse_comparison_expr_package._parse_additive_expr_package"] = MagicMock()
sys.modules[f"._parse_comparison_expr_package._parse_additive_expr_package._parse_additive_expr_src"] = mock_additive_expr

sys.modules[f"._parse_comparison_expr_package"] = MagicMock()
sys.modules[f"._parse_comparison_expr_package._parse_comparison_expr_src"] = mock_comparison_expr

from ._parse_and_expr_src import _parse_and_expr
import _parse_and_expr_src


class TestParseAndExpr(unittest.TestCase):
    """Test cases for _parse_and_expr function."""

    def _create_token(self, token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """Helper to create a token dictionary."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def _create_parser_state(self, tokens: list, pos: int = 0, filename: str = "test.py") -> Dict[str, Any]:
        """Helper to create a parser state dictionary."""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename
        }

    def test_single_expression_no_and(self):
        """Test parsing a single expression without && operator."""
        tokens = [
            self._create_token("IDENTIFIER", "x", 1, 1),
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        mock_left = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        
        call_count = [0]
        def mock_comparison_impl(state):
            call_count[0] += 1
            state["pos"] = 1
            return mock_left
        
        with patch.object(_parse_and_expr_src, '_parse_comparison_expr') as mock_parse_comparison:
            mock_parse_comparison.side_effect = mock_comparison_impl
            
            result = _parse_and_expr(parser_state)
            
            self.assertEqual(result, mock_left)
            self.assertEqual(parser_state["pos"], 1)
            mock_parse_comparison.assert_called_once()

    def test_single_and_operator(self):
        """Test parsing expression with one && operator."""
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("OPERATOR", "&&", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 6),
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        mock_left = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        mock_right = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 6}
        
        call_count = [0]
        def mock_comparison_impl(state):
            call_count[0] += 1
            if call_count[0] == 1:
                state["pos"] = 1
                return mock_left
            else:
                state["pos"] = 3
                return mock_right
        
        with patch.object(_parse_and_expr_src, '_parse_comparison_expr') as mock_parse_comparison:
            mock_parse_comparison.side_effect = mock_comparison_impl
            
            result = _parse_and_expr(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["operator"], "&&")
            self.assertEqual(result["left"], mock_left)
            self.assertEqual(result["right"], mock_right)
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 3)
            self.assertEqual(parser_state["pos"], 3)
            self.assertEqual(mock_parse_comparison.call_count, 2)

    def test_multiple_and_operators_left_associative(self):
        """Test parsing expression with multiple && operators (left-associativity)."""
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("OPERATOR", "&&", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 6),
            self._create_token("OPERATOR", "&&", 1, 8),
            self._create_token("IDENTIFIER", "c", 1, 11),
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        mock_a = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        mock_b = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 6}
        mock_c = {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 11}
        
        call_count = [0]
        def mock_comparison_impl(state):
            call_count[0] += 1
            if call_count[0] == 1:
                state["pos"] = 1
                return mock_a
            elif call_count[0] == 2:
                state["pos"] = 3
                return mock_b
            else:
                state["pos"] = 5
                return mock_c
        
        with patch.object(_parse_and_expr_src, '_parse_comparison_expr') as mock_parse_comparison:
            mock_parse_comparison.side_effect = mock_comparison_impl
            
            result = _parse_and_expr(parser_state)
            
            # Should be left-associative: (a && b) && c
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["operator"], "&&")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 8)
            
            # Left side should be (a && b)
            left_node = result["left"]
            self.assertEqual(left_node["type"], "BINARY_OP")
            self.assertEqual(left_node["operator"], "&&")
            self.assertEqual(left_node["left"], mock_a)
            self.assertEqual(left_node["right"], mock_b)
            self.assertEqual(left_node["line"], 1)
            self.assertEqual(left_node["column"], 3)
            
            # Right side should be c
            self.assertEqual(result["right"], mock_c)
            
            self.assertEqual(parser_state["pos"], 5)
            self.assertEqual(mock_parse_comparison.call_count, 3)

    def test_and_followed_by_non_and_operator(self):
        """Test parsing && followed by a different operator (should stop)."""
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("OPERATOR", "&&", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 6),
            self._create_token("OPERATOR", "||", 1, 8),
            self._create_token("IDENTIFIER", "c", 1, 11),
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        mock_a = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        mock_b = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 6}
        
        call_count = [0]
        def mock_comparison_impl(state):
            call_count[0] += 1
            if call_count[0] == 1:
                state["pos"] = 1
                return mock_a
            else:
                state["pos"] = 3
                return mock_b
        
        with patch.object(_parse_and_expr_src, '_parse_comparison_expr') as mock_parse_comparison:
            mock_parse_comparison.side_effect = mock_comparison_impl
            
            result = _parse_and_expr(parser_state)
            
            # Should parse a && b, then stop at ||
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["operator"], "&&")
            self.assertEqual(result["left"], mock_a)
            self.assertEqual(result["right"], mock_b)
            self.assertEqual(parser_state["pos"], 3)
            self.assertEqual(mock_parse_comparison.call_count, 2)

    def test_empty_tokens(self):
        """Test parsing with empty tokens list."""
        parser_state = self._create_parser_state([], pos=0)
        
        mock_empty = {"type": "EMPTY", "value": None, "line": 0, "column": 0}
        
        call_count = [0]
        def mock_comparison_impl(state):
            call_count[0] += 1
            state["pos"] = 0
            return mock_empty
        
        with patch.object(_parse_and_expr_src, '_parse_comparison_expr') as mock_parse_comparison:
            mock_parse_comparison.side_effect = mock_comparison_impl
            
            result = _parse_and_expr(parser_state)
            
            self.assertEqual(result, mock_empty)
            self.assertEqual(parser_state["pos"], 0)

    def test_position_at_end_of_tokens(self):
        """Test parsing when position is already at end of tokens."""
        tokens = [
            self._create_token("IDENTIFIER", "x", 1, 1),
        ]
        parser_state = self._create_parser_state(tokens, pos=1)
        
        mock_x = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        
        call_count = [0]
        def mock_comparison_impl(state):
            call_count[0] += 1
            state["pos"] = 1
            return mock_x
        
        with patch.object(_parse_and_expr_src, '_parse_comparison_expr') as mock_parse_comparison:
            mock_parse_comparison.side_effect = mock_comparison_impl
            
            result = _parse_and_expr(parser_state)
            
            self.assertEqual(result, mock_x)
            self.assertEqual(parser_state["pos"], 1)

    def test_comparison_expr_raises_error(self):
        """Test that errors from _parse_comparison_expr are propagated."""
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        with patch.object(_parse_and_expr_src, '_parse_comparison_expr') as mock_parse_comparison:
            mock_parse_comparison.side_effect = SyntaxError("Invalid expression")
            
            with self.assertRaises(SyntaxError) as context:
                _parse_and_expr(parser_state)
            
            self.assertEqual(str(context.exception), "Invalid expression")

    def test_token_without_type_field(self):
        """Test parsing when token doesn't have type field."""
        tokens = [
            {"value": "a", "line": 1, "column": 1},  # Missing "type"
            {"type": "OPERATOR", "value": "&&", "line": 1, "column": 3},
            {"value": "b", "line": 1, "column": 6},
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        mock_a = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        
        call_count = [0]
        def mock_comparison_impl(state):
            call_count[0] += 1
            state["pos"] = 1
            return mock_a
        
        with patch.object(_parse_and_expr_src, '_parse_comparison_expr') as mock_parse_comparison:
            mock_parse_comparison.side_effect = mock_comparison_impl
            
            result = _parse_and_expr(parser_state)
            
            # Should not enter the && loop since first token has no type
            self.assertEqual(result, mock_a)
            self.assertEqual(parser_state["pos"], 1)

    def test_token_without_value_field(self):
        """Test parsing when token doesn't have value field."""
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            {"type": "OPERATOR", "line": 1, "column": 3},  # Missing "value"
            self._create_token("IDENTIFIER", "b", 1, 6),
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        mock_a = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        
        call_count = [0]
        def mock_comparison_impl(state):
            call_count[0] += 1
            state["pos"] = 1
            return mock_a
        
        with patch.object(_parse_and_expr_src, '_parse_comparison_expr') as mock_parse_comparison:
            mock_parse_comparison.side_effect = mock_comparison_impl
            
            result = _parse_and_expr(parser_state)
            
            # Should not enter the && loop since operator token has no value
            self.assertEqual(result, mock_a)
            self.assertEqual(parser_state["pos"], 1)

    def test_and_operator_different_line(self):
        """Test that line/column info is preserved from operator token."""
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("OPERATOR", "&&", 2, 5),  # Different line
            self._create_token("IDENTIFIER", "b", 3, 10),
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        mock_a = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        mock_b = {"type": "IDENTIFIER", "value": "b", "line": 3, "column": 10}
        
        call_count = [0]
        def mock_comparison_impl(state):
            call_count[0] += 1
            if call_count[0] == 1:
                state["pos"] = 1
                return mock_a
            else:
                state["pos"] = 3
                return mock_b
        
        with patch.object(_parse_and_expr_src, '_parse_comparison_expr') as mock_parse_comparison:
            mock_parse_comparison.side_effect = mock_comparison_impl
            
            result = _parse_and_expr(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["operator"], "&&")
            self.assertEqual(result["line"], 2)  # From && token
            self.assertEqual(result["column"], 5)  # From && token


if __name__ == "__main__":
    unittest.main()

# -*- coding: utf-8 -*-
"""Unit tests for _parse_unary function."""

import unittest
from unittest.mock import patch

from ._parse_unary_src import _parse_unary


class TestParseUnary(unittest.TestCase):
    """Test cases for _parse_unary function."""

    def test_minus_operator(self):
        """Test parsing MINUS unary operator."""
        parser_state = {
            "tokens": [
                {"type": "MINUS", "value": "-", "line": 1, "column": 5},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 6}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("._parse_primary_package._parse_primary_src._parse_primary") as mock_parse_primary:
            mock_parse_primary.return_value = {
                "type": "IDENTIFIER",
                "value": "x",
                "children": [],
                "line": 1,
                "column": 6
            }
            
            result = _parse_unary(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "-")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 5)
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(parser_state["pos"], 1)
            mock_parse_primary.assert_called_once()

    def test_not_operator(self):
        """Test parsing NOT unary operator."""
        parser_state = {
            "tokens": [
                {"type": "NOT", "value": "not", "line": 2, "column": 10},
                {"type": "IDENTIFIER", "value": "flag", "line": 2, "column": 14}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("._parse_primary_package._parse_primary_src._parse_primary") as mock_parse_primary:
            mock_parse_primary.return_value = {
                "type": "IDENTIFIER",
                "value": "flag",
                "children": [],
                "line": 2,
                "column": 14
            }
            
            result = _parse_unary(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "not")
            self.assertEqual(result["line"], 2)
            self.assertEqual(result["column"], 10)
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(parser_state["pos"], 1)

    def test_chained_minus(self):
        """Test parsing chained MINUS operators (--x)."""
        parser_state = {
            "tokens": [
                {"type": "MINUS", "value": "-", "line": 1, "column": 1},
                {"type": "MINUS", "value": "-", "line": 1, "column": 2},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("._parse_primary_package._parse_primary_src._parse_primary") as mock_parse_primary:
            mock_parse_primary.return_value = {
                "type": "IDENTIFIER",
                "value": "x",
                "children": [],
                "line": 1,
                "column": 3
            }
            
            result = _parse_unary(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "-")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            self.assertEqual(len(result["children"]), 1)
            
            inner_node = result["children"][0]
            self.assertEqual(inner_node["type"], "UNARY_OP")
            self.assertEqual(inner_node["value"], "-")
            self.assertEqual(inner_node["line"], 1)
            self.assertEqual(inner_node["column"], 2)
            self.assertEqual(parser_state["pos"], 2)

    def test_chained_not(self):
        """Test parsing chained NOT operators (not not x)."""
        parser_state = {
            "tokens": [
                {"type": "NOT", "value": "not", "line": 1, "column": 1},
                {"type": "NOT", "value": "not", "line": 1, "column": 5},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 9}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("._parse_primary_package._parse_primary_src._parse_primary") as mock_parse_primary:
            mock_parse_primary.return_value = {
                "type": "IDENTIFIER",
                "value": "x",
                "children": [],
                "line": 1,
                "column": 9
            }
            
            result = _parse_unary(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "not")
            self.assertEqual(len(result["children"]), 1)
            
            inner_node = result["children"][0]
            self.assertEqual(inner_node["type"], "UNARY_OP")
            self.assertEqual(inner_node["value"], "not")
            self.assertEqual(parser_state["pos"], 2)

    def test_mixed_chained_unary(self):
        """Test parsing mixed chained unary operators (-not x)."""
        parser_state = {
            "tokens": [
                {"type": "MINUS", "value": "-", "line": 1, "column": 1},
                {"type": "NOT", "value": "not", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 7}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("._parse_primary_package._parse_primary_src._parse_primary") as mock_parse_primary:
            mock_parse_primary.return_value = {
                "type": "IDENTIFIER",
                "value": "x",
                "children": [],
                "line": 1,
                "column": 7
            }
            
            result = _parse_unary(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "-")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            
            inner_node = result["children"][0]
            self.assertEqual(inner_node["type"], "UNARY_OP")
            self.assertEqual(inner_node["value"], "not")
            self.assertEqual(inner_node["line"], 1)
            self.assertEqual(inner_node["column"], 3)
            self.assertEqual(parser_state["pos"], 2)

    def test_non_unary_token_delegates_to_primary(self):
        """Test that non-unary tokens delegate to _parse_primary."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 2}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        expected_primary_result = {
            "type": "IDENTIFIER",
            "value": "x",
            "children": [],
            "line": 1,
            "column": 1
        }
        
        with patch("._parse_primary_package._parse_primary_src._parse_primary") as mock_parse_primary:
            mock_parse_primary.return_value = expected_primary_result
            
            result = _parse_unary(parser_state)
            
            self.assertEqual(result, expected_primary_result)
            self.assertEqual(parser_state["pos"], 0)
            mock_parse_primary.assert_called_once_with(parser_state)

    def test_empty_tokens_list(self):
        """Test parsing with empty tokens list."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }
        
        expected_primary_result = {
            "type": "LITERAL",
            "value": None,
            "children": [],
            "line": 0,
            "column": 0
        }
        
        with patch("._parse_primary_package._parse_primary_src._parse_primary") as mock_parse_primary:
            mock_parse_primary.return_value = expected_primary_result
            
            result = _parse_unary(parser_state)
            
            self.assertEqual(result, expected_primary_result)
            mock_parse_primary.assert_called_once()

    def test_pos_beyond_tokens_length(self):
        """Test when pos is beyond tokens length."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 5,
            "filename": "test.py"
        }
        
        expected_primary_result = {
            "type": "LITERAL",
            "value": None,
            "children": [],
            "line": 0,
            "column": 0
        }
        
        with patch("._parse_primary_package._parse_primary_src._parse_primary") as mock_parse_primary:
            mock_parse_primary.return_value = expected_primary_result
            
            result = _parse_unary(parser_state)
            
            self.assertEqual(result, expected_primary_result)
            mock_parse_primary.assert_called_once()

    def test_pos_at_last_token_unary(self):
        """Test when pos is at the last token which is unary."""
        parser_state = {
            "tokens": [
                {"type": "MINUS", "value": "-", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("._parse_primary_package._parse_primary_src._parse_primary") as mock_parse_primary:
            mock_parse_primary.return_value = {
                "type": "LITERAL",
                "value": 42,
                "children": [],
                "line": 1,
                "column": 2
            }
            
            result = _parse_unary(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "-")
            self.assertEqual(parser_state["pos"], 1)

    def test_token_without_type_field(self):
        """Test handling of token without type field."""
        parser_state = {
            "tokens": [
                {"value": "x", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        expected_primary_result = {
            "type": "IDENTIFIER",
            "value": "x",
            "children": [],
            "line": 1,
            "column": 1
        }
        
        with patch("._parse_primary_package._parse_primary_src._parse_primary") as mock_parse_primary:
            mock_parse_primary.return_value = expected_primary_result
            
            result = _parse_unary(parser_state)
            
            self.assertEqual(result, expected_primary_result)
            mock_parse_primary.assert_called_once()

    def test_plus_token_delegates_to_primary(self):
        """Test that PLUS token (not unary in this context) delegates to primary."""
        parser_state = {
            "tokens": [
                {"type": "PLUS", "value": "+", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 2}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        expected_primary_result = {
            "type": "IDENTIFIER",
            "value": "x",
            "children": [],
            "line": 1,
            "column": 2
        }
        
        with patch("._parse_primary_package._parse_primary_src._parse_primary") as mock_parse_primary:
            mock_parse_primary.return_value = expected_primary_result
            
            result = _parse_unary(parser_state)
            
            self.assertEqual(result, expected_primary_result)
            self.assertEqual(parser_state["pos"], 0)

    def test_preserves_parser_state_other_fields(self):
        """Test that other parser_state fields are preserved."""
        parser_state = {
            "tokens": [
                {"type": "MINUS", "value": "-", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 2}
            ],
            "pos": 0,
            "filename": "test_module.py",
            "error": None
        }
        
        with patch("._parse_primary_package._parse_primary_src._parse_primary") as mock_parse_primary:
            mock_parse_primary.return_value = {
                "type": "IDENTIFIER",
                "value": "x",
                "children": [],
                "line": 1,
                "column": 2
            }
            
            _parse_unary(parser_state)
            
            self.assertEqual(parser_state["filename"], "test_module.py")
            self.assertIsNone(parser_state["error"])


if __name__ == "__main__":
    unittest.main()

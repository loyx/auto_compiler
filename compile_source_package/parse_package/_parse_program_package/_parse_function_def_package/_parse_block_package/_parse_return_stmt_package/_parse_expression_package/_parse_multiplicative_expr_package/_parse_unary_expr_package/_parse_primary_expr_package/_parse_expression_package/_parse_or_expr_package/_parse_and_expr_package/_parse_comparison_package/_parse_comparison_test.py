"""Unit tests for _parse_comparison function."""

import unittest
from unittest.mock import patch

# Import the function under test using relative import
from ._parse_comparison_src import _parse_comparison


class TestParseComparison(unittest.TestCase):
    """Test cases for _parse_comparison function."""
    
    def test_no_comparison_operator(self):
        """Test parsing when there's no comparison operator."""
        parser_state = {
            "tokens": [{"type": "NUMBER", "value": "42", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("._parse_comparison_src._parse_additive_expr") as mock_additive:
            mock_additive.return_value = {"type": "NUMBER", "value": "42", "line": 1, "column": 1}
            
            result = _parse_comparison(parser_state)
            
            self.assertEqual(result["type"], "NUMBER")
            self.assertEqual(result["value"], "42")
            self.assertEqual(parser_state["pos"], 0)
            mock_additive.assert_called_once_with(parser_state)
    
    def test_simple_equality_comparison(self):
        """Test parsing a simple equality comparison (==)."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "==", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "5", "line": 1, "column": 6}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("._parse_comparison_src._parse_additive_expr") as mock_additive:
            mock_additive.side_effect = [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "NUMBER", "value": "5", "line": 1, "column": 6}
            ]
            
            result = _parse_comparison(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["operator"], "==")
            self.assertEqual(len(result["children"]), 2)
            self.assertEqual(parser_state["pos"], 3)
    
    def test_all_comparison_operators(self):
        """Test all comparison operators: ==, !=, <, <=, >, >=."""
        operators = ["==", "!=", "<", "<=", ">", ">="]
        
        for op in operators:
            with self.subTest(operator=op):
                parser_state = {
                    "tokens": [
                        {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                        {"type": "OPERATOR", "value": op, "line": 1, "column": 3},
                        {"type": "IDENTIFIER", "value": "y", "line": 1, "column": 5}
                    ],
                    "pos": 0,
                    "filename": "test.py"
                }
                
                with patch("._parse_comparison_src._parse_additive_expr") as mock_additive:
                    mock_additive.side_effect = [
                        {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                        {"type": "IDENTIFIER", "value": "y", "line": 1, "column": 5}
                    ]
                    
                    result = _parse_comparison(parser_state)
                    
                    self.assertEqual(result["type"], "BINARY_OP")
                    self.assertEqual(result["operator"], op)
                    self.assertEqual(len(result["children"]), 2)
    
    def test_left_associativity(self):
        """Test that comparison expressions are left-associative."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "<", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 5},
                {"type": "OPERATOR", "value": "<", "line": 1, "column": 7},
                {"type": "NUMBER", "value": "3", "line": 1, "column": 9}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("._parse_comparison_src._parse_additive_expr") as mock_additive:
            mock_additive.side_effect = [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 5},
                {"type": "NUMBER", "value": "3", "line": 1, "column": 9}
            ]
            
            result = _parse_comparison(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["operator"], "<")
            self.assertEqual(len(result["children"]), 2)
            
            left_child = result["children"][0]
            self.assertEqual(left_child["type"], "BINARY_OP")
            self.assertEqual(left_child["operator"], "<")
            
            right_child = result["children"][1]
            self.assertEqual(right_child["type"], "NUMBER")
            self.assertEqual(right_child["value"], "3")
    
    def test_position_updated_correctly(self):
        """Test that parser_state position is updated correctly."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "==", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "10", "line": 1, "column": 6}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("._parse_comparison_src._parse_additive_expr") as mock_additive:
            mock_additive.side_effect = [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "NUMBER", "value": "10", "line": 1, "column": 6}
            ]
            
            _parse_comparison(parser_state)
            
            self.assertEqual(parser_state["pos"], 3)
    
    def test_line_column_preserved(self):
        """Test that line and column information is preserved in AST."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 5, "column": 10},
                {"type": "OPERATOR", "value": ">=", "line": 5, "column": 12},
                {"type": "NUMBER", "value": "100", "line": 5, "column": 15}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("._parse_comparison_src._parse_additive_expr") as mock_additive:
            mock_additive.side_effect = [
                {"type": "IDENTIFIER", "value": "x", "line": 5, "column": 10},
                {"type": "NUMBER", "value": "100", "line": 5, "column": 15}
            ]
            
            result = _parse_comparison(parser_state)
            
            self.assertEqual(result["line"], 5)
            self.assertEqual(result["column"], 12)
    
    def test_mixed_comparison_operators(self):
        """Test parsing with mixed comparison operators."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "<", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 5},
                {"type": "OPERATOR", "value": "!=", "line": 1, "column": 7},
                {"type": "NUMBER", "value": "3", "line": 1, "column": 10}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("._parse_comparison_src._parse_additive_expr") as mock_additive:
            mock_additive.side_effect = [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 5},
                {"type": "NUMBER", "value": "3", "line": 1, "column": 10}
            ]
            
            result = _parse_comparison(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["operator"], "!=")
            self.assertEqual(len(result["children"]), 2)
    
    def test_empty_tokens(self):
        """Test parsing with empty token list."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("._parse_comparison_src._parse_additive_expr") as mock_additive:
            mock_additive.return_value = {"type": "EMPTY", "value": None, "line": 0, "column": 0}
            
            result = _parse_comparison(parser_state)
            
            self.assertEqual(result["type"], "EMPTY")
            self.assertEqual(parser_state["pos"], 0)


if __name__ == "__main__":
    unittest.main()

# === imports ===
import unittest
from unittest.mock import patch, MagicMock
import sys

# === mock _parse_additive before importing _parse_comparison_src ===
# This prevents the import chain from failing due to missing modules
mock_additive = MagicMock()
sys.modules['._parse_additive_package._parse_additive_src'] = MagicMock()
sys.modules['._parse_additive_package._parse_additive_src']._parse_additive = mock_additive

# === relative import of UUT ===
from ._parse_comparison_src import _parse_comparison


class TestParseComparison(unittest.TestCase):
    """Test cases for _parse_comparison function."""

    def test_single_comparison_lt(self):
        """Test single less-than comparison."""
        tokens = [
            {"type": "IDENT", "value": "a", "line": 1, "column": 1},
            {"type": "LT", "value": "<", "line": 1, "column": 3},
            {"type": "IDENT", "value": "b", "line": 1, "column": 5},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.py"}
        
        with patch("._parse_additive_package._parse_additive_src._parse_additive") as mock_additive:
            mock_additive.side_effect = [
                {"type": "IDENT", "value": "a", "line": 1, "column": 1},
                {"type": "IDENT", "value": "b", "line": 1, "column": 5},
            ]
            
            result = _parse_comparison(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "<")
            self.assertEqual(len(result["children"]), 2)
            self.assertEqual(parser_state["pos"], 3)

    def test_single_comparison_eq(self):
        """Test single equality comparison."""
        tokens = [
            {"type": "IDENT", "value": "x", "line": 2, "column": 1},
            {"type": "EQ", "value": "==", "line": 2, "column": 3},
            {"type": "NUM", "value": "5", "line": 2, "column": 6},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.py"}
        
        with patch("._parse_additive_package._parse_additive_src._parse_additive") as mock_additive:
            mock_additive.side_effect = [
                {"type": "IDENT", "value": "x", "line": 2, "column": 1},
                {"type": "NUM", "value": "5", "line": 2, "column": 6},
            ]
            
            result = _parse_comparison(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "==")
            self.assertEqual(parser_state["pos"], 3)

    def test_single_comparison_ne(self):
        """Test single not-equal comparison."""
        tokens = [
            {"type": "IDENT", "value": "a", "line": 1, "column": 1},
            {"type": "NE", "value": "!=", "line": 1, "column": 3},
            {"type": "IDENT", "value": "b", "line": 1, "column": 6},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.py"}
        
        with patch("._parse_additive_package._parse_additive_src._parse_additive") as mock_additive:
            mock_additive.side_effect = [
                {"type": "IDENT", "value": "a", "line": 1, "column": 1},
                {"type": "IDENT", "value": "b", "line": 1, "column": 6},
            ]
            
            result = _parse_comparison(parser_state)
            
            self.assertEqual(result["value"], "!=")
            self.assertEqual(parser_state["pos"], 3)

    def test_single_comparison_gt(self):
        """Test single greater-than comparison."""
        tokens = [
            {"type": "IDENT", "value": "x", "line": 1, "column": 1},
            {"type": "GT", "value": ">", "line": 1, "column": 3},
            {"type": "NUM", "value": "10", "line": 1, "column": 5},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.py"}
        
        with patch("._parse_additive_package._parse_additive_src._parse_additive") as mock_additive:
            mock_additive.side_effect = [
                {"type": "IDENT", "value": "x", "line": 1, "column": 1},
                {"type": "NUM", "value": "10", "line": 1, "column": 5},
            ]
            
            result = _parse_comparison(parser_state)
            
            self.assertEqual(result["value"], ">")
            self.assertEqual(parser_state["pos"], 3)

    def test_single_comparison_le(self):
        """Test single less-than-or-equal comparison."""
        tokens = [
            {"type": "IDENT", "value": "a", "line": 1, "column": 1},
            {"type": "LE", "value": "<=", "line": 1, "column": 3},
            {"type": "IDENT", "value": "b", "line": 1, "column": 6},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.py"}
        
        with patch("._parse_additive_package._parse_additive_src._parse_additive") as mock_additive:
            mock_additive.side_effect = [
                {"type": "IDENT", "value": "a", "line": 1, "column": 1},
                {"type": "IDENT", "value": "b", "line": 1, "column": 6},
            ]
            
            result = _parse_comparison(parser_state)
            
            self.assertEqual(result["value"], "<=")
            self.assertEqual(parser_state["pos"], 3)

    def test_single_comparison_ge(self):
        """Test single greater-than-or-equal comparison."""
        tokens = [
            {"type": "IDENT", "value": "x", "line": 1, "column": 1},
            {"type": "GE", "value": ">=", "line": 1, "column": 3},
            {"type": "NUM", "value": "0", "line": 1, "column": 6},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.py"}
        
        with patch("._parse_additive_package._parse_additive_src._parse_additive") as mock_additive:
            mock_additive.side_effect = [
                {"type": "IDENT", "value": "x", "line": 1, "column": 1},
                {"type": "NUM", "value": "0", "line": 1, "column": 6},
            ]
            
            result = _parse_comparison(parser_state)
            
            self.assertEqual(result["value"], ">=")
            self.assertEqual(parser_state["pos"], 3)

    def test_chained_comparison_left_associative(self):
        """Test chained comparison with left-associative binding."""
        tokens = [
            {"type": "IDENT", "value": "a", "line": 1, "column": 1},
            {"type": "LT", "value": "<", "line": 1, "column": 3},
            {"type": "IDENT", "value": "b", "line": 1, "column": 5},
            {"type": "LT", "value": "<", "line": 1, "column": 7},
            {"type": "IDENT", "value": "c", "line": 1, "column": 9},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.py"}
        
        with patch("._parse_additive_package._parse_additive_src._parse_additive") as mock_additive:
            mock_additive.side_effect = [
                {"type": "IDENT", "value": "a", "line": 1, "column": 1},
                {"type": "IDENT", "value": "b", "line": 1, "column": 5},
                {"type": "IDENT", "value": "c", "line": 1, "column": 9},
            ]
            
            result = _parse_comparison(parser_state)
            
            # Should be left-associative: (a < b) < c
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "<")
            self.assertEqual(len(result["children"]), 2)
            # Right child should be 'c'
            self.assertEqual(result["children"][1]["value"], "c")
            # Left child should be another BINARY_OP (a < b)
            self.assertEqual(result["children"][0]["type"], "BINARY_OP")
            self.assertEqual(result["children"][0]["value"], "<")
            self.assertEqual(parser_state["pos"], 5)

    def test_no_comparison_operator(self):
        """Test expression without comparison operators."""
        tokens = [
            {"type": "IDENT", "value": "x", "line": 1, "column": 1},
            {"type": "PLUS", "value": "+", "line": 1, "column": 3},
            {"type": "NUM", "value": "1", "line": 1, "column": 5},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.py"}
        
        with patch("._parse_additive_package._parse_additive_src._parse_additive") as mock_additive:
            mock_additive.return_value = {"type": "BINARY_OP", "value": "+", "line": 1, "column": 1}
            
            result = _parse_comparison(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "+")
            self.assertEqual(parser_state["pos"], 0)

    def test_empty_tokens(self):
        """Test with empty token list."""
        parser_state = {"tokens": [], "pos": 0, "filename": "test.py"}
        
        with patch("._parse_additive_package._parse_additive_src._parse_additive") as mock_additive:
            mock_additive.return_value = {"type": "IDENT", "value": "x", "line": 1, "column": 1}
            
            result = _parse_comparison(parser_state)
            
            self.assertEqual(result["type"], "IDENT")
            self.assertEqual(result["value"], "x")
            self.assertEqual(parser_state["pos"], 0)

    def test_position_at_end(self):
        """Test when position is already at end of tokens."""
        tokens = [
            {"type": "IDENT", "value": "x", "line": 1, "column": 1},
        ]
        parser_state = {"tokens": tokens, "pos": 1, "filename": "test.py"}
        
        with patch("._parse_additive_package._parse_additive_src._parse_additive") as mock_additive:
            mock_additive.return_value = {"type": "IDENT", "value": "x", "line": 1, "column": 1}
            
            result = _parse_comparison(parser_state)
            
            self.assertEqual(result["type"], "IDENT")
            self.assertEqual(parser_state["pos"], 1)

    def test_mixed_comparison_operators(self):
        """Test mixed comparison operators in chain."""
        tokens = [
            {"type": "IDENT", "value": "a", "line": 1, "column": 1},
            {"type": "LT", "value": "<", "line": 1, "column": 3},
            {"type": "IDENT", "value": "b", "line": 1, "column": 5},
            {"type": "GE", "value": ">=", "line": 1, "column": 7},
            {"type": "IDENT", "value": "c", "line": 1, "column": 10},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.py"}
        
        with patch("._parse_additive_package._parse_additive_src._parse_additive") as mock_additive:
            mock_additive.side_effect = [
                {"type": "IDENT", "value": "a", "line": 1, "column": 1},
                {"type": "IDENT", "value": "b", "line": 1, "column": 5},
                {"type": "IDENT", "value": "c", "line": 1, "column": 10},
            ]
            
            result = _parse_comparison(parser_state)
            
            # Should be left-associative: (a < b) >= c
            self.assertEqual(result["value"], ">=")
            self.assertEqual(result["children"][0]["value"], "<")
            self.assertEqual(parser_state["pos"], 5)

    def test_line_column_preservation(self):
        """Test that line and column information is preserved."""
        tokens = [
            {"type": "IDENT", "value": "x", "line": 5, "column": 10},
            {"type": "EQ", "value": "==", "line": 5, "column": 12},
            {"type": "NUM", "value": "0", "line": 5, "column": 15},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.py"}
        
        with patch("._parse_additive_package._parse_additive_src._parse_additive") as mock_additive:
            mock_additive.side_effect = [
                {"type": "IDENT", "value": "x", "line": 5, "column": 10},
                {"type": "NUM", "value": "0", "line": 5, "column": 15},
            ]
            
            result = _parse_comparison(parser_state)
            
            self.assertEqual(result["line"], 5)
            self.assertEqual(result["column"], 10)


if __name__ == "__main__":
    unittest.main()

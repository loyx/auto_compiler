import unittest
from unittest.mock import patch

# Relative import from the same package structure
from ._parse_comparison_package._parse_comparison_src import _parse_comparison


class TestParseComparison(unittest.TestCase):
    """Test cases for _parse_comparison function."""

    def test_single_comparison_less_than(self):
        """Test single comparison with < operator."""
        parser_state = {"pos": 0, "tokens": []}
        
        with patch('._parse_additive_package._parse_additive_src._parse_additive') as mock_additive, \
             patch('._get_current_token_package._get_current_token_src._get_current_token') as mock_token, \
             patch('._advance_package._advance_src._advance') as mock_advance:
            
            # Setup: left operand, < token, right operand, then None
            mock_additive.side_effect = [
                {"type": "identifier", "value": "a", "line": 1, "column": 1},
                {"type": "identifier", "value": "b", "line": 1, "column": 3}
            ]
            mock_token.side_effect = [
                {"type": "operator", "value": "<", "line": 1, "column": 2},
                None
            ]
            
            result = _parse_comparison(parser_state)
            
            self.assertEqual(result["type"], "comparison")
            self.assertEqual(result["value"], "<")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 2)
            self.assertEqual(len(result["children"]), 2)
            self.assertEqual(result["children"][0]["value"], "a")
            self.assertEqual(result["children"][1]["value"], "b")
            mock_advance.assert_called_once()

    def test_single_comparison_greater_than(self):
        """Test single comparison with > operator."""
        parser_state = {"pos": 0, "tokens": []}
        
        with patch('._parse_additive_package._parse_additive_src._parse_additive') as mock_additive, \
             patch('._get_current_token_package._get_current_token_src._get_current_token') as mock_token, \
             patch('._advance_package._advance_src._advance') as mock_advance:
            
            mock_additive.side_effect = [
                {"type": "number", "value": 5, "line": 1, "column": 1},
                {"type": "number", "value": 3, "line": 1, "column": 3}
            ]
            mock_token.side_effect = [
                {"type": "operator", "value": ">", "line": 1, "column": 2},
                None
            ]
            
            result = _parse_comparison(parser_state)
            
            self.assertEqual(result["type"], "comparison")
            self.assertEqual(result["value"], ">")
            mock_advance.assert_called_once()

    def test_single_comparison_less_equal(self):
        """Test single comparison with <= operator."""
        parser_state = {"pos": 0, "tokens": []}
        
        with patch('._parse_additive_package._parse_additive_src._parse_additive') as mock_additive, \
             patch('._get_current_token_package._get_current_token_src._get_current_token') as mock_token, \
             patch('._advance_package._advance_src._advance') as mock_advance:
            
            mock_additive.side_effect = [
                {"type": "identifier", "value": "x", "line": 2, "column": 1},
                {"type": "number", "value": 10, "line": 2, "column": 4}
            ]
            mock_token.side_effect = [
                {"type": "operator", "value": "<=", "line": 2, "column": 2},
                None
            ]
            
            result = _parse_comparison(parser_state)
            
            self.assertEqual(result["type"], "comparison")
            self.assertEqual(result["value"], "<=")
            self.assertEqual(result["line"], 2)
            self.assertEqual(result["column"], 2)
            mock_advance.assert_called_once()

    def test_single_comparison_greater_equal(self):
        """Test single comparison with >= operator."""
        parser_state = {"pos": 0, "tokens": []}
        
        with patch('._parse_additive_package._parse_additive_src._parse_additive') as mock_additive, \
             patch('._get_current_token_package._get_current_token_src._get_current_token') as mock_token, \
             patch('._advance_package._advance_src._advance') as mock_advance:
            
            mock_additive.side_effect = [
                {"type": "identifier", "value": "y", "line": 3, "column": 1},
                {"type": "number", "value": 0, "line": 3, "column": 4}
            ]
            mock_token.side_effect = [
                {"type": "operator", "value": ">=", "line": 3, "column": 2},
                None
            ]
            
            result = _parse_comparison(parser_state)
            
            self.assertEqual(result["type"], "comparison")
            self.assertEqual(result["value"], ">=")
            mock_advance.assert_called_once()

    def test_single_comparison_equal(self):
        """Test single comparison with == operator."""
        parser_state = {"pos": 0, "tokens": []}
        
        with patch('._parse_additive_package._parse_additive_src._parse_additive') as mock_additive, \
             patch('._get_current_token_package._get_current_token_src._get_current_token') as mock_token, \
             patch('._advance_package._advance_src._advance') as mock_advance:
            
            mock_additive.side_effect = [
                {"type": "identifier", "value": "a", "line": 1, "column": 1},
                {"type": "identifier", "value": "b", "line": 1, "column": 4}
            ]
            mock_token.side_effect = [
                {"type": "operator", "value": "==", "line": 1, "column": 2},
                None
            ]
            
            result = _parse_comparison(parser_state)
            
            self.assertEqual(result["type"], "comparison")
            self.assertEqual(result["value"], "==")
            mock_advance.assert_called_once()

    def test_single_comparison_not_equal(self):
        """Test single comparison with != operator."""
        parser_state = {"pos": 0, "tokens": []}
        
        with patch('._parse_additive_package._parse_additive_src._parse_additive') as mock_additive, \
             patch('._get_current_token_package._get_current_token_src._get_current_token') as mock_token, \
             patch('._advance_package._advance_src._advance') as mock_advance:
            
            mock_additive.side_effect = [
                {"type": "identifier", "value": "x", "line": 1, "column": 1},
                {"type": "number", "value": 0, "line": 1, "column": 4}
            ]
            mock_token.side_effect = [
                {"type": "operator", "value": "!=", "line": 1, "column": 2},
                None
            ]
            
            result = _parse_comparison(parser_state)
            
            self.assertEqual(result["type"], "comparison")
            self.assertEqual(result["value"], "!=")
            mock_advance.assert_called_once()

    def test_chained_comparison_left_associative(self):
        """Test chained comparison with left-associative parsing (a < b < c)."""
        parser_state = {"pos": 0, "tokens": []}
        
        with patch('._parse_additive_package._parse_additive_src._parse_additive') as mock_additive, \
             patch('._get_current_token_package._get_current_token_src._get_current_token') as mock_token, \
             patch('._advance_package._advance_src._advance') as mock_advance:
            
            # Three operands for a < b < c
            mock_additive.side_effect = [
                {"type": "identifier", "value": "a", "line": 1, "column": 1},
                {"type": "identifier", "value": "b", "line": 1, "column": 3},
                {"type": "identifier", "value": "c", "line": 1, "column": 5}
            ]
            # Two comparison operators then None
            mock_token.side_effect = [
                {"type": "operator", "value": "<", "line": 1, "column": 2},
                {"type": "operator", "value": "<", "line": 1, "column": 4},
                None
            ]
            
            result = _parse_comparison(parser_state)
            
            # Result should be left-associative: ((a < b) < c)
            self.assertEqual(result["type"], "comparison")
            self.assertEqual(result["value"], "<")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 4)
            
            # Left child should be the first comparison (a < b)
            left_child = result["children"][0]
            self.assertEqual(left_child["type"], "comparison")
            self.assertEqual(left_child["value"], "<")
            self.assertEqual(left_child["line"], 1)
            self.assertEqual(left_child["column"], 2)
            self.assertEqual(left_child["children"][0]["value"], "a")
            self.assertEqual(left_child["children"][1]["value"], "b")
            
            # Right child should be c
            right_child = result["children"][1]
            self.assertEqual(right_child["value"], "c")
            
            # _advance should be called twice
            self.assertEqual(mock_advance.call_count, 2)

    def test_no_comparison_operator(self):
        """Test when there's no comparison operator, should return additive expression."""
        parser_state = {"pos": 0, "tokens": []}
        
        with patch('._parse_additive_package._parse_additive_src._parse_additive') as mock_additive, \
             patch('._get_current_token_package._get_current_token_src._get_current_token') as mock_token:
            
            additive_result = {"type": "additive", "value": "+", "children": []}
            mock_additive.return_value = additive_result
            mock_token.return_value = None
            
            result = _parse_comparison(parser_state)
            
            # Should return the additive expression unchanged
            self.assertEqual(result, additive_result)
            mock_additive.assert_called_once_with(parser_state)

    def test_non_comparison_token(self):
        """Test when current token is not a comparison operator."""
        parser_state = {"pos": 0, "tokens": []}
        
        with patch('._parse_additive_package._parse_additive_src._parse_additive') as mock_additive, \
             patch('._get_current_token_package._get_current_token_src._get_current_token') as mock_token:
            
            additive_result = {"type": "additive", "value": "x", "line": 1, "column": 1}
            mock_additive.return_value = additive_result
            # Return a non-comparison operator (e.g., +)
            mock_token.return_value = {"type": "operator", "value": "+", "line": 1, "column": 2}
            
            result = _parse_comparison(parser_state)
            
            # Should return the additive expression unchanged
            self.assertEqual(result, additive_result)

    def test_empty_token_value(self):
        """Test when token has empty or missing value."""
        parser_state = {"pos": 0, "tokens": []}
        
        with patch('._parse_additive_package._parse_additive_src._parse_additive') as mock_additive, \
             patch('._get_current_token_package._get_current_token_src._get_current_token') as mock_token:
            
            additive_result = {"type": "identifier", "value": "x", "line": 1, "column": 1}
            mock_additive.return_value = additive_result
            # Token with empty value
            mock_token.return_value = {"type": "unknown", "value": "", "line": 1, "column": 2}
            
            result = _parse_comparison(parser_state)
            
            self.assertEqual(result, additive_result)

    def test_token_missing_value_key(self):
        """Test when token is missing 'value' key."""
        parser_state = {"pos": 0, "tokens": []}
        
        with patch('._parse_additive_package._parse_additive_src._parse_additive') as mock_additive, \
             patch('._get_current_token_package._get_current_token_src._get_current_token') as mock_token:
            
            additive_result = {"type": "identifier", "value": "x", "line": 1, "column": 1}
            mock_additive.return_value = additive_result
            # Token without value key
            mock_token.return_value = {"type": "unknown", "line": 1, "column": 2}
            
            result = _parse_comparison(parser_state)
            
            self.assertEqual(result, additive_result)

    def test_token_missing_line_column(self):
        """Test when token is missing line/column info, should default to 0."""
        parser_state = {"pos": 0, "tokens": []}
        
        with patch('._parse_additive_package._parse_additive_src._parse_additive') as mock_additive, \
             patch('._get_current_token_package._get_current_token_src._get_current_token') as mock_token, \
             patch('._advance_package._advance_src._advance') as mock_advance:
            
            mock_additive.side_effect = [
                {"type": "identifier", "value": "a"},
                {"type": "identifier", "value": "b"}
            ]
            # Token without line/column
            mock_token.side_effect = [
                {"type": "operator", "value": "<"},
                None
            ]
            
            result = _parse_comparison(parser_state)
            
            self.assertEqual(result["type"], "comparison")
            self.assertEqual(result["value"], "<")
            self.assertEqual(result["line"], 0)
            self.assertEqual(result["column"], 0)

    def test_multiple_chained_different_operators(self):
        """Test chained comparison with different operators (a < b >= c)."""
        parser_state = {"pos": 0, "tokens": []}
        
        with patch('._parse_additive_package._parse_additive_src._parse_additive') as mock_additive, \
             patch('._get_current_token_package._get_current_token_src._get_current_token') as mock_token, \
             patch('._advance_package._advance_src._advance') as mock_advance:
            
            mock_additive.side_effect = [
                {"type": "identifier", "value": "a", "line": 1, "column": 1},
                {"type": "identifier", "value": "b", "line": 1, "column": 3},
                {"type": "identifier", "value": "c", "line": 1, "column": 6}
            ]
            mock_token.side_effect = [
                {"type": "operator", "value": "<", "line": 1, "column": 2},
                {"type": "operator", "value": ">=", "line": 1, "column": 4},
                None
            ]
            
            result = _parse_comparison(parser_state)
            
            # Result: ((a < b) >= c)
            self.assertEqual(result["type"], "comparison")
            self.assertEqual(result["value"], ">=")
            self.assertEqual(result["column"], 4)
            
            left_child = result["children"][0]
            self.assertEqual(left_child["value"], "<")
            self.assertEqual(left_child["children"][0]["value"], "a")
            self.assertEqual(left_child["children"][1]["value"], "b")
            
            self.assertEqual(result["children"][1]["value"], "c")
            self.assertEqual(mock_advance.call_count, 2)


if __name__ == "__main__":
    unittest.main()

import unittest
from unittest.mock import patch

# Relative import for the function under test
from ._parse_or_src import _parse_or


class TestParseOr(unittest.TestCase):
    
    def test_no_or_operator(self):
        """Test when there's no || operator, should return result from _parse_and"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
            ],
            "filename": "test.c",
            "pos": 0,
            "error": ""
        }
        
        mock_and_result = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        
        with patch("._parse_and_package._parse_and_src._parse_and") as mock_parse_and:
            mock_parse_and.return_value = mock_and_result
            
            result = _parse_or(parser_state)
            
            self.assertEqual(result, mock_and_result)
            self.assertEqual(parser_state["pos"], 0)
            mock_parse_and.assert_called_once_with(parser_state)
    
    def test_single_or_operator(self):
        """Test a || b expression"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "||", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 6}
            ],
            "filename": "test.c",
            "pos": 0,
            "error": ""
        }
        
        left_operand = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        right_operand = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 6}
        
        with patch("._parse_and_package._parse_and_src._parse_and") as mock_parse_and:
            mock_parse_and.side_effect = [left_operand, right_operand]
            
            result = _parse_or(parser_state)
            
            self.assertEqual(result["type"], "OR")
            self.assertEqual(result["left"], left_operand)
            self.assertEqual(result["right"], right_operand)
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 3)
            self.assertEqual(parser_state["pos"], 2)
            self.assertEqual(mock_parse_and.call_count, 2)
    
    def test_multiple_or_operators_left_associative(self):
        """Test a || b || c should be parsed as (a || b) || c"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "||", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 6},
                {"type": "OPERATOR", "value": "||", "line": 1, "column": 8},
                {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 11}
            ],
            "filename": "test.c",
            "pos": 0,
            "error": ""
        }
        
        operand_a = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        operand_b = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 6}
        operand_c = {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 11}
        
        with patch("._parse_and_package._parse_and_src._parse_and") as mock_parse_and:
            mock_parse_and.side_effect = [operand_a, operand_b, operand_c]
            
            result = _parse_or(parser_state)
            
            # Should be (a || b) || c
            self.assertEqual(result["type"], "OR")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 8)  # Second || position
            
            # Left side should be (a || b)
            left_side = result["left"]
            self.assertEqual(left_side["type"], "OR")
            self.assertEqual(left_side["left"], operand_a)
            self.assertEqual(left_side["right"], operand_b)
            self.assertEqual(left_side["line"], 1)
            self.assertEqual(left_side["column"], 3)  # First || position
            
            # Right side should be c
            self.assertEqual(result["right"], operand_c)
            
            self.assertEqual(parser_state["pos"], 4)  # After all tokens
            self.assertEqual(mock_parse_and.call_count, 3)
    
    def test_empty_tokens(self):
        """Test when tokens list is empty"""
        parser_state = {
            "tokens": [],
            "filename": "test.c",
            "pos": 0,
            "error": ""
        }
        
        mock_result = {"type": "EMPTY", "value": None}
        
        with patch("._parse_and_package._parse_and_src._parse_and") as mock_parse_and:
            mock_parse_and.return_value = mock_result
            
            result = _parse_or(parser_state)
            
            self.assertEqual(result, mock_result)
            self.assertEqual(parser_state["pos"], 0)
    
    def test_pos_at_end(self):
        """Test when pos is already at end of tokens"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
            ],
            "filename": "test.c",
            "pos": 1,  # Already at end
            "error": ""
        }
        
        mock_result = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        
        with patch("._parse_and_package._parse_and_src._parse_and") as mock_parse_and:
            mock_parse_and.return_value = mock_result
            
            result = _parse_or(parser_state)
            
            self.assertEqual(result, mock_result)
            self.assertEqual(parser_state["pos"], 1)
    
    def test_or_at_end_without_right_operand(self):
        """Test when || is at the end without right operand"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "||", "line": 1, "column": 3}
            ],
            "filename": "test.c",
            "pos": 0,
            "error": ""
        }
        
        left_operand = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        right_operand = {"type": "EMPTY", "value": None}
        
        with patch("._parse_and_package._parse_and_src._parse_and") as mock_parse_and:
            mock_parse_and.side_effect = [left_operand, right_operand]
            
            result = _parse_or(parser_state)
            
            self.assertEqual(result["type"], "OR")
            self.assertEqual(result["left"], left_operand)
            self.assertEqual(result["right"], right_operand)
            self.assertEqual(parser_state["pos"], 2)
    
    def test_different_operator_not_or(self):
        """Test when current token is not || operator"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "&&", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 6}
            ],
            "filename": "test.c",
            "pos": 0,
            "error": ""
        }
        
        mock_and_result = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        
        with patch("._parse_and_package._parse_and_src._parse_and") as mock_parse_and:
            mock_parse_and.return_value = mock_and_result
            
            result = _parse_or(parser_state)
            
            self.assertEqual(result, mock_and_result)
            self.assertEqual(parser_state["pos"], 0)  # Should not consume &&
            mock_parse_and.assert_called_once()
    
    def test_or_with_complex_line_column_info(self):
        """Test OR operator with different line/column positions"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "||", "line": 2, "column": 5},
                {"type": "IDENTIFIER", "value": "b", "line": 2, "column": 8}
            ],
            "filename": "test.c",
            "pos": 0,
            "error": ""
        }
        
        left_operand = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        right_operand = {"type": "IDENTIFIER", "value": "b", "line": 2, "column": 8}
        
        with patch("._parse_and_package._parse_and_src._parse_and") as mock_parse_and:
            mock_parse_and.side_effect = [left_operand, right_operand]
            
            result = _parse_or(parser_state)
            
            self.assertEqual(result["type"], "OR")
            self.assertEqual(result["line"], 2)  # From || token
            self.assertEqual(result["column"], 5)  # From || token
            self.assertEqual(parser_state["pos"], 2)


if __name__ == "__main__":
    unittest.main()

import unittest
from unittest.mock import patch
import sys
import os

# Add the parent directory to sys.path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import for the function under test
from _parse_multiplicative_src import _parse_multiplicative


class TestParseMultiplicative(unittest.TestCase):
    """Test cases for _parse_multiplicative function."""
    
    def test_single_operand_no_operator(self):
        """Test parsing a single operand without any multiplicative operator."""
        token_operand = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 1
        }
        parser_state = {
            "tokens": [token_operand],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("._parse_unary_package._parse_unary_src._parse_unary") as mock_unary:
            mock_unary.return_value = {
                "type": "IDENTIFIER",
                "value": "x",
                "line": 1,
                "column": 1
            }
            
            result = _parse_multiplicative(parser_state)
            
            mock_unary.assert_called_once()
            self.assertEqual(result["type"], "IDENTIFIER")
            self.assertEqual(result["value"], "x")
            self.assertEqual(parser_state["pos"], 0)
    
    def test_multiplication_operator(self):
        """Test parsing multiplication expression: a * b."""
        token_a = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        token_mul = {"type": "MUL", "value": "*", "line": 1, "column": 3}
        token_b = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
        
        parser_state = {
            "tokens": [token_a, token_mul, token_b],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("._parse_unary_package._parse_unary_src._parse_unary") as mock_unary:
            mock_unary.side_effect = [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
            ]
            
            result = _parse_multiplicative(parser_state)
            
            self.assertEqual(mock_unary.call_count, 2)
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "*")
            self.assertEqual(len(result["children"]), 2)
            self.assertEqual(parser_state["pos"], 3)
    
    def test_division_operator(self):
        """Test parsing division expression: a / b."""
        token_a = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        token_div = {"type": "DIV", "value": "/", "line": 1, "column": 3}
        token_b = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
        
        parser_state = {
            "tokens": [token_a, token_div, token_b],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("._parse_unary_package._parse_unary_src._parse_unary") as mock_unary:
            mock_unary.side_effect = [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
            ]
            
            result = _parse_multiplicative(parser_state)
            
            self.assertEqual(mock_unary.call_count, 2)
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "/")
            self.assertEqual(len(result["children"]), 2)
            self.assertEqual(parser_state["pos"], 3)
    
    def test_left_associative_chaining(self):
        """Test left-associative chaining: a * b / c."""
        token_a = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        token_mul = {"type": "MUL", "value": "*", "line": 1, "column": 3}
        token_b = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
        token_div = {"type": "DIV", "value": "/", "line": 1, "column": 7}
        token_c = {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 9}
        
        parser_state = {
            "tokens": [token_a, token_mul, token_b, token_div, token_c],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("._parse_unary_package._parse_unary_src._parse_unary") as mock_unary:
            mock_unary.side_effect = [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
                {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 9}
            ]
            
            result = _parse_multiplicative(parser_state)
            
            self.assertEqual(mock_unary.call_count, 3)
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "/")
            self.assertEqual(len(result["children"]), 2)
            self.assertEqual(result["children"][1]["type"], "IDENTIFIER")
            self.assertEqual(result["children"][1]["value"], "c")
            self.assertEqual(result["children"][0]["type"], "BINARY_OP")
            self.assertEqual(result["children"][0]["value"], "*")
            self.assertEqual(parser_state["pos"], 5)
    
    def test_error_from_unary_left(self):
        """Test error propagation when left operand parsing fails."""
        token_a = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        
        parser_state = {
            "tokens": [token_a],
            "pos": 0,
            "filename": "test.py",
            "error": None
        }
        
        with patch("._parse_unary_package._parse_unary_src._parse_unary") as mock_unary:
            mock_unary.return_value = {"type": "ERROR", "value": "invalid"}
            parser_state["error"] = "Invalid operand"
            
            result = _parse_multiplicative(parser_state)
            
            mock_unary.assert_called_once()
            self.assertEqual(parser_state["error"], "Invalid operand")
            self.assertEqual(result["type"], "ERROR")
    
    def test_error_from_unary_right(self):
        """Test error propagation when right operand parsing fails."""
        token_a = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        token_mul = {"type": "MUL", "value": "*", "line": 1, "column": 3}
        token_b = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
        
        parser_state = {
            "tokens": [token_a, token_mul, token_b],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("._parse_unary_package._parse_unary_src._parse_unary") as mock_unary:
            mock_unary.side_effect = [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "ERROR", "value": "invalid"}
            ]
            parser_state["error"] = "Invalid right operand"
            
            result = _parse_multiplicative(parser_state)
            
            self.assertEqual(mock_unary.call_count, 2)
            self.assertEqual(parser_state["error"], "Invalid right operand")
            self.assertEqual(result["type"], "IDENTIFIER")
            self.assertEqual(result["value"], "a")
    
    def test_empty_tokens(self):
        """Test parsing with empty token list."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("._parse_unary_package._parse_unary_src._parse_unary") as mock_unary:
            mock_unary.return_value = {"type": "LITERAL", "value": 0, "line": 0, "column": 0}
            
            result = _parse_multiplicative(parser_state)
            
            mock_unary.assert_called_once()
            self.assertEqual(result["type"], "LITERAL")
            self.assertEqual(parser_state["pos"], 0)
    
    def test_position_at_end(self):
        """Test when position is already at end of tokens."""
        token_a = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        
        parser_state = {
            "tokens": [token_a],
            "pos": 1,
            "filename": "test.py"
        }
        
        with patch("._parse_unary_package._parse_unary_src._parse_unary") as mock_unary:
            mock_unary.return_value = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
            
            result = _parse_multiplicative(parser_state)
            
            mock_unary.assert_called_once()
            self.assertEqual(result["type"], "IDENTIFIER")
            self.assertEqual(parser_state["pos"], 1)
    
    def test_non_multiplicative_token_stops_parsing(self):
        """Test that non-multiplicative tokens stop the parsing loop."""
        token_a = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        token_add = {"type": "ADD", "value": "+", "line": 1, "column": 3}
        token_b = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
        
        parser_state = {
            "tokens": [token_a, token_add, token_b],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("._parse_unary_package._parse_unary_src._parse_unary") as mock_unary:
            mock_unary.return_value = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
            
            result = _parse_multiplicative(parser_state)
            
            mock_unary.assert_called_once()
            self.assertEqual(result["type"], "IDENTIFIER")
            self.assertEqual(parser_state["pos"], 0)


if __name__ == "__main__":
    unittest.main()

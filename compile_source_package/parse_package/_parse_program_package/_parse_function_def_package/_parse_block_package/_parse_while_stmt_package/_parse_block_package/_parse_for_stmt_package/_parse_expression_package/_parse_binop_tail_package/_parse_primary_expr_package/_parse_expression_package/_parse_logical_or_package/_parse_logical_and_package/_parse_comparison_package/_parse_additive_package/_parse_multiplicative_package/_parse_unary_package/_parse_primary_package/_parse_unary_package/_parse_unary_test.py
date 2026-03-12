import unittest
from unittest.mock import patch

# Relative import for the function under test
from ._parse_unary_src import _parse_unary


class TestParseUnary(unittest.TestCase):
    """Test cases for _parse_unary function."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.base_token = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 5
        }
    
    def _create_parser_state(self, tokens, pos=0, filename="test.py"):
        """Helper to create parser state."""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename
        }
    
    def test_parse_unary_plus(self):
        """Test parsing unary plus operator."""
        tokens = [
            {"type": "PLUS", "value": "+", "line": 1, "column": 1},
            self.base_token
        ]
        parser_state = self._create_parser_state(tokens)
        
        with patch("._parse_primary_package._parse_primary_src._parse_primary") as mock_primary:
            mock_primary.return_value = self.base_token
            result = _parse_unary(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["operator"], "+")
            self.assertEqual(result["operand"], self.base_token)
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            self.assertEqual(parser_state["pos"], 2)
    
    def test_parse_unary_minus(self):
        """Test parsing unary minus operator."""
        tokens = [
            {"type": "MINUS", "value": "-", "line": 1, "column": 1},
            self.base_token
        ]
        parser_state = self._create_parser_state(tokens)
        
        with patch("._parse_primary_package._parse_primary_src._parse_primary") as mock_primary:
            mock_primary.return_value = self.base_token
            result = _parse_unary(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["operator"], "-")
            self.assertEqual(result["operand"], self.base_token)
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
    
    def test_parse_unary_not(self):
        """Test parsing logical NOT operator."""
        tokens = [
            {"type": "NOT", "value": "!", "line": 2, "column": 3},
            self.base_token
        ]
        parser_state = self._create_parser_state(tokens)
        
        with patch("._parse_primary_package._parse_primary_src._parse_primary") as mock_primary:
            mock_primary.return_value = self.base_token
            result = _parse_unary(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["operator"], "!")
            self.assertEqual(result["operand"], self.base_token)
            self.assertEqual(result["line"], 2)
            self.assertEqual(result["column"], 3)
    
    def test_parse_unary_tilde(self):
        """Test parsing bitwise NOT operator."""
        tokens = [
            {"type": "TILDE", "value": "~", "line": 3, "column": 1},
            self.base_token
        ]
        parser_state = self._create_parser_state(tokens)
        
        with patch("._parse_primary_package._parse_primary_src._parse_primary") as mock_primary:
            mock_primary.return_value = self.base_token
            result = _parse_unary(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["operator"], "~")
            self.assertEqual(result["operand"], self.base_token)
            self.assertEqual(result["line"], 3)
            self.assertEqual(result["column"], 1)
    
    def test_parse_stacked_unary_operators(self):
        """Test parsing multiple stacked unary operators (e.g., --x)."""
        tokens = [
            {"type": "MINUS", "value": "-", "line": 1, "column": 1},
            {"type": "MINUS", "value": "-", "line": 1, "column": 2},
            self.base_token
        ]
        parser_state = self._create_parser_state(tokens)
        
        with patch("._parse_primary_package._parse_primary_src._parse_primary") as mock_primary:
            mock_primary.return_value = self.base_token
            result = _parse_unary(parser_state)
            
            # Should create nested UNARY_OP nodes
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["operator"], "-")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            
            # Inner node should also be UNARY_OP
            inner = result["operand"]
            self.assertEqual(inner["type"], "UNARY_OP")
            self.assertEqual(inner["operator"], "-")
            self.assertEqual(inner["operand"], self.base_token)
            
            self.assertEqual(parser_state["pos"], 3)
    
    def test_parse_no_unary_operator(self):
        """Test when current token is not a unary operator."""
        tokens = [self.base_token]
        parser_state = self._create_parser_state(tokens)
        
        with patch("._parse_primary_package._parse_primary_src._parse_primary") as mock_primary:
            mock_primary.return_value = self.base_token
            result = _parse_unary(parser_state)
            
            # Should delegate to _parse_primary
            mock_primary.assert_called_once()
            self.assertEqual(result, self.base_token)
            self.assertEqual(parser_state["pos"], 0)  # pos should not change
    
    def test_parse_empty_tokens(self):
        """Test with empty token list."""
        parser_state = self._create_parser_state([])
        
        with patch("._parse_primary_package._parse_primary_src._parse_primary") as mock_primary:
            mock_primary.return_value = {"type": "ERROR", "value": "Unexpected end"}
            result = _parse_unary(parser_state)
            
            mock_primary.assert_called_once()
            self.assertEqual(result["type"], "ERROR")
    
    def test_parse_pos_out_of_bounds(self):
        """Test when pos is beyond token list length."""
        tokens = [self.base_token]
        parser_state = self._create_parser_state(tokens, pos=5)
        
        with patch("._parse_primary_package._parse_primary_src._parse_primary") as mock_primary:
            mock_primary.return_value = self.base_token
            result = _parse_unary(parser_state)
            
            mock_primary.assert_called_once()
            self.assertEqual(result, self.base_token)
    
    def test_parse_error_propagation(self):
        """Test error propagation from _parse_primary."""
        tokens = [
            {"type": "PLUS", "value": "+", "line": 1, "column": 1},
            self.base_token
        ]
        parser_state = self._create_parser_state(tokens)
        
        error_result = {"type": "ERROR", "value": "Invalid expression"}
        
        with patch("._parse_primary_package._parse_primary_src._parse_primary") as mock_primary:
            mock_primary.return_value = error_result
            result = _parse_unary(parser_state)
            
            self.assertEqual(result["type"], "ERROR")
            self.assertEqual(result["value"], "Invalid expression")
    
    def test_parse_mixed_unary_operators(self):
        """Test parsing mixed unary operators (e.g., +!x)."""
        tokens = [
            {"type": "PLUS", "value": "+", "line": 1, "column": 1},
            {"type": "NOT", "value": "!", "line": 1, "column": 2},
            self.base_token
        ]
        parser_state = self._create_parser_state(tokens)
        
        with patch("._parse_primary_package._parse_primary_src._parse_primary") as mock_primary:
            mock_primary.return_value = self.base_token
            result = _parse_unary(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["operator"], "+")
            
            inner = result["operand"]
            self.assertEqual(inner["type"], "UNARY_OP")
            self.assertEqual(inner["operator"], "!")
            self.assertEqual(inner["operand"], self.base_token)
    
    def test_parse_unary_preserves_position_on_error(self):
        """Test that position is updated even when operand has error."""
        tokens = [
            {"type": "MINUS", "value": "-", "line": 1, "column": 1},
            self.base_token
        ]
        parser_state = self._create_parser_state(tokens)
        
        with patch("._parse_primary_package._parse_primary_src._parse_primary") as mock_primary:
            mock_primary.return_value = {"type": "ERROR", "value": "Failed"}
            result = _parse_unary(parser_state)
            
            # Position should be consumed even on error
            self.assertEqual(parser_state["pos"], 2)
            self.assertEqual(result["type"], "ERROR")


if __name__ == "__main__":
    unittest.main()

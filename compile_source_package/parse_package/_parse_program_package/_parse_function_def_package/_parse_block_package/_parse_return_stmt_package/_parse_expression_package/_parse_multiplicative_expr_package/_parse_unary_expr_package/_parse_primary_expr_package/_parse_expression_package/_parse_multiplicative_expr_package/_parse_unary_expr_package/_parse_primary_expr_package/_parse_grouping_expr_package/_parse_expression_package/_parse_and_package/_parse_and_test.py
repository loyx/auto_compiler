import unittest
from unittest.mock import patch
from typing import Dict, Any

# Relative import for the function under test
from ._parse_and_src import _parse_and


class TestParseAnd(unittest.TestCase):
    """Test cases for _parse_and function."""
    
    def _create_parser_state(self, tokens: list, pos: int = 0) -> Dict[str, Any]:
        """Helper to create parser state."""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": "test.py",
            "error": None
        }
    
    def test_single_expression_no_and(self):
        """Test parsing single expression without && operator."""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        ]
        parser_state = self._create_parser_state(tokens)
        
        mock_ast = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        
        with patch("._parse_equality_package._parse_equality_src._parse_equality") as mock_equality:
            mock_equality.return_value = mock_ast
            
            result = _parse_and(parser_state)
            
            self.assertEqual(result, mock_ast)
            mock_equality.assert_called_once()
            self.assertEqual(parser_state["pos"], 1)
    
    def test_simple_and_chain(self):
        """Test parsing a && b."""
        tokens = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            {"type": "OPERATOR", "value": "&&", "line": 1, "column": 3},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 6}
        ]
        parser_state = self._create_parser_state(tokens)
        
        left_ast = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        right_ast = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 6}
        
        with patch("._parse_equality_package._parse_equality_src._parse_equality") as mock_equality:
            mock_equality.side_effect = [left_ast, right_ast]
            
            result = _parse_and(parser_state)
            
            self.assertEqual(result["type"], "BINARY")
            self.assertEqual(result["operator"], "&&")
            self.assertEqual(result["left"], left_ast)
            self.assertEqual(result["right"], right_ast)
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 3)
            self.assertEqual(parser_state["pos"], 3)
    
    def test_multiple_and_left_associative(self):
        """Test parsing a && b && c with left-associativity."""
        tokens = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            {"type": "OPERATOR", "value": "&&", "line": 1, "column": 3},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 6},
            {"type": "OPERATOR", "value": "&&", "line": 1, "column": 8},
            {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 11}
        ]
        parser_state = self._create_parser_state(tokens)
        
        a_ast = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        b_ast = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 6}
        c_ast = {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 11}
        
        with patch("._parse_equality_package._parse_equality_src._parse_equality") as mock_equality:
            mock_equality.side_effect = [a_ast, b_ast, c_ast]
            
            result = _parse_and(parser_state)
            
            # Verify left-associative structure: (a && b) && c
            self.assertEqual(result["type"], "BINARY")
            self.assertEqual(result["operator"], "&&")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 8)
            
            # Left should be (a && b)
            left_node = result["left"]
            self.assertEqual(left_node["type"], "BINARY")
            self.assertEqual(left_node["operator"], "&&")
            self.assertEqual(left_node["left"], a_ast)
            self.assertEqual(left_node["right"], b_ast)
            self.assertEqual(left_node["line"], 1)
            self.assertEqual(left_node["column"], 3)
            
            # Right should be c
            self.assertEqual(result["right"], c_ast)
            self.assertEqual(parser_state["pos"], 5)
    
    def test_and_with_non_operator_token(self):
        """Test that parsing stops at non-&& operator."""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            {"type": "OPERATOR", "value": "+", "line": 1, "column": 3},
            {"type": "IDENTIFIER", "value": "y", "line": 1, "column": 5}
        ]
        parser_state = self._create_parser_state(tokens)
        
        mock_ast = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        
        with patch("._parse_equality_package._parse_equality_src._parse_equality") as mock_equality:
            mock_equality.return_value = mock_ast
            
            result = _parse_and(parser_state)
            
            self.assertEqual(result, mock_ast)
            mock_equality.assert_called_once()
            self.assertEqual(parser_state["pos"], 1)
    
    def test_and_with_wrong_operator_type(self):
        """Test that parsing stops when token type is not OPERATOR."""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            {"type": "KEYWORD", "value": "&&", "line": 1, "column": 3}
        ]
        parser_state = self._create_parser_state(tokens)
        
        mock_ast = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        
        with patch("._parse_equality_package._parse_equality_src._parse_equality") as mock_equality:
            mock_equality.return_value = mock_ast
            
            result = _parse_and(parser_state)
            
            self.assertEqual(result, mock_ast)
            self.assertEqual(parser_state["pos"], 1)
    
    def test_empty_tokens(self):
        """Test parsing with empty token list."""
        parser_state = self._create_parser_state([])
        
        mock_ast = {"type": "EMPTY", "value": None}
        
        with patch("._parse_equality_package._parse_equality_src._parse_equality") as mock_equality:
            mock_equality.return_value = mock_ast
            
            result = _parse_and(parser_state)
            
            self.assertEqual(result, mock_ast)
            mock_equality.assert_called_once()
            self.assertEqual(parser_state["pos"], 0)
    
    def test_pos_at_end(self):
        """Test parsing when pos is already at end of tokens."""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        ]
        parser_state = self._create_parser_state(tokens, pos=1)
        
        mock_ast = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        
        with patch("._parse_equality_package._parse_equality_src._parse_equality") as mock_equality:
            mock_equality.return_value = mock_ast
            
            result = _parse_and(parser_state)
            
            self.assertEqual(result, mock_ast)
            self.assertEqual(parser_state["pos"], 1)
    
    def test_and_operator_line_column_tracking(self):
        """Test that operator line and column are correctly tracked."""
        tokens = [
            {"type": "IDENTIFIER", "value": "a", "line": 2, "column": 5},
            {"type": "OPERATOR", "value": "&&", "line": 2, "column": 7},
            {"type": "IDENTIFIER", "value": "b", "line": 2, "column": 10}
        ]
        parser_state = self._create_parser_state(tokens)
        
        left_ast = {"type": "IDENTIFIER", "value": "a", "line": 2, "column": 5}
        right_ast = {"type": "IDENTIFIER", "value": "b", "line": 2, "column": 10}
        
        with patch("._parse_equality_package._parse_equality_src._parse_equality") as mock_equality:
            mock_equality.side_effect = [left_ast, right_ast]
            
            result = _parse_and(parser_state)
            
            self.assertEqual(result["line"], 2)
            self.assertEqual(result["column"], 7)


if __name__ == "__main__":
    unittest.main()

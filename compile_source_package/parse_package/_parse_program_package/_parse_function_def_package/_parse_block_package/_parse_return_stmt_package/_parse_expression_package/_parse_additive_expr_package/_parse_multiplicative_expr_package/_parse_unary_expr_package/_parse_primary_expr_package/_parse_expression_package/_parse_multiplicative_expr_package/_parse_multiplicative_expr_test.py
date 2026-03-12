import unittest
from unittest.mock import patch
from typing import Dict, Any

from _parse_multiplicative_expr_package._parse_multiplicative_expr_src import _parse_multiplicative_expr


class TestParseMultiplicativeExpr(unittest.TestCase):
    """Test suite for _parse_multiplicative_expr function"""
    
    def _create_parser_state(self, tokens: list, pos: int = 0) -> Dict[str, Any]:
        """Helper to create parser state"""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": "test.py"
        }
    
    def test_single_unary_expr_no_operator(self):
        """Test parsing single expression without multiplicative operator"""
        parser_state = self._create_parser_state([
            {"type": "NUMBER", "value": "5", "line": 1, "column": 1}
        ])
        
        mock_unary_result = {"type": "LITERAL", "value": 5, "line": 1, "column": 1}
        
        with patch("_parse_multiplicative_expr_package._parse_unary_expr_package._parse_unary_expr_src._parse_unary_expr") as mock_unary:
            mock_unary.return_value = mock_unary_result
            
            result = _parse_multiplicative_expr(parser_state)
            
            self.assertEqual(result, mock_unary_result)
            mock_unary.assert_called_once_with(parser_state)
            self.assertEqual(parser_state["pos"], 0)
    
    def test_single_multiplication_operator(self):
        """Test parsing expression with single multiplication operator"""
        parser_state = self._create_parser_state([
            {"type": "NUMBER", "value": "5", "line": 1, "column": 1},
            {"type": "STAR", "value": "*", "line": 1, "column": 3},
            {"type": "NUMBER", "value": "3", "line": 1, "column": 5}
        ])
        
        mock_unary_results = [
            {"type": "LITERAL", "value": 5, "line": 1, "column": 1},
            {"type": "LITERAL", "value": 3, "line": 1, "column": 5}
        ]
        
        with patch("_parse_multiplicative_expr_package._parse_unary_expr_package._parse_unary_expr_src._parse_unary_expr") as mock_unary:
            mock_unary.side_effect = mock_unary_results
            
            result = _parse_multiplicative_expr(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["operator"], "*")
            self.assertEqual(result["left"], mock_unary_results[0])
            self.assertEqual(result["right"], mock_unary_results[1])
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 3)
            self.assertEqual(parser_state["pos"], 3)
            self.assertEqual(mock_unary.call_count, 2)
    
    def test_multiple_operators_left_associative(self):
        """Test left-associative parsing of multiple operators"""
        parser_state = self._create_parser_state([
            {"type": "NUMBER", "value": "5", "line": 1, "column": 1},
            {"type": "STAR", "value": "*", "line": 1, "column": 3},
            {"type": "NUMBER", "value": "3", "line": 1, "column": 5},
            {"type": "SLASH", "value": "/", "line": 1, "column": 7},
            {"type": "NUMBER", "value": "2", "line": 1, "column": 9}
        ])
        
        mock_unary_results = [
            {"type": "LITERAL", "value": 5, "line": 1, "column": 1},
            {"type": "LITERAL", "value": 3, "line": 1, "column": 5},
            {"type": "LITERAL", "value": 2, "line": 1, "column": 9}
        ]
        
        with patch("_parse_multiplicative_expr_package._parse_unary_expr_package._parse_unary_expr_src._parse_unary_expr") as mock_unary:
            mock_unary.side_effect = mock_unary_results
            
            result = _parse_multiplicative_expr(parser_state)
            
            # Should be left-associative: (5 * 3) / 2
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["operator"], "/")
            self.assertEqual(result["left"]["operator"], "*")
            self.assertEqual(result["left"]["left"]["value"], 5)
            self.assertEqual(result["left"]["right"]["value"], 3)
            self.assertEqual(result["right"]["value"], 2)
            self.assertEqual(parser_state["pos"], 5)
            self.assertEqual(mock_unary.call_count, 3)
    
    def test_all_operator_types(self):
        """Test STAR, SLASH, and PERCENT operators"""
        for token_type, expected_op in [
            ("STAR", "*"),
            ("SLASH", "/"),
            ("PERCENT", "%")
        ]:
            with self.subTest(operator=token_type):
                parser_state = self._create_parser_state([
                    {"type": "NUMBER", "value": "10", "line": 1, "column": 1},
                    {"type": token_type, "value": token_type, "line": 1, "column": 3},
                    {"type": "NUMBER", "value": "2", "line": 1, "column": 5}
                ])
                
                mock_unary_results = [
                    {"type": "LITERAL", "value": 10, "line": 1, "column": 1},
                    {"type": "LITERAL", "value": 2, "line": 1, "column": 5}
                ]
                
                with patch("_parse_multiplicative_expr_package._parse_unary_expr_package._parse_unary_expr_src._parse_unary_expr") as mock_unary:
                    mock_unary.side_effect = mock_unary_results
                    
                    result = _parse_multiplicative_expr(parser_state)
                    
                    self.assertEqual(result["type"], "BINARY_OP")
                    self.assertEqual(result["operator"], expected_op)
                    self.assertEqual(parser_state["pos"], 3)
    
    def test_empty_tokens(self):
        """Test handling of empty token list"""
        parser_state = self._create_parser_state([])
        
        mock_unary_result = {"type": "LITERAL", "value": None, "line": 0, "column": 0}
        
        with patch("_parse_multiplicative_expr_package._parse_unary_expr_package._parse_unary_expr_src._parse_unary_expr") as mock_unary:
            mock_unary.return_value = mock_unary_result
            
            result = _parse_multiplicative_expr(parser_state)
            
            self.assertEqual(result, mock_unary_result)
            mock_unary.assert_called_once_with(parser_state)
            self.assertEqual(parser_state["pos"], 0)
    
    def test_position_at_end(self):
        """Test when position is already at end of tokens"""
        parser_state = self._create_parser_state([
            {"type": "NUMBER", "value": "5", "line": 1, "column": 1}
        ], pos=1)
        
        mock_unary_result = {"type": "LITERAL", "value": 5, "line": 1, "column": 1}
        
        with patch("_parse_multiplicative_expr_package._parse_unary_expr_package._parse_unary_expr_src._parse_unary_expr") as mock_unary:
            mock_unary.return_value = mock_unary_result
            
            result = _parse_multiplicative_expr(parser_state)
            
            self.assertEqual(result, mock_unary_result)
            mock_unary.assert_called_once_with(parser_state)
            self.assertEqual(parser_state["pos"], 1)
    
    def test_operator_position_preserved(self):
        """Test that operator line and column are preserved in AST"""
        parser_state = self._create_parser_state([
            {"type": "NUMBER", "value": "5", "line": 1, "column": 1},
            {"type": "STAR", "value": "*", "line": 2, "column": 5},
            {"type": "NUMBER", "value": "3", "line": 2, "column": 7}
        ])
        
        mock_unary_results = [
            {"type": "LITERAL", "value": 5, "line": 1, "column": 1},
            {"type": "LITERAL", "value": 3, "line": 2, "column": 7}
        ]
        
        with patch("._parse_unary_expr_package._parse_unary_expr_src._parse_unary_expr") as mock_unary:
            mock_unary.side_effect = mock_unary_results
            
            result = _parse_multiplicative_expr(parser_state)
            
            self.assertEqual(result["line"], 2)
            self.assertEqual(result["column"], 5)
    
    def test_mixed_operators_sequence(self):
        """Test complex sequence with mixed operators"""
        parser_state = self._create_parser_state([
            {"type": "NUMBER", "value": "100", "line": 1, "column": 1},
            {"type": "STAR", "value": "*", "line": 1, "column": 5},
            {"type": "NUMBER", "value": "2", "line": 1, "column": 7},
            {"type": "PERCENT", "value": "%", "line": 1, "column": 9},
            {"type": "NUMBER", "value": "5", "line": 1, "column": 11},
            {"type": "SLASH", "value": "/", "line": 1, "column": 13},
            {"type": "NUMBER", "value": "3", "line": 1, "column": 15}
        ])
        
        mock_unary_results = [
            {"type": "LITERAL", "value": 100, "line": 1, "column": 1},
            {"type": "LITERAL", "value": 2, "line": 1, "column": 7},
            {"type": "LITERAL", "value": 5, "line": 1, "column": 11},
            {"type": "LITERAL", "value": 3, "line": 1, "column": 15}
        ]
        
        with patch("._parse_unary_expr_package._parse_unary_expr_src._parse_unary_expr") as mock_unary:
            mock_unary.side_effect = mock_unary_results
            
            result = _parse_multiplicative_expr(parser_state)
            
            # Left-associative: ((100 * 2) % 5) / 3
            self.assertEqual(result["operator"], "/")
            self.assertEqual(result["left"]["operator"], "%")
            self.assertEqual(result["left"]["left"]["operator"], "*")
            self.assertEqual(result["left"]["left"]["left"]["value"], 100)
            self.assertEqual(parser_state["pos"], 7)
            self.assertEqual(mock_unary.call_count, 4)


if __name__ == "__main__":
    unittest.main()

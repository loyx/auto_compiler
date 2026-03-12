import unittest
from unittest.mock import patch

# Relative import for the function under test
from ._parse_and_expr_src import _parse_and_expr


class TestParseAndExpr(unittest.TestCase):
    
    def test_single_expression_no_and(self):
        """Test parsing a single expression without AND operator."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.txt"
        }
        
        mock_ast = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        
        with patch("._parse_and_expr_src._parse_comparison_expr") as mock_parse_comparison:
            mock_parse_comparison.return_value = mock_ast
            
            result = _parse_and_expr(parser_state)
            
            self.assertEqual(result, mock_ast)
            self.assertEqual(parser_state["pos"], 0)
            mock_parse_comparison.assert_called_once()
    
    def test_single_and_expression(self):
        """Test parsing a single AND expression."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "KEYWORD", "value": "AND", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "y", "line": 1, "column": 7}
            ],
            "pos": 0,
            "filename": "test.txt"
        }
        
        left_ast = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        right_ast = {"type": "IDENTIFIER", "value": "y", "line": 1, "column": 7}
        
        with patch("._parse_and_expr_package._parse_and_expr_src._parse_comparison_expr") as mock_parse_comparison:
            mock_parse_comparison.side_effect = [left_ast, right_ast]
            
            result = _parse_and_expr(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["operator"], "AND")
            self.assertEqual(len(result["children"]), 2)
            self.assertEqual(result["children"][0], left_ast)
            self.assertEqual(result["children"][1], right_ast)
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 3)
            self.assertEqual(parser_state["pos"], 3)
            self.assertEqual(mock_parse_comparison.call_count, 2)
    
    def test_multiple_and_expressions_left_associative(self):
        """Test parsing multiple AND expressions with left-associative binding."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "KEYWORD", "value": "AND", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 7},
                {"type": "KEYWORD", "value": "AND", "line": 1, "column": 9},
                {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 13}
            ],
            "pos": 0,
            "filename": "test.txt"
        }
        
        ast_a = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        ast_b = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 7}
        ast_c = {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 13}
        
        with patch("._parse_and_expr_package._parse_and_expr_src._parse_comparison_expr") as mock_parse_comparison:
            mock_parse_comparison.side_effect = [ast_a, ast_b, ast_c]
            
            result = _parse_and_expr(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["operator"], "AND")
            self.assertEqual(len(result["children"]), 2)
            
            left_child = result["children"][0]
            self.assertEqual(left_child["type"], "BINARY_OP")
            self.assertEqual(left_child["operator"], "AND")
            self.assertEqual(left_child["children"][0], ast_a)
            self.assertEqual(left_child["children"][1], ast_b)
            
            self.assertEqual(result["children"][1], ast_c)
            self.assertEqual(parser_state["pos"], 5)
            self.assertEqual(mock_parse_comparison.call_count, 3)
    
    def test_empty_tokens(self):
        """Test parsing with empty token list."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.txt"
        }
        
        mock_ast = {"type": "EMPTY", "value": None, "line": 0, "column": 0}
        
        with patch("._parse_and_expr_package._parse_and_expr_src._parse_comparison_expr") as mock_parse_comparison:
            mock_parse_comparison.return_value = mock_ast
            
            result = _parse_and_expr(parser_state)
            
            self.assertEqual(result, mock_ast)
            self.assertEqual(parser_state["pos"], 0)
            mock_parse_comparison.assert_called_once()
    
    def test_and_keyword_not_consumed_when_not_present(self):
        """Test that AND keyword is not consumed when not present."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "+", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.txt"
        }
        
        mock_ast = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        
        with patch("._parse_and_expr_package._parse_and_expr_src._parse_comparison_expr") as mock_parse_comparison:
            mock_parse_comparison.return_value = mock_ast
            
            result = _parse_and_expr(parser_state)
            
            self.assertEqual(result, mock_ast)
            self.assertEqual(parser_state["pos"], 0)
            mock_parse_comparison.assert_called_once()
    
    def test_non_keyword_token_after_expression(self):
        """Test that non-KEYWORD token stops AND parsing."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "+", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "y", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.txt"
        }
        
        mock_ast = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        
        with patch("._parse_and_expr_package._parse_and_expr_src._parse_comparison_expr") as mock_parse_comparison:
            mock_parse_comparison.return_value = mock_ast
            
            result = _parse_and_expr(parser_state)
            
            self.assertEqual(result, mock_ast)
            self.assertEqual(parser_state["pos"], 0)
            mock_parse_comparison.assert_called_once()
    
    def test_wrong_keyword_value(self):
        """Test that KEYWORD with wrong value (not AND) stops parsing."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "KEYWORD", "value": "OR", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "y", "line": 1, "column": 6}
            ],
            "pos": 0,
            "filename": "test.txt"
        }
        
        mock_ast = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        
        with patch("._parse_and_expr_package._parse_and_expr_src._parse_comparison_expr") as mock_parse_comparison:
            mock_parse_comparison.return_value = mock_ast
            
            result = _parse_and_expr(parser_state)
            
            self.assertEqual(result, mock_ast)
            self.assertEqual(parser_state["pos"], 0)
            mock_parse_comparison.assert_called_once()
    
    def test_syntax_error_on_unexpected_end_after_and(self):
        """Test SyntaxError when token consumption fails after AND keyword."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "KEYWORD", "value": "AND", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.txt"
        }
        
        left_ast = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        
        with patch("._parse_and_expr_package._parse_and_expr_src._parse_comparison_expr") as mock_parse_comparison:
            mock_parse_comparison.side_effect = [left_ast, SyntaxError("Unexpected end of input in test.txt")]
            
            with self.assertRaises(SyntaxError) as context:
                _parse_and_expr(parser_state)
            
            self.assertIn("Unexpected end of input", str(context.exception))
            self.assertEqual(mock_parse_comparison.call_count, 2)
    
    def test_position_already_at_end(self):
        """Test parsing when position is already at end of tokens."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 1,
            "filename": "test.txt"
        }
        
        mock_ast = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        
        with patch("._parse_and_expr_package._parse_and_expr_src._parse_comparison_expr") as mock_parse_comparison:
            mock_parse_comparison.return_value = mock_ast
            
            result = _parse_and_expr(parser_state)
            
            self.assertEqual(result, mock_ast)
            self.assertEqual(parser_state["pos"], 1)
            mock_parse_comparison.assert_called_once()
    
    def test_and_with_different_line_numbers(self):
        """Test AND expression with tokens on different lines."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "KEYWORD", "value": "AND", "line": 2, "column": 1},
                {"type": "IDENTIFIER", "value": "y", "line": 3, "column": 1}
            ],
            "pos": 0,
            "filename": "test.txt"
        }
        
        left_ast = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        right_ast = {"type": "IDENTIFIER", "value": "y", "line": 3, "column": 1}
        
        with patch("._parse_and_expr_package._parse_and_expr_src._parse_comparison_expr") as mock_parse_comparison:
            mock_parse_comparison.side_effect = [left_ast, right_ast]
            
            result = _parse_and_expr(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["operator"], "AND")
            self.assertEqual(result["line"], 2)
            self.assertEqual(result["column"], 1)
            self.assertEqual(parser_state["pos"], 3)


if __name__ == "__main__":
    unittest.main()

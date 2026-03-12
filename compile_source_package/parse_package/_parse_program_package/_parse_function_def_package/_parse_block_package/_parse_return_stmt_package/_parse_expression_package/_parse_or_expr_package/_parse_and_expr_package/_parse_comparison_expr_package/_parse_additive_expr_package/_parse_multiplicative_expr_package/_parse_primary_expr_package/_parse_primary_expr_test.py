import unittest
from unittest.mock import patch

# Relative import for the function under test
from ._parse_primary_expr_src import _parse_primary_expr


class TestParsePrimaryExpr(unittest.TestCase):
    """Tests for _parse_primary_expr function."""
    
    def test_parse_identifier(self):
        """Test parsing an identifier token."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "x")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 1)
        self.assertNotIn("error", parser_state)
    
    def test_parse_number_literal(self):
        """Test parsing a number literal token."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "42", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "42")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 1)
        self.assertNotIn("error", parser_state)
    
    def test_parse_string_literal(self):
        """Test parsing a string literal token."""
        parser_state = {
            "tokens": [
                {"type": "STRING", "value": '"hello"', "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], '"hello"')
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 1)
        self.assertNotIn("error", parser_state)
    
    def test_parse_parenthesized_expression(self):
        """Test parsing a parenthesized expression."""
        parser_state = {
            "tokens": [
                {"type": "LPAREN", "value": "(", "line": 1, "column": 1},
                {"type": "NUMBER", "value": "42", "line": 1, "column": 2},
                {"type": "RPAREN", "value": ")", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch('._parse_additive_expr_package._parse_additive_expr_src._parse_additive_expr') as mock_parse:
            def side_effect(state):
                state["pos"] = 2
                return {"type": "LITERAL", "value": "42", "line": 1, "column": 2}
            
            mock_parse.side_effect = side_effect
            
            result = _parse_primary_expr(parser_state)
            
            self.assertEqual(result["type"], "LITERAL")
            self.assertEqual(result["value"], "42")
            self.assertEqual(parser_state["pos"], 3)
            self.assertNotIn("error", parser_state)
            mock_parse.assert_called_once()
    
    def test_empty_tokens(self):
        """Test parsing when there are no tokens available."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertIsNone(result["value"])
        self.assertEqual(result["line"], 0)
        self.assertEqual(result["column"], 0)
        self.assertEqual(parser_state["error"], "Expected primary expression")
    
    def test_pos_beyond_tokens(self):
        """Test parsing when position is beyond token list."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "42", "line": 1, "column": 1}
            ],
            "pos": 5,
            "filename": "test.py"
        }
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertIsNone(result["value"])
        self.assertEqual(result["line"], 0)
        self.assertEqual(result["column"], 0)
        self.assertEqual(parser_state["error"], "Expected primary expression")
    
    def test_invalid_token_type(self):
        """Test parsing with an invalid token type."""
        parser_state = {
            "tokens": [
                {"type": "PLUS", "value": "+", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertIsNone(result["value"])
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["error"], "Expected primary expression")
    
    def test_missing_rparen(self):
        """Test parsing parenthesized expression without closing parenthesis."""
        parser_state = {
            "tokens": [
                {"type": "LPAREN", "value": "(", "line": 1, "column": 1},
                {"type": "NUMBER", "value": "42", "line": 1, "column": 2}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch('._parse_additive_expr_package._parse_additive_expr_src._parse_additive_expr') as mock_parse:
            def side_effect(state):
                state["pos"] = 2
                return {"type": "LITERAL", "value": "42", "line": 1, "column": 2}
            
            mock_parse.side_effect = side_effect
            
            result = _parse_primary_expr(parser_state)
            
            self.assertEqual(result["type"], "ERROR")
            self.assertIsNone(result["value"])
            self.assertEqual(parser_state["error"], "Expected RPAREN")
            mock_parse.assert_called_once()
    
    def test_error_from_additive_expr(self):
        """Test that errors from _parse_additive_expr are propagated."""
        parser_state = {
            "tokens": [
                {"type": "LPAREN", "value": "(", "line": 1, "column": 1},
                {"type": "NUMBER", "value": "42", "line": 1, "column": 2},
                {"type": "RPAREN", "value": ")", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch('._parse_additive_expr_package._parse_additive_expr_src._parse_additive_expr') as mock_parse:
            def side_effect(state):
                state["pos"] = 2
                state["error"] = "Parse error in additive expr"
                return {"type": "ERROR", "value": None, "line": 1, "column": 2}
            
            mock_parse.side_effect = side_effect
            
            result = _parse_primary_expr(parser_state)
            
            self.assertEqual(result["type"], "ERROR")
            self.assertEqual(parser_state["error"], "Parse error in additive expr")
            mock_parse.assert_called_once()
    
    def test_multiple_tokens_remaining(self):
        """Test parsing when there are multiple tokens but only one is consumed."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 2},
                {"type": "NUMBER", "value": "1", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "x")
        self.assertEqual(parser_state["pos"], 1)
        self.assertNotIn("error", parser_state)
    
    def test_identifier_at_non_zero_pos(self):
        """Test parsing identifier when pos is not at start."""
        parser_state = {
            "tokens": [
                {"type": "PLUS", "value": "+", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "y", "line": 1, "column": 2},
                {"type": "NUMBER", "value": "5", "line": 1, "column": 3}
            ],
            "pos": 1,
            "filename": "test.py"
        }
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "y")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 2)
        self.assertEqual(parser_state["pos"], 2)
        self.assertNotIn("error", parser_state)


if __name__ == '__main__':
    unittest.main()

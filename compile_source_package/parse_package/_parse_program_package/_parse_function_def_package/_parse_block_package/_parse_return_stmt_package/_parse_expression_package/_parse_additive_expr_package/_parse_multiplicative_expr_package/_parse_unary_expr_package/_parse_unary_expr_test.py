import unittest
from unittest.mock import patch

# Import the function under test using relative import
from ._parse_unary_expr_src import _parse_unary_expr


class TestParseUnaryExpr(unittest.TestCase):
    """Tests for _parse_unary_expr function."""
    
    def test_plus_operator(self):
        """Test parsing unary plus operator."""
        tokens = [
            {"type": "PLUS", "value": "+", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 2},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch('._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr') as mock_parse:
            mock_parse.return_value = {
                "type": "IDENTIFIER",
                "value": "x",
                "line": 1,
                "column": 2
            }
            
            result = _parse_unary_expr(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "+")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(result["children"][0]["type"], "IDENTIFIER")
            self.assertEqual(parser_state["pos"], 1)
    
    def test_minus_operator(self):
        """Test parsing unary minus operator."""
        tokens = [
            {"type": "MINUS", "value": "-", "line": 1, "column": 1},
            {"type": "LITERAL", "value": "5", "line": 1, "column": 2},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch('._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr') as mock_parse:
            mock_parse.return_value = {
                "type": "LITERAL",
                "value": "5",
                "line": 1,
                "column": 2
            }
            
            result = _parse_unary_expr(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "-")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(parser_state["pos"], 1)
    
    def test_not_operator(self):
        """Test parsing unary NOT operator."""
        tokens = [
            {"type": "NOT", "value": "!", "line": 2, "column": 5},
            {"type": "IDENTIFIER", "value": "flag", "line": 2, "column": 6},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch('._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr') as mock_parse:
            mock_parse.return_value = {
                "type": "IDENTIFIER",
                "value": "flag",
                "line": 2,
                "column": 6
            }
            
            result = _parse_unary_expr(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "!")
            self.assertEqual(result["line"], 2)
            self.assertEqual(result["column"], 5)
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(parser_state["pos"], 1)
    
    def test_chained_unary_operators(self):
        """Test parsing chained unary operators (e.g., --x)."""
        tokens = [
            {"type": "MINUS", "value": "-", "line": 1, "column": 1},
            {"type": "PLUS", "value": "+", "line": 1, "column": 2},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 3},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        def mock_parse_side_effect(state):
            if state["pos"] == 1:
                state["pos"] += 1
                return {
                    "type": "UNARY_OP",
                    "value": "+",
                    "children": [{
                        "type": "IDENTIFIER",
                        "value": "x",
                        "line": 1,
                        "column": 3
                    }],
                    "line": 1,
                    "column": 2
                }
            else:
                return {
                    "type": "IDENTIFIER",
                    "value": "x",
                    "line": 1,
                    "column": 3
                }
        
        with patch('._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr') as mock_parse:
            mock_parse.side_effect = mock_parse_side_effect
            
            result = _parse_unary_expr(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "-")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            self.assertEqual(len(result["children"]), 1)
            
            inner_unary = result["children"][0]
            self.assertEqual(inner_unary["type"], "UNARY_OP")
            self.assertEqual(inner_unary["value"], "+")
            self.assertEqual(inner_unary["line"], 1)
            self.assertEqual(inner_unary["column"], 2)
            
            self.assertEqual(parser_state["pos"], 2)
    
    def test_non_unary_operator_delegates_to_primary(self):
        """Test that non-unary operators delegate to _parse_primary_expr."""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        expected_result = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 1
        }
        
        with patch('._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr') as mock_parse:
            mock_parse.return_value = expected_result
            
            result = _parse_unary_expr(parser_state)
            
            mock_parse.assert_called_once_with(parser_state)
            self.assertEqual(result, expected_result)
            self.assertEqual(parser_state["pos"], 0)
    
    def test_empty_tokens_raises_syntax_error(self):
        """Test that empty token list raises SyntaxError."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_unary_expr(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))
        self.assertEqual(parser_state["pos"], 0)
    
    def test_end_of_input_raises_syntax_error(self):
        """Test that reaching end of input raises SyntaxError."""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 1,
            "filename": "test.py"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_unary_expr(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))
        self.assertEqual(parser_state["pos"], 1)
    
    def test_line_column_preservation(self):
        """Test that line and column information is preserved."""
        tokens = [
            {"type": "NOT", "value": "!", "line": 5, "column": 10},
            {"type": "IDENTIFIER", "value": "flag", "line": 5, "column": 11},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch('._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr') as mock_parse:
            mock_parse.return_value = {
                "type": "IDENTIFIER",
                "value": "flag",
                "line": 5,
                "column": 11
            }
            
            result = _parse_unary_expr(parser_state)
            
            self.assertEqual(result["line"], 5)
            self.assertEqual(result["column"], 10)
    
    def test_mixed_unary_operators(self):
        """Test parsing mixed unary operators."""
        tokens = [
            {"type": "NOT", "value": "!", "line": 1, "column": 1},
            {"type": "MINUS", "value": "-", "line": 1, "column": 2},
            {"type": "PLUS", "value": "+", "line": 1, "column": 3},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 4},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        def mock_parse_side_effect(state):
            if state["pos"] == 1:
                state["pos"] += 1
                return {
                    "type": "UNARY_OP",
                    "value": "-",
                    "children": [{
                        "type": "UNARY_OP",
                        "value": "+",
                        "children": [{
                            "type": "IDENTIFIER",
                            "value": "x",
                            "line": 1,
                            "column": 4
                        }],
                        "line": 1,
                        "column": 3
                    }],
                    "line": 1,
                    "column": 2
                }
            else:
                return {
                    "type": "IDENTIFIER",
                    "value": "x",
                    "line": 1,
                    "column": 4
                }
        
        with patch('._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr') as mock_parse:
            mock_parse.side_effect = mock_parse_side_effect
            
            result = _parse_unary_expr(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "!")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            self.assertEqual(parser_state["pos"], 1)
    
    def test_binary_operator_delegates_to_primary(self):
        """Test that binary operators like PLUS in expression context delegate to primary."""
        tokens = [
            {"type": "PLUS", "value": "+", "line": 1, "column": 1},
            {"type": "PLUS", "value": "+", "line": 1, "column": 2},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 1,
            "filename": "test.py"
        }
        
        expected_result = {
            "type": "LITERAL",
            "value": "5",
            "line": 1,
            "column": 2
        }
        
        with patch('._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr') as mock_parse:
            mock_parse.return_value = expected_result
            
            result = _parse_unary_expr(parser_state)
            
            mock_parse.assert_called_once_with(parser_state)
            self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()

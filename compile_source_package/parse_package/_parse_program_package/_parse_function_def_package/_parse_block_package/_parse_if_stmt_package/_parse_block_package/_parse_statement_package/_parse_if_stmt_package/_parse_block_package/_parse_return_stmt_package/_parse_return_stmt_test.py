import unittest
from unittest.mock import patch

# Relative import for the function under test
from ._parse_return_stmt_src import _parse_return_stmt


class TestParseReturnStmt(unittest.TestCase):
    """Test cases for _parse_return_stmt function."""
    
    def test_return_without_value(self):
        """Test parsing 'return;' statement without return value."""
        tokens = [
            {"type": "RETURN", "value": "return", "line": 1, "column": 5},
            {"type": "SEMICOLON", "value": ";", "line": 1, "column": 11},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_return_stmt(parser_state)
        
        self.assertEqual(result["type"], "RETURN")
        self.assertIsNone(result["value"])
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 5)
        self.assertEqual(parser_state["pos"], 2)
    
    def test_return_with_expression(self):
        """Test parsing 'return expression;' statement with return value."""
        tokens = [
            {"type": "RETURN", "value": "return", "line": 1, "column": 5},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 12},
            {"type": "SEMICOLON", "value": ";", "line": 1, "column": 13},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        mock_ast = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 12}
        
        def mock_parse_expression(state):
            state["pos"] = 2  # Advance past the identifier
            return mock_ast
        
        with patch("._parse_expression_package._parse_expression_src._parse_expression", side_effect=mock_parse_expression) as mock_parse_expr:
            result = _parse_return_stmt(parser_state)
            
            self.assertEqual(result["type"], "RETURN")
            self.assertEqual(result["value"], mock_ast)
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 5)
            self.assertEqual(parser_state["pos"], 3)
            mock_parse_expr.assert_called_once()
    
    def test_unexpected_eof_after_return(self):
        """Test SyntaxError when EOF occurs immediately after RETURN."""
        tokens = [
            {"type": "RETURN", "value": "return", "line": 1, "column": 5},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_return_stmt(parser_state)
        
        self.assertIn("unexpected end of file", str(context.exception))
        self.assertIn("test.py:1:5", str(context.exception))
    
    def test_missing_semicolon_after_expression(self):
        """Test SyntaxError when SEMICOLON is missing after return expression."""
        tokens = [
            {"type": "RETURN", "value": "return", "line": 1, "column": 5},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 12},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        mock_ast = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 12}
        
        def mock_parse_expression(state):
            state["pos"] = 2  # Advance past the identifier (to EOF)
            return mock_ast
        
        with patch("._parse_expression_package._parse_expression_src._parse_expression", side_effect=mock_parse_expression):
            with self.assertRaises(SyntaxError) as context:
                _parse_return_stmt(parser_state)
            
            self.assertIn("expected ';'", str(context.exception))
            self.assertIn("test.py:1:5", str(context.exception))
    
    def test_return_with_default_filename(self):
        """Test parsing return statement when filename is not provided."""
        tokens = [
            {"type": "RETURN", "value": "return", "line": 2, "column": 10},
            {"type": "SEMICOLON", "value": ";", "line": 2, "column": 16},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0
        }
        
        result = _parse_return_stmt(parser_state)
        
        self.assertEqual(result["type"], "RETURN")
        self.assertIsNone(result["value"])
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 10)
        self.assertEqual(parser_state["pos"], 2)
    
    def test_return_at_end_of_tokens_after_expression(self):
        """Test SyntaxError when tokens end after expression without SEMICOLON."""
        tokens = [
            {"type": "RETURN", "value": "return", "line": 1, "column": 5},
            {"type": "NUMBER", "value": "42", "line": 1, "column": 12},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        mock_ast = {"type": "NUMBER", "value": "42", "line": 1, "column": 12}
        
        def mock_parse_expression(state):
            state["pos"] = 2  # Advance past the number (to EOF)
            return mock_ast
        
        with patch("._parse_expression_package._parse_expression_src._parse_expression", side_effect=mock_parse_expression):
            with self.assertRaises(SyntaxError) as context:
                _parse_return_stmt(parser_state)
            
            self.assertIn("expected ';'", str(context.exception))
    
    def test_return_with_complex_expression(self):
        """Test parsing return with complex expression (mocked)."""
        tokens = [
            {"type": "RETURN", "value": "return", "line": 3, "column": 1},
            {"type": "IDENTIFIER", "value": "x", "line": 3, "column": 8},
            {"type": "PLUS", "value": "+", "line": 3, "column": 9},
            {"type": "NUMBER", "value": "1", "line": 3, "column": 10},
            {"type": "SEMICOLON", "value": ";", "line": 3, "column": 11},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        mock_ast = {
            "type": "BINARY_OP",
            "value": "+",
            "children": [
                {"type": "IDENTIFIER", "value": "x", "line": 3, "column": 8},
                {"type": "NUMBER", "value": "1", "line": 3, "column": 10}
            ],
            "line": 3,
            "column": 8
        }
        
        def mock_parse_expression(state):
            state["pos"] = 4  # Advance past the expression (to SEMICOLON)
            return mock_ast
        
        with patch("._parse_expression_package._parse_expression_src._parse_expression", side_effect=mock_parse_expression):
            result = _parse_return_stmt(parser_state)
            
            self.assertEqual(result["type"], "RETURN")
            self.assertEqual(result["value"], mock_ast)
            self.assertEqual(result["line"], 3)
            self.assertEqual(result["column"], 1)
            self.assertEqual(parser_state["pos"], 5)
    
    def test_return_position_advancement(self):
        """Test that parser_state position is correctly advanced."""
        tokens = [
            {"type": "RETURN", "value": "return", "line": 1, "column": 5},
            {"type": "SEMICOLON", "value": ";", "line": 1, "column": 11},
            {"type": "OTHER", "value": "other", "line": 1, "column": 12},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_return_stmt(parser_state)
        
        # Position should be at 2 (after RETURN and SEMICOLON)
        self.assertEqual(parser_state["pos"], 2)
        # Next token should be OTHER
        self.assertEqual(tokens[parser_state["pos"]]["type"], "OTHER")


if __name__ == "__main__":
    unittest.main()

import unittest
from unittest.mock import patch, MagicMock
from ._consume_token_src import _consume_token, _peek_token


class TestConsumeToken(unittest.TestCase):
    
    def test_consume_token_success(self):
        """Test successful token consumption when type matches"""
        parser_state = {
            "tokens": [
                {"type": "RETURN", "value": "return", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _consume_token(parser_state, "RETURN")
        
        self.assertEqual(result["pos"], 1)
        self.assertEqual(parser_state["pos"], 0)  # Original unchanged
        self.assertEqual(len(result["tokens"]), 1)
    
    def test_consume_token_eof(self):
        """Test SyntaxError when reaching end of file"""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, "RETURN")
        
        self.assertIn("Unexpected end of file", str(context.exception))
    
    def test_consume_token_type_mismatch(self):
        """Test SyntaxError when token type doesn't match expected"""
        parser_state = {
            "tokens": [
                {"type": "IF", "value": "if", "line": 5, "column": 10}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, "RETURN")
        
        self.assertIn("Expected token 'RETURN'", str(context.exception))
        self.assertIn("got 'IF'", str(context.exception))
        self.assertIn("line 5", str(context.exception))
    
    def test_consume_token_preserves_original_state(self):
        """Test that original parser_state is not modified"""
        parser_state = {
            "tokens": [
                {"type": "RETURN", "value": "return", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _consume_token(parser_state, "RETURN")
        
        # Original should be unchanged
        self.assertEqual(parser_state["pos"], 0)
        # Result should have updated pos
        self.assertEqual(result["pos"], 1)
        # Other fields should be copied
        self.assertEqual(result["filename"], "test.py")
        self.assertEqual(result["tokens"], parser_state["tokens"])
    
    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_return_stmt_package._consume_token_package._consume_token_src._peek_token')
    def test_consume_token_with_mocked_peek(self, mock_peek):
        """Test with mocked _peek_token function"""
        mock_peek.return_value = {"type": "SEMICOLON", "value": ";", "line": 3, "column": 15}
        
        parser_state = {
            "tokens": [],
            "pos": 2,
            "filename": "test.py"
        }
        
        result = _consume_token(parser_state, "SEMICOLON")
        
        mock_peek.assert_called_once_with(parser_state)
        self.assertEqual(result["pos"], 3)
    
    @patch('_consume_token_package._consume_token_src._peek_token')
    def test_consume_token_mocked_eof(self, mock_peek):
        """Test EOF case with mocked _peek_token returning None"""
        mock_peek.return_value = None
        
        parser_state = {
            "tokens": [{"type": "RETURN", "value": "return", "line": 1, "column": 1}],
            "pos": 1,
            "filename": "test.py"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, "RETURN")
        
        self.assertIn("Unexpected end of file", str(context.exception))
        mock_peek.assert_called_once_with(parser_state)
    
    @patch('_consume_token_package._consume_token_src._peek_token')
    def test_consume_token_mocked_mismatch(self, mock_peek):
        """Test type mismatch with mocked _peek_token"""
        mock_peek.return_value = {"type": "IF", "value": "if", "line": 10, "column": 5}
        
        parser_state = {
            "tokens": [],
            "pos": 5,
            "filename": "test.py"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, "RETURN")
        
        self.assertIn("Expected token 'RETURN'", str(context.exception))
        self.assertIn("got 'IF'", str(context.exception))
        self.assertIn("line 10", str(context.exception))
        mock_peek.assert_called_once_with(parser_state)
    
    def test_consume_token_at_end_of_tokens(self):
        """Test when pos is at or beyond tokens length"""
        parser_state = {
            "tokens": [
                {"type": "RETURN", "value": "return", "line": 1, "column": 1}
            ],
            "pos": 1,  # Already at end
            "filename": "test.py"
        }
        
        with self.assertRaises(SyntaxError):
            _consume_token(parser_state, "RETURN")
    
    def test_consume_token_multiple_successive_calls(self):
        """Test multiple successive token consumptions"""
        parser_state = {
            "tokens": [
                {"type": "RETURN", "value": "return", "line": 1, "column": 1},
                {"type": "SEMICOLON", "value": ";", "line": 1, "column": 7},
                {"type": "EOF", "value": "", "line": 1, "column": 8}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        # First consumption
        result1 = _consume_token(parser_state, "RETURN")
        self.assertEqual(result1["pos"], 1)
        
        # Second consumption (using updated state)
        result2 = _consume_token(result1, "SEMICOLON")
        self.assertEqual(result2["pos"], 2)
        
        # Third consumption
        result3 = _consume_token(result2, "EOF")
        self.assertEqual(result3["pos"], 3)
    
    def test_consume_token_with_missing_token_fields(self):
        """Test handling of tokens with missing optional fields"""
        parser_state = {
            "tokens": [
                {"type": "RETURN", "value": "return"}  # No line/column
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _consume_token(parser_state, "RETURN")
        
        self.assertEqual(result["pos"], 1)
    
    def test_consume_token_case_sensitive(self):
        """Test that token type matching is case-sensitive"""
        parser_state = {
            "tokens": [
                {"type": "return", "value": "return", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with self.assertRaises(SyntaxError):
            _consume_token(parser_state, "RETURN")  # uppercase expected


if __name__ == "__main__":
    unittest.main()

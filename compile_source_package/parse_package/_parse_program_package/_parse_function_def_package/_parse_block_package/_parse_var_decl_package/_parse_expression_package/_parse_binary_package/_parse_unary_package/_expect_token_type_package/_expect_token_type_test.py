import unittest
from unittest.mock import patch

# Ensure relative imports work from the same package
from ._expect_token_type_src import _expect_token_type


class TestExpectTokenType(unittest.TestCase):
    
    def test_token_type_matches_should_advance(self):
        """Happy path: token type matches, parser should advance"""
        parser_state = {
            "tokens": [{"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch('._expect_token_type_src._get_current_token') as mock_get_token, \
             patch('._expect_token_type_src._advance_parser') as mock_advance:
            
            mock_get_token.return_value = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            
            _expect_token_type(parser_state, "IDENTIFIER", "identifier")
            
            mock_get_token.assert_called_once_with(parser_state)
            mock_advance.assert_called_once_with(parser_state)
    
    def test_token_is_none_should_raise_syntax_error(self):
        """EOF case: token is None, should raise SyntaxError"""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch('._expect_token_type_src._get_current_token') as mock_get_token, \
             patch('._expect_token_type_src._advance_parser') as mock_advance:
            
            mock_get_token.return_value = None
            
            with self.assertRaises(SyntaxError) as context:
                _expect_token_type(parser_state, "IDENTIFIER", "identifier")
            
            self.assertIn("期望 'identifier'，但得到 'EOF'", str(context.exception))
            mock_advance.assert_not_called()
    
    def test_token_type_mismatch_should_raise_syntax_error(self):
        """Token type doesn't match, should raise SyntaxError"""
        parser_state = {
            "tokens": [{"type": "NUMBER", "value": "42", "line": 2, "column": 5}],
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch('._expect_token_type_src._get_current_token') as mock_get_token, \
             patch('._expect_token_type_src._advance_parser') as mock_advance:
            
            mock_get_token.return_value = {"type": "NUMBER", "value": "42", "line": 2, "column": 5}
            
            with self.assertRaises(SyntaxError) as context:
                _expect_token_type(parser_state, "IDENTIFIER", "identifier")
            
            self.assertIn("期望 'identifier'，但得到 'NUMBER'", str(context.exception))
            mock_advance.assert_not_called()
    
    def test_error_message_contains_file_info(self):
        """Error message should contain filename, line, and column"""
        parser_state = {
            "tokens": [{"type": "SEMICOLON", "value": ";", "line": 10, "column": 20}],
            "pos": 0,
            "filename": "main.c"
        }
        
        with patch('._expect_token_type_src._get_current_token') as mock_get_token, \
             patch('._expect_token_type_src._advance_parser') as mock_advance:
            
            mock_get_token.return_value = {"type": "SEMICOLON", "value": ";", "line": 10, "column": 20}
            
            with self.assertRaises(SyntaxError) as context:
                _expect_token_type(parser_state, "LPAREN", "(")
            
            error_msg = str(context.exception)
            self.assertIn("main.c:10:20", error_msg)
            self.assertIn("期望 '('，但得到 'SEMICOLON'", error_msg)
            mock_advance.assert_not_called()
    
    def test_unknown_filename_default(self):
        """When filename is not provided, should use '<unknown>'"""
        parser_state = {
            "tokens": [{"type": "NUMBER", "value": "1", "line": 1, "column": 1}],
            "pos": 0
        }
        
        with patch('._expect_token_type_src._get_current_token') as mock_get_token:
            mock_get_token.return_value = {"type": "NUMBER", "value": "1", "line": 1, "column": 1}
            
            with self.assertRaises(SyntaxError) as context:
                _expect_token_type(parser_state, "STRING", "string")
            
            self.assertIn("<unknown>:1:1", str(context.exception))
    
    def test_multiple_token_types(self):
        """Test various token types matching"""
        test_cases = [
            ("LPAREN", "(", {"type": "LPAREN", "value": "(", "line": 1, "column": 1}),
            ("RPAREN", ")", {"type": "RPAREN", "value": ")", "line": 1, "column": 5}),
            ("SEMICOLON", ";", {"type": "SEMICOLON", "value": ";", "line": 2, "column": 10}),
            ("NUMBER", "number", {"type": "NUMBER", "value": "42", "line": 3, "column": 1}),
        ]
        
        for expected_type, expected_display, token in test_cases:
            with self.subTest(expected_type=expected_type):
                parser_state = {
                    "tokens": [token],
                    "pos": 0,
                    "filename": "test.c"
                }
                
                with patch('._get_current_token_package._get_current_token_src._get_current_token') as mock_get_token, \
                     patch('._advance_parser_package._advance_parser_src._advance_parser') as mock_advance:
                    
                    mock_get_token.return_value = token
                    
                    _expect_token_type(parser_state, expected_type, expected_display)
                    
                    mock_advance.assert_called_once()


if __name__ == '__main__':
    unittest.main()

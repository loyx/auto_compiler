"""
Unit tests for _consume_token function.
"""

import unittest
from unittest.mock import patch
from typing import Dict, Any

# Relative import from the same package
from ._consume_token_src import _consume_token


class TestConsumeToken(unittest.TestCase):
    """Test cases for _consume_token function."""

    def setUp(self):
        """Set up test fixtures."""
        self.sample_token: Dict[str, Any] = {
            "type": "PLUS",
            "value": "+",
            "line": 1,
            "column": 5
        }
        self.sample_parser_state: Dict[str, Any] = {
            "tokens": [self.sample_token],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }

    def test_consume_token_success_matching_type(self):
        """Test successful token consumption when type matches."""
        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_expression_package._consume_token_package._peek_token_package._peek_token_src._peek_token') as mock_peek:
            mock_peek.return_value = self.sample_token
            
            token, updated_state = _consume_token(self.sample_parser_state, "PLUS")
            
            # Verify returned token
            self.assertEqual(token, self.sample_token)
            self.assertEqual(token["type"], "PLUS")
            
            # Verify pos is incremented
            self.assertEqual(updated_state["pos"], 1)
            
            # Verify original state is not modified
            self.assertEqual(self.sample_parser_state["pos"], 0)
            
            # Verify other fields are preserved
            self.assertEqual(updated_state["filename"], "test.py")
            self.assertEqual(updated_state["error"], "")
            
            # Verify _peek_token was called with correct argument
            mock_peek.assert_called_once_with(self.sample_parser_state)

    def test_consume_token_different_type(self):
        """Test token consumption fails when type doesn't match."""
        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_expression_package._consume_token_package._peek_token_package._peek_token_src._peek_token') as mock_peek:
            mock_peek.return_value = self.sample_token
            
            with self.assertRaises(SyntaxError) as context:
                _consume_token(self.sample_parser_state, "MINUS")
            
            self.assertEqual(str(context.exception), "Expected MINUS but got PLUS")
            mock_peek.assert_called_once_with(self.sample_parser_state)

    def test_consume_token_none_token_end_of_input(self):
        """Test token consumption fails when no token available (end of input)."""
        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_expression_package._consume_token_package._peek_token_package._peek_token_src._peek_token') as mock_peek:
            mock_peek.return_value = None
            
            with self.assertRaises(SyntaxError) as context:
                _consume_token(self.sample_parser_state, "PLUS")
            
            self.assertEqual(str(context.exception), "Unexpected end of input")
            mock_peek.assert_called_once_with(self.sample_parser_state)

    def test_consume_token_preserves_original_state(self):
        """Test that original parser_state is not modified."""
        with patch('._consume_token_package._consume_token_src._peek_token') as mock_peek:
            mock_peek.return_value = self.sample_token
            
            original_pos = self.sample_parser_state["pos"]
            _consume_token(self.sample_parser_state, "PLUS")
            
            # Original state should remain unchanged
            self.assertEqual(self.sample_parser_state["pos"], original_pos)
            self.assertEqual(self.sample_parser_state["pos"], 0)

    def test_consume_token_with_different_token_types(self):
        """Test token consumption with various token types."""
        token_types = ["IDENTIFIER", "NUMBER", "STRING", "LPAREN", "RPAREN", "EOF"]
        
        for token_type in token_types:
            with self.subTest(token_type=token_type):
                token = {
                    "type": token_type,
                    "value": "test",
                    "line": 1,
                    "column": 1
                }
                parser_state = {
                    "tokens": [token],
                    "pos": 5,
                    "filename": "test.py",
                    "error": ""
                }
                
                with patch('._consume_token_package._consume_token_src._peek_token') as mock_peek:
                    mock_peek.return_value = token
                    
                    result_token, updated_state = _consume_token(parser_state, token_type)
                    
                    self.assertEqual(result_token["type"], token_type)
                    self.assertEqual(updated_state["pos"], 6)

    def test_consume_token_at_different_positions(self):
        """Test token consumption at different position values."""
        for pos in [0, 1, 10, 100]:
            with self.subTest(pos=pos):
                parser_state = {
                    "tokens": [self.sample_token],
                    "pos": pos,
                    "filename": "test.py",
                    "error": ""
                }
                
                with patch('._consume_token_package._consume_token_src._peek_token') as mock_peek:
                    mock_peek.return_value = self.sample_token
                    
                    _, updated_state = _consume_token(parser_state, "PLUS")
                    
                    self.assertEqual(updated_state["pos"], pos + 1)

    def test_consume_token_state_copy_independence(self):
        """Test that returned state is independent copy."""
        with patch('._consume_token_package._consume_token_src._peek_token') as mock_peek:
            mock_peek.return_value = self.sample_token
            
            _, updated_state = _consume_token(self.sample_parser_state, "PLUS")
            
            # Modify updated state
            updated_state["pos"] = 999
            updated_state["filename"] = "modified.py"
            
            # Original state should remain unchanged
            self.assertEqual(self.sample_parser_state["pos"], 0)
            self.assertEqual(self.sample_parser_state["filename"], "test.py")

    def test_consume_token_empty_string_type(self):
        """Test token consumption with empty string as expected type."""
        token = {
            "type": "",
            "value": "",
            "line": 1,
            "column": 1
        }
        parser_state = {
            "tokens": [token],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        with patch('._consume_token_package._consume_token_src._peek_token') as mock_peek:
            mock_peek.return_value = token
            
            result_token, updated_state = _consume_token(parser_state, "")
            
            self.assertEqual(result_token["type"], "")
            self.assertEqual(updated_state["pos"], 1)

    def test_consume_token_case_sensitive_type(self):
        """Test that token type matching is case-sensitive."""
        with patch('._consume_token_package._consume_token_src._peek_token') as mock_peek:
            mock_peek.return_value = self.sample_token
            
            # PLUS != plus (case sensitive)
            with self.assertRaises(SyntaxError) as context:
                _consume_token(self.sample_parser_state, "plus")
            
            self.assertEqual(str(context.exception), "Expected plus but got PLUS")


if __name__ == "__main__":
    unittest.main()

import unittest
from unittest.mock import patch

# Relative import from the same package
from ._consume_token_src import _consume_token


class TestConsumeToken(unittest.TestCase):
    """Test cases for _consume_token function."""
    
    def test_consume_token_without_expected_type(self):
        """Test consuming a token without specifying expected type."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_block_package._consume_token_package._consume_token_src._peek_token") as mock_peek:
            mock_peek.return_value = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            
            result = _consume_token(parser_state)
            
            # Verify pos was incremented
            self.assertEqual(result["pos"], 1)
            # Verify original state was not mutated
            self.assertEqual(parser_state["pos"], 0)
            # Verify other fields are preserved
            self.assertEqual(result["filename"], "test.py")
            self.assertEqual(result["tokens"], parser_state["tokens"])
    
    def test_consume_token_with_matching_expected_type(self):
        """Test consuming a token with matching expected type."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "42", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_block_package._consume_token_package._consume_token_src._peek_token") as mock_peek:
            mock_peek.return_value = {"type": "NUMBER", "value": "42", "line": 1, "column": 1}
            
            result = _consume_token(parser_state, expected_type="NUMBER")
            
            self.assertEqual(result["pos"], 1)
            self.assertEqual(parser_state["pos"], 0)
    
    def test_eof_without_expected_type(self):
        """Test EOF case without expected type."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_block_package._consume_token_package._consume_token_src._peek_token") as mock_peek:
            mock_peek.return_value = None
            
            result = _consume_token(parser_state)
            
            # Should return a copy without incrementing pos
            self.assertEqual(result["pos"], 0)
            self.assertEqual(parser_state["pos"], 0)
            self.assertIsNot(result, parser_state)
    
    def test_eof_with_expected_type_raises_error(self):
        """Test EOF case with expected type raises SyntaxError."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_block_package._consume_token_package._consume_token_src._peek_token") as mock_peek:
            mock_peek.return_value = None
            
            with self.assertRaises(SyntaxError) as context:
                _consume_token(parser_state, expected_type="IDENTIFIER")
            
            self.assertIn("Unexpected end of input", str(context.exception))
            self.assertIn("IDENTIFIER", str(context.exception))
    
    def test_token_type_mismatch_raises_error(self):
        """Test token type mismatch raises SyntaxError."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "42", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_block_package._consume_token_package._consume_token_src._peek_token") as mock_peek:
            mock_peek.return_value = {"type": "NUMBER", "value": "42", "line": 1, "column": 1}
            
            with self.assertRaises(SyntaxError) as context:
                _consume_token(parser_state, expected_type="IDENTIFIER")
            
            self.assertIn("Expected token type", str(context.exception))
            self.assertIn("IDENTIFIER", str(context.exception))
            self.assertIn("NUMBER", str(context.exception))
    
    def test_pos_increment_from_non_zero(self):
        """Test pos increment when starting from non-zero position."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 5,
            "filename": "test.py"
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_block_package._consume_token_package._consume_token_src._peek_token") as mock_peek:
            mock_peek.return_value = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            
            result = _consume_token(parser_state)
            
            self.assertEqual(result["pos"], 6)
            self.assertEqual(parser_state["pos"], 5)
    
    def test_parser_state_is_copied_not_mutated(self):
        """Test that parser_state is copied, not mutated."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py",
            "extra_field": "value"
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._parse_block_package._consume_token_package._consume_token_src._peek_token") as mock_peek:
            mock_peek.return_value = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            
            result = _consume_token(parser_state)
            
            # Verify it's a different object
            self.assertIsNot(result, parser_state)
            # Verify original is unchanged
            self.assertEqual(parser_state["pos"], 0)
            # Verify all fields are preserved in result
            self.assertEqual(result["extra_field"], "value")


if __name__ == "__main__":
    unittest.main()
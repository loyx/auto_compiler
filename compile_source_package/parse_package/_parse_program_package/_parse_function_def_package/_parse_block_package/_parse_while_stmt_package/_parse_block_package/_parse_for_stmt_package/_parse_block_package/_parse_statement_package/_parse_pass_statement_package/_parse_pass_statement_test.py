import unittest
from ._parse_pass_statement_src import _parse_pass_statement


class TestParsePassStatement(unittest.TestCase):
    """Test cases for _parse_pass_statement function."""
    
    def test_happy_path_pass_semicolon(self):
        """Test parsing valid pass statement with semicolon."""
        parser_state = {
            "tokens": [
                {"type": "PASS", "value": "pass", "line": 1, "column": 0},
                {"type": "SEMICOLON", "value": ";", "line": 1, "column": 4},
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_pass_statement(parser_state)
        
        # Verify AST node structure
        self.assertEqual(result["type"], "PASS_STMT")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 0)
        self.assertEqual(result["children"], [])
        
        # Verify parser state updated
        self.assertEqual(parser_state["pos"], 2)
    
    def test_missing_semicolon_at_end(self):
        """Test SyntaxError when pass is at end of tokens (no semicolon)."""
        parser_state = {
            "tokens": [
                {"type": "PASS", "value": "pass", "line": 1, "column": 0},
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_pass_statement(parser_state)
        
        self.assertIn("Expected ';' after pass statement", str(context.exception))
    
    def test_wrong_token_after_pass(self):
        """Test SyntaxError when wrong token type follows pass."""
        parser_state = {
            "tokens": [
                {"type": "PASS", "value": "pass", "line": 1, "column": 0},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 5},
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_pass_statement(parser_state)
        
        self.assertIn("Expected ';' after pass statement", str(context.exception))
    
    def test_pos_updated_correctly_with_more_tokens(self):
        """Test that parser state position is correctly updated when more tokens follow."""
        parser_state = {
            "tokens": [
                {"type": "PASS", "value": "pass", "line": 2, "column": 4},
                {"type": "SEMICOLON", "value": ";", "line": 2, "column": 8},
                {"type": "IDENTIFIER", "value": "x", "line": 3, "column": 0},
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_pass_statement(parser_state)
        
        # pos should point to next token after semicolon
        self.assertEqual(parser_state["pos"], 2)
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 4)
    
    def test_pass_at_different_line_column(self):
        """Test pass statement at different line and column positions."""
        parser_state = {
            "tokens": [
                {"type": "PASS", "value": "pass", "line": 10, "column": 20},
                {"type": "SEMICOLON", "value": ";", "line": 10, "column": 24},
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_pass_statement(parser_state)
        
        self.assertEqual(result["line"], 10)
        self.assertEqual(result["column"], 20)
        self.assertEqual(parser_state["pos"], 2)
    
    def test_empty_tokens_list(self):
        """Test behavior when tokens list is empty (edge case)."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }
        
        # This should raise an error when trying to access tokens[0]
        with self.assertRaises(IndexError):
            _parse_pass_statement(parser_state)


if __name__ == "__main__":
    unittest.main()

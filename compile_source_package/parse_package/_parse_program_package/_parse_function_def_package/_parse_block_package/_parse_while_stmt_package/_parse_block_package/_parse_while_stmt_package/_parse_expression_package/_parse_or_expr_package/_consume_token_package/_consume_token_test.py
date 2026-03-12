import unittest

from ._consume_token_src import _consume_token


class TestConsumeToken(unittest.TestCase):
    """Test cases for _consume_token function."""
    
    def test_consume_token_normal(self):
        """Test consuming a token when position is valid."""
        parser_state = {
            "tokens": [
                {"type": "IDENT", "value": "x", "line": 1, "column": 1},
                {"type": "OP", "value": "+", "line": 1, "column": 2},
                {"type": "NUMBER", "value": "5", "line": 1, "column": 3},
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _consume_token(parser_state)
        
        # Original state should not be modified
        self.assertEqual(parser_state["pos"], 0)
        # New state should have pos incremented
        self.assertEqual(result["pos"], 1)
        # Tokens should remain the same
        self.assertEqual(result["tokens"], parser_state["tokens"])
        # Other fields should be preserved
        self.assertEqual(result["filename"], "test.py")
    
    def test_consume_token_at_last_position(self):
        """Test consuming token when at the last valid position."""
        parser_state = {
            "tokens": [
                {"type": "IDENT", "value": "x", "line": 1, "column": 1},
                {"type": "OP", "value": "+", "line": 1, "column": 2},
            ],
            "pos": 1,
            "filename": "test.py"
        }
        
        result = _consume_token(parser_state)
        
        # Original state should not be modified
        self.assertEqual(parser_state["pos"], 1)
        # New state should have pos incremented to 2
        self.assertEqual(result["pos"], 2)
    
    def test_consume_token_at_end_no_change(self):
        """Test when pos equals len(tokens) - should return original state."""
        parser_state = {
            "tokens": [
                {"type": "IDENT", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 1,
            "filename": "test.py"
        }
        
        result = _consume_token(parser_state)
        
        # Should return the same object (no change)
        self.assertIs(result, parser_state)
        self.assertEqual(result["pos"], 1)
    
    def test_consume_token_beyond_end_no_change(self):
        """Test when pos > len(tokens) - should return original state."""
        parser_state = {
            "tokens": [
                {"type": "IDENT", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 5,
            "filename": "test.py"
        }
        
        result = _consume_token(parser_state)
        
        # Should return the same object (no change)
        self.assertIs(result, parser_state)
        self.assertEqual(result["pos"], 5)
    
    def test_consume_token_empty_tokens(self):
        """Test with empty tokens list - should return original state."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _consume_token(parser_state)
        
        # Should return the same object (no change)
        self.assertIs(result, parser_state)
        self.assertEqual(result["pos"], 0)
    
    def test_consume_token_missing_tokens_key(self):
        """Test when 'tokens' key is missing - should use default empty list."""
        parser_state = {
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _consume_token(parser_state)
        
        # Should return the same object (pos >= len([]) is True)
        self.assertIs(result, parser_state)
    
    def test_consume_token_missing_pos_key(self):
        """Test when 'pos' key is missing - should use default 0."""
        parser_state = {
            "tokens": [
                {"type": "IDENT", "value": "x", "line": 1, "column": 1},
            ],
            "filename": "test.py"
        }
        
        result = _consume_token(parser_state)
        
        # Should increment pos from default 0 to 1
        self.assertEqual(result["pos"], 1)
        # Original should not be modified
        self.assertNotIn("pos", parser_state)
    
    def test_consume_token_preserves_all_fields(self):
        """Test that all other fields in parser_state are preserved."""
        parser_state = {
            "tokens": [
                {"type": "IDENT", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 0,
            "filename": "test.py",
            "error": None,
            "custom_field": "custom_value",
            "nested": {"key": "value"}
        }
        
        result = _consume_token(parser_state)
        
        # All fields should be preserved
        self.assertEqual(result["filename"], "test.py")
        self.assertEqual(result["error"], None)
        self.assertEqual(result["custom_field"], "custom_value")
        self.assertEqual(result["nested"], {"key": "value"})
        # pos should be incremented
        self.assertEqual(result["pos"], 1)
    
    def test_consume_token_functional_style(self):
        """Test that original parser_state is not modified (functional style)."""
        parser_state = {
            "tokens": [
                {"type": "IDENT", "value": "x", "line": 1, "column": 1},
                {"type": "OP", "value": "+", "line": 1, "column": 2},
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        # Keep a reference to original tokens
        original_tokens = parser_state["tokens"]
        original_pos = parser_state["pos"]
        
        result = _consume_token(parser_state)
        
        # Verify original is unchanged
        self.assertEqual(parser_state["pos"], original_pos)
        self.assertEqual(parser_state["tokens"], original_tokens)
        # Verify result is a different object
        self.assertIsNot(result, parser_state)
        # But tokens list should be the same reference (shallow copy)
        self.assertIs(result["tokens"], parser_state["tokens"])


if __name__ == "__main__":
    unittest.main()

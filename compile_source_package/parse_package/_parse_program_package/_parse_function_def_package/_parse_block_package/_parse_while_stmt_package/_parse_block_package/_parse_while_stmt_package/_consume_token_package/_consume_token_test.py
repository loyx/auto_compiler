import unittest
from unittest.mock import patch

# Relative import from the same package
from ._consume_token_src import _consume_token
from . import _consume_token_src


class TestConsumeToken(unittest.TestCase):
    """Test cases for _consume_token function"""
    
    def test_consume_token_success(self):
        """Test successful token consumption when type matches"""
        parser_state = {
            "tokens": [
                {"type": "WHILE", "value": "while", "line": 1, "column": 1},
                {"type": "LPAREN", "value": "(", "line": 1, "column": 6},
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        new_state = _consume_token(parser_state, "WHILE")
        
        # Verify pos was incremented
        self.assertEqual(new_state["pos"], 1)
        # Verify original state was not modified
        self.assertEqual(parser_state["pos"], 0)
        # Verify other fields are preserved
        self.assertEqual(new_state["filename"], "test.py")
        self.assertEqual(len(new_state["tokens"]), 2)
    
    def test_consume_token_end_of_input(self):
        """Test that SyntaxError is raised when token is None (end of input)"""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, "WHILE")
        
        self.assertEqual(str(context.exception), "Unexpected end of input")
    
    def test_consume_token_type_mismatch(self):
        """Test that SyntaxError is raised when token type doesn't match"""
        parser_state = {
            "tokens": [
                {"type": "IF", "value": "if", "line": 1, "column": 1},
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, "WHILE")
        
        self.assertEqual(str(context.exception), "Expected WHILE but got IF")
    
    def test_consume_token_does_not_modify_original(self):
        """Test that the original parser_state is not modified (copy is returned)"""
        parser_state = {
            "tokens": [
                {"type": "WHILE", "value": "while", "line": 1, "column": 1},
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        new_state = _consume_token(parser_state, "WHILE")
        
        # Verify original state is unchanged
        self.assertEqual(parser_state["pos"], 0)
        # Verify new state has incremented pos
        self.assertEqual(new_state["pos"], 1)
        # Verify they are different objects
        self.assertIsNot(parser_state, new_state)
    
    def test_consume_token_middle_position(self):
        """Test consuming token when pos is not at the beginning"""
        parser_state = {
            "tokens": [
                {"type": "WHILE", "value": "while", "line": 1, "column": 1},
                {"type": "LPAREN", "value": "(", "line": 1, "column": 6},
                {"type": "RPAREN", "value": ")", "line": 1, "column": 7},
            ],
            "pos": 1,
            "filename": "test.py"
        }
        
        new_state = _consume_token(parser_state, "LPAREN")
        
        self.assertEqual(new_state["pos"], 2)
        self.assertEqual(parser_state["pos"], 1)
    
    def test_consume_token_last_token(self):
        """Test consuming the last token in the list"""
        parser_state = {
            "tokens": [
                {"type": "WHILE", "value": "while", "line": 1, "column": 1},
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        new_state = _consume_token(parser_state, "WHILE")
        
        self.assertEqual(new_state["pos"], 1)
        # pos now points beyond the last token
    
    def test_consume_token_multiple_sequential_calls(self):
        """Test multiple consecutive token consumptions"""
        parser_state = {
            "tokens": [
                {"type": "WHILE", "value": "while", "line": 1, "column": 1},
                {"type": "LPAREN", "value": "(", "line": 1, "column": 6},
                {"type": "RPAREN", "value": ")", "line": 1, "column": 7},
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        # Consume first token
        state1 = _consume_token(parser_state, "WHILE")
        self.assertEqual(state1["pos"], 1)
        
        # Consume second token
        state2 = _consume_token(state1, "LPAREN")
        self.assertEqual(state2["pos"], 2)
        
        # Consume third token
        state3 = _consume_token(state2, "RPAREN")
        self.assertEqual(state3["pos"], 3)
    
    @patch.object(_consume_token_src, '_peek_token')
    def test_consume_token_calls_peek_token(self, mock_peek):
        """Test that _peek_token is called with correct arguments"""
        mock_token = {"type": "IDENT", "value": "x", "line": 1, "column": 1}
        mock_peek.return_value = mock_token
        
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }
        
        new_state = _consume_token(parser_state, "IDENT")
        
        # Verify _peek_token was called
        mock_peek.assert_called_once_with(parser_state)
        self.assertEqual(new_state["pos"], 1)
    
    @patch.object(_consume_token_src, '_peek_token')
    def test_consume_token_peek_returns_none(self, mock_peek):
        """Test behavior when _peek_token returns None"""
        mock_peek.return_value = None
        
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, "WHILE")
        
        self.assertEqual(str(context.exception), "Unexpected end of input")
        mock_peek.assert_called_once_with(parser_state)
    
    def test_consume_token_preserves_all_state_fields(self):
        """Test that all parser_state fields are preserved in the copy"""
        parser_state = {
            "tokens": [
                {"type": "WHILE", "value": "while", "line": 1, "column": 1},
            ],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        new_state = _consume_token(parser_state, "WHILE")
        
        self.assertEqual(new_state["filename"], "test.py")
        self.assertEqual(new_state["error"], "")
        self.assertEqual(new_state["tokens"], parser_state["tokens"])
        self.assertEqual(new_state["pos"], 1)


if __name__ == "__main__":
    unittest.main()

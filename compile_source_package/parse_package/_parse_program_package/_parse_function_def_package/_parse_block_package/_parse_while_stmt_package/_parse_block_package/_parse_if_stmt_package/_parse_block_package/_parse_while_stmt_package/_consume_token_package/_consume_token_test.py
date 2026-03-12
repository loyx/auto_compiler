# === test file for _consume_token ===
import unittest
from typing import Any, Dict

from ._consume_token_src import _consume_token


class TestConsumeToken(unittest.TestCase):
    """Test cases for _consume_token function."""

    def _create_token(self, token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """Helper to create a token dict."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def _create_parser_state(self, tokens: list = None, pos: int = 0, filename: str = "test.py") -> Dict[str, Any]:
        """Helper to create a parser state dict."""
        return {
            "tokens": tokens if tokens is not None else [],
            "pos": pos,
            "filename": filename,
            "error": None
        }

    def test_consume_token_success(self):
        """Test successful token consumption when type matches."""
        tokens = [self._create_token("WHILE", "while")]
        parser_state = self._create_parser_state(tokens=tokens, pos=0)
        
        result = _consume_token(parser_state, "WHILE")
        
        self.assertEqual(result, tokens[0])
        self.assertEqual(parser_state["pos"], 1)
        self.assertIsNone(parser_state["error"])

    def test_consume_token_type_mismatch(self):
        """Test token consumption fails when type does not match."""
        tokens = [self._create_token("IF", "if", line=5, column=10)]
        parser_state = self._create_parser_state(tokens=tokens, pos=0)
        
        result = _consume_token(parser_state, "WHILE")
        
        self.assertIsNone(result)
        self.assertEqual(parser_state["pos"], 0)
        self.assertIsNotNone(parser_state["error"])
        self.assertIn("Expected token type 'WHILE' but got 'IF'", parser_state["error"])
        self.assertIn("line 5, column 10", parser_state["error"])

    def test_consume_token_end_of_input(self):
        """Test token consumption fails when at end of tokens."""
        parser_state = self._create_parser_state(tokens=[], pos=0)
        
        result = _consume_token(parser_state, "WHILE")
        
        self.assertIsNone(result)
        self.assertEqual(parser_state["pos"], 0)
        self.assertIsNotNone(parser_state["error"])
        self.assertIn("Unexpected end of input, expected WHILE", parser_state["error"])

    def test_consume_token_end_of_input_with_existing_tokens(self):
        """Test token consumption fails when pos is beyond token list."""
        tokens = [self._create_token("WHILE", "while")]
        parser_state = self._create_parser_state(tokens=tokens, pos=1)
        
        result = _consume_token(parser_state, "WHILE")
        
        self.assertIsNone(result)
        self.assertEqual(parser_state["pos"], 1)
        self.assertIsNotNone(parser_state["error"])
        self.assertIn("Unexpected end of input, expected WHILE", parser_state["error"])

    def test_consume_token_multiple_tokens(self):
        """Test consuming token from middle of token list."""
        tokens = [
            self._create_token("IF", "if"),
            self._create_token("WHILE", "while"),
            self._create_token("FOR", "for")
        ]
        parser_state = self._create_parser_state(tokens=tokens, pos=1)
        
        result = _consume_token(parser_state, "WHILE")
        
        self.assertEqual(result, tokens[1])
        self.assertEqual(parser_state["pos"], 2)
        self.assertIsNone(parser_state["error"])

    def test_consume_token_missing_type_field(self):
        """Test handling of token with missing type field."""
        tokens = [{"value": "test", "line": 1, "column": 1}]
        parser_state = self._create_parser_state(tokens=tokens, pos=0)
        
        result = _consume_token(parser_state, "WHILE")
        
        self.assertIsNone(result)
        self.assertEqual(parser_state["pos"], 0)
        self.assertIsNotNone(parser_state["error"])
        self.assertIn("Expected token type 'WHILE' but got 'UNKNOWN'", parser_state["error"])

    def test_consume_token_missing_value_field(self):
        """Test handling of token with missing value field."""
        tokens = [{"type": "IF", "line": 1, "column": 1}]
        parser_state = self._create_parser_state(tokens=tokens, pos=0)
        
        result = _consume_token(parser_state, "IF")
        
        self.assertEqual(result, tokens[0])
        self.assertEqual(parser_state["pos"], 1)
        self.assertIsNone(parser_state["error"])

    def test_consume_token_parser_state_missing_fields(self):
        """Test handling of parser state with missing optional fields."""
        parser_state = {"tokens": [self._create_token("WHILE", "while")]}
        
        result = _consume_token(parser_state, "WHILE")
        
        self.assertEqual(result["type"], "WHILE")
        self.assertEqual(parser_state["pos"], 1)

    def test_consume_token_various_types(self):
        """Test consuming different token types."""
        for token_type in ["LPAREN", "RPAREN", "LBRACE", "RBRACE", "SEMICOLON", "IDENTIFIER", "NUMBER"]:
            tokens = [self._create_token(token_type, token_type.lower())]
            parser_state = self._create_parser_state(tokens=tokens, pos=0)
            
            result = _consume_token(parser_state, token_type)
            
            self.assertEqual(result["type"], token_type)
            self.assertEqual(parser_state["pos"], 1)
            self.assertIsNone(parser_state["error"])

    def test_consume_token_preserves_other_state_fields(self):
        """Test that other parser state fields are preserved."""
        tokens = [self._create_token("WHILE", "while")]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test_file.py",
            "error": None,
            "custom_field": "custom_value"
        }
        
        result = _consume_token(parser_state, "WHILE")
        
        self.assertEqual(result, tokens[0])
        self.assertEqual(parser_state["pos"], 1)
        self.assertEqual(parser_state["filename"], "test_file.py")
        self.assertEqual(parser_state["custom_field"], "custom_value")


if __name__ == "__main__":
    unittest.main()

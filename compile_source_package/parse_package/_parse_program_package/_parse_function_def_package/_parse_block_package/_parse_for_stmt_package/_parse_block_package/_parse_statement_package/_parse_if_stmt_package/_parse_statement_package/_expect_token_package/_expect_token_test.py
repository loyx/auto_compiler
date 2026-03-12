# === std / third-party imports ===
import unittest
from typing import Any, Dict

# === relative import of UUT ===
from ._expect_token_src import _expect_token

# === type aliases (matching UUT) ===
Token = Dict[str, Any]
ParserState = Dict[str, Any]


class TestExpectToken(unittest.TestCase):
    """Test cases for _expect_token function."""

    def _create_parser_state(self, tokens: list, pos: int = 0, filename: str = "test.py") -> ParserState:
        """Helper to create a parser state dict."""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename,
            "error": ""
        }

    def _create_token(self, token_type: str, value: str, line: int = 1, column: int = 1) -> Token:
        """Helper to create a token dict."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    # === Happy Path Tests ===

    def test_expect_token_matches_first_token(self):
        """Test matching the first token advances pos."""
        tokens = [
            self._create_token("NAME", "x"),
            self._create_token("OP", "="),
            self._create_token("NUMBER", "42")
        ]
        state = self._create_parser_state(tokens, pos=0)
        
        _expect_token(state, "NAME")
        
        self.assertEqual(state["pos"], 1)

    def test_expect_token_matches_middle_token(self):
        """Test matching a middle token advances pos."""
        tokens = [
            self._create_token("NAME", "x"),
            self._create_token("OP", "="),
            self._create_token("NUMBER", "42")
        ]
        state = self._create_parser_state(tokens, pos=1)
        
        _expect_token(state, "OP")
        
        self.assertEqual(state["pos"], 2)

    def test_expect_token_matches_last_token(self):
        """Test matching the last token advances pos."""
        tokens = [
            self._create_token("NAME", "x"),
            self._create_token("OP", "="),
            self._create_token("NUMBER", "42")
        ]
        state = self._create_parser_state(tokens, pos=2)
        
        _expect_token(state, "NUMBER")
        
        self.assertEqual(state["pos"], 3)

    def test_expect_token_multiple_calls(self):
        """Test multiple consecutive calls advance pos correctly."""
        tokens = [
            self._create_token("NAME", "x"),
            self._create_token("OP", "="),
            self._create_token("NUMBER", "42")
        ]
        state = self._create_parser_state(tokens, pos=0)
        
        _expect_token(state, "NAME")
        _expect_token(state, "OP")
        _expect_token(state, "NUMBER")
        
        self.assertEqual(state["pos"], 3)

    # === Boundary Value Tests ===

    def test_expect_token_empty_tokens_list(self):
        """Test with empty tokens list raises SyntaxError."""
        state = self._create_parser_state([], pos=0)
        
        with self.assertRaises(SyntaxError) as context:
            _expect_token(state, "NAME")
        
        self.assertEqual(str(context.exception), "Unexpected end of input")

    def test_expect_token_pos_at_end(self):
        """Test when pos equals len(tokens) raises SyntaxError."""
        tokens = [self._create_token("NAME", "x")]
        state = self._create_parser_state(tokens, pos=1)
        
        with self.assertRaises(SyntaxError) as context:
            _expect_token(state, "NAME")
        
        self.assertEqual(str(context.exception), "Unexpected end of input")

    def test_expect_token_pos_beyond_end(self):
        """Test when pos exceeds len(tokens) raises SyntaxError."""
        tokens = [self._create_token("NAME", "x")]
        state = self._create_parser_state(tokens, pos=5)
        
        with self.assertRaises(SyntaxError) as context:
            _expect_token(state, "NAME")
        
        self.assertEqual(str(context.exception), "Unexpected end of input")

    # === Error Case Tests ===

    def test_expect_token_type_mismatch(self):
        """Test mismatched token type raises SyntaxError with details."""
        tokens = [self._create_token("NAME", "x", line=3, column=5)]
        state = self._create_parser_state(tokens, pos=0)
        
        with self.assertRaises(SyntaxError) as context:
            _expect_token(state, "NUMBER")
        
        error_msg = str(context.exception)
        self.assertIn("Unexpected token 'x'", error_msg)
        self.assertIn("line 3", error_msg)
        self.assertIn("column 5", error_msg)
        self.assertIn("expected NUMBER", error_msg)

    def test_expect_token_type_mismatch_with_operator(self):
        """Test mismatched operator token raises SyntaxError."""
        tokens = [self._create_token("OP", "+", line=1, column=10)]
        state = self._create_parser_state(tokens, pos=0)
        
        with self.assertRaises(SyntaxError) as context:
            _expect_token(state, "NAME")
        
        error_msg = str(context.exception)
        self.assertIn("Unexpected token '+'", error_msg)
        self.assertIn("expected NAME", error_msg)

    def test_expect_token_type_mismatch_with_keyword(self):
        """Test mismatched keyword token raises SyntaxError."""
        tokens = [self._create_token("KEYWORD", "if", line=5, column=1)]
        state = self._create_parser_state(tokens, pos=0)
        
        with self.assertRaises(SyntaxError) as context:
            _expect_token(state, "NAME")
        
        error_msg = str(context.exception)
        self.assertIn("Unexpected token 'if'", error_msg)
        self.assertIn("line 5", error_msg)
        self.assertIn("column 1", error_msg)

    # === State Mutation Tests ===

    def test_expect_token_does_not_modify_tokens(self):
        """Test that tokens list is not modified."""
        tokens = [self._create_token("NAME", "x")]
        state = self._create_parser_state(tokens, pos=0)
        original_tokens = state["tokens"].copy()
        
        _expect_token(state, "NAME")
        
        self.assertEqual(state["tokens"], original_tokens)

    def test_expect_token_does_not_modify_other_fields(self):
        """Test that other parser state fields are not modified."""
        tokens = [self._create_token("NAME", "x")]
        state = self._create_parser_state(tokens, pos=0, filename="my_file.py")
        state["error"] = "some error"
        original_filename = state["filename"]
        original_error = state["error"]
        
        _expect_token(state, "NAME")
        
        self.assertEqual(state["filename"], original_filename)
        self.assertEqual(state["error"], original_error)


if __name__ == "__main__":
    unittest.main()

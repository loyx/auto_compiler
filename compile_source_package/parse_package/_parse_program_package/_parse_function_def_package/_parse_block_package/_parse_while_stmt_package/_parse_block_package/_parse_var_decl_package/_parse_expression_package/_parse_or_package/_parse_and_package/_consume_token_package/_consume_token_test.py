# === std / third-party imports ===
import unittest

# === sub function imports ===
from ._consume_token_src import _consume_token, ParserState


class TestConsumeToken(unittest.TestCase):
    """Test cases for _consume_token function."""

    def test_consume_matching_token_first_position(self):
        """Happy path: consume matching token at first position."""
        tokens = [
            {"type": "IDENT", "value": "x", "line": 1, "column": 1},
            {"type": "ASSIGN", "value": "=", "line": 1, "column": 3},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }

        token, updated_state = _consume_token(parser_state, "IDENT")

        self.assertEqual(token, tokens[0])
        self.assertEqual(updated_state["pos"], 1)
        self.assertEqual(updated_state["tokens"], tokens)
        self.assertEqual(updated_state["filename"], "test.py")

    def test_consume_matching_token_middle_position(self):
        """Happy path: consume matching token at middle position."""
        tokens = [
            {"type": "IDENT", "value": "x", "line": 1, "column": 1},
            {"type": "ASSIGN", "value": "=", "line": 1, "column": 3},
            {"type": "NUMBER", "value": "42", "line": 1, "column": 5},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 1,
            "filename": "test.py"
        }

        token, updated_state = _consume_token(parser_state, "ASSIGN")

        self.assertEqual(token, tokens[1])
        self.assertEqual(updated_state["pos"], 2)

    def test_consume_matching_token_last_position(self):
        """Happy path: consume matching token at last position."""
        tokens = [
            {"type": "IDENT", "value": "x", "line": 1, "column": 1},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }

        token, updated_state = _consume_token(parser_state, "IDENT")

        self.assertEqual(token, tokens[0])
        self.assertEqual(updated_state["pos"], 1)

    def test_consume_preserves_error_field(self):
        """State preservation: error field should be preserved if present."""
        tokens = [
            {"type": "IDENT", "value": "x", "line": 1, "column": 1},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
            "error": "previous_error"
        }

        token, updated_state = _consume_token(parser_state, "IDENT")

        self.assertIn("error", updated_state)
        self.assertEqual(updated_state["error"], "previous_error")

    def test_consume_without_error_field(self):
        """State handling: no error field in input means no error field in output."""
        tokens = [
            {"type": "IDENT", "value": "x", "line": 1, "column": 1},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }

        token, updated_state = _consume_token(parser_state, "IDENT")

        self.assertNotIn("error", updated_state)

    def test_consume_default_filename(self):
        """Boundary: uses 'unknown' filename when not provided."""
        tokens = [
            {"type": "IDENT", "value": "x", "line": 1, "column": 1},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0
        }

        token, updated_state = _consume_token(parser_state, "IDENT")

        self.assertEqual(updated_state["filename"], "unknown")

    def test_consume_type_mismatch(self):
        """Error case: token type mismatch raises SyntaxError."""
        tokens = [
            {"type": "IDENT", "value": "x", "line": 2, "column": 5},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }

        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, "NUMBER")

        error_msg = str(context.exception)
        self.assertIn("Syntax error at test.py:2:5", error_msg)
        self.assertIn("expected NUMBER", error_msg)
        self.assertIn("got IDENT", error_msg)

    def test_consume_end_of_tokens(self):
        """Error case: end of tokens raises SyntaxError."""
        tokens = [
            {"type": "IDENT", "value": "x", "line": 1, "column": 1},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 1,
            "filename": "test.py"
        }

        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, "IDENT")

        error_msg = str(context.exception)
        self.assertIn("Syntax error at test.py", error_msg)
        self.assertIn("unexpected end of input", error_msg)
        self.assertIn("expected IDENT", error_msg)

    def test_consume_end_of_tokens_empty_list(self):
        """Boundary: empty token list raises SyntaxError."""
        tokens = []
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "empty.py"
        }

        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, "IDENT")

        error_msg = str(context.exception)
        self.assertIn("Syntax error at empty.py", error_msg)
        self.assertIn("unexpected end of input", error_msg)

    def test_consume_multiple_sequential(self):
        """Integration: multiple consecutive consumes work correctly."""
        tokens = [
            {"type": "IDENT", "value": "x", "line": 1, "column": 1},
            {"type": "ASSIGN", "value": "=", "line": 1, "column": 3},
            {"type": "NUMBER", "value": "42", "line": 1, "column": 5},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }

        # Consume IDENT
        token1, state1 = _consume_token(parser_state, "IDENT")
        self.assertEqual(token1["type"], "IDENT")
        self.assertEqual(state1["pos"], 1)

        # Consume ASSIGN
        token2, state2 = _consume_token(state1, "ASSIGN")
        self.assertEqual(token2["type"], "ASSIGN")
        self.assertEqual(state2["pos"], 2)

        # Consume NUMBER
        token3, state3 = _consume_token(state2, "NUMBER")
        self.assertEqual(token3["type"], "NUMBER")
        self.assertEqual(state3["pos"], 3)

    def test_consume_token_missing_type_field(self):
        """Boundary: token without type field uses UNKNOWN."""
        tokens = [
            {"value": "x", "line": 1, "column": 1},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }

        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, "IDENT")

        error_msg = str(context.exception)
        self.assertIn("got UNKNOWN", error_msg)

    def test_consume_token_missing_line_column(self):
        """Boundary: token without line/column uses 0."""
        tokens = [
            {"type": "IDENT", "value": "x"},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }

        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, "NUMBER")

        error_msg = str(context.exception)
        self.assertIn("Syntax error at test.py:0:0", error_msg)


if __name__ == "__main__":
    unittest.main()

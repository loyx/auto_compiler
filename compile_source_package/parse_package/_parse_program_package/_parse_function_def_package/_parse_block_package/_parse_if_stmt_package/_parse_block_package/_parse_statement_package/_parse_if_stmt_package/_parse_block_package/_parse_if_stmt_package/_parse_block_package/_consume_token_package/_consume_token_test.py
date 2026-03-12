import unittest
from ._consume_token_src import _consume_token


class TestConsumeToken(unittest.TestCase):
    """Test cases for _consume_token function."""

    def test_consume_token_success(self):
        """Happy path: token type matches, pos advances, token returned."""
        parser_state = {
            "tokens": [
                {"type": "IF", "value": "if", "line": 1, "column": 1}
            ],
            "filename": "test.py",
            "pos": 0
        }

        result = _consume_token(parser_state, "IF")

        self.assertEqual(result["type"], "IF")
        self.assertEqual(result["value"], "if")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 1)

    def test_consume_token_multiple_tokens(self):
        """Success with multiple tokens, consumes only current token."""
        parser_state = {
            "tokens": [
                {"type": "IF", "value": "if", "line": 1, "column": 1},
                {"type": "LPAREN", "value": "(", "line": 1, "column": 3},
                {"type": "RPAREN", "value": ")", "line": 1, "column": 4}
            ],
            "filename": "test.py",
            "pos": 1
        }

        result = _consume_token(parser_state, "LPAREN")

        self.assertEqual(result["type"], "LPAREN")
        self.assertEqual(result["value"], "(")
        self.assertEqual(parser_state["pos"], 2)

    def test_consume_token_eof_empty_tokens(self):
        """Boundary: empty tokens list raises SyntaxError."""
        parser_state = {
            "tokens": [],
            "filename": "test.py",
            "pos": 0
        }

        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, "IF")

        self.assertIn("end of file", str(context.exception))
        self.assertIn("test.py", str(context.exception))
        self.assertEqual(parser_state["pos"], 0)

    def test_consume_token_eof_pos_beyond_length(self):
        """Boundary: pos beyond tokens length raises SyntaxError."""
        parser_state = {
            "tokens": [
                {"type": "IF", "value": "if", "line": 1, "column": 1}
            ],
            "filename": "test.py",
            "pos": 1
        }

        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, "IF")

        self.assertIn("end of file", str(context.exception))
        self.assertEqual(parser_state["pos"], 1)

    def test_consume_token_type_mismatch(self):
        """Error: token type doesn't match expected type."""
        parser_state = {
            "tokens": [
                {"type": "WHILE", "value": "while", "line": 2, "column": 5}
            ],
            "filename": "test.py",
            "pos": 0
        }

        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, "IF")

        error_msg = str(context.exception)
        self.assertIn("test.py:2:5", error_msg)
        self.assertIn("expected 'IF'", error_msg)
        self.assertIn("got 'WHILE'", error_msg)
        self.assertEqual(parser_state["pos"], 0)

    def test_consume_token_type_mismatch_middle_position(self):
        """Error: mismatch at non-zero position."""
        parser_state = {
            "tokens": [
                {"type": "IF", "value": "if", "line": 1, "column": 1},
                {"type": "WHILE", "value": "while", "line": 3, "column": 10},
                {"type": "IF", "value": "if", "line": 5, "column": 1}
            ],
            "filename": "main.py",
            "pos": 1
        }

        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, "IF")

        error_msg = str(context.exception)
        self.assertIn("main.py:3:10", error_msg)
        self.assertIn("expected 'IF'", error_msg)
        self.assertIn("got 'WHILE'", error_msg)
        self.assertEqual(parser_state["pos"], 1)

    def test_consume_token_preserves_other_state(self):
        """Verify other parser_state fields are not modified."""
        parser_state = {
            "tokens": [
                {"type": "LBRACE", "value": "{", "line": 1, "column": 1}
            ],
            "filename": "test.py",
            "pos": 0,
            "error": None,
            "extra_field": "unchanged"
        }

        _consume_token(parser_state, "LBRACE")

        self.assertEqual(parser_state["filename"], "test.py")
        self.assertEqual(parser_state["error"], None)
        self.assertEqual(parser_state["extra_field"], "unchanged")
        self.assertEqual(len(parser_state["tokens"]), 1)

    def test_consume_token_various_token_types(self):
        """Test with various common token types."""
        token_types = ["LBRACE", "RBRACE", "LPAREN", "RPAREN", "SEMICOLON", "IDENTIFIER"]

        for token_type in token_types:
            parser_state = {
                "tokens": [
                    {"type": token_type, "value": token_type.lower(), "line": 1, "column": 1}
                ],
                "filename": "test.py",
                "pos": 0
            }

            result = _consume_token(parser_state, token_type)

            self.assertEqual(result["type"], token_type)
            self.assertEqual(parser_state["pos"], 1)


if __name__ == "__main__":
    unittest.main()

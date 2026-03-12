import unittest
from unittest.mock import patch
from typing import Any, Dict

from ._expect_src import _expect

Token = Dict[str, Any]
ParserState = Dict[str, Any]


class TestExpect(unittest.TestCase):
    """Test cases for _expect function."""

    def test_expect_success_token_matches(self):
        """Test that _expect returns token and increments pos when type matches."""
        token: Token = {
            "type": "OPERATOR",
            "value": "+",
            "line": 1,
            "column": 5
        }
        parser_state: ParserState = {
            "tokens": [token],
            "pos": 0,
            "filename": "test.py"
        }

        with patch("._current_token_package._current_token_src._current_token", return_value=token):
            result = _expect(parser_state, "OPERATOR")

            self.assertEqual(result, token)
            self.assertEqual(parser_state["pos"], 1)

    def test_expect_failure_token_mismatch(self):
        """Test that _expect raises SyntaxError when token type doesn't match."""
        token: Token = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 2,
            "column": 10
        }
        parser_state: ParserState = {
            "tokens": [token],
            "pos": 0,
            "filename": "test.py"
        }

        with patch("._current_token_package._current_token_src._current_token", return_value=token):
            with self.assertRaises(SyntaxError) as context:
                _expect(parser_state, "OPERATOR")

            error_msg = str(context.exception)
            self.assertIn("Expected token type 'OPERATOR'", error_msg)
            self.assertIn("got 'IDENTIFIER'", error_msg)
            self.assertIn("line 2", error_msg)
            self.assertIn("column 10", error_msg)
            self.assertIn("test.py", error_msg)
            self.assertEqual(parser_state["pos"], 0)

    def test_expect_pos_not_incremented_on_failure(self):
        """Test that pos is not incremented when token type doesn't match."""
        token: Token = {
            "type": "KEYWORD",
            "value": "if",
            "line": 1,
            "column": 1
        }
        parser_state: ParserState = {
            "tokens": [token],
            "pos": 0,
            "filename": "test.py"
        }

        with patch("._current_token_package._current_token_src._current_token", return_value=token):
            with self.assertRaises(SyntaxError):
                _expect(parser_state, "OPERATOR")

            self.assertEqual(parser_state["pos"], 0)

    def test_expect_with_filename_in_error(self):
        """Test that error message includes filename."""
        token: Token = {
            "type": "STRING",
            "value": '"hello"',
            "line": 5,
            "column": 20
        }
        parser_state: ParserState = {
            "tokens": [token],
            "pos": 0,
            "filename": "my_module.py"
        }

        with patch("._current_token_package._current_token_src._current_token", return_value=token):
            with self.assertRaises(SyntaxError) as context:
                _expect(parser_state, "NUMBER")

            error_msg = str(context.exception)
            self.assertIn("my_module.py", error_msg)
            self.assertIn("line 5", error_msg)
            self.assertIn("column 20", error_msg)

    def test_expect_without_filename(self):
        """Test that error message uses '<unknown>' when filename is missing."""
        token: Token = {
            "type": "OPERATOR",
            "value": "*",
            "line": 1,
            "column": 1
        }
        parser_state: ParserState = {
            "tokens": [token],
            "pos": 0
        }

        with patch("._current_token_package._current_token_src._current_token", return_value=token):
            with self.assertRaises(SyntaxError) as context:
                _expect(parser_state, "NUMBER")

            self.assertIn("<unknown>", str(context.exception))

    def test_expect_multiple_tokens(self):
        """Test _expect with multiple tokens in the list."""
        token1: Token = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 1
        }
        token2: Token = {
            "type": "OPERATOR",
            "value": "=",
            "line": 1,
            "column": 3
        }
        parser_state: ParserState = {
            "tokens": [token1, token2],
            "pos": 0,
            "filename": "test.py"
        }

        with patch("._current_token_package._current_token_src._current_token", return_value=token1):
            result = _expect(parser_state, "IDENTIFIER")

            self.assertEqual(result, token1)
            self.assertEqual(parser_state["pos"], 1)

    def test_expect_various_token_types(self):
        """Test _expect with various token types."""
        for token_type in ["NUMBER", "STRING", "KEYWORD", "PUNCTUATION"]:
            token: Token = {
                "type": token_type,
                "value": "test",
                "line": 1,
                "column": 1
            }
            parser_state: ParserState = {
                "tokens": [token],
                "pos": 0,
                "filename": "test.py"
            }

            with patch("._current_token_package._current_token_src._current_token", return_value=token):
                result = _expect(parser_state, token_type)

                self.assertEqual(result, token)
                self.assertEqual(parser_state["pos"], 1)


if __name__ == "__main__":
    unittest.main()

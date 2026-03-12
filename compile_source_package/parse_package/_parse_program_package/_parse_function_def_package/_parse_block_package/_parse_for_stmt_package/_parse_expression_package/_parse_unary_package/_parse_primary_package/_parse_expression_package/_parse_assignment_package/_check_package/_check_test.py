# -*- coding: utf-8 -*-
"""Unit tests for _check function in parser lookahead helper."""

import unittest
from ._check_src import _check


class TestCheckFunction(unittest.TestCase):
    """Test cases for _check lookahead helper function."""

    def test_token_matches_expected_type(self):
        """Happy path: current token matches expected type returns True."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "EQUALS", "value": "=", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "42", "line": 1, "column": 5},
            ],
            "pos": 0,
            "filename": "test.py",
        }
        result = _check(parser_state, "IDENTIFIER")
        self.assertTrue(result)

    def test_token_does_not_match_expected_type(self):
        """Current token type mismatch returns False."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "EQUALS", "value": "=", "line": 1, "column": 3},
            ],
            "pos": 0,
            "filename": "test.py",
        }
        result = _check(parser_state, "NUMBER")
        self.assertFalse(result)

    def test_position_at_end_of_tokens(self):
        """Position at exact end of tokens list returns False."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "EQUALS", "value": "=", "line": 1, "column": 3},
            ],
            "pos": 2,
            "filename": "test.py",
        }
        result = _check(parser_state, "IDENTIFIER")
        self.assertFalse(result)

    def test_position_beyond_end_of_tokens(self):
        """Position beyond end of tokens list returns False."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 5,
            "filename": "test.py",
        }
        result = _check(parser_state, "IDENTIFIER")
        self.assertFalse(result)

    def test_empty_tokens_list(self):
        """Empty tokens list returns False regardless of position."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py",
        }
        result = _check(parser_state, "IDENTIFIER")
        self.assertFalse(result)

    def test_check_middle_token(self):
        """Check token at middle position works correctly."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "EQUALS", "value": "=", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "42", "line": 1, "column": 5},
            ],
            "pos": 1,
            "filename": "test.py",
        }
        result = _check(parser_state, "EQUALS")
        self.assertTrue(result)

    def test_check_last_token(self):
        """Check last token in list works correctly."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "EQUALS", "value": "=", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "42", "line": 1, "column": 5},
            ],
            "pos": 2,
            "filename": "test.py",
        }
        result = _check(parser_state, "NUMBER")
        self.assertTrue(result)

    def test_case_sensitive_type_matching(self):
        """Token type matching is case-sensitive."""
        parser_state = {
            "tokens": [
                {"type": "identifier", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 0,
            "filename": "test.py",
        }
        result = _check(parser_state, "IDENTIFIER")
        self.assertFalse(result)

    def test_does_not_modify_parser_state(self):
        """_check does not have side effects on parser_state."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 0,
            "filename": "test.py",
        }
        original_pos = parser_state["pos"]
        original_tokens_len = len(parser_state["tokens"])
        
        _check(parser_state, "IDENTIFIER")
        
        self.assertEqual(parser_state["pos"], original_pos)
        self.assertEqual(len(parser_state["tokens"]), original_tokens_len)


if __name__ == "__main__":
    unittest.main()

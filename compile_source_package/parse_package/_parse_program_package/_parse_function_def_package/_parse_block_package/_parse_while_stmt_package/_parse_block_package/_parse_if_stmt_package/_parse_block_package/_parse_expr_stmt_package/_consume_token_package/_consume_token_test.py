# === Test file for _consume_token ===
import unittest
from typing import Any, Dict

from ._consume_token_src import _consume_token


class TestConsumeToken(unittest.TestCase):
    """Test cases for _consume_token function."""

    def _create_parser_state(
        self,
        tokens: list = None,
        pos: int = 0,
        filename: str = "test.py"
    ) -> Dict[str, Any]:
        """Helper to create parser state dictionary."""
        state = {
            "tokens": tokens if tokens is not None else [],
            "pos": pos,
            "filename": filename
        }
        return state

    def _create_token(
        self,
        token_type: str,
        value: str,
        line: int = 1,
        column: int = 1
    ) -> Dict[str, Any]:
        """Helper to create a token dictionary."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    # === Happy Path Tests ===

    def test_consume_token_matches_by_type(self):
        """Token matches by type field - should consume and return True."""
        tokens = [
            self._create_token("IDENT", "x"),
            self._create_token("NUMBER", "42"),
        ]
        parser_state = self._create_parser_state(tokens=tokens, pos=0)

        result = _consume_token(parser_state, "IDENT")

        self.assertTrue(result)
        self.assertEqual(parser_state["pos"], 1)

    def test_consume_token_matches_by_value(self):
        """Token matches by value field - should consume and return True."""
        tokens = [
            self._create_token("SEMICOLON", ";"),
            self._create_token("IDENT", "x"),
        ]
        parser_state = self._create_parser_state(tokens=tokens, pos=0)

        result = _consume_token(parser_state, ";")

        self.assertTrue(result)
        self.assertEqual(parser_state["pos"], 1)

    def test_consume_token_second_position(self):
        """Consume token at non-zero position."""
        tokens = [
            self._create_token("IDENT", "x"),
            self._create_token("NUMBER", "42"),
            self._create_token("SEMICOLON", ";"),
        ]
        parser_state = self._create_parser_state(tokens=tokens, pos=1)

        result = _consume_token(parser_state, "NUMBER")

        self.assertTrue(result)
        self.assertEqual(parser_state["pos"], 2)

    # === Boundary Value Tests ===

    def test_consume_token_empty_tokens_list(self):
        """Empty tokens list - should return False without error."""
        parser_state = self._create_parser_state(tokens=[], pos=0)

        result = _consume_token(parser_state, "IDENT")

        self.assertFalse(result)
        self.assertEqual(parser_state["pos"], 0)

    def test_consume_token_pos_at_end(self):
        """Position at end of tokens list - should return False."""
        tokens = [
            self._create_token("IDENT", "x"),
            self._create_token("NUMBER", "42"),
        ]
        parser_state = self._create_parser_state(tokens=tokens, pos=2)

        result = _consume_token(parser_state, "SEMICOLON")

        self.assertFalse(result)
        self.assertEqual(parser_state["pos"], 2)

    def test_consume_token_pos_beyond_end(self):
        """Position beyond tokens list - should return False."""
        tokens = [
            self._create_token("IDENT", "x"),
        ]
        parser_state = self._create_parser_state(tokens=tokens, pos=5)

        result = _consume_token(parser_state, "IDENT")

        self.assertFalse(result)
        self.assertEqual(parser_state["pos"], 5)

    # === Invalid Input Tests ===

    def test_consume_token_missing_tokens_field(self):
        """Missing tokens field - should return False gracefully."""
        parser_state = {"pos": 0, "filename": "test.py"}

        result = _consume_token(parser_state, "IDENT")

        self.assertFalse(result)

    def test_consume_token_missing_pos_field(self):
        """Missing pos field - should default to 0."""
        tokens = [
            self._create_token("IDENT", "x"),
        ]
        parser_state = {"tokens": tokens, "filename": "test.py"}

        result = _consume_token(parser_state, "IDENT")

        self.assertTrue(result)
        self.assertEqual(parser_state["pos"], 1)

    def test_consume_token_empty_parser_state(self):
        """Empty parser state dictionary - should return False."""
        parser_state = {}

        result = _consume_token(parser_state, "IDENT")

        self.assertFalse(result)

    # === No Match Tests ===

    def test_consume_token_no_match_by_type_or_value(self):
        """Token doesn't match by type or value - should return False."""
        tokens = [
            self._create_token("IDENT", "x"),
        ]
        parser_state = self._create_parser_state(tokens=tokens, pos=0)

        result = _consume_token(parser_state, "NUMBER")

        self.assertFalse(result)
        self.assertEqual(parser_state["pos"], 0)

    def test_consume_token_partial_match_type_only(self):
        """Token type doesn't match but value also doesn't match."""
        tokens = [
            self._create_token("KEYWORD", "if"),
        ]
        parser_state = self._create_parser_state(tokens=tokens, pos=0)

        result = _consume_token(parser_state, "IDENT")

        self.assertFalse(result)
        self.assertEqual(parser_state["pos"], 0)

    # === State Modification Tests ===

    def test_consume_token_does_not_modify_on_failure(self):
        """Position should not change when token doesn't match."""
        tokens = [
            self._create_token("IDENT", "x"),
            self._create_token("NUMBER", "42"),
        ]
        parser_state = self._create_parser_state(tokens=tokens, pos=0)
        original_pos = parser_state["pos"]

        result = _consume_token(parser_state, "NUMBER")

        self.assertFalse(result)
        self.assertEqual(parser_state["pos"], original_pos)

    def test_consume_token_increments_pos_by_one(self):
        """Position should increment by exactly 1 on success."""
        tokens = [
            self._create_token("IDENT", "x"),
            self._create_token("NUMBER", "42"),
            self._create_token("SEMICOLON", ";"),
        ]
        parser_state = self._create_parser_state(tokens=tokens, pos=0)

        _consume_token(parser_state, "IDENT")
        _consume_token(parser_state, "NUMBER")
        _consume_token(parser_state, ";")

        self.assertEqual(parser_state["pos"], 3)

    def test_consume_token_does_not_set_error_field(self):
        """Function should not set error field on failure (silent failure)."""
        tokens = [
            self._create_token("IDENT", "x"),
        ]
        parser_state = self._create_parser_state(tokens=tokens, pos=0)

        result = _consume_token(parser_state, "NUMBER")

        self.assertFalse(result)
        self.assertNotIn("error", parser_state)

    # === Token Structure Edge Cases ===

    def test_consume_token_missing_type_field(self):
        """Token missing type field - should check value only."""
        tokens = [
            {"value": ";", "line": 1, "column": 1},
        ]
        parser_state = self._create_parser_state(tokens=tokens, pos=0)

        result = _consume_token(parser_state, ";")

        self.assertTrue(result)
        self.assertEqual(parser_state["pos"], 1)

    def test_consume_token_missing_value_field(self):
        """Token missing value field - should check type only."""
        tokens = [
            {"type": "SEMICOLON", "line": 1, "column": 1},
        ]
        parser_state = self._create_parser_state(tokens=tokens, pos=0)

        result = _consume_token(parser_state, "SEMICOLON")

        self.assertTrue(result)
        self.assertEqual(parser_state["pos"], 1)

    def test_consume_token_none_type_field(self):
        """Token with None type field - should handle gracefully."""
        tokens = [
            {"type": None, "value": ";", "line": 1, "column": 1},
        ]
        parser_state = self._create_parser_state(tokens=tokens, pos=0)

        result = _consume_token(parser_state, "SEMICOLON")

        self.assertFalse(result)
        self.assertEqual(parser_state["pos"], 0)


if __name__ == "__main__":
    unittest.main()

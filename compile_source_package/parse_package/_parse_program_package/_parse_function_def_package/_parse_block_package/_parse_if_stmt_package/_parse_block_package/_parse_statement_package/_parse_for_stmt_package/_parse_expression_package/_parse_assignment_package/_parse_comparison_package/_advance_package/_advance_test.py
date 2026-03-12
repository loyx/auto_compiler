# === std / third-party imports ===
import unittest
from typing import Any, Dict

# === relative import of UUT ===
from ._advance_src import _advance

# === type alias (matching UUT) ===
ParserState = Dict[str, Any]


class TestAdvance(unittest.TestCase):
    """Unit tests for _advance function."""

    def test_advance_increments_pos_by_one(self):
        """Happy path: pos should be incremented by exactly 1."""
        parser_state: ParserState = {
            "tokens": ["tok1", "tok2", "tok3"],
            "pos": 0,
            "filename": "test.py"
        }
        result = _advance(parser_state)
        self.assertIsNone(result)
        self.assertEqual(parser_state["pos"], 1)

    def test_advance_modifies_in_place(self):
        """Verify the function modifies the dictionary in-place."""
        parser_state: ParserState = {
            "tokens": ["tok1", "tok2"],
            "pos": 5
        }
        original_id = id(parser_state)
        _advance(parser_state)
        self.assertEqual(id(parser_state), original_id)
        self.assertEqual(parser_state["pos"], 6)

    def test_advance_from_zero_position(self):
        """Edge case: advancing from position 0."""
        parser_state: ParserState = {
            "tokens": ["tok1"],
            "pos": 0
        }
        _advance(parser_state)
        self.assertEqual(parser_state["pos"], 1)

    def test_advance_from_middle_position(self):
        """Edge case: advancing from middle position."""
        parser_state: ParserState = {
            "tokens": ["tok1", "tok2", "tok3", "tok4", "tok5"],
            "pos": 2
        }
        _advance(parser_state)
        self.assertEqual(parser_state["pos"], 3)

    def test_advance_from_last_position(self):
        """Edge case: advancing from last valid position (no boundary check)."""
        parser_state: ParserState = {
            "tokens": ["tok1", "tok2"],
            "pos": 1
        }
        _advance(parser_state)
        self.assertEqual(parser_state["pos"], 2)

    def test_advance_beyond_tokens_length(self):
        """Edge case: pos can exceed tokens length (no boundary checking)."""
        parser_state: ParserState = {
            "tokens": ["tok1"],
            "pos": 10
        }
        _advance(parser_state)
        self.assertEqual(parser_state["pos"], 11)

    def test_advance_with_empty_tokens(self):
        """Edge case: advancing with empty tokens list."""
        parser_state: ParserState = {
            "tokens": [],
            "pos": 0
        }
        _advance(parser_state)
        self.assertEqual(parser_state["pos"], 1)

    def test_advance_preserves_other_fields(self):
        """Verify other fields in parser_state are not modified."""
        parser_state: ParserState = {
            "tokens": ["tok1", "tok2"],
            "pos": 0,
            "filename": "test.py",
            "error": None
        }
        _advance(parser_state)
        self.assertEqual(parser_state["tokens"], ["tok1", "tok2"])
        self.assertEqual(parser_state["filename"], "test.py")
        self.assertIsNone(parser_state["error"])

    def test_advance_multiple_times(self):
        """Verify multiple consecutive advances."""
        parser_state: ParserState = {
            "tokens": ["tok1", "tok2", "tok3", "tok4"],
            "pos": 0
        }
        _advance(parser_state)
        _advance(parser_state)
        _advance(parser_state)
        self.assertEqual(parser_state["pos"], 3)


if __name__ == "__main__":
    unittest.main()

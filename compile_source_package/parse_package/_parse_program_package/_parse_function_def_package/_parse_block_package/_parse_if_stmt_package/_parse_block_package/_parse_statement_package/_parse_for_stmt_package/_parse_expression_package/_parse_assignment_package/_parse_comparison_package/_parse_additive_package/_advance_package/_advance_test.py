# === std / third-party imports ===
import unittest
from typing import Dict, Any

# === relative import of UUT ===
from ._advance_src import _advance

# === type definitions ===
ParserState = Dict[str, Any]


class TestAdvance(unittest.TestCase):
    """Test cases for _advance function."""

    def test_advance_increments_pos_by_one(self):
        """Happy path: pos exists and gets incremented by 1."""
        parser_state: ParserState = {
            "tokens": ["token1", "token2", "token3"],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _advance(parser_state)
        
        self.assertIsNone(result)
        self.assertEqual(parser_state["pos"], 1)

    def test_advance_pos_from_nonzero(self):
        """Pos increments correctly from non-zero value."""
        parser_state: ParserState = {
            "tokens": ["token1", "token2", "token3"],
            "pos": 5,
            "filename": "test.py"
        }
        
        _advance(parser_state)
        
        self.assertEqual(parser_state["pos"], 6)

    def test_advance_pos_missing_defaults_to_zero(self):
        """Edge case: pos key missing, defaults to 0 then becomes 1."""
        parser_state: ParserState = {
            "tokens": ["token1", "token2"],
            "filename": "test.py"
        }
        
        _advance(parser_state)
        
        self.assertEqual(parser_state["pos"], 1)

    def test_advance_pos_zero(self):
        """Edge case: pos is 0, becomes 1."""
        parser_state: ParserState = {
            "tokens": ["token1"],
            "pos": 0,
            "filename": "test.py"
        }
        
        _advance(parser_state)
        
        self.assertEqual(parser_state["pos"], 1)

    def test_advance_pos_negative(self):
        """Edge case: pos is negative, still increments."""
        parser_state: ParserState = {
            "tokens": ["token1"],
            "pos": -3,
            "filename": "test.py"
        }
        
        _advance(parser_state)
        
        self.assertEqual(parser_state["pos"], -2)

    def test_advance_modifies_in_place(self):
        """Verify parser_state dict is modified in-place (same object)."""
        parser_state: ParserState = {
            "tokens": ["token1"],
            "pos": 10,
            "filename": "test.py"
        }
        original_id = id(parser_state)
        
        _advance(parser_state)
        
        self.assertEqual(id(parser_state), original_id)
        self.assertEqual(parser_state["pos"], 11)

    def test_advance_multiple_calls(self):
        """Multiple calls increment pos each time."""
        parser_state: ParserState = {
            "tokens": ["token1", "token2", "token3", "token4", "token5"],
            "pos": 0,
            "filename": "test.py"
        }
        
        _advance(parser_state)
        _advance(parser_state)
        _advance(parser_state)
        
        self.assertEqual(parser_state["pos"], 3)

    def test_advance_preserves_other_fields(self):
        """Verify other fields in parser_state are not modified."""
        parser_state: ParserState = {
            "tokens": ["token1", "token2"],
            "pos": 0,
            "filename": "test.py",
            "error": None
        }
        
        _advance(parser_state)
        
        self.assertEqual(parser_state["tokens"], ["token1", "token2"])
        self.assertEqual(parser_state["filename"], "test.py")
        self.assertIsNone(parser_state["error"])


if __name__ == "__main__":
    unittest.main()

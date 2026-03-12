# === std / third-party imports ===
import unittest
from typing import Dict, Any

# === relative import of UUT ===
try:
    from ._parse_continue_stmt_src import _parse_continue_stmt
except ImportError:
    from _parse_continue_stmt_src import _parse_continue_stmt


class TestParseContinueStmt(unittest.TestCase):
    """Test cases for _parse_continue_stmt function."""

    def _create_parser_state(
        self,
        tokens: list,
        pos: int = 0,
        filename: str = "test.py"
    ) -> Dict[str, Any]:
        """Helper to create parser state."""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename
        }

    def _create_token(
        self,
        token_type: str,
        value: str,
        line: int = 1,
        column: int = 1
    ) -> Dict[str, Any]:
        """Helper to create a token."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    # === Happy Path Tests ===

    def test_parse_continue_stmt_valid(self):
        """Test parsing valid continue; statement."""
        tokens = [
            self._create_token("CONTINUE", "continue", line=1, column=1),
            self._create_token("SEMICOLON", ";", line=1, column=9)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        result = _parse_continue_stmt(parser_state)

        # Verify AST node structure
        self.assertEqual(result["type"], "CONTINUE_STMT")
        self.assertEqual(result["children"], [])
        self.assertIsNone(result["value"])
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)

        # Verify pos mutation
        self.assertEqual(parser_state["pos"], 2)

    def test_parse_continue_stmt_with_different_position(self):
        """Test parsing continue; when not at position 0."""
        tokens = [
            self._create_token("IDENTIFIER", "x", line=1, column=1),
            self._create_token("CONTINUE", "continue", line=2, column=5),
            self._create_token("SEMICOLON", ";", line=2, column=13)
        ]
        parser_state = self._create_parser_state(tokens, pos=1)

        result = _parse_continue_stmt(parser_state)

        self.assertEqual(result["type"], "CONTINUE_STMT")
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 5)
        self.assertEqual(parser_state["pos"], 3)

    def test_parse_continue_stmt_multiline(self):
        """Test parsing continue; across different lines."""
        tokens = [
            self._create_token("CONTINUE", "continue", line=5, column=10),
            self._create_token("SEMICOLON", ";", line=6, column=1)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        result = _parse_continue_stmt(parser_state)

        self.assertEqual(result["type"], "CONTINUE_STMT")
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 10)
        self.assertEqual(parser_state["pos"], 2)

    # === Boundary Value Tests ===

    def test_parse_continue_stmt_empty_tokens(self):
        """Test parsing with empty token list."""
        tokens = []
        parser_state = self._create_parser_state(tokens, pos=0)

        with self.assertRaises(SyntaxError) as context:
            _parse_continue_stmt(parser_state)

        self.assertIn("Unexpected end of input", str(context.exception))
        self.assertIn("expected 'continue'", str(context.exception))

    def test_parse_continue_stmt_only_continue_no_semicolon(self):
        """Test parsing continue without semicolon."""
        tokens = [
            self._create_token("CONTINUE", "continue", line=1, column=1)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        with self.assertRaises(SyntaxError) as context:
            _parse_continue_stmt(parser_state)

        self.assertIn("Unexpected end of input", str(context.exception))
        self.assertIn("expected ';'", str(context.exception))

    def test_parse_continue_stmt_pos_at_end(self):
        """Test when pos is already at end of tokens."""
        tokens = [
            self._create_token("CONTINUE", "continue", line=1, column=1)
        ]
        parser_state = self._create_parser_state(tokens, pos=1)

        with self.assertRaises(SyntaxError) as context:
            _parse_continue_stmt(parser_state)

        self.assertIn("Unexpected end of input", str(context.exception))

    # === Error Path Tests ===

    def test_parse_continue_stmt_wrong_token_type(self):
        """Test when first token is not CONTINUE."""
        tokens = [
            self._create_token("BREAK", "break", line=1, column=1),
            self._create_token("SEMICOLON", ";", line=1, column=6)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        with self.assertRaises(SyntaxError) as context:
            _parse_continue_stmt(parser_state)

        self.assertIn("Expected CONTINUE token", str(context.exception))
        self.assertIn("BREAK", str(context.exception))

    def test_parse_continue_stmt_missing_semicolon_wrong_token(self):
        """Test when semicolon is replaced by wrong token."""
        tokens = [
            self._create_token("CONTINUE", "continue", line=1, column=1),
            self._create_token("IDENTIFIER", "x", line=1, column=9)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        with self.assertRaises(SyntaxError) as context:
            _parse_continue_stmt(parser_state)

        self.assertIn("Expected ';' after continue", str(context.exception))
        self.assertIn("IDENTIFIER", str(context.exception))

    def test_parse_continue_stmt_extra_tokens_after_semicolon(self):
        """Test that extra tokens after semicolon don't affect parsing."""
        tokens = [
            self._create_token("CONTINUE", "continue", line=1, column=1),
            self._create_token("SEMICOLON", ";", line=1, column=9),
            self._create_token("IDENTIFIER", "x", line=1, column=11)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        result = _parse_continue_stmt(parser_state)

        self.assertEqual(result["type"], "CONTINUE_STMT")
        self.assertEqual(parser_state["pos"], 2)

    # === Side Effect Tests ===

    def test_parse_continue_stmt_pos_mutation_verified(self):
        """Verify that parser_state pos is mutated correctly."""
        tokens = [
            self._create_token("CONTINUE", "continue", line=1, column=1),
            self._create_token("SEMICOLON", ";", line=1, column=9)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        original_pos = parser_state["pos"]

        result = _parse_continue_stmt(parser_state)

        # Verify pos changed
        self.assertNotEqual(parser_state["pos"], original_pos)
        # Verify pos advanced by 2 (CONTINUE + SEMICOLON)
        self.assertEqual(parser_state["pos"], original_pos + 2)

    def test_parse_continue_stmt_original_dict_mutated(self):
        """Verify the same dict object is mutated."""
        tokens = [
            self._create_token("CONTINUE", "continue", line=1, column=1),
            self._create_token("SEMICOLON", ";", line=1, column=9)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        parser_state_id = id(parser_state)

        _parse_continue_stmt(parser_state)

        # Verify same object
        self.assertEqual(id(parser_state), parser_state_id)
        self.assertEqual(parser_state["pos"], 2)


if __name__ == "__main__":
    unittest.main()

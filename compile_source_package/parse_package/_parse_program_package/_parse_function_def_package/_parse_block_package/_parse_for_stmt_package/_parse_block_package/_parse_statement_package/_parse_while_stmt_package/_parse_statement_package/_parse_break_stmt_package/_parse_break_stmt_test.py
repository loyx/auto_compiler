# === std / third-party imports ===
import unittest
from typing import Any, Dict

# === relative imports ===
from ._parse_break_stmt_src import _parse_break_stmt


# === Test Cases ===
class TestParseBreakStmt(unittest.TestCase):
    """Test cases for _parse_break_stmt function."""

    def _create_parser_state(
        self,
        tokens: list,
        pos: int = 0,
        filename: str = "test.c"
    ) -> Dict[str, Any]:
        """Helper to create parser state."""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename,
            "error": ""
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

    def test_parse_break_stmt_valid(self):
        """Test valid break statement: break ;"""
        tokens = [
            self._create_token("BREAK", "break", 1, 1),
            self._create_token("SEMICOLON", ";", 1, 6)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        result = _parse_break_stmt(parser_state)

        # Verify AST node
        self.assertEqual(result["type"], "BREAK_STMT")
        self.assertEqual(result["children"], [])
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)

        # Verify parser state updated
        self.assertEqual(parser_state["pos"], 2)

    def test_parse_break_stmt_with_different_position(self):
        """Test break statement at different position in token stream."""
        tokens = [
            self._create_token("IDENTIFIER", "x", 1, 1),
            self._create_token("BREAK", "break", 1, 5),
            self._create_token("SEMICOLON", ";", 1, 10)
        ]
        parser_state = self._create_parser_state(tokens, pos=1)

        result = _parse_break_stmt(parser_state)

        self.assertEqual(result["type"], "BREAK_STMT")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 5)
        self.assertEqual(parser_state["pos"], 3)

    def test_parse_break_stmt_multiline(self):
        """Test break statement on different line."""
        tokens = [
            self._create_token("BREAK", "break", 5, 10),
            self._create_token("SEMICOLON", ";", 5, 15)
        ]
        parser_state = self._create_parser_state(tokens, pos=0, filename="main.c")

        result = _parse_break_stmt(parser_state)

        self.assertEqual(result["type"], "BREAK_STMT")
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 10)
        self.assertEqual(parser_state["pos"], 2)

    # === Error Path Tests ===

    def test_parse_break_stmt_empty_tokens(self):
        """Test error when tokens list is empty."""
        tokens = []
        parser_state = self._create_parser_state(tokens, pos=0)

        with self.assertRaises(SyntaxError) as context:
            _parse_break_stmt(parser_state)

        self.assertIn("Unexpected end of input", str(context.exception))
        self.assertIn("test.c:0:0", str(context.exception))

    def test_parse_break_stmt_pos_beyond_tokens(self):
        """Test error when pos is beyond tokens length."""
        tokens = [
            self._create_token("IDENTIFIER", "x", 1, 1)
        ]
        parser_state = self._create_parser_state(tokens, pos=5)

        with self.assertRaises(SyntaxError) as context:
            _parse_break_stmt(parser_state)

        self.assertIn("Unexpected end of input", str(context.exception))

    def test_parse_break_stmt_wrong_token_type(self):
        """Test error when current token is not BREAK."""
        tokens = [
            self._create_token("IDENTIFIER", "x", 2, 5),
            self._create_token("SEMICOLON", ";", 2, 6)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        with self.assertRaises(SyntaxError) as context:
            _parse_break_stmt(parser_state)

        self.assertIn("Expected 'break'", str(context.exception))
        self.assertIn("2:5", str(context.exception))
        self.assertIn("got 'x'", str(context.exception))

    def test_parse_break_stmt_missing_semicolon_end_of_input(self):
        """Test error when SEMICOLON is missing (end of input)."""
        tokens = [
            self._create_token("BREAK", "break", 3, 8)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        with self.assertRaises(SyntaxError) as context:
            _parse_break_stmt(parser_state)

        self.assertIn("Expected ';' after 'break'", str(context.exception))
        self.assertIn("3:8", str(context.exception))

    def test_parse_break_stmt_wrong_token_after_break(self):
        """Test error when token after BREAK is not SEMICOLON."""
        tokens = [
            self._create_token("BREAK", "break", 4, 12),
            self._create_token("IDENTIFIER", "x", 4, 18)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        with self.assertRaises(SyntaxError) as context:
            _parse_break_stmt(parser_state)

        self.assertIn("Expected ';'", str(context.exception))
        self.assertIn("4:18", str(context.exception))
        self.assertIn("got 'x'", str(context.exception))

    def test_parse_break_stmt_unknown_filename(self):
        """Test error message with missing filename."""
        tokens = []
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "error": ""
        }

        with self.assertRaises(SyntaxError) as context:
            _parse_break_stmt(parser_state)

        self.assertIn("<unknown>:0:0", str(context.exception))

    # === Edge Cases ===

    def test_parse_break_stmt_multiple_breaks(self):
        """Test parsing multiple break statements sequentially."""
        tokens = [
            self._create_token("BREAK", "break", 1, 1),
            self._create_token("SEMICOLON", ";", 1, 6),
            self._create_token("BREAK", "break", 2, 1),
            self._create_token("SEMICOLON", ";", 2, 6)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        # Parse first break
        result1 = _parse_break_stmt(parser_state)
        self.assertEqual(result1["type"], "BREAK_STMT")
        self.assertEqual(result1["line"], 1)
        self.assertEqual(parser_state["pos"], 2)

        # Parse second break
        result2 = _parse_break_stmt(parser_state)
        self.assertEqual(result2["type"], "BREAK_STMT")
        self.assertEqual(result2["line"], 2)
        self.assertEqual(parser_state["pos"], 4)

    def test_parse_break_stmt_with_extra_tokens_after(self):
        """Test break statement with extra tokens remaining."""
        tokens = [
            self._create_token("BREAK", "break", 1, 1),
            self._create_token("SEMICOLON", ";", 1, 6),
            self._create_token("IDENTIFIER", "return", 1, 8),
            self._create_token("SEMICOLON", ";", 1, 14)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        result = _parse_break_stmt(parser_state)

        self.assertEqual(result["type"], "BREAK_STMT")
        self.assertEqual(parser_state["pos"], 2)
        # Remaining tokens should not be consumed
        self.assertEqual(tokens[2]["value"], "return")


# === Test Runner ===
if __name__ == "__main__":
    unittest.main()

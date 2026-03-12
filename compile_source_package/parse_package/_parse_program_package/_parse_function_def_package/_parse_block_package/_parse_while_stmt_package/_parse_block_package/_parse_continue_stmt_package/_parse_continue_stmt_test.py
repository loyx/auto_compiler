# === std / third-party imports ===
import unittest
from typing import Any, Dict

# === relative imports ===
from ._parse_continue_stmt_src import _parse_continue_stmt

# === Type aliases for clarity ===
Token = Dict[str, Any]
ParserState = Dict[str, Any]
AST = Dict[str, Any]


class TestParseContinueStmt(unittest.TestCase):
    """Test cases for _parse_continue_stmt function."""

    def _make_token(self, token_type: str, value: str = "", line: int = 1, column: int = 1) -> Token:
        """Helper to create a token dictionary."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def _make_parser_state(self, tokens: list, pos: int = 0, filename: str = "test.py") -> ParserState:
        """Helper to create a parser state dictionary."""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename,
            "error": ""
        }

    # ==================== Happy Path Tests ====================

    def test_parse_valid_continue_stmt(self):
        """Test parsing a valid continue; statement."""
        tokens = [
            self._make_token("CONTINUE", "continue", line=5, column=10),
            self._make_token("SEMICOLON", ";", line=5, column=18)
        ]
        parser_state = self._make_parser_state(tokens, pos=0)

        result = _parse_continue_stmt(parser_state)

        # Verify AST structure
        self.assertEqual(result["type"], "CONTINUE_STMT")
        self.assertEqual(result["children"], [])
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 10)

        # Verify parser state was updated
        self.assertEqual(parser_state["pos"], 2)

    def test_parse_continue_stmt_with_different_position(self):
        """Test parsing continue; when parser is not at position 0."""
        tokens = [
            self._make_token("OTHER", "other"),
            self._make_token("OTHER", "other2"),
            self._make_token("CONTINUE", "continue", line=3, column=5),
            self._make_token("SEMICOLON", ";", line=3, column=13)
        ]
        parser_state = self._make_parser_state(tokens, pos=2)

        result = _parse_continue_stmt(parser_state)

        self.assertEqual(result["type"], "CONTINUE_STMT")
        self.assertEqual(result["line"], 3)
        self.assertEqual(result["column"], 5)
        self.assertEqual(parser_state["pos"], 4)

    # ==================== Boundary Value Tests ====================

    def test_parse_continue_stmt_at_end_of_file(self):
        """Test parsing continue; at the end of token list."""
        tokens = [
            self._make_token("CONTINUE", "continue", line=10, column=1),
            self._make_token("SEMICOLON", ";", line=10, column=9)
        ]
        parser_state = self._make_parser_state(tokens, pos=0)

        result = _parse_continue_stmt(parser_state)

        self.assertEqual(result["type"], "CONTINUE_STMT")
        self.assertEqual(parser_state["pos"], 2)

    def test_parse_continue_stmt_with_tokens_after(self):
        """Test parsing continue; when there are more tokens after."""
        tokens = [
            self._make_token("CONTINUE", "continue", line=7, column=3),
            self._make_token("SEMICOLON", ";", line=7, column=11),
            self._make_token("OTHER", "next_token", line=8, column=1)
        ]
        parser_state = self._make_parser_state(tokens, pos=0)

        result = _parse_continue_stmt(parser_state)

        self.assertEqual(result["type"], "CONTINUE_STMT")
        self.assertEqual(parser_state["pos"], 2)
        # Should not consume the token after semicolon
        self.assertEqual(tokens[parser_state["pos"]]["type"], "OTHER")

    # ==================== Error Case Tests ====================

    def test_parse_empty_tokens_list(self):
        """Test parsing with empty tokens list raises SyntaxError."""
        parser_state = self._make_parser_state([], pos=0)

        with self.assertRaises(SyntaxError) as context:
            _parse_continue_stmt(parser_state)

        self.assertIn("Unexpected end of input", str(context.exception))

    def test_parse_position_beyond_tokens(self):
        """Test parsing when position is beyond token list length."""
        tokens = [self._make_token("OTHER", "token")]
        parser_state = self._make_parser_state(tokens, pos=5)

        with self.assertRaises(SyntaxError) as context:
            _parse_continue_stmt(parser_state)

        self.assertIn("Unexpected end of input", str(context.exception))

    def test_parse_wrong_token_type_not_continue(self):
        """Test parsing when current token is not CONTINUE."""
        tokens = [
            self._make_token("BREAK", "break", line=2, column=5),
            self._make_token("SEMICOLON", ";", line=2, column=10)
        ]
        parser_state = self._make_parser_state(tokens, pos=0)

        with self.assertRaises(SyntaxError) as context:
            _parse_continue_stmt(parser_state)

        self.assertIn("Expected CONTINUE keyword", str(context.exception))
        self.assertIn("got BREAK", str(context.exception))
        # Verify position was not updated on error
        self.assertEqual(parser_state["pos"], 0)

    def test_parse_missing_semicolon_end_of_input(self):
        """Test parsing when semicolon is missing (end of input)."""
        tokens = [
            self._make_token("CONTINUE", "continue", line=4, column=2)
        ]
        parser_state = self._make_parser_state(tokens, pos=0)

        with self.assertRaises(SyntaxError) as context:
            _parse_continue_stmt(parser_state)

        self.assertIn("Expected ';' after 'continue'", str(context.exception))
        self.assertIn("line 4", str(context.exception))
        # Verify position was not updated on error
        self.assertEqual(parser_state["pos"], 0)

    def test_parse_wrong_token_after_continue(self):
        """Test parsing when token after continue is not semicolon."""
        tokens = [
            self._make_token("CONTINUE", "continue", line=6, column=8),
            self._make_token("IDENTIFIER", "x", line=6, column=16)
        ]
        parser_state = self._make_parser_state(tokens, pos=0)

        with self.assertRaises(SyntaxError) as context:
            _parse_continue_stmt(parser_state)

        self.assertIn("Expected ';' after 'continue'", str(context.exception))
        self.assertIn("got IDENTIFIER", str(context.exception))
        self.assertIn("line 6", str(context.exception))
        # Verify position was not updated on error (should still be at CONTINUE)
        self.assertEqual(parser_state["pos"], 0)

    def test_parse_continue_with_keyword_instead_of_semicolon(self):
        """Test parsing when a keyword appears instead of semicolon."""
        tokens = [
            self._make_token("CONTINUE", "continue", line=9, column=1),
            self._make_token("IF", "if", line=9, column=10)
        ]
        parser_state = self._make_parser_state(tokens, pos=0)

        with self.assertRaises(SyntaxError) as context:
            _parse_continue_stmt(parser_state)

        self.assertIn("Expected ';' after 'continue'", str(context.exception))
        self.assertIn("got IF", str(context.exception))

    # ==================== AST Structure Tests ====================

    def test_ast_node_has_required_fields(self):
        """Test that returned AST node has all required fields."""
        tokens = [
            self._make_token("CONTINUE", "continue", line=1, column=1),
            self._make_token("SEMICOLON", ";", line=1, column=9)
        ]
        parser_state = self._make_parser_state(tokens, pos=0)

        result = _parse_continue_stmt(parser_state)

        # Check all required fields exist
        self.assertIn("type", result)
        self.assertIn("children", result)
        self.assertIn("line", result)
        self.assertIn("column", result)

        # Check field types
        self.assertIsInstance(result["type"], str)
        self.assertIsInstance(result["children"], list)
        self.assertIsInstance(result["line"], int)
        self.assertIsInstance(result["column"], int)

    def test_ast_node_children_is_empty_list(self):
        """Test that CONTINUE_STMT has empty children list."""
        tokens = [
            self._make_token("CONTINUE", "continue"),
            self._make_token("SEMICOLON", ";")
        ]
        parser_state = self._make_parser_state(tokens, pos=0)

        result = _parse_continue_stmt(parser_state)

        self.assertEqual(result["children"], [])
        self.assertEqual(len(result["children"]), 0)

    # ==================== Line/Column Preservation Tests ====================

    def test_preserves_line_column_from_continue_token(self):
        """Test that line and column are preserved from CONTINUE token."""
        tokens = [
            self._make_token("CONTINUE", "continue", line=15, column=25),
            self._make_token("SEMICOLON", ";", line=15, column=33)
        ]
        parser_state = self._make_parser_state(tokens, pos=0)

        result = _parse_continue_stmt(parser_state)

        self.assertEqual(result["line"], 15)
        self.assertEqual(result["column"], 25)

    def test_preserves_line_column_multiline_scenario(self):
        """Test line/column when continue and semicolon are on different lines."""
        tokens = [
            self._make_token("CONTINUE", "continue", line=10, column=5),
            self._make_token("SEMICOLON", ";", line=11, column=1)
        ]
        parser_state = self._make_parser_state(tokens, pos=0)

        result = _parse_continue_stmt(parser_state)

        # Should use CONTINUE token's position, not semicolon's
        self.assertEqual(result["line"], 10)
        self.assertEqual(result["column"], 5)


class TestParseContinueStmtEdgeCases(unittest.TestCase):
    """Additional edge case tests for _parse_continue_stmt."""

    def _make_token(self, token_type: str, value: str = "", line: int = 1, column: int = 1) -> Token:
        """Helper to create a token dictionary."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def _make_parser_state(self, tokens: list, pos: int = 0, filename: str = "test.py") -> ParserState:
        """Helper to create a parser state dictionary."""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename,
            "error": ""
        }

    def test_parser_state_not_modified_on_success_except_pos(self):
        """Test that parser state fields other than pos are not modified on success."""
        tokens = [
            self._make_token("CONTINUE", "continue"),
            self._make_token("SEMICOLON", ";")
        ]
        parser_state = self._make_parser_state(tokens, pos=0, filename="original.py")
        original_filename = parser_state["filename"]
        original_error = parser_state["error"]

        _parse_continue_stmt(parser_state)

        # Only pos should change
        self.assertEqual(parser_state["filename"], original_filename)
        self.assertEqual(parser_state["error"], original_error)

    def test_multiple_continue_statements_sequential(self):
        """Test parsing multiple continue statements sequentially."""
        tokens = [
            self._make_token("CONTINUE", "continue", line=1, column=1),
            self._make_token("SEMICOLON", ";", line=1, column=9),
            self._make_token("CONTINUE", "continue", line=2, column=1),
            self._make_token("SEMICOLON", ";", line=2, column=9)
        ]
        parser_state = self._make_parser_state(tokens, pos=0)

        # Parse first continue
        result1 = _parse_continue_stmt(parser_state)
        self.assertEqual(result1["line"], 1)
        self.assertEqual(parser_state["pos"], 2)

        # Parse second continue
        result2 = _parse_continue_stmt(parser_state)
        self.assertEqual(result2["line"], 2)
        self.assertEqual(parser_state["pos"], 4)


if __name__ == "__main__":
    unittest.main()

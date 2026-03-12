# === std / third-party imports ===
import unittest
from unittest.mock import patch
from typing import Dict, Any

# === relative imports ===
from ._parse_block_src import _parse_block


class TestParseBlock(unittest.TestCase):
    """Test cases for _parse_block function."""

    def _create_parser_state(
        self,
        tokens: list,
        filename: str = "test.py",
        pos: int = 0
    ) -> Dict[str, Any]:
        """Helper to create parser state dict."""
        return {
            "tokens": tokens,
            "filename": filename,
            "pos": pos,
            "error": None
        }

    def _create_token(
        self,
        token_type: str,
        value: str = "",
        line: int = 1,
        column: int = 1
    ) -> Dict[str, Any]:
        """Helper to create a token dict."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def test_parse_empty_block(self):
        """Test parsing an empty block (LBRACE followed immediately by RBRACE)."""
        tokens = [
            self._create_token("LBRACE", line=1, column=1),
            self._create_token("RBRACE", line=1, column=2)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        with patch("._parse_statement_package._parse_statement_src._parse_statement") as mock_parse_stmt:
            result = _parse_block(parser_state)

        # Verify result structure
        self.assertEqual(result["type"], "BLOCK")
        self.assertEqual(result["statements"], [])
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)

        # Verify pos is after RBRACE
        self.assertEqual(parser_state["pos"], 2)

        # Verify _parse_statement was not called (empty block)
        mock_parse_stmt.assert_not_called()

    def test_parse_block_with_statements(self):
        """Test parsing a block with multiple statements."""
        tokens = [
            self._create_token("LBRACE", line=1, column=1),
            self._create_token("IDENT", "x", line=2, column=1),
            self._create_token("IDENT", "y", line=3, column=1),
            self._create_token("RBRACE", line=4, column=1)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        # Mock _parse_statement to return different AST nodes
        mock_stmt1 = {"type": "EXPR_STMT", "value": "x", "line": 2, "column": 1}
        mock_stmt2 = {"type": "EXPR_STMT", "value": "y", "line": 3, "column": 1}

        with patch("._parse_statement_package._parse_statement_src._parse_statement") as mock_parse_stmt:
            mock_parse_stmt.side_effect = [mock_stmt1, mock_stmt2]
            result = _parse_block(parser_state)

        # Verify result structure
        self.assertEqual(result["type"], "BLOCK")
        self.assertEqual(len(result["statements"]), 2)
        self.assertEqual(result["statements"][0], mock_stmt1)
        self.assertEqual(result["statements"][1], mock_stmt2)
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)

        # Verify pos is after RBRACE
        self.assertEqual(parser_state["pos"], 4)

        # Verify _parse_statement was called twice
        self.assertEqual(mock_parse_stmt.call_count, 2)

    def test_parse_block_missing_lbrace(self):
        """Test that SyntaxError is raised when LBRACE is missing."""
        tokens = [
            self._create_token("IDENT", "x", line=1, column=1),
            self._create_token("RBRACE", line=1, column=2)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        with self.assertRaises(SyntaxError) as context:
            _parse_block(parser_state)

        # Verify error message format
        error_msg = str(context.exception)
        self.assertIn("test.py:1:1", error_msg)
        self.assertIn("Expected LBRACE", error_msg)
        self.assertIn("IDENT", error_msg)

        # Verify pos was not advanced (error before consuming)
        self.assertEqual(parser_state["pos"], 0)

    def test_parse_block_missing_rbrace_eof(self):
        """Test that SyntaxError is raised when RBRACE is missing (unexpected EOF)."""
        tokens = [
            self._create_token("LBRACE", line=1, column=1),
            self._create_token("IDENT", "x", line=2, column=1)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        # Mock _parse_statement to return one statement, then we'll hit EOF
        mock_stmt = {"type": "EXPR_STMT", "value": "x", "line": 2, "column": 1}

        with patch("._parse_statement_package._parse_statement_src._parse_statement") as mock_parse_stmt:
            mock_parse_stmt.return_value = mock_stmt
            with self.assertRaises(SyntaxError) as context:
                _parse_block(parser_state)

        # Verify error message format
        error_msg = str(context.exception)
        self.assertIn("test.py:1:1", error_msg)
        self.assertIn("Unexpected end of file", error_msg)
        self.assertIn("expected RBRACE", error_msg)

    def test_parse_block_position_advancement(self):
        """Test that parser_state pos is correctly advanced through the block."""
        tokens = [
            self._create_token("LBRACE", line=1, column=1),
            self._create_token("IDENT", "stmt1", line=2, column=1),
            self._create_token("IDENT", "stmt2", line=3, column=1),
            self._create_token("IDENT", "stmt3", line=4, column=1),
            self._create_token("RBRACE", line=5, column=1),
            self._create_token("IDENT", "after", line=6, column=1)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        mock_stmt1 = {"type": "EXPR_STMT", "value": "stmt1", "line": 2, "column": 1}
        mock_stmt2 = {"type": "EXPR_STMT", "value": "stmt2", "line": 3, "column": 1}
        mock_stmt3 = {"type": "EXPR_STMT", "value": "stmt3", "line": 4, "column": 1}

        with patch("._parse_statement_package._parse_statement_src._parse_statement") as mock_parse_stmt:
            mock_parse_stmt.side_effect = [mock_stmt1, mock_stmt2, mock_stmt3]
            result = _parse_block(parser_state)

        # Verify pos points to token after RBRACE
        self.assertEqual(parser_state["pos"], 5)

        # Verify we can still access the token after the block
        self.assertEqual(tokens[parser_state["pos"]]["type"], "IDENT")
        self.assertEqual(tokens[parser_state["pos"]]["value"], "after")

    def test_parse_block_line_column_preservation(self):
        """Test that line and column from LBRACE are preserved in result."""
        tokens = [
            self._create_token("LBRACE", line=10, column=5),
            self._create_token("RBRACE", line=15, column=3)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        with patch("._parse_statement_package._parse_statement_src._parse_statement"):
            result = _parse_block(parser_state)

        # Verify line and column come from LBRACE, not RBRACE
        self.assertEqual(result["line"], 10)
        self.assertEqual(result["column"], 5)

    def test_parse_block_with_custom_filename(self):
        """Test that error messages use the correct filename."""
        tokens = [
            self._create_token("IDENT", "x", line=1, column=1)
        ]
        parser_state = self._create_parser_state(tokens, filename="my_module.py", pos=0)

        with self.assertRaises(SyntaxError) as context:
            _parse_block(parser_state)

        error_msg = str(context.exception)
        self.assertIn("my_module.py:1:1", error_msg)


if __name__ == "__main__":
    unittest.main()

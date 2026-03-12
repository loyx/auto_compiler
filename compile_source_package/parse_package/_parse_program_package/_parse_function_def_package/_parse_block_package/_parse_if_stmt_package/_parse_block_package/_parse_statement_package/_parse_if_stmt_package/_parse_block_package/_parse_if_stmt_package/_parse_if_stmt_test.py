# === imports ===
import unittest
from unittest.mock import patch
from typing import Dict, Any

# === import the function under test ===
from ._parse_if_stmt_src import _parse_if_stmt


class TestParseIfStmt(unittest.TestCase):
    """Test cases for _parse_if_stmt function."""

    def _create_parser_state(self, tokens: list, pos: int = 0, filename: str = "test.c") -> Dict[str, Any]:
        """Helper to create parser state."""
        return {
            "tokens": tokens,
            "filename": filename,
            "pos": pos
        }

    def _create_token(self, token_type: str, value: str = "", line: int = 1, column: int = 1) -> Dict[str, Any]:
        """Helper to create a token."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    @patch('._parse_if_stmt_src._parse_expression')
    @patch('._parse_if_stmt_src._parse_block')
    @patch('._parse_if_stmt_src._consume_token')
    def test_if_without_else(self, mock_consume, mock_parse_block, mock_parse_expr):
        """Test parsing if statement without else block."""
        # Setup mocks
        mock_parse_expr.return_value = {"type": "EXPR", "value": "x > 0", "line": 1, "column": 4}
        mock_parse_block.return_value = {"type": "BLOCK", "statements": [], "line": 1, "column": 11}

        tokens = [
            self._create_token("IF", "if", 1, 1),
            self._create_token("LPAREN", "(", 1, 3),
            self._create_token("IDENT", "x", 1, 4),
            self._create_token("GT", ">", 1, 6),
            self._create_token("NUM", "0", 1, 8),
            self._create_token("RPAREN", ")", 1, 9),
            self._create_token("LBRACE", "{", 1, 11),
            self._create_token("RBRACE", "}", 1, 12),
        ]

        parser_state = self._create_parser_state(tokens)

        result = _parse_if_stmt(parser_state)

        # Verify result structure
        self.assertEqual(result["type"], "IF")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(result["condition"], {"type": "EXPR", "value": "x > 0", "line": 1, "column": 4})
        self.assertEqual(result["then_block"], {"type": "BLOCK", "statements": [], "line": 1, "column": 11})
        self.assertIsNone(result["else_block"])

        # Verify consume_token was called for IF, LPAREN, RPAREN (not ELSE)
        consume_types = [call_args[0][1] for call_args in mock_consume.call_args_list]
        self.assertEqual(consume_types, ["IF", "LPAREN", "RPAREN"])

    @patch('._parse_if_stmt_src._parse_expression')
    @patch('._parse_if_stmt_src._parse_block')
    @patch('._parse_if_stmt_src._consume_token')
    def test_if_with_else(self, mock_consume, mock_parse_block, mock_parse_expr):
        """Test parsing if statement with else block."""
        # Setup mocks
        mock_parse_expr.return_value = {"type": "EXPR", "value": "x == 0", "line": 2, "column": 4}
        mock_parse_block.side_effect = [
            {"type": "BLOCK", "statements": [], "line": 2, "column": 12},  # then block
            {"type": "BLOCK", "statements": [], "line": 2, "column": 20}   # else block
        ]

        tokens = [
            self._create_token("IF", "if", 2, 1),
            self._create_token("LPAREN", "(", 2, 3),
            self._create_token("IDENT", "x", 2, 4),
            self._create_token("EQ", "==", 2, 6),
            self._create_token("NUM", "0", 2, 9),
            self._create_token("RPAREN", ")", 2, 10),
            self._create_token("LBRACE", "{", 2, 12),
            self._create_token("RBRACE", "}", 2, 13),
            self._create_token("ELSE", "else", 2, 15),
            self._create_token("LBRACE", "{", 2, 20),
            self._create_token("RBRACE", "}", 2, 21),
        ]

        parser_state = self._create_parser_state(tokens)

        result = _parse_if_stmt(parser_state)

        # Verify result structure
        self.assertEqual(result["type"], "IF")
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 1)
        self.assertEqual(result["condition"], {"type": "EXPR", "value": "x == 0", "line": 2, "column": 4})
        self.assertIsNotNone(result["then_block"])
        self.assertIsNotNone(result["else_block"])

        # Verify consume_token was called for IF, LPAREN, RPAREN, ELSE
        consume_types = [call_args[0][1] for call_args in mock_consume.call_args_list]
        self.assertEqual(consume_types, ["IF", "LPAREN", "RPAREN", "ELSE"])

    @patch('._parse_if_stmt_src._parse_expression')
    @patch('._parse_if_stmt_src._parse_block')
    @patch('._parse_if_stmt_src._consume_token')
    def test_if_with_nested_blocks(self, mock_consume, mock_parse_block, mock_parse_expr):
        """Test parsing if statement with non-empty blocks."""
        # Setup mocks
        mock_parse_expr.return_value = {"type": "BINARY", "left": "x", "op": ">", "right": "0", "line": 1, "column": 5}
        mock_parse_block.side_effect = [
            {"type": "BLOCK", "statements": [{"type": "ASSIGN", "target": "y", "value": "1"}], "line": 1, "column": 15},
            {"type": "BLOCK", "statements": [{"type": "ASSIGN", "target": "y", "value": "2"}], "line": 2, "column": 5}
        ]

        tokens = [
            self._create_token("IF", "if", 1, 1),
            self._create_token("LPAREN", "(", 1, 3),
            self._create_token("IDENT", "x", 1, 5),
            self._create_token("GT", ">", 1, 7),
            self._create_token("NUM", "0", 1, 9),
            self._create_token("RPAREN", ")", 1, 10),
            self._create_token("LBRACE", "{", 1, 15),
            self._create_token("RBRACE", "}", 1, 20),
            self._create_token("ELSE", "else", 2, 1),
            self._create_token("LBRACE", "{", 2, 5),
            self._create_token("RBRACE", "}", 2, 10),
        ]

        parser_state = self._create_parser_state(tokens)

        result = _parse_if_stmt(parser_state)

        # Verify blocks contain statements
        self.assertEqual(len(result["then_block"]["statements"]), 1)
        self.assertEqual(len(result["else_block"]["statements"]), 1)

    def test_unexpected_end_of_input(self):
        """Test handling of unexpected end of input (empty tokens)."""
        tokens = []
        parser_state = self._create_parser_state(tokens)

        with self.assertRaises(SyntaxError) as context:
            _parse_if_stmt(parser_state)

        self.assertIn("Unexpected end of input", str(context.exception))

    @patch('._parse_if_stmt_src._consume_token')
    def test_consume_token_raises_error(self, mock_consume):
        """Test that SyntaxError from consume_token is propagated."""
        mock_consume.side_effect = SyntaxError("test.c:1:1: Expected IF token, found IDENT")

        tokens = [self._create_token("IDENT", "x", 1, 1)]
        parser_state = self._create_parser_state(tokens)

        with self.assertRaises(SyntaxError) as context:
            _parse_if_stmt(parser_state)

        self.assertIn("Expected IF token", str(context.exception))

    @patch('._parse_if_stmt_src._parse_expression')
    @patch('._parse_if_stmt_src._parse_block')
    @patch('._parse_if_stmt_src._consume_token')
    def test_parser_state_pos_updated(self, mock_consume, mock_parse_block, mock_parse_expr):
        """Test that parser_state pos is updated after parsing."""
        # Setup mocks to simulate pos updates
        def consume_side_effect(state, expected_type):
            state["pos"] += 1

        mock_consume.side_effect = consume_side_effect
        mock_parse_expr.return_value = {"type": "EXPR", "line": 1, "column": 1}
        mock_parse_block.return_value = {"type": "BLOCK", "statements": [], "line": 1, "column": 1}

        tokens = [
            self._create_token("IF", "if", 1, 1),
            self._create_token("LPAREN", "(", 1, 3),
            self._create_token("IDENT", "x", 1, 4),
            self._create_token("RPAREN", ")", 1, 5),
            self._create_token("LBRACE", "{", 1, 6),
            self._create_token("RBRACE", "}", 1, 7),
        ]

        parser_state = self._create_parser_state(tokens, pos=0)
        initial_pos = parser_state["pos"]

        _parse_if_stmt(parser_state)

        # pos should be updated (at least consumed IF, LPAREN, RPAREN)
        self.assertGreater(parser_state["pos"], initial_pos)

    @patch('._parse_if_stmt_src._parse_expression')
    @patch('._parse_if_stmt_src._parse_block')
    @patch('._parse_if_stmt_src._consume_token')
    def test_else_not_consumed_when_absent(self, mock_consume, mock_parse_block, mock_parse_expr):
        """Test that ELSE token is not consumed when not present."""
        mock_parse_expr.return_value = {"type": "EXPR", "line": 1, "column": 1}
        mock_parse_block.return_value = {"type": "BLOCK", "statements": [], "line": 1, "column": 1}

        # Tokens without ELSE
        tokens = [
            self._create_token("IF", "if", 1, 1),
            self._create_token("LPAREN", "(", 1, 3),
            self._create_token("IDENT", "x", 1, 4),
            self._create_token("RPAREN", ")", 1, 5),
            self._create_token("LBRACE", "{", 1, 6),
            self._create_token("RBRACE", "}", 1, 7),
            self._create_token("IDENT", "next", 1, 8),  # Next statement, not ELSE
        ]

        parser_state = self._create_parser_state(tokens)

        result = _parse_if_stmt(parser_state)

        # Verify else_block is None
        self.assertIsNone(result["else_block"])

        # Verify ELSE was not consumed
        consume_types = [call_args[0][1] for call_args in mock_consume.call_args_list]
        self.assertNotIn("ELSE", consume_types)

    @patch('._parse_if_stmt_src._parse_expression')
    @patch('._parse_if_stmt_src._parse_block')
    @patch('._parse_if_stmt_src._consume_token')
    def test_different_line_column_positions(self, mock_consume, mock_parse_block, mock_parse_expr):
        """Test that line and column are correctly captured from IF token."""
        mock_parse_expr.return_value = {"type": "EXPR", "line": 5, "column": 10}
        mock_parse_block.return_value = {"type": "BLOCK", "statements": [], "line": 5, "column": 20}

        tokens = [
            self._create_token("IF", "if", 5, 10),
            self._create_token("LPAREN", "(", 5, 12),
            self._create_token("IDENT", "x", 5, 13),
            self._create_token("RPAREN", ")", 5, 14),
            self._create_token("LBRACE", "{", 5, 20),
            self._create_token("RBRACE", "}", 5, 25),
        ]

        parser_state = self._create_parser_state(tokens)

        result = _parse_if_stmt(parser_state)

        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 10)


if __name__ == "__main__":
    unittest.main()

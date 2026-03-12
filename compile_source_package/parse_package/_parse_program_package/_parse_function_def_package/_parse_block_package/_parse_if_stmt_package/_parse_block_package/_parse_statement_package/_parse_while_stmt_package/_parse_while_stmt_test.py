# === std / third-party imports ===
import unittest
from unittest.mock import patch
from typing import Any, Dict, List

# === sub function imports ===
from ._parse_while_stmt_src import _parse_while_stmt


class TestParseWhileStmt(unittest.TestCase):
    """Test cases for _parse_while_stmt function."""

    def _create_token(self, token_type: str, value: str, line: int, column: int) -> Dict[str, Any]:
        """Helper to create a token dict."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def _create_parser_state(self, tokens: List[Dict[str, Any]], pos: int = 0, filename: str = "test.c") -> Dict[str, Any]:
        """Helper to create a parser state dict."""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename
        }

    def test_happy_path_simple_while(self):
        """Test parsing a simple while statement with valid condition and body."""
        tokens = [
            self._create_token("WHILE", "while", 1, 0),
            self._create_token("LPAREN", "(", 1, 6),
            self._create_token("IDENTIFIER", "x", 1, 8),
            self._create_token("RPAREN", ")", 1, 9),
            self._create_token("LBRACE", "{", 1, 11),
            self._create_token("RBRACE", "}", 1, 12),
        ]
        parser_state = self._create_parser_state(tokens)

        mock_condition_ast = {"type": "EXPR", "value": "x"}
        mock_body_ast = {"type": "BLOCK", "children": []}

        with patch("._parse_while_stmt_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr, \
             patch("._parse_while_stmt_package._parse_block_package._parse_block_src._parse_block") as mock_parse_block:
            mock_parse_expr.return_value = mock_condition_ast
            mock_parse_block.return_value = mock_body_ast

            result = _parse_while_stmt(parser_state)

        self.assertEqual(result["type"], "WHILE_STMT")
        self.assertEqual(result["condition"], mock_condition_ast)
        self.assertEqual(result["body"], mock_body_ast)
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 0)
        self.assertEqual(parser_state["pos"], 6)  # All tokens consumed

    def test_happy_path_with_complex_condition(self):
        """Test parsing while with complex condition expression."""
        tokens = [
            self._create_token("WHILE", "while", 2, 4),
            self._create_token("LPAREN", "(", 2, 10),
            self._create_token("IDENTIFIER", "i", 2, 12),
            self._create_token("LT", "<", 2, 14),
            self._create_token("NUMBER", "10", 2, 16),
            self._create_token("RPAREN", ")", 2, 18),
            self._create_token("LBRACE", "{", 2, 20),
            self._create_token("RBRACE", "}", 2, 21),
        ]
        parser_state = self._create_parser_state(tokens)

        mock_condition_ast = {"type": "BINARY_OP", "left": "i", "op": "<", "right": "10"}
        mock_body_ast = {"type": "BLOCK", "children": []}

        with patch("._parse_while_stmt_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr, \
             patch("._parse_while_stmt_package._parse_block_package._parse_block_src._parse_block") as mock_parse_block:
            mock_parse_expr.return_value = mock_condition_ast
            mock_parse_block.return_value = mock_body_ast

            result = _parse_while_stmt(parser_state)

        self.assertEqual(result["type"], "WHILE_STMT")
        self.assertEqual(result["condition"], mock_condition_ast)
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 4)

    def test_empty_tokens_raises_syntax_error(self):
        """Test that empty token list raises SyntaxError."""
        parser_state = self._create_parser_state([], pos=0, filename="empty.c")

        with self.assertRaises(SyntaxError) as context:
            _parse_while_stmt(parser_state)

        self.assertIn("empty.c:0:0: Unexpected end of input while parsing while statement", str(context.exception))

    def test_pos_at_end_raises_syntax_error(self):
        """Test that pos >= len(tokens) raises SyntaxError."""
        tokens = [self._create_token("WHILE", "while", 1, 0)]
        parser_state = self._create_parser_state(tokens, pos=1, filename="end.c")

        with self.assertRaises(SyntaxError) as context:
            _parse_while_stmt(parser_state)

        self.assertIn("end.c:0:0: Unexpected end of input while parsing while statement", str(context.exception))

    def test_missing_lparen_raises_syntax_error(self):
        """Test that missing LPAREN after WHILE raises SyntaxError."""
        tokens = [
            self._create_token("WHILE", "while", 3, 5),
            self._create_token("IDENTIFIER", "x", 3, 11),
        ]
        parser_state = self._create_parser_state(tokens, filename="missing_lparen.c")

        with self.assertRaises(SyntaxError) as context:
            _parse_while_stmt(parser_state)

        self.assertIn("missing_lparen.c:3:5: Expected '(' after 'while'", str(context.exception))

    def test_wrong_token_for_lparen_raises_syntax_error(self):
        """Test that wrong token type for LPAREN raises SyntaxError."""
        tokens = [
            self._create_token("WHILE", "while", 4, 0),
            self._create_token("LBRACE", "{", 4, 6),
        ]
        parser_state = self._create_parser_state(tokens, filename="wrong_lparen.c")

        with self.assertRaises(SyntaxError) as context:
            _parse_while_stmt(parser_state)

        self.assertIn("wrong_lparen.c:4:6: Expected '(' after 'while', got '{'", str(context.exception))

    def test_missing_rparen_raises_syntax_error(self):
        """Test that missing RPAREN after condition raises SyntaxError."""
        tokens = [
            self._create_token("WHILE", "while", 5, 0),
            self._create_token("LPAREN", "(", 5, 6),
            self._create_token("IDENTIFIER", "x", 5, 8),
        ]
        parser_state = self._create_parser_state(tokens, filename="missing_rparen.c")

        mock_condition_ast = {"type": "EXPR", "value": "x"}

        with patch("._parse_while_stmt_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = mock_condition_ast
            mock_parse_expr.side_effect = lambda state: state.update({"pos": 3}) or mock_condition_ast

            with self.assertRaises(SyntaxError) as context:
                _parse_while_stmt(parser_state)

        self.assertIn("missing_rparen.c:5:0: Expected ')' after condition expression", str(context.exception))

    def test_wrong_token_for_rparen_raises_syntax_error(self):
        """Test that wrong token type for RPAREN raises SyntaxError."""
        tokens = [
            self._create_token("WHILE", "while", 6, 0),
            self._create_token("LPAREN", "(", 6, 6),
            self._create_token("IDENTIFIER", "x", 6, 8),
            self._create_token("LBRACE", "{", 6, 10),
        ]
        parser_state = self._create_parser_state(tokens, filename="wrong_rparen.c")

        mock_condition_ast = {"type": "EXPR", "value": "x"}

        def mock_parse_expression_side_effect(state):
            state["pos"] = 3
            return mock_condition_ast

        with patch("._parse_while_stmt_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.side_effect = mock_parse_expression_side_effect

            with self.assertRaises(SyntaxError) as context:
                _parse_while_stmt(parser_state)

        self.assertIn("wrong_rparen.c:6:10: Expected ')' after condition, got '{'", str(context.exception))

    def test_parser_state_pos_updated_correctly(self):
        """Test that parser_state pos is updated correctly through the parsing."""
        tokens = [
            self._create_token("WHILE", "while", 1, 0),
            self._create_token("LPAREN", "(", 1, 6),
            self._create_token("IDENTIFIER", "x", 1, 8),
            self._create_token("RPAREN", ")", 1, 9),
            self._create_token("LBRACE", "{", 1, 11),
            self._create_token("RBRACE", "}", 1, 12),
        ]
        parser_state = self._create_parser_state(tokens)

        mock_condition_ast = {"type": "EXPR", "value": "x"}
        mock_body_ast = {"type": "BLOCK", "children": []}

        def mock_parse_expression_side_effect(state):
            state["pos"] = 3  # After consuming identifier
            return mock_condition_ast

        def mock_parse_block_side_effect(state):
            state["pos"] = 6  # After consuming LBRACE and RBRACE
            return mock_body_ast

        with patch("._parse_while_stmt_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr, \
             patch("._parse_while_stmt_package._parse_block_package._parse_block_src._parse_block") as mock_parse_block:
            mock_parse_expr.side_effect = mock_parse_expression_side_effect
            mock_parse_block.side_effect = mock_parse_block_side_effect

            result = _parse_while_stmt(parser_state)

        self.assertEqual(parser_state["pos"], 6)
        self.assertIsNotNone(result)

    def test_ast_node_structure(self):
        """Test that the returned AST node has all required fields."""
        tokens = [
            self._create_token("WHILE", "while", 10, 20),
            self._create_token("LPAREN", "(", 10, 26),
            self._create_token("IDENTIFIER", "flag", 10, 28),
            self._create_token("RPAREN", ")", 10, 32),
            self._create_token("LBRACE", "{", 10, 34),
            self._create_token("RBRACE", "}", 10, 35),
        ]
        parser_state = self._create_parser_state(tokens)

        mock_condition_ast = {"type": "IDENTIFIER", "value": "flag"}
        mock_body_ast = {"type": "BLOCK", "children": []}

        with patch("._parse_while_stmt_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr, \
             patch("._parse_while_stmt_package._parse_block_package._parse_block_src._parse_block") as mock_parse_block:
            mock_parse_expr.return_value = mock_condition_ast
            mock_parse_block.return_value = mock_body_ast

            result = _parse_while_stmt(parser_state)

        self.assertIn("type", result)
        self.assertIn("condition", result)
        self.assertIn("body", result)
        self.assertIn("line", result)
        self.assertIn("column", result)
        self.assertEqual(result["type"], "WHILE_STMT")
        self.assertEqual(result["line"], 10)
        self.assertEqual(result["column"], 20)

    def test_nested_while_statements(self):
        """Test parsing nested while statements."""
        tokens = [
            self._create_token("WHILE", "while", 1, 0),
            self._create_token("LPAREN", "(", 1, 6),
            self._create_token("IDENTIFIER", "outer", 1, 8),
            self._create_token("RPAREN", ")", 1, 13),
            self._create_token("LBRACE", "{", 1, 15),
            self._create_token("WHILE", "while", 2, 4),
            self._create_token("LPAREN", "(", 2, 10),
            self._create_token("IDENTIFIER", "inner", 2, 12),
            self._create_token("RPAREN", ")", 2, 17),
            self._create_token("LBRACE", "{", 2, 19),
            self._create_token("RBRACE", "}", 2, 20),
            self._create_token("RBRACE", "}", 3, 0),
        ]
        parser_state = self._create_parser_state(tokens)

        mock_outer_condition = {"type": "IDENTIFIER", "value": "outer"}
        mock_inner_condition = {"type": "IDENTIFIER", "value": "inner"}
        mock_inner_body = {"type": "BLOCK", "children": []}
        mock_outer_body = {"type": "BLOCK", "children": []}

        call_count = {"expr": 0, "block": 0}

        def mock_parse_expression_side_effect(state):
            call_count["expr"] += 1
            if call_count["expr"] == 1:
                state["pos"] = 3
                return mock_outer_condition
            else:
                state["pos"] = 9
                return mock_inner_condition

        def mock_parse_block_side_effect(state):
            call_count["block"] += 1
            if call_count["block"] == 1:
                state["pos"] = 12
                return mock_outer_body
            else:
                state["pos"] = 11
                return mock_inner_body

        with patch("._parse_while_stmt_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr, \
             patch("._parse_while_stmt_package._parse_block_package._parse_block_src._parse_block") as mock_parse_block:
            mock_parse_expr.side_effect = mock_parse_expression_side_effect
            mock_parse_block.side_effect = mock_parse_block_side_effect

            result = _parse_while_stmt(parser_state)

        self.assertEqual(result["type"], "WHILE_STMT")
        self.assertEqual(result["condition"], mock_outer_condition)
        self.assertEqual(parser_state["pos"], 12)


if __name__ == "__main__":
    unittest.main()

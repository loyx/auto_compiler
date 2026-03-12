# === std / third-party imports ===
import unittest
from unittest.mock import patch
from typing import Dict, Any

# === UUT import ===
from ._parse_for_stmt_src import _parse_for_stmt


# === Test Helper Functions ===
def _make_token(token_type: str, value: str = "", line: int = 1, column: int = 1) -> Dict[str, Any]:
    """Helper to create a token dict."""
    return {"type": token_type, "value": value, "line": line, "column": column}


def _make_parser_state(tokens: list, filename: str = "test.c") -> Dict[str, Any]:
    """Helper to create a parser state dict."""
    return {"tokens": tokens, "pos": 0, "filename": filename}


# === Test Cases ===
class TestParseForStmt(unittest.TestCase):
    """Test cases for _parse_for_stmt function."""

    def test_happy_path_all_expressions(self):
        """Test FOR statement with all three expressions present."""
        tokens = [
            _make_token("FOR", "for", 1, 1),
            _make_token("LPAREN", "(", 1, 5),
            _make_token("IDENTIFIER", "i", 1, 6),
            _make_token("SEMICOLON", ";", 1, 7),
            _make_token("IDENTIFIER", "i", 1, 9),
            _make_token("SEMICOLON", ";", 1, 10),
            _make_token("IDENTIFIER", "i", 1, 12),
            _make_token("RPAREN", ")", 1, 13),
            _make_token("LBRACE", "{", 1, 15),
            _make_token("RBRACE", "}", 1, 16),
        ]
        parser_state = _make_parser_state(tokens)
        
        with patch("._parse_for_stmt_src._parse_expression") as mock_parse_expr, \
             patch("._parse_for_stmt_src._parse_block") as mock_parse_block:
            # Setup mocks to return dummy ASTs and advance pos
            def parse_expr_side_effect(state):
                state["pos"] += 1  # Consume one token
                return {"type": "EXPR", "value": "dummy"}
            
            mock_parse_expr.side_effect = parse_expr_side_effect
            mock_parse_block.return_value = {"type": "BLOCK", "children": []}
            
            result = _parse_for_stmt(parser_state)
            
            # Verify result structure
            self.assertEqual(result["type"], "FOR")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            self.assertIsNotNone(result["initializer"])
            self.assertIsNotNone(result["condition"])
            self.assertIsNotNone(result["increment"])
            self.assertIsNotNone(result["body"])
            
            # Verify pos advancement
            self.assertEqual(parser_state["pos"], len(tokens))
            
            # Verify mock calls
            self.assertEqual(mock_parse_expr.call_count, 3)
            mock_parse_block.assert_called_once()

    def test_empty_initializer(self):
        """Test FOR statement with empty initializer: for (; cond; inc) block"""
        tokens = [
            _make_token("FOR", "for", 1, 1),
            _make_token("LPAREN", "(", 1, 5),
            _make_token("SEMICOLON", ";", 1, 6),
            _make_token("IDENTIFIER", "i", 1, 8),
            _make_token("SEMICOLON", ";", 1, 9),
            _make_token("IDENTIFIER", "i", 1, 11),
            _make_token("RPAREN", ")", 1, 12),
            _make_token("LBRACE", "{", 1, 14),
            _make_token("RBRACE", "}", 1, 15),
        ]
        parser_state = _make_parser_state(tokens)
        
        with patch("._parse_for_stmt_src._parse_expression") as mock_parse_expr, \
             patch("._parse_for_stmt_src._parse_block") as mock_parse_block:
            def parse_expr_side_effect(state):
                state["pos"] += 1
                return {"type": "EXPR", "value": "dummy"}
            
            mock_parse_expr.side_effect = parse_expr_side_effect
            mock_parse_block.return_value = {"type": "BLOCK", "children": []}
            
            result = _parse_for_stmt(parser_state)
            
            self.assertEqual(result["type"], "FOR")
            self.assertIsNone(result["initializer"])
            self.assertIsNotNone(result["condition"])
            self.assertIsNotNone(result["increment"])
            
            # _parse_expression should be called only 2 times (condition and increment)
            self.assertEqual(mock_parse_expr.call_count, 2)

    def test_empty_condition(self):
        """Test FOR statement with empty condition: for (init; ; inc) block"""
        tokens = [
            _make_token("FOR", "for", 1, 1),
            _make_token("LPAREN", "(", 1, 5),
            _make_token("IDENTIFIER", "i", 1, 6),
            _make_token("SEMICOLON", ";", 1, 7),
            _make_token("SEMICOLON", ";", 1, 9),
            _make_token("IDENTIFIER", "i", 1, 11),
            _make_token("RPAREN", ")", 1, 12),
            _make_token("LBRACE", "{", 1, 14),
            _make_token("RBRACE", "}", 1, 15),
        ]
        parser_state = _make_parser_state(tokens)
        
        with patch("._parse_for_stmt_src._parse_expression") as mock_parse_expr, \
             patch("._parse_for_stmt_src._parse_block") as mock_parse_block:
            def parse_expr_side_effect(state):
                state["pos"] += 1
                return {"type": "EXPR", "value": "dummy"}
            
            mock_parse_expr.side_effect = parse_expr_side_effect
            mock_parse_block.return_value = {"type": "BLOCK", "children": []}
            
            result = _parse_for_stmt(parser_state)
            
            self.assertEqual(result["type"], "FOR")
            self.assertIsNotNone(result["initializer"])
            self.assertIsNone(result["condition"])
            self.assertIsNotNone(result["increment"])
            
            self.assertEqual(mock_parse_expr.call_count, 2)

    def test_empty_increment(self):
        """Test FOR statement with empty increment: for (init; cond; ) block"""
        tokens = [
            _make_token("FOR", "for", 1, 1),
            _make_token("LPAREN", "(", 1, 5),
            _make_token("IDENTIFIER", "i", 1, 6),
            _make_token("SEMICOLON", ";", 1, 7),
            _make_token("IDENTIFIER", "i", 1, 9),
            _make_token("SEMICOLON", ";", 1, 10),
            _make_token("RPAREN", ")", 1, 12),
            _make_token("LBRACE", "{", 1, 14),
            _make_token("RBRACE", "}", 1, 15),
        ]
        parser_state = _make_parser_state(tokens)
        
        with patch("._parse_for_stmt_src._parse_expression") as mock_parse_expr, \
             patch("._parse_for_stmt_src._parse_block") as mock_parse_block:
            def parse_expr_side_effect(state):
                state["pos"] += 1
                return {"type": "EXPR", "value": "dummy"}
            
            mock_parse_expr.side_effect = parse_expr_side_effect
            mock_parse_block.return_value = {"type": "BLOCK", "children": []}
            
            result = _parse_for_stmt(parser_state)
            
            self.assertEqual(result["type"], "FOR")
            self.assertIsNotNone(result["initializer"])
            self.assertIsNotNone(result["condition"])
            self.assertIsNone(result["increment"])
            
            self.assertEqual(mock_parse_expr.call_count, 2)

    def test_all_empty_expressions(self):
        """Test FOR statement with all empty expressions: for (; ; ) block"""
        tokens = [
            _make_token("FOR", "for", 1, 1),
            _make_token("LPAREN", "(", 1, 5),
            _make_token("SEMICOLON", ";", 1, 6),
            _make_token("SEMICOLON", ";", 1, 8),
            _make_token("RPAREN", ")", 1, 10),
            _make_token("LBRACE", "{", 1, 12),
            _make_token("RBRACE", "}", 1, 13),
        ]
        parser_state = _make_parser_state(tokens)
        
        with patch("._parse_for_stmt_src._parse_expression") as mock_parse_expr, \
             patch("._parse_for_stmt_src._parse_block") as mock_parse_block:
            mock_parse_block.return_value = {"type": "BLOCK", "children": []}
            
            result = _parse_for_stmt(parser_state)
            
            self.assertEqual(result["type"], "FOR")
            self.assertIsNone(result["initializer"])
            self.assertIsNone(result["condition"])
            self.assertIsNone(result["increment"])
            
            # _parse_expression should not be called
            self.assertEqual(mock_parse_expr.call_count, 0)

    def test_missing_lparen_raises_syntax_error(self):
        """Test that missing LPAREN raises SyntaxError."""
        tokens = [
            _make_token("FOR", "for", 1, 1),
            _make_token("IDENTIFIER", "i", 1, 5),  # Missing LPAREN
        ]
        parser_state = _make_parser_state(tokens)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_for_stmt(parser_state)
        
        self.assertIn("FOR 语句期望 LPAREN", str(context.exception))
        self.assertIn("1:5", str(context.exception))

    def test_missing_first_semicolon_raises_syntax_error(self):
        """Test that missing first SEMICOLON raises SyntaxError."""
        tokens = [
            _make_token("FOR", "for", 1, 1),
            _make_token("LPAREN", "(", 1, 5),
            _make_token("IDENTIFIER", "i", 1, 6),
            _make_token("RPAREN", ")", 1, 7),  # Missing SEMICOLON
        ]
        parser_state = _make_parser_state(tokens)
        
        with patch("._parse_for_stmt_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = {"type": "EXPR"}
            
            with self.assertRaises(SyntaxError) as context:
                _parse_for_stmt(parser_state)
            
            self.assertIn("FOR 语句期望 SEMICOLON", str(context.exception))

    def test_missing_second_semicolon_raises_syntax_error(self):
        """Test that missing second SEMICOLON raises SyntaxError."""
        tokens = [
            _make_token("FOR", "for", 1, 1),
            _make_token("LPAREN", "(", 1, 5),
            _make_token("SEMICOLON", ";", 1, 6),
            _make_token("IDENTIFIER", "i", 1, 8),
            _make_token("RPAREN", ")", 1, 9),  # Missing second SEMICOLON
        ]
        parser_state = _make_parser_state(tokens)
        
        with patch("._parse_for_stmt_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = {"type": "EXPR"}
            
            with self.assertRaises(SyntaxError) as context:
                _parse_for_stmt(parser_state)
            
            self.assertIn("FOR 语句期望 SEMICOLON", str(context.exception))

    def test_missing_rparen_raises_syntax_error(self):
        """Test that missing RPAREN raises SyntaxError."""
        tokens = [
            _make_token("FOR", "for", 1, 1),
            _make_token("LPAREN", "(", 1, 5),
            _make_token("SEMICOLON", ";", 1, 6),
            _make_token("SEMICOLON", ";", 1, 8),
            _make_token("IDENTIFIER", "i", 1, 10),  # Missing RPAREN
        ]
        parser_state = _make_parser_state(tokens)
        
        with patch("._parse_for_stmt_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = {"type": "EXPR"}
            
            with self.assertRaises(SyntaxError) as context:
                _parse_for_stmt(parser_state)
            
            self.assertIn("FOR 语句期望 RPAREN", str(context.exception))

    def test_eof_handling_in_current_token(self):
        """Test that _current_token returns EOF token when pos is out of bounds."""
        tokens = [
            _make_token("FOR", "for", 1, 1),
        ]
        parser_state = _make_parser_state(tokens)
        parser_state["pos"] = 100  # Out of bounds
        
        # Import the helper to test it directly
        from ._parse_for_stmt_src import _current_token
        result = _current_token(parser_state)
        
        self.assertEqual(result["type"], "EOF")
        self.assertEqual(result["line"], -1)
        self.assertEqual(result["column"], -1)

    def test_position_advancement(self):
        """Test that parser_state pos is correctly advanced through all tokens."""
        tokens = [
            _make_token("FOR", "for", 1, 1),
            _make_token("LPAREN", "(", 1, 5),
            _make_token("SEMICOLON", ";", 1, 6),
            _make_token("SEMICOLON", ";", 1, 8),
            _make_token("RPAREN", ")", 1, 10),
            _make_token("LBRACE", "{", 1, 12),
            _make_token("RBRACE", "}", 1, 13),
            _make_token("IDENTIFIER", "next", 1, 15),  # Token after FOR statement
        ]
        parser_state = _make_parser_state(tokens)
        
        with patch("._parse_for_stmt_src._parse_block") as mock_parse_block:
            # Mock _parse_block to consume LBRACE and RBRACE
            def parse_block_side_effect(state):
                state["pos"] += 2  # Consume LBRACE and RBRACE
                return {"type": "BLOCK", "children": []}
            
            mock_parse_block.side_effect = parse_block_side_effect
            
            result = _parse_for_stmt(parser_state)
            
            # pos should point to the token after RBRACE (index 7)
            self.assertEqual(parser_state["pos"], 7)

    def test_ast_position_from_for_token(self):
        """Test that AST line/column come from FOR token, not other tokens."""
        tokens = [
            _make_token("FOR", "for", 5, 10),  # Line 5, Column 10
            _make_token("LPAREN", "(", 5, 14),
            _make_token("SEMICOLON", ";", 5, 15),
            _make_token("SEMICOLON", ";", 5, 17),
            _make_token("RPAREN", ")", 5, 19),
            _make_token("LBRACE", "{", 5, 21),
            _make_token("RBRACE", "}", 5, 22),
        ]
        parser_state = _make_parser_state(tokens)
        
        with patch("._parse_for_stmt_src._parse_block") as mock_parse_block:
            mock_parse_block.return_value = {"type": "BLOCK", "children": []}
            
            result = _parse_for_stmt(parser_state)
            
            self.assertEqual(result["line"], 5)
            self.assertEqual(result["column"], 10)


if __name__ == "__main__":
    unittest.main()

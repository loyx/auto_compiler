# === std / third-party imports ===
import unittest
from unittest.mock import patch
from typing import Any, Dict

# === UUT import ===
from ._parse_for_stmt_src import _parse_for_stmt

# === Test Class ===
class TestParseForStmt(unittest.TestCase):
    """Test cases for _parse_for_stmt function."""
    
    def _create_token(self, token_type: str, value: str = "", line: int = 1, column: int = 1) -> Dict[str, Any]:
        """Helper to create a token dict."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }
    
    def _create_parser_state(self, tokens: list, filename: str = "test.c", pos: int = 0) -> Dict[str, Any]:
        """Helper to create a parser state dict."""
        return {
            "tokens": tokens,
            "filename": filename,
            "pos": pos,
            "error": ""
        }
    
    @patch("_parse_for_stmt_package._parse_for_stmt_src._parse_block")
    @patch("_parse_for_stmt_package._parse_for_stmt_src._parse_expression")
    @patch("_parse_for_stmt_package._parse_for_stmt_src._consume_token")
    def test_happy_path_full_for_stmt(self, mock_consume, mock_parse_expr, mock_parse_block):
        """Test parsing a complete for statement with all parts."""
        # Setup tokens
        tokens = [
            self._create_token("FOR", "for", 1, 1),
            self._create_token("LPAREN", "(", 1, 5),
            self._create_token("IDENT", "i", 1, 6),
            self._create_token("SEMICOLON", ";", 1, 7),
            self._create_token("IDENT", "i", 1, 9),
            self._create_token("LT", "<", 1, 11),
            self._create_token("NUMBER", "10", 1, 12),
            self._create_token("SEMICOLON", ";", 1, 14),
            self._create_token("IDENT", "i", 1, 16),
            self._create_token("PLUSPLUS", "++", 1, 17),
            self._create_token("RPAREN", ")", 1, 19),
            self._create_token("LBRACE", "{", 1, 21),
            self._create_token("RBRACE", "}", 1, 22),
        ]
        parser_state = self._create_parser_state(tokens)
        
        # Setup mocks
        mock_consume.side_effect = lambda state, expected: state.__setitem__("pos", state["pos"] + 1) or self._create_token(expected, "")
        mock_parse_expr.side_effect = [
            {"type": "EXPR", "value": "i = 0", "line": 1, "column": 6},
            {"type": "EXPR", "value": "i < 10", "line": 1, "column": 9},
            {"type": "EXPR", "value": "i++", "line": 1, "column": 16},
        ]
        mock_parse_block.return_value = {"type": "BLOCK", "statements": [], "line": 1, "column": 21}
        
        # Execute
        result = _parse_for_stmt(parser_state)
        
        # Verify
        self.assertEqual(result["type"], "FOR")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertIsNotNone(result["initializer"])
        self.assertIsNotNone(result["condition"])
        self.assertIsNotNone(result["increment"])
        self.assertIsNotNone(result["body"])
        self.assertEqual(mock_consume.call_count, 5)  # FOR, LPAREN, 2x SEMICOLON, RPAREN
        self.assertEqual(mock_parse_expr.call_count, 3)
        mock_parse_block.assert_called_once()
    
    @patch("_parse_for_stmt_package._parse_for_stmt_src._parse_block")
    @patch("_parse_for_stmt_package._parse_for_stmt_src._parse_expression")
    @patch("_parse_for_stmt_package._parse_for_stmt_src._consume_token")
    def test_empty_initializer(self, mock_consume, mock_parse_expr, mock_parse_block):
        """Test for statement with empty initializer."""
        tokens = [
            self._create_token("FOR", "for", 1, 1),
            self._create_token("LPAREN", "(", 1, 5),
            self._create_token("SEMICOLON", ";", 1, 6),
            self._create_token("IDENT", "i", 1, 8),
            self._create_token("LT", "<", 1, 10),
            self._create_token("NUMBER", "10", 1, 11),
            self._create_token("SEMICOLON", ";", 1, 13),
            self._create_token("IDENT", "i", 1, 15),
            self._create_token("PLUSPLUS", "++", 1, 16),
            self._create_token("RPAREN", ")", 1, 18),
            self._create_token("LBRACE", "{", 1, 20),
            self._create_token("RBRACE", "}", 1, 21),
        ]
        parser_state = self._create_parser_state(tokens)
        
        mock_consume.side_effect = lambda state, expected: state.__setitem__("pos", state["pos"] + 1) or self._create_token(expected, "")
        mock_parse_expr.side_effect = [
            {"type": "EXPR", "value": "i < 10", "line": 1, "column": 8},
            {"type": "EXPR", "value": "i++", "line": 1, "column": 15},
        ]
        mock_parse_block.return_value = {"type": "BLOCK", "statements": [], "line": 1, "column": 20}
        
        result = _parse_for_stmt(parser_state)
        
        self.assertEqual(result["type"], "FOR")
        self.assertIsNone(result["initializer"])
        self.assertIsNotNone(result["condition"])
        self.assertIsNotNone(result["increment"])
        self.assertEqual(mock_parse_expr.call_count, 2)
    
    @patch("_parse_for_stmt_package._parse_for_stmt_src._parse_block")
    @patch("_parse_for_stmt_package._parse_for_stmt_src._parse_expression")
    @patch("_parse_for_stmt_package._parse_for_stmt_src._consume_token")
    def test_empty_condition(self, mock_consume, mock_parse_expr, mock_parse_block):
        """Test for statement with empty condition."""
        tokens = [
            self._create_token("FOR", "for", 1, 1),
            self._create_token("LPAREN", "(", 1, 5),
            self._create_token("IDENT", "i", 1, 6),
            self._create_token("EQUAL", "=", 1, 8),
            self._create_token("NUMBER", "0", 1, 9),
            self._create_token("SEMICOLON", ";", 1, 10),
            self._create_token("SEMICOLON", ";", 1, 12),
            self._create_token("IDENT", "i", 1, 14),
            self._create_token("PLUSPLUS", "++", 1, 15),
            self._create_token("RPAREN", ")", 1, 17),
            self._create_token("LBRACE", "{", 1, 19),
            self._create_token("RBRACE", "}", 1, 20),
        ]
        parser_state = self._create_parser_state(tokens)
        
        mock_consume.side_effect = lambda state, expected: state.__setitem__("pos", state["pos"] + 1) or self._create_token(expected, "")
        mock_parse_expr.side_effect = [
            {"type": "EXPR", "value": "i = 0", "line": 1, "column": 6},
            {"type": "EXPR", "value": "i++", "line": 1, "column": 14},
        ]
        mock_parse_block.return_value = {"type": "BLOCK", "statements": [], "line": 1, "column": 19}
        
        result = _parse_for_stmt(parser_state)
        
        self.assertEqual(result["type"], "FOR")
        self.assertIsNotNone(result["initializer"])
        self.assertIsNone(result["condition"])
        self.assertIsNotNone(result["increment"])
        self.assertEqual(mock_parse_expr.call_count, 2)
    
    @patch("_parse_for_stmt_package._parse_for_stmt_src._parse_block")
    @patch("_parse_for_stmt_package._parse_for_stmt_src._parse_expression")
    @patch("_parse_for_stmt_package._parse_for_stmt_src._consume_token")
    def test_empty_increment(self, mock_consume, mock_parse_expr, mock_parse_block):
        """Test for statement with empty increment."""
        tokens = [
            self._create_token("FOR", "for", 1, 1),
            self._create_token("LPAREN", "(", 1, 5),
            self._create_token("IDENT", "i", 1, 6),
            self._create_token("EQUAL", "=", 1, 8),
            self._create_token("NUMBER", "0", 1, 9),
            self._create_token("SEMICOLON", ";", 1, 10),
            self._create_token("IDENT", "i", 1, 12),
            self._create_token("LT", "<", 1, 14),
            self._create_token("NUMBER", "10", 1, 15),
            self._create_token("SEMICOLON", ";", 1, 17),
            self._create_token("RPAREN", ")", 1, 19),
            self._create_token("LBRACE", "{", 1, 21),
            self._create_token("RBRACE", "}", 1, 22),
        ]
        parser_state = self._create_parser_state(tokens)
        
        mock_consume.side_effect = lambda state, expected: state.__setitem__("pos", state["pos"] + 1) or self._create_token(expected, "")
        mock_parse_expr.side_effect = [
            {"type": "EXPR", "value": "i = 0", "line": 1, "column": 6},
            {"type": "EXPR", "value": "i < 10", "line": 1, "column": 12},
        ]
        mock_parse_block.return_value = {"type": "BLOCK", "statements": [], "line": 1, "column": 21}
        
        result = _parse_for_stmt(parser_state)
        
        self.assertEqual(result["type"], "FOR")
        self.assertIsNotNone(result["initializer"])
        self.assertIsNotNone(result["condition"])
        self.assertIsNone(result["increment"])
        self.assertEqual(mock_parse_expr.call_count, 2)
    
    @patch("_parse_for_stmt_package._parse_for_stmt_src._parse_block")
    @patch("_parse_for_stmt_package._parse_for_stmt_src._parse_expression")
    @patch("_parse_for_stmt_package._parse_for_stmt_src._consume_token")
    def test_all_parts_empty(self, mock_consume, mock_parse_expr, mock_parse_block):
        """Test for statement with all parts empty (infinite loop)."""
        tokens = [
            self._create_token("FOR", "for", 1, 1),
            self._create_token("LPAREN", "(", 1, 5),
            self._create_token("SEMICOLON", ";", 1, 6),
            self._create_token("SEMICOLON", ";", 1, 7),
            self._create_token("RPAREN", ")", 1, 8),
            self._create_token("LBRACE", "{", 1, 10),
            self._create_token("RBRACE", "}", 1, 11),
        ]
        parser_state = self._create_parser_state(tokens)
        
        mock_consume.side_effect = lambda state, expected: state.__setitem__("pos", state["pos"] + 1) or self._create_token(expected, "")
        mock_parse_block.return_value = {"type": "BLOCK", "statements": [], "line": 1, "column": 10}
        
        result = _parse_for_stmt(parser_state)
        
        self.assertEqual(result["type"], "FOR")
        self.assertIsNone(result["initializer"])
        self.assertIsNone(result["condition"])
        self.assertIsNone(result["increment"])
        self.assertEqual(mock_parse_expr.call_count, 0)
        mock_parse_block.assert_called_once()
    
    @patch("_parse_for_stmt_package._parse_for_stmt_src._parse_block")
    @patch("_parse_for_stmt_package._parse_for_stmt_src._parse_expression")
    @patch("_parse_for_stmt_package._parse_for_stmt_src._consume_token")
    def test_unexpected_end_of_input_at_for(self, mock_consume, mock_parse_expr, mock_parse_block):
        """Test error when input ends at FOR token."""
        tokens = [
            self._create_token("FOR", "for", 5, 10),
        ]
        parser_state = self._create_parser_state(tokens, "test.c", 0)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_for_stmt(parser_state)
        
        self.assertIn("test.c:0:0", str(context.exception))
        self.assertIn("Unexpected end of input", str(context.exception))
    
    @patch("_parse_for_stmt_package._parse_for_stmt_src._parse_block")
    @patch("_parse_for_stmt_package._parse_for_stmt_src._parse_expression")
    @patch("_parse_for_stmt_package._parse_for_stmt_src._consume_token")
    def test_missing_lparen_raises_error(self, mock_consume, mock_parse_expr, mock_parse_block):
        """Test error when LPAREN is missing after FOR."""
        tokens = [
            self._create_token("FOR", "for", 1, 1),
            self._create_token("IDENT", "i", 1, 5),
        ]
        parser_state = self._create_parser_state(tokens)
        
        def consume_side_effect(state, expected_type):
            if expected_type == "FOR":
                state["pos"] += 1
                return tokens[0]
            else:
                raise SyntaxError(f"{state['filename']}:1:5: Expected {expected_type}, got {tokens[state['pos']]['type']}")
        
        mock_consume.side_effect = consume_side_effect
        
        with self.assertRaises(SyntaxError) as context:
            _parse_for_stmt(parser_state)
        
        self.assertIn("test.c:1:5", str(context.exception))
        self.assertIn("Expected LPAREN", str(context.exception))
    
    @patch("_parse_for_stmt_package._parse_for_stmt_src._parse_block")
    @patch("_parse_for_stmt_package._parse_for_stmt_src._parse_expression")
    @patch("_parse_for_stmt_package._parse_for_stmt_src._consume_token")
    def test_missing_semicolon_raises_error(self, mock_consume, mock_parse_expr, mock_parse_block):
        """Test error when first SEMICOLON is missing."""
        tokens = [
            self._create_token("FOR", "for", 1, 1),
            self._create_token("LPAREN", "(", 1, 5),
            self._create_token("IDENT", "i", 1, 6),
            self._create_token("RPAREN", ")", 1, 7),
        ]
        parser_state = self._create_parser_state(tokens)
        
        def consume_side_effect(state, expected_type):
            if expected_type in ["FOR", "LPAREN"]:
                state["pos"] += 1
                return self._create_token(expected_type, "")
            else:
                raise SyntaxError(f"{state['filename']}:1:7: Expected {expected_type}, got {tokens[state['pos']]['type']}")
        
        mock_consume.side_effect = consume_side_effect
        mock_parse_expr.return_value = {"type": "EXPR", "value": "i", "line": 1, "column": 6}
        
        with self.assertRaises(SyntaxError) as context:
            _parse_for_stmt(parser_state)
        
        self.assertIn("test.c:1:7", str(context.exception))
        self.assertIn("Expected SEMICOLON", str(context.exception))
    
    @patch("_parse_for_stmt_package._parse_for_stmt_src._parse_block")
    @patch("_parse_for_stmt_package._parse_for_stmt_src._parse_expression")
    @patch("_parse_for_stmt_package._parse_for_stmt_src._consume_token")
    def test_missing_rparen_raises_error(self, mock_consume, mock_parse_expr, mock_parse_block):
        """Test error when RPAREN is missing."""
        tokens = [
            self._create_token("FOR", "for", 1, 1),
            self._create_token("LPAREN", "(", 1, 5),
            self._create_token("SEMICOLON", ";", 1, 6),
            self._create_token("SEMICOLON", ";", 1, 7),
            self._create_token("LBRACE", "{", 1, 8),
        ]
        parser_state = self._create_parser_state(tokens)
        
        def consume_side_effect(state, expected_type):
            if expected_type in ["FOR", "LPAREN", "SEMICOLON", "SEMICOLON"]:
                state["pos"] += 1
                return self._create_token(expected_type, "")
            else:
                raise SyntaxError(f"{state['filename']}:1:8: Expected {expected_type}, got {tokens[state['pos']]['type']}")
        
        mock_consume.side_effect = consume_side_effect
        mock_parse_block.side_effect = SyntaxError("test.c:1:8: Expected RPAREN, got LBRACE")
        
        with self.assertRaises(SyntaxError):
            _parse_for_stmt(parser_state)
    
    @patch("_parse_for_stmt_package._parse_for_stmt_src._parse_block")
    @patch("_parse_for_stmt_package._parse_for_stmt_src._parse_expression")
    @patch("_parse_for_stmt_package._parse_for_stmt_src._consume_token")
    def test_parser_state_pos_updated(self, mock_consume, mock_parse_expr, mock_parse_block):
        """Test that parser_state pos is updated correctly."""
        tokens = [
            self._create_token("FOR", "for", 1, 1),
            self._create_token("LPAREN", "(", 1, 5),
            self._create_token("SEMICOLON", ";", 1, 6),
            self._create_token("SEMICOLON", ";", 1, 7),
            self._create_token("RPAREN", ")", 1, 8),
            self._create_token("LBRACE", "{", 1, 10),
            self._create_token("RBRACE", "}", 1, 11),
        ]
        parser_state = self._create_parser_state(tokens)
        initial_pos = parser_state["pos"]
        
        mock_consume.side_effect = lambda state, expected: state.__setitem__("pos", state["pos"] + 1) or self._create_token(expected, "")
        mock_parse_block.return_value = {"type": "BLOCK", "statements": [], "line": 1, "column": 10}
        
        _parse_for_stmt(parser_state)
        
        self.assertGreater(parser_state["pos"], initial_pos)
    
    @patch("_parse_for_stmt_package._parse_for_stmt_src._parse_block")
    @patch("_parse_for_stmt_package._parse_for_stmt_src._parse_expression")
    @patch("_parse_for_stmt_package._parse_for_stmt_src._consume_token")
    def test_ast_node_structure(self, mock_consume, mock_parse_expr, mock_parse_block):
        """Test that returned AST node has correct structure."""
        tokens = [
            self._create_token("FOR", "for", 3, 5),
            self._create_token("LPAREN", "(", 3, 9),
            self._create_token("SEMICOLON", ";", 3, 10),
            self._create_token("SEMICOLON", ";", 3, 11),
            self._create_token("RPAREN", ")", 3, 12),
            self._create_token("LBRACE", "{", 3, 14),
            self._create_token("RBRACE", "}", 3, 15),
        ]
        parser_state = self._create_parser_state(tokens)
        
        mock_consume.side_effect = lambda state, expected: state.__setitem__("pos", state["pos"] + 1) or self._create_token(expected, "")
        expected_body = {"type": "BLOCK", "statements": [], "line": 3, "column": 14}
        mock_parse_block.return_value = expected_body
        
        result = _parse_for_stmt(parser_state)
        
        self.assertIn("type", result)
        self.assertIn("initializer", result)
        self.assertIn("condition", result)
        self.assertIn("increment", result)
        self.assertIn("body", result)
        self.assertIn("line", result)
        self.assertIn("column", result)
        self.assertEqual(result["type"], "FOR")
        self.assertEqual(result["line"], 3)
        self.assertEqual(result["column"], 5)
        self.assertEqual(result["body"], expected_body)


# === Test Runner ===
if __name__ == "__main__":
    unittest.main()

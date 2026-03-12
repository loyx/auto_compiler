# === std / third-party imports ===
import unittest
from unittest.mock import patch
from typing import Dict, Any

# === UUT imports ===
from ._parse_for_stmt_src import _parse_for_stmt


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
    
    def _create_parser_state(self, tokens: list, pos: int = 0, filename: str = "test.py") -> Dict[str, Any]:
        """Helper to create a parser state dict."""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename,
            "error": ""
        }
    
    @patch('._parse_for_stmt_src._parse_expression')
    @patch('._parse_for_stmt_src._parse_block')
    def test_happy_path_valid_for_statement(self, mock_parse_block, mock_parse_expression):
        """Test parsing a valid for statement."""
        # Setup tokens for: FOR ( LET i EQUALS expr ) : block ;
        tokens = [
            self._create_token("FOR", "for", 1, 1),
            self._create_token("LPAREN", "(", 1, 5),
            self._create_token("LET", "let", 1, 7),
            self._create_token("IDENTIFIER", "i", 1, 11),
            self._create_token("EQUALS", "=", 1, 13),
            self._create_token("EXPR_START", "range", 1, 15),
            self._create_token("RPAREN", ")", 1, 25),
            self._create_token("COLON", ":", 1, 27),
            self._create_token("STATEMENT", "print", 2, 5),
            self._create_token("SEMICOLON", ";", 2, 15),
        ]
        
        parser_state = self._create_parser_state(tokens, 0)
        
        # Setup mocks
        mock_expression_ast = {"type": "EXPR", "value": "range(10)", "line": 1, "column": 15}
        mock_parse_expression.return_value = mock_expression_ast
        mock_parse_expression.side_effect = lambda state: state.update({"pos": 6}) or mock_expression_ast
        
        mock_block_ast = {"type": "BLOCK", "children": [], "line": 2, "column": 5}
        mock_parse_block.return_value = mock_block_ast
        mock_parse_block.side_effect = lambda state: state.update({"pos": 10}) or mock_block_ast
        
        # Execute
        result = _parse_for_stmt(parser_state)
        
        # Verify result structure
        self.assertEqual(result["type"], "FOR")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(len(result["children"]), 3)
        
        # Verify ITER_VAR child
        iter_var = result["children"][0]
        self.assertEqual(iter_var["type"], "ITER_VAR")
        self.assertEqual(iter_var["value"], "i")
        self.assertEqual(iter_var["line"], 1)
        self.assertEqual(iter_var["column"], 11)
        
        # Verify expression child
        self.assertEqual(result["children"][1], mock_expression_ast)
        
        # Verify block child
        self.assertEqual(result["children"][2], mock_block_ast)
        
        # Verify parser_state pos was updated
        self.assertEqual(parser_state["pos"], 10)
        
        # Verify mocks were called
        mock_parse_expression.assert_called_once()
        mock_parse_block.assert_called_once()
    
    @patch('._parse_for_stmt_src._parse_expression')
    @patch('._parse_for_stmt_src._parse_block')
    def test_happy_path_with_different_variable_name(self, mock_parse_block, mock_parse_expression):
        """Test parsing for statement with different iteration variable."""
        tokens = [
            self._create_token("FOR", "for", 2, 1),
            self._create_token("LPAREN", "(", 2, 5),
            self._create_token("LET", "let", 2, 7),
            self._create_token("IDENTIFIER", "item", 2, 11),
            self._create_token("EQUALS", "=", 2, 16),
            self._create_token("EXPR_START", "items", 2, 18),
            self._create_token("RPAREN", ")", 2, 25),
            self._create_token("COLON", ":", 2, 27),
            self._create_token("STATEMENT", "pass", 3, 5),
            self._create_token("SEMICOLON", ";", 3, 10),
        ]
        
        parser_state = self._create_parser_state(tokens, 0)
        
        mock_parse_expression.side_effect = lambda state: state.update({"pos": 6}) or {"type": "EXPR"}
        mock_parse_block.side_effect = lambda state: state.update({"pos": 10}) or {"type": "BLOCK"}
        
        result = _parse_for_stmt(parser_state)
        
        self.assertEqual(result["children"][0]["value"], "item")
        self.assertEqual(result["children"][0]["line"], 2)
        self.assertEqual(result["children"][0]["column"], 11)
    
    def test_error_missing_for_keyword(self):
        """Test error when FOR keyword is missing."""
        tokens = [
            self._create_token("IF", "if", 1, 1),
        ]
        
        parser_state = self._create_parser_state(tokens, 0)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_for_stmt(parser_state)
        
        self.assertIn("Expected FOR keyword", str(context.exception))
    
    def test_error_missing_for_keyword_at_eof(self):
        """Test error when FOR keyword is missing at EOF."""
        tokens = []
        parser_state = self._create_parser_state(tokens, 0)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_for_stmt(parser_state)
        
        self.assertIn("Expected FOR keyword", str(context.exception))
        self.assertIn("EOF", str(context.exception))
    
    def test_error_missing_lparen(self):
        """Test error when LPAREN is missing after FOR."""
        tokens = [
            self._create_token("FOR", "for", 1, 1),
            self._create_token("IF", "if", 1, 5),
        ]
        
        parser_state = self._create_parser_state(tokens, 0)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_for_stmt(parser_state)
        
        self.assertIn("Expected '('", str(context.exception))
    
    def test_error_missing_let_keyword(self):
        """Test error when LET keyword is missing."""
        tokens = [
            self._create_token("FOR", "for", 1, 1),
            self._create_token("LPAREN", "(", 1, 5),
            self._create_token("IDENTIFIER", "i", 1, 7),
        ]
        
        parser_state = self._create_parser_state(tokens, 0)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_for_stmt(parser_state)
        
        self.assertIn("Expected LET keyword", str(context.exception))
    
    def test_error_missing_identifier(self):
        """Test error when iteration variable identifier is missing."""
        tokens = [
            self._create_token("FOR", "for", 1, 1),
            self._create_token("LPAREN", "(", 1, 5),
            self._create_token("LET", "let", 1, 7),
            self._create_token("EQUALS", "=", 1, 11),
        ]
        
        parser_state = self._create_parser_state(tokens, 0)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_for_stmt(parser_state)
        
        self.assertIn("Expected iteration variable", str(context.exception))
    
    def test_error_missing_equals(self):
        """Test error when EQUALS is missing."""
        tokens = [
            self._create_token("FOR", "for", 1, 1),
            self._create_token("LPAREN", "(", 1, 5),
            self._create_token("LET", "let", 1, 7),
            self._create_token("IDENTIFIER", "i", 1, 11),
            self._create_token("RPAREN", ")", 1, 13),
        ]
        
        parser_state = self._create_parser_state(tokens, 0)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_for_stmt(parser_state)
        
        self.assertIn("Expected '='", str(context.exception))
    
    @patch('._parse_for_stmt_src._parse_expression')
    def test_error_missing_rparen(self, mock_parse_expression):
        """Test error when RPAREN is missing."""
        tokens = [
            self._create_token("FOR", "for", 1, 1),
            self._create_token("LPAREN", "(", 1, 5),
            self._create_token("LET", "let", 1, 7),
            self._create_token("IDENTIFIER", "i", 1, 11),
            self._create_token("EQUALS", "=", 1, 13),
            self._create_token("EXPR_START", "expr", 1, 15),
            self._create_token("COLON", ":", 1, 25),
        ]
        
        parser_state = self._create_parser_state(tokens, 0)
        mock_parse_expression.side_effect = lambda state: state.update({"pos": 6}) or {"type": "EXPR"}
        
        with self.assertRaises(SyntaxError) as context:
            _parse_for_stmt(parser_state)
        
        self.assertIn("Expected ')'", str(context.exception))
    
    @patch('._parse_for_stmt_src._parse_expression')
    def test_error_missing_colon(self, mock_parse_expression):
        """Test error when COLON is missing after RPAREN."""
        tokens = [
            self._create_token("FOR", "for", 1, 1),
            self._create_token("LPAREN", "(", 1, 5),
            self._create_token("LET", "let", 1, 7),
            self._create_token("IDENTIFIER", "i", 1, 11),
            self._create_token("EQUALS", "=", 1, 13),
            self._create_token("EXPR_START", "expr", 1, 15),
            self._create_token("RPAREN", ")", 1, 25),
            self._create_token("STATEMENT", "print", 2, 5),
        ]
        
        parser_state = self._create_parser_state(tokens, 0)
        mock_parse_expression.side_effect = lambda state: state.update({"pos": 6}) or {"type": "EXPR"}
        
        with self.assertRaises(SyntaxError) as context:
            _parse_for_stmt(parser_state)
        
        self.assertIn("Expected ':'", str(context.exception))
    
    @patch('._parse_for_stmt_src._parse_expression')
    @patch('._parse_for_stmt_src._parse_block')
    def test_position_updates_correctly(self, mock_parse_block, mock_parse_expression):
        """Test that parser_state position is updated correctly throughout parsing."""
        tokens = [
            self._create_token("FOR", "for", 1, 1),
            self._create_token("LPAREN", "(", 1, 5),
            self._create_token("LET", "let", 1, 7),
            self._create_token("IDENTIFIER", "i", 1, 11),
            self._create_token("EQUALS", "=", 1, 13),
            self._create_token("EXPR_START", "expr", 1, 15),
            self._create_token("RPAREN", ")", 1, 25),
            self._create_token("COLON", ":", 1, 27),
            self._create_token("STATEMENT", "print", 2, 5),
            self._create_token("SEMICOLON", ";", 2, 15),
        ]
        
        parser_state = self._create_parser_state(tokens, 0)
        
        # Track position updates
        def track_expression_pos(state):
            state["pos"] = 6
            return {"type": "EXPR"}
        
        def track_block_pos(state):
            state["pos"] = 10
            return {"type": "BLOCK"}
        
        mock_parse_expression.side_effect = track_expression_pos
        mock_parse_block.side_effect = track_block_pos
        
        result = _parse_for_stmt(parser_state)
        
        # Final position should be after SEMICOLON
        self.assertEqual(parser_state["pos"], 10)
    
    @patch('._parse_for_stmt_src._parse_expression')
    @patch('._parse_for_stmt_src._parse_block')
    def test_ast_node_preserves_line_column_info(self, mock_parse_block, mock_parse_expression):
        """Test that AST node preserves line and column information from tokens."""
        tokens = [
            self._create_token("FOR", "for", 5, 10),
            self._create_token("LPAREN", "(", 5, 14),
            self._create_token("LET", "let", 5, 16),
            self._create_token("IDENTIFIER", "idx", 5, 20),
            self._create_token("EQUALS", "=", 5, 24),
            self._create_token("EXPR_START", "expr", 5, 26),
            self._create_token("RPAREN", ")", 5, 35),
            self._create_token("COLON", ":", 5, 37),
            self._create_token("STATEMENT", "stmt", 6, 5),
            self._create_token("SEMICOLON", ";", 6, 15),
        ]
        
        parser_state = self._create_parser_state(tokens, 0)
        mock_parse_expression.side_effect = lambda state: state.update({"pos": 6}) or {"type": "EXPR"}
        mock_parse_block.side_effect = lambda state: state.update({"pos": 10}) or {"type": "BLOCK"}
        
        result = _parse_for_stmt(parser_state)
        
        # FOR node should have line/column from FOR token
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 10)
        
        # ITER_VAR should have line/column from IDENTIFIER token
        iter_var = result["children"][0]
        self.assertEqual(iter_var["line"], 5)
        self.assertEqual(iter_var["column"], 20)
    
    @patch('._parse_for_stmt_src._parse_expression')
    @patch('._parse_for_stmt_src._parse_block')
    def test_expression_and_block_delegation(self, mock_parse_block, mock_parse_expression):
        """Test that _parse_expression and _parse_block are called with correct parser_state."""
        tokens = [
            self._create_token("FOR", "for", 1, 1),
            self._create_token("LPAREN", "(", 1, 5),
            self._create_token("LET", "let", 1, 7),
            self._create_token("IDENTIFIER", "i", 1, 11),
            self._create_token("EQUALS", "=", 1, 13),
            self._create_token("EXPR_START", "expr", 1, 15),
            self._create_token("RPAREN", ")", 1, 25),
            self._create_token("COLON", ":", 1, 27),
            self._create_token("STATEMENT", "stmt", 2, 5),
            self._create_token("SEMICOLON", ";", 2, 15),
        ]
        
        parser_state = self._create_parser_state(tokens, 0)
        mock_parse_expression.side_effect = lambda state: state.update({"pos": 6}) or {"type": "EXPR"}
        mock_parse_block.side_effect = lambda state: state.update({"pos": 10}) or {"type": "BLOCK"}
        
        _parse_for_stmt(parser_state)
        
        # Verify both functions were called
        self.assertEqual(mock_parse_expression.call_count, 1)
        self.assertEqual(mock_parse_block.call_count, 1)
        
        # Verify _parse_expression was called when pos was at expression (after EQUALS)
        expr_call_args = mock_parse_expression.call_args[0][0]
        self.assertEqual(expr_call_args["pos"], 6)
        
        # Verify _parse_block was called when pos was at COLON
        block_call_args = mock_parse_block.call_args[0][0]
        self.assertEqual(block_call_args["pos"], 8)
    
    @patch('._parse_for_stmt_src._parse_expression')
    @patch('._parse_for_stmt_src._parse_block')
    def test_for_statement_in_middle_of_tokens(self, mock_parse_block, mock_parse_expression):
        """Test parsing for statement when pos starts in the middle of token list."""
        tokens = [
            self._create_token("STATEMENT", "x = 1", 1, 1),
            self._create_token("SEMICOLON", ";", 1, 10),
            self._create_token("FOR", "for", 2, 1),
            self._create_token("LPAREN", "(", 2, 5),
            self._create_token("LET", "let", 2, 7),
            self._create_token("IDENTIFIER", "i", 2, 11),
            self._create_token("EQUALS", "=", 2, 13),
            self._create_token("EXPR_START", "expr", 2, 15),
            self._create_token("RPAREN", ")", 2, 25),
            self._create_token("COLON", ":", 2, 27),
            self._create_token("STATEMENT", "print", 3, 5),
            self._create_token("SEMICOLON", ";", 3, 15),
        ]
        
        # Start parsing at position 2 (FOR token)
        parser_state = self._create_parser_state(tokens, 2)
        mock_parse_expression.side_effect = lambda state: state.update({"pos": 8}) or {"type": "EXPR"}
        mock_parse_block.side_effect = lambda state: state.update({"pos": 12}) or {"type": "BLOCK"}
        
        result = _parse_for_stmt(parser_state)
        
        self.assertEqual(result["type"], "FOR")
        self.assertEqual(parser_state["pos"], 12)
    
    @patch('._parse_for_stmt_src._parse_expression')
    @patch('._parse_for_stmt_src._parse_block')
    def test_empty_block_handling(self, mock_parse_block, mock_parse_expression):
        """Test for statement with empty block."""
        tokens = [
            self._create_token("FOR", "for", 1, 1),
            self._create_token("LPAREN", "(", 1, 5),
            self._create_token("LET", "let", 1, 7),
            self._create_token("IDENTIFIER", "i", 1, 11),
            self._create_token("EQUALS", "=", 1, 13),
            self._create_token("EXPR_START", "expr", 1, 15),
            self._create_token("RPAREN", ")", 1, 25),
            self._create_token("COLON", ":", 1, 27),
            self._create_token("SEMICOLON", ";", 1, 28),
        ]
        
        parser_state = self._create_parser_state(tokens, 0)
        mock_parse_expression.side_effect = lambda state: state.update({"pos": 6}) or {"type": "EXPR"}
        mock_parse_block.side_effect = lambda state: state.update({"pos": 9}) or {"type": "BLOCK", "children": []}
        
        result = _parse_for_stmt(parser_state)
        
        self.assertEqual(result["type"], "FOR")
        self.assertEqual(len(result["children"]), 3)


if __name__ == "__main__":
    unittest.main()

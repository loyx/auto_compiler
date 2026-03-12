import unittest
from unittest.mock import patch
from typing import Dict, Any
import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from _parse_statement_src import _parse_statement


class TestParseStatement(unittest.TestCase):
    """Test cases for _parse_statement function."""
    
    def _create_parser_state(self, tokens: list, pos: int = 0) -> Dict[str, Any]:
        """Helper to create parser_state dict."""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": "test.cc",
            "error": None
        }
    
    def _create_token(self, token_type: str, value: str = "", line: int = 1, column: int = 1) -> Dict[str, Any]:
        """Helper to create a token dict."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }
    
    def test_empty_input_raises_syntax_error(self):
        """Test that empty token list raises SyntaxError."""
        parser_state = self._create_parser_state(tokens=[], pos=0)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_statement(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))
    
    def test_pos_beyond_tokens_raises_syntax_error(self):
        """Test that pos >= len(tokens) raises SyntaxError."""
        tokens = [self._create_token("IDENTIFIER", "x")]
        parser_state = self._create_parser_state(tokens=tokens, pos=1)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_statement(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))
    
    @patch('_parse_statement_src._parse_var_decl')
    def test_let_token_routes_to_var_decl(self, mock_var_decl):
        """Test LET token routes to _parse_var_decl."""
        mock_var_decl.return_value = {"type": "VAR_DECL", "value": "let x = 5"}
        
        tokens = [self._create_token("LET", "let")]
        parser_state = self._create_parser_state(tokens=tokens, pos=0)
        
        result = _parse_statement(parser_state)
        
        mock_var_decl.assert_called_once_with(parser_state)
        self.assertEqual(result, {"type": "VAR_DECL", "value": "let x = 5"})
    
    @patch('_parse_statement_src._parse_var_decl')
    def test_var_token_routes_to_var_decl(self, mock_var_decl):
        """Test VAR token routes to _parse_var_decl."""
        mock_var_decl.return_value = {"type": "VAR_DECL", "value": "var y = 10"}
        
        tokens = [self._create_token("VAR", "var")]
        parser_state = self._create_parser_state(tokens=tokens, pos=0)
        
        result = _parse_statement(parser_state)
        
        mock_var_decl.assert_called_once_with(parser_state)
        self.assertEqual(result, {"type": "VAR_DECL", "value": "var y = 10"})
    
    @patch('_parse_statement_src._parse_if_stmt')
    def test_if_token_routes_to_if_stmt(self, mock_if_stmt):
        """Test IF token routes to _parse_if_stmt."""
        mock_if_stmt.return_value = {"type": "IF_STMT"}
        
        tokens = [self._create_token("IF", "if")]
        parser_state = self._create_parser_state(tokens=tokens, pos=0)
        
        result = _parse_statement(parser_state)
        
        mock_if_stmt.assert_called_once_with(parser_state)
        self.assertEqual(result, {"type": "IF_STMT"})
    
    @patch('_parse_statement_src._parse_while_stmt')
    def test_while_token_routes_to_while_stmt(self, mock_while_stmt):
        """Test WHILE token routes to _parse_while_stmt."""
        mock_while_stmt.return_value = {"type": "WHILE_STMT"}
        
        tokens = [self._create_token("WHILE", "while")]
        parser_state = self._create_parser_state(tokens=tokens, pos=0)
        
        result = _parse_statement(parser_state)
        
        mock_while_stmt.assert_called_once_with(parser_state)
        self.assertEqual(result, {"type": "WHILE_STMT"})
    
    @patch('_parse_statement_src._parse_for_stmt')
    def test_for_token_routes_to_for_stmt(self, mock_for_stmt):
        """Test FOR token routes to _parse_for_stmt."""
        mock_for_stmt.return_value = {"type": "FOR_STMT"}
        
        tokens = [self._create_token("FOR", "for")]
        parser_state = self._create_parser_state(tokens=tokens, pos=0)
        
        result = _parse_statement(parser_state)
        
        mock_for_stmt.assert_called_once_with(parser_state)
        self.assertEqual(result, {"type": "FOR_STMT"})
    
    @patch('_parse_statement_src._parse_return_stmt')
    def test_return_token_routes_to_return_stmt(self, mock_return_stmt):
        """Test RETURN token routes to _parse_return_stmt."""
        mock_return_stmt.return_value = {"type": "RETURN_STMT"}
        
        tokens = [self._create_token("RETURN", "return")]
        parser_state = self._create_parser_state(tokens=tokens, pos=0)
        
        result = _parse_statement(parser_state)
        
        mock_return_stmt.assert_called_once_with(parser_state)
        self.assertEqual(result, {"type": "RETURN_STMT"})
    
    @patch('_parse_statement_src._parse_break_stmt')
    def test_break_token_routes_to_break_stmt(self, mock_break_stmt):
        """Test BREAK token routes to _parse_break_stmt."""
        mock_break_stmt.return_value = {"type": "BREAK_STMT"}
        
        tokens = [self._create_token("BREAK", "break")]
        parser_state = self._create_parser_state(tokens=tokens, pos=0)
        
        result = _parse_statement(parser_state)
        
        mock_break_stmt.assert_called_once_with(parser_state)
        self.assertEqual(result, {"type": "BREAK_STMT"})
    
    @patch('_parse_statement_src._parse_continue_stmt')
    def test_continue_token_routes_to_continue_stmt(self, mock_continue_stmt):
        """Test CONTINUE token routes to _parse_continue_stmt."""
        mock_continue_stmt.return_value = {"type": "CONTINUE_STMT"}
        
        tokens = [self._create_token("CONTINUE", "continue")]
        parser_state = self._create_parser_state(tokens=tokens, pos=0)
        
        result = _parse_statement(parser_state)
        
        mock_continue_stmt.assert_called_once_with(parser_state)
        self.assertEqual(result, {"type": "CONTINUE_STMT"})
    
    @patch('_parse_statement_src._parse_expr_stmt')
    def test_identifier_token_routes_to_expr_stmt(self, mock_expr_stmt):
        """Test IDENTIFIER token (default) routes to _parse_expr_stmt."""
        mock_expr_stmt.return_value = {"type": "EXPR_STMT"}
        
        tokens = [self._create_token("IDENTIFIER", "x")]
        parser_state = self._create_parser_state(tokens=tokens, pos=0)
        
        result = _parse_statement(parser_state)
        
        mock_expr_stmt.assert_called_once_with(parser_state)
        self.assertEqual(result, {"type": "EXPR_STMT"})
    
    @patch('_parse_statement_src._parse_expr_stmt')
    def test_unknown_token_type_routes_to_expr_stmt(self, mock_expr_stmt):
        """Test unknown token type routes to _parse_expr_stmt as default."""
        mock_expr_stmt.return_value = {"type": "EXPR_STMT"}
        
        tokens = [self._create_token("UNKNOWN", "unknown")]
        parser_state = self._create_parser_state(tokens=tokens, pos=0)
        
        result = _parse_statement(parser_state)
        
        mock_expr_stmt.assert_called_once_with(parser_state)
        self.assertEqual(result, {"type": "EXPR_STMT"})
    
    @patch('_parse_statement_src._parse_expr_stmt')
    def test_number_token_routes_to_expr_stmt(self, mock_expr_stmt):
        """Test NUMBER token (default) routes to _parse_expr_stmt."""
        mock_expr_stmt.return_value = {"type": "EXPR_STMT"}
        
        tokens = [self._create_token("NUMBER", "42")]
        parser_state = self._create_parser_state(tokens=tokens, pos=0)
        
        result = _parse_statement(parser_state)
        
        mock_expr_stmt.assert_called_once_with(parser_state)
        self.assertEqual(result, {"type": "EXPR_STMT"})
    
    @patch('_parse_statement_src._parse_var_decl')
    def test_var_decl_propagates_exception(self, mock_var_decl):
        """Test that exceptions from child parsers are propagated."""
        mock_var_decl.side_effect = SyntaxError("Invalid variable declaration")
        
        tokens = [self._create_token("LET", "let")]
        parser_state = self._create_parser_state(tokens=tokens, pos=0)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_statement(parser_state)
        
        self.assertEqual(str(context.exception), "Invalid variable declaration")
    
    @patch('_parse_statement_src._parse_if_stmt')
    def test_if_stmt_propagates_exception(self, mock_if_stmt):
        """Test that exceptions from _parse_if_stmt are propagated."""
        mock_if_stmt.side_effect = SyntaxError("Invalid if statement")
        
        tokens = [self._create_token("IF", "if")]
        parser_state = self._create_parser_state(tokens=tokens, pos=0)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_statement(parser_state)
        
        self.assertEqual(str(context.exception), "Invalid if statement")


if __name__ == '__main__':
    unittest.main()

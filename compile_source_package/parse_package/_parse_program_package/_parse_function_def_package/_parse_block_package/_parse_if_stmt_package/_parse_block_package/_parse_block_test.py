#!/usr/bin/env python3
"""Unit tests for _parse_block function."""

import unittest
from unittest.mock import patch, MagicMock
from typing import Dict, Any

# Import the function under test using relative import
from ._parse_block_src import _parse_block


class TestParseBlock(unittest.TestCase):
    """Test cases for _parse_block function."""
    
    def _create_token(self, token_type: str, value: str, line: int, column: int) -> Dict[str, Any]:
        """Helper to create a token dict."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }
    
    def _create_parser_state(self, tokens: list, pos: int = 0) -> Dict[str, Any]:
        """Helper to create a parser state dict."""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": "test.c"
        }
    
    def test_explicit_block_multiple_statements(self):
        """Test explicit block with LBRACE/RBRACE containing multiple statements."""
        tokens = [
            self._create_token("LBRACE", "{", 1, 1),
            self._create_token("IDENTIFIER", "stmt1", 2, 5),
            self._create_token("IDENTIFIER", "stmt2", 3, 5),
            self._create_token("RBRACE", "}", 4, 1),
        ]
        parser_state = self._create_parser_state(tokens)
        
        mock_ast1 = {"type": "VAR_DECL", "children": [], "line": 2, "column": 5}
        mock_ast2 = {"type": "EXPR_STMT", "children": [], "line": 3, "column": 5}
        
        mock_parse_stmt = MagicMock()
        mock_parse_stmt.side_effect = [mock_ast1, mock_ast2]
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_block_src._get_parse_statement", return_value=mock_parse_stmt):
            
            result = _parse_block(parser_state)
            
            self.assertEqual(result["type"], "BLOCK")
            self.assertEqual(len(result["children"]), 2)
            self.assertEqual(result["children"][0]["type"], "VAR_DECL")
            self.assertEqual(result["children"][1]["type"], "EXPR_STMT")
            self.assertEqual(parser_state["pos"], 4)
            self.assertEqual(mock_parse_stmt.call_count, 2)
    
    def test_explicit_block_single_statement(self):
        """Test explicit block with single statement."""
        tokens = [
            self._create_token("LBRACE", "{", 1, 1),
            self._create_token("IDENTIFIER", "x", 2, 5),
            self._create_token("RBRACE", "}", 3, 1),
        ]
        parser_state = self._create_parser_state(tokens)
        
        mock_ast = {"type": "VAR_DECL", "children": [], "line": 2, "column": 5}
        
        mock_parse_stmt = MagicMock()
        mock_parse_stmt.return_value = mock_ast
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_block_src._get_parse_statement", return_value=mock_parse_stmt):
            
            result = _parse_block(parser_state)
            
            self.assertEqual(result["type"], "BLOCK")
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(result["children"][0]["type"], "VAR_DECL")
            self.assertEqual(parser_state["pos"], 3)
    
    def test_explicit_block_empty(self):
        """Test empty explicit block (LBRACE immediately followed by RBRACE)."""
        tokens = [
            self._create_token("LBRACE", "{", 1, 1),
            self._create_token("RBRACE", "}", 1, 2),
        ]
        parser_state = self._create_parser_state(tokens)
        
        result = _parse_block(parser_state)
        
        self.assertEqual(result["type"], "BLOCK")
        self.assertEqual(len(result["children"]), 0)
        self.assertEqual(parser_state["pos"], 2)
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
    
    def test_implicit_block_single_statement(self):
        """Test implicit block (single statement without braces)."""
        tokens = [
            self._create_token("IDENTIFIER", "x", 1, 5),
            self._create_token("SEMICOLON", ";", 1, 6),
        ]
        parser_state = self._create_parser_state(tokens)
        
        mock_ast = {"type": "VAR_DECL", "children": [], "line": 1, "column": 5}
        
        mock_parse_stmt = MagicMock()
        mock_parse_stmt.return_value = mock_ast
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_block_src._get_parse_statement", return_value=mock_parse_stmt):
            
            result = _parse_block(parser_state)
            
            self.assertEqual(result["type"], "BLOCK")
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(result["children"][0]["type"], "VAR_DECL")
            self.assertEqual(parser_state["pos"], 1)
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 5)
    
    def test_missing_closing_brace(self):
        """Test that missing RBRACE raises SyntaxError."""
        tokens = [
            self._create_token("LBRACE", "{", 1, 1),
            self._create_token("IDENTIFIER", "stmt", 2, 5),
        ]
        parser_state = self._create_parser_state(tokens)
        
        mock_ast = {"type": "VAR_DECL", "children": [], "line": 2, "column": 5}
        
        mock_parse_stmt = MagicMock()
        mock_parse_stmt.return_value = mock_ast
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_block_src._get_parse_statement", return_value=mock_parse_stmt):
            
            with self.assertRaises(SyntaxError) as context:
                _parse_block(parser_state)
            
            self.assertIn("Missing closing brace", str(context.exception))
    
    def test_unexpected_end_of_input(self):
        """Test that unexpected end of input raises SyntaxError."""
        tokens = []
        parser_state = self._create_parser_state(tokens, pos=0)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_block(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))
    
    def test_position_at_end_of_tokens(self):
        """Test that position at or beyond token length raises SyntaxError."""
        tokens = [
            self._create_token("IDENTIFIER", "x", 1, 1),
        ]
        parser_state = self._create_parser_state(tokens, pos=1)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_block(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))
    
    def test_block_node_preserves_position_info(self):
        """Test that BLOCK node preserves line and column from start token."""
        tokens = [
            self._create_token("LBRACE", "{", 10, 25),
            self._create_token("RBRACE", "}", 12, 30),
        ]
        parser_state = self._create_parser_state(tokens)
        
        result = _parse_block(parser_state)
        
        self.assertEqual(result["line"], 10)
        self.assertEqual(result["column"], 25)
        self.assertEqual(result["type"], "BLOCK")
    
    def test_multiple_statements_consume_all_tokens(self):
        """Test that all statements in block are parsed and tokens consumed."""
        tokens = [
            self._create_token("LBRACE", "{", 1, 1),
            self._create_token("IDENTIFIER", "stmt1", 2, 5),
            self._create_token("IDENTIFIER", "stmt2", 3, 5),
            self._create_token("IDENTIFIER", "stmt3", 4, 5),
            self._create_token("RBRACE", "}", 5, 1),
        ]
        parser_state = self._create_parser_state(tokens)
        
        mock_asts = [
            {"type": "VAR_DECL", "children": [], "line": 2, "column": 5},
            {"type": "IF_STMT", "children": [], "line": 3, "column": 5},
            {"type": "RETURN_STMT", "children": [], "line": 4, "column": 5},
        ]
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_statement_src._parse_statement") as mock_parse_stmt:
            mock_parse_stmt.side_effect = mock_asts
            
            result = _parse_block(parser_state)
            
            self.assertEqual(len(result["children"]), 3)
            self.assertEqual(result["children"][0]["type"], "VAR_DECL")
            self.assertEqual(result["children"][1]["type"], "IF_STMT")
            self.assertEqual(result["children"][2]["type"], "RETURN_STMT")
            self.assertEqual(parser_state["pos"], 5)


if __name__ == "__main__":
    unittest.main()

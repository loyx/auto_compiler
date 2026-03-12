import unittest
from unittest.mock import patch
from typing import Dict, Any

from ._parse_expr_stmt_src import _parse_expr_stmt


class TestParseExprStmt(unittest.TestCase):
    """Test cases for _parse_expr_stmt function."""
    
    def _create_parser_state(self, tokens: list, pos: int = 0) -> Dict[str, Any]:
        """Helper to create parser state."""
        return {
            "tokens": tokens,
            "filename": "test.py",
            "pos": pos,
            "error": None
        }
    
    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_def_statement_package._parse_block_package._parse_expr_stmt_package._parse_expression_package._parse_expression_src._parse_expression')
    def test_happy_path_simple_expression(self, mock_parse_expr):
        """Test parsing a simple expression statement with SEMICOLON."""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 0},
            {"type": "SEMICOLON", "value": ";", "line": 1, "column": 1}
        ]
        parser_state = self._create_parser_state(tokens)
        
        mock_expr_ast = {
            "type": "IDENTIFIER",
            "line": 1,
            "column": 0,
            "children": []
        }
        
        def parse_expr_side_effect(state):
            state["pos"] = 1
            return mock_expr_ast
        
        mock_parse_expr.side_effect = parse_expr_side_effect
        
        result = _parse_expr_stmt(parser_state)
        
        self.assertEqual(result["type"], "EXPR")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 0)
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0], mock_expr_ast)
        self.assertEqual(parser_state["pos"], 2)
        mock_parse_expr.assert_called_once()
    
    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_def_statement_package._parse_block_package._parse_expr_stmt_package._parse_expression_package._parse_expression_src._parse_expression')
    def test_missing_semicolon(self, mock_parse_expr):
        """Test that missing SEMICOLON raises SyntaxError."""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 0}
        ]
        parser_state = self._create_parser_state(tokens)
        
        mock_expr_ast = {
            "type": "IDENTIFIER",
            "line": 1,
            "column": 0,
            "children": []
        }
        
        def parse_expr_side_effect(state):
            state["pos"] = 1
            return mock_expr_ast
        
        mock_parse_expr.side_effect = parse_expr_side_effect
        
        with self.assertRaises(SyntaxError) as context:
            _parse_expr_stmt(parser_state)
        
        self.assertIn("Expected ';'", str(context.exception))
    
    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_def_statement_package._parse_block_package._parse_expr_stmt_package._parse_expression_package._parse_expression_src._parse_expression')
    def test_wrong_token_instead_of_semicolon(self, mock_parse_expr):
        """Test that wrong token instead of SEMICOLON raises SyntaxError."""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 0},
            {"type": "IDENTIFIER", "value": "y", "line": 1, "column": 2}
        ]
        parser_state = self._create_parser_state(tokens)
        
        mock_expr_ast = {
            "type": "IDENTIFIER",
            "line": 1,
            "column": 0,
            "children": []
        }
        
        def parse_expr_side_effect(state):
            state["pos"] = 1
            return mock_expr_ast
        
        mock_parse_expr.side_effect = parse_expr_side_effect
        
        with self.assertRaises(SyntaxError) as context:
            _parse_expr_stmt(parser_state)
        
        self.assertIn("Expected ';' but got 'y'", str(context.exception))
    
    def test_empty_tokens(self):
        """Test that empty tokens list raises SyntaxError."""
        tokens = []
        parser_state = self._create_parser_state(tokens)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_expr_stmt(parser_state)
        
        self.assertIn("Unexpected end of input, expected expression", str(context.exception))
    
    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_def_statement_package._parse_block_package._parse_expr_stmt_package._parse_expression_package._parse_expression_src._parse_expression')
    def test_expression_at_end_without_semicolon(self, mock_parse_expr):
        """Test expression at end of input without SEMICOLON."""
        tokens = [
            {"type": "NUMBER", "value": "42", "line": 1, "column": 0}
        ]
        parser_state = self._create_parser_state(tokens)
        
        mock_expr_ast = {
            "type": "NUMBER",
            "line": 1,
            "column": 0,
            "value": "42"
        }
        
        def parse_expr_side_effect(state):
            state["pos"] = 1
            return mock_expr_ast
        
        mock_parse_expr.side_effect = parse_expr_side_effect
        
        with self.assertRaises(SyntaxError) as context:
            _parse_expr_stmt(parser_state)
        
        self.assertIn("Unexpected end of input, expected ';'", str(context.exception))
    
    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_def_statement_package._parse_block_package._parse_expr_stmt_package._parse_expression_package._parse_expression_src._parse_expression')
    def test_complex_expression(self, mock_parse_expr):
        """Test parsing a complex expression statement."""
        tokens = [
            {"type": "NUMBER", "value": "1", "line": 2, "column": 4},
            {"type": "PLUS", "value": "+", "line": 2, "column": 6},
            {"type": "NUMBER", "value": "2", "line": 2, "column": 8},
            {"type": "SEMICOLON", "value": ";", "line": 2, "column": 9}
        ]
        parser_state = self._create_parser_state(tokens)
        
        mock_expr_ast = {
            "type": "BINARY_OP",
            "line": 2,
            "column": 4,
            "children": [
                {"type": "NUMBER", "value": "1"},
                {"type": "NUMBER", "value": "2"}
            ]
        }
        
        def parse_expr_side_effect(state):
            state["pos"] = 3
            return mock_expr_ast
        
        mock_parse_expr.side_effect = parse_expr_side_effect
        
        result = _parse_expr_stmt(parser_state)
        
        self.assertEqual(result["type"], "EXPR")
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 4)
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0], mock_expr_ast)
        self.assertEqual(parser_state["pos"], 4)


if __name__ == '__main__':
    unittest.main()

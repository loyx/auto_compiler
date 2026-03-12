#!/usr/bin/env python3
"""Unit tests for _parse_block function."""

import unittest
from unittest.mock import patch, MagicMock

# Import the function under test using relative import
from ._parse_block_src import _parse_block


class TestParseBlock(unittest.TestCase):
    """Test cases for _parse_block function."""
    
    def test_brace_enclosed_block_with_multiple_statements(self):
        """Test parsing a brace-enclosed block with multiple statements."""
        mock_state = {
            "tokens": [
                {"type": "LBRACE", "value": "{", "line": 1, "column": 1},
                {"type": "VAR", "value": "int", "line": 2, "column": 5},
                {"type": "IF", "value": "if", "line": 3, "column": 5},
                {"type": "RBRACE", "value": "}", "line": 4, "column": 1}
            ],
            "pos": 0,
            "filename": "test.c",
            "error": ""
        }
        
        mock_var_decl = MagicMock(return_value={
            "type": "VAR_DECL",
            "children": [],
            "line": 2,
            "column": 5
        })
        
        mock_if_stmt = MagicMock(return_value={
            "type": "IF_STMT",
            "children": [],
            "line": 3,
            "column": 5
        })
        
        module_path = "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_block_src"
        
        with patch(f"{module_path}._parse_var_decl", mock_var_decl):
            with patch(f"{module_path}._parse_if_stmt", mock_if_stmt):
                with patch(f"{module_path}._peek_token") as mock_peek:
                    with patch(f"{module_path}._consume_token") as mock_consume:
                        mock_peek.side_effect = [
                            {"type": "LBRACE", "value": "{", "line": 1, "column": 1},
                            {"type": "VAR", "value": "int", "line": 2, "column": 5},
                            {"type": "IF", "value": "if", "line": 3, "column": 5},
                            {"type": "RBRACE", "value": "}", "line": 4, "column": 1},
                            {"type": "RBRACE", "value": "}", "line": 4, "column": 1}
                        ]
                        
                        mock_consume.side_effect = [mock_state, mock_state]
                        
                        result = _parse_block(mock_state)
                        
                        self.assertEqual(result["type"], "BLOCK")
                        self.assertEqual(len(result["children"]), 2)
                        self.assertEqual(result["line"], 1)
                        self.assertEqual(result["column"], 1)
                        
                        mock_var_decl.assert_called_once()
                        mock_if_stmt.assert_called_once()
                        self.assertEqual(mock_consume.call_count, 2)
    
    def test_single_statement_block_without_braces(self):
        """Test parsing a single statement without braces."""
        mock_state = {
            "tokens": [{"type": "VAR", "value": "x", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test.c",
            "error": ""
        }
        
        mock_var_decl = MagicMock(return_value={
            "type": "VAR_DECL",
            "children": [],
            "line": 1,
            "column": 1
        })
        
        module_path = "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_block_src"
        
        with patch(f"{module_path}._parse_var_decl", mock_var_decl):
            with patch(f"{module_path}._peek_token") as mock_peek:
                mock_peek.return_value = {"type": "VAR", "value": "x", "line": 1, "column": 1}
                
                result = _parse_block(mock_state)
                
                self.assertEqual(result["type"], "BLOCK")
                self.assertEqual(len(result["children"]), 1)
                self.assertEqual(result["line"], 1)
                self.assertEqual(result["column"], 1)
                
                mock_var_decl.assert_called_once()
    
    def test_expression_statement_as_block(self):
        """Test parsing an expression statement as a block."""
        mock_state = {
            "tokens": [{"type": "IDENTIFIER", "value": "x", "line": 5, "column": 10}],
            "pos": 0,
            "filename": "test.c",
            "error": ""
        }
        
        mock_expr_stmt = MagicMock(return_value={
            "type": "EXPR_STMT",
            "children": [],
            "line": 5,
            "column": 10
        })
        
        module_path = "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_block_src"
        
        with patch(f"{module_path}._parse_expr_stmt", mock_expr_stmt):
            with patch(f"{module_path}._peek_token") as mock_peek:
                mock_peek.return_value = {"type": "IDENTIFIER", "value": "x", "line": 5, "column": 10}
                
                result = _parse_block(mock_state)
                
                self.assertEqual(result["type"], "BLOCK")
                self.assertEqual(len(result["children"]), 1)
                mock_expr_stmt.assert_called_once()
    
    def test_empty_block(self):
        """Test parsing an empty block (just braces)."""
        mock_state = {
            "tokens": [
                {"type": "LBRACE", "value": "{", "line": 1, "column": 1},
                {"type": "RBRACE", "value": "}", "line": 1, "column": 2}
            ],
            "pos": 0,
            "filename": "test.c",
            "error": ""
        }
        
        module_path = "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_block_src"
        
        with patch(f"{module_path}._peek_token") as mock_peek:
            with patch(f"{module_path}._consume_token") as mock_consume:
                mock_peek.side_effect = [
                    {"type": "LBRACE", "value": "{", "line": 1, "column": 1},
                    {"type": "RBRACE", "value": "}", "line": 1, "column": 2},
                    {"type": "RBRACE", "value": "}", "line": 1, "column": 2}
                ]
                
                mock_consume.side_effect = [mock_state, mock_state]
                
                result = _parse_block(mock_state)
                
                self.assertEqual(result["type"], "BLOCK")
                self.assertEqual(len(result["children"]), 0)
                self.assertEqual(result["line"], 1)
                self.assertEqual(result["column"], 1)
                
                self.assertEqual(mock_consume.call_count, 2)
    
    def test_error_unexpected_end_of_input_at_start(self):
        """Test error when input ends immediately at block start."""
        mock_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.c",
            "error": ""
        }
        
        module_path = "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_block_src"
        
        with patch(f"{module_path}._peek_token") as mock_peek:
            mock_peek.return_value = None
            
            with self.assertRaises(SyntaxError) as context:
                _parse_block(mock_state)
            
            self.assertIn("Unexpected end of input while parsing block", str(context.exception))
    
    def test_error_missing_closing_brace(self):
        """Test error when closing brace is missing."""
        mock_state = {
            "tokens": [
                {"type": "LBRACE", "value": "{", "line": 1, "column": 1},
                {"type": "VAR", "value": "int", "line": 2, "column": 5}
            ],
            "pos": 0,
            "filename": "test.c",
            "error": ""
        }
        
        module_path = "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_block_src"
        
        with patch(f"{module_path}._peek_token") as mock_peek:
            mock_peek.side_effect = [
                {"type": "LBRACE", "value": "{", "line": 1, "column": 1},
                {"type": "VAR", "value": "int", "line": 2, "column": 5},
                None
            ]
            
            with self.assertRaises(SyntaxError) as context:
                _parse_block(mock_state)
            
            self.assertIn("Unexpected end of input, expected '}'", str(context.exception))
    
    def test_all_statement_types_in_block(self):
        """Test parsing block with all supported statement types."""
        mock_state = {
            "tokens": [
                {"type": "LBRACE", "value": "{", "line": 1, "column": 1},
                {"type": "VAR", "value": "int", "line": 2, "column": 1},
                {"type": "IF", "value": "if", "line": 3, "column": 1},
                {"type": "WHILE", "value": "while", "line": 4, "column": 1},
                {"type": "FOR", "value": "for", "line": 5, "column": 1},
                {"type": "RETURN", "value": "return", "line": 6, "column": 1},
                {"type": "BREAK", "value": "break", "line": 7, "column": 1},
                {"type": "CONTINUE", "value": "continue", "line": 8, "column": 1},
                {"type": "IDENTIFIER", "value": "x", "line": 9, "column": 1},
                {"type": "RBRACE", "value": "}", "line": 10, "column": 1}
            ],
            "pos": 0,
            "filename": "test.c",
            "error": ""
        }
        
        mock_returns = {
            "var": {"type": "VAR_DECL", "children": [], "line": 2, "column": 1},
            "if": {"type": "IF_STMT", "children": [], "line": 3, "column": 1},
            "while": {"type": "WHILE_STMT", "children": [], "line": 4, "column": 1},
            "for": {"type": "FOR_STMT", "children": [], "line": 5, "column": 1},
            "return": {"type": "RETURN_STMT", "children": [], "line": 6, "column": 1},
            "break": {"type": "BREAK_STMT", "children": [], "line": 7, "column": 1},
            "continue": {"type": "CONTINUE_STMT", "children": [], "line": 8, "column": 1},
            "expr": {"type": "EXPR_STMT", "children": [], "line": 9, "column": 1}
        }
        
        module_path = "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_block_src"
        
        with patch(f"{module_path}._parse_var_decl", return_value=mock_returns["var"]):
            with patch(f"{module_path}._parse_if_stmt", return_value=mock_returns["if"]):
                with patch(f"{module_path}._parse_while_stmt", return_value=mock_returns["while"]):
                    with patch(f"{module_path}._parse_for_stmt", return_value=mock_returns["for"]):
                        with patch(f"{module_path}._parse_return_stmt", return_value=mock_returns["return"]):
                            with patch(f"{module_path}._parse_break_stmt", return_value=mock_returns["break"]):
                                with patch(f"{module_path}._parse_continue_stmt", return_value=mock_returns["continue"]):
                                    with patch(f"{module_path}._parse_expr_stmt", return_value=mock_returns["expr"]):
                                        with patch(f"{module_path}._peek_token") as mock_peek:
                                            with patch(f"{module_path}._consume_token") as mock_consume:
                                                peek_tokens = [
                                                    {"type": "LBRACE", "value": "{", "line": 1, "column": 1},
                                                    {"type": "VAR", "value": "int", "line": 2, "column": 1},
                                                    {"type": "IF", "value": "if", "line": 3, "column": 1},
                                                    {"type": "WHILE", "value": "while", "line": 4, "column": 1},
                                                    {"type": "FOR", "value": "for", "line": 5, "column": 1},
                                                    {"type": "RETURN", "value": "return", "line": 6, "column": 1},
                                                    {"type": "BREAK", "value": "break", "line": 7, "column": 1},
                                                    {"type": "CONTINUE", "value": "continue", "line": 8, "column": 1},
                                                    {"type": "IDENTIFIER", "value": "x", "line": 9, "column": 1},
                                                    {"type": "RBRACE", "value": "}", "line": 10, "column": 1},
                                                    {"type": "RBRACE", "value": "}", "line": 10, "column": 1}
                                                ]
                                                mock_peek.side_effect = peek_tokens
                                                mock_consume.side_effect = [mock_state] * 2
                                                
                                                result = _parse_block(mock_state)
                                                
                                                self.assertEqual(result["type"], "BLOCK")
                                                self.assertEqual(len(result["children"]), 8)
                                                self.assertEqual(result["children"][0]["type"], "VAR_DECL")
                                                self.assertEqual(result["children"][1]["type"], "IF_STMT")
                                                self.assertEqual(result["children"][2]["type"], "WHILE_STMT")
                                                self.assertEqual(result["children"][3]["type"], "FOR_STMT")
                                                self.assertEqual(result["children"][4]["type"], "RETURN_STMT")
                                                self.assertEqual(result["children"][5]["type"], "BREAK_STMT")
                                                self.assertEqual(result["children"][6]["type"], "CONTINUE_STMT")
                                                self.assertEqual(result["children"][7]["type"], "EXPR_STMT")


if __name__ == "__main__":
    unittest.main()

"""
Unit tests for _parse_grouping_expr function.
Tests parsing of grouping expressions (parenthesized expressions).
"""

import unittest
from unittest.mock import patch
from typing import Any, Dict

# Relative import for the function under test
from ._parse_grouping_expr_src import _parse_grouping_expr

# Type aliases for clarity
Token = Dict[str, Any]
AST = Dict[str, Any]
ParserState = Dict[str, Any]


class TestParseGroupingExpr(unittest.TestCase):
    """Test cases for _parse_grouping_expr function."""

    def _create_token(self, token_type: str, value: str, line: int = 1, column: int = 1) -> Token:
        """Helper to create a token dictionary."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def _create_parser_state(self, tokens: list, pos: int = 0, filename: str = "test.txt") -> ParserState:
        """Helper to create a parser state dictionary."""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename,
            "error": ""
        }

    def test_happy_path_simple_grouping(self):
        """Test parsing a simple grouping expression: (expr)."""
        left_paren = self._create_token("LEFT_PAREN", "(", line=1, column=1)
        right_paren = self._create_token("RIGHT_PAREN", ")", line=1, column=7)
        number_token = self._create_token("NUMBER", "42", line=1, column=3)
        
        tokens = [left_paren, number_token, right_paren]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # Mock inner expression AST
        mock_inner_expr = {
            "type": "NUMBER",
            "children": [],
            "value": "42",
            "line": 1,
            "column": 3
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_expression_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_grouping_expr_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = mock_inner_expr
            
            result = _parse_grouping_expr(parser_state, left_paren)
            
            # Verify result structure
            self.assertEqual(result["type"], "GROUPING")
            self.assertEqual(result["children"], [mock_inner_expr])
            self.assertIsNone(result["value"])
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            
            # Verify parser state was updated correctly
            self.assertEqual(parser_state["pos"], 3)  # Consumed both parens
            
            # Verify _parse_expression was called
            mock_parse_expr.assert_called_once()

    def test_happy_path_nested_grouping(self):
        """Test parsing nested grouping expressions: ((expr))."""
        left_paren1 = self._create_token("LEFT_PAREN", "(", line=1, column=1)
        left_paren2 = self._create_token("LEFT_PAREN", "(", line=1, column=2)
        right_paren1 = self._create_token("RIGHT_PAREN", ")", line=1, column=8)
        right_paren2 = self._create_token("RIGHT_PAREN", ")", line=1, column=9)
        number_token = self._create_token("NUMBER", "42", line=1, column=3)
        
        tokens = [left_paren1, left_paren2, number_token, right_paren1, right_paren2]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # Mock inner expression (which itself could be a grouping)
        mock_inner_expr = {
            "type": "GROUPING",
            "children": [],
            "value": None,
            "line": 1,
            "column": 2
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_expression_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_grouping_expr_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = mock_inner_expr
            
            result = _parse_grouping_expr(parser_state, left_paren1)
            
            self.assertEqual(result["type"], "GROUPING")
            self.assertEqual(result["children"], [mock_inner_expr])
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            
            # Should have consumed: left_paren1, then inner expression consumed rest
            # After function: pos should be 5 (all tokens consumed)
            self.assertEqual(parser_state["pos"], 5)

    def test_missing_right_paren_at_end_of_file(self):
        """Test error when RIGHT_PAREN is missing (end of tokens)."""
        left_paren = self._create_token("LEFT_PAREN", "(", line=2, column=5)
        number_token = self._create_token("NUMBER", "42", line=2, column=7)
        
        tokens = [left_paren, number_token]
        parser_state = self._create_parser_state(tokens, pos=0, filename="test.txt")
        
        mock_inner_expr = {
            "type": "NUMBER",
            "children": [],
            "value": "42",
            "line": 2,
            "column": 7
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_expression_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_grouping_expr_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = mock_inner_expr
            
            with self.assertRaises(SyntaxError) as context:
                _parse_grouping_expr(parser_state, left_paren)
            
            # Verify error message contains expected information
            error_msg = str(context.exception)
            self.assertIn("Missing ')'", error_msg)
            self.assertIn("test.txt", error_msg)
            self.assertIn("2:5", error_msg)
            
            # Position should have been incremented for LEFT_PAREN
            self.assertEqual(parser_state["pos"], 1)

    def test_wrong_token_instead_of_right_paren(self):
        """Test error when unexpected token appears instead of RIGHT_PAREN."""
        left_paren = self._create_token("LEFT_PAREN", "(", line=3, column=10)
        number_token = self._create_token("NUMBER", "42", line=3, column=12)
        semicolon = self._create_token("SEMICOLON", ";", line=3, column=15)
        
        tokens = [left_paren, number_token, semicolon]
        parser_state = self._create_parser_state(tokens, pos=0, filename="main.c")
        
        mock_inner_expr = {
            "type": "NUMBER",
            "children": [],
            "value": "42",
            "line": 3,
            "column": 12
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_expression_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_grouping_expr_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = mock_inner_expr
            
            with self.assertRaises(SyntaxError) as context:
                _parse_grouping_expr(parser_state, left_paren)
            
            error_msg = str(context.exception)
            self.assertIn("Expected ')'", error_msg)
            self.assertIn("got ';'", error_msg)
            self.assertIn("main.c", error_msg)
            self.assertIn("3:15", error_msg)
            
            # Position should have been incremented for LEFT_PAREN only
            self.assertEqual(parser_state["pos"], 1)

    def test_position_incremented_correctly(self):
        """Test that parser position is incremented correctly through the function."""
        left_paren = self._create_token("LEFT_PAREN", "(", line=1, column=1)
        right_paren = self._create_token("RIGHT_PAREN", ")", line=1, column=3)
        number_token = self._create_token("NUMBER", "42", line=1, column=2)
        
        tokens = [left_paren, number_token, right_paren]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        mock_inner_expr = {
            "type": "NUMBER",
            "children": [],
            "value": "42",
            "line": 1,
            "column": 2
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_expression_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_grouping_expr_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = mock_inner_expr
            mock_parse_expr.side_effect = lambda state: state.update({"pos": 2}) or mock_inner_expr
            
            result = _parse_grouping_expr(parser_state, left_paren)
            
            # After parsing: pos should be 3 (LEFT_PAREN consumed, inner expr consumed, RIGHT_PAREN consumed)
            self.assertEqual(parser_state["pos"], 3)

    def test_ast_node_structure(self):
        """Test that the returned AST node has correct structure."""
        left_paren = self._create_token("LEFT_PAREN", "(", line=5, column=20)
        right_paren = self._create_token("RIGHT_PAREN", ")", line=5, column=30)
        number_token = self._create_token("NUMBER", "100", line=5, column=22)
        
        tokens = [left_paren, number_token, right_paren]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        mock_inner_expr = {
            "type": "NUMBER",
            "children": [],
            "value": "100",
            "line": 5,
            "column": 22
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_expression_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_grouping_expr_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = mock_inner_expr
            
            result = _parse_grouping_expr(parser_state, left_paren)
            
            # Verify all required fields exist
            self.assertIn("type", result)
            self.assertIn("children", result)
            self.assertIn("value", result)
            self.assertIn("line", result)
            self.assertIn("column", result)
            
            # Verify field values
            self.assertEqual(result["type"], "GROUPING")
            self.assertIsInstance(result["children"], list)
            self.assertEqual(len(result["children"]), 1)
            self.assertIsNone(result["value"])
            self.assertEqual(result["line"], 5)
            self.assertEqual(result["column"], 20)

    def test_preserves_left_paren_location(self):
        """Test that GROUPING node preserves the left parenthesis location."""
        for line, column in [(1, 1), (10, 5), (100, 50)]:
            with self.subTest(line=line, column=column):
                left_paren = self._create_token("LEFT_PAREN", "(", line=line, column=column)
                right_paren = self._create_token("RIGHT_PAREN", ")", line=line, column=column + 10)
                number_token = self._create_token("NUMBER", "1", line=line, column=column + 2)
                
                tokens = [left_paren, number_token, right_paren]
                parser_state = self._create_parser_state(tokens, pos=0)
                
                mock_inner_expr = {
                    "type": "NUMBER",
                    "children": [],
                    "value": "1",
                    "line": line,
                    "column": column + 2
                }
                
                with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_expression_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_grouping_expr_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
                    mock_parse_expr.return_value = mock_inner_expr
                    
                    result = _parse_grouping_expr(parser_state, left_paren)
                    
                    self.assertEqual(result["line"], line)
                    self.assertEqual(result["column"], column)


if __name__ == "__main__":
    unittest.main()

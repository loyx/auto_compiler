# -*- coding: utf-8 -*-
"""Unit tests for _parse_while_stmt function."""

import unittest
from unittest.mock import patch
from typing import Dict, Any


# Import the function under test using relative import
from ._parse_while_stmt_src import _parse_while_stmt


class TestParseWhileStmt(unittest.TestCase):
    """Test cases for _parse_while_stmt function."""

    def setUp(self):
        """Set up test fixtures."""
        self.maxDiff = None

    def _create_parser_state(self, tokens: list, pos: int = 0, filename: str = "test.py") -> Dict[str, Any]:
        """Helper to create parser state."""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename
        }

    def _create_token(self, token_type: str, value: str = "", line: int = 1, column: int = 1) -> Dict[str, Any]:
        """Helper to create a token."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def test_happy_path_valid_while_statement(self):
        """Test parsing a valid while statement with all required tokens."""
        # Arrange
        tokens = [
            self._create_token("WHILE", "while", 1, 1),
            self._create_token("LPAREN", "(", 1, 7),
            self._create_token("IDENTIFIER", "x", 1, 8),
            self._create_token("RPAREN", ")", 1, 9),
            self._create_token("LBRACE", "{", 1, 11),
            self._create_token("RBRACE", "}", 1, 12),
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        mock_condition = {"type": "EXPR", "value": "x", "line": 1, "column": 8}
        mock_body = {"type": "BLOCK", "statements": [], "line": 1, "column": 11}
        
        with patch("._parse_while_stmt_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr, \
             patch("._parse_while_stmt_package._parse_block_package._parse_block_src._parse_block") as mock_parse_block:
            mock_parse_expr.return_value = mock_condition
            mock_parse_block.return_value = mock_body
            
            # Act
            result = _parse_while_stmt(parser_state)
            
            # Assert
            self.assertEqual(result["type"], "WHILE")
            self.assertEqual(result["condition"], mock_condition)
            self.assertEqual(result["body"], mock_body)
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            self.assertEqual(parser_state["pos"], 6)  # Should consume all tokens
            mock_parse_expr.assert_called_once()
            mock_parse_block.assert_called_once()

    def test_missing_lparen_raises_syntax_error(self):
        """Test that missing LPAREN raises SyntaxError."""
        # Arrange
        tokens = [
            self._create_token("WHILE", "while", 1, 1),
            self._create_token("IDENTIFIER", "x", 1, 7),  # Should be LPAREN
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        with patch("._parse_while_stmt_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            # Act & Assert
            with self.assertRaises(SyntaxError) as context:
                _parse_while_stmt(parser_state)
            
            self.assertIn("Expected LPAREN", str(context.exception))
            self.assertIn("test.py:1:1", str(context.exception))
            mock_parse_expr.assert_not_called()

    def test_missing_rparen_raises_syntax_error(self):
        """Test that missing RPAREN raises SyntaxError."""
        # Arrange
        tokens = [
            self._create_token("WHILE", "while", 1, 1),
            self._create_token("LPAREN", "(", 1, 7),
            self._create_token("IDENTIFIER", "x", 1, 8),
            self._create_token("LBRACE", "{", 1, 10),  # Should be RPAREN
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        mock_condition = {"type": "EXPR", "value": "x", "line": 1, "column": 8}
        
        with patch("._parse_while_stmt_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr, \
             patch("._parse_while_stmt_package._parse_block_package._parse_block_src._parse_block") as mock_parse_block:
            mock_parse_expr.return_value = mock_condition
            
            # Act & Assert
            with self.assertRaises(SyntaxError) as context:
                _parse_while_stmt(parser_state)
            
            self.assertIn("Expected RPAREN", str(context.exception))
            mock_parse_block.assert_not_called()

    def test_empty_tokens_raises_syntax_error(self):
        """Test that empty token list raises SyntaxError."""
        # Arrange
        tokens = []
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # Act & Assert
        with self.assertRaises(SyntaxError) as context:
            _parse_while_stmt(parser_state)
        
        self.assertIn("Expected WHILE", str(context.exception))

    def test_eof_token_raises_syntax_error(self):
        """Test that EOF token raises SyntaxError."""
        # Arrange
        tokens = [
            self._create_token("EOF", "", 0, 0),
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # Act & Assert
        with self.assertRaises(SyntaxError) as context:
            _parse_while_stmt(parser_state)
        
        self.assertIn("Expected WHILE", str(context.exception))

    def test_wrong_first_token_raises_syntax_error(self):
        """Test that non-WHILE first token raises SyntaxError."""
        # Arrange
        tokens = [
            self._create_token("IF", "if", 1, 1),  # Should be WHILE
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # Act & Assert
        with self.assertRaises(SyntaxError) as context:
            _parse_while_stmt(parser_state)
        
        self.assertIn("Expected WHILE", str(context.exception))
        self.assertIn("got IF", str(context.exception))

    def test_position_advances_correctly(self):
        """Test that parser_state position advances through all tokens."""
        # Arrange
        tokens = [
            self._create_token("WHILE", "while", 1, 1),
            self._create_token("LPAREN", "(", 1, 7),
            self._create_token("IDENTIFIER", "x", 1, 8),
            self._create_token("RPAREN", ")", 1, 9),
            self._create_token("LBRACE", "{", 1, 11),
            self._create_token("RBRACE", "}", 1, 12),
            self._create_token("SEMICOLON", ";", 1, 13),  # Extra token
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        mock_condition = {"type": "EXPR", "value": "x", "line": 1, "column": 8}
        mock_body = {"type": "BLOCK", "statements": [], "line": 1, "column": 11}
        
        with patch("._parse_while_stmt_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr, \
             patch("._parse_while_stmt_package._parse_block_package._parse_block_src._parse_block") as mock_parse_block:
            mock_parse_expr.return_value = mock_condition
            mock_parse_block.return_value = mock_body
            
            # Act
            result = _parse_while_stmt(parser_state)
            
            # Assert
            self.assertEqual(parser_state["pos"], 6)  # Should stop after RBRACE, before SEMICOLON

    def test_line_column_preserved_from_while_token(self):
        """Test that line and column are preserved from WHILE token."""
        # Arrange
        tokens = [
            self._create_token("WHILE", "while", 5, 10),  # Line 5, Column 10
            self._create_token("LPAREN", "(", 5, 16),
            self._create_token("IDENTIFIER", "x", 5, 17),
            self._create_token("RPAREN", ")", 5, 18),
            self._create_token("LBRACE", "{", 5, 20),
            self._create_token("RBRACE", "}", 5, 21),
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        mock_condition = {"type": "EXPR", "value": "x", "line": 5, "column": 17}
        mock_body = {"type": "BLOCK", "statements": [], "line": 5, "column": 20}
        
        with patch("._parse_while_stmt_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr, \
             patch("._parse_while_stmt_package._parse_block_package._parse_block_src._parse_block") as mock_parse_block:
            mock_parse_expr.return_value = mock_condition
            mock_parse_block.return_value = mock_body
            
            # Act
            result = _parse_while_stmt(parser_state)
            
            # Assert
            self.assertEqual(result["line"], 5)
            self.assertEqual(result["column"], 10)

    def test_parse_expression_called_with_correct_state(self):
        """Test that _parse_expression is called with the parser state."""
        # Arrange
        tokens = [
            self._create_token("WHILE", "while", 1, 1),
            self._create_token("LPAREN", "(", 1, 7),
            self._create_token("IDENTIFIER", "x", 1, 8),
            self._create_token("RPAREN", ")", 1, 9),
            self._create_token("LBRACE", "{", 1, 11),
            self._create_token("RBRACE", "}", 1, 12),
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        mock_condition = {"type": "EXPR", "value": "x", "line": 1, "column": 8}
        mock_body = {"type": "BLOCK", "statements": [], "line": 1, "column": 11}
        
        with patch("._parse_while_stmt_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr, \
             patch("._parse_while_stmt_package._parse_block_package._parse_block_src._parse_block") as mock_parse_block:
            mock_parse_expr.return_value = mock_condition
            mock_parse_block.return_value = mock_body
            
            # Act
            _parse_while_stmt(parser_state)
            
            # Assert
            mock_parse_expr.assert_called_once_with(parser_state)

    def test_parse_block_called_with_correct_state(self):
        """Test that _parse_block is called with the parser state after condition."""
        # Arrange
        tokens = [
            self._create_token("WHILE", "while", 1, 1),
            self._create_token("LPAREN", "(", 1, 7),
            self._create_token("IDENTIFIER", "x", 1, 8),
            self._create_token("RPAREN", ")", 1, 9),
            self._create_token("LBRACE", "{", 1, 11),
            self._create_token("RBRACE", "}", 1, 12),
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        mock_condition = {"type": "EXPR", "value": "x", "line": 1, "column": 8}
        mock_body = {"type": "BLOCK", "statements": [], "line": 1, "column": 11}
        
        with patch("._parse_while_stmt_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr, \
             patch("._parse_while_stmt_package._parse_block_package._parse_block_src._parse_block") as mock_parse_block:
            mock_parse_expr.return_value = mock_condition
            mock_parse_block.return_value = mock_body
            
            # Act
            _parse_while_stmt(parser_state)
            
            # Assert
            mock_parse_block.assert_called_once_with(parser_state)

    def test_complex_condition_expression(self):
        """Test while statement with complex condition expression."""
        # Arrange
        tokens = [
            self._create_token("WHILE", "while", 1, 1),
            self._create_token("LPAREN", "(", 1, 7),
            self._create_token("IDENTIFIER", "x", 1, 8),
            self._create_token("GT", ">", 1, 10),
            self._create_token("NUMBER", "0", 1, 12),
            self._create_token("RPAREN", ")", 1, 13),
            self._create_token("LBRACE", "{", 1, 15),
            self._create_token("RBRACE", "}", 1, 16),
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        mock_condition = {
            "type": "BINARY_OP",
            "left": {"type": "IDENTIFIER", "value": "x"},
            "operator": ">",
            "right": {"type": "NUMBER", "value": "0"},
            "line": 1,
            "column": 8
        }
        mock_body = {"type": "BLOCK", "statements": [], "line": 1, "column": 15}
        
        with patch("._parse_while_stmt_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr, \
             patch("._parse_while_stmt_package._parse_block_package._parse_block_src._parse_block") as mock_parse_block:
            mock_parse_expr.return_value = mock_condition
            mock_parse_block.return_value = mock_body
            
            # Act
            result = _parse_while_stmt(parser_state)
            
            # Assert
            self.assertEqual(result["condition"], mock_condition)
            self.assertEqual(parser_state["pos"], 8)

    def test_block_with_statements(self):
        """Test while statement with block containing statements."""
        # Arrange
        tokens = [
            self._create_token("WHILE", "while", 1, 1),
            self._create_token("LPAREN", "(", 1, 7),
            self._create_token("IDENTIFIER", "x", 1, 8),
            self._create_token("RPAREN", ")", 1, 9),
            self._create_token("LBRACE", "{", 1, 11),
            self._create_token("IDENTIFIER", "y", 1, 13),
            self._create_token("ASSIGN", "=", 1, 15),
            self._create_token("NUMBER", "1", 1, 17),
            self._create_token("SEMICOLON", ";", 1, 18),
            self._create_token("RBRACE", "}", 1, 20),
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        mock_condition = {"type": "EXPR", "value": "x", "line": 1, "column": 8}
        mock_body = {
            "type": "BLOCK",
            "statements": [
                {"type": "ASSIGNMENT", "target": "y", "value": "1"}
            ],
            "line": 1,
            "column": 11
        }
        
        with patch("._parse_while_stmt_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr, \
             patch("._parse_while_stmt_package._parse_block_package._parse_block_src._parse_block") as mock_parse_block:
            mock_parse_expr.return_value = mock_condition
            mock_parse_block.return_value = mock_body
            
            # Act
            result = _parse_while_stmt(parser_state)
            
            # Assert
            self.assertEqual(result["body"], mock_body)
            self.assertEqual(len(mock_body["statements"]), 1)

    def test_nested_while_statement(self):
        """Test while statement with nested while in body."""
        # Arrange
        tokens = [
            self._create_token("WHILE", "while", 1, 1),
            self._create_token("LPAREN", "(", 1, 7),
            self._create_token("IDENTIFIER", "x", 1, 8),
            self._create_token("RPAREN", ")", 1, 9),
            self._create_token("LBRACE", "{", 1, 11),
            self._create_token("WHILE", "while", 2, 5),
            self._create_token("LPAREN", "(", 2, 11),
            self._create_token("IDENTIFIER", "y", 2, 12),
            self._create_token("RPAREN", ")", 2, 13),
            self._create_token("LBRACE", "{", 2, 15),
            self._create_token("RBRACE", "}", 2, 16),
            self._create_token("RBRACE", "}", 3, 1),
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        mock_condition = {"type": "EXPR", "value": "x", "line": 1, "column": 8}
        mock_inner_while = {
            "type": "WHILE",
            "condition": {"type": "EXPR", "value": "y", "line": 2, "column": 12},
            "body": {"type": "BLOCK", "statements": [], "line": 2, "column": 15},
            "line": 2,
            "column": 5
        }
        mock_body = {
            "type": "BLOCK",
            "statements": [mock_inner_while],
            "line": 1,
            "column": 11
        }
        
        with patch("._parse_while_stmt_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr, \
             patch("._parse_while_stmt_package._parse_block_package._parse_block_src._parse_block") as mock_parse_block:
            mock_parse_expr.return_value = mock_condition
            mock_parse_block.return_value = mock_body
            
            # Act
            result = _parse_while_stmt(parser_state)
            
            # Assert
            self.assertEqual(result["body"]["statements"][0]["type"], "WHILE")
            self.assertEqual(result["body"]["statements"][0]["condition"]["value"], "y")

    def test_parser_state_filename_used_in_error(self):
        """Test that parser_state filename is used in error messages."""
        # Arrange
        tokens = [
            self._create_token("WHILE", "while", 1, 1),
            self._create_token("IDENTIFIER", "x", 1, 7),  # Should be LPAREN
        ]
        parser_state = self._create_parser_state(tokens, pos=0, filename="my_source.py")
        
        # Act & Assert
        with self.assertRaises(SyntaxError) as context:
            _parse_while_stmt(parser_state)
        
        self.assertIn("my_source.py", str(context.exception))


if __name__ == "__main__":
    unittest.main()

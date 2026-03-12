# -*- coding: utf-8 -*-
"""
Unit tests for _parse_expression_stmt function.
Tests expression statement parsing (expression ;).
"""

import unittest
from unittest.mock import patch, MagicMock
from typing import Dict, Any

from ._parse_expression_stmt_src import _parse_expression_stmt


class TestParseExpressionStmt(unittest.TestCase):
    """Test cases for _parse_expression_stmt function."""

    def _create_parser_state(
        self,
        tokens: list,
        pos: int = 0,
        filename: str = "<test>"
    ) -> Dict[str, Any]:
        """Helper to create parser state dict."""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename
        }

    def _create_token(
        self,
        token_type: str,
        value: str = "",
        line: int = 1,
        column: int = 1
    ) -> Dict[str, Any]:
        """Helper to create a token dict."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    @patch("._parse_expression_package._parse_expression_src._parse_expression")
    def test_happy_path_simple_expression(self, mock_parse_expression: MagicMock) -> None:
        """Test parsing a simple expression followed by semicolon."""
        # Setup tokens: IDENTIFIER + SEMICOLON
        tokens = [
            self._create_token("IDENTIFIER", "x", 1, 1),
            self._create_token("SEMICOLON", ";", 1, 2),
            self._create_token("EOF", "", 1, 3)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # Mock _parse_expression to return a simple AST
        mock_expression_ast = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 1
        }
        mock_parse_expression.return_value = mock_expression_ast
        mock_parse_expression.side_effect = lambda state: state.update({"pos": 1}) or mock_expression_ast
        
        # Call function
        result = _parse_expression_stmt(parser_state)
        
        # Verify result structure
        self.assertEqual(result["type"], "EXPRESSION_STMT")
        self.assertEqual(result["expression"], mock_expression_ast)
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        
        # Verify parser_state was updated
        self.assertEqual(parser_state["pos"], 2)

    @patch("._parse_expression_package._parse_expression_src._parse_expression")
    def test_happy_path_binary_expression(self, mock_parse_expression: MagicMock) -> None:
        """Test parsing a binary expression followed by semicolon."""
        # Setup tokens: binary expression + SEMICOLON
        tokens = [
            self._create_token("NUMBER", "5", 2, 5),
            self._create_token("PLUS", "+", 2, 7),
            self._create_token("NUMBER", "3", 2, 9),
            self._create_token("SEMICOLON", ";", 2, 10),
            self._create_token("EOF", "", 3, 1)
        ]
        parser_state = self._create_parser_state(tokens, pos=0, filename="test.py")
        
        # Mock _parse_expression to consume 3 tokens and return binary expr AST
        mock_expression_ast = {
            "type": "BINARY_EXPR",
            "operator": "+",
            "left": {"type": "NUMBER", "value": "5"},
            "right": {"type": "NUMBER", "value": "3"},
            "line": 2,
            "column": 5
        }
        
        def mock_parse_side_effect(state: Dict[str, Any]) -> Dict[str, Any]:
            state["pos"] = 3  # Consume 3 tokens
            return mock_expression_ast
        
        mock_parse_expression.side_effect = mock_parse_side_effect
        
        # Call function
        result = _parse_expression_stmt(parser_state)
        
        # Verify result
        self.assertEqual(result["type"], "EXPRESSION_STMT")
        self.assertEqual(result["expression"]["type"], "BINARY_EXPR")
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 5)
        
        # Verify parser_state was updated to point after semicolon
        self.assertEqual(parser_state["pos"], 4)

    @patch("._parse_expression_package._parse_expression_src._parse_expression")
    def test_error_missing_semicolon(self, mock_parse_expression: MagicMock) -> None:
        """Test error when semicolon is missing after expression."""
        # Setup tokens: expression without semicolon
        tokens = [
            self._create_token("IDENTIFIER", "x", 1, 1),
            self._create_token("IDENTIFIER", "y", 1, 3)  # Wrong token type
        ]
        parser_state = self._create_parser_state(tokens, pos=0, filename="error.py")
        
        # Mock _parse_expression to consume 1 token
        mock_expression_ast = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 1
        }
        
        def mock_parse_side_effect(state: Dict[str, Any]) -> Dict[str, Any]:
            state["pos"] = 1
            return mock_expression_ast
        
        mock_parse_expression.side_effect = mock_parse_side_effect
        
        # Call function and expect SyntaxError
        with self.assertRaises(SyntaxError) as context:
            _parse_expression_stmt(parser_state)
        
        # Verify error message
        error_msg = str(context.exception)
        self.assertIn("error.py", error_msg)
        self.assertIn("Expected ';' after expression", error_msg)

    @patch("._parse_expression_package._parse_expression_src._parse_expression")
    def test_error_end_of_tokens(self, mock_parse_expression: MagicMock) -> None:
        """Test error when tokens end before semicolon."""
        # Setup tokens: expression at end, no semicolon
        tokens = [
            self._create_token("IDENTIFIER", "x", 5, 10)
        ]
        parser_state = self._create_parser_state(tokens, pos=0, filename="eof.py")
        
        # Mock _parse_expression to consume all tokens
        mock_expression_ast = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 5,
            "column": 10
        }
        
        def mock_parse_side_effect(state: Dict[str, Any]) -> Dict[str, Any]:
            state["pos"] = 1  # Move past the only token
            return mock_expression_ast
        
        mock_parse_expression.side_effect = mock_parse_side_effect
        
        # Call function and expect SyntaxError
        with self.assertRaises(SyntaxError) as context:
            _parse_expression_stmt(parser_state)
        
        # Verify error message
        error_msg = str(context.exception)
        self.assertIn("eof.py", error_msg)
        self.assertIn("Expected ';' after expression", error_msg)

    @patch("._parse_expression_package._parse_expression_src._parse_expression")
    def test_position_tracking_after_semicolon(self, mock_parse_expression: MagicMock) -> None:
        """Test that parser position is correctly updated after consuming semicolon."""
        # Setup multiple statements
        tokens = [
            self._create_token("IDENTIFIER", "x", 1, 1),
            self._create_token("SEMICOLON", ";", 1, 2),
            self._create_token("IDENTIFIER", "y", 1, 4),
            self._create_token("SEMICOLON", ";", 1, 5)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # Mock _parse_expression to consume 1 token
        mock_expression_ast = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 1
        }
        
        def mock_parse_side_effect(state: Dict[str, Any]) -> Dict[str, Any]:
            state["pos"] = 1
            return mock_expression_ast
        
        mock_parse_expression.side_effect = mock_parse_side_effect
        
        # Call function
        result = _parse_expression_stmt(parser_state)
        
        # Verify position is now at token 2 (second IDENTIFIER)
        self.assertEqual(parser_state["pos"], 2)
        self.assertEqual(tokens[parser_state["pos"]]["type"], "IDENTIFIER")
        self.assertEqual(tokens[parser_state["pos"]]["value"], "y")

    @patch("._parse_expression_package._parse_expression_src._parse_expression")
    def test_line_column_from_first_token(self, mock_parse_expression: MagicMock) -> None:
        """Test that line/column in result comes from first token of expression."""
        # Setup tokens starting at different position
        tokens = [
            self._create_token("NUMBER", "42", 10, 25),
            self._create_token("SEMICOLON", ";", 10, 28)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # Mock _parse_expression
        mock_expression_ast = {
            "type": "NUMBER",
            "value": "42",
            "line": 10,
            "column": 25
        }
        
        def mock_parse_side_effect(state: Dict[str, Any]) -> Dict[str, Any]:
            state["pos"] = 1
            return mock_expression_ast
        
        mock_parse_expression.side_effect = mock_parse_side_effect
        
        # Call function
        result = _parse_expression_stmt(parser_state)
        
        # Verify line/column from first token
        self.assertEqual(result["line"], 10)
        self.assertEqual(result["column"], 25)

    @patch("._parse_expression_package._parse_expression_src._parse_expression")
    def test_default_filename_when_missing(self, mock_parse_expression: MagicMock) -> None:
        """Test that default filename is used when not provided."""
        # Setup tokens without filename in parser_state
        tokens = [
            self._create_token("IDENTIFIER", "x", 1, 1),
            self._create_token("SEMICOLON", ";", 1, 2)
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0
            # No filename key
        }
        
        # Mock _parse_expression
        mock_expression_ast = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 1
        }
        
        def mock_parse_side_effect(state: Dict[str, Any]) -> Dict[str, Any]:
            state["pos"] = 1
            return mock_expression_ast
        
        mock_parse_expression.side_effect = mock_parse_side_effect
        
        # Remove filename to trigger error
        parser_state_no_semicolon = {
            "tokens": [self._create_token("IDENTIFIER", "x", 1, 1)],
            "pos": 0
        }
        
        def mock_parse_no_semi(state: Dict[str, Any]) -> Dict[str, Any]:
            state["pos"] = 1
            return mock_expression_ast
        
        mock_parse_expression.side_effect = mock_parse_no_semi
        
        # Call function and expect error with default filename
        with self.assertRaises(SyntaxError) as context:
            _parse_expression_stmt(parser_state_no_semicolon)
        
        # Verify default filename in error
        error_msg = str(context.exception)
        self.assertIn("<unknown>", error_msg)


if __name__ == "__main__":
    unittest.main()

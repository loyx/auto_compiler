# === std / third-party imports ===
import unittest
from unittest.mock import patch, MagicMock
from typing import Dict, Any
import sys

# === Mock dependent modules before importing UUT ===
# We need to prevent the actual import of dependency modules to avoid circular imports
# and path issues. We'll mock the entire dependency tree.

# Create a comprehensive mock for all dependencies
_mock_func = MagicMock(return_value={"type": "MOCK"})
_mock_consume_func = MagicMock()
_mock_peek_func = MagicMock(return_value=None)

# Mock _consume_token
_mock_consume_module = MagicMock()
_mock_consume_module._consume_token = _mock_consume_func
sys.modules['._consume_token_package'] = MagicMock()
sys.modules['._consume_token_package._consume_token_src'] = _mock_consume_module

# Mock _peek_token
_mock_peek_module = MagicMock()
_mock_peek_module._peek_token = _mock_peek_func
sys.modules['._peek_token_package'] = MagicMock()
sys.modules['._peek_token_package._peek_token_src'] = _mock_peek_module

# Mock _parse_block
_mock_block_module = MagicMock()
_mock_block_module._parse_block = MagicMock(return_value={"type": "BLOCK", "statements": []})
sys.modules['._parse_block_package'] = MagicMock()
sys.modules['._parse_block_package._parse_block_src'] = _mock_block_module

# Mock _parse_expression and all its submodules to break circular import
_mock_expr_module = MagicMock()
_mock_expr_module._parse_expression = _mock_func
sys.modules['._parse_expression_package'] = MagicMock()
sys.modules['._parse_expression_package._parse_expression_src'] = _mock_expr_module

# Mock _parse_primary_package and all its submodules
sys.modules['._parse_expression_package._parse_primary_package'] = MagicMock()
sys.modules['._parse_expression_package._parse_primary_package._parse_primary_src'] = MagicMock()
sys.modules['._parse_expression_package._parse_primary_package._parse_primary_src']._parse_primary = _mock_func

sys.modules['._parse_expression_package._parse_primary_package._parse_literal_package'] = MagicMock()
sys.modules['._parse_expression_package._parse_primary_package._parse_literal_package._parse_literal_src'] = MagicMock()

sys.modules['._parse_expression_package._parse_primary_package._parse_function_call_package'] = MagicMock()
sys.modules['._parse_expression_package._parse_primary_package._parse_function_call_package._parse_function_call_src'] = MagicMock()
sys.modules['._parse_expression_package._parse_primary_package._parse_function_call_package._parse_function_call_src']._parse_function_call = _mock_func

sys.modules['._parse_expression_package._get_precedence_package'] = MagicMock()
sys.modules['._parse_expression_package._get_precedence_package._get_precedence_src'] = MagicMock()

# === UUT import (relative) ===
from ._parse_if_statement_src import _parse_if_statement


class TestParseIfStatement(unittest.TestCase):
    """Test cases for _parse_if_statement function."""

    def _create_mock_token(self, token_type: str, value: str = "", line: int = 1, column: int = 1) -> Dict[str, Any]:
        """Helper to create a mock token dict."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def _create_parser_state(self, tokens: list, pos: int = 0, filename: str = "test.py") -> Dict[str, Any]:
        """Helper to create a parser_state dict."""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename,
            "error": ""
        }

    @patch('._parse_if_statement_src._consume_token')
    @patch('._parse_if_statement_src._parse_expression')
    @patch('._parse_if_statement_src._parse_block')
    @patch('._parse_if_statement_src._peek_token')
    def test_if_statement_without_else(self, mock_peek, mock_parse_block, mock_parse_expr, mock_consume):
        """Test parsing IF statement without ELSE block."""
        # Setup tokens
        if_token = self._create_mock_token("IF", "if", line=5, column=10)
        lparen_token = self._create_mock_token("LPAREN", "(")
        rparen_token = self._create_mock_token("RPAREN", ")")
        tokens = [if_token, lparen_token, rparen_token]
        
        parser_state = self._create_parser_state(tokens, pos=1)  # pos after IF
        
        # Setup mocks
        mock_consume.side_effect = lambda state, expected: None  # Just consume, don't modify
        mock_parse_expr.return_value = {"type": "EXPRESSION", "value": "x > 0"}
        mock_parse_block.return_value = {"type": "BLOCK", "statements": []}
        mock_peek.return_value = None  # No ELSE token
        
        # Execute
        result = _parse_if_statement(parser_state)
        
        # Verify
        self.assertEqual(result["type"], "IF_STATEMENT")
        self.assertEqual(result["condition"], {"type": "EXPRESSION", "value": "x > 0"})
        self.assertEqual(result["then_block"], {"type": "BLOCK", "statements": []})
        self.assertIsNone(result["else_block"])
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 10)
        
        # Verify consume was called for LPAREN and RPAREN
        self.assertEqual(mock_consume.call_count, 2)
        mock_consume.assert_any_call(parser_state, "LPAREN")
        mock_consume.assert_any_call(parser_state, "RPAREN")

    @patch('._parse_if_statement_src._consume_token')
    @patch('._parse_if_statement_src._parse_expression')
    @patch('._parse_if_statement_src._parse_block')
    @patch('._parse_if_statement_src._peek_token')
    def test_if_statement_with_else(self, mock_peek, mock_parse_block, mock_parse_expr, mock_consume):
        """Test parsing IF statement with ELSE block."""
        # Setup tokens
        if_token = self._create_mock_token("IF", "if", line=3, column=5)
        lparen_token = self._create_mock_token("LPAREN", "(")
        rparen_token = self._create_mock_token("RPAREN", ")")
        else_token = self._create_mock_token("ELSE", "else")
        tokens = [if_token, lparen_token, rparen_token, else_token]
        
        parser_state = self._create_parser_state(tokens, pos=1)  # pos after IF
        
        # Setup mocks
        mock_consume.side_effect = lambda state, expected: None
        mock_parse_expr.return_value = {"type": "EXPRESSION", "value": "y < 10"}
        mock_parse_block.side_effect = [
            {"type": "BLOCK", "statements": ["stmt1"]},  # then block
            {"type": "BLOCK", "statements": ["stmt2"]}   # else block
        ]
        mock_peek.return_value = else_token  # ELSE token present
        
        # Execute
        result = _parse_if_statement(parser_state)
        
        # Verify
        self.assertEqual(result["type"], "IF_STATEMENT")
        self.assertEqual(result["condition"], {"type": "EXPRESSION", "value": "y < 10"})
        self.assertEqual(result["then_block"], {"type": "BLOCK", "statements": ["stmt1"]})
        self.assertEqual(result["else_block"], {"type": "BLOCK", "statements": ["stmt2"]})
        self.assertEqual(result["line"], 3)
        self.assertEqual(result["column"], 5)
        
        # Verify consume was called for LPAREN, RPAREN, and ELSE
        self.assertEqual(mock_consume.call_count, 3)
        mock_consume.assert_any_call(parser_state, "LPAREN")
        mock_consume.assert_any_call(parser_state, "RPAREN")
        mock_consume.assert_any_call(parser_state, "ELSE")

    @patch('._parse_if_statement_src._consume_token')
    @patch('._parse_if_statement_src._parse_expression')
    @patch('._parse_if_statement_src._parse_block')
    @patch('._parse_if_statement_src._peek_token')
    def test_if_statement_complex_condition(self, mock_peek, mock_parse_block, mock_parse_expr, mock_consume):
        """Test IF statement with complex condition expression."""
        # Setup tokens
        if_token = self._create_mock_token("IF", "if", line=1, column=1)
        tokens = [if_token]
        
        parser_state = self._create_parser_state(tokens, pos=1)
        
        # Setup mocks
        mock_consume.side_effect = lambda state, expected: None
        mock_parse_expr.return_value = {
            "type": "BINARY_OP",
            "left": {"type": "VAR", "name": "a"},
            "op": "and",
            "right": {"type": "VAR", "name": "b"}
        }
        mock_parse_block.return_value = {"type": "BLOCK", "statements": []}
        mock_peek.return_value = None
        
        # Execute
        result = _parse_if_statement(parser_state)
        
        # Verify
        self.assertEqual(result["type"], "IF_STATEMENT")
        self.assertEqual(result["condition"]["type"], "BINARY_OP")
        self.assertEqual(result["condition"]["op"], "and")
        self.assertIsNone(result["else_block"])

    @patch('._parse_if_statement_src._consume_token')
    @patch('._parse_if_statement_src._parse_expression')
    @patch('._parse_if_statement_src._parse_block')
    @patch('._parse_if_statement_src._peek_token')
    def test_if_statement_nested_blocks(self, mock_peek, mock_parse_block, mock_parse_expr, mock_consume):
        """Test IF statement with nested blocks."""
        # Setup tokens
        if_token = self._create_mock_token("IF", "if", line=10, column=20)
        tokens = [if_token]
        
        parser_state = self._create_parser_state(tokens, pos=1)
        
        # Setup mocks
        mock_consume.side_effect = lambda state, expected: None
        mock_parse_expr.return_value = {"type": "EXPRESSION", "value": "flag"}
        
        nested_if_block = {
            "type": "BLOCK",
            "statements": [
                {"type": "IF_STATEMENT", "condition": {"type": "EXPR"}}
            ]
        }
        else_block = {"type": "BLOCK", "statements": [{"type": "RETURN"}]}
        
        mock_parse_block.side_effect = [nested_if_block, else_block]
        mock_peek.return_value = self._create_mock_token("ELSE", "else")
        
        # Execute
        result = _parse_if_statement(parser_state)
        
        # Verify
        self.assertEqual(result["type"], "IF_STATEMENT")
        self.assertEqual(len(result["then_block"]["statements"]), 1)
        self.assertEqual(result["then_block"]["statements"][0]["type"], "IF_STATEMENT")
        self.assertEqual(len(result["else_block"]["statements"]), 1)
        self.assertEqual(result["else_block"]["statements"][0]["type"], "RETURN")

    @patch('._parse_if_statement_src._consume_token')
    @patch('._parse_if_statement_src._parse_expression')
    @patch('._parse_if_statement_src._parse_block')
    @patch('._parse_if_statement_src._peek_token')
    def test_if_statement_position_tracking(self, mock_peek, mock_parse_block, mock_parse_expr, mock_consume):
        """Test that line and column are correctly tracked from IF token."""
        # Test various positions
        test_cases = [
            (1, 1),
            (5, 10),
            (100, 50),
            (1, 100)
        ]
        
        for line, column in test_cases:
            with self.subTest(line=line, column=column):
                if_token = self._create_mock_token("IF", "if", line=line, column=column)
                tokens = [if_token]
                
                parser_state = self._create_parser_state(tokens, pos=1)
                
                mock_consume.side_effect = lambda state, expected: None
                mock_parse_expr.return_value = {"type": "EXPRESSION"}
                mock_parse_block.return_value = {"type": "BLOCK", "statements": []}
                mock_peek.return_value = None
                
                result = _parse_if_statement(parser_state)
                
                self.assertEqual(result["line"], line)
                self.assertEqual(result["column"], column)

    @patch('._parse_if_statement_src._consume_token')
    @patch('._parse_if_statement_src._parse_expression')
    @patch('._parse_if_statement_src._parse_block')
    @patch('._parse_if_statement_src._peek_token')
    def test_peek_returns_none_at_eof(self, mock_peek, mock_parse_block, mock_parse_expr, mock_consume):
        """Test that ELSE is not parsed when peek returns None (EOF)."""
        if_token = self._create_mock_token("IF", "if", line=1, column=1)
        tokens = [if_token]
        
        parser_state = self._create_parser_state(tokens, pos=1)
        
        mock_consume.side_effect = lambda state, expected: None
        mock_parse_expr.return_value = {"type": "EXPRESSION"}
        mock_parse_block.return_value = {"type": "BLOCK", "statements": []}
        mock_peek.return_value = None  # EOF
        
        result = _parse_if_statement(parser_state)
        
        self.assertIsNone(result["else_block"])
        mock_consume.assert_called_with(parser_state, "RPAREN")
        # ELSE should not be consumed
        consume_calls = [call[0] for call in mock_consume.call_args_list]
        self.assertNotIn((parser_state, "ELSE"), consume_calls)

    @patch('._parse_if_statement_src._consume_token')
    @patch('._parse_if_statement_src._parse_expression')
    @patch('._parse_if_statement_src._parse_block')
    @patch('._parse_if_statement_src._peek_token')
    def test_peek_returns_non_else_token(self, mock_peek, mock_parse_block, mock_parse_expr, mock_consume):
        """Test that ELSE block is not parsed when next token is not ELSE."""
        if_token = self._create_mock_token("IF", "if", line=1, column=1)
        tokens = [if_token]
        
        parser_state = self._create_parser_state(tokens, pos=1)
        
        mock_consume.side_effect = lambda state, expected: None
        mock_parse_expr.return_value = {"type": "EXPRESSION"}
        mock_parse_block.return_value = {"type": "BLOCK", "statements": []}
        mock_peek.return_value = self._create_mock_token("WHILE", "while")  # Not ELSE
        
        result = _parse_if_statement(parser_state)
        
        self.assertIsNone(result["else_block"])
        # ELSE should not be consumed
        consume_calls = [call[0] for call in mock_consume.call_args_list]
        self.assertNotIn((parser_state, "ELSE"), consume_calls)

    @patch('._parse_if_statement_src._consume_token')
    @patch('._parse_if_statement_src._parse_expression')
    @patch('._parse_if_statement_src._parse_block')
    @patch('._parse_if_statement_src._peek_token')
    def test_consume_token_called_with_correct_types(self, mock_peek, mock_parse_block, mock_parse_expr, mock_consume):
        """Test that _consume_token is called with correct token types in order."""
        if_token = self._create_mock_token("IF", "if", line=1, column=1)
        else_token = self._create_mock_token("ELSE", "else")
        tokens = [if_token, else_token]
        
        parser_state = self._create_parser_state(tokens, pos=1)
        
        mock_consume.side_effect = lambda state, expected: None
        mock_parse_expr.return_value = {"type": "EXPRESSION"}
        mock_parse_block.side_effect = [
            {"type": "BLOCK", "statements": []},
            {"type": "BLOCK", "statements": []}
        ]
        mock_peek.return_value = else_token
        
        result = _parse_if_statement(parser_state)
        
        # Verify consume was called in correct order
        expected_calls = [
            unittest.mock.call(parser_state, "LPAREN"),
            unittest.mock.call(parser_state, "RPAREN"),
            unittest.mock.call(parser_state, "ELSE")
        ]
        mock_consume.assert_has_calls(expected_calls, any_order=False)


class TestParseIfStatementIntegration(unittest.TestCase):
    """Integration-style tests with more realistic parser_state manipulation."""

    @patch('._parse_if_statement_src._consume_token')
    @patch('._parse_if_statement_src._parse_expression')
    @patch('._parse_if_statement_src._parse_block')
    @patch('._parse_if_statement_src._peek_token')
    def test_full_if_else_structure(self, mock_peek, mock_parse_block, mock_parse_expr, mock_consume):
        """Test complete IF-ELSE structure with all components."""
        if_token = {"type": "IF", "value": "if", "line": 7, "column": 3}
        tokens = [if_token]
        
        parser_state = {
            "tokens": tokens,
            "pos": 1,
            "filename": "example.py",
            "error": ""
        }
        
        # Setup realistic mocks
        def consume_side_effect(state, expected_type):
            state["pos"] += 1  # Simulate position advance
        
        mock_consume.side_effect = consume_side_effect
        mock_parse_expr.return_value = {
            "type": "COMPARISON",
            "left": {"type": "IDENTIFIER", "name": "count"},
            "operator": ">",
            "right": {"type": "NUMBER", "value": 0}
        }
        
        then_block = {
            "type": "BLOCK",
            "statements": [
                {"type": "ASSIGNMENT", "target": "x", "value": {"type": "NUMBER", "value": 1}}
            ]
        }
        else_block = {
            "type": "BLOCK",
            "statements": [
                {"type": "ASSIGNMENT", "target": "x", "value": {"type": "NUMBER", "value": 0}}
            ]
        }
        mock_parse_block.side_effect = [then_block, else_block]
        mock_peek.return_value = {"type": "ELSE", "value": "else", "line": 9, "column": 3}
        
        result = _parse_if_statement(parser_state)
        
        # Verify complete structure
        self.assertEqual(result["type"], "IF_STATEMENT")
        self.assertEqual(result["condition"]["type"], "COMPARISON")
        self.assertEqual(result["condition"]["operator"], ">")
        self.assertEqual(result["then_block"]["type"], "BLOCK")
        self.assertEqual(len(result["then_block"]["statements"]), 1)
        self.assertEqual(result["else_block"]["type"], "BLOCK")
        self.assertEqual(len(result["else_block"]["statements"]), 1)
        self.assertEqual(result["line"], 7)
        self.assertEqual(result["column"], 3)


if __name__ == "__main__":
    unittest.main()

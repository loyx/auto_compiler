# === std / third-party imports ===
import unittest
from typing import Any, Dict
from unittest.mock import patch, MagicMock
import sys

# === Mock _parse_expression before importing to avoid missing dependency chain ===
_mock_parse_expression = MagicMock()
sys.modules['main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_expression_src'] = MagicMock()
sys.modules['main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_return_stmt_package._parse_expression_package'] = MagicMock()

# === sub function imports ===
from ._peek_token_package._peek_token_src import _peek_token
from ._consume_token_package._consume_token_src import _consume_token
from ._parse_return_stmt_src import _parse_return_stmt

# Import _parse_expression after setting up mocks
from ._parse_expression_package._parse_expression_src import _parse_expression

# === Module paths for patching ===
# These are the paths where the functions are imported and used in _parse_return_stmt_src
_PEEK_TOKEN_PATH = 'main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_return_stmt_package._parse_return_stmt_src._peek_token'
_CONSUME_TOKEN_PATH = 'main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_return_stmt_package._parse_return_stmt_src._consume_token'
_PARSE_EXPRESSION_PATH = 'main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_return_stmt_package._parse_return_stmt_src._parse_expression'

# === Type Aliases ===
Token = Dict[str, Any]
AST = Dict[str, Any]
ParserState = Dict[str, Any]


class TestParseReturnStmt(unittest.TestCase):
    """Test cases for _parse_return_stmt function."""

    def _create_token(self, token_type: str, value: str, line: int = 1, column: int = 1) -> Token:
        """Helper to create a token dictionary."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def _create_parser_state(self, tokens: list, pos: int = 0, filename: str = "test.py") -> ParserState:
        """Helper to create a parser state dictionary."""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename,
            "error": ""
        }

    def test_return_stmt_no_expression(self):
        """Test return statement without expression: return;"""
        tokens = [
            self._create_token("RETURN", "return", 1, 1),
            self._create_token("SEMICOLON", ";", 1, 7)
        ]
        parser_state = self._create_parser_state(tokens, 0)

        with patch(_PEEK_TOKEN_PATH, side_effect=[
            self._create_token("RETURN", "return", 1, 1),  # _parse_return_stmt first peek
            self._create_token("SEMICOLON", ";", 1, 7)     # _parse_return_stmt second peek (after consuming RETURN)
        ]) as mock_peek, patch(_CONSUME_TOKEN_PATH, side_effect=[
            self._create_parser_state(tokens, 1),  # after consuming RETURN
            self._create_parser_state(tokens, 2)   # after consuming SEMICOLON
        ]) as mock_consume, patch(_PARSE_EXPRESSION_PATH) as mock_parse_expr:
            
            result = _parse_return_stmt(parser_state)

            self.assertEqual(result["type"], "RETURN_STMT")
            self.assertEqual(result["children"], [])
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)

            mock_parse_expr.assert_not_called()
            self.assertEqual(mock_consume.call_count, 2)

    def test_return_stmt_with_expression(self):
        """Test return statement with expression: return x + 1;"""
        tokens = [
            self._create_token("RETURN", "return", 2, 5),
            self._create_token("IDENTIFIER", "x", 2, 12),
            self._create_token("PLUS", "+", 2, 14),
            self._create_token("NUMBER", "1", 2, 16),
            self._create_token("SEMICOLON", ";", 2, 17)
        ]
        parser_state = self._create_parser_state(tokens, 0)

        expr_ast = {
            "type": "BINARY_EXPR",
            "children": [],
            "value": "x + 1",
            "line": 2,
            "column": 12
        }

        with patch.object(_peek_token, '__call__', side_effect=[
            self._create_token("RETURN", "return", 2, 5),
            self._create_token("IDENTIFIER", "x", 2, 12)
        ]) as mock_peek, patch.object(_consume_token, '__call__', side_effect=[
            parser_state,
            parser_state
        ]) as mock_consume, patch.object(_parse_expression, '__call__', return_value=expr_ast) as mock_parse_expr:
            
            result = _parse_return_stmt(parser_state)

            self.assertEqual(result["type"], "RETURN_STMT")
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(result["children"][0], expr_ast)
            self.assertEqual(result["line"], 2)
            self.assertEqual(result["column"], 5)

            mock_parse_expr.assert_called_once()

    def test_return_stmt_complex_expression(self):
        """Test return statement with complex expression: return (a + b) * c;"""
        tokens = [
            self._create_token("RETURN", "return", 3, 1),
            self._create_token("LPAREN", "(", 3, 8),
            self._create_token("SEMICOLON", ";", 3, 20)
        ]
        parser_state = self._create_parser_state(tokens, 0)

        expr_ast = {
            "type": "BINARY_EXPR",
            "children": [],
            "value": "(a + b) * c",
            "line": 3,
            "column": 8
        }

        with patch.object(_peek_token, '__call__', side_effect=[
            self._create_token("RETURN", "return", 3, 1),
            self._create_token("LPAREN", "(", 3, 8)
        ]), patch.object(_consume_token, '__call__', side_effect=[
            parser_state,
            parser_state
        ]), patch.object(_parse_expression, '__call__', return_value=expr_ast):
            
            result = _parse_return_stmt(parser_state)

            self.assertEqual(result["type"], "RETURN_STMT")
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(result["children"][0]["type"], "BINARY_EXPR")

    def test_return_stmt_position_tracking(self):
        """Test that line and column are correctly tracked from RETURN token."""
        tokens = [
            self._create_token("RETURN", "return", 10, 25),
            self._create_token("SEMICOLON", ";", 10, 31)
        ]
        parser_state = self._create_parser_state(tokens, 0)

        with patch.object(_peek_token, '__call__', return_value=self._create_token("RETURN", "return", 10, 25)), \
             patch.object(_consume_token, '__call__', side_effect=[parser_state, parser_state]):
            
            result = _parse_return_stmt(parser_state)

            self.assertEqual(result["line"], 10)
            self.assertEqual(result["column"], 25)

    def test_return_stmt_multiple_children_not_allowed(self):
        """Test that return statement only has one expression child at most."""
        tokens = [
            self._create_token("RETURN", "return", 1, 1),
            self._create_token("NUMBER", "42", 1, 8),
            self._create_token("SEMICOLON", ";", 1, 10)
        ]
        parser_state = self._create_parser_state(tokens, 0)

        expr_ast = {
            "type": "NUMBER_EXPR",
            "children": [],
            "value": "42",
            "line": 1,
            "column": 8
        }

        with patch.object(_peek_token, '__call__', side_effect=[
            self._create_token("RETURN", "return", 1, 1),
            self._create_token("NUMBER", "42", 1, 8)
        ]), patch.object(_consume_token, '__call__', side_effect=[parser_state, parser_state]), \
             patch.object(_parse_expression, '__call__', return_value=expr_ast):
            
            result = _parse_return_stmt(parser_state)

            self.assertEqual(len(result["children"]), 1)
            self.assertIn(expr_ast, result["children"])

    def test_return_stmt_at_end_of_tokens(self):
        """Test return statement when peek returns None after RETURN."""
        tokens = [
            self._create_token("RETURN", "return", 1, 1)
        ]
        parser_state = self._create_parser_state(tokens, 0)

        with patch.object(_peek_token, '__call__', side_effect=[
            self._create_token("RETURN", "return", 1, 1),
            None
        ]) as mock_peek, patch.object(_consume_token, '__call__', side_effect=[
            parser_state,
            parser_state
        ]) as mock_consume:
            
            result = _parse_return_stmt(parser_state)

            self.assertEqual(result["type"], "RETURN_STMT")
            self.assertEqual(result["children"], [])

    def test_return_stmt_default_line_column(self):
        """Test that default line/column values are used when token lacks them."""
        tokens = [
            {"type": "RETURN", "value": "return"},
            {"type": "SEMICOLON", "value": ";"}
        ]
        parser_state = self._create_parser_state(tokens, 0)

        with patch.object(_peek_token, '__call__', return_value={"type": "RETURN", "value": "return"}), \
             patch.object(_consume_token, '__call__', side_effect=[parser_state, parser_state]):
            
            result = _parse_return_stmt(parser_state)

            self.assertEqual(result["line"], 0)
            self.assertEqual(result["column"], 0)

    def test_return_stmt_parser_state_propagation(self):
        """Test that parser_state is properly passed through consume calls."""
        tokens = [
            self._create_token("RETURN", "return", 1, 1),
            self._create_token("NUMBER", "1", 1, 8),
            self._create_token("SEMICOLON", ";", 1, 9)
        ]
        initial_state = self._create_parser_state(tokens, 0)
        after_return = self._create_parser_state(tokens, 1)
        after_semi = self._create_parser_state(tokens, 2)

        with patch.object(_peek_token, '__call__', side_effect=[
            self._create_token("RETURN", "return", 1, 1),
            self._create_token("NUMBER", "1", 1, 8)
        ]), patch.object(_consume_token, '__call__', side_effect=[
            after_return,
            after_semi
        ]), patch.object(_parse_expression, '__call__', return_value={
            "type": "NUMBER_EXPR",
            "children": [],
            "value": "1",
            "line": 1,
            "column": 8
        }):
            
            result = _parse_return_stmt(initial_state)

            self.assertEqual(result["type"], "RETURN_STMT")
            self.assertEqual(len(result["children"]), 1)


class TestParseReturnStmtIntegration(unittest.TestCase):
    """Integration-style tests with more realistic mock behavior."""

    def _create_token(self, token_type: str, value: str, line: int = 1, column: int = 1) -> Token:
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def _create_parser_state(self, tokens: list, pos: int = 0) -> ParserState:
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": "test.py",
            "error": ""
        }

    def test_return_with_variable_reference(self):
        """Test return with a variable reference expression."""
        tokens = [
            self._create_token("RETURN", "return", 5, 10),
            self._create_token("IDENTIFIER", "result", 5, 17),
            self._create_token("SEMICOLON", ";", 5, 23)
        ]
        parser_state = self._create_parser_state(tokens, 0)

        expr_ast = {
            "type": "IDENTIFIER_EXPR",
            "children": [],
            "value": "result",
            "line": 5,
            "column": 17
        }

        with patch.object(_peek_token, '__call__', side_effect=[
            self._create_token("RETURN", "return", 5, 10),
            self._create_token("IDENTIFIER", "result", 5, 17)
        ]), patch.object(_consume_token, '__call__', side_effect=[
            self._create_parser_state(tokens, 1),
            self._create_parser_state(tokens, 2)
        ]), patch.object(_parse_expression, '__call__', return_value=expr_ast):
            
            result = _parse_return_stmt(parser_state)

            self.assertEqual(result["type"], "RETURN_STMT")
            self.assertEqual(result["line"], 5)
            self.assertEqual(result["column"], 10)
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(result["children"][0]["value"], "result")

    def test_return_with_function_call(self):
        """Test return with a function call expression."""
        tokens = [
            self._create_token("RETURN", "return", 7, 3),
            self._create_token("IDENTIFIER", "getValue", 7, 10),
            self._create_token("SEMICOLON", ";", 7, 20)
        ]
        parser_state = self._create_parser_state(tokens, 0)

        expr_ast = {
            "type": "CALL_EXPR",
            "children": [],
            "value": "getValue()",
            "line": 7,
            "column": 10
        }

        with patch.object(_peek_token, '__call__', side_effect=[
            self._create_token("RETURN", "return", 7, 3),
            self._create_token("IDENTIFIER", "getValue", 7, 10)
        ]), patch.object(_consume_token, '__call__', side_effect=[
            self._create_parser_state(tokens, 1),
            self._create_parser_state(tokens, 2)
        ]), patch.object(_parse_expression, '__call__', return_value=expr_ast):
            
            result = _parse_return_stmt(parser_state)

            self.assertEqual(result["type"], "RETURN_STMT")
            self.assertEqual(result["children"][0]["type"], "CALL_EXPR")


if __name__ == "__main__":
    unittest.main()

# === std / third-party imports ===
import unittest
from unittest.mock import patch, MagicMock
from typing import Dict, Any, List

# === relative imports ===
from ._parse_or_src import _parse_or, _current_token_is_or

# === Type aliases ===
Token = Dict[str, Any]
AST = Dict[str, Any]
ParserState = Dict[str, Any]


class TestParseOr(unittest.TestCase):
    """Test cases for _parse_or function."""

    def _create_token(self, token_type: str, value: str = "", line: int = 1, column: int = 1) -> Token:
        """Helper to create a token dict."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def _create_parser_state(self, tokens: List[Token], pos: int = 0, filename: str = "test.txt") -> ParserState:
        """Helper to create a parser state dict."""
        return {
            "tokens": tokens,
            "filename": filename,
            "pos": pos,
            "error": ""
        }

    def _create_ast_node(self, node_type: str, **kwargs) -> AST:
        """Helper to create an AST node dict."""
        node = {"type": node_type}
        node.update(kwargs)
        return node

    @patch('._parse_or_src._parse_and')
    @patch('._parse_or_src._current_token_is_or', return_value=False)
    def test_parse_or_single_expression_no_or(self, mock_is_or: MagicMock, mock_parse_and: MagicMock):
        """Test parsing a single expression without OR operator."""
        # Arrange
        left_ast = self._create_ast_node("IDENT", value="x", line=1, column=1)
        mock_parse_and.return_value = left_ast
        
        parser_state = self._create_parser_state([
            self._create_token("IDENT", "x")
        ])
        
        # Act
        result = _parse_or(parser_state)
        
        # Assert
        self.assertEqual(result, left_ast)
        mock_parse_and.assert_called_once_with(parser_state)
        mock_is_or.assert_called_once_with(parser_state)

    @patch('._parse_or_src._parse_and')
    @patch('._parse_or_src._expect_token')
    @patch('._parse_or_src._current_token_is_or')
    def test_parse_or_single_or_expression(self, mock_is_or: MagicMock, mock_expect_token: MagicMock, mock_parse_and: MagicMock):
        """Test parsing a single OR expression (a OR b)."""
        # Arrange
        left_ast = self._create_ast_node("IDENT", value="a", line=1, column=1)
        right_ast = self._create_ast_node("IDENT", value="b", line=1, column=5)
        or_token = self._create_token("OR", "or", line=1, column=3)
        
        mock_parse_and.side_effect = [left_ast, right_ast]
        mock_expect_token.return_value = or_token
        mock_is_or.side_effect = [True, False]  # First call True, second call False
        
        parser_state = self._create_parser_state([
            self._create_token("IDENT", "a", 1, 1),
            self._create_token("OR", "or", 1, 3),
            self._create_token("IDENT", "b", 1, 5)
        ])
        
        # Act
        result = _parse_or(parser_state)
        
        # Assert
        self.assertEqual(result["type"], "BINOP")
        self.assertEqual(result["op"], "or")
        self.assertEqual(result["left"], left_ast)
        self.assertEqual(result["right"], right_ast)
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 3)
        self.assertEqual(result["children"], [left_ast, right_ast])
        
        self.assertEqual(mock_parse_and.call_count, 2)
        mock_expect_token.assert_called_once_with(parser_state, "OR")

    @patch('._parse_or_src._parse_and')
    @patch('._parse_or_src._expect_token')
    @patch('._parse_or_src._current_token_is_or')
    def test_parse_or_multiple_or_left_associative(self, mock_is_or: MagicMock, mock_expect_token: MagicMock, mock_parse_and: MagicMock):
        """Test parsing multiple OR expressions with left-associativity (a OR b OR c)."""
        # Arrange
        ast_a = self._create_ast_node("IDENT", value="a", line=1, column=1)
        ast_b = self._create_ast_node("IDENT", value="b", line=1, column=5)
        ast_c = self._create_ast_node("IDENT", value="c", line=1, column=9)
        
        or_token_1 = self._create_token("OR", "or", line=1, column=3)
        or_token_2 = self._create_token("OR", "or", line=1, column=7)
        
        mock_parse_and.side_effect = [ast_a, ast_b, ast_c]
        mock_expect_token.side_effect = [or_token_1, or_token_2]
        mock_is_or.side_effect = [True, True, False]  # Three calls
        
        parser_state = self._create_parser_state([
            self._create_token("IDENT", "a", 1, 1),
            self._create_token("OR", "or", 1, 3),
            self._create_token("IDENT", "b", 1, 5),
            self._create_token("OR", "or", 1, 7),
            self._create_token("IDENT", "c", 1, 9)
        ])
        
        # Act
        result = _parse_or(parser_state)
        
        # Assert - Left associative: (a OR b) OR c
        self.assertEqual(result["type"], "BINOP")
        self.assertEqual(result["op"], "or")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 7)  # Second OR token position
        
        # Left should be (a OR b)
        left_node = result["left"]
        self.assertEqual(left_node["type"], "BINOP")
        self.assertEqual(left_node["op"], "or")
        self.assertEqual(left_node["left"], ast_a)
        self.assertEqual(left_node["right"], ast_b)
        self.assertEqual(left_node["line"], 1)
        self.assertEqual(left_node["column"], 3)
        
        # Right should be c
        self.assertEqual(result["right"], ast_c)
        
        self.assertEqual(mock_parse_and.call_count, 3)
        self.assertEqual(mock_expect_token.call_count, 2)

    @patch('._parse_or_src._parse_and')
    @patch('._parse_or_src._current_token_is_or', return_value=False)
    def test_parse_or_empty_tokens(self, mock_is_or: MagicMock, mock_parse_and: MagicMock):
        """Test parsing with empty token list."""
        # Arrange
        empty_ast = self._create_ast_node("EMPTY")
        mock_parse_and.return_value = empty_ast
        
        parser_state = self._create_parser_state([], pos=0)
        
        # Act
        result = _parse_or(parser_state)
        
        # Assert
        self.assertEqual(result, empty_ast)
        mock_parse_and.assert_called_once_with(parser_state)

    @patch('._parse_or_src._parse_and')
    @patch('._parse_or_src._expect_token')
    @patch('._parse_or_src._current_token_is_or')
    def test_parse_or_or_at_end_raises_error(self, mock_is_or: MagicMock, mock_expect_token: MagicMock, mock_parse_and: MagicMock):
        """Test that OR at end without right operand raises error from _expect_token."""
        # Arrange
        left_ast = self._create_ast_node("IDENT", value="a", line=1, column=1)
        mock_parse_and.return_value = left_ast
        mock_is_or.return_value = True
        mock_expect_token.side_effect = SyntaxError("Expected OR token but reached end")
        
        parser_state = self._create_parser_state([
            self._create_token("IDENT", "a", 1, 1),
            self._create_token("OR", "or", 1, 3)
        ], pos=1)
        
        # Act & Assert
        with self.assertRaises(SyntaxError):
            _parse_or(parser_state)
        
        mock_expect_token.assert_called_once_with(parser_state, "OR")

    @patch('._parse_or_src._parse_and')
    @patch('._parse_or_src._expect_token')
    @patch('._parse_or_src._current_token_is_or')
    def test_parse_or_preserves_position_updates(self, mock_is_or: MagicMock, mock_expect_token: MagicMock, mock_parse_and: MagicMock):
        """Test that parser state position is updated by child functions."""
        # Arrange
        ast_a = self._create_ast_node("IDENT", value="a", line=1, column=1)
        ast_b = self._create_ast_node("IDENT", value="b", line=1, column=5)
        or_token = self._create_token("OR", "or", line=1, column=3)
        
        mock_parse_and.side_effect = [ast_a, ast_b]
        mock_expect_token.return_value = or_token
        mock_is_or.side_effect = [True, False]
        
        parser_state = self._create_parser_state([
            self._create_token("IDENT", "a", 1, 1),
            self._create_token("OR", "or", 1, 3),
            self._create_token("IDENT", "b", 1, 5)
        ], pos=0)
        
        # Act
        result = _parse_or(parser_state)
        
        # Assert
        self.assertEqual(result["type"], "BINOP")
        # Verify _parse_and was called twice (for left and right operands)
        self.assertEqual(mock_parse_and.call_count, 2)


class TestCurrentTokenIsOr(unittest.TestCase):
    """Test cases for _current_token_is_or helper function."""

    def _create_token(self, token_type: str, value: str = "", line: int = 1, column: int = 1) -> Token:
        """Helper to create a token dict."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def _create_parser_state(self, tokens: List[Token], pos: int = 0) -> ParserState:
        """Helper to create a parser state dict."""
        return {
            "tokens": tokens,
            "filename": "test.txt",
            "pos": pos,
            "error": ""
        }

    def test_current_token_is_or_true(self):
        """Test when current token is OR."""
        parser_state = self._create_parser_state([
            self._create_token("OR", "or")
        ], pos=0)
        
        result = _current_token_is_or(parser_state)
        
        self.assertTrue(result)

    def test_current_token_is_or_false_different_type(self):
        """Test when current token is not OR."""
        parser_state = self._create_parser_state([
            self._create_token("AND", "and")
        ], pos=0)
        
        result = _current_token_is_or(parser_state)
        
        self.assertFalse(result)

    def test_current_token_is_or_false_empty_tokens(self):
        """Test when token list is empty."""
        parser_state = self._create_parser_state([], pos=0)
        
        result = _current_token_is_or(parser_state)
        
        self.assertFalse(result)

    def test_current_token_is_or_false_pos_at_end(self):
        """Test when pos is at or beyond token list length."""
        parser_state = self._create_parser_state([
            self._create_token("IDENT", "x")
        ], pos=1)
        
        result = _current_token_is_or(parser_state)
        
        self.assertFalse(result)

    def test_current_token_is_or_false_pos_beyond_end(self):
        """Test when pos is beyond token list length."""
        parser_state = self._create_parser_state([
            self._create_token("IDENT", "x")
        ], pos=5)
        
        result = _current_token_is_or(parser_state)
        
        self.assertFalse(result)

    def test_current_token_is_or_true_in_middle(self):
        """Test when OR token is in the middle of token list."""
        parser_state = self._create_parser_state([
            self._create_token("IDENT", "a"),
            self._create_token("OR", "or"),
            self._create_token("IDENT", "b")
        ], pos=1)
        
        result = _current_token_is_or(parser_state)
        
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()

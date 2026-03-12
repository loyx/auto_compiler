import unittest
from unittest.mock import patch
from typing import Dict, Any

from ._parse_expression_src import _parse_expression, _current_token, _expect

ParserState = Dict[str, Any]
AST = Dict[str, Any]
Token = Dict[str, Any]


class TestParseExpression(unittest.TestCase):
    """Test cases for _parse_expression function."""

    def test_delegates_to_parse_logical_or(self):
        """Test that _parse_expression delegates to _parse_logical_or."""
        mock_ast: AST = {"type": "BINARY_OP", "value": "||"}
        mock_state: ParserState = {"tokens": [], "pos": 0}

        with patch("._parse_logical_or_package._parse_logical_or_src._parse_logical_or") as mock_parse:
            mock_parse.return_value = mock_ast
            result = _parse_expression(mock_state)

            mock_parse.assert_called_once_with(mock_state)
            self.assertEqual(result, mock_ast)

    def test_returns_ast_from_logical_or(self):
        """Test that _parse_expression returns the AST from _parse_logical_or."""
        mock_ast: AST = {"type": "IDENTIFIER", "value": "x"}
        mock_state: ParserState = {"tokens": [{"type": "IDENTIFIER", "value": "x"}], "pos": 0}

        with patch("._parse_logical_or_package._parse_logical_or_src._parse_logical_or") as mock_parse:
            mock_parse.return_value = mock_ast
            result = _parse_expression(mock_state)

            self.assertEqual(result, mock_ast)

    def test_parser_state_position_updated(self):
        """Test that parser state position is updated by _parse_logical_or."""
        mock_ast: AST = {"type": "LITERAL", "value": 42}
        mock_state: ParserState = {"tokens": [{"type": "NUMBER", "value": "42"}], "pos": 0}

        def update_position(state: ParserState) -> AST:
            state["pos"] = 1
            return mock_ast

        with patch("._parse_logical_or_package._parse_logical_or_src._parse_logical_or") as mock_parse:
            mock_parse.side_effect = update_position
            _parse_expression(mock_state)

            self.assertEqual(mock_state["pos"], 1)

    def test_propagates_exception_from_logical_or(self):
        """Test that _parse_expression propagates exceptions from _parse_logical_or."""
        mock_state: ParserState = {"tokens": [], "pos": 0}

        with patch("._parse_logical_or_package._parse_logical_or_src._parse_logical_or") as mock_parse:
            mock_parse.side_effect = SyntaxError("Unexpected token")

            with self.assertRaises(SyntaxError) as context:
                _parse_expression(mock_state)

            self.assertEqual(str(context.exception), "Unexpected token")


class TestCurrentToken(unittest.TestCase):
    """Test cases for _current_token helper function."""

    def test_returns_token_when_available(self):
        """Test _current_token returns the current token."""
        token: Token = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        state: ParserState = {"tokens": [token], "pos": 0}

        result = _current_token(state)
        self.assertEqual(result, token)

    def test_returns_none_when_pos_exceeds_tokens(self):
        """Test _current_token returns None when pos is beyond tokens."""
        state: ParserState = {"tokens": [{"type": "IDENTIFIER", "value": "x"}], "pos": 1}

        result = _current_token(state)
        self.assertIsNone(result)

    def test_returns_none_when_tokens_empty(self):
        """Test _current_token returns None when tokens list is empty."""
        state: ParserState = {"tokens": [], "pos": 0}

        result = _current_token(state)
        self.assertIsNone(result)

    def test_returns_token_at_current_position(self):
        """Test _current_token returns token at current pos, not always first."""
        token1: Token = {"type": "IDENTIFIER", "value": "x"}
        token2: Token = {"type": "NUMBER", "value": "42"}
        state: ParserState = {"tokens": [token1, token2], "pos": 1}

        result = _current_token(state)
        self.assertEqual(result, token2)

    def test_does_not_modify_state(self):
        """Test _current_token does not modify parser state."""
        token: Token = {"type": "IDENTIFIER", "value": "x"}
        state: ParserState = {"tokens": [token], "pos": 0}
        original_pos = state["pos"]

        _current_token(state)

        self.assertEqual(state["pos"], original_pos)


class TestExpect(unittest.TestCase):
    """Test cases for _expect helper function."""

    def test_consumes_token_when_type_matches(self):
        """Test _expect consumes token when type matches."""
        token: Token = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        state: ParserState = {"tokens": [token], "pos": 0}

        result = _expect(state, "IDENTIFIER")

        self.assertEqual(result, token)
        self.assertEqual(state["pos"], 1)

    def test_raises_syntax_error_when_type_mismatches(self):
        """Test _expect raises SyntaxError when token type doesn't match."""
        token: Token = {"type": "NUMBER", "value": "42", "line": 1, "column": 1}
        state: ParserState = {"tokens": [token], "pos": 0}

        with self.assertRaises(SyntaxError) as context:
            _expect(state, "IDENTIFIER")

        self.assertIn("Expected IDENTIFIER", str(context.exception))
        self.assertEqual(state["pos"], 0)

    def test_raises_syntax_error_when_no_tokens(self):
        """Test _expect raises SyntaxError when no tokens available."""
        state: ParserState = {"tokens": [], "pos": 0}

        with self.assertRaises(SyntaxError) as context:
            _expect(state, "IDENTIFIER")

        self.assertIn("Expected IDENTIFIER", str(context.exception))

    def test_raises_syntax_error_when_pos_beyond_tokens(self):
        """Test _expect raises SyntaxError when pos is beyond tokens."""
        state: ParserState = {"tokens": [{"type": "IDENTIFIER", "value": "x"}], "pos": 1}

        with self.assertRaises(SyntaxError) as context:
            _expect(state, "IDENTIFIER")

        self.assertIn("Expected IDENTIFIER", str(context.exception))

    def test_consumes_and_returns_correct_token(self):
        """Test _expect returns the consumed token with all fields."""
        token: Token = {"type": "LPAREN", "value": "(", "line": 5, "column": 10}
        state: ParserState = {"tokens": [token], "pos": 0}

        result = _expect(state, "LPAREN")

        self.assertEqual(result["type"], "LPAREN")
        self.assertEqual(result["value"], "(")
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 10)

    def test_does_not_consume_on_mismatch(self):
        """Test _expect does not consume token when type doesn't match."""
        token1: Token = {"type": "NUMBER", "value": "42"}
        token2: Token = {"type": "IDENTIFIER", "value": "x"}
        state: ParserState = {"tokens": [token1, token2], "pos": 0}

        with self.assertRaises(SyntaxError):
            _expect(state, "IDENTIFIER")

        self.assertEqual(state["pos"], 0)


if __name__ == "__main__":
    unittest.main()

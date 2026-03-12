"""Unit tests for _parse_or_expression function."""
import sys
from unittest.mock import MagicMock, patch

# Pre-mock the _parse_and_expression module to avoid deep import chain
mock_parse_and = MagicMock()
sys.modules['._parse_and_expression_package._parse_and_expression_src'] = MagicMock()
sys.modules['._parse_and_expression_package._parse_and_expression_src']._parse_and_expression = mock_parse_and

from ._parse_or_expression_src import _parse_or_expression


class TestParseOrExpression:
    """Test cases for _parse_or_expression function."""

    def test_single_and_expression_no_or(self):
        """Test parsing a single AND expression without OR operator."""
        parser_state = {
            "tokens": [{"type": "NUMBER", "value": "1", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test.cc"
        }

        mock_and_ast = {"type": "number", "value": "1", "line": 1, "column": 1}

        with patch("._parse_and_expression_package._parse_and_expression_src._parse_and_expression") as mock_parse_and:
            mock_parse_and.return_value = mock_and_ast

            result = _parse_or_expression(parser_state)

            assert result == mock_and_ast
            mock_parse_and.assert_called_once_with(parser_state)
            assert parser_state["pos"] == 0

    def test_multiple_or_operators_left_associative(self):
        """Test parsing multiple OR operators with left associativity."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "OR", "value": "or", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 6},
                {"type": "OR", "value": "OR", "line": 1, "column": 8},
                {"type": "NUMBER", "value": "3", "line": 1, "column": 11},
            ],
            "pos": 0,
            "filename": "test.cc"
        }

        mock_ast_1 = {"type": "number", "value": "1", "line": 1, "column": 1}
        mock_ast_2 = {"type": "number", "value": "2", "line": 1, "column": 6}
        mock_ast_3 = {"type": "number", "value": "3", "line": 1, "column": 11}

        with patch("._parse_and_expression_package._parse_and_expression_src._parse_and_expression") as mock_parse_and:
            mock_parse_and.side_effect = [mock_ast_1, mock_ast_2, mock_ast_3]

            result = _parse_or_expression(parser_state)

            expected = {
                "type": "binary_op",
                "operator": "or",
                "left": {
                    "type": "binary_op",
                    "operator": "or",
                    "left": mock_ast_1,
                    "right": mock_ast_2,
                    "line": 1,
                    "column": 3,
                },
                "right": mock_ast_3,
                "line": 1,
                "column": 8,
            }
            assert result == expected
            assert parser_state["pos"] == 5
            assert mock_parse_and.call_count == 3

    def test_error_after_left_and_expression(self):
        """Test that error in parser_state after left parsing is propagated."""
        parser_state = {
            "tokens": [{"type": "NUMBER", "value": "1", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test.cc",
            "error": "syntax error"
        }

        mock_and_ast = {"type": "error", "message": "syntax error"}

        with patch("._parse_or_expression_package._parse_and_expression_package._parse_and_expression_src._parse_and_expression") as mock_parse_and:
            mock_parse_and.return_value = mock_and_ast

            result = _parse_or_expression(parser_state)

            assert result == mock_and_ast
            mock_parse_and.assert_called_once_with(parser_state)

    def test_error_after_right_and_expression(self):
        """Test that error after right parsing returns left AST without building OR node."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "OR", "value": "or", "line": 1, "column": 3},
            ],
            "pos": 0,
            "filename": "test.cc"
        }

        mock_left_ast = {"type": "number", "value": "1", "line": 1, "column": 1}
        mock_right_ast = {"type": "error", "message": "unexpected end"}

        with patch("._parse_or_expression_package._parse_and_expression_package._parse_and_expression_src._parse_and_expression") as mock_parse_and:
            mock_parse_and.side_effect = [mock_left_ast, mock_right_ast]

            result = _parse_or_expression(parser_state)

            assert result == mock_left_ast
            assert parser_state["pos"] == 1
            assert mock_parse_and.call_count == 2

    def test_empty_tokens(self):
        """Test parsing with empty token list."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.cc"
        }

        mock_and_ast = {"type": "empty", "value": None}

        with patch("._parse_or_expression_package._parse_and_expression_package._parse_and_expression_src._parse_and_expression") as mock_parse_and:
            mock_parse_and.return_value = mock_and_ast

            result = _parse_or_expression(parser_state)

            assert result == mock_and_ast
            assert parser_state["pos"] == 0

    def test_position_at_end(self):
        """Test parsing when position is already at end of tokens."""
        parser_state = {
            "tokens": [{"type": "NUMBER", "value": "1", "line": 1, "column": 1}],
            "pos": 1,
            "filename": "test.cc"
        }

        mock_and_ast = {"type": "number", "value": "1", "line": 1, "column": 1}

        with patch("._parse_or_expression_package._parse_and_expression_package._parse_and_expression_src._parse_and_expression") as mock_parse_and:
            mock_parse_and.return_value = mock_and_ast

            result = _parse_or_expression(parser_state)

            assert result == mock_and_ast
            assert parser_state["pos"] == 1

    def test_or_token_by_value_uppercase(self):
        """Test OR detection by value (uppercase OR)."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "OR", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 6},
            ],
            "pos": 0,
            "filename": "test.cc"
        }

        mock_ast_a = {"type": "identifier", "value": "a", "line": 1, "column": 1}
        mock_ast_b = {"type": "identifier", "value": "b", "line": 1, "column": 6}

        with patch("._parse_or_expression_package._parse_and_expression_package._parse_and_expression_src._parse_and_expression") as mock_parse_and:
            mock_parse_and.side_effect = [mock_ast_a, mock_ast_b]

            result = _parse_or_expression(parser_state)

            expected = {
                "type": "binary_op",
                "operator": "or",
                "left": mock_ast_a,
                "right": mock_ast_b,
                "line": 1,
                "column": 3,
            }
            assert result == expected
            assert parser_state["pos"] == 3

    def test_or_token_by_type(self):
        """Test OR detection by token type."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "OR", "value": "||", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "0", "line": 1, "column": 6},
            ],
            "pos": 0,
            "filename": "test.cc"
        }

        mock_ast_1 = {"type": "number", "value": "1", "line": 1, "column": 1}
        mock_ast_0 = {"type": "number", "value": "0", "line": 1, "column": 6}

        with patch("._parse_or_expression_package._parse_and_expression_package._parse_and_expression_src._parse_and_expression") as mock_parse_and:
            mock_parse_and.side_effect = [mock_ast_1, mock_ast_0]

            result = _parse_or_expression(parser_state)

            expected = {
                "type": "binary_op",
                "operator": "or",
                "left": mock_ast_1,
                "right": mock_ast_0,
                "line": 1,
                "column": 3,
            }
            assert result == expected
            assert parser_state["pos"] == 3

    def test_non_or_token_stops_loop(self):
        """Test that non-OR token stops the OR parsing loop."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "AND", "value": "and", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "0", "line": 1, "column": 7},
            ],
            "pos": 0,
            "filename": "test.cc"
        }

        mock_ast_1 = {"type": "number", "value": "1", "line": 1, "column": 1}

        with patch("._parse_or_expression_package._parse_and_expression_package._parse_and_expression_src._parse_and_expression") as mock_parse_and:
            mock_parse_and.return_value = mock_ast_1

            result = _parse_or_expression(parser_state)

            assert result == mock_ast_1
            assert parser_state["pos"] == 0
            mock_parse_and.assert_called_once()

    def test_missing_token_fields_handled_gracefully(self):
        """Test that missing line/column fields are handled with defaults."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1"},
                {"type": "OR", "value": "or"},
                {"type": "NUMBER", "value": "2"},
            ],
            "pos": 0,
            "filename": "test.cc"
        }

        mock_ast_1 = {"type": "number", "value": "1"}
        mock_ast_2 = {"type": "number", "value": "2"}

        with patch("._parse_or_expression_package._parse_and_expression_package._parse_and_expression_src._parse_and_expression") as mock_parse_and:
            mock_parse_and.side_effect = [mock_ast_1, mock_ast_2]

            result = _parse_or_expression(parser_state)

            expected = {
                "type": "binary_op",
                "operator": "or",
                "left": mock_ast_1,
                "right": mock_ast_2,
                "line": 0,
                "column": 0,
            }
            assert result == expected
            assert parser_state["pos"] == 3

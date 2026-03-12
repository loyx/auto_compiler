# -*- coding: utf-8 -*-
"""Unit tests for _parse_expression function."""

import pytest
from unittest.mock import patch

from ._parse_expression_src import _parse_expression


def _make_token(type_: str, value: str, line: int = 1, column: int = 1) -> dict:
    """Helper to create a token dict."""
    return {"type": type_, "value": value, "line": line, "column": column}


def _make_parser_state(tokens: list, pos: int = 0, filename: str = "test.py") -> dict:
    """Helper to create a parser state dict."""
    return {"tokens": tokens, "pos": pos, "filename": filename}


class TestParseExpressionEmpty:
    """Test cases for empty or end-of-input scenarios."""

    def test_empty_tokens_raises_syntax_error(self):
        """Empty token list should raise SyntaxError."""
        parser_state = _make_parser_state([], pos=0)
        with pytest.raises(SyntaxError) as exc_info:
            _parse_expression(parser_state)
        assert "Unexpected end of input" in str(exc_info.value)
        assert "test.py:0:0" in str(exc_info.value)

    def test_pos_beyond_tokens_raises_syntax_error(self):
        """Position beyond token list should raise SyntaxError."""
        tokens = [_make_token("NUMBER", "5")]
        parser_state = _make_parser_state(tokens, pos=1)
        with pytest.raises(SyntaxError) as exc_info:
            _parse_expression(parser_state)
        assert "Unexpected end of input" in str(exc_info.value)


class TestParseExpressionPrimary:
    """Test cases for primary expression parsing."""

    @patch("._parse_expression_src._parse_primary")
    @patch("._parse_expression_src._parse_binary_op")
    def test_simple_number_returns_primary(self, mock_binary_op, mock_primary):
        """Simple number expression should return primary result."""
        token = _make_token("NUMBER", "42")
        tokens = [token]
        parser_state = _make_parser_state(tokens, pos=0)
        
        expected_ast = {"type": "NUMBER", "value": "42", "line": 1, "column": 1}
        mock_primary.return_value = expected_ast
        mock_binary_op.return_value = expected_ast
        
        result = _parse_expression(parser_state)
        
        mock_primary.assert_called_once_with(parser_state)
        mock_binary_op.assert_called_once_with(parser_state, 0, expected_ast)
        assert result == expected_ast

    @patch("._parse_expression_src._parse_primary")
    @patch("._parse_expression_src._parse_binary_op")
    def test_simple_identifier_returns_primary(self, mock_binary_op, mock_primary):
        """Simple identifier expression should return primary result."""
        token = _make_token("IDENTIFIER", "x")
        tokens = [token]
        parser_state = _make_parser_state(tokens, pos=0)
        
        expected_ast = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        mock_primary.return_value = expected_ast
        mock_binary_op.return_value = expected_ast
        
        result = _parse_expression(parser_state)
        
        mock_primary.assert_called_once_with(parser_state)
        mock_binary_op.assert_called_once_with(parser_state, 0, expected_ast)
        assert result == expected_ast

    @patch("._parse_expression_src._parse_primary")
    @patch("._parse_expression_src._parse_binary_op")
    def test_string_literal_returns_primary(self, mock_binary_op, mock_primary):
        """String literal expression should return primary result."""
        token = _make_token("STRING", '"hello"')
        tokens = [token]
        parser_state = _make_parser_state(tokens, pos=0)
        
        expected_ast = {"type": "STRING", "value": '"hello"', "line": 1, "column": 1}
        mock_primary.return_value = expected_ast
        mock_binary_op.return_value = expected_ast
        
        result = _parse_expression(parser_state)
        
        mock_primary.assert_called_once_with(parser_state)
        mock_binary_op.assert_called_once_with(parser_state, 0, expected_ast)
        assert result == expected_ast


class TestParseExpressionFunctionCall:
    """Test cases for function call parsing."""

    @patch("._parse_expression_src._parse_primary")
    @patch("._parse_expression_src._parse_call_args")
    def test_function_call_no_args(self, mock_call_args, mock_primary):
        """Function call with no arguments."""
        tokens = [
            _make_token("IDENTIFIER", "func", line=1, column=1),
            _make_token("LPAREN", "(", line=1, column=5),
            _make_token("RPAREN", ")", line=1, column=6),
        ]
        parser_state = _make_parser_state(tokens, pos=0)
        
        identifier_ast = {"type": "IDENTIFIER", "value": "func", "line": 1, "column": 1}
        mock_primary.return_value = identifier_ast
        mock_call_args.return_value = []
        
        result = _parse_expression(parser_state)
        
        mock_primary.assert_called_once_with(parser_state)
        mock_call_args.assert_called_once_with(parser_state)
        assert parser_state["pos"] == 3  # consumed all tokens
        assert result["type"] == "CALL"
        assert result["value"] == "func"
        assert result["children"] == []
        assert result["line"] == 1
        assert result["column"] == 1

    @patch("._parse_expression_src._parse_primary")
    @patch("._parse_expression_src._parse_call_args")
    def test_function_call_with_args(self, mock_call_args, mock_primary):
        """Function call with arguments."""
        tokens = [
            _make_token("IDENTIFIER", "func", line=1, column=1),
            _make_token("LPAREN", "(", line=1, column=5),
            _make_token("NUMBER", "1", line=1, column=6),
            _make_token("COMMA", ",", line=1, column=7),
            _make_token("NUMBER", "2", line=1, column=8),
            _make_token("RPAREN", ")", line=1, column=9),
        ]
        parser_state = _make_parser_state(tokens, pos=0)
        
        identifier_ast = {"type": "IDENTIFIER", "value": "func", "line": 1, "column": 1}
        mock_primary.return_value = identifier_ast
        arg1 = {"type": "NUMBER", "value": "1", "line": 1, "column": 6}
        arg2 = {"type": "NUMBER", "value": "2", "line": 1, "column": 8}
        mock_call_args.return_value = [arg1, arg2]
        
        result = _parse_expression(parser_state)
        
        mock_primary.assert_called_once_with(parser_state)
        mock_call_args.assert_called_once_with(parser_state)
        assert parser_state["pos"] == 6  # consumed all tokens
        assert result["type"] == "CALL"
        assert result["value"] == "func"
        assert len(result["children"]) == 2

    @patch("._parse_expression_src._parse_primary")
    def test_function_call_missing_rparen_raises_error(self, mock_primary):
        """Function call missing closing paren should raise SyntaxError."""
        tokens = [
            _make_token("IDENTIFIER", "func", line=2, column=10),
            _make_token("LPAREN", "(", line=2, column=14),
        ]
        parser_state = _make_parser_state(tokens, pos=0)
        
        identifier_ast = {"type": "IDENTIFIER", "value": "func", "line": 2, "column": 10}
        mock_primary.return_value = identifier_ast
        
        with pytest.raises(SyntaxError) as exc_info:
            _parse_expression(parser_state)
        assert "Expected ')'" in str(exc_info.value)
        assert "2:10" in str(exc_info.value)

    @patch("._parse_expression_src._parse_primary")
    @patch("._parse_expression_src._parse_call_args")
    def test_function_call_pos_after_lparen(self, mock_call_args, mock_primary):
        """Verify pos is incremented after consuming LPAREN."""
        tokens = [
            _make_token("IDENTIFIER", "func"),
            _make_token("LPAREN", "("),
            _make_token("RPAREN", ")"),
        ]
        parser_state = _make_parser_state(tokens, pos=0)
        
        identifier_ast = {"type": "IDENTIFIER", "value": "func", "line": 1, "column": 1}
        mock_primary.return_value = identifier_ast
        mock_call_args.return_value = []
        
        # _parse_call_args should be called when pos is at LPAREN (pos=1)
        def check_pos(state):
            assert state["pos"] == 1
            state["pos"] = 2  # simulate consuming args
            return []
        mock_call_args.side_effect = check_pos
        
        result = _parse_expression(parser_state)
        
        assert result["type"] == "CALL"


class TestParseExpressionAssignment:
    """Test cases for assignment expression parsing."""

    @patch("._parse_expression_src._parse_primary")
    @patch("._parse_expression_src._parse_assignment")
    def test_assignment_expression(self, mock_assignment, mock_primary):
        """Assignment expression should call _parse_assignment."""
        tokens = [
            _make_token("IDENTIFIER", "x", line=1, column=1),
            _make_token("ASSIGN", "=", line=1, column=3),
            _make_token("NUMBER", "5", line=1, column=5),
        ]
        parser_state = _make_parser_state(tokens, pos=0)
        
        identifier_ast = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        mock_primary.return_value = identifier_ast
        
        expected_result = {
            "type": "ASSIGNMENT",
            "children": [identifier_ast, {"type": "NUMBER", "value": "5"}],
            "line": 1,
            "column": 1
        }
        mock_assignment.return_value = expected_result
        
        result = _parse_expression(parser_state)
        
        mock_primary.assert_called_once_with(parser_state)
        mock_assignment.assert_called_once_with(parser_state, identifier_ast)
        assert result == expected_result

    @patch("._parse_expression_src._parse_primary")
    @patch("._parse_expression_src._parse_assignment")
    def test_assignment_pos_at_assign_token(self, mock_assignment, mock_primary):
        """Verify _parse_assignment is called when pos is at ASSIGN token."""
        tokens = [
            _make_token("IDENTIFIER", "x"),
            _make_token("ASSIGN", "="),
            _make_token("NUMBER", "5"),
        ]
        parser_state = _make_parser_state(tokens, pos=0)
        
        identifier_ast = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        mock_primary.return_value = identifier_ast
        
        def check_pos(state, left):
            assert state["pos"] == 1  # pos should be at ASSIGN
            assert left == identifier_ast
            state["pos"] = 3
            return {"type": "ASSIGNMENT"}
        mock_assignment.side_effect = check_pos
        
        result = _parse_expression(parser_state)
        
        assert result["type"] == "ASSIGNMENT"


class TestParseExpressionBinaryOp:
    """Test cases for binary operation parsing."""

    @patch("._parse_expression_src._parse_primary")
    @patch("._parse_expression_src._parse_binary_op")
    def test_binary_expression(self, mock_binary_op, mock_primary):
        """Binary expression should call _parse_binary_op with min_precedence 0."""
        tokens = [
            _make_token("NUMBER", "1", line=1, column=1),
            _make_token("PLUS", "+", line=1, column=3),
            _make_token("NUMBER", "2", line=1, column=5),
        ]
        parser_state = _make_parser_state(tokens, pos=0)
        
        left_ast = {"type": "NUMBER", "value": "1", "line": 1, "column": 1}
        mock_primary.return_value = left_ast
        
        expected_result = {
            "type": "BINARY_OP",
            "value": "+",
            "children": [left_ast, {"type": "NUMBER", "value": "2"}],
            "line": 1,
            "column": 1
        }
        mock_binary_op.return_value = expected_result
        
        result = _parse_expression(parser_state)
        
        mock_primary.assert_called_once_with(parser_state)
        mock_binary_op.assert_called_once_with(parser_state, 0, left_ast)
        assert result == expected_result

    @patch("._parse_expression_src._parse_primary")
    @patch("._parse_expression_src._parse_binary_op")
    def test_binary_op_called_when_no_assignment(self, mock_binary_op, mock_primary):
        """_parse_binary_op should be called when no ASSIGN token follows."""
        tokens = [
            _make_token("NUMBER", "1"),
            _make_token("PLUS", "+"),
            _make_token("NUMBER", "2"),
        ]
        parser_state = _make_parser_state(tokens, pos=0)
        
        left_ast = {"type": "NUMBER", "value": "1", "line": 1, "column": 1}
        mock_primary.return_value = left_ast
        mock_binary_op.return_value = left_ast
        
        result = _parse_expression(parser_state)
        
        mock_binary_op.assert_called_once()


class TestParseExpressionPrecedence:
    """Test cases for expression precedence (call > assignment > binary op)."""

    @patch("._parse_expression_src._parse_primary")
    @patch("._parse_expression_src._parse_call_args")
    def test_function_call_takes_precedence_over_assignment(self, mock_call_args, mock_primary):
        """Function call should be parsed before checking for assignment."""
        tokens = [
            _make_token("IDENTIFIER", "func"),
            _make_token("LPAREN", "("),
            _make_token("RPAREN", ")"),
            _make_token("ASSIGN", "="),
            _make_token("NUMBER", "5"),
        ]
        parser_state = _make_parser_state(tokens, pos=0)
        
        identifier_ast = {"type": "IDENTIFIER", "value": "func", "line": 1, "column": 1}
        mock_primary.return_value = identifier_ast
        mock_call_args.return_value = []
        
        result = _parse_expression(parser_state)
        
        # Should return CALL, not ASSIGNMENT
        assert result["type"] == "CALL"
        assert result["value"] == "func"
        assert parser_state["pos"] == 3  # stopped after RPAREN

    @patch("._parse_expression_src._parse_primary")
    @patch("._parse_expression_src._parse_binary_op")
    def test_non_identifier_no_function_call(self, mock_binary_op, mock_primary):
        """Non-identifier primary should not attempt function call parsing."""
        tokens = [
            _make_token("NUMBER", "42"),
            _make_token("PLUS", "+"),
            _make_token("NUMBER", "1"),
        ]
        parser_state = _make_parser_state(tokens, pos=0)
        
        number_ast = {"type": "NUMBER", "value": "42", "line": 1, "column": 1}
        mock_primary.return_value = number_ast
        mock_binary_op.return_value = number_ast
        
        result = _parse_expression(parser_state)
        
        # _parse_call_args should not be called for NUMBER
        assert result == number_ast


class TestParseExpressionEdgeCases:
    """Edge case tests."""

    @patch("._parse_expression_src._parse_primary")
    @patch("._parse_expression_src._parse_binary_op")
    def test_single_token_expression(self, mock_binary_op, mock_primary):
        """Single token expression should work correctly."""
        tokens = [_make_token("NUMBER", "42")]
        parser_state = _make_parser_state(tokens, pos=0)
        
        expected_ast = {"type": "NUMBER", "value": "42", "line": 1, "column": 1}
        mock_primary.return_value = expected_ast
        mock_binary_op.return_value = expected_ast
        
        result = _parse_expression(parser_state)
        
        assert result == expected_ast

    @patch("._parse_expression_src._parse_primary")
    @patch("._parse_expression_src._parse_binary_op")
    def test_custom_filename_in_error(self, mock_binary_op, mock_primary):
        """Custom filename should appear in error messages."""
        tokens = []
        parser_state = _make_parser_state(tokens, pos=0, filename="custom_file.py")
        
        with pytest.raises(SyntaxError) as exc_info:
            _parse_expression(parser_state)
        assert "custom_file.py:0:0" in str(exc_info.value)

    @patch("._parse_expression_src._parse_primary")
    def test_primary_raises_error_propagates(self, mock_primary):
        """Errors from _parse_primary should propagate."""
        tokens = [_make_token("INVALID", "???")]
        parser_state = _make_parser_state(tokens, pos=0)
        
        mock_primary.side_effect = SyntaxError("Invalid token")
        
        with pytest.raises(SyntaxError) as exc_info:
            _parse_expression(parser_state)
        assert "Invalid token" in str(exc_info.value)

    @patch("._parse_expression_src._parse_primary")
    @patch("._parse_expression_src._parse_call_args")
    def test_call_args_raises_error_propagates(self, mock_call_args, mock_primary):
        """Errors from _parse_call_args should propagate."""
        tokens = [
            _make_token("IDENTIFIER", "func"),
            _make_token("LPAREN", "("),
        ]
        parser_state = _make_parser_state(tokens, pos=0)
        
        identifier_ast = {"type": "IDENTIFIER", "value": "func", "line": 1, "column": 1}
        mock_primary.return_value = identifier_ast
        mock_call_args.side_effect = SyntaxError("Invalid argument")
        
        with pytest.raises(SyntaxError) as exc_info:
            _parse_expression(parser_state)
        assert "Invalid argument" in str(exc_info.value)

    @patch("._parse_expression_src._parse_primary")
    @patch("._parse_expression_src._parse_assignment")
    def test_assignment_raises_error_propagates(self, mock_assignment, mock_primary):
        """Errors from _parse_assignment should propagate."""
        tokens = [
            _make_token("IDENTIFIER", "x"),
            _make_token("ASSIGN", "="),
        ]
        parser_state = _make_parser_state(tokens, pos=0)
        
        identifier_ast = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        mock_primary.return_value = identifier_ast
        mock_assignment.side_effect = SyntaxError("Invalid assignment")
        
        with pytest.raises(SyntaxError) as exc_info:
            _parse_expression(parser_state)
        assert "Invalid assignment" in str(exc_info.value)

    @patch("._parse_expression_src._parse_primary")
    @patch("._parse_expression_src._parse_binary_op")
    def test_binary_op_raises_error_propagates(self, mock_binary_op, mock_primary):
        """Errors from _parse_binary_op should propagate."""
        tokens = [
            _make_token("NUMBER", "1"),
            _make_token("PLUS", "+"),
        ]
        parser_state = _make_parser_state(tokens, pos=0)
        
        left_ast = {"type": "NUMBER", "value": "1", "line": 1, "column": 1}
        mock_primary.return_value = left_ast
        mock_binary_op.side_effect = SyntaxError("Invalid expression")
        
        with pytest.raises(SyntaxError) as exc_info:
            _parse_expression(parser_state)
        assert "Invalid expression" in str(exc_info.value)

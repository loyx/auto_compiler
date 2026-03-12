"""Unit tests for _parse_params function."""

import pytest
from unittest.mock import patch, MagicMock
from typing import Any, Dict
import sys

# Pre-mock the _parse_expr module to avoid import chain issues
_mock_parse_expr = MagicMock()
_mock_parse_expr_module = MagicMock()
_mock_parse_expr_module._parse_expr = _mock_parse_expr
sys.modules["main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_def_statement_package._parse_params_package._parse_expr_package._parse_expr_src"] = _mock_parse_expr_module

from ._parse_params_src import _parse_params


Token = Dict[str, Any]
ParserState = Dict[str, Any]
AST = Dict[str, Any]


def _make_token(tok_type: str, value: str = "", line: int = 1, column: int = 1) -> Token:
    """Helper to create a token."""
    return {"type": tok_type, "value": value, "line": line, "column": column}


def _make_parser_state(tokens: list, pos: int = 0, filename: str = "test.py") -> ParserState:
    """Helper to create a parser state."""
    return {"tokens": tokens, "pos": pos, "filename": filename}


class TestParseParamsEmpty:
    """Test empty parameter list."""

    def test_empty_params(self):
        """Test parsing empty parameter list ()."""
        tokens = [_make_token("RPAREN", ")", line=1, column=5)]
        parser_state = _make_parser_state(tokens, pos=0)
        
        result = _parse_params(parser_state)
        
        assert result["type"] == "PARAMS"
        assert result["children"] == []
        assert result["line"] == 0
        assert result["column"] == 0
        assert parser_state["pos"] == 0


class TestParseParamsSingle:
    """Test single parameter."""

    def test_single_param_no_default(self):
        """Test parsing single parameter without default (a)."""
        tokens = [
            _make_token("IDENT", "a", line=1, column=2),
            _make_token("RPAREN", ")", line=1, column=3)
        ]
        parser_state = _make_parser_state(tokens, pos=0)
        
        result = _parse_params(parser_state)
        
        assert result["type"] == "PARAMS"
        assert len(result["children"]) == 1
        assert result["children"][0]["type"] == "PARAM"
        assert result["children"][0]["children"][0]["type"] == "NAME"
        assert result["children"][0]["children"][0]["value"] == "a"
        assert result["line"] == 1
        assert result["column"] == 2
        assert parser_state["pos"] == 1

    def test_single_param_with_default(self):
        """Test parsing single parameter with default (a=1)."""
        tokens = [
            _make_token("IDENT", "a", line=1, column=2),
            _make_token("EQUALS", "=", line=1, column=3),
            _make_token("NUMBER", "1", line=1, column=4),
            _make_token("RPAREN", ")", line=1, column=5)
        ]
        parser_state = _make_parser_state(tokens, pos=0)
        
        def mock_parse_expr_side_effect(ps):
            ps["pos"] = 3
            return {"type": "NUMBER", "value": "1", "line": 1, "column": 4}
        
        _mock_parse_expr.side_effect = mock_parse_expr_side_effect
        try:
            result = _parse_params(parser_state)
        finally:
            _mock_parse_expr.side_effect = None
        
        assert result["type"] == "PARAMS"
        assert len(result["children"]) == 1
        assert result["children"][0]["type"] == "PARAM"
        assert len(result["children"][0]["children"]) == 2
        assert result["children"][0]["children"][0]["value"] == "a"
        assert result["children"][0]["children"][1]["type"] == "NUMBER"
        assert parser_state["pos"] == 3


class TestParseParamsMultiple:
    """Test multiple parameters."""

    def test_multiple_params_no_defaults(self):
        """Test parsing multiple parameters without defaults (a, b, c)."""
        tokens = [
            _make_token("IDENT", "a", line=1, column=2),
            _make_token("COMMA", ",", line=1, column=3),
            _make_token("IDENT", "b", line=1, column=5),
            _make_token("COMMA", ",", line=1, column=6),
            _make_token("IDENT", "c", line=1, column=8),
            _make_token("RPAREN", ")", line=1, column=9)
        ]
        parser_state = _make_parser_state(tokens, pos=0)
        
        result = _parse_params(parser_state)
        
        assert result["type"] == "PARAMS"
        assert len(result["children"]) == 3
        assert result["children"][0]["children"][0]["value"] == "a"
        assert result["children"][1]["children"][0]["value"] == "b"
        assert result["children"][2]["children"][0]["value"] == "c"
        assert parser_state["pos"] == 5

    def test_multiple_params_with_defaults(self):
        """Test parsing multiple parameters with defaults (a=1, b=2)."""
        tokens = [
            _make_token("IDENT", "a", line=1, column=2),
            _make_token("EQUALS", "=", line=1, column=3),
            _make_token("NUMBER", "1", line=1, column=4),
            _make_token("COMMA", ",", line=1, column=5),
            _make_token("IDENT", "b", line=1, column=7),
            _make_token("EQUALS", "=", line=1, column=8),
            _make_token("NUMBER", "2", line=1, column=9),
            _make_token("RPAREN", ")", line=1, column=10)
        ]
        parser_state = _make_parser_state(tokens, pos=0)
        
        call_count = [0]
        
        def mock_parse_expr_side_effect(ps):
            call_count[0] += 1
            if call_count[0] == 1:
                ps["pos"] = 3
                return {"type": "NUMBER", "value": "1", "line": 1, "column": 4}
            else:
                ps["pos"] = 7
                return {"type": "NUMBER", "value": "2", "line": 1, "column": 9}
        
        _mock_parse_expr.side_effect = mock_parse_expr_side_effect
        try:
            result = _parse_params(parser_state)
        finally:
            _mock_parse_expr.side_effect = None
        
        assert result["type"] == "PARAMS"
        assert len(result["children"]) == 2
        assert len(result["children"][0]["children"]) == 2
        assert len(result["children"][1]["children"]) == 2
        assert parser_state["pos"] == 7

    def test_mixed_params(self):
        """Test parsing mixed parameters (a, b=1, c)."""
        tokens = [
            _make_token("IDENT", "a", line=1, column=2),
            _make_token("COMMA", ",", line=1, column=3),
            _make_token("IDENT", "b", line=1, column=5),
            _make_token("EQUALS", "=", line=1, column=6),
            _make_token("NUMBER", "1", line=1, column=7),
            _make_token("COMMA", ",", line=1, column=8),
            _make_token("IDENT", "c", line=1, column=10),
            _make_token("RPAREN", ")", line=1, column=11)
        ]
        parser_state = _make_parser_state(tokens, pos=0)
        
        def mock_parse_expr_side_effect(ps):
            ps["pos"] = 5
            return {"type": "NUMBER", "value": "1", "line": 1, "column": 7}
        
        _mock_parse_expr.side_effect = mock_parse_expr_side_effect
        try:
            result = _parse_params(parser_state)
        finally:
            _mock_parse_expr.side_effect = None
        
        assert result["type"] == "PARAMS"
        assert len(result["children"]) == 3
        assert len(result["children"][0]["children"]) == 1
        assert len(result["children"][1]["children"]) == 2
        assert len(result["children"][2]["children"]) == 1
        assert parser_state["pos"] == 5


class TestParseParamsErrors:
    """Test error cases."""

    def test_comma_without_param_before(self):
        """Test error when comma appears without parameter before ()."""
        tokens = [
            _make_token("COMMA", ",", line=1, column=2),
            _make_token("RPAREN", ")", line=1, column=3)
        ]
        parser_state = _make_parser_state(tokens, pos=0)
        
        with pytest.raises(SyntaxError, match="Expected parameter before ','"):
            _parse_params(parser_state)

    def test_comma_without_param_after(self):
        """Test error when comma appears without parameter after (a,)."""
        tokens = [
            _make_token("IDENT", "a", line=1, column=2),
            _make_token("COMMA", ",", line=1, column=3),
            _make_token("RPAREN", ")", line=1, column=4)
        ]
        parser_state = _make_parser_state(tokens, pos=0)
        
        with pytest.raises(SyntaxError, match="Expected parameter after ','"):
            _parse_params(parser_state)

    def test_invalid_token_type(self):
        """Test error when invalid token type appears in parameter position."""
        tokens = [
            _make_token("NUMBER", "1", line=1, column=2),
            _make_token("RPAREN", ")", line=1, column=3)
        ]
        parser_state = _make_parser_state(tokens, pos=0)
        
        with pytest.raises(SyntaxError, match="Expected parameter name, got NUMBER"):
            _parse_params(parser_state)

    def test_missing_expression_after_equals(self):
        """Test error when expression is missing after =."""
        tokens = [
            _make_token("IDENT", "a", line=1, column=2),
            _make_token("EQUALS", "=", line=1, column=3),
            _make_token("RPAREN", ")", line=1, column=4)
        ]
        parser_state = _make_parser_state(tokens, pos=0)
        
        with pytest.raises(SyntaxError, match="Expected expression after '='"):
            _parse_params(parser_state)

    def test_invalid_token_after_param(self):
        """Test error when invalid token appears after parameter."""
        tokens = [
            _make_token("IDENT", "a", line=1, column=2),
            _make_token("NUMBER", "1", line=1, column=3),
            _make_token("RPAREN", ")", line=1, column=4)
        ]
        parser_state = _make_parser_state(tokens, pos=0)
        
        with pytest.raises(SyntaxError, match=r"Expected ',' or '\)' after parameter"):
            _parse_params(parser_state)

    def test_comma_then_invalid_token(self):
        """Test error when comma is followed by invalid token."""
        tokens = [
            _make_token("IDENT", "a", line=1, column=2),
            _make_token("COMMA", ",", line=1, column=3),
            _make_token("NUMBER", "1", line=1, column=4),
            _make_token("RPAREN", ")", line=1, column=5)
        ]
        parser_state = _make_parser_state(tokens, pos=0)
        
        with pytest.raises(SyntaxError, match="Expected parameter after ','"):
            _parse_params(parser_state)


class TestParseParamsEdgeCases:
    """Test edge cases."""

    def test_param_line_column_tracking(self):
        """Test that line and column are correctly tracked for first param."""
        tokens = [
            _make_token("IDENT", "x", line=5, column=10),
            _make_token("RPAREN", ")", line=5, column=11)
        ]
        parser_state = _make_parser_state(tokens, pos=0)
        
        result = _parse_params(parser_state)
        
        assert result["line"] == 5
        assert result["column"] == 10

    def test_empty_params_line_column_zero(self):
        """Test that empty params have line/column 0."""
        tokens = [_make_token("RPAREN", ")", line=5, column=10)]
        parser_state = _make_parser_state(tokens, pos=0)
        
        result = _parse_params(parser_state)
        
        assert result["line"] == 0
        assert result["column"] == 0

    def test_pos_updated_correctly(self):
        """Test that parser_state pos is updated to point before RPAREN."""
        tokens = [
            _make_token("IDENT", "a", line=1, column=2),
            _make_token("COMMA", ",", line=1, column=3),
            _make_token("IDENT", "b", line=1, column=5),
            _make_token("RPAREN", ")", line=1, column=6)
        ]
        parser_state = _make_parser_state(tokens, pos=0)
        
        result = _parse_params(parser_state)
        
        assert parser_state["pos"] == 3
        assert tokens[parser_state["pos"]]["type"] == "RPAREN"

    def test_single_param_at_end_of_tokens(self):
        """Test single parameter when RPAREN is at end of tokens."""
        tokens = [
            _make_token("IDENT", "x", line=1, column=2),
            _make_token("RPAREN", ")", line=1, column=3)
        ]
        parser_state = _make_parser_state(tokens, pos=0)
        
        result = _parse_params(parser_state)
        
        assert len(result["children"]) == 1
        assert parser_state["pos"] == 1

"""Unit tests for _parse_unary function."""
import pytest
from unittest.mock import patch
from typing import Any, Dict

# Relative import for the function under test
from ._parse_unary_src import _parse_unary

# Type aliases matching the source
Token = Dict[str, Any]
AST = Dict[str, Any]
ParserState = Dict[str, Any]


class TestParseUnary:
    """Test cases for _parse_unary function."""

    def test_parse_unary_minus_operator(self):
        """Test parsing MINUS unary operator."""
        parser_state: ParserState = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }
        token: Token = {
            "type": "MINUS",
            "value": "-",
            "line": 1,
            "column": 5
        }

        mock_operand: AST = {
            "type": "NUMBER",
            "value": 42,
            "line": 1,
            "column": 6
        }

        with patch("._parse_unary_src._parse_atom", return_value=mock_operand):
            result = _parse_unary(parser_state, token)

            assert result["type"] == "UNOP"
            assert result["op"] == "-"
            assert result["line"] == 1
            assert result["column"] == 5
            assert result["children"] == [mock_operand]
            assert parser_state["pos"] == 1

    def test_parse_unary_not_operator(self):
        """Test parsing NOT unary operator."""
        parser_state: ParserState = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }
        token: Token = {
            "type": "NOT",
            "value": "not",
            "line": 2,
            "column": 10
        }

        mock_operand: AST = {
            "type": "IDENTIFIER",
            "value": "flag",
            "line": 2,
            "column": 14
        }

        with patch("._parse_unary_src._parse_atom", return_value=mock_operand):
            result = _parse_unary(parser_state, token)

            assert result["type"] == "UNOP"
            assert result["op"] == "not"
            assert result["line"] == 2
            assert result["column"] == 10
            assert result["children"] == [mock_operand]
            assert parser_state["pos"] == 1

    def test_parse_unary_invalid_token_type(self):
        """Test that invalid token type raises ValueError."""
        parser_state: ParserState = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }
        token: Token = {
            "type": "PLUS",
            "value": "+",
            "line": 1,
            "column": 5
        }

        with pytest.raises(ValueError) as exc_info:
            _parse_unary(parser_state, token)

        assert "Invalid unary operator token type: PLUS" in str(exc_info.value)
        assert parser_state["pos"] == 0

    def test_parse_unary_pos_update_before_atom_parse(self):
        """Test that pos is updated before _parse_atom is called."""
        parser_state: ParserState = {
            "tokens": [],
            "pos": 5,
            "filename": "test.py"
        }
        token: Token = {
            "type": "MINUS",
            "value": "-",
            "line": 1,
            "column": 5
        }

        mock_operand: AST = {
            "type": "NUMBER",
            "value": 10,
            "line": 1,
            "column": 6
        }

        with patch("._parse_unary_src._parse_atom", return_value=mock_operand):
            _parse_unary(parser_state, token)

            assert parser_state["pos"] == 6

    def test_parse_unary_with_nested_unary(self):
        """Test parsing nested unary operators (via _parse_atom returning another UNOP)."""
        parser_state: ParserState = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }
        token: Token = {
            "type": "MINUS",
            "value": "-",
            "line": 1,
            "column": 1
        }

        nested_unop: AST = {
            "type": "UNOP",
            "op": "not",
            "line": 1,
            "column": 2,
            "children": [
                {
                    "type": "IDENTIFIER",
                    "value": "x",
                    "line": 1,
                    "column": 5
                }
            ]
        }

        with patch("._parse_unary_src._parse_atom", return_value=nested_unop):
            result = _parse_unary(parser_state, token)

            assert result["type"] == "UNOP"
            assert result["op"] == "-"
            assert len(result["children"]) == 1
            assert result["children"][0] == nested_unop

    def test_parse_unary_preserves_other_state_fields(self):
        """Test that other parser_state fields are preserved."""
        parser_state: ParserState = {
            "tokens": [{"type": "MINUS"}, {"type": "NUMBER"}],
            "pos": 0,
            "filename": "my_module.py",
            "error": None
        }
        token: Token = {
            "type": "NOT",
            "value": "not",
            "line": 3,
            "column": 1
        }

        mock_operand: AST = {
            "type": "IDENTIFIER",
            "value": "value",
            "line": 3,
            "column": 5
        }

        with patch("._parse_unary_src._parse_atom", return_value=mock_operand):
            _parse_unary(parser_state, token)

            assert parser_state["tokens"] == [{"type": "MINUS"}, {"type": "NUMBER"}]
            assert parser_state["filename"] == "my_module.py"
            assert parser_state["error"] is None
            assert parser_state["pos"] == 1

    def test_parse_unary_multiple_operands_via_mock(self):
        """Test _parse_atom can be called multiple times with different results."""
        parser_state: ParserState = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }
        token1: Token = {
            "type": "MINUS",
            "value": "-",
            "line": 1,
            "column": 1
        }
        token2: Token = {
            "type": "NOT",
            "value": "not",
            "line": 2,
            "column": 1
        }

        mock_operand1: AST = {"type": "NUMBER", "value": 1, "line": 1, "column": 2}
        mock_operand2: AST = {"type": "IDENTIFIER", "value": "x", "line": 2, "column": 5}

        with patch("._parse_unary_src._parse_atom") as mock_parse_atom:
            mock_parse_atom.side_effect = [mock_operand1, mock_operand2]

            result1 = _parse_unary(parser_state, token1)
            result2 = _parse_unary(parser_state, token2)

            assert result1["op"] == "-"
            assert result1["children"] == [mock_operand1]
            assert result2["op"] == "not"
            assert result2["children"] == [mock_operand2]
            assert mock_parse_atom.call_count == 2
            assert parser_state["pos"] == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

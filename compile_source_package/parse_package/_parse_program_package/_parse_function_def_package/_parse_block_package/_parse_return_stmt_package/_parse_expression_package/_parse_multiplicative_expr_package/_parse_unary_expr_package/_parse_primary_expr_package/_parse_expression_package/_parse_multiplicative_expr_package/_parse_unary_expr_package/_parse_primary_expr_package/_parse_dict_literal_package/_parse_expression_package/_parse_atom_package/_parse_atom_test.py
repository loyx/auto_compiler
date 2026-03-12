# -*- coding: utf-8 -*-
"""Unit tests for _parse_atom function."""

import pytest
from ._parse_atom_src import _parse_atom


class TestParseAtom:
    """Test cases for _parse_atom parser function."""

    def test_parse_string_token(self):
        """Test parsing a STRING token - should strip quotes."""
        parser_state = {
            "tokens": [
                {"type": "STRING", "value": '"hello world"', "line": 1, "column": 5}
            ],
            "filename": "test.py",
            "pos": 0
        }
        
        result = _parse_atom(parser_state)
        
        assert result["type"] == "string"
        assert result["value"] == "hello world"
        assert result["line"] == 1
        assert result["column"] == 5
        assert result["children"] == []
        assert parser_state["pos"] == 1

    def test_parse_string_token_single_quotes(self):
        """Test parsing a STRING token with single quotes."""
        parser_state = {
            "tokens": [
                {"type": "STRING", "value": "'hello'", "line": 1, "column": 10}
            ],
            "filename": "test.py",
            "pos": 0
        }
        
        result = _parse_atom(parser_state)
        
        assert result["type"] == "string"
        assert result["value"] == "hello"
        assert parser_state["pos"] == 1

    def test_parse_number_token_int(self):
        """Test parsing a NUMBER token as integer."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "42", "line": 2, "column": 3}
            ],
            "filename": "test.py",
            "pos": 0
        }
        
        result = _parse_atom(parser_state)
        
        assert result["type"] == "number"
        assert result["value"] == 42
        assert isinstance(result["value"], int)
        assert result["line"] == 2
        assert result["column"] == 3
        assert parser_state["pos"] == 1

    def test_parse_number_token_float(self):
        """Test parsing a NUMBER token as float."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "3.14", "line": 1, "column": 8}
            ],
            "filename": "test.py",
            "pos": 0
        }
        
        result = _parse_atom(parser_state)
        
        assert result["type"] == "number"
        assert result["value"] == 3.14
        assert isinstance(result["value"], float)
        assert parser_state["pos"] == 1

    def test_parse_number_token_scientific_notation(self):
        """Test parsing a NUMBER token with scientific notation as float."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1.5e10", "line": 1, "column": 1}
            ],
            "filename": "test.py",
            "pos": 0
        }
        
        result = _parse_atom(parser_state)
        
        assert result["type"] == "number"
        assert result["value"] == 1.5e10
        assert isinstance(result["value"], float)
        assert parser_state["pos"] == 1

    def test_parse_number_token_negative_scientific(self):
        """Test parsing a NUMBER token with negative exponent."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "2E-5", "line": 1, "column": 1}
            ],
            "filename": "test.py",
            "pos": 0
        }
        
        result = _parse_atom(parser_state)
        
        assert result["type"] == "number"
        assert result["value"] == 2e-5
        assert isinstance(result["value"], float)
        assert parser_state["pos"] == 1

    def test_parse_identifier_token(self):
        """Test parsing an IDENTIFIER token."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "myVariable", "line": 3, "column": 7}
            ],
            "filename": "test.py",
            "pos": 0
        }
        
        result = _parse_atom(parser_state)
        
        assert result["type"] == "identifier"
        assert result["value"] == "myVariable"
        assert result["line"] == 3
        assert result["column"] == 7
        assert parser_state["pos"] == 1

    def test_parse_true_token(self):
        """Test parsing a TRUE token."""
        parser_state = {
            "tokens": [
                {"type": "TRUE", "value": "true", "line": 1, "column": 1}
            ],
            "filename": "test.py",
            "pos": 0
        }
        
        result = _parse_atom(parser_state)
        
        assert result["type"] == "boolean"
        assert result["value"] is True
        assert result["line"] == 1
        assert result["column"] == 1
        assert parser_state["pos"] == 1

    def test_parse_false_token(self):
        """Test parsing a FALSE token."""
        parser_state = {
            "tokens": [
                {"type": "FALSE", "value": "false", "line": 2, "column": 5}
            ],
            "filename": "test.py",
            "pos": 0
        }
        
        result = _parse_atom(parser_state)
        
        assert result["type"] == "boolean"
        assert result["value"] is False
        assert result["line"] == 2
        assert result["column"] == 5
        assert parser_state["pos"] == 1

    def test_parse_none_token(self):
        """Test parsing a NONE token."""
        parser_state = {
            "tokens": [
                {"type": "NONE", "value": "None", "line": 1, "column": 10}
            ],
            "filename": "test.py",
            "pos": 0
        }
        
        result = _parse_atom(parser_state)
        
        assert result["type"] == "none"
        assert result["value"] is None
        assert result["line"] == 1
        assert result["column"] == 10
        assert parser_state["pos"] == 1

    def test_parse_atom_out_of_bounds(self):
        """Test that SyntaxError is raised when position is out of bounds."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "42", "line": 1, "column": 1}
            ],
            "filename": "test.py",
            "pos": 5  # Beyond token list
        }
        
        with pytest.raises(SyntaxError) as exc_info:
            _parse_atom(parser_state)
        
        assert "Unexpected end of input" in str(exc_info.value)
        assert "test.py" in str(exc_info.value)

    def test_parse_atom_unknown_token_type(self):
        """Test that SyntaxError is raised for unknown token type."""
        parser_state = {
            "tokens": [
                {"type": "UNKNOWN", "value": "???", "line": 5, "column": 12}
            ],
            "filename": "test.py",
            "pos": 0
        }
        
        with pytest.raises(SyntaxError) as exc_info:
            _parse_atom(parser_state)
        
        assert "Unexpected token type 'UNKNOWN'" in str(exc_info.value)
        assert "line 5" in str(exc_info.value)
        assert "column 12" in str(exc_info.value)
        assert "test.py" in str(exc_info.value)

    def test_parse_atom_empty_tokens_list(self):
        """Test that SyntaxError is raised with empty tokens list."""
        parser_state = {
            "tokens": [],
            "filename": "empty.py",
            "pos": 0
        }
        
        with pytest.raises(SyntaxError) as exc_info:
            _parse_atom(parser_state)
        
        assert "Unexpected end of input" in str(exc_info.value)
        assert "empty.py" in str(exc_info.value)

    def test_parse_atom_advances_position(self):
        """Test that parser position is advanced after parsing."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "3", "line": 1, "column": 5}
            ],
            "filename": "test.py",
            "pos": 1  # Start at second token
        }
        
        result = _parse_atom(parser_state)
        
        assert result["value"] == 2
        assert parser_state["pos"] == 2  # Advanced from 1 to 2

    def test_parse_atom_missing_line_column(self):
        """Test parsing when line/column are missing from token."""
        parser_state = {
            "tokens": [
                {"type": "STRING", "value": '"test"', "line": 0, "column": 0}
            ],
            "filename": "test.py",
            "pos": 0
        }
        
        result = _parse_atom(parser_state)
        
        assert result["type"] == "string"
        assert result["value"] == "test"
        assert result["line"] == 0
        assert result["column"] == 0

    def test_parse_atom_negative_number(self):
        """Test parsing a negative number."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "-42", "line": 1, "column": 1}
            ],
            "filename": "test.py",
            "pos": 0
        }
        
        result = _parse_atom(parser_state)
        
        assert result["type"] == "number"
        assert result["value"] == -42
        assert isinstance(result["value"], int)
        assert parser_state["pos"] == 1

    def test_parse_atom_float_without_leading_zero(self):
        """Test parsing a float without leading zero."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": ".5", "line": 1, "column": 1}
            ],
            "filename": "test.py",
            "pos": 0
        }
        
        result = _parse_atom(parser_state)
        
        assert result["type"] == "number"
        assert result["value"] == 0.5
        assert isinstance(result["value"], float)
        assert parser_state["pos"] == 1

    def test_parse_atom_preserves_parser_state_structure(self):
        """Test that other parser_state fields are not modified."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "filename": "original.py",
            "pos": 0,
            "error": None
        }
        
        _parse_atom(parser_state)
        
        assert parser_state["filename"] == "original.py"
        assert parser_state["error"] is None
        assert len(parser_state["tokens"]) == 1

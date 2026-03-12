import pytest
from ._parse_identifier_src import _parse_identifier


class TestParseIdentifier:
    """Test suite for _parse_identifier function"""

    def test_parse_identifier_success(self):
        """Test successful parsing of an identifier token"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "myVar", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.py"
        }

        result = _parse_identifier(parser_state)

        assert result["type"] == "IDENTIFIER"
        assert result["value"] == "myVar"
        assert result["line"] == 1
        assert result["column"] == 5
        assert parser_state["pos"] == 1

    def test_parse_identifier_multiple_tokens(self):
        """Test parsing identifier when there are multiple tokens"""
        parser_state = {
            "tokens": [
                {"type": "KEYWORD", "value": "for", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "i", "line": 1, "column": 5},
                {"type": "OPERATOR", "value": "in", "line": 1, "column": 7}
            ],
            "pos": 1,
            "filename": "test.py"
        }

        result = _parse_identifier(parser_state)

        assert result["type"] == "IDENTIFIER"
        assert result["value"] == "i"
        assert result["line"] == 1
        assert result["column"] == 5
        assert parser_state["pos"] == 2

    def test_parse_identifier_at_end_of_input(self):
        """Test SyntaxError when position is at end of tokens"""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }

        with pytest.raises(SyntaxError) as exc_info:
            _parse_identifier(parser_state)

        assert "Unexpected end of input" in str(exc_info.value)
        assert parser_state["pos"] == 0

    def test_parse_identifier_beyond_tokens(self):
        """Test SyntaxError when position is beyond token list"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 5,
            "filename": "test.py"
        }

        with pytest.raises(SyntaxError) as exc_info:
            _parse_identifier(parser_state)

        assert "Unexpected end of input" in str(exc_info.value)

    def test_parse_identifier_wrong_token_type(self):
        """Test SyntaxError when token type is not IDENTIFIER"""
        parser_state = {
            "tokens": [
                {"type": "KEYWORD", "value": "if", "line": 2, "column": 10}
            ],
            "pos": 0,
            "filename": "test.py"
        }

        with pytest.raises(SyntaxError) as exc_info:
            _parse_identifier(parser_state)

        assert "Expected identifier" in str(exc_info.value)
        assert "line 2" in str(exc_info.value)
        assert "column 10" in str(exc_info.value)
        assert "got KEYWORD" in str(exc_info.value)
        assert parser_state["pos"] == 0

    def test_parse_identifier_operator_token(self):
        """Test SyntaxError when token is an operator"""
        parser_state = {
            "tokens": [
                {"type": "OPERATOR", "value": "+", "line": 3, "column": 15}
            ],
            "pos": 0,
            "filename": "test.py"
        }

        with pytest.raises(SyntaxError) as exc_info:
            _parse_identifier(parser_state)

        assert "Expected identifier" in str(exc_info.value)
        assert "got OPERATOR" in str(exc_info.value)

    def test_parse_identifier_literal_token(self):
        """Test SyntaxError when token is a literal"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "42", "line": 4, "column": 20}
            ],
            "pos": 0,
            "filename": "test.py"
        }

        with pytest.raises(SyntaxError) as exc_info:
            _parse_identifier(parser_state)

        assert "Expected identifier" in str(exc_info.value)
        assert "got NUMBER" in str(exc_info.value)

    def test_parse_identifier_preserves_other_state(self):
        """Test that other parser state fields are not modified"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "test", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "myfile.py",
            "error": None
        }

        result = _parse_identifier(parser_state)

        assert parser_state["filename"] == "myfile.py"
        assert parser_state["error"] is None
        assert len(parser_state["tokens"]) == 1

    def test_parse_identifier_empty_value(self):
        """Test identifier with empty string value"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }

        result = _parse_identifier(parser_state)

        assert result["type"] == "IDENTIFIER"
        assert result["value"] == ""
        assert result["line"] == 1
        assert result["column"] == 1
        assert parser_state["pos"] == 1

    def test_parse_identifier_special_characters_in_value(self):
        """Test identifier with underscores and numbers in value"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "_private_var123", "line": 5, "column": 10}
            ],
            "pos": 0,
            "filename": "test.py"
        }

        result = _parse_identifier(parser_state)

        assert result["type"] == "IDENTIFIER"
        assert result["value"] == "_private_var123"
        assert result["line"] == 5
        assert result["column"] == 10

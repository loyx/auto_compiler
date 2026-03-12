"""Unit tests for _parse_atom function."""
import pytest
from ._parse_atom_src import _parse_atom


class TestParseAtomNumber:
    """Test cases for NUMBER token parsing."""

    def test_parse_integer_number(self):
        """Test parsing an integer number token."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "42", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        result = _parse_atom(parser_state)
        
        assert result["type"] == "NUMBER_LITERAL"
        assert result["value"] == 42
        assert result["children"] == []
        assert result["line"] == 1
        assert result["column"] == 5
        assert parser_state["pos"] == 1

    def test_parse_float_number_with_decimal(self):
        """Test parsing a float number with decimal point."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "3.14", "line": 1, "column": 10}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        result = _parse_atom(parser_state)
        
        assert result["type"] == "NUMBER_LITERAL"
        assert result["value"] == 3.14
        assert isinstance(result["value"], float)
        assert parser_state["pos"] == 1

    def test_parse_float_number_with_exponent(self):
        """Test parsing a float number with exponent notation."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1e10", "line": 2, "column": 3}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        result = _parse_atom(parser_state)
        
        assert result["type"] == "NUMBER_LITERAL"
        assert result["value"] == 1e10
        assert isinstance(result["value"], float)
        assert parser_state["pos"] == 1

    def test_parse_float_number_with_uppercase_exponent(self):
        """Test parsing a float number with uppercase E exponent."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "2E5", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        result = _parse_atom(parser_state)
        
        assert result["type"] == "NUMBER_LITERAL"
        assert result["value"] == 200000.0
        assert isinstance(result["value"], float)
        assert parser_state["pos"] == 1

    def test_parse_negative_integer(self):
        """Test parsing a negative integer number."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "-100", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        result = _parse_atom(parser_state)
        
        assert result["type"] == "NUMBER_LITERAL"
        assert result["value"] == -100
        assert parser_state["pos"] == 1


class TestParseAtomString:
    """Test cases for STRING token parsing."""

    def test_parse_double_quoted_string(self):
        """Test parsing a double-quoted string."""
        parser_state = {
            "tokens": [
                {"type": "STRING", "value": '"hello"', "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        result = _parse_atom(parser_state)
        
        assert result["type"] == "STRING_LITERAL"
        assert result["value"] == "hello"
        assert result["children"] == []
        assert result["line"] == 1
        assert result["column"] == 5
        assert parser_state["pos"] == 1

    def test_parse_single_quoted_string(self):
        """Test parsing a single-quoted string."""
        parser_state = {
            "tokens": [
                {"type": "STRING", "value": "'world'", "line": 2, "column": 10}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        result = _parse_atom(parser_state)
        
        assert result["type"] == "STRING_LITERAL"
        assert result["value"] == "world"
        assert parser_state["pos"] == 1

    def test_parse_empty_string_double_quotes(self):
        """Test parsing an empty string with double quotes."""
        parser_state = {
            "tokens": [
                {"type": "STRING", "value": '""', "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        result = _parse_atom(parser_state)
        
        assert result["type"] == "STRING_LITERAL"
        assert result["value"] == ""
        assert parser_state["pos"] == 1

    def test_parse_empty_string_single_quotes(self):
        """Test parsing an empty string with single quotes."""
        parser_state = {
            "tokens": [
                {"type": "STRING", "value": "''", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        result = _parse_atom(parser_state)
        
        assert result["type"] == "STRING_LITERAL"
        assert result["value"] == ""
        assert parser_state["pos"] == 1

    def test_parse_string_without_quotes_fallback(self):
        """Test parsing a string token without quotes (fallback case)."""
        parser_state = {
            "tokens": [
                {"type": "STRING", "value": "no_quotes", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        result = _parse_atom(parser_state)
        
        assert result["type"] == "STRING_LITERAL"
        assert result["value"] == "no_quotes"
        assert parser_state["pos"] == 1


class TestParseAtomIdentifier:
    """Test cases for IDENTIFIER token parsing."""

    def test_parse_simple_identifier(self):
        """Test parsing a simple identifier."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        result = _parse_atom(parser_state)
        
        assert result["type"] == "IDENTIFIER"
        assert result["value"] == "x"
        assert result["children"] == []
        assert result["line"] == 1
        assert result["column"] == 5
        assert parser_state["pos"] == 1

    def test_parse_long_identifier(self):
        """Test parsing a longer identifier."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "myVariable", "line": 3, "column": 15}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        result = _parse_atom(parser_state)
        
        assert result["type"] == "IDENTIFIER"
        assert result["value"] == "myVariable"
        assert parser_state["pos"] == 1

    def test_parse_identifier_with_underscore(self):
        """Test parsing an identifier with underscores."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "_private_var", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        result = _parse_atom(parser_state)
        
        assert result["type"] == "IDENTIFIER"
        assert result["value"] == "_private_var"
        assert parser_state["pos"] == 1


class TestParseAtomKeyword:
    """Test cases for KEYWORD token parsing."""

    def test_parse_true_keyword_lowercase(self):
        """Test parsing lowercase 'true' keyword."""
        parser_state = {
            "tokens": [
                {"type": "KEYWORD", "value": "true", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        result = _parse_atom(parser_state)
        
        assert result["type"] == "BOOLEAN_LITERAL"
        assert result["value"] is True
        assert result["children"] == []
        assert result["line"] == 1
        assert result["column"] == 5
        assert parser_state["pos"] == 1

    def test_parse_true_keyword_uppercase(self):
        """Test parsing uppercase 'TRUE' keyword."""
        parser_state = {
            "tokens": [
                {"type": "KEYWORD", "value": "TRUE", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        result = _parse_atom(parser_state)
        
        assert result["type"] == "BOOLEAN_LITERAL"
        assert result["value"] is True
        assert parser_state["pos"] == 1

    def test_parse_false_keyword_lowercase(self):
        """Test parsing lowercase 'false' keyword."""
        parser_state = {
            "tokens": [
                {"type": "KEYWORD", "value": "false", "line": 2, "column": 10}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        result = _parse_atom(parser_state)
        
        assert result["type"] == "BOOLEAN_LITERAL"
        assert result["value"] is False
        assert parser_state["pos"] == 1

    def test_parse_false_keyword_uppercase(self):
        """Test parsing uppercase 'FALSE' keyword."""
        parser_state = {
            "tokens": [
                {"type": "KEYWORD", "value": "FALSE", "line": 2, "column": 10}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        result = _parse_atom(parser_state)
        
        assert result["type"] == "BOOLEAN_LITERAL"
        assert result["value"] is False
        assert parser_state["pos"] == 1

    def test_parse_null_keyword_lowercase(self):
        """Test parsing lowercase 'null' keyword."""
        parser_state = {
            "tokens": [
                {"type": "KEYWORD", "value": "null", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        result = _parse_atom(parser_state)
        
        assert result["type"] == "NULL_LITERAL"
        assert result["value"] is None
        assert result["children"] == []
        assert result["line"] == 1
        assert result["column"] == 5
        assert parser_state["pos"] == 1

    def test_parse_null_keyword_uppercase(self):
        """Test parsing uppercase 'NULL' keyword."""
        parser_state = {
            "tokens": [
                {"type": "KEYWORD", "value": "NULL", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        result = _parse_atom(parser_state)
        
        assert result["type"] == "NULL_LITERAL"
        assert result["value"] is None
        assert parser_state["pos"] == 1

    def test_parse_none_keyword_lowercase(self):
        """Test parsing lowercase 'none' keyword."""
        parser_state = {
            "tokens": [
                {"type": "KEYWORD", "value": "none", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        result = _parse_atom(parser_state)
        
        assert result["type"] == "NULL_LITERAL"
        assert result["value"] is None
        assert parser_state["pos"] == 1

    def test_parse_none_keyword_uppercase(self):
        """Test parsing uppercase 'NONE' keyword."""
        parser_state = {
            "tokens": [
                {"type": "KEYWORD", "value": "NONE", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        result = _parse_atom(parser_state)
        
        assert result["type"] == "NULL_LITERAL"
        assert result["value"] is None
        assert parser_state["pos"] == 1

    def test_parse_invalid_keyword_raises_syntax_error(self):
        """Test that invalid keyword raises SyntaxError."""
        parser_state = {
            "tokens": [
                {"type": "KEYWORD", "value": "if", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        with pytest.raises(SyntaxError) as exc_info:
            _parse_atom(parser_state)
        
        assert "Invalid keyword as atom" in str(exc_info.value)
        assert "if" in str(exc_info.value)
        assert parser_state["pos"] == 0  # pos should not advance on error


class TestParseAtomErrors:
    """Test cases for error conditions."""

    def test_empty_tokens_raises_syntax_error(self):
        """Test that empty tokens list raises SyntaxError."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.src"
        }
        
        with pytest.raises(SyntaxError) as exc_info:
            _parse_atom(parser_state)
        
        assert "Unexpected end of input" in str(exc_info.value)
        assert "test.src" in str(exc_info.value)

    def test_pos_beyond_tokens_raises_syntax_error(self):
        """Test that pos beyond tokens length raises SyntaxError."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1}
            ],
            "pos": 5,
            "filename": "test.src"
        }
        
        with pytest.raises(SyntaxError) as exc_info:
            _parse_atom(parser_state)
        
        assert "Unexpected end of input" in str(exc_info.value)

    def test_invalid_token_type_raises_syntax_error(self):
        """Test that invalid token type raises SyntaxError."""
        parser_state = {
            "tokens": [
                {"type": "OPERATOR", "value": "+", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        with pytest.raises(SyntaxError) as exc_info:
            _parse_atom(parser_state)
        
        assert "Invalid atom token type" in str(exc_info.value)
        assert "OPERATOR" in str(exc_info.value)
        assert "5:5" in str(exc_info.value)
        assert parser_state["pos"] == 0  # pos should not advance on error

    def test_unknown_filename_in_error(self):
        """Test error message when filename is not provided."""
        parser_state = {
            "tokens": [],
            "pos": 0
        }
        
        with pytest.raises(SyntaxError) as exc_info:
            _parse_atom(parser_state)
        
        assert "Unexpected end of input" in str(exc_info.value)
        assert "unknown" in str(exc_info.value)


class TestParseAtomPositionAdvancement:
    """Test cases for position advancement behavior."""

    def test_pos_advances_after_successful_parse(self):
        """Test that pos advances by 1 after successful parse."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        result = _parse_atom(parser_state)
        
        assert parser_state["pos"] == 1
        assert result["value"] == 1

    def test_pos_advances_from_non_zero_start(self):
        """Test that pos advances correctly from non-zero starting position."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "3", "line": 1, "column": 5}
            ],
            "pos": 1,
            "filename": "test.src"
        }
        
        result = _parse_atom(parser_state)
        
        assert parser_state["pos"] == 2
        assert result["value"] == 2

    def test_pos_not_advanced_on_error(self):
        """Test that pos is not advanced when parsing fails."""
        parser_state = {
            "tokens": [
                {"type": "OPERATOR", "value": "+", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        with pytest.raises(SyntaxError):
            _parse_atom(parser_state)
        
        assert parser_state["pos"] == 0  # Should remain unchanged


class TestParseAtomPreservesMetadata:
    """Test cases for metadata preservation in AST nodes."""

    def test_line_and_column_preserved(self):
        """Test that line and column are preserved from token to AST."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "var", "line": 10, "column": 25}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        result = _parse_atom(parser_state)
        
        assert result["line"] == 10
        assert result["column"] == 25

    def test_children_always_empty_list(self):
        """Test that children is always an empty list for atom nodes."""
        test_cases = [
            {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
            {"type": "STRING", "value": '"test"', "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            {"type": "KEYWORD", "value": "true", "line": 1, "column": 1},
            {"type": "KEYWORD", "value": "null", "line": 1, "column": 1}
        ]
        
        for token in test_cases:
            parser_state = {
                "tokens": [token],
                "pos": 0,
                "filename": "test.src"
            }
            
            result = _parse_atom(parser_state)
            assert result["children"] == []

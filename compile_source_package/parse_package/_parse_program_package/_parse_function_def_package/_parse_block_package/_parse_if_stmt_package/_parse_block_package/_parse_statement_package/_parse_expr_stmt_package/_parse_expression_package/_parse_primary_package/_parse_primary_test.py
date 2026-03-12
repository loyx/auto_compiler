import pytest
from typing import Dict, Any
from ._parse_primary_src import _parse_primary


def create_token(token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
    """Helper to create a token dict."""
    return {
        "type": token_type,
        "value": value,
        "line": line,
        "column": column
    }


def create_parser_state(tokens: list, pos: int = 0, filename: str = "<test>") -> Dict[str, Any]:
    """Helper to create a parser state dict."""
    return {
        "tokens": tokens,
        "pos": pos,
        "filename": filename
    }


class TestParsePrimaryNumber:
    """Tests for NUMBER token parsing."""

    def test_parse_primary_number_integer(self):
        """Test parsing an integer NUMBER token."""
        tokens = [create_token("NUMBER", "42")]
        parser_state = create_parser_state(tokens)

        result = _parse_primary(parser_state)

        assert result["type"] == "LITERAL"
        assert result["value"] == 42
        assert result["line"] == 1
        assert result["column"] == 1
        assert parser_state["pos"] == 1

    def test_parse_primary_number_float(self):
        """Test parsing a float NUMBER token."""
        tokens = [create_token("NUMBER", "3.14")]
        parser_state = create_parser_state(tokens)

        result = _parse_primary(parser_state)

        assert result["type"] == "LITERAL"
        assert result["value"] == 3.14
        assert result["line"] == 1
        assert result["column"] == 1
        assert parser_state["pos"] == 1

    def test_parse_primary_number_negative(self):
        """Test parsing a negative integer NUMBER token."""
        tokens = [create_token("NUMBER", "-17")]
        parser_state = create_parser_state(tokens)

        result = _parse_primary(parser_state)

        assert result["type"] == "LITERAL"
        assert result["value"] == -17
        assert parser_state["pos"] == 1

    def test_parse_primary_invalid_number(self):
        """Test parsing an invalid NUMBER token raises SyntaxError."""
        tokens = [create_token("NUMBER", "not_a_number")]
        parser_state = create_parser_state(tokens)

        with pytest.raises(SyntaxError) as exc_info:
            _parse_primary(parser_state)

        assert "Invalid number" in str(exc_info.value)


class TestParsePrimaryString:
    """Tests for STRING token parsing."""

    def test_parse_primary_string_double_quotes(self):
        """Test parsing a STRING token with double quotes."""
        tokens = [create_token("STRING", '"hello"')]
        parser_state = create_parser_state(tokens)

        result = _parse_primary(parser_state)

        assert result["type"] == "LITERAL"
        assert result["value"] == "hello"
        assert result["line"] == 1
        assert result["column"] == 1
        assert parser_state["pos"] == 1

    def test_parse_primary_string_single_quotes(self):
        """Test parsing a STRING token with single quotes."""
        tokens = [create_token("STRING", "'world'")]
        parser_state = create_parser_state(tokens)

        result = _parse_primary(parser_state)

        assert result["type"] == "LITERAL"
        assert result["value"] == "world"
        assert result["line"] == 1
        assert result["column"] == 1
        assert parser_state["pos"] == 1

    def test_parse_primary_string_empty(self):
        """Test parsing an empty STRING token."""
        tokens = [create_token("STRING", '""')]
        parser_state = create_parser_state(tokens)

        result = _parse_primary(parser_state)

        assert result["type"] == "LITERAL"
        assert result["value"] == ""
        assert parser_state["pos"] == 1

    def test_parse_primary_invalid_string_no_quotes(self):
        """Test parsing an invalid STRING token without quotes raises SyntaxError."""
        tokens = [create_token("STRING", "no_quotes")]
        parser_state = create_parser_state(tokens)

        with pytest.raises(SyntaxError) as exc_info:
            _parse_primary(parser_state)

        assert "Invalid string literal" in str(exc_info.value)

    def test_parse_primary_invalid_string_mismatched_quotes(self):
        """Test parsing an invalid STRING token with mismatched quotes raises SyntaxError."""
        tokens = [create_token("STRING", '"mismatch\'')]
        parser_state = create_parser_state(tokens)

        with pytest.raises(SyntaxError) as exc_info:
            _parse_primary(parser_state)

        assert "Invalid string literal" in str(exc_info.value)


class TestParsePrimaryIdentifier:
    """Tests for IDENTIFIER token parsing."""

    def test_parse_primary_identifier(self):
        """Test parsing an IDENTIFIER token."""
        tokens = [create_token("IDENTIFIER", "myVar")]
        parser_state = create_parser_state(tokens)

        result = _parse_primary(parser_state)

        assert result["type"] == "IDENTIFIER"
        assert result["value"] == "myVar"
        assert result["line"] == 1
        assert result["column"] == 1
        assert parser_state["pos"] == 1

    def test_parse_primary_identifier_underscore(self):
        """Test parsing an IDENTIFIER token with underscore."""
        tokens = [create_token("IDENTIFIER", "_private_var")]
        parser_state = create_parser_state(tokens)

        result = _parse_primary(parser_state)

        assert result["type"] == "IDENTIFIER"
        assert result["value"] == "_private_var"
        assert parser_state["pos"] == 1


class TestParsePrimaryParenthesized:
    """Tests for LPAREN (parenthesized expression) parsing."""

    def test_parse_primary_parenthesized_expression(self):
        """Test parsing a parenthesized expression with callback."""
        tokens = [
            create_token("LPAREN", "(", 1, 1),
            create_token("NUMBER", "42", 1, 2),
            create_token("RPAREN", ")", 1, 3)
        ]
        parser_state = create_parser_state(tokens)

        def mock_expression_parser(state):
            # Simulate parsing the inner expression (NUMBER)
            state["pos"] = 2  # Move past LPAREN and NUMBER
            return {
                "type": "LITERAL",
                "value": 42,
                "line": 1,
                "column": 2
            }

        result = _parse_primary(parser_state, expression_parser=mock_expression_parser)

        assert result["type"] == "LITERAL"
        assert result["value"] == 42
        assert parser_state["pos"] == 3  # LPAREN + inner + RPAREN consumed

    def test_parse_primary_no_expression_parser_for_paren(self):
        """Test parsing LPAREN without expression_parser raises SyntaxError."""
        tokens = [create_token("LPAREN", "(")]
        parser_state = create_parser_state(tokens)

        with pytest.raises(SyntaxError) as exc_info:
            _parse_primary(parser_state, expression_parser=None)

        assert "expression_parser not provided" in str(exc_info.value)

    def test_parse_primary_missing_rparen(self):
        """Test parsing parenthesized expression without closing paren raises SyntaxError."""
        tokens = [
            create_token("LPAREN", "(", 1, 1),
            create_token("NUMBER", "42", 1, 2)
        ]
        parser_state = create_parser_state(tokens)

        def mock_expression_parser(state):
            state["pos"] = 2  # Simulate consuming the NUMBER
            return {
                "type": "LITERAL",
                "value": 42,
                "line": 1,
                "column": 2
            }

        with pytest.raises(SyntaxError) as exc_info:
            _parse_primary(parser_state, expression_parser=mock_expression_parser)

        assert "Expected ')'" in str(exc_info.value)

    def test_parse_primary_missing_rparen_at_end(self):
        """Test parsing parenthesized expression when RPAREN is at end of tokens raises SyntaxError."""
        tokens = [
            create_token("LPAREN", "(", 1, 1),
        ]
        parser_state = create_parser_state(tokens)

        def mock_expression_parser(state):
            state["pos"] = 1  # Simulate consuming everything
            return {
                "type": "LITERAL",
                "value": 42,
                "line": 1,
                "column": 1
            }

        with pytest.raises(SyntaxError) as exc_info:
            _parse_primary(parser_state, expression_parser=mock_expression_parser)

        assert "Expected ')'" in str(exc_info.value)


class TestParsePrimaryErrorCases:
    """Tests for error conditions."""

    def test_parse_primary_empty_input(self):
        """Test parsing with empty token list raises SyntaxError."""
        parser_state = create_parser_state([])

        with pytest.raises(SyntaxError) as exc_info:
            _parse_primary(parser_state)

        assert "Unexpected end of input" in str(exc_info.value)

    def test_parse_primary_position_beyond_tokens(self):
        """Test parsing when pos is beyond token list raises SyntaxError."""
        tokens = [create_token("NUMBER", "42")]
        parser_state = create_parser_state(tokens, pos=5)

        with pytest.raises(SyntaxError) as exc_info:
            _parse_primary(parser_state)

        assert "Unexpected end of input" in str(exc_info.value)

    def test_parse_primary_unexpected_token(self):
        """Test parsing an unexpected token type raises SyntaxError."""
        tokens = [create_token("PLUS", "+")]
        parser_state = create_parser_state(tokens)

        with pytest.raises(SyntaxError) as exc_info:
            _parse_primary(parser_state)

        assert "Unexpected token" in str(exc_info.value)

    def test_parse_primary_with_filename(self):
        """Test that error messages include the filename."""
        tokens = [create_token("PLUS", "+", 5, 10)]
        parser_state = create_parser_state(tokens, filename="test.py")

        with pytest.raises(SyntaxError) as exc_info:
            _parse_primary(parser_state)

        assert "test.py:5:10" in str(exc_info.value)

    def test_parse_primary_default_filename(self):
        """Test that error messages use default filename when not provided."""
        tokens = [create_token("PLUS", "+")]
        parser_state = {"tokens": tokens, "pos": 0}  # No filename key

        with pytest.raises(SyntaxError) as exc_info:
            _parse_primary(parser_state)

        assert "<unknown>:" in str(exc_info.value)


class TestParsePrimaryPosition:
    """Tests for position tracking."""

    def test_parse_primary_position_not_at_start(self):
        """Test parsing when pos is not at 0."""
        tokens = [
            create_token("PLUS", "+"),
            create_token("NUMBER", "100")
        ]
        parser_state = create_parser_state(tokens, pos=1)

        result = _parse_primary(parser_state)

        assert result["type"] == "LITERAL"
        assert result["value"] == 100
        assert parser_state["pos"] == 2

    def test_parse_primary_multiple_tokens_remaining(self):
        """Test that only one token is consumed, leaving others."""
        tokens = [
            create_token("NUMBER", "42"),
            create_token("PLUS", "+"),
            create_token("NUMBER", "10")
        ]
        parser_state = create_parser_state(tokens)

        result = _parse_primary(parser_state)

        assert result["value"] == 42
        assert parser_state["pos"] == 1
        # Remaining tokens should still be accessible
        assert parser_state["tokens"][1]["type"] == "PLUS"

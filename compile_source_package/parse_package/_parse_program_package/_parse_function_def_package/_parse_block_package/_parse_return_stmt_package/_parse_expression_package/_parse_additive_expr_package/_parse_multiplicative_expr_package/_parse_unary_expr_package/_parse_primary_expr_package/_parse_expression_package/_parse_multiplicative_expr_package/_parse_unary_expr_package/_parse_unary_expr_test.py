import pytest
from typing import Any

from ._parse_unary_expr_src import _parse_unary_expr, ParserState, Token


def _make_parser_state(tokens: list, pos: int = 0, filename: str = "test.py") -> ParserState:
    """Helper to create a parser state dict."""
    return {
        "tokens": tokens,
        "pos": pos,
        "filename": filename
    }


def _make_token(token_type: str, value: Any, line: int = 1, column: int = 1) -> Token:
    """Helper to create a token dict."""
    return {
        "type": token_type,
        "value": value,
        "line": line,
        "column": column
    }


class TestParseUnaryExprHappyPath:
    """Test happy path scenarios for _parse_unary_expr."""

    def test_parse_unary_plus(self):
        """Test parsing unary plus operator."""
        tokens = [
            _make_token("PLUS", "+", 1, 1),
            _make_token("LITERAL", 5, 1, 3)
        ]
        parser_state = _make_parser_state(tokens)
        
        result = _parse_unary_expr(parser_state)
        
        assert result["type"] == "UNARY_OP"
        assert result["operator"] == "+"
        assert result["operand"]["type"] == "LITERAL"
        assert result["operand"]["value"] == 5
        assert result["line"] == 1
        assert result["column"] == 1
        assert parser_state["pos"] == 2

    def test_parse_unary_minus(self):
        """Test parsing unary minus operator."""
        tokens = [
            _make_token("MINUS", "-", 1, 1),
            _make_token("LITERAL", 10, 1, 3)
        ]
        parser_state = _make_parser_state(tokens)
        
        result = _parse_unary_expr(parser_state)
        
        assert result["type"] == "UNARY_OP"
        assert result["operator"] == "-"
        assert result["operand"]["type"] == "LITERAL"
        assert result["operand"]["value"] == 10
        assert result["line"] == 1
        assert result["column"] == 1
        assert parser_state["pos"] == 2

    def test_parse_unary_not(self):
        """Test parsing unary NOT operator."""
        tokens = [
            _make_token("NOT", "not", 1, 1),
            _make_token("IDENTIFIER", "flag", 1, 5)
        ]
        parser_state = _make_parser_state(tokens)
        
        result = _parse_unary_expr(parser_state)
        
        assert result["type"] == "UNARY_OP"
        assert result["operator"] == "not"
        assert result["operand"]["type"] == "IDENTIFIER"
        assert result["operand"]["value"] == "flag"
        assert result["line"] == 1
        assert result["column"] == 1
        assert parser_state["pos"] == 2

    def test_parse_unary_tilde(self):
        """Test parsing unary TILDE operator."""
        tokens = [
            _make_token("TILDE", "~", 1, 1),
            _make_token("LITERAL", 42, 1, 3)
        ]
        parser_state = _make_parser_state(tokens)
        
        result = _parse_unary_expr(parser_state)
        
        assert result["type"] == "UNARY_OP"
        assert result["operator"] == "~"
        assert result["operand"]["type"] == "LITERAL"
        assert result["operand"]["value"] == 42
        assert result["line"] == 1
        assert result["column"] == 1
        assert parser_state["pos"] == 2

    def test_parse_nested_unary_operators(self):
        """Test parsing nested unary operators."""
        tokens = [
            _make_token("MINUS", "-", 1, 1),
            _make_token("PLUS", "+", 1, 3),
            _make_token("LITERAL", 5, 1, 5)
        ]
        parser_state = _make_parser_state(tokens)
        
        result = _parse_unary_expr(parser_state)
        
        assert result["type"] == "UNARY_OP"
        assert result["operator"] == "-"
        assert result["operand"]["type"] == "UNARY_OP"
        assert result["operand"]["operator"] == "+"
        assert result["operand"]["operand"]["type"] == "LITERAL"
        assert result["operand"]["operand"]["value"] == 5
        assert parser_state["pos"] == 3

    def test_parse_identifier(self):
        """Test parsing an identifier."""
        tokens = [
            _make_token("IDENTIFIER", "x", 1, 1)
        ]
        parser_state = _make_parser_state(tokens)
        
        result = _parse_unary_expr(parser_state)
        
        assert result["type"] == "IDENTIFIER"
        assert result["value"] == "x"
        assert result["line"] == 1
        assert result["column"] == 1
        assert parser_state["pos"] == 1

    def test_parse_literal(self):
        """Test parsing a literal."""
        tokens = [
            _make_token("LITERAL", 42, 1, 1)
        ]
        parser_state = _make_parser_state(tokens)
        
        result = _parse_unary_expr(parser_state)
        
        assert result["type"] == "LITERAL"
        assert result["value"] == 42
        assert result["line"] == 1
        assert result["column"] == 1
        assert parser_state["pos"] == 1

    def test_parse_parenthesized_expression(self):
        """Test parsing a parenthesized expression."""
        tokens = [
            _make_token("LPAREN", "(", 1, 1),
            _make_token("LITERAL", 5, 1, 3),
            _make_token("RPAREN", ")", 1, 5)
        ]
        parser_state = _make_parser_state(tokens)
        
        result = _parse_unary_expr(parser_state)
        
        assert result["type"] == "LITERAL"
        assert result["value"] == 5
        assert parser_state["pos"] == 3

    def test_parse_parenthesized_unary_expression(self):
        """Test parsing a parenthesized unary expression."""
        tokens = [
            _make_token("LPAREN", "(", 1, 1),
            _make_token("MINUS", "-", 1, 3),
            _make_token("LITERAL", 10, 1, 5),
            _make_token("RPAREN", ")", 1, 7)
        ]
        parser_state = _make_parser_state(tokens)
        
        result = _parse_unary_expr(parser_state)
        
        assert result["type"] == "UNARY_OP"
        assert result["operator"] == "-"
        assert result["operand"]["type"] == "LITERAL"
        assert result["operand"]["value"] == 10
        assert parser_state["pos"] == 4


class TestParseUnaryExprEdgeCases:
    """Test edge cases for _parse_unary_expr."""

    def test_empty_tokens_raises_syntax_error(self):
        """Test that empty tokens list raises SyntaxError."""
        parser_state = _make_parser_state([])
        
        with pytest.raises(SyntaxError) as exc_info:
            _parse_unary_expr(parser_state)
        
        assert "Unexpected end of input" in str(exc_info.value)

    def test_pos_beyond_tokens_raises_syntax_error(self):
        """Test that pos beyond tokens length raises SyntaxError."""
        tokens = [_make_token("LITERAL", 5, 1, 1)]
        parser_state = _make_parser_state(tokens, pos=1)
        
        with pytest.raises(SyntaxError) as exc_info:
            _parse_unary_expr(parser_state)
        
        assert "Unexpected end of input" in str(exc_info.value)

    def test_missing_closing_parenthesis_raises_syntax_error(self):
        """Test that missing closing parenthesis raises SyntaxError."""
        tokens = [
            _make_token("LPAREN", "(", 1, 1),
            _make_token("LITERAL", 5, 1, 3)
        ]
        parser_state = _make_parser_state(tokens)
        
        with pytest.raises(SyntaxError) as exc_info:
            _parse_unary_expr(parser_state)
        
        assert "Missing closing parenthesis" in str(exc_info.value)

    def test_wrong_closing_token_raises_syntax_error(self):
        """Test that wrong closing token raises SyntaxError."""
        tokens = [
            _make_token("LPAREN", "(", 1, 1),
            _make_token("LITERAL", 5, 1, 3),
            _make_token("COMMA", ",", 1, 5)
        ]
        parser_state = _make_parser_state(tokens)
        
        with pytest.raises(SyntaxError) as exc_info:
            _parse_unary_expr(parser_state)
        
        assert "Expected RPAREN" in str(exc_info.value)

    def test_unexpected_token_type_raises_syntax_error(self):
        """Test that unexpected token type raises SyntaxError."""
        tokens = [
            _make_token("COMMA", ",", 1, 1)
        ]
        parser_state = _make_parser_state(tokens)
        
        with pytest.raises(SyntaxError) as exc_info:
            _parse_unary_expr(parser_state)
        
        assert "Unexpected token" in str(exc_info.value)
        assert "COMMA" in str(exc_info.value)

    def test_error_includes_line_and_column(self):
        """Test that error message includes line and column information."""
        tokens = [
            _make_token("COMMA", ",", 5, 10)
        ]
        parser_state = _make_parser_state(tokens)
        
        with pytest.raises(SyntaxError) as exc_info:
            _parse_unary_expr(parser_state)
        
        assert "line 5" in str(exc_info.value)
        assert "column 10" in str(exc_info.value)


class TestParseUnaryExprPositionTracking:
    """Test that parser_state position is correctly updated."""

    def test_position_not_modified_on_error(self):
        """Test that position is not modified when parsing fails."""
        tokens = [
            _make_token("COMMA", ",", 1, 1)
        ]
        parser_state = _make_parser_state(tokens, pos=0)
        original_pos = parser_state["pos"]
        
        with pytest.raises(SyntaxError):
            _parse_unary_expr(parser_state)
        
        # Position should remain unchanged on error
        assert parser_state["pos"] == original_pos

    def test_position_advanced_correctly_for_unary_op(self):
        """Test that position is advanced correctly for unary operator."""
        tokens = [
            _make_token("MINUS", "-", 1, 1),
            _make_token("LITERAL", 5, 1, 3)
        ]
        parser_state = _make_parser_state(tokens)
        
        _parse_unary_expr(parser_state)
        
        assert parser_state["pos"] == 2

    def test_position_advanced_correctly_for_identifier(self):
        """Test that position is advanced correctly for identifier."""
        tokens = [
            _make_token("IDENTIFIER", "x", 1, 1)
        ]
        parser_state = _make_parser_state(tokens)
        
        _parse_unary_expr(parser_state)
        
        assert parser_state["pos"] == 1

    def test_position_advanced_correctly_for_parenthesized(self):
        """Test that position is advanced correctly for parenthesized expression."""
        tokens = [
            _make_token("LPAREN", "(", 1, 1),
            _make_token("LITERAL", 5, 1, 3),
            _make_token("RPAREN", ")", 1, 5)
        ]
        parser_state = _make_parser_state(tokens)
        
        _parse_unary_expr(parser_state)
        
        assert parser_state["pos"] == 3


class TestParseUnaryExprASTStructure:
    """Test that AST structure is correctly formed."""

    def test_unary_op_has_required_fields(self):
        """Test that UNARY_OP node has all required fields."""
        tokens = [
            _make_token("MINUS", "-", 1, 1),
            _make_token("LITERAL", 5, 1, 3)
        ]
        parser_state = _make_parser_state(tokens)
        
        result = _parse_unary_expr(parser_state)
        
        assert "type" in result
        assert "operator" in result
        assert "operand" in result
        assert "line" in result
        assert "column" in result

    def test_identifier_has_required_fields(self):
        """Test that IDENTIFIER node has all required fields."""
        tokens = [
            _make_token("IDENTIFIER", "x", 1, 1)
        ]
        parser_state = _make_parser_state(tokens)
        
        result = _parse_unary_expr(parser_state)
        
        assert "type" in result
        assert "value" in result
        assert "line" in result
        assert "column" in result

    def test_literal_has_required_fields(self):
        """Test that LITERAL node has all required fields."""
        tokens = [
            _make_token("LITERAL", 42, 1, 1)
        ]
        parser_state = _make_parser_state(tokens)
        
        result = _parse_unary_expr(parser_state)
        
        assert "type" in result
        assert "value" in result
        assert "line" in result
        assert "column" in result

    def test_line_column_preserved_from_operator_token(self):
        """Test that line and column are preserved from the operator token."""
        tokens = [
            _make_token("MINUS", "-", 5, 10),
            _make_token("LITERAL", 5, 6, 1)
        ]
        parser_state = _make_parser_state(tokens)
        
        result = _parse_unary_expr(parser_state)
        
        assert result["line"] == 5
        assert result["column"] == 10

"""Unit tests for _parse_primary function."""

import pytest
from unittest.mock import patch
from typing import Dict, Any

from ._parse_primary_src import _parse_primary


def _create_token(token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
    """Helper to create a token dictionary."""
    return {
        "type": token_type,
        "value": value,
        "line": line,
        "column": column
    }


def _create_parser_state(tokens: list, pos: int = 0, filename: str = "test.py") -> Dict[str, Any]:
    """Helper to create a parser state dictionary."""
    return {
        "tokens": tokens,
        "pos": pos,
        "filename": filename
    }


class TestParsePrimaryLiterals:
    """Test parsing literal values."""
    
    def test_parse_integer_number(self):
        """Test parsing integer number literal."""
        tokens = [_create_token("NUMBER", "42")]
        parser_state = _create_parser_state(tokens)
        
        result = _parse_primary(parser_state)
        
        assert result["type"] == "LITERAL"
        assert result["value"] == 42
        assert result["children"] == []
        assert result["line"] == 1
        assert result["column"] == 1
        assert parser_state["pos"] == 1
    
    def test_parse_float_number(self):
        """Test parsing float number literal."""
        tokens = [_create_token("NUMBER", "3.14")]
        parser_state = _create_parser_state(tokens)
        
        result = _parse_primary(parser_state)
        
        assert result["type"] == "LITERAL"
        assert result["value"] == 3.14
        assert isinstance(result["value"], float)
        assert parser_state["pos"] == 1
    
    def test_parse_negative_number(self):
        """Test parsing negative number (as string value)."""
        tokens = [_create_token("NUMBER", "-10")]
        parser_state = _create_parser_state(tokens)
        
        result = _parse_primary(parser_state)
        
        assert result["type"] == "LITERAL"
        assert result["value"] == -10
        assert parser_state["pos"] == 1
    
    def test_parse_string_double_quotes(self):
        """Test parsing string literal with double quotes."""
        tokens = [_create_token("STRING", '"hello world"')]
        parser_state = _create_parser_state(tokens)
        
        result = _parse_primary(parser_state)
        
        assert result["type"] == "LITERAL"
        assert result["value"] == "hello world"
        assert parser_state["pos"] == 1
    
    def test_parse_string_single_quotes(self):
        """Test parsing string literal with single quotes."""
        tokens = [_create_token("STRING", "'hello world'")]
        parser_state = _create_parser_state(tokens)
        
        result = _parse_primary(parser_state)
        
        assert result["type"] == "LITERAL"
        assert result["value"] == "hello world"
        assert parser_state["pos"] == 1
    
    def test_parse_string_without_quotes(self):
        """Test parsing string token without surrounding quotes."""
        tokens = [_create_token("STRING", "hello")]
        parser_state = _create_parser_state(tokens)
        
        result = _parse_primary(parser_state)
        
        assert result["type"] == "LITERAL"
        assert result["value"] == "hello"
        assert parser_state["pos"] == 1
    
    def test_parse_bool_true(self):
        """Test parsing boolean true literal."""
        tokens = [_create_token("BOOL", "True")]
        parser_state = _create_parser_state(tokens)
        
        result = _parse_primary(parser_state)
        
        assert result["type"] == "LITERAL"
        assert result["value"] is True
        assert parser_state["pos"] == 1
    
    def test_parse_bool_false(self):
        """Test parsing boolean false literal."""
        tokens = [_create_token("BOOL", "False")]
        parser_state = _create_parser_state(tokens)
        
        result = _parse_primary(parser_state)
        
        assert result["type"] == "LITERAL"
        assert result["value"] is False
        assert parser_state["pos"] == 1
    
    def test_parse_bool_lowercase_true(self):
        """Test parsing boolean true in lowercase."""
        tokens = [_create_token("BOOL", "true")]
        parser_state = _create_parser_state(tokens)
        
        result = _parse_primary(parser_state)
        
        assert result["type"] == "LITERAL"
        assert result["value"] is True
    
    def test_parse_none(self):
        """Test parsing None literal."""
        tokens = [_create_token("NONE", "None")]
        parser_state = _create_parser_state(tokens)
        
        result = _parse_primary(parser_state)
        
        assert result["type"] == "LITERAL"
        assert result["value"] is None
        assert parser_state["pos"] == 1


class TestParsePrimaryIdentifier:
    """Test parsing identifier references."""
    
    def test_parse_simple_identifier(self):
        """Test parsing simple identifier."""
        tokens = [_create_token("IDENTIFIER", "x")]
        parser_state = _create_parser_state(tokens)
        
        result = _parse_primary(parser_state)
        
        assert result["type"] == "IDENTIFIER"
        assert result["value"] == "x"
        assert result["children"] == []
        assert parser_state["pos"] == 1
    
    def test_parse_long_identifier(self):
        """Test parsing longer identifier name."""
        tokens = [_create_token("IDENTIFIER", "my_variable_name")]
        parser_state = _create_parser_state(tokens)
        
        result = _parse_primary(parser_state)
        
        assert result["type"] == "IDENTIFIER"
        assert result["value"] == "my_variable_name"
        assert parser_state["pos"] == 1


class TestParsePrimaryParenthesized:
    """Test parsing parenthesized expressions."""
    
    @patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_primary_package._parse_primary_src._parse_or_expr")
    def test_parse_parenthesized_expression(self, mock_parse_or_expr):
        """Test parsing expression in parentheses."""
        inner_expr = {
            "type": "BINARY_OP",
            "value": "+",
            "children": [
                {"type": "LITERAL", "value": 1},
                {"type": "LITERAL", "value": 2}
            ],
            "line": 1,
            "column": 1
        }
        def mock_impl(state):
            state["pos"] = 3  # consume both NUMBER tokens
            return inner_expr
        mock_parse_or_expr.side_effect = mock_impl
        
        tokens = [
            _create_token("LPAREN", "("),
            _create_token("NUMBER", "1"),
            _create_token("NUMBER", "2"),
            _create_token("RPAREN", ")")
        ]
        parser_state = _create_parser_state(tokens)
        
        result = _parse_primary(parser_state)
        
        assert result == inner_expr
        assert parser_state["pos"] == 4
        mock_parse_or_expr.assert_called_once()
    
    @patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_primary_package._parse_primary_src._parse_or_expr")
    def test_parse_nested_parentheses(self, mock_parse_or_expr):
        """Test parsing nested parenthesized expression."""
        inner_expr = {"type": "LITERAL", "value": 42}
        mock_parse_or_expr.return_value = inner_expr
        
        tokens = [
            _create_token("LPAREN", "("),
            _create_token("LPAREN", "("),
            _create_token("NUMBER", "42"),
            _create_token("RPAREN", ")"),
            _create_token("RPAREN", ")")
        ]
        parser_state = _create_parser_state(tokens)
        
        result = _parse_primary(parser_state)
        
        assert result == inner_expr
        assert parser_state["pos"] == 5


class TestParsePrimaryErrors:
    """Test error cases."""
    
    def test_empty_tokens(self):
        """Test parsing with empty token list."""
        parser_state = _create_parser_state([])
        
        with pytest.raises(SyntaxError, match="Unexpected end of input"):
            _parse_primary(parser_state)
    
    def test_pos_beyond_tokens(self):
        """Test parsing when pos is beyond token list."""
        tokens = [_create_token("NUMBER", "42")]
        parser_state = _create_parser_state(tokens, pos=1)
        
        with pytest.raises(SyntaxError, match="Unexpected end of input"):
            _parse_primary(parser_state)
    
    def test_missing_closing_paren(self):
        """Test error when closing parenthesis is missing."""
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_primary_package._parse_primary_src._parse_or_expr") as mock_parse_or_expr:
            mock_parse_or_expr.return_value = {"type": "LITERAL", "value": 42}
            
            tokens = [
                _create_token("LPAREN", "("),
                _create_token("NUMBER", "42")
            ]
            parser_state = _create_parser_state(tokens)
            
            with pytest.raises(SyntaxError, match=r"Expected '\)' at line 1"):
                _parse_primary(parser_state)
    
    def test_missing_closing_paren_at_end(self):
        """Test error when closing parenthesis is missing at end of input."""
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_primary_package._parse_primary_src._parse_or_expr") as mock_parse_or_expr:
            mock_parse_or_expr.return_value = {"type": "LITERAL", "value": 42}
            
            tokens = [
                _create_token("LPAREN", "("),
                _create_token("NUMBER", "42"),
                _create_token("NUMBER", "43")
            ]
            parser_state = _create_parser_state(tokens)
            
            with pytest.raises(SyntaxError, match=r"Expected '\)' at line 1"):
                _parse_primary(parser_state)
    
    def test_invalid_token_type(self):
        """Test error when token type is not valid expression start."""
        tokens = [_create_token("PLUS", "+")]
        parser_state = _create_parser_state(tokens)
        
        with pytest.raises(SyntaxError, match="Expected expression at line 1"):
            _parse_primary(parser_state)
    
    def test_operator_as_primary(self):
        """Test error when operator token is encountered."""
        tokens = [_create_token("STAR", "*")]
        parser_state = _create_parser_state(tokens)
        
        with pytest.raises(SyntaxError, match="Expected expression at line 1"):
            _parse_primary(parser_state)


class TestParsePrimaryPosition:
    """Test position tracking."""
    
    def test_position_at_middle_of_tokens(self):
        """Test parsing when starting from middle of token list."""
        tokens = [
            _create_token("NUMBER", "1"),
            _create_token("NUMBER", "2"),
            _create_token("NUMBER", "3")
        ]
        parser_state = _create_parser_state(tokens, pos=1)
        
        result = _parse_primary(parser_state)
        
        assert result["value"] == 2
        assert parser_state["pos"] == 2
    
    def test_preserves_line_column_info(self):
        """Test that line and column information is preserved."""
        tokens = [_create_token("IDENTIFIER", "var", line=5, column=10)]
        parser_state = _create_parser_state(tokens)
        
        result = _parse_primary(parser_state)
        
        assert result["line"] == 5
        assert result["column"] == 10
    
    def test_multiple_calls_update_position(self):
        """Test that multiple calls properly update position."""
        tokens = [
            _create_token("NUMBER", "1"),
            _create_token("NUMBER", "2"),
            _create_token("NUMBER", "3")
        ]
        parser_state = _create_parser_state(tokens)
        
        result1 = _parse_primary(parser_state)
        assert result1["value"] == 1
        assert parser_state["pos"] == 1
        
        result2 = _parse_primary(parser_state)
        assert result2["value"] == 2
        assert parser_state["pos"] == 2
        
        result3 = _parse_primary(parser_state)
        assert result3["value"] == 3
        assert parser_state["pos"] == 3


class TestParsePrimaryEdgeCases:
    """Test edge cases and special scenarios."""
    
    def test_float_with_many_decimals(self):
        """Test parsing float with many decimal places."""
        tokens = [_create_token("NUMBER", "3.14159265359")]
        parser_state = _create_parser_state(tokens)
        
        result = _parse_primary(parser_state)
        
        assert result["type"] == "LITERAL"
        assert isinstance(result["value"], float)
        assert abs(result["value"] - 3.14159265359) < 1e-10
    
    def test_large_integer(self):
        """Test parsing large integer."""
        tokens = [_create_token("NUMBER", "999999999999")]
        parser_state = _create_parser_state(tokens)
        
        result = _parse_primary(parser_state)
        
        assert result["value"] == 999999999999
        assert isinstance(result["value"], int)
    
    def test_empty_string(self):
        """Test parsing empty string literal."""
        tokens = [_create_token("STRING", '""')]
        parser_state = _create_parser_state(tokens)
        
        result = _parse_primary(parser_state)
        
        assert result["value"] == ""
    
    def test_string_with_spaces(self):
        """Test parsing string with internal spaces."""
        tokens = [_create_token("STRING", '"hello   world"')]
        parser_state = _create_parser_state(tokens)
        
        result = _parse_primary(parser_state)
        
        assert result["value"] == "hello   world"
    
    def test_identifier_with_underscore(self):
        """Test parsing identifier with underscores."""
        tokens = [_create_token("IDENTIFIER", "_private_var_")]
        parser_state = _create_parser_state(tokens)
        
        result = _parse_primary(parser_state)
        
        assert result["value"] == "_private_var_"
    
    @patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_primary_package._parse_primary_src._parse_or_expr")
    def test_parenthesized_returns_inner_ast_unchanged(self, mock_parse_or_expr):
        """Test that parenthesized expression returns the inner AST unchanged."""
        expected_ast = {
            "type": "BINARY_OP",
            "value": "+",
            "children": [
                {"type": "IDENTIFIER", "value": "a"},
                {"type": "LITERAL", "value": 1}
            ],
            "line": 1,
            "column": 1
        }
        mock_parse_or_expr.return_value = expected_ast
        
        tokens = [
            _create_token("LPAREN", "("),
            _create_token("IDENTIFIER", "a"),
            _create_token("PLUS", "+"),
            _create_token("NUMBER", "1"),
            _create_token("RPAREN", ")")
        ]
        parser_state = _create_parser_state(tokens)
        
        result = _parse_primary(parser_state)
        
        assert result is expected_ast

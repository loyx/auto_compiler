"""
Unit tests for _parse_expression function.
Tests the expression parsing entry point that delegates to _parse_or_expr.
"""

import pytest
from unittest.mock import patch

# Relative import from the same package
from ._parse_expression_src import _parse_expression


class TestParseExpression:
    """Test cases for _parse_expression function."""

    def test_parse_expression_delegates_to_parse_or_expr(self):
        """Test that _parse_expression correctly delegates to _parse_or_expr."""
        mock_parser_state = {"tokens": [], "pos": 0, "filename": "test.c"}
        mock_ast = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_expression_src._parse_or_expr") as mock_or_expr:
            mock_or_expr.return_value = mock_ast
            
            result = _parse_expression(mock_parser_state)
            
            mock_or_expr.assert_called_once_with(mock_parser_state)
            assert result == mock_ast

    def test_parse_expression_with_simple_identifier(self):
        """Test parsing a simple identifier expression."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_expression_src._parse_or_expr") as mock_or_expr:
            mock_or_expr.return_value = {
                "type": "IDENTIFIER",
                "value": "x",
                "line": 1,
                "column": 1
            }
            
            result = _parse_expression(parser_state)
            
            assert result["type"] == "IDENTIFIER"
            assert result["value"] == "x"
            mock_or_expr.assert_called_once()

    def test_parse_expression_with_integer_literal(self):
        """Test parsing an integer literal expression."""
        parser_state = {
            "tokens": [
                {"type": "INTEGER", "value": "42", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_expression_src._parse_or_expr") as mock_or_expr:
            mock_or_expr.return_value = {
                "type": "LITERAL",
                "value": 42,
                "line": 1,
                "column": 1
            }
            
            result = _parse_expression(parser_state)
            
            assert result["type"] == "LITERAL"
            assert result["value"] == 42

    def test_parse_expression_with_binary_operation(self):
        """Test parsing a binary operation expression."""
        parser_state = {
            "tokens": [
                {"type": "INTEGER", "value": "1", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 2},
                {"type": "INTEGER", "value": "2", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_expression_src._parse_or_expr") as mock_or_expr:
            mock_or_expr.return_value = {
                "type": "BINARY_OP",
                "operator": "+",
                "left": {"type": "LITERAL", "value": 1},
                "right": {"type": "LITERAL", "value": 2},
                "line": 1,
                "column": 1
            }
            
            result = _parse_expression(parser_state)
            
            assert result["type"] == "BINARY_OP"
            assert result["operator"] == "+"

    def test_parse_expression_with_unary_operation(self):
        """Test parsing a unary operation expression."""
        parser_state = {
            "tokens": [
                {"type": "MINUS", "value": "-", "line": 1, "column": 1},
                {"type": "INTEGER", "value": "5", "line": 1, "column": 2}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_expression_src._parse_or_expr") as mock_or_expr:
            mock_or_expr.return_value = {
                "type": "UNARY_OP",
                "operator": "-",
                "operand": {"type": "LITERAL", "value": 5},
                "line": 1,
                "column": 1
            }
            
            result = _parse_expression(parser_state)
            
            assert result["type"] == "UNARY_OP"
            assert result["operator"] == "-"

    def test_parse_expression_with_logical_or(self):
        """Test parsing a logical OR expression."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "OR", "value": "||", "line": 1, "column": 2},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_expression_src._parse_or_expr") as mock_or_expr:
            mock_or_expr.return_value = {
                "type": "BINARY_OP",
                "operator": "||",
                "left": {"type": "IDENTIFIER", "value": "a"},
                "right": {"type": "IDENTIFIER", "value": "b"},
                "line": 1,
                "column": 1
            }
            
            result = _parse_expression(parser_state)
            
            assert result["type"] == "BINARY_OP"
            assert result["operator"] == "||"

    def test_parse_expression_with_logical_and(self):
        """Test parsing a logical AND expression."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "AND", "value": "&&", "line": 1, "column": 2},
                {"type": "IDENTIFIER", "value": "y", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_expression_src._parse_or_expr") as mock_or_expr:
            mock_or_expr.return_value = {
                "type": "BINARY_OP",
                "operator": "&&",
                "left": {"type": "IDENTIFIER", "value": "x"},
                "right": {"type": "IDENTIFIER", "value": "y"},
                "line": 1,
                "column": 1
            }
            
            result = _parse_expression(parser_state)
            
            assert result["type"] == "BINARY_OP"
            assert result["operator"] == "&&"

    def test_parse_expression_with_comparison(self):
        """Test parsing a comparison expression."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "LT", "value": "<", "line": 1, "column": 2},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_expression_src._parse_or_expr") as mock_or_expr:
            mock_or_expr.return_value = {
                "type": "BINARY_OP",
                "operator": "<",
                "left": {"type": "IDENTIFIER", "value": "a"},
                "right": {"type": "IDENTIFIER", "value": "b"},
                "line": 1,
                "column": 1
            }
            
            result = _parse_expression(parser_state)
            
            assert result["type"] == "BINARY_OP"
            assert result["operator"] == "<"

    def test_parse_expression_with_parentheses(self):
        """Test parsing a parenthesized expression."""
        parser_state = {
            "tokens": [
                {"type": "LPAREN", "value": "(", "line": 1, "column": 1},
                {"type": "INTEGER", "value": "1", "line": 1, "column": 2},
                {"type": "PLUS", "value": "+", "line": 1, "column": 3},
                {"type": "INTEGER", "value": "2", "line": 1, "column": 4},
                {"type": "RPAREN", "value": ")", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_expression_src._parse_or_expr") as mock_or_expr:
            mock_or_expr.return_value = {
                "type": "BINARY_OP",
                "operator": "+",
                "left": {"type": "LITERAL", "value": 1},
                "right": {"type": "LITERAL", "value": 2},
                "line": 1,
                "column": 1
            }
            
            result = _parse_expression(parser_state)
            
            assert result["type"] == "BINARY_OP"

    def test_parse_expression_with_boolean_true(self):
        """Test parsing a boolean true literal."""
        parser_state = {
            "tokens": [
                {"type": "TRUE", "value": "true", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_expression_src._parse_or_expr") as mock_or_expr:
            mock_or_expr.return_value = {
                "type": "LITERAL",
                "value": True,
                "line": 1,
                "column": 1
            }
            
            result = _parse_expression(parser_state)
            
            assert result["type"] == "LITERAL"
            assert result["value"] is True

    def test_parse_expression_with_boolean_false(self):
        """Test parsing a boolean false literal."""
        parser_state = {
            "tokens": [
                {"type": "FALSE", "value": "false", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_expression_src._parse_or_expr") as mock_or_expr:
            mock_or_expr.return_value = {
                "type": "LITERAL",
                "value": False,
                "line": 1,
                "column": 1
            }
            
            result = _parse_expression(parser_state)
            
            assert result["type"] == "LITERAL"
            assert result["value"] is False

    def test_parse_expression_with_null(self):
        """Test parsing a null literal."""
        parser_state = {
            "tokens": [
                {"type": "NULL", "value": "null", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_expression_src._parse_or_expr") as mock_or_expr:
            mock_or_expr.return_value = {
                "type": "LITERAL",
                "value": None,
                "line": 1,
                "column": 1
            }
            
            result = _parse_expression(parser_state)
            
            assert result["type"] == "LITERAL"
            assert result["value"] is None

    def test_parse_expression_with_string_literal(self):
        """Test parsing a string literal."""
        parser_state = {
            "tokens": [
                {"type": "STRING", "value": "hello", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_expression_src._parse_or_expr") as mock_or_expr:
            mock_or_expr.return_value = {
                "type": "LITERAL",
                "value": "hello",
                "line": 1,
                "column": 1
            }
            
            result = _parse_expression(parser_state)
            
            assert result["type"] == "LITERAL"
            assert result["value"] == "hello"

    def test_parse_expression_syntax_error_propagation(self):
        """Test that SyntaxError from _parse_or_expr is propagated."""
        parser_state = {
            "tokens": [
                {"type": "PLUS", "value": "+", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_expression_src._parse_or_expr") as mock_or_expr:
            mock_or_expr.side_effect = SyntaxError("Unexpected token '+' at line 1, column 1")
            
            with pytest.raises(SyntaxError) as exc_info:
                _parse_expression(parser_state)
            
            assert "Unexpected token '+'" in str(exc_info.value)

    def test_parse_expression_empty_tokens(self):
        """Test parsing with empty token list."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_expression_src._parse_or_expr") as mock_or_expr:
            mock_or_expr.side_effect = SyntaxError("Unexpected end of input")
            
            with pytest.raises(SyntaxError):
                _parse_expression(parser_state)

    def test_parse_expression_preserves_parser_state_reference(self):
        """Test that parser_state is passed by reference (not copied)."""
        parser_state = {"tokens": [], "pos": 0, "filename": "test.c"}
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_expression_src._parse_or_expr") as mock_or_expr:
            mock_or_expr.return_value = {"type": "LITERAL", "value": 42}
            
            _parse_expression(parser_state)
            
            # Verify the same object reference was passed
            assert mock_or_expr.call_args[0][0] is parser_state

    def test_parse_expression_position_advanced(self):
        """Test that parser position is advanced after parsing."""
        parser_state = {
            "tokens": [
                {"type": "INTEGER", "value": "42", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        def advance_position(state):
            state["pos"] = 1
            return {"type": "LITERAL", "value": 42}
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_expression_src._parse_or_expr") as mock_or_expr:
            mock_or_expr.side_effect = advance_position
            
            result = _parse_expression(parser_state)
            
            assert parser_state["pos"] == 1
            assert result["type"] == "LITERAL"

    def test_parse_expression_complex_mixed_operators(self):
        """Test parsing expression with mixed operators respecting precedence."""
        parser_state = {
            "tokens": [
                {"type": "INTEGER", "value": "1", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 2},
                {"type": "INTEGER", "value": "2", "line": 1, "column": 3},
                {"type": "STAR", "value": "*", "line": 1, "column": 4},
                {"type": "INTEGER", "value": "3", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_expression_src._parse_or_expr") as mock_or_expr:
            # 1 + (2 * 3) due to operator precedence
            mock_or_expr.return_value = {
                "type": "BINARY_OP",
                "operator": "+",
                "left": {"type": "LITERAL", "value": 1},
                "right": {
                    "type": "BINARY_OP",
                    "operator": "*",
                    "left": {"type": "LITERAL", "value": 2},
                    "right": {"type": "LITERAL", "value": 3}
                },
                "line": 1,
                "column": 1
            }
            
            result = _parse_expression(parser_state)
            
            assert result["type"] == "BINARY_OP"
            assert result["operator"] == "+"

    def test_parse_expression_with_not_operator(self):
        """Test parsing expression with logical NOT operator."""
        parser_state = {
            "tokens": [
                {"type": "NOT", "value": "!", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "flag", "line": 1, "column": 2}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_expression_src._parse_or_expr") as mock_or_expr:
            mock_or_expr.return_value = {
                "type": "UNARY_OP",
                "operator": "!",
                "operand": {"type": "IDENTIFIER", "value": "flag"},
                "line": 1,
                "column": 1
            }
            
            result = _parse_expression(parser_state)
            
            assert result["type"] == "UNARY_OP"
            assert result["operator"] == "!"

    def test_parse_expression_with_float_literal(self):
        """Test parsing a float literal."""
        parser_state = {
            "tokens": [
                {"type": "FLOAT", "value": "3.14", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_expression_src._parse_or_expr") as mock_or_expr:
            mock_or_expr.return_value = {
                "type": "LITERAL",
                "value": 3.14,
                "line": 1,
                "column": 1
            }
            
            result = _parse_expression(parser_state)
            
            assert result["type"] == "LITERAL"
            assert result["value"] == 3.14

    def test_parse_expression_with_char_literal(self):
        """Test parsing a character literal."""
        parser_state = {
            "tokens": [
                {"type": "CHAR", "value": "a", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_expression_src._parse_or_expr") as mock_or_expr:
            mock_or_expr.return_value = {
                "type": "LITERAL",
                "value": "a",
                "line": 1,
                "column": 1
            }
            
            result = _parse_expression(parser_state)
            
            assert result["type"] == "LITERAL"
            assert result["value"] == "a"

    def test_parse_expression_multiple_calls_independent(self):
        """Test that multiple calls to _parse_expression are independent."""
        parser_state1 = {
            "tokens": [{"type": "INTEGER", "value": "1", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test1.c"
        }
        parser_state2 = {
            "tokens": [{"type": "INTEGER", "value": "2", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test2.c"
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_expression_src._parse_or_expr") as mock_or_expr:
            mock_or_expr.side_effect = [
                {"type": "LITERAL", "value": 1},
                {"type": "LITERAL", "value": 2}
            ]
            
            result1 = _parse_expression(parser_state1)
            result2 = _parse_expression(parser_state2)
            
            assert result1["value"] == 1
            assert result2["value"] == 2
            assert mock_or_expr.call_count == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

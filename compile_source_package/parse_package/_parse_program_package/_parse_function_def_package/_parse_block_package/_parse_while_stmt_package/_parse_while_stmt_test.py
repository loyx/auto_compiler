"""Unit tests for _parse_while_stmt function."""
import pytest
from unittest.mock import patch, MagicMock
import sys

# Pre-mock the dependencies to avoid import errors
# Mock _parse_expression module
mock_parse_expression = MagicMock()
mock_expression_pkg = MagicMock()
mock_expression_pkg._parse_expression_src = MagicMock()
mock_expression_pkg._parse_expression_src._parse_expression = mock_parse_expression
sys.modules['main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_expression_package'] = mock_expression_pkg
sys.modules['main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_expression_package._parse_expression_src'] = mock_expression_pkg._parse_expression_src

# Mock _parse_block module and its dependencies
mock_parse_block = MagicMock()
mock_block_pkg = MagicMock()
mock_block_pkg._parse_block_src = MagicMock()
mock_block_pkg._parse_block_src._parse_block = mock_parse_block
sys.modules['main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package'] = mock_block_pkg
sys.modules['main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_block_src'] = mock_block_pkg._parse_block_src

# Mock all transitive dependencies of _parse_block
sys.modules['main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_var_decl_package'] = MagicMock()
sys.modules['main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_var_decl_package._parse_var_decl_src'] = MagicMock()
sys.modules['main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._consume_token_package'] = MagicMock()
sys.modules['main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._consume_token_package._consume_token_src'] = MagicMock()

from ._parse_while_stmt_src import _parse_while_stmt


class TestParseWhileStmt:
    """Test cases for _parse_while_stmt function."""

    def test_happy_path_valid_while_statement(self):
        """Test parsing a valid while statement."""
        parser_state = {
            "tokens": [
                {"type": "WHILE", "value": "while", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 7},
                {"type": "LBRACE", "value": "{", "line": 1, "column": 9},
                {"type": "RBRACE", "value": "}", "line": 1, "column": 10},
            ],
            "pos": 0,
            "filename": "test.c"
        }

        mock_condition = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 7}
        mock_body = {"type": "BLOCK", "children": [], "line": 1, "column": 9}

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_while_stmt_src._parse_expression") as mock_parse_expr, \
             patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_while_stmt_src._parse_block") as mock_parse_block:
            mock_parse_expr.return_value = mock_condition
            mock_parse_block.return_value = mock_body

            result = _parse_while_stmt(parser_state)

            assert result["type"] == "WHILE_STMT"
            assert len(result["children"]) == 2
            assert result["children"][0] == mock_condition
            assert result["children"][1] == mock_body
            assert result["line"] == 1
            assert result["column"] == 1
            assert parser_state["pos"] == 1
            mock_parse_expr.assert_called_once()
            mock_parse_block.assert_called_once()

    def test_error_unexpected_end_of_input(self):
        """Test error when tokens are exhausted."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.c"
        }

        with pytest.raises(SyntaxError) as exc_info:
            _parse_while_stmt(parser_state)

        assert "Unexpected end of input" in str(exc_info.value)

    def test_error_non_while_token(self):
        """Test error when current token is not WHILE."""
        parser_state = {
            "tokens": [
                {"type": "IF", "value": "if", "line": 5, "column": 3},
            ],
            "pos": 0,
            "filename": "test.c"
        }

        with pytest.raises(SyntaxError) as exc_info:
            _parse_while_stmt(parser_state)

        assert "Expected WHILE token, got IF at line 5" in str(exc_info.value)

    def test_position_advances_after_while_token(self):
        """Test that parser position advances after consuming WHILE token."""
        parser_state = {
            "tokens": [
                {"type": "WHILE", "value": "while", "line": 2, "column": 5},
                {"type": "LPAREN", "value": "(", "line": 2, "column": 11},
            ],
            "pos": 0,
            "filename": "test.c"
        }

        mock_condition = {"type": "IDENTIFIER", "value": "x", "line": 2, "column": 12}
        mock_body = {"type": "BLOCK", "children": [], "line": 2, "column": 15}

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_while_stmt_src._parse_expression") as mock_parse_expr, \
             patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_while_stmt_src._parse_block") as mock_parse_block:
            mock_parse_expr.return_value = mock_condition
            mock_parse_block.return_value = mock_body

            _parse_while_stmt(parser_state)

            assert parser_state["pos"] == 1

    def test_complex_condition_and_body(self):
        """Test while statement with complex condition and body."""
        parser_state = {
            "tokens": [
                {"type": "WHILE", "value": "while", "line": 10, "column": 1},
                {"type": "LPAREN", "value": "(", "line": 10, "column": 7},
                {"type": "IDENTIFIER", "value": "i", "line": 10, "column": 8},
                {"type": "LT", "value": "<", "line": 10, "column": 10},
                {"type": "NUMBER", "value": "10", "line": 10, "column": 12},
                {"type": "RPAREN", "value": ")", "line": 10, "column": 14},
                {"type": "LBRACE", "value": "{", "line": 10, "column": 16},
                {"type": "RBRACE", "value": "}", "line": 11, "column": 1},
            ],
            "pos": 0,
            "filename": "test.c"
        }

        mock_condition = {
            "type": "BINARY_OP",
            "value": "<",
            "children": [
                {"type": "IDENTIFIER", "value": "i", "line": 10, "column": 8},
                {"type": "LITERAL", "value": "10", "line": 10, "column": 12}
            ],
            "line": 10,
            "column": 8
        }
        mock_body = {
            "type": "BLOCK",
            "children": [
                {"type": "EXPR_STMT", "value": "i++", "line": 10, "column": 17}
            ],
            "line": 10,
            "column": 16
        }

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_while_stmt_src._parse_expression") as mock_parse_expr, \
             patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_while_stmt_src._parse_block") as mock_parse_block:
            mock_parse_expr.return_value = mock_condition
            mock_parse_block.return_value = mock_body

            result = _parse_while_stmt(parser_state)

            assert result["type"] == "WHILE_STMT"
            assert result["line"] == 10
            assert result["column"] == 1
            assert len(result["children"]) == 2
            assert result["children"][0] == mock_condition
            assert result["children"][1] == mock_body

    def test_position_not_at_start(self):
        """Test parsing while statement when position is not at start of tokens."""
        parser_state = {
            "tokens": [
                {"type": "VAR_DECL", "value": "int x", "line": 1, "column": 1},
                {"type": "SEMICOLON", "value": ";", "line": 1, "column": 7},
                {"type": "WHILE", "value": "while", "line": 2, "column": 1},
                {"type": "LPAREN", "value": "(", "line": 2, "column": 7},
            ],
            "pos": 2,
            "filename": "test.c"
        }

        mock_condition = {"type": "IDENTIFIER", "value": "x", "line": 2, "column": 8}
        mock_body = {"type": "BLOCK", "children": [], "line": 2, "column": 10}

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_while_stmt_src._parse_expression") as mock_parse_expr, \
             patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_while_stmt_src._parse_block") as mock_parse_block:
            mock_parse_expr.return_value = mock_condition
            mock_parse_block.return_value = mock_body

            result = _parse_while_stmt(parser_state)

            assert result["type"] == "WHILE_STMT"
            assert result["line"] == 2
            assert result["column"] == 1
            assert parser_state["pos"] == 3

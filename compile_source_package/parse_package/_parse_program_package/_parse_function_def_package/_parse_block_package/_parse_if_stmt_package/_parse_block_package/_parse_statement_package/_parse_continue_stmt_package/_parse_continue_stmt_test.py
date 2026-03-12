"""Unit tests for _parse_continue_stmt function."""

import pytest
from ._parse_continue_stmt_src import _parse_continue_stmt


class TestParseContinueStmt:
    """Test cases for _parse_continue_stmt parser function."""

    def test_happy_path_valid_continue_stmt(self):
        """Test parsing a valid continue; statement."""
        tokens = [
            {"type": "CONTINUE", "value": "continue", "line": 5, "column": 10},
            {"type": "SEMICOLON", "value": ";", "line": 5, "column": 18},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c",
        }

        result = _parse_continue_stmt(parser_state)

        assert result["type"] == "CONTINUE_STMT"
        assert result["children"] == []
        assert result["line"] == 5
        assert result["column"] == 10
        assert parser_state["pos"] == 2

    def test_parser_state_pos_updated_correctly(self):
        """Test that parser_state pos is updated to point after SEMICOLON."""
        tokens = [
            {"type": "CONTINUE", "value": "continue", "line": 1, "column": 1},
            {"type": "SEMICOLON", "value": ";", "line": 1, "column": 9},
            {"type": "RETURN", "value": "return", "line": 2, "column": 1},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c",
        }

        result = _parse_continue_stmt(parser_state)

        assert parser_state["pos"] == 2
        assert tokens[parser_state["pos"]]["type"] == "RETURN"

    def test_line_column_preserved_from_continue_token(self):
        """Test that line and column are preserved from CONTINUE token."""
        tokens = [
            {"type": "CONTINUE", "value": "continue", "line": 42, "column": 7},
            {"type": "SEMICOLON", "value": ";", "line": 42, "column": 15},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c",
        }

        result = _parse_continue_stmt(parser_state)

        assert result["line"] == 42
        assert result["column"] == 7

    def test_error_missing_semicolon_raises_syntax_error(self):
        """Test that missing SEMICOLON raises SyntaxError."""
        tokens = [
            {"type": "CONTINUE", "value": "continue", "line": 10, "column": 5},
            {"type": "RETURN", "value": "return", "line": 11, "column": 1},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c",
        }

        with pytest.raises(SyntaxError) as exc_info:
            _parse_continue_stmt(parser_state)

        assert "Expected ';' after continue" in str(exc_info.value)
        assert "test.c:10:5" in str(exc_info.value)

    def test_error_end_of_tokens_no_semicolon(self):
        """Test that end of tokens without SEMICOLON raises SyntaxError."""
        tokens = [
            {"type": "CONTINUE", "value": "continue", "line": 3, "column": 12},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "main.c",
        }

        with pytest.raises(SyntaxError) as exc_info:
            _parse_continue_stmt(parser_state)

        assert "Expected ';' after continue" in str(exc_info.value)
        assert "main.c:3:12" in str(exc_info.value)

    def test_error_wrong_token_type_after_continue(self):
        """Test that wrong token type after CONTINUE raises SyntaxError."""
        tokens = [
            {"type": "CONTINUE", "value": "continue", "line": 7, "column": 3},
            {"type": "IDENTIFIER", "value": "x", "line": 7, "column": 12},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c",
        }

        with pytest.raises(SyntaxError) as exc_info:
            _parse_continue_stmt(parser_state)

        assert "Expected ';' after continue" in str(exc_info.value)

    def test_continue_stmt_has_no_children(self):
        """Test that CONTINUE_STMT AST node has empty children list."""
        tokens = [
            {"type": "CONTINUE", "value": "continue", "line": 1, "column": 1},
            {"type": "SEMICOLON", "value": ";", "line": 1, "column": 9},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c",
        }

        result = _parse_continue_stmt(parser_state)

        assert result["children"] == []
        assert len(result) == 4  # type, children, line, column
        assert "value" not in result

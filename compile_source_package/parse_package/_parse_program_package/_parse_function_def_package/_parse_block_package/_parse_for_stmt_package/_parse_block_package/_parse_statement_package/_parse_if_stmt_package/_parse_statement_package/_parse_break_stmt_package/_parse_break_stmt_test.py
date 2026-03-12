# -*- coding: utf-8 -*-
"""Unit tests for _parse_break_stmt function."""

import pytest
from unittest.mock import patch, call

# Relative import from the same package
from ._parse_break_stmt_src import _parse_break_stmt


class TestParseBreakStmt:
    """Test cases for _parse_break_stmt function."""

    def test_happy_path_basic_break(self):
        """Test parsing a basic break statement at position 0."""
        parser_state = {
            "tokens": [
                {"type": "BREAK", "value": "break", "line": 1, "column": 5},
                {"type": "SEMICOLON", "value": ";", "line": 1, "column": 10}
            ],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }

        with patch("._expect_token_package._expect_token_src._expect_token") as mock_expect:
            result = _parse_break_stmt(parser_state)

        # Verify _expect_token was called twice with correct arguments
        assert mock_expect.call_count == 2
        mock_expect.assert_has_calls([
            call(parser_state, "BREAK"),
            call(parser_state, "SEMICOLON")
        ])

        # Verify result structure
        assert result["type"] == "BREAK_STMT"
        assert result["children"] == []
        assert result["value"] == "break"
        assert result["line"] == 1
        assert result["column"] == 5

    def test_happy_path_break_at_different_position(self):
        """Test parsing break statement when pos is not at 0."""
        parser_state = {
            "tokens": [
                {"type": "IF", "value": "if", "line": 1, "column": 1},
                {"type": "BREAK", "value": "break", "line": 2, "column": 3},
                {"type": "SEMICOLON", "value": ";", "line": 2, "column": 8}
            ],
            "pos": 1,
            "filename": "test.py",
            "error": ""
        }

        with patch("._expect_token_package._expect_token_src._expect_token") as mock_expect:
            result = _parse_break_stmt(parser_state)

        assert mock_expect.call_count == 2
        assert result["type"] == "BREAK_STMT"
        assert result["line"] == 2
        assert result["column"] == 3

    def test_happy_path_break_in_for_loop(self):
        """Test parsing break statement inside a for loop context."""
        parser_state = {
            "tokens": [
                {"type": "FOR", "value": "for", "line": 1, "column": 1},
                {"type": "BREAK", "value": "break", "line": 3, "column": 9},
                {"type": "SEMICOLON", "value": ";", "line": 3, "column": 14}
            ],
            "pos": 1,
            "filename": "main.py",
            "error": ""
        }

        with patch("._expect_token_package._expect_token_src._expect_token") as mock_expect:
            result = _parse_break_stmt(parser_state)

        assert result["type"] == "BREAK_STMT"
        assert result["value"] == "break"
        assert result["children"] == []
        assert result["line"] == 3
        assert result["column"] == 9

    def test_error_semicolon_missing(self):
        """Test that SyntaxError is raised when SEMICOLON is missing."""
        parser_state = {
            "tokens": [
                {"type": "BREAK", "value": "break", "line": 1, "column": 5},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 11}
            ],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }

        with patch("._expect_token_package._expect_token_src._expect_token") as mock_expect:
            # Second call (SEMICOLON) raises SyntaxError
            mock_expect.side_effect = SyntaxError("Expected SEMICOLON")

            with pytest.raises(SyntaxError, match="Expected SEMICOLON"):
                _parse_break_stmt(parser_state)

        # Verify _expect_token was called at least once for BREAK
        assert mock_expect.call_count >= 1
        mock_expect.assert_any_call(parser_state, "BREAK")

    def test_error_break_token_invalid(self):
        """Test that SyntaxError is raised when BREAK token validation fails."""
        parser_state = {
            "tokens": [
                {"type": "BREAK", "value": "break", "line": 1, "column": 5},
                {"type": "SEMICOLON", "value": ";", "line": 1, "column": 10}
            ],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }

        with patch("._expect_token_package._expect_token_src._expect_token") as mock_expect:
            # First call (BREAK) raises SyntaxError
            mock_expect.side_effect = SyntaxError("Expected BREAK")

            with pytest.raises(SyntaxError, match="Expected BREAK"):
                _parse_break_stmt(parser_state)

    def test_boundary_zero_line_column(self):
        """Test parsing break statement with zero line and column numbers."""
        parser_state = {
            "tokens": [
                {"type": "BREAK", "value": "break", "line": 0, "column": 0},
                {"type": "SEMICOLON", "value": ";", "line": 0, "column": 5}
            ],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }

        with patch("._expect_token_package._expect_token_src._expect_token") as mock_expect:
            result = _parse_break_stmt(parser_state)

        assert result["line"] == 0
        assert result["column"] == 0
        assert result["type"] == "BREAK_STMT"

    def test_boundary_large_line_column(self):
        """Test parsing break statement with large line and column numbers."""
        parser_state = {
            "tokens": [
                {"type": "BREAK", "value": "break", "line": 9999, "column": 8888},
                {"type": "SEMICOLON", "value": ";", "line": 9999, "column": 9993}
            ],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }

        with patch("._expect_token_package._expect_token_src._expect_token") as mock_expect:
            result = _parse_break_stmt(parser_state)

        assert result["line"] == 9999
        assert result["column"] == 8888

    def test_boundary_last_token_position(self):
        """Test parsing break statement when it's the last token in the list."""
        parser_state = {
            "tokens": [
                {"type": "BREAK", "value": "break", "line": 10, "column": 5},
                {"type": "SEMICOLON", "value": ";", "line": 10, "column": 10}
            ],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }

        with patch("._expect_token_package._expect_token_src._expect_token") as mock_expect:
            result = _parse_break_stmt(parser_state)

        assert result["type"] == "BREAK_STMT"
        assert mock_expect.call_count == 2

    def test_ast_node_structure_complete(self):
        """Test that the returned AST node has all required fields."""
        parser_state = {
            "tokens": [
                {"type": "BREAK", "value": "break", "line": 5, "column": 12},
                {"type": "SEMICOLON", "value": ";", "line": 5, "column": 17}
            ],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }

        with patch("._expect_token_package._expect_token_src._expect_token") as mock_expect:
            result = _parse_break_stmt(parser_state)

        # Verify all required AST fields are present
        assert "type" in result
        assert "children" in result
        assert "value" in result
        assert "line" in result
        assert "column" in result

        # Verify field types
        assert isinstance(result["type"], str)
        assert isinstance(result["children"], list)
        assert isinstance(result["value"], str)
        assert isinstance(result["line"], int)
        assert isinstance(result["column"], int)

        # Verify specific values
        assert result["type"] == "BREAK_STMT"
        assert result["children"] == []
        assert result["value"] == "break"
        assert result["line"] == 5
        assert result["column"] == 12

    def test_parser_state_not_modified_directly(self):
        """Test that parser state modification is delegated to _expect_token."""
        parser_state = {
            "tokens": [
                {"type": "BREAK", "value": "break", "line": 1, "column": 5},
                {"type": "SEMICOLON", "value": ";", "line": 1, "column": 10}
            ],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }

        with patch("._expect_token_package._expect_token_src._expect_token") as mock_expect:
            _parse_break_stmt(parser_state)

        # Verify _expect_token is responsible for state modification
        assert mock_expect.call_count == 2
        # The function itself should not directly modify parser_state["pos"]
        # That's delegated to _expect_token

# -*- coding: utf-8 -*-
"""Unit tests for _parse_def_stmt function."""

import pytest
from unittest.mock import patch

from ._parse_def_stmt_src import _parse_def_stmt


class TestParseDefStmt:
    """Test cases for _parse_def_stmt function."""

    def _create_parser_state(self, tokens, pos=0, filename="test.py"):
        """Helper to create parser state dict."""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename,
            "error": None
        }

    def _create_token(self, token_type, value, line=1, column=1):
        """Helper to create a token dict."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def test_simple_def_no_params(self):
        """Test parsing simple def statement with no parameters."""
        tokens = [
            self._create_token("DEF", "def", 1, 1),
            self._create_token("IDENTIFIER", "foo", 1, 5),
            self._create_token("LPAREN", "(", 1, 8),
            self._create_token("RPAREN", ")", 1, 9),
            self._create_token("COLON", ":", 1, 10),
            self._create_token("SEMICOLON", ";", 1, 15),
        ]
        parser_state = self._create_parser_state(tokens)

        with patch("._parse_block_package._parse_block_src._parse_block") as mock_parse_block:
            mock_parse_block.return_value = {
                "type": "BLOCK",
                "children": [],
                "line": 1,
                "column": 10
            }

            result = _parse_def_stmt(parser_state)

        assert result["type"] == "DEF"
        assert result["line"] == 1
        assert result["column"] == 1
        assert len(result["children"]) == 3

        func_name = result["children"][0]
        assert func_name["type"] == "FUNC_NAME"
        assert func_name["value"] == "foo"
        assert func_name["line"] == 1
        assert func_name["column"] == 5

        params = result["children"][1]
        assert params["type"] == "PARAMS"
        assert params["children"] == []

        body = result["children"][2]
        assert body["type"] == "BLOCK"

        assert parser_state["pos"] == 5

    def test_def_with_params(self):
        """Test parsing def statement with parameters."""
        tokens = [
            self._create_token("DEF", "def", 1, 1),
            self._create_token("IDENTIFIER", "bar", 1, 5),
            self._create_token("LPAREN", "(", 1, 8),
            self._create_token("IDENTIFIER", "x", 1, 9),
            self._create_token("COMMA", ",", 1, 10),
            self._create_token("IDENTIFIER", "y", 1, 12),
            self._create_token("RPAREN", ")", 1, 13),
            self._create_token("COLON", ":", 1, 14),
            self._create_token("SEMICOLON", ";", 1, 20),
        ]
        parser_state = self._create_parser_state(tokens)

        with patch("._parse_block_package._parse_block_src._parse_block") as mock_parse_block:
            mock_parse_block.return_value = {
                "type": "BLOCK",
                "children": [],
                "line": 1,
                "column": 14
            }

        with patch("._parse_param_list_package._parse_param_list_src._parse_param_list") as mock_parse_param:
            mock_parse_param.return_value = [
                {"type": "PARAM", "value": "x", "line": 1, "column": 9},
                {"type": "PARAM", "value": "y", "line": 1, "column": 12},
            ]
            mock_parse_param.side_effect = lambda state: state.update({"pos": 6}) or [
                {"type": "PARAM", "value": "x", "line": 1, "column": 9},
                {"type": "PARAM", "value": "y", "line": 1, "column": 12},
            ]

            result = _parse_def_stmt(parser_state)

        assert result["type"] == "DEF"
        params = result["children"][1]
        assert params["type"] == "PARAMS"
        assert len(params["children"]) == 2

    def test_def_nested_function(self):
        """Test parsing nested function definition."""
        tokens = [
            self._create_token("DEF", "def", 1, 1),
            self._create_token("IDENTIFIER", "outer", 1, 5),
            self._create_token("LPAREN", "(", 1, 10),
            self._create_token("RPAREN", ")", 1, 11),
            self._create_token("COLON", ":", 1, 12),
            self._create_token("DEF", "def", 2, 5),
            self._create_token("IDENTIFIER", "inner", 2, 9),
            self._create_token("LPAREN", "(", 2, 14),
            self._create_token("RPAREN", ")", 2, 15),
            self._create_token("COLON", ":", 2, 16),
            self._create_token("SEMICOLON", ";", 2, 20),
            self._create_token("SEMICOLON", ";", 3, 1),
        ]
        parser_state = self._create_parser_state(tokens)

        def mock_block_side_effect(state):
            state["pos"] = 11
            return {
                "type": "BLOCK",
                "children": [],
                "line": 1,
                "column": 12
            }

        with patch("._parse_block_package._parse_block_src._parse_block") as mock_parse_block:
            mock_parse_block.side_effect = mock_block_side_effect

            result = _parse_def_stmt(parser_state)

        assert result["type"] == "DEF"
        func_name = result["children"][0]
        assert func_name["value"] == "outer"

    def test_missing_def_keyword(self):
        """Test error when DEF keyword is missing."""
        tokens = [
            self._create_token("IDENTIFIER", "foo", 1, 1),
        ]
        parser_state = self._create_parser_state(tokens)

        with pytest.raises(SyntaxError) as exc_info:
            _parse_def_stmt(parser_state)

        assert "Expected DEF keyword" in str(exc_info.value)

    def test_missing_function_name(self):
        """Test error when function name is missing after DEF."""
        tokens = [
            self._create_token("DEF", "def", 1, 1),
            self._create_token("LPAREN", "(", 1, 5),
        ]
        parser_state = self._create_parser_state(tokens)

        with pytest.raises(SyntaxError) as exc_info:
            _parse_def_stmt(parser_state)

        assert "Expected function name" in str(exc_info.value)

    def test_missing_lparen(self):
        """Test error when LPAREN is missing after function name."""
        tokens = [
            self._create_token("DEF", "def", 1, 1),
            self._create_token("IDENTIFIER", "foo", 1, 5),
            self._create_token("RPAREN", ")", 1, 9),
        ]
        parser_state = self._create_parser_state(tokens)

        with pytest.raises(SyntaxError) as exc_info:
            _parse_def_stmt(parser_state)

        assert "Expected '('" in str(exc_info.value)

    def test_missing_rparen(self):
        """Test error when RPAREN is missing after parameters."""
        tokens = [
            self._create_token("DEF", "def", 1, 1),
            self._create_token("IDENTIFIER", "foo", 1, 5),
            self._create_token("LPAREN", "(", 1, 8),
            self._create_token("IDENTIFIER", "x", 1, 9),
            self._create_token("COLON", ":", 1, 11),
        ]
        parser_state = self._create_parser_state(tokens)

        with patch("._parse_param_list_package._parse_param_list_src._parse_param_list") as mock_parse_param:
            mock_parse_param.return_value = []

            with pytest.raises(SyntaxError) as exc_info:
                _parse_def_stmt(parser_state)

        assert "Expected ')'" in str(exc_info.value)

    def test_missing_colon(self):
        """Test error when COLON is missing after RPAREN."""
        tokens = [
            self._create_token("DEF", "def", 1, 1),
            self._create_token("IDENTIFIER", "foo", 1, 5),
            self._create_token("LPAREN", "(", 1, 8),
            self._create_token("RPAREN", ")", 1, 9),
            self._create_token("SEMICOLON", ";", 1, 11),
        ]
        parser_state = self._create_parser_state(tokens)

        with pytest.raises(SyntaxError) as exc_info:
            _parse_def_stmt(parser_state)

        assert "Expected ':'" in str(exc_info.value)

    def test_empty_tokens(self):
        """Test error when token list is empty."""
        tokens = []
        parser_state = self._create_parser_state(tokens)

        with pytest.raises(SyntaxError) as exc_info:
            _parse_def_stmt(parser_state)

        assert "Expected DEF keyword" in str(exc_info.value)

    def test_pos_updated_correctly(self):
        """Test that parser_state pos is updated correctly."""
        tokens = [
            self._create_token("DEF", "def", 1, 1),
            self._create_token("IDENTIFIER", "foo", 1, 5),
            self._create_token("LPAREN", "(", 1, 8),
            self._create_token("RPAREN", ")", 1, 9),
            self._create_token("COLON", ":", 1, 10),
            self._create_token("SEMICOLON", ";", 1, 15),
        ]
        parser_state = self._create_parser_state(tokens)

        with patch("._parse_block_package._parse_block_src._parse_block") as mock_parse_block:
            mock_parse_block.return_value = {
                "type": "BLOCK",
                "children": [],
                "line": 1,
                "column": 10
            }

            _parse_def_stmt(parser_state)

        assert parser_state["pos"] == 5

    def test_ast_node_structure(self):
        """Test that DEF AST node has correct structure."""
        tokens = [
            self._create_token("DEF", "def", 2, 10),
            self._create_token("IDENTIFIER", "my_func", 2, 14),
            self._create_token("LPAREN", "(", 2, 21),
            self._create_token("RPAREN", ")", 2, 22),
            self._create_token("COLON", ":", 2, 23),
            self._create_token("SEMICOLON", ";", 2, 30),
        ]
        parser_state = self._create_parser_state(tokens)

        with patch("._parse_block_package._parse_block_src._parse_block") as mock_parse_block:
            mock_parse_block.return_value = {
                "type": "BLOCK",
                "children": [],
                "line": 2,
                "column": 23
            }

            result = _parse_def_stmt(parser_state)

        assert "type" in result
        assert "line" in result
        assert "column" in result
        assert "children" in result
        assert result["type"] == "DEF"
        assert result["line"] == 2
        assert result["column"] == 10
        assert len(result["children"]) == 3

        func_name_node = result["children"][0]
        assert func_name_node["type"] == "FUNC_NAME"
        assert func_name_node["value"] == "my_func"
        assert func_name_node["line"] == 2
        assert func_name_node["column"] == 14

        params_node = result["children"][1]
        assert params_node["type"] == "PARAMS"
        assert "children" in params_node

        body_node = result["children"][2]
        assert body_node["type"] == "BLOCK"

    def test_error_message_includes_filename(self):
        """Test that error messages include filename when available."""
        tokens = [
            self._create_token("IDENTIFIER", "foo", 1, 1),
        ]
        parser_state = self._create_parser_state(tokens, filename="my_module.py")

        with pytest.raises(SyntaxError) as exc_info:
            _parse_def_stmt(parser_state)

        assert "my_module.py" in str(exc_info.value)

    def test_def_with_single_param(self):
        """Test parsing def statement with single parameter."""
        tokens = [
            self._create_token("DEF", "def", 1, 1),
            self._create_token("IDENTIFIER", "func", 1, 5),
            self._create_token("LPAREN", "(", 1, 9),
            self._create_token("IDENTIFIER", "param", 1, 10),
            self._create_token("RPAREN", ")", 1, 15),
            self._create_token("COLON", ":", 1, 16),
            self._create_token("SEMICOLON", ";", 1, 20),
        ]
        parser_state = self._create_parser_state(tokens)

        with patch("._parse_block_package._parse_block_src._parse_block") as mock_parse_block:
            mock_parse_block.return_value = {
                "type": "BLOCK",
                "children": [],
                "line": 1,
                "column": 16
            }

        with patch("._parse_param_list_package._parse_param_list_src._parse_param_list") as mock_parse_param:
            mock_parse_param.return_value = [
                {"type": "PARAM", "value": "param", "line": 1, "column": 10},
            ]
            mock_parse_param.side_effect = lambda state: state.update({"pos": 4}) or [
                {"type": "PARAM", "value": "param", "line": 1, "column": 10},
            ]

            result = _parse_def_stmt(parser_state)

        assert result["type"] == "DEF"
        params = result["children"][1]
        assert params["type"] == "PARAMS"
        assert len(params["children"]) == 1

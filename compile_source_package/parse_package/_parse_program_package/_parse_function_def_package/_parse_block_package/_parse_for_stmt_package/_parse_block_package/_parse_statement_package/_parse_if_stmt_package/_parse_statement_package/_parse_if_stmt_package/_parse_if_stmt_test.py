# -*- coding: utf-8 -*-
"""
Unit tests for _parse_if_stmt function.
Tests parsing of if statements: if ( expression ) block [ else block ]
"""

from unittest.mock import patch, call

# Relative import from the same package
from ._parse_if_stmt_src import _parse_if_stmt


class TestParseIfStmt:
    """Test cases for _parse_if_stmt function"""

    def test_parse_if_without_else_happy_path(self):
        """Test parsing if statement without else branch - happy path"""
        tokens = [
            {"type": "IF", "value": "if", "line": 1, "column": 1},
            {"type": "LPAREN", "value": "(", "line": 1, "column": 3},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 4},
            {"type": "RPAREN", "value": ")", "line": 1, "column": 5},
            {"type": "LBRACE", "value": "{", "line": 1, "column": 7},
            {"type": "RBRACE", "value": "}", "line": 1, "column": 8},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c",
            "error": None
        }

        condition_ast = {"type": "EXPR", "value": "x", "line": 1, "column": 4}
        then_block_ast = {"type": "BLOCK", "children": [], "line": 1, "column": 7}

        with patch("._parse_expression_package._parse_expression_src._parse_expression", return_value=condition_ast) as mock_parse_expr, \
             patch("._parse_block_package._parse_block_src._parse_block", return_value=then_block_ast) as mock_parse_block, \
             patch("._expect_token_package._expect_token_src._expect_token") as mock_expect:

            result = _parse_if_stmt(parser_state)

            assert result["type"] == "IF_STMT"
            assert result["line"] == 1
            assert result["column"] == 1
            assert result["value"] is None
            assert len(result["children"]) == 2
            assert result["children"][0] == condition_ast
            assert result["children"][1] == then_block_ast

            assert parser_state["pos"] == 5

            mock_expect.assert_has_calls([
                call(parser_state, "LPAREN"),
                call(parser_state, "RPAREN")
            ])
            mock_parse_expr.assert_called_once_with(parser_state)
            mock_parse_block.assert_called_once_with(parser_state)

    def test_parse_if_with_else_happy_path(self):
        """Test parsing if statement with else branch - happy path"""
        tokens = [
            {"type": "IF", "value": "if", "line": 2, "column": 5},
            {"type": "LPAREN", "value": "(", "line": 2, "column": 7},
            {"type": "NUMBER", "value": "1", "line": 2, "column": 8},
            {"type": "RPAREN", "value": ")", "line": 2, "column": 9},
            {"type": "LBRACE", "value": "{", "line": 2, "column": 11},
            {"type": "RBRACE", "value": "}", "line": 2, "column": 12},
            {"type": "ELSE", "value": "else", "line": 3, "column": 1},
            {"type": "LBRACE", "value": "{", "line": 3, "column": 6},
            {"type": "RBRACE", "value": "}", "line": 3, "column": 7},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c",
            "error": None
        }

        condition_ast = {"type": "EXPR", "value": "1", "line": 2, "column": 8}
        then_block_ast = {"type": "BLOCK", "children": [], "line": 2, "column": 11}
        else_block_ast = {"type": "BLOCK", "children": [], "line": 3, "column": 6}

        def parse_block_side_effect(state):
            pos = state["pos"]
            if tokens[pos]["type"] == "LBRACE" and pos == 4:
                state["pos"] = 6
                return then_block_ast
            elif tokens[pos]["type"] == "LBRACE" and pos == 7:
                state["pos"] = 9
                return else_block_ast
            return then_block_ast

        with patch("._parse_expression_package._parse_expression_src._parse_expression", return_value=condition_ast) as mock_parse_expr, \
             patch("._parse_block_package._parse_block_src._parse_block", side_effect=parse_block_side_effect) as mock_parse_block, \
             patch("._expect_token_package._expect_token_src._expect_token") as mock_expect:

            result = _parse_if_stmt(parser_state)

            assert result["type"] == "IF_STMT"
            assert result["line"] == 2
            assert result["column"] == 5
            assert result["value"] is None
            assert len(result["children"]) == 3
            assert result["children"][0] == condition_ast
            assert result["children"][1] == then_block_ast
            assert result["children"][2] == else_block_ast

            assert parser_state["pos"] == 9

            mock_expect.assert_has_calls([
                call(parser_state, "LPAREN"),
                call(parser_state, "RPAREN")
            ])
            mock_parse_expr.assert_called_once_with(parser_state)
            assert mock_parse_block.call_count == 2

    def test_parse_if_with_complex_condition(self):
        """Test parsing if statement with complex condition expression"""
        tokens = [
            {"type": "IF", "value": "if", "line": 1, "column": 1},
            {"type": "LPAREN", "value": "(", "line": 1, "column": 3},
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 4},
            {"type": "OPERATOR", "value": ">", "line": 1, "column": 5},
            {"type": "NUMBER", "value": "10", "line": 1, "column": 6},
            {"type": "RPAREN", "value": ")", "line": 1, "column": 8},
            {"type": "LBRACE", "value": "{", "line": 1, "column": 10},
            {"type": "RBRACE", "value": "}", "line": 1, "column": 11},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c",
            "error": None
        }

        condition_ast = {
            "type": "BINARY_OP",
            "children": [
                {"type": "IDENTIFIER", "value": "a"},
                {"type": "NUMBER", "value": "10"}
            ],
            "value": ">",
            "line": 1,
            "column": 4
        }
        then_block_ast = {"type": "BLOCK", "children": [], "line": 1, "column": 10}

        with patch("._parse_expression_package._parse_expression_src._parse_expression", return_value=condition_ast), \
             patch("._parse_block_package._parse_block_src._parse_block", return_value=then_block_ast), \
             patch("._expect_token_package._expect_token_src._expect_token"):

            result = _parse_if_stmt(parser_state)

            assert result["type"] == "IF_STMT"
            assert len(result["children"]) == 2
            assert result["children"][0] == condition_ast

    def test_parse_if_with_nested_blocks(self):
        """Test parsing if statement with nested blocks in then branch"""
        tokens = [
            {"type": "IF", "value": "if", "line": 1, "column": 1},
            {"type": "LPAREN", "value": "(", "line": 1, "column": 3},
            {"type": "IDENTIFIER", "value": "flag", "line": 1, "column": 4},
            {"type": "RPAREN", "value": ")", "line": 1, "column": 8},
            {"type": "LBRACE", "value": "{", "line": 1, "column": 10},
            {"type": "IDENTIFIER", "value": "x", "line": 2, "column": 2},
            {"type": "RBRACE", "value": "}", "line": 2, "column": 3},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c",
            "error": None
        }

        condition_ast = {"type": "EXPR", "value": "flag", "line": 1, "column": 4}
        then_block_ast = {
            "type": "BLOCK",
            "children": [{"type": "STMT", "value": "x"}],
            "line": 1,
            "column": 10
        }

        with patch("._parse_expression_package._parse_expression_src._parse_expression", return_value=condition_ast), \
             patch("._parse_block_package._parse_block_src._parse_block", return_value=then_block_ast), \
             patch("._expect_token_package._expect_token_src._expect_token"):

            result = _parse_if_stmt(parser_state)

            assert result["type"] == "IF_STMT"
            assert result["children"][1] == then_block_ast
            assert len(then_block_ast["children"]) == 1

    def test_parse_if_position_at_end_of_tokens_no_else(self):
        """Test parsing if when position is at end of tokens (no else possible)"""
        tokens = [
            {"type": "IF", "value": "if", "line": 1, "column": 1},
            {"type": "LPAREN", "value": "(", "line": 1, "column": 3},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 4},
            {"type": "RPAREN", "value": ")", "line": 1, "column": 5},
            {"type": "LBRACE", "value": "{", "line": 1, "column": 7},
            {"type": "RBRACE", "value": "}", "line": 1, "column": 8},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c",
            "error": None
        }

        condition_ast = {"type": "EXPR", "value": "x", "line": 1, "column": 4}
        then_block_ast = {"type": "BLOCK", "children": [], "line": 1, "column": 7}

        with patch("._parse_expression_package._parse_expression_src._parse_expression", return_value=condition_ast), \
             patch("._parse_block_package._parse_block_src._parse_block", return_value=then_block_ast), \
             patch("._expect_token_package._expect_token_src._expect_token"):

            result = _parse_if_stmt(parser_state)

            assert result["type"] == "IF_STMT"
            assert len(result["children"]) == 2
            assert parser_state["pos"] == 5

    def test_parse_if_with_else_token_but_no_block_should_be_handled_by_parse_block(self):
        """Test that else branch parsing is delegated to _parse_block"""
        tokens = [
            {"type": "IF", "value": "if", "line": 1, "column": 1},
            {"type": "LPAREN", "value": "(", "line": 1, "column": 3},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 4},
            {"type": "RPAREN", "value": ")", "line": 1, "column": 5},
            {"type": "LBRACE", "value": "{", "line": 1, "column": 7},
            {"type": "RBRACE", "value": "}", "line": 1, "column": 8},
            {"type": "ELSE", "value": "else", "line": 1, "column": 10},
            {"type": "LBRACE", "value": "{", "line": 1, "column": 15},
            {"type": "RBRACE", "value": "}", "line": 1, "column": 16},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c",
            "error": None
        }

        condition_ast = {"type": "EXPR", "value": "x", "line": 1, "column": 4}
        then_block_ast = {"type": "BLOCK", "children": [], "line": 1, "column": 7}
        else_block_ast = {"type": "BLOCK", "children": [], "line": 1, "column": 15}

        call_count = [0]

        def parse_block_side_effect(state):
            call_count[0] += 1
            pos = state["pos"]
            if call_count[0] == 1:
                state["pos"] = 6
                return then_block_ast
            else:
                state["pos"] = 8
                return else_block_ast

        with patch("._parse_expression_package._parse_expression_src._parse_expression", return_value=condition_ast), \
             patch("._parse_block_package._parse_block_src._parse_block", side_effect=parse_block_side_effect), \
             patch("._expect_token_package._expect_token_src._expect_token"):

            result = _parse_if_stmt(parser_state)

            assert result["type"] == "IF_STMT"
            assert len(result["children"]) == 3
            assert parser_state["pos"] == 8

    def test_parse_if_preserves_filename_in_state(self):
        """Test that parser_state filename is preserved"""
        tokens = [
            {"type": "IF", "value": "if", "line": 1, "column": 1},
            {"type": "LPAREN", "value": "(", "line": 1, "column": 3},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 4},
            {"type": "RPAREN", "value": ")", "line": 1, "column": 5},
            {"type": "LBRACE", "value": "{", "line": 1, "column": 7},
            {"type": "RBRACE", "value": "}", "line": 1, "column": 8},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "my_source_file.c",
            "error": None
        }

        condition_ast = {"type": "EXPR", "value": "x"}
        then_block_ast = {"type": "BLOCK", "children": []}

        with patch("._parse_expression_package._parse_expression_src._parse_expression", return_value=condition_ast), \
             patch("._parse_block_package._parse_block_src._parse_block", return_value=then_block_ast), \
             patch("._expect_token_package._expect_token_src._expect_token"):

            _parse_if_stmt(parser_state)

            assert parser_state["filename"] == "my_source_file.c"

    def test_parse_if_multiline_statement(self):
        """Test parsing multi-line if statement"""
        tokens = [
            {"type": "IF", "value": "if", "line": 5, "column": 1},
            {"type": "LPAREN", "value": "(", "line": 5, "column": 3},
            {"type": "IDENTIFIER", "value": "condition", "line": 5, "column": 4},
            {"type": "RPAREN", "value": ")", "line": 5, "column": 13},
            {"type": "LBRACE", "value": "{", "line": 5, "column": 15},
            {"type": "RBRACE", "value": "}", "line": 10, "column": 1},
            {"type": "ELSE", "value": "else", "line": 11, "column": 1},
            {"type": "LBRACE", "value": "{", "line": 11, "column": 6},
            {"type": "RBRACE", "value": "}", "line": 15, "column": 1},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c",
            "error": None
        }

        condition_ast = {"type": "EXPR", "value": "condition", "line": 5, "column": 4}
        then_block_ast = {"type": "BLOCK", "children": [], "line": 5, "column": 15}
        else_block_ast = {"type": "BLOCK", "children": [], "line": 11, "column": 6}

        call_count = [0]

        def parse_block_side_effect(state):
            call_count[0] += 1
            if call_count[0] == 1:
                state["pos"] = 6
                return then_block_ast
            else:
                state["pos"] = 8
                return else_block_ast

        with patch("._parse_expression_package._parse_expression_src._parse_expression", return_value=condition_ast), \
             patch("._parse_block_package._parse_block_src._parse_block", side_effect=parse_block_side_effect), \
             patch("._expect_token_package._expect_token_src._expect_token"):

            result = _parse_if_stmt(parser_state)

            assert result["line"] == 5
            assert result["column"] == 1
            assert len(result["children"]) == 3

    def test_parse_if_with_whitespace_tokens_between(self):
        """Test parsing if statement with various token positions"""
        tokens = [
            {"type": "IF", "value": "if", "line": 1, "column": 1},
            {"type": "LPAREN", "value": "(", "line": 1, "column": 10},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 15},
            {"type": "RPAREN", "value": ")", "line": 1, "column": 20},
            {"type": "LBRACE", "value": "{", "line": 1, "column": 25},
            {"type": "RBRACE", "value": "}", "line": 1, "column": 30},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c",
            "error": None
        }

        condition_ast = {"type": "EXPR", "value": "x", "line": 1, "column": 15}
        then_block_ast = {"type": "BLOCK", "children": [], "line": 1, "column": 25}

        with patch("._parse_expression_package._parse_expression_src._parse_expression", return_value=condition_ast), \
             patch("._parse_block_package._parse_block_src._parse_block", return_value=then_block_ast), \
             patch("._expect_token_package._expect_token_src._expect_token"):

            result = _parse_if_stmt(parser_state)

            assert result["line"] == 1
            assert result["column"] == 1
            assert result["children"][0]["line"] == 1
            assert result["children"][0]["column"] == 15

    def test_parse_if_expect_token_called_correctly(self):
        """Test that _expect_token is called with correct parameters"""
        tokens = [
            {"type": "IF", "value": "if", "line": 1, "column": 1},
            {"type": "LPAREN", "value": "(", "line": 1, "column": 3},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 4},
            {"type": "RPAREN", "value": ")", "line": 1, "column": 5},
            {"type": "LBRACE", "value": "{", "line": 1, "column": 7},
            {"type": "RBRACE", "value": "}", "line": 1, "column": 8},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c",
            "error": None
        }

        condition_ast = {"type": "EXPR", "value": "x"}
        then_block_ast = {"type": "BLOCK", "children": []}

        with patch("._parse_expression_package._parse_expression_src._parse_expression", return_value=condition_ast), \
             patch("._parse_block_package._parse_block_src._parse_block", return_value=then_block_ast), \
             patch("._expect_token_package._expect_token_src._expect_token") as mock_expect:

            _parse_if_stmt(parser_state)

            assert mock_expect.call_count == 2
            mock_expect.assert_any_call(parser_state, "LPAREN")
            mock_expect.assert_any_call(parser_state, "RPAREN")

    def test_parse_if_consumes_if_token(self):
        """Test that IF token is consumed (pos incremented)"""
        tokens = [
            {"type": "IF", "value": "if", "line": 1, "column": 1},
            {"type": "LPAREN", "value": "(", "line": 1, "column": 3},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 4},
            {"type": "RPAREN", "value": ")", "line": 1, "column": 5},
            {"type": "LBRACE", "value": "{", "line": 1, "column": 7},
            {"type": "RBRACE", "value": "}", "line": 1, "column": 8},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c",
            "error": None
        }

        condition_ast = {"type": "EXPR", "value": "x"}
        then_block_ast = {"type": "BLOCK", "children": []}

        with patch("._parse_expression_package._parse_expression_src._parse_expression", return_value=condition_ast), \
             patch("._parse_block_package._parse_block_src._parse_block", return_value=then_block_ast), \
             patch("._expect_token_package._expect_token_src._expect_token"):

            initial_pos = parser_state["pos"]
            _parse_if_stmt(parser_state)

            assert parser_state["pos"] > initial_pos
            assert parser_state["pos"] == 5
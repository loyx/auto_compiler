# -*- coding: utf-8 -*-
"""单元测试：_parse_block 函数"""

import unittest
from unittest.mock import patch

from ._parse_block_src import _parse_block


# Patch the dependencies in _parse_block_src module before any test runs
# This prevents import errors from deep dependencies
import unittest.mock as mock
_parse_statement_mock = mock.MagicMock()
_expect_token_mock = mock.MagicMock()

# Apply patches to _parse_block_src module
import sys
_module = sys.modules[__package__ + '._parse_block_src']
_module._parse_statement = _parse_statement_mock
_module._expect_token = _expect_token_mock


class TestParseBlock(unittest.TestCase):
    """_parse_block 函数测试用例"""

    def test_empty_block(self):
        """测试空块 {} 的解析"""
        tokens = [
            {"type": "LBRACE", "value": "{", "line": 1, "column": 1},
            {"type": "RBRACE", "value": "}", "line": 1, "column": 2},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c",
            "error": ""
        }

        with patch("._expect_token_package._expect_token_src._expect_token") as mock_expect:
            mock_expect.side_effect = lambda state, t_type, t_val: None

            result = _parse_block(parser_state)

            self.assertEqual(result["type"], "BLOCK")
            self.assertEqual(result["children"], [])
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            self.assertEqual(parser_state["pos"], 1)
            self.assertEqual(mock_expect.call_count, 2)

    def test_block_with_single_statement(self):
        """测试包含单条语句的块"""
        tokens = [
            {"type": "LBRACE", "value": "{", "line": 1, "column": 1},
            {"type": "SEMICOLON", "value": ";", "line": 1, "column": 5},
            {"type": "RBRACE", "value": "}", "line": 1, "column": 6},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c",
            "error": ""
        }

        mock_stmt_ast = {"type": "EMPTY_STMT", "line": 1, "column": 5}

        with patch("._parse_statement_package._parse_statement_src._parse_statement") as mock_parse_stmt:
            with patch("._expect_token_package._expect_token_src._expect_token") as mock_expect:
                mock_parse_stmt.return_value = mock_stmt_ast
                mock_expect.side_effect = lambda state, t_type, t_val: None

                result = _parse_block(parser_state)

                self.assertEqual(result["type"], "BLOCK")
                self.assertEqual(len(result["children"]), 1)
                self.assertEqual(result["children"][0], mock_stmt_ast)
                self.assertEqual(result["line"], 1)
                self.assertEqual(result["column"], 1)
                mock_parse_stmt.assert_called_once()

    def test_block_with_multiple_statements(self):
        """测试包含多条语句的块"""
        tokens = [
            {"type": "LBRACE", "value": "{", "line": 1, "column": 1},
            {"type": "IDENT", "value": "a", "line": 2, "column": 2},
            {"type": "IDENT", "value": "b", "line": 3, "column": 2},
            {"type": "RBRACE", "value": "}", "line": 4, "column": 1},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c",
            "error": ""
        }

        mock_stmt1 = {"type": "ASSIGN_STMT", "line": 2, "column": 2}
        mock_stmt2 = {"type": "ASSIGN_STMT", "line": 3, "column": 2}

        with patch("._parse_statement_package._parse_statement_src._parse_statement") as mock_parse_stmt:
            with patch("._expect_token_package._expect_token_src._expect_token") as mock_expect:
                mock_parse_stmt.side_effect = [mock_stmt1, mock_stmt2]
                mock_expect.side_effect = lambda state, t_type, t_val: None

                result = _parse_block(parser_state)

                self.assertEqual(result["type"], "BLOCK")
                self.assertEqual(len(result["children"]), 2)
                self.assertEqual(result["children"][0], mock_stmt1)
                self.assertEqual(result["children"][1], mock_stmt2)
                mock_parse_stmt.assert_has_calls([
                    unittest.mock.call(parser_state),
                    unittest.mock.call(parser_state)
                ])
                self.assertEqual(mock_parse_stmt.call_count, 2)

    def test_block_preserves_start_position(self):
        """测试 BLOCK 节点记录起始 LBRACE 的位置"""
        tokens = [
            {"type": "LBRACE", "value": "{", "line": 5, "column": 10},
            {"type": "RBRACE", "value": "}", "line": 5, "column": 11},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c",
            "error": ""
        }

        with patch("._expect_token_package._expect_token_src._expect_token") as mock_expect:
            mock_expect.side_effect = lambda state, t_type, t_val: None

            result = _parse_block(parser_state)

            self.assertEqual(result["line"], 5)
            self.assertEqual(result["column"], 10)

    def test_eof_without_lbrace_raises_error(self):
        """测试在文件末尾没有 LBRACE 时抛出 SyntaxError"""
        tokens = []
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c",
            "error": ""
        }

        with self.assertRaises(SyntaxError) as context:
            _parse_block(parser_state)

        self.assertIn("Expected '{'", str(context.exception))

    def test_eof_without_rbrace_raises_error(self):
        """测试块没有闭合 RBRACE 时抛出 SyntaxError"""
        tokens = [
            {"type": "LBRACE", "value": "{", "line": 1, "column": 1},
            {"type": "IDENT", "value": "a", "line": 1, "column": 3},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c",
            "error": ""
        }

        mock_stmt = {"type": "ASSIGN_STMT", "line": 1, "column": 3}

        with patch("._parse_statement_package._parse_statement_src._parse_statement") as mock_parse_stmt:
            with patch("._expect_token_package._expect_token_src._expect_token") as mock_expect:
                mock_parse_stmt.return_value = mock_stmt
                mock_expect.side_effect = lambda state, t_type, t_val: None

                with self.assertRaises(SyntaxError):
                    _parse_block(parser_state)

    def test_expect_token_called_for_lbrace_and_rbrace(self):
        """验证 _expect_token 被正确调用以消费 LBRACE 和 RBRACE"""
        tokens = [
            {"type": "LBRACE", "value": "{", "line": 1, "column": 1},
            {"type": "RBRACE", "value": "}", "line": 1, "column": 2},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c",
            "error": ""
        }

        with patch("._expect_token_package._expect_token_src._expect_token") as mock_expect:
            mock_expect.side_effect = lambda state, t_type, t_val: None

            _parse_block(parser_state)

            self.assertEqual(mock_expect.call_count, 2)
            mock_expect.assert_any_call(parser_state, "LBRACE", "{")
            mock_expect.assert_any_call(parser_state, "RBRACE", "}")

    def test_statement_parse_error_propagates(self):
        """测试语句解析错误向上传播"""
        tokens = [
            {"type": "LBRACE", "value": "{", "line": 1, "column": 1},
            {"type": "INVALID", "value": "x", "line": 1, "column": 3},
            {"type": "RBRACE", "value": "}", "line": 1, "column": 4},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c",
            "error": ""
        }

        with patch("._parse_statement_package._parse_statement_src._parse_statement") as mock_parse_stmt:
            with patch("._expect_token_package._expect_token_src._expect_token") as mock_expect:
                mock_parse_stmt.side_effect = SyntaxError("Invalid statement")
                mock_expect.side_effect = lambda state, t_type, t_val: None

                with self.assertRaises(SyntaxError) as context:
                    _parse_block(parser_state)

                self.assertIn("Invalid statement", str(context.exception))
                mock_parse_stmt.assert_called_once()

    def test_pos_updated_after_parsing(self):
        """测试解析完成后 pos 指向 RBRACE 之后"""
        tokens = [
            {"type": "LBRACE", "value": "{", "line": 1, "column": 1},
            {"type": "SEMICOLON", "value": ";", "line": 1, "column": 3},
            {"type": "RBRACE", "value": "}", "line": 1, "column": 4},
            {"type": "IDENT", "value": "next", "line": 1, "column": 6},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c",
            "error": ""
        }

        mock_stmt = {"type": "EMPTY_STMT", "line": 1, "column": 3}

        def expect_token_side_effect(state, t_type, t_val):
            state["pos"] += 1

        def parse_stmt_side_effect(state):
            state["pos"] += 1
            return mock_stmt

        with patch("._parse_statement_package._parse_statement_src._parse_statement") as mock_parse_stmt:
            with patch("._expect_token_package._expect_token_src._expect_token") as mock_expect:
                mock_parse_stmt.side_effect = parse_stmt_side_effect
                mock_expect.side_effect = expect_token_side_effect

                result = _parse_block(parser_state)

                self.assertEqual(parser_state["pos"], 3)
                self.assertEqual(tokens[parser_state["pos"]]["type"], "IDENT")


if __name__ == "__main__":
    unittest.main()

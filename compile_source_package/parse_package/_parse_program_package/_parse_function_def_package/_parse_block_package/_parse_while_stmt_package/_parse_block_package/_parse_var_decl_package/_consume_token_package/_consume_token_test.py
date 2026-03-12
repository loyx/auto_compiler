# -*- coding: utf-8 -*-
"""
单元测试文件：_consume_token 函数测试
"""

import unittest
from typing import Any, Dict

from ._consume_token_src import _consume_token


Token = Dict[str, Any]
ParserState = Dict[str, Any]


class TestConsumeToken(unittest.TestCase):
    """_consume_token 函数测试用例"""

    def test_consume_token_success(self):
        """测试成功消费匹配类型的 token"""
        tokens: list[Token] = [
            {"type": "IDENT", "value": "x", "line": 1, "column": 1},
            {"type": "ASSIGN", "value": "=", "line": 1, "column": 3},
            {"type": "NUMBER", "value": "42", "line": 1, "column": 5},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c",
        }

        new_state = _consume_token(parser_state, "IDENT")

        self.assertEqual(new_state["pos"], 1)
        self.assertEqual(new_state["tokens"], tokens)
        self.assertEqual(new_state["filename"], "test.c")

    def test_consume_token_advances_position(self):
        """测试消费 token 后位置正确推进"""
        tokens: list[Token] = [
            {"type": "KEYWORD", "value": "while", "line": 1, "column": 1},
            {"type": "LPAREN", "value": "(", "line": 1, "column": 7},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c",
        }

        new_state = _consume_token(parser_state, "KEYWORD")

        self.assertEqual(new_state["pos"], 1)

    def test_consume_token_from_middle_position(self):
        """测试从中间位置消费 token"""
        tokens: list[Token] = [
            {"type": "IDENT", "value": "x", "line": 1, "column": 1},
            {"type": "ASSIGN", "value": "=", "line": 1, "column": 3},
            {"type": "NUMBER", "value": "42", "line": 1, "column": 5},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 1,
            "filename": "test.c",
        }

        new_state = _consume_token(parser_state, "ASSIGN")

        self.assertEqual(new_state["pos"], 2)

    def test_consume_token_from_last_position(self):
        """测试从最后一个位置消费 token"""
        tokens: list[Token] = [
            {"type": "IDENT", "value": "x", "line": 1, "column": 1},
            {"type": "ASSIGN", "value": "=", "line": 1, "column": 3},
            {"type": "NUMBER", "value": "42", "line": 1, "column": 5},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 2,
            "filename": "test.c",
        }

        new_state = _consume_token(parser_state, "NUMBER")

        self.assertEqual(new_state["pos"], 3)

    def test_consume_token_does_not_modify_original(self):
        """测试原始 parser_state 不被修改"""
        tokens: list[Token] = [
            {"type": "IDENT", "value": "x", "line": 1, "column": 1},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c",
        }
        original_pos = parser_state["pos"]

        _consume_token(parser_state, "IDENT")

        self.assertEqual(parser_state["pos"], original_pos)

    def test_consume_token_type_mismatch(self):
        """测试 token 类型不匹配时抛出 SyntaxError"""
        tokens: list[Token] = [
            {"type": "IDENT", "value": "x", "line": 1, "column": 1},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c",
        }

        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, "NUMBER")

        self.assertIn("Expected NUMBER, got IDENT", str(context.exception))

    def test_consume_token_empty_tokens(self):
        """测试空 tokens 列表时抛出 SyntaxError"""
        tokens: list[Token] = []
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c",
        }

        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, "IDENT")

        self.assertIn("Unexpected end of input", str(context.exception))

    def test_consume_token_pos_at_end(self):
        """测试 pos 在 tokens 末尾时抛出 SyntaxError"""
        tokens: list[Token] = [
            {"type": "IDENT", "value": "x", "line": 1, "column": 1},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 1,
            "filename": "test.c",
        }

        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, "IDENT")

        self.assertIn("Unexpected end of input", str(context.exception))

    def test_consume_token_pos_beyond_end(self):
        """测试 pos 超出 tokens 范围时抛出 SyntaxError"""
        tokens: list[Token] = [
            {"type": "IDENT", "value": "x", "line": 1, "column": 1},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 5,
            "filename": "test.c",
        }

        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, "IDENT")

        self.assertIn("Unexpected end of input", str(context.exception))

    def test_consume_token_error_message_includes_expected_type(self):
        """测试错误消息包含期望的 token 类型"""
        tokens: list[Token] = [
            {"type": "SEMICOLON", "value": ";", "line": 1, "column": 1},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c",
        }

        with self.assertRaises(SyntaxError) as context:
            _consume_token(parser_state, "IDENT")

        self.assertIn("IDENT", str(context.exception))
        self.assertIn("SEMICOLON", str(context.exception))

    def test_consume_token_preserves_other_fields(self):
        """测试返回状态保留其他字段"""
        tokens: list[Token] = [
            {"type": "IDENT", "value": "x", "line": 1, "column": 1},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c",
            "extra_field": "extra_value",
        }

        new_state = _consume_token(parser_state, "IDENT")

        self.assertEqual(new_state["filename"], "test.c")
        self.assertEqual(new_state["extra_field"], "extra_value")


if __name__ == "__main__":
    unittest.main()

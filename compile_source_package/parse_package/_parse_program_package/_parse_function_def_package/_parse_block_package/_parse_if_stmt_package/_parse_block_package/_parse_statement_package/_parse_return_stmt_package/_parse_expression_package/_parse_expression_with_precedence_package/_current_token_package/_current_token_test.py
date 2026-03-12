# -*- coding: utf-8 -*-
"""单元测试：_current_token 函数"""

import unittest

# 相对导入被测模块
from ._current_token_src import _current_token, Token, ParserState


class TestCurrentToken(unittest.TestCase):
    """_current_token 函数的单元测试类"""

    def test_get_first_token(self):
        """测试获取第一个 token（pos=0）"""
        tokens: list[Token] = [
            {"type": "IDENT", "value": "x", "line": 1, "column": 1},
            {"type": "OP", "value": "=", "line": 1, "column": 3},
            {"type": "NUM", "value": "42", "line": 1, "column": 5},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
            "error": "",
        }
        
        result = _current_token(parser_state)
        
        self.assertIsNotNone(result)
        self.assertEqual(result["type"], "IDENT")
        self.assertEqual(result["value"], "x")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)

    def test_get_middle_token(self):
        """测试获取中间的 token"""
        tokens: list[Token] = [
            {"type": "IDENT", "value": "x", "line": 1, "column": 1},
            {"type": "OP", "value": "=", "line": 1, "column": 3},
            {"type": "NUM", "value": "42", "line": 1, "column": 5},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 1,
            "filename": "test.py",
            "error": "",
        }
        
        result = _current_token(parser_state)
        
        self.assertIsNotNone(result)
        self.assertEqual(result["type"], "OP")
        self.assertEqual(result["value"], "=")

    def test_get_last_token(self):
        """测试获取最后一个 token（pos=len(tokens)-1）"""
        tokens: list[Token] = [
            {"type": "IDENT", "value": "x", "line": 1, "column": 1},
            {"type": "OP", "value": "=", "line": 1, "column": 3},
            {"type": "NUM", "value": "42", "line": 1, "column": 5},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 2,
            "filename": "test.py",
            "error": "",
        }
        
        result = _current_token(parser_state)
        
        self.assertIsNotNone(result)
        self.assertEqual(result["type"], "NUM")
        self.assertEqual(result["value"], "42")

    def test_pos_equals_len_returns_none(self):
        """测试 pos 等于 tokens 长度时返回 None"""
        tokens: list[Token] = [
            {"type": "IDENT", "value": "x", "line": 1, "column": 1},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 1,
            "filename": "test.py",
            "error": "",
        }
        
        result = _current_token(parser_state)
        
        self.assertIsNone(result)

    def test_pos_greater_than_len_returns_none(self):
        """测试 pos 大于 tokens 长度时返回 None"""
        tokens: list[Token] = [
            {"type": "IDENT", "value": "x", "line": 1, "column": 1},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 5,
            "filename": "test.py",
            "error": "",
        }
        
        result = _current_token(parser_state)
        
        self.assertIsNone(result)

    def test_empty_tokens_returns_none(self):
        """测试空 tokens 列表时返回 None"""
        parser_state: ParserState = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py",
            "error": "",
        }
        
        result = _current_token(parser_state)
        
        self.assertIsNone(result)

    def test_missing_tokens_key_defaults_to_empty(self):
        """测试 parser_state 缺少 tokens 键时默认使用空列表"""
        parser_state: ParserState = {
            "pos": 0,
            "filename": "test.py",
            "error": "",
        }
        
        result = _current_token(parser_state)
        
        self.assertIsNone(result)

    def test_missing_pos_key_defaults_to_zero(self):
        """测试 parser_state 缺少 pos 键时默认使用 0"""
        tokens: list[Token] = [
            {"type": "IDENT", "value": "x", "line": 1, "column": 1},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "filename": "test.py",
            "error": "",
        }
        
        result = _current_token(parser_state)
        
        self.assertIsNotNone(result)
        self.assertEqual(result["type"], "IDENT")
        self.assertEqual(result["value"], "x")

    def test_does_not_modify_pos(self):
        """测试函数不修改 parser_state 的 pos（无副作用）"""
        tokens: list[Token] = [
            {"type": "IDENT", "value": "x", "line": 1, "column": 1},
            {"type": "OP", "value": "=", "line": 1, "column": 3},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
            "error": "",
        }
        original_pos = parser_state["pos"]
        
        _current_token(parser_state)
        
        self.assertEqual(parser_state["pos"], original_pos)
        
        _current_token(parser_state)
        _current_token(parser_state)
        
        self.assertEqual(parser_state["pos"], original_pos)

    def test_token_with_all_fields(self):
        """测试包含所有字段的完整 token"""
        tokens: list[Token] = [
            {
                "type": "STRING",
                "value": '"hello world"',
                "line": 10,
                "column": 25,
            },
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
            "error": "",
        }
        
        result = _current_token(parser_state)
        
        self.assertIsNotNone(result)
        self.assertEqual(result["type"], "STRING")
        self.assertEqual(result["value"], '"hello world"')
        self.assertEqual(result["line"], 10)
        self.assertEqual(result["column"], 25)


if __name__ == "__main__":
    unittest.main()

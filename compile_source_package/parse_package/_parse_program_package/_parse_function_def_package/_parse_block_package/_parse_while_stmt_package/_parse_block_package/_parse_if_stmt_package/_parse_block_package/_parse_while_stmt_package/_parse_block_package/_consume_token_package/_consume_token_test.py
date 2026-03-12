# -*- coding: utf-8 -*-
"""
单元测试：_consume_token 函数
测试文件位于与被测代码相同的包层级，使用相对导入
"""

import unittest
from typing import Any, Dict

from ._consume_token_src import _consume_token

Token = Dict[str, Any]
ParserState = Dict[str, Any]


class TestConsumeToken(unittest.TestCase):
    """测试 _consume_token 函数的各种场景"""

    def test_consume_token_success(self):
        """Happy path: token 类型匹配，pos 递增，返回 True"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "=", "line": 1, "column": 3},
            ],
            "pos": 0,
            "filename": "test.py",
        }
        
        result = _consume_token(parser_state, "IDENTIFIER")
        
        self.assertTrue(result)
        self.assertEqual(parser_state["pos"], 1)

    def test_consume_token_type_mismatch(self):
        """Token 类型不匹配，返回 False，pos 不变"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 0,
            "filename": "test.py",
        }
        
        result = _consume_token(parser_state, "OPERATOR")
        
        self.assertFalse(result)
        self.assertEqual(parser_state["pos"], 0)

    def test_consume_token_empty_tokens(self):
        """tokens 列表为空，返回 False"""
        parser_state: ParserState = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py",
        }
        
        result = _consume_token(parser_state, "IDENTIFIER")
        
        self.assertFalse(result)
        self.assertEqual(parser_state["pos"], 0)

    def test_consume_token_pos_at_end(self):
        """pos 在 tokens 末尾（越界），返回 False"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 1,  # pos 等于 tokens 长度
            "filename": "test.py",
        }
        
        result = _consume_token(parser_state, "IDENTIFIER")
        
        self.assertFalse(result)
        self.assertEqual(parser_state["pos"], 1)

    def test_consume_token_pos_beyond_end(self):
        """pos 超出 tokens 长度（越界），返回 False"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 5,  # pos 远大于 tokens 长度
            "filename": "test.py",
        }
        
        result = _consume_token(parser_state, "IDENTIFIER")
        
        self.assertFalse(result)
        self.assertEqual(parser_state["pos"], 5)

    def test_consume_token_missing_type_field(self):
        """Token 缺少 type 字段，返回 False"""
        parser_state: ParserState = {
            "tokens": [
                {"value": "x", "line": 1, "column": 1},  # 没有 type 字段
            ],
            "pos": 0,
            "filename": "test.py",
        }
        
        result = _consume_token(parser_state, "IDENTIFIER")
        
        self.assertFalse(result)
        self.assertEqual(parser_state["pos"], 0)

    def test_consume_token_missing_tokens_key(self):
        """parser_state 缺少 tokens 键，返回 False"""
        parser_state: ParserState = {
            "pos": 0,
            "filename": "test.py",
        }
        
        result = _consume_token(parser_state, "IDENTIFIER")
        
        self.assertFalse(result)
        self.assertEqual(parser_state["pos"], 0)

    def test_consume_token_missing_pos_key(self):
        """parser_state 缺少 pos 键，使用默认值 0"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "filename": "test.py",
        }
        
        result = _consume_token(parser_state, "IDENTIFIER")
        
        self.assertTrue(result)
        self.assertEqual(parser_state["pos"], 1)

    def test_consume_token_multiple_consumes(self):
        """连续消费多个 token"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "KEYWORD", "value": "while", "line": 1, "column": 1},
                {"type": "LPAREN", "value": "(", "line": 1, "column": 7},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 8},
                {"type": "RPAREN", "value": ")", "line": 1, "column": 9},
            ],
            "pos": 0,
            "filename": "test.py",
        }
        
        # 消费 KEYWORD
        self.assertTrue(_consume_token(parser_state, "KEYWORD"))
        self.assertEqual(parser_state["pos"], 1)
        
        # 消费 LPAREN
        self.assertTrue(_consume_token(parser_state, "LPAREN"))
        self.assertEqual(parser_state["pos"], 2)
        
        # 消费 IDENTIFIER
        self.assertTrue(_consume_token(parser_state, "IDENTIFIER"))
        self.assertEqual(parser_state["pos"], 3)
        
        # 消费 RPAREN
        self.assertTrue(_consume_token(parser_state, "RPAREN"))
        self.assertEqual(parser_state["pos"], 4)
        
        # 再次消费应该失败（越界）
        self.assertFalse(_consume_token(parser_state, "SEMICOLON"))
        self.assertEqual(parser_state["pos"], 4)

    def test_consume_token_state_unchanged_on_failure(self):
        """消费失败时 parser_state 完全不变"""
        original_state: ParserState = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 0,
            "filename": "test.py",
        }
        parser_state = original_state.copy()
        parser_state["tokens"] = original_state["tokens"].copy()
        
        result = _consume_token(parser_state, "OPERATOR")
        
        self.assertFalse(result)
        self.assertEqual(parser_state["pos"], original_state["pos"])
        self.assertEqual(parser_state["tokens"], original_state["tokens"])
        self.assertEqual(parser_state["filename"], original_state["filename"])

    def test_consume_token_empty_string_type(self):
        """token_type 为空字符串的边界情况"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 0,
            "filename": "test.py",
        }
        
        result = _consume_token(parser_state, "")
        
        self.assertTrue(result)
        self.assertEqual(parser_state["pos"], 1)

    def test_consume_token_none_type_in_token(self):
        """Token 的 type 字段为 None 的情况"""
        parser_state: ParserState = {
            "tokens": [
                {"type": None, "value": "x", "line": 1, "column": 1},
            ],
            "pos": 0,
            "filename": "test.py",
        }
        
        result = _consume_token(parser_state, "IDENTIFIER")
        
        self.assertFalse(result)
        self.assertEqual(parser_state["pos"], 0)


if __name__ == "__main__":
    unittest.main()

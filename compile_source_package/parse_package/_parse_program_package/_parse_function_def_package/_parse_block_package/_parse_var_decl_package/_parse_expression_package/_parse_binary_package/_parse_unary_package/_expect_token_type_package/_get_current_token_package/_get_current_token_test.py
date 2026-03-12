# -*- coding: utf-8 -*-
"""
单元测试文件：_get_current_token
测试目标：验证从 parser_state 获取当前 token 的逻辑
"""

import unittest

# 相对导入被测试模块
from ._get_current_token_src import _get_current_token


class TestGetCurrentToken(unittest.TestCase):
    """_get_current_token 函数的单元测试类"""

    def test_get_first_token(self):
        """测试获取第一个 token (pos=0)"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "=", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "42", "line": 1, "column": 5},
            ],
            "pos": 0,
            "filename": "test.c"
        }
        result = _get_current_token(parser_state)
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "x")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)

    def test_get_middle_token(self):
        """测试获取中间的 token"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "=", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "42", "line": 1, "column": 5},
            ],
            "pos": 1,
            "filename": "test.c"
        }
        result = _get_current_token(parser_state)
        self.assertEqual(result["type"], "OPERATOR")
        self.assertEqual(result["value"], "=")

    def test_get_last_token(self):
        """测试获取最后一个 token (pos=len(tokens)-1)"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "=", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "42", "line": 1, "column": 5},
            ],
            "pos": 2,
            "filename": "test.c"
        }
        result = _get_current_token(parser_state)
        self.assertEqual(result["type"], "NUMBER")
        self.assertEqual(result["value"], "42")

    def test_pos_at_end_returns_none(self):
        """测试 pos 等于 tokens 长度时返回 None"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "=", "line": 1, "column": 3},
            ],
            "pos": 2,
            "filename": "test.c"
        }
        result = _get_current_token(parser_state)
        self.assertIsNone(result)

    def test_pos_beyond_end_returns_none(self):
        """测试 pos 超过 tokens 长度时返回 None"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 5,
            "filename": "test.c"
        }
        result = _get_current_token(parser_state)
        self.assertIsNone(result)

    def test_empty_tokens_list_returns_none(self):
        """测试 tokens 为空列表时返回 None"""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.c"
        }
        result = _get_current_token(parser_state)
        self.assertIsNone(result)

    def test_missing_tokens_key_uses_default(self):
        """测试 parser_state 缺少 tokens 键时使用默认空列表"""
        parser_state = {
            "pos": 0,
            "filename": "test.c"
        }
        result = _get_current_token(parser_state)
        self.assertIsNone(result)

    def test_missing_pos_key_uses_default_zero(self):
        """测试 parser_state 缺少 pos 键时使用默认值 0"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "=", "line": 1, "column": 3},
            ],
            "filename": "test.c"
        }
        result = _get_current_token(parser_state)
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "x")

    def test_missing_both_tokens_and_pos(self):
        """测试 parser_state 同时缺少 tokens 和 pos 键"""
        parser_state = {
            "filename": "test.c"
        }
        result = _get_current_token(parser_state)
        self.assertIsNone(result)

    def test_empty_parser_state(self):
        """测试 parser_state 为空字典"""
        parser_state = {}
        result = _get_current_token(parser_state)
        self.assertIsNone(result)

    def test_token_with_all_fields(self):
        """测试 token 包含所有标准字段"""
        parser_state = {
            "tokens": [
                {
                    "type": "STRING_LITERAL",
                    "value": '"hello"',
                    "line": 10,
                    "column": 25
                },
            ],
            "pos": 0,
            "filename": "test.c"
        }
        result = _get_current_token(parser_state)
        self.assertEqual(result["type"], "STRING_LITERAL")
        self.assertEqual(result["value"], '"hello"')
        self.assertEqual(result["line"], 10)
        self.assertEqual(result["column"], 25)

    def test_no_side_effects_on_parser_state(self):
        """测试函数不修改 parser_state"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 0,
            "filename": "test.c"
        }
        original_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 0,
            "filename": "test.c"
        }
        _get_current_token(parser_state)
        self.assertEqual(parser_state, original_state)


if __name__ == "__main__":
    unittest.main()

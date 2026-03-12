#!/usr/bin/env python3
"""
单元测试文件：测试 _current_token 函数
"""

import unittest

# 相对导入被测试模块
from ._current_token_src import _current_token


class TestCurrentToken(unittest.TestCase):
    """测试 _current_token 函数的各种场景"""

    def test_current_token_valid_position_zero(self):
        """测试 pos=0 时返回第一个 token"""
        parser_state = {
            "tokens": [
                {"type": "IDENT", "value": "x", "line": 1, "column": 1},
                {"type": "ASSIGN", "value": "=", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "42", "line": 1, "column": 5},
            ],
            "pos": 0,
            "filename": "test.c",
        }
        result = _current_token(parser_state)
        self.assertEqual(result, {"type": "IDENT", "value": "x", "line": 1, "column": 1})

    def test_current_token_valid_position_middle(self):
        """测试 pos 在中间位置时返回对应 token"""
        parser_state = {
            "tokens": [
                {"type": "IDENT", "value": "x", "line": 1, "column": 1},
                {"type": "ASSIGN", "value": "=", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "42", "line": 1, "column": 5},
            ],
            "pos": 1,
            "filename": "test.c",
        }
        result = _current_token(parser_state)
        self.assertEqual(result, {"type": "ASSIGN", "value": "=", "line": 1, "column": 3})

    def test_current_token_valid_position_last(self):
        """测试 pos 在最后一个位置时返回最后一个 token"""
        parser_state = {
            "tokens": [
                {"type": "IDENT", "value": "x", "line": 1, "column": 1},
                {"type": "ASSIGN", "value": "=", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "42", "line": 1, "column": 5},
            ],
            "pos": 2,
            "filename": "test.c",
        }
        result = _current_token(parser_state)
        self.assertEqual(result, {"type": "NUMBER", "value": "42", "line": 1, "column": 5})

    def test_current_token_pos_out_of_bounds_positive(self):
        """测试 pos 超出 tokens 范围（正数）时返回 None"""
        parser_state = {
            "tokens": [
                {"type": "IDENT", "value": "x", "line": 1, "column": 1},
                {"type": "ASSIGN", "value": "=", "line": 1, "column": 3},
            ],
            "pos": 5,
            "filename": "test.c",
        }
        result = _current_token(parser_state)
        self.assertIsNone(result)

    def test_current_token_pos_negative(self):
        """测试 pos 为负数时返回 None"""
        parser_state = {
            "tokens": [
                {"type": "IDENT", "value": "x", "line": 1, "column": 1},
                {"type": "ASSIGN", "value": "=", "line": 1, "column": 3},
            ],
            "pos": -1,
            "filename": "test.c",
        }
        result = _current_token(parser_state)
        self.assertIsNone(result)

    def test_current_token_empty_tokens_list(self):
        """测试 tokens 为空列表时返回 None"""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.c",
        }
        result = _current_token(parser_state)
        self.assertIsNone(result)

    def test_current_token_missing_tokens_key(self):
        """测试 parser_state 缺少 tokens 键时返回 None（使用默认空列表）"""
        parser_state = {
            "pos": 0,
            "filename": "test.c",
        }
        result = _current_token(parser_state)
        self.assertIsNone(result)

    def test_current_token_missing_pos_key(self):
        """测试 parser_state 缺少 pos 键时使用默认值 0"""
        parser_state = {
            "tokens": [
                {"type": "IDENT", "value": "x", "line": 1, "column": 1},
            ],
            "filename": "test.c",
        }
        result = _current_token(parser_state)
        self.assertEqual(result, {"type": "IDENT", "value": "x", "line": 1, "column": 1})

    def test_current_token_single_token(self):
        """测试只有一个 token 的情况"""
        parser_state = {
            "tokens": [
                {"type": "SEMICOLON", "value": ";", "line": 1, "column": 10},
            ],
            "pos": 0,
            "filename": "test.c",
        }
        result = _current_token(parser_state)
        self.assertEqual(result, {"type": "SEMICOLON", "value": ";", "line": 1, "column": 10})

    def test_current_token_pos_at_boundary(self):
        """测试 pos 刚好等于 tokens 长度时返回 None（边界情况）"""
        parser_state = {
            "tokens": [
                {"type": "IDENT", "value": "x", "line": 1, "column": 1},
                {"type": "ASSIGN", "value": "=", "line": 1, "column": 3},
            ],
            "pos": 2,  # 等于 len(tokens)
            "filename": "test.c",
        }
        result = _current_token(parser_state)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()

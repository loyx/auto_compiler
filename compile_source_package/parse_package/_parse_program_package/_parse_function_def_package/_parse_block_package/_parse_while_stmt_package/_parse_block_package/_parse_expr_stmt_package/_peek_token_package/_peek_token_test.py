# -*- coding: utf-8 -*-
"""
单元测试文件：_peek_token 函数测试
测试查看当前位置 token 但不消费的功能
"""

import unittest

# 相对导入被测模块
from ._peek_token_src import _peek_token


class TestPeekToken(unittest.TestCase):
    """_peek_token 函数的单元测试类"""

    def test_peek_token_valid_position(self):
        """测试在有效位置查看 token"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "=", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "42", "line": 1, "column": 5},
            ],
            "pos": 1,
            "filename": "test.py",
        }
        
        result = _peek_token(parser_state)
        
        self.assertIsNotNone(result)
        self.assertEqual(result["type"], "OPERATOR")
        self.assertEqual(result["value"], "=")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 3)

    def test_peek_token_first_position(self):
        """测试在第一个位置 (pos=0) 查看 token"""
        parser_state = {
            "tokens": [
                {"type": "KEYWORD", "value": "while", "line": 1, "column": 1},
                {"type": "LPAREN", "value": "(", "line": 1, "column": 7},
            ],
            "pos": 0,
            "filename": "test.py",
        }
        
        result = _peek_token(parser_state)
        
        self.assertIsNotNone(result)
        self.assertEqual(result["type"], "KEYWORD")
        self.assertEqual(result["value"], "while")

    def test_peek_token_at_end_boundary(self):
        """测试 pos 等于 tokens 长度时返回 None"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "NUMBER", "value": "10", "line": 1, "column": 3},
            ],
            "pos": 2,
            "filename": "test.py",
        }
        
        result = _peek_token(parser_state)
        
        self.assertIsNone(result)

    def test_peek_token_beyond_end(self):
        """测试 pos 超出 tokens 长度时返回 None"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 5,
            "filename": "test.py",
        }
        
        result = _peek_token(parser_state)
        
        self.assertIsNone(result)

    def test_peek_token_empty_tokens(self):
        """测试 tokens 为空列表时返回 None"""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py",
        }
        
        result = _peek_token(parser_state)
        
        self.assertIsNone(result)

    def test_peek_token_does_not_modify_state(self):
        """测试 _peek_token 不修改 parser_state"""
        original_token = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        parser_state = {
            "tokens": [original_token],
            "pos": 0,
            "filename": "test.py",
        }
        
        original_tokens_copy = list(parser_state["tokens"])
        original_pos = parser_state["pos"]
        
        _peek_token(parser_state)
        
        self.assertEqual(parser_state["tokens"], original_tokens_copy)
        self.assertEqual(parser_state["pos"], original_pos)
        self.assertIs(parser_state["tokens"][0], original_token)

    def test_peek_token_missing_tokens_key(self):
        """测试 parser_state 缺少 tokens 键时使用默认空列表"""
        parser_state = {
            "pos": 0,
            "filename": "test.py",
        }
        
        result = _peek_token(parser_state)
        
        self.assertIsNone(result)

    def test_peek_token_missing_pos_key(self):
        """测试 parser_state 缺少 pos 键时使用默认值 0"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "filename": "test.py",
        }
        
        result = _peek_token(parser_state)
        
        self.assertIsNotNone(result)
        self.assertEqual(result["value"], "x")

    def test_peek_token_missing_both_keys(self):
        """测试 parser_state 缺少 tokens 和 pos 键时使用默认值"""
        parser_state = {
            "filename": "test.py",
        }
        
        result = _peek_token(parser_state)
        
        self.assertIsNone(result)

    def test_peek_token_returns_same_token_on_multiple_calls(self):
        """测试多次调用返回相同的 token 对象引用"""
        token = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        parser_state = {
            "tokens": [token],
            "pos": 0,
            "filename": "test.py",
        }
        
        result1 = _peek_token(parser_state)
        result2 = _peek_token(parser_state)
        
        self.assertIs(result1, result2)
        self.assertIs(result1, token)


if __name__ == "__main__":
    unittest.main()

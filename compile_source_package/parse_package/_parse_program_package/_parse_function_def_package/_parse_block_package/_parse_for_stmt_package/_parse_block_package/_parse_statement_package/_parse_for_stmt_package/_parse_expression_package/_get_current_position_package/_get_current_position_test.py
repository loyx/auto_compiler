#!/usr/bin/env python3
"""
单元测试文件：_get_current_position 函数测试
测试目标：验证从 ParserState 中获取当前 token 位置信息的正确性
"""

import unittest

# 相对导入被测模块
from ._get_current_position_src import _get_current_position, ParserState


class TestGetCurrentPosition(unittest.TestCase):
    """_get_current_position 函数的单元测试类"""

    def test_happy_path_normal_token(self):
        """测试正常情况：pos 在有效范围内，token 有完整的 line 和 column"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "IDENT", "value": "x", "line": 1, "column": 5},
                {"type": "OP", "value": "=", "line": 1, "column": 7},
                {"type": "NUM", "value": "42", "line": 1, "column": 9},
            ],
            "pos": 1,
            "filename": "test.py"
        }
        result = _get_current_position(parser_state)
        self.assertEqual(result, (1, 7))

    def test_happy_path_first_token(self):
        """测试边界值：pos=0，第一个 token"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "KEYWORD", "value": "def", "line": 10, "column": 1},
            ],
            "pos": 0,
            "filename": "test.py"
        }
        result = _get_current_position(parser_state)
        self.assertEqual(result, (10, 1))

    def test_happy_path_last_token(self):
        """测试边界值：pos=len(tokens)-1，最后一个 token"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "IDENT", "value": "a", "line": 5, "column": 1},
                {"type": "OP", "value": "+", "line": 5, "column": 3},
                {"type": "IDENT", "value": "b", "line": 5, "column": 5},
            ],
            "pos": 2,
            "filename": "test.py"
        }
        result = _get_current_position(parser_state)
        self.assertEqual(result, (5, 5))

    def test_empty_tokens(self):
        """测试非法输入：tokens 为空列表"""
        parser_state: ParserState = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }
        result = _get_current_position(parser_state)
        self.assertEqual(result, (0, 0))

    def test_missing_tokens_key(self):
        """测试非法输入：parser_state 缺少 tokens 键"""
        parser_state: ParserState = {
            "pos": 0,
            "filename": "test.py"
        }
        result = _get_current_position(parser_state)
        self.assertEqual(result, (0, 0))

    def test_pos_negative(self):
        """测试非法输入：pos 为负数"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "IDENT", "value": "x", "line": 1, "column": 5},
            ],
            "pos": -1,
            "filename": "test.py"
        }
        result = _get_current_position(parser_state)
        self.assertEqual(result, (0, 0))

    def test_pos_out_of_range(self):
        """测试非法输入：pos 大于等于 tokens 长度"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "IDENT", "value": "x", "line": 1, "column": 5},
                {"type": "OP", "value": "=", "line": 1, "column": 7},
            ],
            "pos": 5,
            "filename": "test.py"
        }
        result = _get_current_position(parser_state)
        self.assertEqual(result, (0, 0))

    def test_pos_equal_to_length(self):
        """测试边界值：pos 等于 tokens 长度"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "IDENT", "value": "x", "line": 1, "column": 5},
            ],
            "pos": 1,
            "filename": "test.py"
        }
        result = _get_current_position(parser_state)
        self.assertEqual(result, (0, 0))

    def test_token_missing_line(self):
        """测试 token 缺少 line 字段，应返回默认值 0"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "IDENT", "value": "x", "column": 5},
            ],
            "pos": 0,
            "filename": "test.py"
        }
        result = _get_current_position(parser_state)
        self.assertEqual(result, (0, 5))

    def test_token_missing_column(self):
        """测试 token 缺少 column 字段，应返回默认值 0"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "IDENT", "value": "x", "line": 10},
            ],
            "pos": 0,
            "filename": "test.py"
        }
        result = _get_current_position(parser_state)
        self.assertEqual(result, (10, 0))

    def test_token_missing_both_line_and_column(self):
        """测试 token 同时缺少 line 和 column 字段"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "IDENT", "value": "x"},
            ],
            "pos": 0,
            "filename": "test.py"
        }
        result = _get_current_position(parser_state)
        self.assertEqual(result, (0, 0))

    def test_no_side_effect(self):
        """测试无副作用：调用后 parser_state 不被修改"""
        import copy
        original_state: ParserState = {
            "tokens": [
                {"type": "IDENT", "value": "x", "line": 1, "column": 5},
            ],
            "pos": 0,
            "filename": "test.py"
        }
        # 深拷贝用于比较
        expected_state = copy.deepcopy(original_state)
        
        _get_current_position(original_state)
        
        self.assertEqual(original_state, expected_state)

    def test_missing_pos_key(self):
        """测试 parser_state 缺少 pos 键，应使用默认值 0"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "IDENT", "value": "x", "line": 1, "column": 5},
            ],
            "filename": "test.py"
        }
        result = _get_current_position(parser_state)
        self.assertEqual(result, (1, 5))

    def test_multiple_calls_consistency(self):
        """测试多次调用结果一致性"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "IDENT", "value": "x", "line": 3, "column": 10},
                {"type": "OP", "value": "+", "line": 3, "column": 12},
            ],
            "pos": 1,
            "filename": "test.py"
        }
        result1 = _get_current_position(parser_state)
        result2 = _get_current_position(parser_state)
        result3 = _get_current_position(parser_state)
        
        self.assertEqual(result1, result2)
        self.assertEqual(result2, result3)
        self.assertEqual(result1, (3, 12))


if __name__ == "__main__":
    unittest.main()

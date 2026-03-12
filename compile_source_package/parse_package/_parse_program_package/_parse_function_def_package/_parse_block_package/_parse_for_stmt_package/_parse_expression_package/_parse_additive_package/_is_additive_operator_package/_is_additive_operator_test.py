# -*- coding: utf-8 -*-
"""
单元测试文件：_is_additive_operator
测试目标：验证 _is_additive_operator 函数是否正确检查当前 token 是否为加法运算符 (PLUS/MINUS)
"""

import unittest
from ._is_additive_operator_src import _is_additive_operator


class TestIsAdditiveOperator(unittest.TestCase):
    """测试 _is_additive_operator 函数的各种场景"""

    def test_token_is_plus_returns_true(self):
        """当前 token 类型为 PLUS 时返回 True"""
        parser_state = {
            "tokens": [
                {"type": "PLUS", "value": "+", "line": 1, "column": 5}
            ],
            "pos": 0
        }
        result = _is_additive_operator(parser_state)
        self.assertTrue(result)

    def test_token_is_minus_returns_true(self):
        """当前 token 类型为 MINUS 时返回 True"""
        parser_state = {
            "tokens": [
                {"type": "MINUS", "value": "-", "line": 1, "column": 5}
            ],
            "pos": 0
        }
        result = _is_additive_operator(parser_state)
        self.assertTrue(result)

    def test_token_is_not_additive_operator_returns_false(self):
        """当前 token 类型不是 PLUS 或 MINUS 时返回 False"""
        parser_state = {
            "tokens": [
                {"type": "MULTIPLY", "value": "*", "line": 1, "column": 5}
            ],
            "pos": 0
        }
        result = _is_additive_operator(parser_state)
        self.assertFalse(result)

    def test_token_is_identifier_returns_false(self):
        """当前 token 是标识符时返回 False"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 0
        }
        result = _is_additive_operator(parser_state)
        self.assertFalse(result)

    def test_token_is_number_returns_false(self):
        """当前 token 是数字时返回 False"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "42", "line": 1, "column": 1}
            ],
            "pos": 0
        }
        result = _is_additive_operator(parser_state)
        self.assertFalse(result)

    def test_pos_negative_returns_false(self):
        """pos 为负数时返回 False"""
        parser_state = {
            "tokens": [
                {"type": "PLUS", "value": "+", "line": 1, "column": 5}
            ],
            "pos": -1
        }
        result = _is_additive_operator(parser_state)
        self.assertFalse(result)

    def test_pos_at_end_of_tokens_returns_false(self):
        """pos 等于 tokens 长度时返回 False"""
        parser_state = {
            "tokens": [
                {"type": "PLUS", "value": "+", "line": 1, "column": 5}
            ],
            "pos": 1
        }
        result = _is_additive_operator(parser_state)
        self.assertFalse(result)

    def test_pos_beyond_tokens_length_returns_false(self):
        """pos 超出 tokens 长度时返回 False"""
        parser_state = {
            "tokens": [
                {"type": "PLUS", "value": "+", "line": 1, "column": 5}
            ],
            "pos": 10
        }
        result = _is_additive_operator(parser_state)
        self.assertFalse(result)

    def test_empty_tokens_list_returns_false(self):
        """tokens 列表为空时返回 False"""
        parser_state = {
            "tokens": [],
            "pos": 0
        }
        result = _is_additive_operator(parser_state)
        self.assertFalse(result)

    def test_missing_tokens_key_returns_false(self):
        """parser_state 缺少 tokens 键时返回 False"""
        parser_state = {
            "pos": 0
        }
        result = _is_additive_operator(parser_state)
        self.assertFalse(result)

    def test_missing_pos_key_defaults_to_zero(self):
        """parser_state 缺少 pos 键时默认为 0"""
        parser_state = {
            "tokens": [
                {"type": "PLUS", "value": "+", "line": 1, "column": 5}
            ]
        }
        result = _is_additive_operator(parser_state)
        self.assertTrue(result)

    def test_token_missing_type_key_returns_false(self):
        """token 缺少 type 键时返回 False"""
        parser_state = {
            "tokens": [
                {"value": "+", "line": 1, "column": 5}
            ],
            "pos": 0
        }
        result = _is_additive_operator(parser_state)
        self.assertFalse(result)

    def test_multiple_tokens_check_current_pos(self):
        """有多个 tokens 时检查当前位置的 token"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 5}
            ],
            "pos": 1
        }
        result = _is_additive_operator(parser_state)
        self.assertTrue(result)

    def test_multiple_tokens_check_different_pos(self):
        """有多个 tokens 时在不同位置检查"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 3},
                {"type": "MINUS", "value": "-", "line": 1, "column": 5}
            ],
            "pos": 2
        }
        result = _is_additive_operator(parser_state)
        self.assertTrue(result)

    def test_multiple_tokens_non_additive_at_pos(self):
        """有多个 tokens 时当前位置不是加法运算符"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "MULTIPLY", "value": "*", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 5}
            ],
            "pos": 1
        }
        result = _is_additive_operator(parser_state)
        self.assertFalse(result)

    def test_does_not_modify_parser_state(self):
        """验证函数不修改 parser_state"""
        parser_state = {
            "tokens": [
                {"type": "PLUS", "value": "+", "line": 1, "column": 5}
            ],
            "pos": 0
        }
        original_state = parser_state.copy()
        original_tokens = [token.copy() for token in parser_state["tokens"]]
        
        _is_additive_operator(parser_state)
        
        self.assertEqual(parser_state, original_state)
        self.assertEqual(parser_state["tokens"], original_tokens)

    def test_case_sensitive_token_type(self):
        """token 类型区分大小写"""
        parser_state = {
            "tokens": [
                {"type": "plus", "value": "+", "line": 1, "column": 5}
            ],
            "pos": 0
        }
        result = _is_additive_operator(parser_state)
        self.assertFalse(result)

    def test_empty_string_token_type_returns_false(self):
        """token 类型为空字符串时返回 False"""
        parser_state = {
            "tokens": [
                {"type": "", "value": "+", "line": 1, "column": 5}
            ],
            "pos": 0
        }
        result = _is_additive_operator(parser_state)
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()

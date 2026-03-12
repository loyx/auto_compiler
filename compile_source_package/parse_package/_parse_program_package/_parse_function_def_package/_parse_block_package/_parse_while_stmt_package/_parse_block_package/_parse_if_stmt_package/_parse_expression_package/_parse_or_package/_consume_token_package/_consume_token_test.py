# -*- coding: utf-8 -*-
"""
单元测试文件：_consume_token 函数测试
"""
import unittest

# 相对导入被测模块
from ._consume_token_src import _consume_token


class TestConsumeToken(unittest.TestCase):
    """测试 _consume_token 函数的各种场景"""

    def test_consume_token_success(self):
        """测试成功消耗匹配类型的 token"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "=", "line": 1, "column": 3},
            ],
            "pos": 0,
            "filename": "test.py",
        }
        
        result = _consume_token(parser_state, "IDENTIFIER")
        
        self.assertIsNotNone(result)
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "x")
        self.assertEqual(parser_state["pos"], 1)
        self.assertNotIn("error", parser_state)

    def test_consume_token_second_token(self):
        """测试消耗第二个 token"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "=", "line": 1, "column": 3},
            ],
            "pos": 1,
            "filename": "test.py",
        }
        
        result = _consume_token(parser_state, "OPERATOR")
        
        self.assertIsNotNone(result)
        self.assertEqual(result["type"], "OPERATOR")
        self.assertEqual(result["value"], "=")
        self.assertEqual(parser_state["pos"], 2)
        self.assertNotIn("error", parser_state)

    def test_consume_token_empty_tokens_list(self):
        """测试 tokens 列表为空的情况"""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py",
        }
        
        result = _consume_token(parser_state, "IDENTIFIER")
        
        self.assertIsNone(result)
        self.assertEqual(parser_state["error"], "No tokens available")
        self.assertEqual(parser_state["pos"], 0)

    def test_consume_token_tokens_is_none(self):
        """测试 tokens 为 None 的情况"""
        parser_state = {
            "tokens": None,
            "pos": 0,
            "filename": "test.py",
        }
        
        result = _consume_token(parser_state, "IDENTIFIER")
        
        self.assertIsNone(result)
        self.assertEqual(parser_state["error"], "No tokens available")
        self.assertEqual(parser_state["pos"], 0)

    def test_consume_token_tokens_key_missing(self):
        """测试 tokens 键不存在的情况"""
        parser_state = {
            "pos": 0,
            "filename": "test.py",
        }
        
        result = _consume_token(parser_state, "IDENTIFIER")
        
        self.assertIsNone(result)
        self.assertEqual(parser_state["error"], "No tokens available")

    def test_consume_token_pos_at_end(self):
        """测试 pos 已到达 token 列表末尾"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 1,
            "filename": "test.py",
        }
        
        result = _consume_token(parser_state, "OPERATOR")
        
        self.assertIsNone(result)
        self.assertEqual(parser_state["error"], "Unexpected end of input, expected 'OPERATOR'")
        self.assertEqual(parser_state["pos"], 1)

    def test_consume_token_pos_beyond_end(self):
        """测试 pos 超出 token 列表范围"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 5,
            "filename": "test.py",
        }
        
        result = _consume_token(parser_state, "OPERATOR")
        
        self.assertIsNone(result)
        self.assertEqual(parser_state["error"], "Unexpected end of input, expected 'OPERATOR'")
        self.assertEqual(parser_state["pos"], 5)

    def test_consume_token_type_mismatch(self):
        """测试 token 类型不匹配"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 2, "column": 5},
            ],
            "pos": 0,
            "filename": "test.py",
        }
        
        result = _consume_token(parser_state, "OPERATOR")
        
        self.assertIsNone(result)
        self.assertEqual(
            parser_state["error"],
            "Expected token type 'OPERATOR', got 'IDENTIFIER' at line 2, column 5"
        )
        self.assertEqual(parser_state["pos"], 0)

    def test_consume_token_type_mismatch_missing_fields(self):
        """测试 token 类型不匹配且 token 缺少 line/column 字段"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x"},
            ],
            "pos": 0,
            "filename": "test.py",
        }
        
        result = _consume_token(parser_state, "OPERATOR")
        
        self.assertIsNone(result)
        self.assertEqual(
            parser_state["error"],
            "Expected token type 'OPERATOR', got 'IDENTIFIER' at line 0, column 0"
        )
        self.assertEqual(parser_state["pos"], 0)

    def test_consume_token_type_mismatch_missing_type_field(self):
        """测试 token 缺少 type 字段"""
        parser_state = {
            "tokens": [
                {"value": "x", "line": 1, "column": 1},
            ],
            "pos": 0,
            "filename": "test.py",
        }
        
        result = _consume_token(parser_state, "OPERATOR")
        
        self.assertIsNone(result)
        self.assertEqual(
            parser_state["error"],
            "Expected token type 'OPERATOR', got '' at line 1, column 1"
        )
        self.assertEqual(parser_state["pos"], 0)

    def test_consume_token_pos_not_set_defaults_to_zero(self):
        """测试 pos 未设置时默认为 0"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "filename": "test.py",
        }
        
        result = _consume_token(parser_state, "IDENTIFIER")
        
        self.assertIsNotNone(result)
        self.assertEqual(parser_state["pos"], 1)

    def test_consume_token_multiple_consumes(self):
        """测试连续消耗多个 token"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "=", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "5", "line": 1, "column": 5},
            ],
            "pos": 0,
            "filename": "test.py",
        }
        
        token1 = _consume_token(parser_state, "IDENTIFIER")
        self.assertIsNotNone(token1)
        self.assertEqual(token1["value"], "x")
        self.assertEqual(parser_state["pos"], 1)
        
        token2 = _consume_token(parser_state, "OPERATOR")
        self.assertIsNotNone(token2)
        self.assertEqual(token2["value"], "=")
        self.assertEqual(parser_state["pos"], 2)
        
        token3 = _consume_token(parser_state, "NUMBER")
        self.assertIsNotNone(token3)
        self.assertEqual(token3["value"], "5")
        self.assertEqual(parser_state["pos"], 3)

    def test_consume_token_error_preserved_on_success(self):
        """测试成功消耗时不会清除已有的 error 字段"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 0,
            "filename": "test.py",
            "error": "previous error",
        }
        
        result = _consume_token(parser_state, "IDENTIFIER")
        
        self.assertIsNotNone(result)
        self.assertEqual(parser_state["pos"], 1)
        # 成功时不会修改 error 字段
        self.assertEqual(parser_state["error"], "previous error")

    def test_consume_token_error_overwritten_on_failure(self):
        """测试失败时会覆盖已有的 error 字段"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 0,
            "filename": "test.py",
            "error": "previous error",
        }
        
        result = _consume_token(parser_state, "OPERATOR")
        
        self.assertIsNone(result)
        self.assertEqual(parser_state["pos"], 0)
        # 失败时会覆盖 error 字段
        self.assertNotEqual(parser_state["error"], "previous error")
        self.assertIn("Expected token type 'OPERATOR'", parser_state["error"])


if __name__ == "__main__":
    unittest.main()

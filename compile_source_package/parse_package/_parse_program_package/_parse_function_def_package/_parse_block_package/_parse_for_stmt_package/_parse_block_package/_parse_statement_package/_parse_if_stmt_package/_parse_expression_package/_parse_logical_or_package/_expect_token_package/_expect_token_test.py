# -*- coding: utf-8 -*-
"""单元测试文件：_expect_token 函数测试"""

import unittest
from typing import Any, Dict

from ._expect_token_src import _expect_token


class TestExpectToken(unittest.TestCase):
    """_expect_token 函数的单元测试类"""

    def _create_parser_state(
        self,
        tokens: list,
        pos: int = 0,
        filename: str = "test.py"
    ) -> Dict[str, Any]:
        """创建解析器状态的辅助函数"""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename
        }

    def _create_token(
        self,
        token_type: str,
        value: str,
        line: int = 1,
        column: int = 1
    ) -> Dict[str, Any]:
        """创建 token 的辅助函数"""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    # ==================== Happy Path Tests ====================

    def test_expect_token_success_single_token(self):
        """测试：单个 token 匹配成功"""
        token = self._create_token("OR", "or", 1, 5)
        parser_state = self._create_parser_state([token], 0, "test.py")

        result = _expect_token(parser_state, "OR")

        self.assertEqual(result, token)
        self.assertEqual(parser_state["pos"], 1)

    def test_expect_token_success_multiple_tokens(self):
        """测试：多个 token 中匹配成功"""
        token1 = self._create_token("AND", "and", 1, 1)
        token2 = self._create_token("OR", "or", 1, 5)
        token3 = self._create_token("IDENTIFIER", "x", 1, 10)
        parser_state = self._create_parser_state([token1, token2, token3], 1, "test.py")

        result = _expect_token(parser_state, "OR")

        self.assertEqual(result, token2)
        self.assertEqual(parser_state["pos"], 2)

    def test_expect_token_success_at_last_position(self):
        """测试：在最后一个 token 位置匹配成功"""
        token1 = self._create_token("AND", "and", 1, 1)
        token2 = self._create_token("OR", "or", 2, 3)
        parser_state = self._create_parser_state([token1, token2], 1, "test.py")

        result = _expect_token(parser_state, "OR")

        self.assertEqual(result, token2)
        self.assertEqual(parser_state["pos"], 2)

    def test_expect_token_success_various_token_types(self):
        """测试：不同 token 类型匹配成功"""
        token_types = [
            "PLUS", "MINUS", "STAR", "SLASH", "PERCENT",
            "EQ", "NE", "LT", "GT", "LE", "GE",
            "BANG", "LPAREN", "RPAREN", "IDENTIFIER", "INTEGER", "STRING"
        ]

        for token_type in token_types:
            token = self._create_token(token_type, token_type.lower(), 1, 1)
            parser_state = self._create_parser_state([token], 0, "test.py")

            result = _expect_token(parser_state, token_type)

            self.assertEqual(result, token)
            self.assertEqual(parser_state["pos"], 1)

    # ==================== Edge Cases: No More Tokens ====================

    def test_expect_token_no_tokens_empty_list(self):
        """测试：tokens 列表为空时抛出 SyntaxError"""
        parser_state = self._create_parser_state([], 0, "test.py")

        with self.assertRaises(SyntaxError) as context:
            _expect_token(parser_state, "OR")

        self.assertIn("Unexpected end of input", str(context.exception))
        self.assertIn("test.py:1:1", str(context.exception))
        self.assertEqual(parser_state["pos"], 0)  # pos 不应改变

    def test_expect_token_no_tokens_pos_beyond_length(self):
        """测试：pos 超出 tokens 长度时抛出 SyntaxError"""
        token = self._create_token("OR", "or", 1, 5)
        parser_state = self._create_parser_state([token], 2, "test.py")

        with self.assertRaises(SyntaxError) as context:
            _expect_token(parser_state, "AND")

        self.assertIn("Unexpected end of input", str(context.exception))
        self.assertIn("test.py:1:5", str(context.exception))
        self.assertEqual(parser_state["pos"], 2)  # pos 不应改变

    def test_expect_token_no_tokens_pos_at_length(self):
        """测试：pos 等于 tokens 长度时抛出 SyntaxError"""
        token = self._create_token("OR", "or", 1, 5)
        parser_state = self._create_parser_state([token], 1, "test.py")

        with self.assertRaises(SyntaxError) as context:
            _expect_token(parser_state, "AND")

        self.assertIn("Unexpected end of input", str(context.exception))
        self.assertIn("test.py:1:5", str(context.exception))
        self.assertEqual(parser_state["pos"], 1)  # pos 不应改变

    def test_expect_token_no_tokens_custom_filename(self):
        """测试：自定义文件名在错误信息中正确显示"""
        parser_state = self._create_parser_state([], 0, "my_module.py")

        with self.assertRaises(SyntaxError) as context:
            _expect_token(parser_state, "OR")

        self.assertIn("my_module.py:1:1", str(context.exception))

    # ==================== Edge Cases: Token Type Mismatch ====================

    def test_expect_token_type_mismatch(self):
        """测试：token 类型不匹配时抛出 SyntaxError"""
        token = self._create_token("AND", "and", 1, 5)
        parser_state = self._create_parser_state([token], 0, "test.py")

        with self.assertRaises(SyntaxError) as context:
            _expect_token(parser_state, "OR")

        self.assertIn("Expected token 'OR' but got 'AND'", str(context.exception))
        self.assertIn("test.py:1:5", str(context.exception))
        self.assertEqual(parser_state["pos"], 0)  # pos 不应改变

    def test_expect_token_type_mismatch_at_different_position(self):
        """测试：在不同位置 token 类型不匹配"""
        token1 = self._create_token("AND", "and", 1, 1)
        token2 = self._create_token("PLUS", "+", 2, 3)
        token3 = self._create_token("IDENTIFIER", "x", 3, 5)
        parser_state = self._create_parser_state([token1, token2, token3], 2, "test.py")

        with self.assertRaises(SyntaxError) as context:
            _expect_token(parser_state, "OR")

        self.assertIn("Expected token 'OR' but got 'IDENTIFIER'", str(context.exception))
        self.assertIn("test.py:3:5", str(context.exception))
        self.assertEqual(parser_state["pos"], 2)  # pos 不应改变

    def test_expect_token_type_mismatch_custom_filename(self):
        """测试：自定义文件名在类型不匹配错误中正确显示"""
        token = self._create_token("AND", "and", 5, 10)
        parser_state = self._create_parser_state([token], 0, "custom_file.py")

        with self.assertRaises(SyntaxError) as context:
            _expect_token(parser_state, "OR")

        self.assertIn("custom_file.py:5:10", str(context.exception))

    # ==================== Side Effect Tests ====================

    def test_expect_token_pos_incremented_by_one(self):
        """测试：pos 只增加 1"""
        token = self._create_token("OR", "or", 1, 1)
        parser_state = self._create_parser_state([token], 0, "test.py")

        _expect_token(parser_state, "OR")

        self.assertEqual(parser_state["pos"], 1)

    def test_expect_token_pos_incremented_from_non_zero(self):
        """测试：从非零位置开始 pos 正确增加"""
        token1 = self._create_token("AND", "and", 1, 1)
        token2 = self._create_token("OR", "or", 1, 5)
        token3 = self._create_token("PLUS", "+", 1, 10)
        parser_state = self._create_parser_state([token1, token2, token3], 1, "test.py")

        _expect_token(parser_state, "OR")

        self.assertEqual(parser_state["pos"], 2)

    def test_expect_token_returns_correct_token(self):
        """测试：返回正确的 token 对象"""
        token = self._create_token("IDENTIFIER", "my_var", 10, 20)
        parser_state = self._create_parser_state([token], 0, "test.py")

        result = _expect_token(parser_state, "IDENTIFIER")

        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "my_var")
        self.assertEqual(result["line"], 10)
        self.assertEqual(result["column"], 20)

    def test_expect_token_returns_same_object_reference(self):
        """测试：返回的 token 是同一个对象引用"""
        token = self._create_token("OR", "or", 1, 1)
        parser_state = self._create_parser_state([token], 0, "test.py")

        result = _expect_token(parser_state, "OR")

        self.assertIs(result, token)

    # ==================== Multiple Calls Tests ====================

    def test_expect_token_multiple_successive_calls(self):
        """测试：多次连续调用成功"""
        token1 = self._create_token("AND", "and", 1, 1)
        token2 = self._create_token("OR", "or", 1, 5)
        token3 = self._create_token("PLUS", "+", 1, 10)
        parser_state = self._create_parser_state([token1, token2, token3], 0, "test.py")

        result1 = _expect_token(parser_state, "AND")
        result2 = _expect_token(parser_state, "OR")
        result3 = _expect_token(parser_state, "PLUS")

        self.assertEqual(result1, token1)
        self.assertEqual(result2, token2)
        self.assertEqual(result3, token3)
        self.assertEqual(parser_state["pos"], 3)

    def test_expect_token_multiple_calls_then_fail(self):
        """测试：多次调用成功后再调用失败"""
        token1 = self._create_token("AND", "and", 1, 1)
        token2 = self._create_token("OR", "or", 1, 5)
        parser_state = self._create_parser_state([token1, token2], 0, "test.py")

        _expect_token(parser_state, "AND")
        _expect_token(parser_state, "OR")

        with self.assertRaises(SyntaxError):
            _expect_token(parser_state, "PLUS")

        self.assertEqual(parser_state["pos"], 2)


if __name__ == "__main__":
    unittest.main()

# -*- coding: utf-8 -*-
"""单元测试：_expect_token 函数"""

import unittest
from typing import Any, Dict

# 相对导入被测模块
from ._expect_token_src import _expect_token


class TestExpectToken(unittest.TestCase):
    """_expect_token 函数的单元测试"""

    def _create_parser_state(self, tokens: list, pos: int = 0, filename: str = "test.py") -> Dict[str, Any]:
        """辅助函数：创建 parser_state 字典"""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename
        }

    def _create_token(self, token_type: str, value: str = "", line: int = 1, column: int = 1) -> Dict[str, Any]:
        """辅助函数：创建 token 字典"""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def test_expect_token_success_at_start(self):
        """测试：在起始位置成功匹配 token"""
        tokens = [
            self._create_token("PLUS", "+", 1, 1),
            self._create_token("INTEGER", "42", 1, 3),
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        result = _expect_token(parser_state, "PLUS")

        self.assertEqual(result, tokens[0])
        self.assertEqual(parser_state["pos"], 1)

    def test_expect_token_success_at_middle(self):
        """测试：在中间位置成功匹配 token"""
        tokens = [
            self._create_token("PLUS", "+", 1, 1),
            self._create_token("STAR", "*", 1, 3),
            self._create_token("INTEGER", "42", 1, 5),
        ]
        parser_state = self._create_parser_state(tokens, pos=1)

        result = _expect_token(parser_state, "STAR")

        self.assertEqual(result, tokens[1])
        self.assertEqual(parser_state["pos"], 2)

    def test_expect_token_success_at_end(self):
        """测试：在最后一个 token 位置成功匹配"""
        tokens = [
            self._create_token("PLUS", "+", 1, 1),
            self._create_token("STAR", "*", 1, 3),
        ]
        parser_state = self._create_parser_state(tokens, pos=1)

        result = _expect_token(parser_state, "STAR")

        self.assertEqual(result, tokens[1])
        self.assertEqual(parser_state["pos"], 2)

    def test_expect_token_eof_empty_tokens(self):
        """测试：空 tokens 列表时抛出 EOF 错误"""
        tokens = []
        parser_state = self._create_parser_state(tokens, pos=0, filename="empty.py")

        with self.assertRaises(SyntaxError) as context:
            _expect_token(parser_state, "PLUS")

        self.assertEqual(str(context.exception), "empty.py:0:0: expected PLUS, got EOF")
        self.assertEqual(parser_state["pos"], 0)  # pos 不应改变

    def test_expect_token_eof_at_end(self):
        """测试：pos 在 tokens 末尾时抛出 EOF 错误"""
        tokens = [
            self._create_token("PLUS", "+", 1, 1),
        ]
        parser_state = self._create_parser_state(tokens, pos=1, filename="end.py")

        with self.assertRaises(SyntaxError) as context:
            _expect_token(parser_state, "STAR")

        self.assertEqual(str(context.exception), "end.py:0:0: expected STAR, got EOF")
        self.assertEqual(parser_state["pos"], 1)  # pos 不应改变

    def test_expect_token_type_mismatch(self):
        """测试：token 类型不匹配时抛出错误"""
        tokens = [
            self._create_token("PLUS", "+", 2, 5),
            self._create_token("INTEGER", "42", 2, 7),
        ]
        parser_state = self._create_parser_state(tokens, pos=0, filename="mismatch.py")

        with self.assertRaises(SyntaxError) as context:
            _expect_token(parser_state, "STAR")

        self.assertEqual(str(context.exception), "mismatch.py:2:5: expected STAR, got PLUS")
        self.assertEqual(parser_state["pos"], 0)  # pos 不应改变

    def test_expect_token_type_mismatch_at_different_position(self):
        """测试：在不同位置 token 类型不匹配"""
        tokens = [
            self._create_token("PLUS", "+", 1, 1),
            self._create_token("MINUS", "-", 3, 10),
            self._create_token("INTEGER", "42", 3, 12),
        ]
        parser_state = self._create_parser_state(tokens, pos=1, filename="diff_pos.py")

        with self.assertRaises(SyntaxError) as context:
            _expect_token(parser_state, "STAR")

        self.assertEqual(str(context.exception), "diff_pos.py:3:10: expected STAR, got MINUS")
        self.assertEqual(parser_state["pos"], 1)  # pos 不应改变

    def test_expect_token_preserves_other_state_fields(self):
        """测试：函数不修改 parser_state 的其他字段"""
        tokens = [
            self._create_token("PLUS", "+", 1, 1),
        ]
        parser_state = self._create_parser_state(tokens, pos=0, filename="preserve.py")
        parser_state["extra_field"] = "should_not_change"

        _expect_token(parser_state, "PLUS")

        self.assertEqual(parser_state["extra_field"], "should_not_change")
        self.assertEqual(parser_state["filename"], "preserve.py")
        self.assertEqual(parser_state["tokens"], tokens)

    def test_expect_token_various_token_types(self):
        """测试：多种 token 类型的匹配"""
        token_types = ["PLUS", "MINUS", "STAR", "SLASH", "PERCENT", "EQ", "NE", 
                       "LT", "GT", "LE", "GE", "AND", "OR", "BANG", "IDENTIFIER", 
                       "INTEGER", "STRING", "LPAREN", "RPAREN"]
        
        for token_type in token_types:
            tokens = [self._create_token(token_type, "val", 1, 1)]
            parser_state = self._create_parser_state(tokens, pos=0)
            
            result = _expect_token(parser_state, token_type)
            
            self.assertEqual(result["type"], token_type)
            self.assertEqual(parser_state["pos"], 1)

    def test_expect_token_does_not_modify_token(self):
        """测试：返回的 token 是原始引用，不修改 token 内容"""
        tokens = [
            self._create_token("PLUS", "+", 1, 1),
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        result = _expect_token(parser_state, "PLUS")

        self.assertIs(result, tokens[0])  # 应该是同一个对象引用


if __name__ == "__main__":
    unittest.main()

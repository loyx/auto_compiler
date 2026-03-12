# -*- coding: utf-8 -*-
"""
单元测试文件：_expect_token 函数测试
"""
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
        """辅助函数：创建 parser_state 字典"""
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
        """辅助函数：创建 token 字典"""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    # ==================== Happy Path ====================

    def test_expect_token_success_first_token(self):
        """测试：成功消耗第一个 token"""
        tokens = [
            self._create_token("IDENTIFIER", "x", 1, 1),
            self._create_token("OPERATOR", "=", 1, 3),
            self._create_token("NUMBER", "42", 1, 5)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        result = _expect_token(parser_state, "IDENTIFIER")

        self.assertEqual(result, tokens[0])
        self.assertEqual(parser_state["pos"], 1)

    def test_expect_token_success_middle_token(self):
        """测试：成功消耗中间的 token"""
        tokens = [
            self._create_token("IDENTIFIER", "x", 1, 1),
            self._create_token("OPERATOR", "=", 1, 3),
            self._create_token("NUMBER", "42", 1, 5)
        ]
        parser_state = self._create_parser_state(tokens, pos=1)

        result = _expect_token(parser_state, "OPERATOR")

        self.assertEqual(result, tokens[1])
        self.assertEqual(parser_state["pos"], 2)

    def test_expect_token_success_last_token(self):
        """测试：成功消耗最后一个 token"""
        tokens = [
            self._create_token("IDENTIFIER", "x", 1, 1),
            self._create_token("OPERATOR", "=", 1, 3),
            self._create_token("NUMBER", "42", 1, 5)
        ]
        parser_state = self._create_parser_state(tokens, pos=2)

        result = _expect_token(parser_state, "NUMBER")

        self.assertEqual(result, tokens[2])
        self.assertEqual(parser_state["pos"], 3)

    def test_expect_token_success_single_token(self):
        """测试：成功消耗唯一的 token"""
        tokens = [
            self._create_token("KEYWORD", "if", 1, 1)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        result = _expect_token(parser_state, "KEYWORD")

        self.assertEqual(result, tokens[0])
        self.assertEqual(parser_state["pos"], 1)

    # ==================== Boundary Cases ====================

    def test_expect_token_empty_tokens_list(self):
        """测试：tokens 列表为空时抛出 SyntaxError"""
        tokens = []
        parser_state = self._create_parser_state(tokens, pos=0)

        with self.assertRaises(SyntaxError) as context:
            _expect_token(parser_state, "IDENTIFIER")

        self.assertIn("Unexpected end of input", str(context.exception))
        self.assertIn("test.py", str(context.exception))

    def test_expect_token_pos_at_end(self):
        """测试：pos 等于 tokens 长度时抛出 SyntaxError"""
        tokens = [
            self._create_token("IDENTIFIER", "x", 1, 1)
        ]
        parser_state = self._create_parser_state(tokens, pos=1)

        with self.assertRaises(SyntaxError) as context:
            _expect_token(parser_state, "OPERATOR")

        self.assertIn("Unexpected end of input", str(context.exception))
        self.assertIn("test.py", str(context.exception))

    def test_expect_token_pos_beyond_end(self):
        """测试：pos 超过 tokens 长度时抛出 SyntaxError"""
        tokens = [
            self._create_token("IDENTIFIER", "x", 1, 1)
        ]
        parser_state = self._create_parser_state(tokens, pos=5)

        with self.assertRaises(SyntaxError) as context:
            _expect_token(parser_state, "OPERATOR")

        self.assertIn("Unexpected end of input", str(context.exception))

    def test_expect_token_pos_negative(self):
        """测试：pos 为负数时的行为（应能正常访问 token）"""
        tokens = [
            self._create_token("IDENTIFIER", "x", 1, 1),
            self._create_token("OPERATOR", "=", 1, 3)
        ]
        parser_state = self._create_parser_state(tokens, pos=-1)

        # Python 允许负索引，-1 指向最后一个元素
        result = _expect_token(parser_state, "OPERATOR")

        self.assertEqual(result, tokens[-1])
        self.assertEqual(parser_state["pos"], 0)

    # ==================== Error Cases ====================

    def test_expect_token_type_mismatch(self):
        """测试：token 类型不匹配时抛出 SyntaxError"""
        tokens = [
            self._create_token("IDENTIFIER", "x", 1, 1)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        with self.assertRaises(SyntaxError) as context:
            _expect_token(parser_state, "NUMBER")

        error_msg = str(context.exception)
        self.assertIn("Syntax error", error_msg)
        self.assertIn("test.py", error_msg)
        self.assertIn("line 1", error_msg)
        self.assertIn("column 1", error_msg)
        self.assertIn("expected token type 'NUMBER'", error_msg)
        self.assertIn("got 'IDENTIFIER'", error_msg)

    def test_expect_token_type_mismatch_multiple_tokens(self):
        """测试：多个 token 中类型不匹配时抛出 SyntaxError"""
        tokens = [
            self._create_token("IDENTIFIER", "x", 2, 5),
            self._create_token("OPERATOR", "=", 2, 7),
            self._create_token("STRING", '"hello"', 3, 1)
        ]
        parser_state = self._create_parser_state(tokens, pos=2)

        with self.assertRaises(SyntaxError) as context:
            _expect_token(parser_state, "NUMBER")

        error_msg = str(context.exception)
        self.assertIn("line 3", error_msg)
        self.assertIn("column 1", error_msg)
        self.assertIn("expected token type 'NUMBER'", error_msg)
        self.assertIn("got 'STRING'", error_msg)

    def test_expect_token_pos_not_updated_on_error(self):
        """测试：抛出异常时 pos 不应被更新"""
        tokens = [
            self._create_token("IDENTIFIER", "x", 1, 1)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        original_pos = parser_state["pos"]

        try:
            _expect_token(parser_state, "NUMBER")
        except SyntaxError:
            pass

        self.assertEqual(parser_state["pos"], original_pos)

    # ==================== Error Message Details ====================

    def test_expect_token_error_message_with_filename(self):
        """测试：错误消息包含自定义文件名"""
        tokens = [
            self._create_token("IDENTIFIER", "x", 1, 1)
        ]
        parser_state = self._create_parser_state(tokens, pos=0, filename="my_module.py")

        with self.assertRaises(SyntaxError) as context:
            _expect_token(parser_state, "NUMBER")

        self.assertIn("my_module.py", str(context.exception))

    def test_expect_token_error_message_without_filename(self):
        """测试：缺少 filename 时使用默认值"""
        tokens = [
            self._create_token("IDENTIFIER", "x", 1, 1)
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0
        }

        with self.assertRaises(SyntaxError) as context:
            _expect_token(parser_state, "NUMBER")

        self.assertIn("<unknown>", str(context.exception))

    def test_expect_token_error_message_without_line_column(self):
        """测试：token 缺少 line/column 时使用默认值"""
        tokens = [
            {
                "type": "IDENTIFIER",
                "value": "x"
            }
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        with self.assertRaises(SyntaxError) as context:
            _expect_token(parser_state, "NUMBER")

        error_msg = str(context.exception)
        self.assertIn("line ?", error_msg)
        self.assertIn("column ?", error_msg)

    # ==================== Side Effects ====================

    def test_expect_token_updates_pos_only_once(self):
        """测试：pos 只增加 1"""
        tokens = [
            self._create_token("IDENTIFIER", "x", 1, 1),
            self._create_token("OPERATOR", "=", 1, 3),
            self._create_token("NUMBER", "42", 1, 5)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        _expect_token(parser_state, "IDENTIFIER")
        self.assertEqual(parser_state["pos"], 1)

        _expect_token(parser_state, "OPERATOR")
        self.assertEqual(parser_state["pos"], 2)

        _expect_token(parser_state, "NUMBER")
        self.assertEqual(parser_state["pos"], 3)

    def test_expect_token_returns_correct_token(self):
        """测试：返回的 token 是正确的引用"""
        tokens = [
            self._create_token("IDENTIFIER", "x", 1, 1)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        result = _expect_token(parser_state, "IDENTIFIER")

        self.assertIs(result, tokens[0])


if __name__ == "__main__":
    unittest.main()

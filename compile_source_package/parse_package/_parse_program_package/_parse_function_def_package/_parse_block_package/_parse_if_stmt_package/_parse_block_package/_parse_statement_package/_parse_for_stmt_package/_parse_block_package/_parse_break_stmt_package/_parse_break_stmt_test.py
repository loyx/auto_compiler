# -*- coding: utf-8 -*-
"""
单元测试：_parse_break_stmt 函数
测试 BREAK 语句解析功能
"""

import unittest
from typing import Dict, Any, List

# 相对导入被测模块
from ._parse_break_stmt_src import _parse_break_stmt


class TestParseBreakStmt(unittest.TestCase):
    """测试 _parse_break_stmt 函数"""

    def _create_parser_state(
        self,
        tokens: List[Dict[str, Any]],
        pos: int = 0,
        filename: str = "test.py"
    ) -> Dict[str, Any]:
        """辅助函数：创建 parser_state"""
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
        """辅助函数：创建 token"""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def test_happy_path_basic_break(self):
        """测试基本的 break ; 语句解析"""
        tokens = [
            self._create_token("BREAK", "break", line=5, column=10),
            self._create_token("SEMICOLON", ";", line=5, column=15)
        ]
        parser_state = self._create_parser_state(tokens)

        result = _parse_break_stmt(parser_state)

        # 验证返回的 AST 节点
        self.assertEqual(result["type"], "BREAK")
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 10)

        # 验证 parser_state 位置已更新
        self.assertEqual(parser_state["pos"], 2)

    def test_happy_path_break_in_sequence(self):
        """测试 break 语句在语句序列中的解析"""
        tokens = [
            self._create_token("BREAK", "break", line=3, column=5),
            self._create_token("SEMICOLON", ";", line=3, column=10),
            self._create_token("RETURN", "return", line=4, column=5),
            self._create_token("SEMICOLON", ";", line=4, column=11)
        ]
        parser_state = self._create_parser_state(tokens)

        result = _parse_break_stmt(parser_state)

        # 验证 AST 节点
        self.assertEqual(result["type"], "BREAK")
        self.assertEqual(result["line"], 3)
        self.assertEqual(result["column"], 5)

        # 验证位置指向下一个语句
        self.assertEqual(parser_state["pos"], 2)

    def test_error_missing_semicolon_at_end(self):
        """测试缺少分号且位于 token 末尾的情况"""
        tokens = [
            self._create_token("BREAK", "break", line=10, column=1)
        ]
        parser_state = self._create_parser_state(tokens)

        with self.assertRaises(SyntaxError) as context:
            _parse_break_stmt(parser_state)

        # 验证错误消息格式
        error_msg = str(context.exception)
        self.assertIn("test.py:10:1:", error_msg)
        self.assertIn("expected ';' after 'break'", error_msg)

    def test_error_wrong_token_after_break(self):
        """测试 break 后跟错误 token 的情况"""
        tokens = [
            self._create_token("BREAK", "break", line=7, column=3),
            self._create_token("IDENTIFIER", "x", line=7, column=9)
        ]
        parser_state = self._create_parser_state(tokens)

        with self.assertRaises(SyntaxError) as context:
            _parse_break_stmt(parser_state)

        error_msg = str(context.exception)
        self.assertIn("test.py:7:3:", error_msg)
        self.assertIn("expected ';' after 'break'", error_msg)
        self.assertIn("got 'x'", error_msg)

    def test_error_unknown_filename_default(self):
        """测试未提供 filename 时使用默认值"""
        tokens = [
            self._create_token("BREAK", "break", line=1, column=1)
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0
            # 未提供 filename
        }

        with self.assertRaises(SyntaxError) as context:
            _parse_break_stmt(parser_state)

        error_msg = str(context.exception)
        self.assertIn("<unknown>:1:1:", error_msg)

    def test_boundary_single_token_break(self):
        """测试只有一个 BREAK token 的边界情况"""
        tokens = [
            self._create_token("BREAK", "break", line=100, column=50)
        ]
        parser_state = self._create_parser_state(tokens)

        with self.assertRaises(SyntaxError):
            _parse_break_stmt(parser_state)

        # 验证 parser_state 位置未被修改（因为抛出了异常）
        self.assertEqual(parser_state["pos"], 0)

    def test_boundary_break_at_start_of_file(self):
        """测试 break 位于文件开头的情况"""
        tokens = [
            self._create_token("BREAK", "break", line=1, column=1),
            self._create_token("SEMICOLON", ";", line=1, column=6)
        ]
        parser_state = self._create_parser_state(tokens)

        result = _parse_break_stmt(parser_state)

        self.assertEqual(result["type"], "BREAK")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 2)

    def test_boundary_break_at_end_of_file(self):
        """测试 break 位于文件末尾（有分号）"""
        tokens = [
            self._create_token("IDENTIFIER", "x", line=1, column=1),
            self._create_token("SEMICOLON", ";", line=1, column=2),
            self._create_token("BREAK", "break", line=2, column=1),
            self._create_token("SEMICOLON", ";", line=2, column=6)
        ]
        parser_state = self._create_parser_state(tokens, pos=2)

        result = _parse_break_stmt(parser_state)

        self.assertEqual(result["type"], "BREAK")
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 4)

    def test_whitespace_token_between_break_and_semicolon(self):
        """测试 break 和分号之间有其他 token（应报错）"""
        tokens = [
            self._create_token("BREAK", "break", line=5, column=1),
            self._create_token("WHITESPACE", "  ", line=5, column=6),
            self._create_token("SEMICOLON", ";", line=5, column=8)
        ]
        parser_state = self._create_parser_state(tokens)

        with self.assertRaises(SyntaxError) as context:
            _parse_break_stmt(parser_state)

        error_msg = str(context.exception)
        self.assertIn("got '  '", error_msg)

    def test_multiple_break_statements_sequential(self):
        """测试连续解析多个 break 语句"""
        tokens = [
            self._create_token("BREAK", "break", line=1, column=1),
            self._create_token("SEMICOLON", ";", line=1, column=6),
            self._create_token("BREAK", "break", line=2, column=1),
            self._create_token("SEMICOLON", ";", line=2, column=6)
        ]
        parser_state = self._create_parser_state(tokens)

        # 解析第一个 break
        result1 = _parse_break_stmt(parser_state)
        self.assertEqual(result1["line"], 1)
        self.assertEqual(parser_state["pos"], 2)

        # 解析第二个 break
        result2 = _parse_break_stmt(parser_state)
        self.assertEqual(result2["line"], 2)
        self.assertEqual(parser_state["pos"], 4)


if __name__ == "__main__":
    unittest.main()

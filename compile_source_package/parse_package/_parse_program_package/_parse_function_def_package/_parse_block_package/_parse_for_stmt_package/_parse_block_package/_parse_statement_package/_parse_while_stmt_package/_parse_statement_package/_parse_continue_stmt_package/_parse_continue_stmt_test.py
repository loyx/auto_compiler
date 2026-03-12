# -*- coding: utf-8 -*-
"""
单元测试文件：_parse_continue_stmt
测试目标：验证 continue 语句解析器的正确性
"""

import unittest
from typing import Any, Dict

from ._parse_continue_stmt_src import _parse_continue_stmt


def _make_parser_state(
    tokens: list,
    pos: int = 0,
    filename: str = "test.c"
) -> Dict[str, Any]:
    """辅助函数：创建 parser_state 对象"""
    return {
        "tokens": tokens,
        "pos": pos,
        "filename": filename
    }


def _make_token(
    token_type: str,
    value: str,
    line: int = 1,
    column: int = 1
) -> Dict[str, Any]:
    """辅助函数：创建 token 对象"""
    return {
        "type": token_type,
        "value": value,
        "line": line,
        "column": column
    }


class TestParseContinueStmt(unittest.TestCase):
    """_parse_continue_stmt 函数的单元测试类"""

    def test_happy_path_simple_continue(self):
        """测试用例：最简单的 continue; 语句"""
        tokens = [
            _make_token("CONTINUE", "continue", line=5, column=10),
            _make_token("SEMICOLON", ";", line=5, column=18)
        ]
        parser_state = _make_parser_state(tokens, pos=0, filename="test.c")

        result = _parse_continue_stmt(parser_state)

        self.assertEqual(result["type"], "CONTINUE_STMT")
        self.assertEqual(result["children"], [])
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 10)
        self.assertEqual(parser_state["pos"], 2)

    def test_happy_path_with_surrounding_tokens(self):
        """测试用例：continue 前后有其他 token"""
        tokens = [
            _make_token("IF", "if", line=1, column=1),
            _make_token("CONTINUE", "continue", line=2, column=5),
            _make_token("SEMICOLON", ";", line=2, column=13),
            _make_token("BREAK", "break", line=3, column=1)
        ]
        parser_state = _make_parser_state(tokens, pos=1, filename="loop.c")

        result = _parse_continue_stmt(parser_state)

        self.assertEqual(result["type"], "CONTINUE_STMT")
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 5)
        self.assertEqual(parser_state["pos"], 3)

    def test_error_empty_tokens(self):
        """测试用例：空 token 列表，应抛出 SyntaxError"""
        parser_state = _make_parser_state([], pos=0, filename="empty.c")

        with self.assertRaises(SyntaxError) as context:
            _parse_continue_stmt(parser_state)

        self.assertIn("empty.c:0:0: unexpected end of input, expected 'continue'", str(context.exception))

    def test_error_pos_beyond_tokens(self):
        """测试用例：pos 超出 token 列表范围"""
        tokens = [_make_token("BREAK", "break", line=1, column=1)]
        parser_state = _make_parser_state(tokens, pos=5, filename="overflow.c")

        with self.assertRaises(SyntaxError) as context:
            _parse_continue_stmt(parser_state)

        self.assertIn("overflow.c:0:0: unexpected end of input, expected 'continue'", str(context.exception))

    def test_error_wrong_token_type(self):
        """测试用例：当前 token 不是 CONTINUE"""
        tokens = [
            _make_token("BREAK", "break", line=10, column=3),
            _make_token("SEMICOLON", ";", line=10, column=8)
        ]
        parser_state = _make_parser_state(tokens, pos=0, filename="wrong.c")

        with self.assertRaises(SyntaxError) as context:
            _parse_continue_stmt(parser_state)

        self.assertIn("wrong.c:10:3: expected 'continue', found 'break'", str(context.exception))

    def test_error_missing_semicolon_eof(self):
        """测试用例：CONTINUE 后缺少分号（到达文件末尾）"""
        tokens = [
            _make_token("CONTINUE", "continue", line=7, column=12)
        ]
        parser_state = _make_parser_state(tokens, pos=0, filename="missing_semi.c")

        with self.assertRaises(SyntaxError) as context:
            _parse_continue_stmt(parser_state)

        self.assertIn("missing_semi.c:7:12: expected ';' after 'continue'", str(context.exception))

    def test_error_wrong_token_after_continue(self):
        """测试用例：CONTINUE 后不是分号"""
        tokens = [
            _make_token("CONTINUE", "continue", line=4, column=8),
            _make_token("BREAK", "break", line=4, column=17)
        ]
        parser_state = _make_parser_state(tokens, pos=0, filename="wrong_after.c")

        with self.assertRaises(SyntaxError) as context:
            _parse_continue_stmt(parser_state)

        self.assertIn("wrong_after.c:4:17: expected ';', found 'break'", str(context.exception))

    def test_error_continue_with_identifier(self):
        """测试用例：CONTINUE 后是标识符而不是分号"""
        tokens = [
            _make_token("CONTINUE", "continue", line=15, column=20),
            _make_token("IDENTIFIER", "x", line=15, column=29)
        ]
        parser_state = _make_parser_state(tokens, pos=0, filename="identifier.c")

        with self.assertRaises(SyntaxError) as context:
            _parse_continue_stmt(parser_state)

        self.assertIn("identifier.c:15:29: expected ';', found 'x'", str(context.exception))

    def test_ast_node_structure(self):
        """测试用例：验证 AST 节点结构完整性"""
        tokens = [
            _make_token("CONTINUE", "continue", line=100, column=50),
            _make_token("SEMICOLON", ";", line=100, column=58)
        ]
        parser_state = _make_parser_state(tokens, pos=0, filename="structure.c")

        result = _parse_continue_stmt(parser_state)

        self.assertIn("type", result)
        self.assertIn("children", result)
        self.assertIn("line", result)
        self.assertIn("column", result)
        self.assertIsInstance(result["children"], list)
        self.assertEqual(len(result["children"]), 0)

    def test_pos_update_exact(self):
        """测试用例：验证 pos 更新精确性"""
        tokens = [
            _make_token("CONTINUE", "continue", line=1, column=1),
            _make_token("SEMICOLON", ";", line=1, column=9),
            _make_token("RETURN", "return", line=2, column=1)
        ]
        parser_state = _make_parser_state(tokens, pos=0, filename="pos_test.c")

        _parse_continue_stmt(parser_state)

        self.assertEqual(parser_state["pos"], 2)
        self.assertEqual(tokens[parser_state["pos"]]["type"], "RETURN")

    def test_multiple_continue_statements(self):
        """测试用例：连续解析多个 continue 语句"""
        tokens = [
            _make_token("CONTINUE", "continue", line=1, column=1),
            _make_token("SEMICOLON", ";", line=1, column=9),
            _make_token("CONTINUE", "continue", line=2, column=1),
            _make_token("SEMICOLON", ";", line=2, column=9)
        ]
        parser_state = _make_parser_state(tokens, pos=0, filename="multi.c")

        result1 = _parse_continue_stmt(parser_state)
        self.assertEqual(result1["line"], 1)
        self.assertEqual(result1["column"], 1)
        self.assertEqual(parser_state["pos"], 2)

        result2 = _parse_continue_stmt(parser_state)
        self.assertEqual(result2["line"], 2)
        self.assertEqual(result2["column"], 1)
        self.assertEqual(parser_state["pos"], 4)

    def test_error_message_filename_preservation(self):
        """测试用例：验证错误消息中文件名正确传递"""
        tokens = [_make_token("IF", "if", line=1, column=1)]
        parser_state = _make_parser_state(tokens, pos=0, filename="/path/to/my/file.c")

        with self.assertRaises(SyntaxError) as context:
            _parse_continue_stmt(parser_state)

        self.assertIn("/path/to/my/file.c:1:1:", str(context.exception))


if __name__ == "__main__":
    unittest.main()

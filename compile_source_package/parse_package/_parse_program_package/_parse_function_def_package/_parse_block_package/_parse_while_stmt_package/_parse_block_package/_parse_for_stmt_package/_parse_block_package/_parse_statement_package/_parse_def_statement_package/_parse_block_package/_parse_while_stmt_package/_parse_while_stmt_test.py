# -*- coding: utf-8 -*-
"""单元测试：_parse_while_stmt 函数"""

import unittest
from unittest.mock import patch
from typing import Dict, Any, List

# 相对导入被测模块
from ._parse_while_stmt_src import _parse_while_stmt


class TestParseWhileStmt(unittest.TestCase):
    """_parse_while_stmt 函数测试类"""

    def setUp(self) -> None:
        """测试前准备"""
        self.maxDiff = None

    def _create_parser_state(
        self,
        tokens: List[Dict[str, Any]],
        pos: int = 0,
        filename: str = "test.py"
    ) -> Dict[str, Any]:
        """创建 parser_state 辅助函数"""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename
        }

    def test_happy_path_basic_while(self) -> None:
        """测试基本 while 语句解析"""
        tokens = [
            {"type": "WHILE", "value": "while", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 7},
            {"type": "COLON", "value": ":", "line": 1, "column": 8},
            {"type": "INDENT", "value": "", "line": 2, "column": 1},
            {"type": "IDENTIFIER", "value": "pass", "line": 2, "column": 5},
            {"type": "SEMICOLON", "value": ";", "line": 2, "column": 9},
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        # Mock 子函数
        mock_condition_ast = {"type": "EXPR", "value": "x"}
        mock_body_ast = {"type": "BODY", "children": [{"type": "PASS"}]}

        with patch(
            "._parse_while_stmt_package._parse_block_package._parse_block_src._parse_block",
            return_value=mock_body_ast
        ) as mock_parse_block:
            with patch(
                "._parse_while_stmt_package._parse_expression_package._parse_expression_src._parse_expression",
                return_value=mock_condition_ast
            ) as mock_parse_expression:
                result = _parse_while_stmt(parser_state)

        # 验证返回的 AST
        self.assertEqual(result["type"], "WHILE")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(result["children"], [mock_condition_ast, mock_body_ast])

        # 验证 parser_state 的 pos 更新（消费了所有 token）
        self.assertEqual(parser_state["pos"], 6)

        # 验证子函数调用
        mock_parse_expression.assert_called_once()
        mock_parse_block.assert_called_once()

    def test_happy_path_with_complex_condition(self) -> None:
        """测试带复杂条件的 while 语句"""
        tokens = [
            {"type": "WHILE", "value": "while", "line": 5, "column": 10},
            {"type": "IDENTIFIER", "value": "x", "line": 5, "column": 16},
            {"type": "OPERATOR", "value": ">", "line": 5, "column": 18},
            {"type": "NUMBER", "value": "0", "line": 5, "column": 20},
            {"type": "COLON", "value": ":", "line": 5, "column": 21},
            {"type": "INDENT", "value": "", "line": 6, "column": 1},
            {"type": "IDENTIFIER", "value": "stmt", "line": 6, "column": 5},
            {"type": "SEMICOLON", "value": ";", "line": 6, "column": 9},
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        mock_condition_ast = {"type": "BINOP", "left": "x", "op": ">", "right": "0"}
        mock_body_ast = {"type": "BODY", "children": [{"type": "STMT"}]}

        with patch(
            "._parse_while_stmt_package._parse_block_package._parse_block_src._parse_block",
            return_value=mock_body_ast
        ):
            with patch(
                "._parse_while_stmt_package._parse_expression_package._parse_expression_src._parse_expression",
                return_value=mock_condition_ast
            ):
                result = _parse_while_stmt(parser_state)

        self.assertEqual(result["type"], "WHILE")
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 10)
        self.assertEqual(parser_state["pos"], 8)

    def test_error_missing_expression(self) -> None:
        """测试缺少表达式时的错误处理"""
        tokens = [
            {"type": "WHILE", "value": "while", "line": 1, "column": 1},
            {"type": "COLON", "value": ":", "line": 1, "column": 6},
        ]
        parser_state = self._create_parser_state(tokens, pos=0, filename="error_test.py")

        with self.assertRaises(SyntaxError) as context:
            _parse_while_stmt(parser_state)

        self.assertIn("Expected expression after WHILE", str(context.exception))
        self.assertIn("error_test.py:1:1", str(context.exception))

    def test_error_missing_expression_at_end(self) -> None:
        """测试 WHILE 后直接到达 token 末尾的错误"""
        tokens = [
            {"type": "WHILE", "value": "while", "line": 10, "column": 5},
        ]
        parser_state = self._create_parser_state(tokens, pos=0, filename="eof_test.py")

        with self.assertRaises(SyntaxError) as context:
            _parse_while_stmt(parser_state)

        self.assertIn("Expected expression after WHILE", str(context.exception))
        self.assertIn("eof_test.py:10:5", str(context.exception))

    def test_error_missing_colon(self) -> None:
        """测试缺少 COLON 时的错误处理"""
        tokens = [
            {"type": "WHILE", "value": "while", "line": 3, "column": 1},
            {"type": "IDENTIFIER", "value": "x", "line": 3, "column": 7},
            {"type": "IDENTIFIER", "value": "unexpected", "line": 3, "column": 9},
        ]
        parser_state = self._create_parser_state(tokens, pos=0, filename="colon_error.py")

        mock_condition_ast = {"type": "EXPR", "value": "x"}

        with patch(
            "._parse_while_stmt_package._parse_expression_package._parse_expression_src._parse_expression",
            return_value=mock_condition_ast
        ):
            with self.assertRaises(SyntaxError) as context:
                _parse_while_stmt(parser_state)

        self.assertIn("Expected COLON after while condition", str(context.exception))
        self.assertIn("colon_error.py:3:9", str(context.exception))

    def test_error_missing_colon_at_end(self) -> None:
        """测试条件表达式后直接到达 token 末尾的错误"""
        tokens = [
            {"type": "WHILE", "value": "while", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 7},
        ]
        parser_state = self._create_parser_state(tokens, pos=0, filename="eof_colon.py")

        mock_condition_ast = {"type": "EXPR", "value": "x"}

        with patch(
            "._parse_while_stmt_package._parse_expression_package._parse_expression_src._parse_expression",
            return_value=mock_condition_ast
        ):
            with self.assertRaises(SyntaxError) as context:
                _parse_while_stmt(parser_state)

        self.assertIn("Expected COLON after while condition", str(context.exception))

    def test_pos_update_consumes_semicolon(self) -> None:
        """测试 pos 更新正确消费 SEMICOLON"""
        tokens = [
            {"type": "WHILE", "value": "while", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 7},
            {"type": "COLON", "value": ":", "line": 1, "column": 8},
            {"type": "INDENT", "value": "", "line": 2, "column": 1},
            {"type": "SEMICOLON", "value": ";", "line": 2, "column": 5},
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        mock_condition_ast = {"type": "EXPR", "value": "x"}
        mock_body_ast = {"type": "BODY", "children": []}

        with patch(
            "._parse_while_stmt_package._parse_block_package._parse_block_src._parse_block",
            return_value=mock_body_ast
        ):
            with patch(
                "._parse_while_stmt_package._parse_expression_package._parse_expression_src._parse_expression",
                return_value=mock_condition_ast
            ):
                result = _parse_while_stmt(parser_state)

        # _parse_block 停在 SEMICOLON 位置，然后 _parse_while_stmt 消费 SEMICOLON
        self.assertEqual(parser_state["pos"], 5)

    def test_pos_not_exceed_tokens_length(self) -> None:
        """测试当没有 SEMICOLON 时不会越界"""
        tokens = [
            {"type": "WHILE", "value": "while", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 7},
            {"type": "COLON", "value": ":", "line": 1, "column": 8},
            {"type": "INDENT", "value": "", "line": 2, "column": 1},
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        mock_condition_ast = {"type": "EXPR", "value": "x"}
        mock_body_ast = {"type": "BODY", "children": []}

        with patch(
            "._parse_while_stmt_package._parse_block_package._parse_block_src._parse_block",
            return_value=mock_body_ast
        ):
            with patch(
                "._parse_while_stmt_package._parse_expression_package._parse_expression_src._parse_expression",
                return_value=mock_condition_ast
            ):
                result = _parse_while_stmt(parser_state)

        # _parse_block 停在末尾，没有 SEMICOLON 可消费，pos 不应越界
        self.assertEqual(parser_state["pos"], 4)

    def test_ast_structure_complete(self) -> None:
        """测试返回的 AST 结构完整性"""
        tokens = [
            {"type": "WHILE", "value": "while", "line": 100, "column": 50},
            {"type": "IDENTIFIER", "value": "cond", "line": 100, "column": 56},
            {"type": "COLON", "value": ":", "line": 100, "column": 60},
            {"type": "INDENT", "value": "", "line": 101, "column": 1},
            {"type": "SEMICOLON", "value": ";", "line": 101, "column": 5},
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        mock_condition_ast = {"type": "CONDITION", "value": "cond"}
        mock_body_ast = {"type": "BODY", "children": [{"type": "STMT"}]}

        with patch(
            "._parse_while_stmt_package._parse_block_package._parse_block_src._parse_block",
            return_value=mock_body_ast
        ):
            with patch(
                "._parse_while_stmt_package._parse_expression_package._parse_expression_src._parse_expression",
                return_value=mock_condition_ast
            ):
                result = _parse_while_stmt(parser_state)

        # 验证 AST 结构
        self.assertIn("type", result)
        self.assertIn("line", result)
        self.assertIn("column", result)
        self.assertIn("children", result)
        self.assertEqual(result["type"], "WHILE")
        self.assertEqual(result["line"], 100)
        self.assertEqual(result["column"], 50)
        self.assertIsInstance(result["children"], list)
        self.assertEqual(len(result["children"]), 2)
        self.assertEqual(result["children"][0], mock_condition_ast)
        self.assertEqual(result["children"][1], mock_body_ast)


if __name__ == "__main__":
    unittest.main()

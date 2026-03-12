# === std / third-party imports ===
import unittest
from typing import Any, Dict
from unittest.mock import patch

# === sub function imports ===
from ._parse_expr_stmt_src import _parse_expr_stmt


class TestParseExprStmt(unittest.TestCase):
    """测试 _parse_expr_stmt 函数"""

    def setUp(self):
        """设置测试夹具"""
        self.mock_tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            {"type": "OPERATOR", "value": "=", "line": 1, "column": 3},
            {"type": "NUMBER", "value": "42", "line": 1, "column": 5},
            {"type": "SEMICOLON", "value": ";", "line": 1, "column": 7},
        ]

    def _create_parser_state(
        self,
        tokens: list = None,
        pos: int = 0,
        filename: str = "test.py",
        error: str = None
    ) -> Dict[str, Any]:
        """创建 parser_state 辅助函数"""
        state = {
            "tokens": tokens if tokens is not None else [],
            "pos": pos,
            "filename": filename,
        }
        if error is not None:
            state["error"] = error
        return state

    @patch("._parse_expr_stmt_src._parse_expr")
    @patch("._parse_expr_stmt_src._consume_token")
    def test_happy_path_valid_expr_with_semicolon(self, mock_consume, mock_parse_expr):
        """测试正常路径：有效表达式后跟分号"""
        # 设置 mock 返回值
        mock_expr_ast = {
            "type": "BINARY_EXPR",
            "children": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "NUMBER", "value": "42", "line": 1, "column": 5}
            ],
            "line": 1,
            "column": 1
        }
        mock_parse_expr.return_value = mock_expr_ast
        mock_consume.return_value = True

        parser_state = self._create_parser_state(tokens=self.mock_tokens, pos=0)

        # 调用被测函数
        result = _parse_expr_stmt(parser_state)

        # 验证返回的 AST 结构
        self.assertEqual(result["type"], "EXPR_STMT")
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0], mock_expr_ast)
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)

        # 验证子函数调用
        mock_parse_expr.assert_called_once_with(parser_state)
        mock_consume.assert_called_once_with(parser_state, ";")

    @patch("._parse_expr_stmt_src._parse_expr")
    @patch("._parse_expr_stmt_src._consume_token")
    def test_expr_parse_failure_returns_empty_children(self, mock_consume, mock_parse_expr):
        """测试表达式解析失败时返回空 children"""
        # 设置 mock：解析表达式时设置 error
        def set_error(state):
            state["error"] = "Unexpected token"
            return {}

        mock_parse_expr.side_effect = set_error
        mock_consume.return_value = True

        parser_state = self._create_parser_state(tokens=self.mock_tokens, pos=0)

        # 调用被测函数
        result = _parse_expr_stmt(parser_state)

        # 验证返回的 AST 结构（空 children）
        self.assertEqual(result["type"], "EXPR_STMT")
        self.assertEqual(result["children"], [])
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)

        # 验证即使解析失败仍尝试消费分号
        mock_consume.assert_called_once_with(parser_state, ";")

    @patch("._parse_expr_stmt_src._parse_expr")
    @patch("._parse_expr_stmt_src._consume_token")
    def test_no_semicolon_after_expr(self, mock_consume, mock_parse_expr):
        """测试表达式后没有分号的情况"""
        mock_expr_ast = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 1
        }
        mock_parse_expr.return_value = mock_expr_ast
        # 消费分号失败
        mock_consume.return_value = False

        parser_state = self._create_parser_state(tokens=self.mock_tokens, pos=0)

        # 调用被测函数
        result = _parse_expr_stmt(parser_state)

        # 验证仍返回 EXPR_STMT 节点（consume_token 失败不影响返回结构）
        self.assertEqual(result["type"], "EXPR_STMT")
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0], mock_expr_ast)

        # 验证尝试消费分号
        mock_consume.assert_called_once_with(parser_state, ";")

    @patch("._parse_expr_stmt_src._parse_expr")
    @patch("._parse_expr_stmt_src._consume_token")
    def test_empty_tokens_list(self, mock_consume, mock_parse_expr):
        """测试空 tokens 列表"""
        mock_parse_expr.return_value = {}
        mock_consume.return_value = False

        parser_state = self._create_parser_state(tokens=[], pos=0)

        # 调用被测函数
        result = _parse_expr_stmt(parser_state)

        # 验证返回的 AST 结构（line/column 应为 0）
        self.assertEqual(result["type"], "EXPR_STMT")
        self.assertEqual(result["line"], 0)
        self.assertEqual(result["column"], 0)

    @patch("._parse_expr_stmt_src._parse_expr")
    @patch("._parse_expr_stmt_src._consume_token")
    def test_pos_out_of_bounds(self, mock_consume, mock_parse_expr):
        """测试 pos 超出 tokens 范围"""
        mock_parse_expr.return_value = {}
        mock_consume.return_value = False

        parser_state = self._create_parser_state(tokens=self.mock_tokens, pos=10)

        # 调用被测函数
        result = _parse_expr_stmt(parser_state)

        # 验证返回的 AST 结构（line/column 应为 0）
        self.assertEqual(result["type"], "EXPR_STMT")
        self.assertEqual(result["line"], 0)
        self.assertEqual(result["column"], 0)

    @patch("._parse_expr_stmt_src._parse_expr")
    @patch("._parse_expr_stmt_src._consume_token")
    def test_complex_expression_ast(self, mock_consume, mock_parse_expr):
        """测试复杂表达式 AST 结构"""
        mock_expr_ast = {
            "type": "CALL_EXPR",
            "children": [
                {
                    "type": "IDENTIFIER",
                    "value": "func",
                    "line": 5,
                    "column": 10
                },
                {
                    "type": "ARG_LIST",
                    "children": [
                        {"type": "NUMBER", "value": "1", "line": 5, "column": 15},
                        {"type": "NUMBER", "value": "2", "line": 5, "column": 17}
                    ],
                    "line": 5,
                    "column": 15
                }
            ],
            "line": 5,
            "column": 10
        }
        mock_parse_expr.return_value = mock_expr_ast
        mock_consume.return_value = True

        parser_state = self._create_parser_state(tokens=self.mock_tokens, pos=0)

        # 调用被测函数
        result = _parse_expr_stmt(parser_state)

        # 验证复杂表达式 AST 被正确包含
        self.assertEqual(result["type"], "EXPR_STMT")
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0]["type"], "CALL_EXPR")
        self.assertEqual(result["children"][0]["line"], 5)
        self.assertEqual(result["children"][0]["column"], 10)

    @patch("._parse_expr_stmt_src._parse_expr")
    @patch("._parse_expr_stmt_src._consume_token")
    def test_parser_state_error_pre_existing(self, mock_consume, mock_parse_expr):
        """测试 parser_state 中已存在 error 字段"""
        mock_parse_expr.return_value = {}
        mock_consume.return_value = True

        parser_state = self._create_parser_state(
            tokens=self.mock_tokens,
            pos=0,
            error="Pre-existing error"
        )

        # 调用被测函数
        result = _parse_expr_stmt(parser_state)

        # 验证返回空 children
        self.assertEqual(result["type"], "EXPR_STMT")
        self.assertEqual(result["children"], [])

    @patch("._parse_expr_stmt_src._parse_expr")
    @patch("._parse_expr_stmt_src._consume_token")
    def test_position_tracking_different_start(self, mock_consume, mock_parse_expr):
        """测试不同起始位置的 line/column 追踪"""
        mock_expr_ast = {
            "type": "IDENTIFIER",
            "value": "y",
            "line": 10,
            "column": 25
        }
        mock_parse_expr.return_value = mock_expr_ast
        mock_consume.return_value = True

        tokens = [
            {"type": "NEWLINE", "value": "\n", "line": 9, "column": 1},
            {"type": "IDENTIFIER", "value": "y", "line": 10, "column": 25},
            {"type": "SEMICOLON", "value": ";", "line": 10, "column": 26},
        ]
        parser_state = self._create_parser_state(tokens=tokens, pos=1)

        # 调用被测函数
        result = _parse_expr_stmt(parser_state)

        # 验证使用起始 token 的 line/column
        self.assertEqual(result["line"], 10)
        self.assertEqual(result["column"], 25)


if __name__ == "__main__":
    unittest.main()

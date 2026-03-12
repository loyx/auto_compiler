"""
单元测试：_parse_expression 函数
测试 Pratt Parsing 算法的表达式解析逻辑
"""

import unittest
from unittest.mock import patch
from typing import Dict, Any

# 相对导入被测函数
from ._parse_expression_src import _parse_expression

# 类型别名
Token = Dict[str, Any]
AST = Dict[str, Any]
ParserState = Dict[str, Any]


class TestParseExpression(unittest.TestCase):
    """测试 _parse_expression 函数"""

    def _make_token(self, type_: str, value: str, line: int = 1, column: int = 1) -> Token:
        """辅助函数：创建 token"""
        return {"type": type_, "value": value, "line": line, "column": column}

    def _make_parser_state(
        self, tokens: list, pos: int = 0, filename: str = "test.txt"
    ) -> ParserState:
        """辅助函数：创建 parser_state"""
        return {"tokens": tokens, "pos": pos, "filename": filename, "error": None}

    def _make_ast_node(
        self,
        type_: str,
        value: Any = None,
        children: list = None,
        line: int = 1,
        column: int = 1,
    ) -> AST:
        """辅助函数：创建 AST 节点"""
        return {
            "type": type_,
            "value": value,
            "children": children if children is not None else [],
            "line": line,
            "column": column,
        }

    @patch("._consume_token_package._consume_token_src._consume_token")
    @patch("._current_token_package._current_token_src._current_token")
    @patch("._parse_expression_with_precedence_package._parse_expression_with_precedence_src._parse_expression_with_precedence")
    @patch("._parse_primary_package._parse_primary_src._parse_primary")
    def test_simple_identifier(self, mock_primary, mock_prec, mock_current, mock_consume):
        """测试：简单标识符表达式（无二元运算）"""
        # 设置：primary 返回标识符节点
        identifier_node = self._make_ast_node("IDENTIFIER", value="x", line=1, column=1)
        mock_primary.return_value = identifier_node

        # 设置：current_token 返回 None（无后续 token）
        mock_current.return_value = None

        parser_state = self._make_parser_state(tokens=[self._make_token("IDENT", "x")])
        result = _parse_expression(parser_state)

        # 验证：返回 primary 的结果
        self.assertEqual(result, identifier_node)
        mock_primary.assert_called_once_with(parser_state)
        mock_current.assert_called_once_with(parser_state)
        mock_prec.assert_not_called()
        mock_consume.assert_not_called()

    @patch("._consume_token_package._consume_token_src._consume_token")
    @patch("._current_token_package._current_token_src._current_token")
    @patch("._parse_expression_with_precedence_package._parse_expression_with_precedence_src._parse_expression_with_precedence")
    @patch("._parse_primary_package._parse_primary_src._parse_primary")
    def test_single_binary_op(self, mock_primary, mock_prec, mock_current, mock_consume):
        """测试：单个二元运算表达式 (a + b)"""
        # 设置：primary 返回左操作数
        left_node = self._make_ast_node("IDENTIFIER", value="a", line=1, column=1)
        mock_primary.return_value = left_node

        # 设置：第一次 current_token 返回 '+'，第二次返回 None
        plus_token = self._make_token("OP", "+", line=1, column=3)
        mock_current.side_effect = [plus_token, None]

        # 设置：consume 返回 '+' token
        mock_consume.return_value = plus_token

        # 设置：parse_expression_with_precedence 返回右操作数
        right_node = self._make_ast_node("IDENTIFIER", value="b", line=1, column=5)
        mock_prec.return_value = right_node

        parser_state = self._make_parser_state(
            tokens=[
                self._make_token("IDENT", "a"),
                self._make_token("OP", "+"),
                self._make_token("IDENT", "b"),
            ]
        )
        result = _parse_expression(parser_state)

        # 验证：返回 BINARY_OP 节点
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "+")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 3)
        self.assertEqual(len(result["children"]), 2)
        self.assertEqual(result["children"][0], left_node)
        self.assertEqual(result["children"][1], right_node)

        mock_primary.assert_called_once_with(parser_state)
        self.assertEqual(mock_current.call_count, 2)
        mock_consume.assert_called_once_with(parser_state)
        mock_prec.assert_called_once_with(parser_state, 5)  # '+' 优先级为 5

    @patch("._consume_token_package._consume_token_src._consume_token")
    @patch("._current_token_package._current_token_src._current_token")
    @patch("._parse_expression_with_precedence_package._parse_expression_with_precedence_src._parse_expression_with_precedence")
    @patch("._parse_primary_package._parse_primary_src._parse_primary")
    def test_multiple_binary_ops_left_assoc(
        self, mock_primary, mock_prec, mock_current, mock_consume
    ):
        """测试：多个二元运算，验证左结合性 (a + b - c)"""
        # 设置：primary 返回第一个操作数
        left_node = self._make_ast_node("IDENTIFIER", value="a", line=1, column=1)
        mock_primary.return_value = left_node

        # 设置：current_token 依次返回 '+', '-', None
        plus_token = self._make_token("OP", "+", line=1, column=3)
        minus_token = self._make_token("OP", "-", line=1, column=7)
        mock_current.side_effect = [plus_token, minus_token, None]

        # 设置：consume 返回对应的 token
        mock_consume.side_effect = [plus_token, minus_token]

        # 设置：第一次 parse_expression_with_precedence 返回 'b'
        right_node_b = self._make_ast_node("IDENTIFIER", value="b", line=1, column=5)
        # 设置：第二次 parse_expression_with_precedence 返回 'c'
        right_node_c = self._make_ast_node("IDENTIFIER", value="c", line=1, column=9)
        mock_prec.side_effect = [right_node_b, right_node_c]

        parser_state = self._make_parser_state(
            tokens=[
                self._make_token("IDENT", "a"),
                self._make_token("OP", "+"),
                self._make_token("IDENT", "b"),
                self._make_token("OP", "-"),
                self._make_token("IDENT", "c"),
            ]
        )
        result = _parse_expression(parser_state)

        # 验证：左结合，应该是 ((a + b) - c)
        # 最外层应该是 '-' 运算
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "-")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 7)

        # 左子节点应该是 '+' 运算的结果
        left_child = result["children"][0]
        self.assertEqual(left_child["type"], "BINARY_OP")
        self.assertEqual(left_child["value"], "+")
        self.assertEqual(left_child["children"][0], left_node)
        self.assertEqual(left_child["children"][1], right_node_b)

        # 右子节点应该是 'c'
        self.assertEqual(result["children"][1], right_node_c)

    @patch("._consume_token_package._consume_token_src._consume_token")
    @patch("._current_token_package._current_token_src._current_token")
    @patch("._parse_expression_with_precedence_package._parse_expression_with_precedence_src._parse_expression_with_precedence")
    @patch("._parse_primary_package._parse_primary_src._parse_primary")
    def test_precedence_levels(self, mock_primary, mock_prec, mock_current, mock_consume):
        """测试：不同优先级的运算符"""
        test_cases = [
            ("||", 1),
            ("&&", 2),
            ("|", 3),
            ("^", 3),
            ("&", 3),
            ("==", 4),
            ("!=", 4),
            ("<", 4),
            (">", 4),
            ("<=", 4),
            (">=", 4),
            ("+", 5),
            ("-", 5),
            ("*", 6),
            ("/", 6),
            ("%", 6),
        ]

        for op, expected_prec in test_cases:
            with self.subTest(op=op):
                # 重置 mock
                mock_primary.reset_mock()
                mock_current.reset_mock()
                mock_consume.reset_mock()
                mock_prec.reset_mock()

                left_node = self._make_ast_node("LITERAL", value=1, line=1, column=1)
                mock_primary.return_value = left_node

                op_token = self._make_token("OP", op, line=1, column=3)
                mock_current.side_effect = [op_token, None]
                mock_consume.return_value = op_token

                right_node = self._make_ast_node("LITERAL", value=2, line=1, column=5)
                mock_prec.return_value = right_node

                parser_state = self._make_parser_state(
                    tokens=[
                        self._make_token("NUM", "1"),
                        self._make_token("OP", op),
                        self._make_token("NUM", "2"),
                    ]
                )
                result = _parse_expression(parser_state)

                self.assertEqual(result["type"], "BINARY_OP")
                self.assertEqual(result["value"], op)
                mock_prec.assert_called_once_with(parser_state, expected_prec)

    @patch("._consume_token_package._consume_token_src._consume_token")
    @patch("._current_token_package._current_token_src._current_token")
    @patch("._parse_expression_with_precedence_package._parse_expression_with_precedence_src._parse_expression_with_precedence")
    @patch("._parse_primary_package._parse_primary_src._parse_primary")
    def test_non_operator_token_stops_loop(
        self, mock_primary, mock_prec, mock_current, mock_consume
    ):
        """测试：遇到非运算符 token 时停止循环"""
        left_node = self._make_ast_node("IDENTIFIER", value="x", line=1, column=1)
        mock_primary.return_value = left_node

        # 设置：current_token 返回一个非运算符 token（如 ';'）
        semicolon_token = self._make_token("SEMICOLON", ";", line=1, column=3)
        mock_current.return_value = semicolon_token

        parser_state = self._make_parser_state(
            tokens=[self._make_token("IDENT", "x"), self._make_token("SEMICOLON", ";")]
        )
        result = _parse_expression(parser_state)

        # 验证：返回 primary 的结果，不进入二元运算循环
        self.assertEqual(result, left_node)
        mock_current.assert_called_once_with(parser_state)
        mock_consume.assert_not_called()
        mock_prec.assert_not_called()

    @patch("._consume_token_package._consume_token_src._consume_token")
    @patch("._current_token_package._current_token_src._current_token")
    @patch("._parse_expression_with_precedence_package._parse_expression_with_precedence_src._parse_expression_with_precedence")
    @patch("._parse_primary_package._parse_primary_src._parse_primary")
    def test_literal_expression(self, mock_primary, mock_prec, mock_current, mock_consume):
        """测试：字面量表达式"""
        literal_node = self._make_ast_node("LITERAL", value=42, line=1, column=1)
        mock_primary.return_value = literal_node
        mock_current.return_value = None

        parser_state = self._make_parser_state(tokens=[self._make_token("NUM", "42")])
        result = _parse_expression(parser_state)

        self.assertEqual(result, literal_node)
        mock_primary.assert_called_once_with(parser_state)

    @patch("._consume_token_package._consume_token_src._consume_token")
    @patch("._current_token_package._current_token_src._current_token")
    @patch("._parse_expression_with_precedence_package._parse_expression_with_precedence_src._parse_expression_with_precedence")
    @patch("._parse_primary_package._parse_primary_src._parse_primary")
    def test_parser_state_pos_updated(
        self, mock_primary, mock_prec, mock_current, mock_consume
    ):
        """测试：parser_state 的 pos 被正确更新（通过 consume_token 调用）"""
        left_node = self._make_ast_node("IDENTIFIER", value="a", line=1, column=1)
        mock_primary.return_value = left_node

        plus_token = self._make_token("OP", "+", line=1, column=3)
        mock_current.side_effect = [plus_token, None]
        mock_consume.return_value = plus_token

        right_node = self._make_ast_node("IDENTIFIER", value="b", line=1, column=5)
        mock_prec.return_value = right_node

        parser_state = self._make_parser_state(
            tokens=[
                self._make_token("IDENT", "a"),
                self._make_token("OP", "+"),
                self._make_token("IDENT", "b"),
            ],
            pos=0,
        )
        result = _parse_expression(parser_state)

        # 验证 consume_token 被调用，这会更新 pos
        mock_consume.assert_called_once_with(parser_state)
        self.assertEqual(result["type"], "BINARY_OP")


class TestParseExpressionEdgeCases(unittest.TestCase):
    """测试边界情况"""

    @patch("._consume_token_package._consume_token_src._consume_token")
    @patch("._current_token_package._current_token_src._current_token")
    @patch("._parse_expression_with_precedence_package._parse_expression_with_precedence_src._parse_expression_with_precedence")
    @patch("._parse_primary_package._parse_primary_src._parse_primary")
    def test_empty_token_list(self, mock_primary, mock_prec, mock_current, mock_consume):
        """测试：空 token 列表"""
        mock_primary.return_value = None
        mock_current.return_value = None

        parser_state = self._make_parser_state(tokens=[], pos=0)
        result = _parse_expression(parser_state)

        self.assertIsNone(result)
        mock_primary.assert_called_once_with(parser_state)

    @patch("._consume_token_package._consume_token_src._consume_token")
    @patch("._current_token_package._current_token_src._current_token")
    @patch("._parse_expression_with_precedence_package._parse_expression_with_precedence_src._parse_expression_with_precedence")
    @patch("._parse_primary_package._parse_primary_src._parse_primary")
    def test_complex_expression_chain(
        self, mock_primary, mock_prec, mock_current, mock_consume
    ):
        """测试：复杂表达式链 (a + b * c - d)"""
        # 模拟：a + (b * c) - d
        # 由于 * 优先级高于 +，b * c 应该先被 parse_expression_with_precedence 处理

        left_node = self._make_ast_node("IDENTIFIER", value="a", line=1, column=1)
        mock_primary.return_value = left_node

        # token 序列：+, *, -
        plus_token = self._make_token("OP", "+", line=1, column=3)
        star_token = self._make_token("OP", "*", line=1, column=7)
        minus_token = self._make_token("OP", "-", line=1, column=11)

        # current_token 调用序列
        mock_current.side_effect = [plus_token, star_token, minus_token, None]
        mock_consume.side_effect = [plus_token, minus_token]

        # 第一次 parse_expression_with_precedence(parser_state, 5) 应该处理 'b * c'
        # 第二次 parse_expression_with_precedence(parser_state, 5) 应该处理 'd'
        mul_result = self._make_ast_node(
            "BINARY_OP", value="*", line=1, column=7,
            children=[
                self._make_ast_node("IDENTIFIER", value="b"),
                self._make_ast_node("IDENTIFIER", value="c"),
            ]
        )
        right_node_d = self._make_ast_node("IDENTIFIER", value="d", line=1, column=13)
        mock_prec.side_effect = [mul_result, right_node_d]

        parser_state = self._make_parser_state(
            tokens=[
                self._make_token("IDENT", "a"),
                self._make_token("OP", "+"),
                self._make_token("IDENT", "b"),
                self._make_token("OP", "*"),
                self._make_token("IDENT", "c"),
                self._make_token("OP", "-"),
                self._make_token("IDENT", "d"),
            ]
        )
        result = _parse_expression(parser_state)

        # 验证：最外层是 '-' 运算
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "-")

        # 左子节点是 '+' 运算
        left_child = result["children"][0]
        self.assertEqual(left_child["type"], "BINARY_OP")
        self.assertEqual(left_child["value"], "+")
        self.assertEqual(left_child["children"][0]["value"], "a")
        # '+' 的右子节点应该是 'b * c'
        self.assertEqual(left_child["children"][1]["type"], "BINARY_OP")
        self.assertEqual(left_child["children"][1]["value"], "*")

        # 右子节点是 'd'
        self.assertEqual(result["children"][1]["value"], "d")


if __name__ == "__main__":
    unittest.main()

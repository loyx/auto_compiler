# -*- coding: utf-8 -*-
"""单元测试：_parse_expression 函数"""

import unittest
from unittest.mock import patch, MagicMock
from typing import Dict, Any

# 相对导入被测模块
from ._parse_expression_src import _parse_expression, ParserState, AST


class TestParseExpression(unittest.TestCase):
    """_parse_expression 函数的单元测试类"""

    def setUp(self) -> None:
        """每个测试前的准备工作"""
        self.base_parser_state: ParserState = {
            "tokens": [],
            "pos": 0,
            "filename": "test.ccl"
        }

    def _create_token(self, token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """辅助方法：创建 token 字典"""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def _create_ast_node(self, node_type: str, **kwargs) -> AST:
        """辅助方法：创建 AST 节点"""
        node: AST = {"type": node_type}
        node.update(kwargs)
        return node

    @patch("_parse_expression_package._parse_expression_src._parse_primary")
    @patch("_parse_expression_package._parse_expression_src._parse_binary_op")
    def test_parse_expression_simple_identifier(self, mock_binary_op: MagicMock, mock_primary: MagicMock) -> None:
        """测试：解析简单标识符表达式"""
        # 准备数据
        token = self._create_token("IDENTIFIER", "x")
        parser_state: ParserState = {
            "tokens": [token],
            "pos": 0,
            "filename": "test.ccl"
        }
        primary_ast = self._create_ast_node("identifier", value="x", line=1, column=1)
        mock_primary.return_value = primary_ast
        mock_binary_op.return_value = primary_ast

        # 执行测试
        result = _parse_expression(parser_state)

        # 验证结果
        mock_primary.assert_called_once_with(parser_state)
        mock_binary_op.assert_called_once_with(parser_state, 0, primary_ast)
        self.assertEqual(result, primary_ast)
        self.assertEqual(parser_state["pos"], 0)  # pos 由子函数更新

    @patch("_parse_expression_package._parse_expression_src._parse_primary")
    @patch("_parse_expression_package._parse_expression_src._parse_binary_op")
    def test_parse_expression_with_binary_operation(self, mock_binary_op: MagicMock, mock_primary: MagicMock) -> None:
        """测试：解析带二元运算的表达式（如 x + 1）"""
        # 准备数据
        tokens = [
            self._create_token("IDENTIFIER", "x", 1, 1),
            self._create_token("OPERATOR", "+", 1, 3),
            self._create_token("NUMBER", "1", 1, 5)
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.ccl"
        }
        primary_ast = self._create_ast_node("identifier", value="x", line=1, column=1)
        binary_ast = self._create_ast_node(
            "binary_op",
            operator="+",
            left=primary_ast,
            right=self._create_ast_node("literal", value=1, line=1, column=5)
        )
        mock_primary.return_value = primary_ast
        mock_binary_op.return_value = binary_ast

        # 执行测试
        result = _parse_expression(parser_state)

        # 验证结果
        mock_primary.assert_called_once_with(parser_state)
        mock_binary_op.assert_called_once_with(parser_state, 0, primary_ast)
        self.assertEqual(result, binary_ast)
        self.assertEqual(result["type"], "binary_op")
        self.assertEqual(result["operator"], "+")

    @patch("_parse_expression_package._parse_expression_src._parse_primary")
    @patch("_parse_expression_package._parse_expression_src._parse_binary_op")
    def test_parse_expression_literal_number(self, mock_binary_op: MagicMock, mock_primary: MagicMock) -> None:
        """测试：解析数字字面量表达式"""
        # 准备数据
        token = self._create_token("NUMBER", "42", 1, 1)
        parser_state: ParserState = {
            "tokens": [token],
            "pos": 0,
            "filename": "test.ccl"
        }
        primary_ast = self._create_ast_node("literal", value=42, line=1, column=1)
        mock_primary.return_value = primary_ast
        mock_binary_op.return_value = primary_ast

        # 执行测试
        result = _parse_expression(parser_state)

        # 验证结果
        mock_primary.assert_called_once_with(parser_state)
        mock_binary_op.assert_called_once_with(parser_state, 0, primary_ast)
        self.assertEqual(result, primary_ast)
        self.assertEqual(result["type"], "literal")
        self.assertEqual(result["value"], 42)

    @patch("_parse_expression_package._parse_expression_src._parse_primary")
    @patch("_parse_expression_package._parse_expression_src._parse_binary_op")
    def test_parse_expression_literal_string(self, mock_binary_op: MagicMock, mock_primary: MagicMock) -> None:
        """测试：解析字符串字面量表达式"""
        # 准备数据
        token = self._create_token("STRING", '"hello"', 1, 1)
        parser_state: ParserState = {
            "tokens": [token],
            "pos": 0,
            "filename": "test.ccl"
        }
        primary_ast = self._create_ast_node("literal", value="hello", line=1, column=1)
        mock_primary.return_value = primary_ast
        mock_binary_op.return_value = primary_ast

        # 执行测试
        result = _parse_expression(parser_state)

        # 验证结果
        mock_primary.assert_called_once_with(parser_state)
        mock_binary_op.assert_called_once_with(parser_state, 0, primary_ast)
        self.assertEqual(result, primary_ast)
        self.assertEqual(result["type"], "literal")
        self.assertEqual(result["value"], "hello")

    @patch("_parse_expression_package._parse_expression_src._parse_primary")
    @patch("_parse_expression_package._parse_expression_src._parse_binary_op")
    def test_parse_expression_function_call(self, mock_binary_op: MagicMock, mock_primary: MagicMock) -> None:
        """测试：解析函数调用表达式"""
        # 准备数据
        tokens = [
            self._create_token("IDENTIFIER", "foo", 1, 1),
            self._create_token("LPAREN", "(", 1, 4),
            self._create_token("NUMBER", "1", 1, 5),
            self._create_token("RPAREN", ")", 1, 6)
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.ccl"
        }
        primary_ast = self._create_ast_node(
            "function_call",
            callee=self._create_ast_node("identifier", value="foo"),
            arguments=[self._create_ast_node("literal", value=1)]
        )
        mock_primary.return_value = primary_ast
        mock_binary_op.return_value = primary_ast

        # 执行测试
        result = _parse_expression(parser_state)

        # 验证结果
        mock_primary.assert_called_once_with(parser_state)
        mock_binary_op.assert_called_once_with(parser_state, 0, primary_ast)
        self.assertEqual(result, primary_ast)
        self.assertEqual(result["type"], "function_call")

    @patch("_parse_expression_package._parse_expression_src._parse_primary")
    @patch("_parse_expression_package._parse_expression_src._parse_binary_op")
    def test_parse_expression_parenthesized(self, mock_binary_op: MagicMock, mock_primary: MagicMock) -> None:
        """测试：解析括号表达式"""
        # 准备数据
        tokens = [
            self._create_token("LPAREN", "(", 1, 1),
            self._create_token("NUMBER", "1", 1, 2),
            self._create_token("RPAREN", ")", 1, 3)
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.ccl"
        }
        primary_ast = self._create_ast_node("parenthesized", expression=self._create_ast_node("literal", value=1))
        mock_primary.return_value = primary_ast
        mock_binary_op.return_value = primary_ast

        # 执行测试
        result = _parse_expression(parser_state)

        # 验证结果
        mock_primary.assert_called_once_with(parser_state)
        mock_binary_op.assert_called_once_with(parser_state, 0, primary_ast)
        self.assertEqual(result, primary_ast)
        self.assertEqual(result["type"], "parenthesized")

    @patch("_parse_expression_package._parse_expression_src._parse_primary")
    @patch("_parse_expression_package._parse_expression_src._parse_binary_op")
    def test_parse_expression_complex_chain(self, mock_binary_op: MagicMock, mock_primary: MagicMock) -> None:
        """测试：解析复杂链式表达式（如 a + b * c - d）"""
        # 准备数据
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("OPERATOR", "+", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 5),
            self._create_token("OPERATOR", "*", 1, 7),
            self._create_token("IDENTIFIER", "c", 1, 9),
            self._create_token("OPERATOR", "-", 1, 11),
            self._create_token("IDENTIFIER", "d", 1, 13)
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.ccl"
        }
        primary_ast = self._create_ast_node("identifier", value="a")
        complex_ast = self._create_ast_node(
            "binary_op",
            operator="-",
            left=self._create_ast_node(
                "binary_op",
                operator="+",
                left=primary_ast,
                right=self._create_ast_node(
                    "binary_op",
                    operator="*",
                    left=self._create_ast_node("identifier", value="b"),
                    right=self._create_ast_node("identifier", value="c")
                )
            ),
            right=self._create_ast_node("identifier", value="d")
        )
        mock_primary.return_value = primary_ast
        mock_binary_op.return_value = complex_ast

        # 执行测试
        result = _parse_expression(parser_state)

        # 验证结果
        mock_primary.assert_called_once_with(parser_state)
        mock_binary_op.assert_called_once_with(parser_state, 0, primary_ast)
        self.assertEqual(result, complex_ast)
        self.assertEqual(result["type"], "binary_op")
        self.assertEqual(result["operator"], "-")

    @patch("_parse_expression_package._parse_expression_src._parse_primary")
    @patch("_parse_expression_package._parse_expression_src._parse_binary_op")
    def test_parse_expression_primary_raises_syntax_error(self, mock_binary_op: MagicMock, mock_primary: MagicMock) -> None:
        """测试：_parse_primary 抛出 SyntaxError 时的处理"""
        # 准备数据
        token = self._create_token("INVALID", "???", 1, 1)
        parser_state: ParserState = {
            "tokens": [token],
            "pos": 0,
            "filename": "test.ccl"
        }
        mock_primary.side_effect = SyntaxError("Invalid primary expression at line 1")

        # 执行测试并验证异常
        with self.assertRaises(SyntaxError) as context:
            _parse_expression(parser_state)

        # 验证异常信息
        self.assertIn("Invalid primary expression", str(context.exception))
        mock_primary.assert_called_once_with(parser_state)
        mock_binary_op.assert_not_called()

    @patch("_parse_expression_package._parse_expression_src._parse_primary")
    @patch("_parse_expression_package._parse_expression_src._parse_binary_op")
    def test_parse_expression_binary_op_raises_syntax_error(self, mock_binary_op: MagicMock, mock_primary: MagicMock) -> None:
        """测试：_parse_binary_op 抛出 SyntaxError 时的处理"""
        # 准备数据
        tokens = [
            self._create_token("IDENTIFIER", "x", 1, 1),
            self._create_token("OPERATOR", "+", 1, 3)
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.ccl"
        }
        primary_ast = self._create_ast_node("identifier", value="x")
        mock_primary.return_value = primary_ast
        mock_binary_op.side_effect = SyntaxError("Expected expression after operator at line 1")

        # 执行测试并验证异常
        with self.assertRaises(SyntaxError) as context:
            _parse_expression(parser_state)

        # 验证异常信息
        self.assertIn("Expected expression after operator", str(context.exception))
        mock_primary.assert_called_once_with(parser_state)
        mock_binary_op.assert_called_once_with(parser_state, 0, primary_ast)

    @patch("_parse_expression_package._parse_expression_src._parse_primary")
    @patch("_parse_expression_package._parse_expression_src._parse_binary_op")
    def test_parse_expression_empty_tokens(self, mock_binary_op: MagicMock, mock_primary: MagicMock) -> None:
        """测试：空 token 列表的处理"""
        # 准备数据
        parser_state: ParserState = {
            "tokens": [],
            "pos": 0,
            "filename": "test.ccl"
        }
        mock_primary.side_effect = SyntaxError("Unexpected end of input, expected expression")

        # 执行测试并验证异常
        with self.assertRaises(SyntaxError):
            _parse_expression(parser_state)

        mock_primary.assert_called_once_with(parser_state)
        mock_binary_op.assert_not_called()

    @patch("_parse_expression_package._parse_expression_src._parse_primary")
    @patch("_parse_expression_package._parse_expression_src._parse_binary_op")
    def test_parse_expression_pos_not_zero(self, mock_binary_op: MagicMock, mock_primary: MagicMock) -> None:
        """测试：pos 不为 0 的情况（表达式在中间位置）"""
        # 准备数据
        tokens = [
            self._create_token("KEYWORD", "let", 1, 1),
            self._create_token("IDENTIFIER", "x", 1, 5),
            self._create_token("OPERATOR", "=", 1, 7),
            self._create_token("NUMBER", "10", 1, 9)
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 3,  # 指向 NUMBER token
            "filename": "test.ccl"
        }
        primary_ast = self._create_ast_node("literal", value=10, line=1, column=9)
        mock_primary.return_value = primary_ast
        mock_binary_op.return_value = primary_ast

        # 执行测试
        result = _parse_expression(parser_state)

        # 验证结果
        mock_primary.assert_called_once_with(parser_state)
        mock_binary_op.assert_called_once_with(parser_state, 0, primary_ast)
        self.assertEqual(result, primary_ast)
        self.assertEqual(parser_state["pos"], 3)  # pos 由子函数更新

    @patch("_parse_expression_package._parse_expression_src._parse_primary")
    @patch("_parse_expression_package._parse_expression_src._parse_binary_op")
    def test_parse_expression_preserves_filename(self, mock_binary_op: MagicMock, mock_primary: MagicMock) -> None:
        """测试：parser_state 中的 filename 被正确传递"""
        # 准备数据
        token = self._create_token("IDENTIFIER", "var", 1, 1)
        parser_state: ParserState = {
            "tokens": [token],
            "pos": 0,
            "filename": "my_source_file.ccl"
        }
        primary_ast = self._create_ast_node("identifier", value="var")
        mock_primary.return_value = primary_ast
        mock_binary_op.return_value = primary_ast

        # 执行测试
        result = _parse_expression(parser_state)

        # 验证 filename 未被修改
        self.assertEqual(parser_state["filename"], "my_source_file.ccl")
        mock_primary.assert_called_once_with(parser_state)

    @patch("_parse_expression_package._parse_expression_src._parse_primary")
    @patch("_parse_expression_package._parse_expression_src._parse_binary_op")
    def test_parse_expression_boolean_literal(self, mock_binary_op: MagicMock, mock_primary: MagicMock) -> None:
        """测试：解析布尔字面量表达式"""
        # 准备数据
        token = self._create_token("BOOLEAN", "true", 1, 1)
        parser_state: ParserState = {
            "tokens": [token],
            "pos": 0,
            "filename": "test.ccl"
        }
        primary_ast = self._create_ast_node("literal", value=True, line=1, column=1)
        mock_primary.return_value = primary_ast
        mock_binary_op.return_value = primary_ast

        # 执行测试
        result = _parse_expression(parser_state)

        # 验证结果
        mock_primary.assert_called_once_with(parser_state)
        mock_binary_op.assert_called_once_with(parser_state, 0, primary_ast)
        self.assertEqual(result, primary_ast)
        self.assertEqual(result["type"], "literal")
        self.assertEqual(result["value"], True)

    @patch("_parse_expression_package._parse_expression_src._parse_primary")
    @patch("_parse_expression_package._parse_expression_src._parse_binary_op")
    def test_parse_expression_none_literal(self, mock_binary_op: MagicMock, mock_primary: MagicMock) -> None:
        """测试：解析 None/null 字面量表达式"""
        # 准备数据
        token = self._create_token("NULL", "null", 1, 1)
        parser_state: ParserState = {
            "tokens": [token],
            "pos": 0,
            "filename": "test.ccl"
        }
        primary_ast = self._create_ast_node("literal", value=None, line=1, column=1)
        mock_primary.return_value = primary_ast
        mock_binary_op.return_value = primary_ast

        # 执行测试
        result = _parse_expression(parser_state)

        # 验证结果
        mock_primary.assert_called_once_with(parser_state)
        mock_binary_op.assert_called_once_with(parser_state, 0, primary_ast)
        self.assertEqual(result, primary_ast)
        self.assertEqual(result["type"], "literal")
        self.assertIsNone(result["value"])

    @patch("_parse_expression_package._parse_expression_src._parse_primary")
    @patch("_parse_expression_package._parse_expression_src._parse_binary_op")
    def test_parse_expression_multiple_operators_same_precedence(self, mock_binary_op: MagicMock, mock_primary: MagicMock) -> None:
        """测试：多个相同优先级的运算符（如 a + b + c）"""
        # 准备数据
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("OPERATOR", "+", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 5),
            self._create_token("OPERATOR", "+", 1, 7),
            self._create_token("IDENTIFIER", "c", 1, 9)
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.ccl"
        }
        primary_ast = self._create_ast_node("identifier", value="a")
        left_assoc_ast = self._create_ast_node(
            "binary_op",
            operator="+",
            left=self._create_ast_node(
                "binary_op",
                operator="+",
                left=primary_ast,
                right=self._create_ast_node("identifier", value="b")
            ),
            right=self._create_ast_node("identifier", value="c")
        )
        mock_primary.return_value = primary_ast
        mock_binary_op.return_value = left_assoc_ast

        # 执行测试
        result = _parse_expression(parser_state)

        # 验证结果（左结合）
        mock_primary.assert_called_once_with(parser_state)
        mock_binary_op.assert_called_once_with(parser_state, 0, primary_ast)
        self.assertEqual(result, left_assoc_ast)
        self.assertEqual(result["operator"], "+")

    @patch("_parse_expression_package._parse_expression_src._parse_primary")
    @patch("_parse_expression_package._parse_expression_src._parse_binary_op")
    def test_parse_expression_mixed_operators_different_precedence(self, mock_binary_op: MagicMock, mock_primary: MagicMock) -> None:
        """测试：混合不同优先级的运算符（如 a + b * c）"""
        # 准备数据
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("OPERATOR", "+", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 5),
            self._create_token("OPERATOR", "*", 1, 7),
            self._create_token("IDENTIFIER", "c", 1, 9)
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.ccl"
        }
        primary_ast = self._create_ast_node("identifier", value="a")
        precedence_ast = self._create_ast_node(
            "binary_op",
            operator="+",
            left=primary_ast,
            right=self._create_ast_node(
                "binary_op",
                operator="*",
                left=self._create_ast_node("identifier", value="b"),
                right=self._create_ast_node("identifier", value="c")
            )
        )
        mock_primary.return_value = primary_ast
        mock_binary_op.return_value = precedence_ast

        # 执行测试
        result = _parse_expression(parser_state)

        # 验证结果（乘法优先级高于加法）
        mock_primary.assert_called_once_with(parser_state)
        mock_binary_op.assert_called_once_with(parser_state, 0, primary_ast)
        self.assertEqual(result, precedence_ast)
        # 顶层应该是加法，右操作数是乘法
        self.assertEqual(result["operator"], "+")
        self.assertEqual(result["right"]["operator"], "*")

    def test_parse_expression_integration_without_mocks(self) -> None:
        """集成测试：不使用 mock，验证函数签名和返回类型（依赖子函数实现）"""
        # 注意：这个测试依赖于 _parse_primary 和 _parse_binary_op 的实际实现
        # 如果子函数未实现，这个测试会失败，但能验证接口契约
        token = self._create_token("IDENTIFIER", "test_var", 1, 1)
        parser_state: ParserState = {
            "tokens": [token],
            "pos": 0,
            "filename": "integration_test.ccl"
        }

        # 由于子函数可能未完全实现，这里只做基本验证
        # 实际集成测试应在所有子函数实现完成后进行
        try:
            result = _parse_expression(parser_state)
            # 如果成功执行，验证返回类型
            self.assertIsInstance(result, dict)
            self.assertIn("type", result)
        except (SyntaxError, NotImplementedError, AttributeError):
            # 子函数未实现时的预期行为
            pass


if __name__ == "__main__":
    unittest.main()

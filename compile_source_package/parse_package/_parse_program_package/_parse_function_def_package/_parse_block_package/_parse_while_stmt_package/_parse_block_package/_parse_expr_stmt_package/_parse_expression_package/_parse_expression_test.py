# === std / third-party imports ===
import unittest
from unittest.mock import patch, MagicMock
from typing import Dict, Any

# === relative imports ===
from ._parse_expression_src import _parse_expression


class TestParseExpression(unittest.TestCase):
    """测试 _parse_expression 函数"""

    def _create_parser_state(self, tokens: list, pos: int = 0, filename: str = "test.src") -> Dict[str, Any]:
        """创建测试用的 parser_state"""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename,
            "error": None
        }

    def _create_token(self, token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """创建测试用的 token"""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def _create_ast_node(self, node_type: str, value: Any = None, children: list = None, 
                         line: int = 1, column: int = 1) -> Dict[str, Any]:
        """创建测试用的 AST 节点"""
        return {
            "type": node_type,
            "value": value,
            "children": children or [],
            "line": line,
            "column": column
        }

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_expr_stmt_package._parse_expression_package._parse_or_package._parse_or_src._parse_or')
    def test_parse_expression_delegates_to_parse_or(self, mock_parse_or: MagicMock):
        """测试 _parse_expression 正确委托给 _parse_or"""
        # 准备测试数据
        parser_state = self._create_parser_state([
            self._create_token("NUMBER", "42")
        ])
        expected_ast = self._create_ast_node("LITERAL", 42)
        mock_parse_or.return_value = expected_ast

        # 执行测试
        result = _parse_expression(parser_state)

        # 验证结果
        self.assertEqual(result, expected_ast)
        mock_parse_or.assert_called_once_with(parser_state)

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_expr_stmt_package._parse_expression_package._parse_or_package._parse_or_src._parse_or')
    def test_parse_expression_with_simple_number(self, mock_parse_or: MagicMock):
        """测试解析简单数字表达式"""
        parser_state = self._create_parser_state([
            self._create_token("NUMBER", "42", line=1, column=1)
        ])
        expected_ast = self._create_ast_node("LITERAL", 42, line=1, column=1)
        mock_parse_or.return_value = expected_ast

        result = _parse_expression(parser_state)

        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], 42)
        mock_parse_or.assert_called_once()

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_expr_stmt_package._parse_expression_package._parse_or_package._parse_or_src._parse_or')
    def test_parse_expression_with_string_literal(self, mock_parse_or: MagicMock):
        """测试解析字符串字面量"""
        parser_state = self._create_parser_state([
            self._create_token("STRING", "hello", line=2, column=5)
        ])
        expected_ast = self._create_ast_node("LITERAL", "hello", line=2, column=5)
        mock_parse_or.return_value = expected_ast

        result = _parse_expression(parser_state)

        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "hello")

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_expr_stmt_package._parse_expression_package._parse_or_package._parse_or_src._parse_or')
    def test_parse_expression_with_boolean_true(self, mock_parse_or: MagicMock):
        """测试解析布尔值 true"""
        parser_state = self._create_parser_state([
            self._create_token("TRUE", "true", line=1, column=1)
        ])
        expected_ast = self._create_ast_node("LITERAL", True, line=1, column=1)
        mock_parse_or.return_value = expected_ast

        result = _parse_expression(parser_state)

        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], True)

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_expr_stmt_package._parse_expression_package._parse_or_package._parse_or_src._parse_or')
    def test_parse_expression_with_boolean_false(self, mock_parse_or: MagicMock):
        """测试解析布尔值 false"""
        parser_state = self._create_parser_state([
            self._create_token("FALSE", "false", line=1, column=1)
        ])
        expected_ast = self._create_ast_node("LITERAL", False, line=1, column=1)
        mock_parse_or.return_value = expected_ast

        result = _parse_expression(parser_state)

        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], False)

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_expr_stmt_package._parse_expression_package._parse_or_package._parse_or_src._parse_or')
    def test_parse_expression_with_nil(self, mock_parse_or: MagicMock):
        """测试解析 nil 值"""
        parser_state = self._create_parser_state([
            self._create_token("NIL", "nil", line=1, column=1)
        ])
        expected_ast = self._create_ast_node("LITERAL", None, line=1, column=1)
        mock_parse_or.return_value = expected_ast

        result = _parse_expression(parser_state)

        self.assertEqual(result["type"], "LITERAL")
        self.assertIsNone(result["value"])

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_expr_stmt_package._parse_expression_package._parse_or_package._parse_or_src._parse_or')
    def test_parse_expression_with_identifier(self, mock_parse_or: MagicMock):
        """测试解析标识符"""
        parser_state = self._create_parser_state([
            self._create_token("IDENTIFIER", "x", line=1, column=1)
        ])
        expected_ast = self._create_ast_node("IDENTIFIER", "x", line=1, column=1)
        mock_parse_or.return_value = expected_ast

        result = _parse_expression(parser_state)

        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "x")

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_expr_stmt_package._parse_expression_package._parse_or_package._parse_or_src._parse_or')
    def test_parse_expression_with_binary_operation(self, mock_parse_or: MagicMock):
        """测试解析二元运算表达式"""
        parser_state = self._create_parser_state([
            self._create_token("NUMBER", "1", line=1, column=1),
            self._create_token("PLUS", "+", line=1, column=3),
            self._create_token("NUMBER", "2", line=1, column=5)
        ])
        expected_ast = self._create_ast_node(
            "BINARY_OP",
            children=[
                self._create_ast_node("LITERAL", 1),
                self._create_ast_node("LITERAL", 2)
            ],
            value="+"
        )
        mock_parse_or.return_value = expected_ast

        result = _parse_expression(parser_state)

        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "+")
        self.assertEqual(len(result["children"]), 2)

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_expr_stmt_package._parse_expression_package._parse_or_package._parse_or_src._parse_or')
    def test_parse_expression_with_unary_operation(self, mock_parse_or: MagicMock):
        """测试解析一元运算表达式"""
        parser_state = self._create_parser_state([
            self._create_token("MINUS", "-", line=1, column=1),
            self._create_token("NUMBER", "5", line=1, column=2)
        ])
        expected_ast = self._create_ast_node(
            "UNARY_OP",
            children=[self._create_ast_node("LITERAL", 5)],
            value="-"
        )
        mock_parse_or.return_value = expected_ast

        result = _parse_expression(parser_state)

        self.assertEqual(result["type"], "UNARY_OP")
        self.assertEqual(result["value"], "-")

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_expr_stmt_package._parse_expression_package._parse_or_package._parse_or_src._parse_or')
    def test_parse_expression_with_parenthesized_expression(self, mock_parse_or: MagicMock):
        """测试解析带括号的表达式"""
        parser_state = self._create_parser_state([
            self._create_token("LEFT_PAREN", "(", line=1, column=1),
            self._create_token("NUMBER", "42", line=1, column=2),
            self._create_token("RIGHT_PAREN", ")", line=1, column=4)
        ])
        expected_ast = self._create_ast_node("LITERAL", 42, line=1, column=2)
        mock_parse_or.return_value = expected_ast

        result = _parse_expression(parser_state)

        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], 42)

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_expr_stmt_package._parse_expression_package._parse_or_package._parse_or_src._parse_or')
    def test_parse_expression_with_complex_expression(self, mock_parse_or: MagicMock):
        """测试解析复杂表达式（多运算符）"""
        parser_state = self._create_parser_state([
            self._create_token("NUMBER", "1", line=1, column=1),
            self._create_token("PLUS", "+", line=1, column=3),
            self._create_token("NUMBER", "2", line=1, column=5),
            self._create_token("STAR", "*", line=1, column=7),
            self._create_token("NUMBER", "3", line=1, column=9)
        ])
        expected_ast = self._create_ast_node(
            "BINARY_OP",
            value="+",
            children=[
                self._create_ast_node("LITERAL", 1),
                self._create_ast_node(
                    "BINARY_OP",
                    value="*",
                    children=[
                        self._create_ast_node("LITERAL", 2),
                        self._create_ast_node("LITERAL", 3)
                    ]
                )
            ]
        )
        mock_parse_or.return_value = expected_ast

        result = _parse_expression(parser_state)

        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(len(result["children"]), 2)

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_expr_stmt_package._parse_expression_package._parse_or_package._parse_or_src._parse_or')
    def test_parse_expression_propagates_syntax_error(self, mock_parse_or: MagicMock):
        """测试语法错误正确传播"""
        parser_state = self._create_parser_state([
            self._create_token("PLUS", "+", line=1, column=1)
        ])
        mock_parse_or.side_effect = SyntaxError("test.src:1:1: Unexpected token PLUS")

        with self.assertRaises(SyntaxError) as context:
            _parse_expression(parser_state)

        self.assertIn("Unexpected token PLUS", str(context.exception))
        mock_parse_or.assert_called_once_with(parser_state)

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_expr_stmt_package._parse_expression_package._parse_or_package._parse_or_src._parse_or')
    def test_parse_expression_with_unknown_filename(self, mock_parse_or: MagicMock):
        """测试文件名为空时的错误格式"""
        parser_state = self._create_parser_state(
            [self._create_token("PLUS", "+", line=1, column=1)],
            filename=""
        )
        mock_parse_or.side_effect = SyntaxError("unknown:1:1: Unexpected token")

        with self.assertRaises(SyntaxError):
            _parse_expression(parser_state)

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_expr_stmt_package._parse_expression_package._parse_or_package._parse_or_src._parse_or')
    def test_parse_expression_modifies_pos(self, mock_parse_or: MagicMock):
        """测试 parser_state 的 pos 被正确修改"""
        initial_pos = 0
        parser_state = self._create_parser_state([
            self._create_token("NUMBER", "42", line=1, column=1)
        ], pos=initial_pos)
        
        expected_ast = self._create_ast_node("LITERAL", 42)
        
        def side_effect(state):
            state["pos"] = 1  # 模拟消费了一个 token
            return expected_ast
        
        mock_parse_or.side_effect = side_effect

        result = _parse_expression(parser_state)

        self.assertEqual(parser_state["pos"], 1)
        self.assertEqual(result, expected_ast)

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_expr_stmt_package._parse_expression_package._parse_or_package._parse_or_src._parse_or')
    def test_parse_expression_with_comparison_operators(self, mock_parse_or: MagicMock):
        """测试比较运算符表达式"""
        parser_state = self._create_parser_state([
            self._create_token("NUMBER", "1", line=1, column=1),
            self._create_token("LESS", "<", line=1, column=3),
            self._create_token("NUMBER", "2", line=1, column=5)
        ])
        expected_ast = self._create_ast_node(
            "BINARY_OP",
            value="<",
            children=[
                self._create_ast_node("LITERAL", 1),
                self._create_ast_node("LITERAL", 2)
            ]
        )
        mock_parse_or.return_value = expected_ast

        result = _parse_expression(parser_state)

        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "<")

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_expr_stmt_package._parse_expression_package._parse_or_package._parse_or_src._parse_or')
    def test_parse_expression_with_equality_operators(self, mock_parse_or: MagicMock):
        """测试相等性运算符表达式"""
        parser_state = self._create_parser_state([
            self._create_token("IDENTIFIER", "a", line=1, column=1),
            self._create_token("EQUAL_EQUAL", "==", line=1, column=3),
            self._create_token("NIL", "nil", line=1, column=6)
        ])
        expected_ast = self._create_ast_node(
            "BINARY_OP",
            value="==",
            children=[
                self._create_ast_node("IDENTIFIER", "a"),
                self._create_ast_node("LITERAL", None)
            ]
        )
        mock_parse_or.return_value = expected_ast

        result = _parse_expression(parser_state)

        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "==")

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_expr_stmt_package._parse_expression_package._parse_or_package._parse_or_src._parse_or')
    def test_parse_expression_with_logical_operators(self, mock_parse_or: MagicMock):
        """测试逻辑运算符表达式"""
        parser_state = self._create_parser_state([
            self._create_token("TRUE", "true", line=1, column=1),
            self._create_token("AND", "and", line=1, column=6),
            self._create_token("FALSE", "false", line=1, column=10)
        ])
        expected_ast = self._create_ast_node(
            "BINARY_OP",
            value="and",
            children=[
                self._create_ast_node("LITERAL", True),
                self._create_ast_node("LITERAL", False)
            ]
        )
        mock_parse_or.return_value = expected_ast

        result = _parse_expression(parser_state)

        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "and")


if __name__ == "__main__":
    unittest.main()

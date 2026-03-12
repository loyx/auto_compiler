# === std / third-party imports ===
import unittest
from typing import Any, Dict
from unittest.mock import patch

# === relative imports for tested module ===
from ._parse_expression_src import _parse_expression


class TestParseExpression(unittest.TestCase):
    """测试 _parse_expression 函数"""

    def _create_mock_parser_state(self, tokens: list = None, pos: int = 0) -> Dict[str, Any]:
        """创建模拟的 parser_state"""
        return {
            "tokens": tokens or [],
            "pos": pos,
            "filename": "test.py",
            "error": None
        }

    def _create_mock_ast_node(self, node_type: str = "BINARY_OP", value: Any = None) -> Dict[str, Any]:
        """创建模拟的 AST 节点"""
        return {
            "type": node_type,
            "children": [],
            "value": value,
            "line": 1,
            "column": 1
        }

    @patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_statement_package._parse_if_stmt_package._parse_expression_package._parse_binary_package._parse_binary_src._parse_binary")
    def test_parse_expression_calls_parse_binary_with_zero_precedence(self, mock_parse_binary):
        """测试 _parse_expression 以优先级 0 调用 _parse_binary"""
        parser_state = self._create_mock_parser_state(pos=0)
        expected_ast = self._create_mock_ast_node()
        mock_parse_binary.return_value = expected_ast

        result = _parse_expression(parser_state)

        mock_parse_binary.assert_called_once_with(parser_state, 0)
        self.assertEqual(result, expected_ast)

    @patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_statement_package._parse_if_stmt_package._parse_expression_package._parse_binary_package._parse_binary_src._parse_binary")
    def test_parse_expression_returns_ast_from_parse_binary(self, mock_parse_binary):
        """测试 _parse_expression 返回 _parse_binary 的 AST 结果"""
        parser_state = self._create_mock_parser_state(pos=5)
        expected_ast = self._create_mock_ast_node("IDENTIFIER", "x")
        mock_parse_binary.return_value = expected_ast

        result = _parse_expression(parser_state)

        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "x")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)

    @patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_statement_package._parse_if_stmt_package._parse_expression_package._parse_binary_package._parse_binary_src._parse_binary")
    def test_parse_expression_propagates_syntax_error(self, mock_parse_binary):
        """测试 _parse_expression 传播 _parse_binary 抛出的 SyntaxError"""
        parser_state = self._create_mock_parser_state(pos=10)
        mock_parse_binary.side_effect = SyntaxError("Invalid expression at line 5")

        with self.assertRaises(SyntaxError) as context:
            _parse_expression(parser_state)

        self.assertEqual(str(context.exception), "Invalid expression at line 5")
        mock_parse_binary.assert_called_once_with(parser_state, 0)

    @patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_statement_package._parse_if_stmt_package._parse_expression_package._parse_binary_package._parse_binary_src._parse_binary")
    def test_parse_expression_with_empty_tokens(self, mock_parse_binary):
        """测试 _parse_expression 处理空 tokens 列表"""
        parser_state = self._create_mock_parser_state(tokens=[], pos=0)
        expected_ast = self._create_mock_ast_node("LITERAL", None)
        mock_parse_binary.return_value = expected_ast

        result = _parse_expression(parser_state)

        mock_parse_binary.assert_called_once_with(parser_state, 0)
        self.assertEqual(result["type"], "LITERAL")

    @patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_statement_package._parse_if_stmt_package._parse_expression_package._parse_binary_package._parse_binary_src._parse_binary")
    def test_parse_expression_with_complex_ast(self, mock_parse_binary):
        """测试 _parse_expression 处理复杂 AST 结构"""
        parser_state = self._create_mock_parser_state(pos=3)
        complex_ast = {
            "type": "BINARY_OP",
            "children": [
                {"type": "IDENTIFIER", "value": "a", "children": [], "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "b", "children": [], "line": 1, "column": 5}
            ],
            "value": "+",
            "line": 1,
            "column": 3
        }
        mock_parse_binary.return_value = complex_ast

        result = _parse_expression(parser_state)

        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "+")
        self.assertEqual(len(result["children"]), 2)
        self.assertEqual(result["children"][0]["value"], "a")
        self.assertEqual(result["children"][1]["value"], "b")

    @patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_statement_package._parse_if_stmt_package._parse_expression_package._parse_binary_package._parse_binary_src._parse_binary")
    def test_parse_expression_preserves_parser_state_reference(self, mock_parse_binary):
        """测试 _parse_expression 传递的是 parser_state 引用（可被 _parse_binary 修改）"""
        parser_state = self._create_mock_parser_state(pos=0)
        mock_parse_binary.return_value = self._create_mock_ast_node()

        _parse_expression(parser_state)

        # 验证传递的是同一个对象引用
        mock_parse_binary.assert_called_once()
        called_args = mock_parse_binary.call_args[0]
        self.assertIs(called_args[0], parser_state)


if __name__ == "__main__":
    unittest.main()

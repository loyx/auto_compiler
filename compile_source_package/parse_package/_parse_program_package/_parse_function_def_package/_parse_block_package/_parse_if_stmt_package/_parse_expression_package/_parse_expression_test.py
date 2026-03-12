# === std / third-party imports ===
import unittest
from unittest.mock import patch, MagicMock
from typing import Dict, Any

# === relative imports ===
from ._parse_expression_src import _parse_expression


class TestParseExpression(unittest.TestCase):
    """测试 _parse_expression 函数"""

    def _create_parser_state(self, tokens: list, pos: int = 0, filename: str = "test.c") -> Dict[str, Any]:
        """创建测试用的 parser_state"""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename
        }

    def _create_token(self, token_type: str, value: Any, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """创建测试用的 token"""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    @patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_expression_package._parse_expression_src._parse_or_expr")
    def test_parse_expression_delegates_to_or_expr(self, mock_parse_or_expr: MagicMock):
        """测试 _parse_expression 委托给 _parse_or_expr"""
        # Arrange
        parser_state = self._create_parser_state([
            self._create_token("NUMBER", "42")
        ])
        expected_ast = {
            "type": "LITERAL",
            "value": 42,
            "line": 1,
            "column": 1
        }
        mock_parse_or_expr.return_value = expected_ast

        # Act
        result = _parse_expression(parser_state)

        # Assert
        mock_parse_or_expr.assert_called_once_with(parser_state)
        self.assertEqual(result, expected_ast)

    @patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_expression_package._parse_expression_src._parse_or_expr")
    def test_parse_expression_with_number_literal(self, mock_parse_or_expr: MagicMock):
        """测试解析数字字面量"""
        # Arrange
        token = self._create_token("NUMBER", "123", line=2, column=5)
        parser_state = self._create_parser_state([token])
        expected_ast = {
            "type": "LITERAL",
            "value": 123,
            "line": 2,
            "column": 5
        }
        mock_parse_or_expr.return_value = expected_ast

        # Act
        result = _parse_expression(parser_state)

        # Assert
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], 123)
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 5)

    @patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_expression_package._parse_or_expr_package._parse_or_expr_src._parse_or_expr")
    def test_parse_expression_with_string_literal(self, mock_parse_or_expr: MagicMock):
        """测试解析字符串字面量"""
        # Arrange
        token = self._create_token("STRING", "hello world", line=1, column=10)
        parser_state = self._create_parser_state([token])
        expected_ast = {
            "type": "LITERAL",
            "value": "hello world",
            "line": 1,
            "column": 10
        }
        mock_parse_or_expr.return_value = expected_ast

        # Act
        result = _parse_expression(parser_state)

        # Assert
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "hello world")

    @patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_expression_package._parse_or_expr_package._parse_or_expr_src._parse_or_expr")
    def test_parse_expression_with_identifier(self, mock_parse_or_expr: MagicMock):
        """测试解析标识符"""
        # Arrange
        token = self._create_token("IDENTIFIER", "myVar", line=3, column=1)
        parser_state = self._create_parser_state([token])
        expected_ast = {
            "type": "IDENTIFIER",
            "value": "myVar",
            "line": 3,
            "column": 1
        }
        mock_parse_or_expr.return_value = expected_ast

        # Act
        result = _parse_expression(parser_state)

        # Assert
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "myVar")

    @patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_expression_package._parse_or_expr_package._parse_or_expr_src._parse_or_expr")
    def test_parse_expression_with_boolean_literal(self, mock_parse_or_expr: MagicMock):
        """测试解析布尔字面量"""
        # Arrange
        token = self._create_token("BOOLEAN", "true", line=1, column=1)
        parser_state = self._create_parser_state([token])
        expected_ast = {
            "type": "LITERAL",
            "value": True,
            "line": 1,
            "column": 1
        }
        mock_parse_or_expr.return_value = expected_ast

        # Act
        result = _parse_expression(parser_state)

        # Assert
        self.assertEqual(result["type"], "LITERAL")
        self.assertTrue(result["value"])

    @patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_expression_package._parse_or_expr_package._parse_or_expr_src._parse_or_expr")
    def test_parse_expression_with_binary_operation(self, mock_parse_or_expr: MagicMock):
        """测试解析二元运算表达式"""
        # Arrange
        parser_state = self._create_parser_state([
            self._create_token("NUMBER", "10"),
            self._create_token("OPERATOR", "+"),
            self._create_token("NUMBER", "20")
        ])
        expected_ast = {
            "type": "BINARY_OP",
            "operator": "+",
            "left": {"type": "LITERAL", "value": 10},
            "right": {"type": "LITERAL", "value": 20},
            "line": 1,
            "column": 1
        }
        mock_parse_or_expr.return_value = expected_ast

        # Act
        result = _parse_expression(parser_state)

        # Assert
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["operator"], "+")

    @patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_expression_package._parse_or_expr_package._parse_or_expr_src._parse_or_expr")
    def test_parse_expression_with_unary_operation(self, mock_parse_or_expr: MagicMock):
        """测试解析一元运算表达式"""
        # Arrange
        parser_state = self._create_parser_state([
            self._create_token("OPERATOR", "-"),
            self._create_token("NUMBER", "5")
        ])
        expected_ast = {
            "type": "UNARY_OP",
            "operator": "-",
            "operand": {"type": "LITERAL", "value": 5},
            "line": 1,
            "column": 1
        }
        mock_parse_or_expr.return_value = expected_ast

        # Act
        result = _parse_expression(parser_state)

        # Assert
        self.assertEqual(result["type"], "UNARY_OP")
        self.assertEqual(result["operator"], "-")

    @patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_expression_package._parse_or_expr_package._parse_or_expr_src._parse_or_expr")
    def test_parse_expression_with_parentheses(self, mock_parse_or_expr: MagicMock):
        """测试解析带括号的表达式"""
        # Arrange
        parser_state = self._create_parser_state([
            self._create_token("LPAREN", "("),
            self._create_token("NUMBER", "10"),
            self._create_token("OPERATOR", "+"),
            self._create_token("NUMBER", "20"),
            self._create_token("RPAREN", ")")
        ])
        expected_ast = {
            "type": "BINARY_OP",
            "operator": "+",
            "left": {"type": "LITERAL", "value": 10},
            "right": {"type": "LITERAL", "value": 20},
            "line": 1,
            "column": 1
        }
        mock_parse_or_expr.return_value = expected_ast

        # Act
        result = _parse_expression(parser_state)

        # Assert
        self.assertEqual(result["type"], "BINARY_OP")

    @patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_expression_package._parse_or_expr_package._parse_or_expr_src._parse_or_expr")
    def test_parse_expression_empty_tokens(self, mock_parse_or_expr: MagicMock):
        """测试空 token 列表"""
        # Arrange
        parser_state = self._create_parser_state([])
        mock_parse_or_expr.side_effect = SyntaxError("Unexpected end of expression")

        # Act & Assert
        with self.assertRaises(SyntaxError):
            _parse_expression(parser_state)

    @patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_expression_package._parse_or_expr_package._parse_or_expr_src._parse_or_expr")
    def test_parse_expression_propagates_syntax_error(self, mock_parse_or_expr: MagicMock):
        """测试语法错误传播"""
        # Arrange
        parser_state = self._create_parser_state([
            self._create_token("OPERATOR", "+")
        ])
        error_msg = "Unexpected operator at start of expression"
        mock_parse_or_expr.side_effect = SyntaxError(error_msg)

        # Act & Assert
        with self.assertRaises(SyntaxError) as context:
            _parse_expression(parser_state)
        self.assertEqual(str(context.exception), error_msg)

    @patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_expression_package._parse_or_expr_package._parse_or_expr_src._parse_or_expr")
    def test_parse_expression_with_complex_nested_expression(self, mock_parse_or_expr: MagicMock):
        """测试复杂嵌套表达式"""
        # Arrange
        parser_state = self._create_parser_state([
            self._create_token("LPAREN", "("),
            self._create_token("NUMBER", "10"),
            self._create_token("OPERATOR", "*"),
            self._create_token("LPAREN", "("),
            self._create_token("NUMBER", "2"),
            self._create_token("OPERATOR", "+"),
            self._create_token("NUMBER", "3"),
            self._create_token("RPAREN", ")"),
            self._create_token("RPAREN", ")")
        ])
        expected_ast = {
            "type": "BINARY_OP",
            "operator": "*",
            "left": {"type": "LITERAL", "value": 10},
            "right": {
                "type": "BINARY_OP",
                "operator": "+",
                "left": {"type": "LITERAL", "value": 2},
                "right": {"type": "LITERAL", "value": 3}
            },
            "line": 1,
            "column": 1
        }
        mock_parse_or_expr.return_value = expected_ast

        # Act
        result = _parse_expression(parser_state)

        # Assert
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["operator"], "*")

    @patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_expression_package._parse_or_expr_package._parse_or_expr_src._parse_or_expr")
    def test_parse_expression_preserves_parser_state_reference(self, mock_parse_or_expr: MagicMock):
        """测试 parser_state 引用被正确传递"""
        # Arrange
        parser_state = self._create_parser_state([
            self._create_token("NUMBER", "42")
        ])
        mock_parse_or_expr.return_value = {"type": "LITERAL", "value": 42}

        # Act
        _parse_expression(parser_state)

        # Assert
        mock_parse_or_expr.assert_called_once()
        called_state = mock_parse_or_expr.call_args[0][0]
        self.assertIs(called_state, parser_state)

    @patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_expression_package._parse_or_expr_package._parse_or_expr_src._parse_or_expr")
    def test_parse_expression_with_logical_operators(self, mock_parse_or_expr: MagicMock):
        """测试逻辑运算符表达式"""
        # Arrange
        parser_state = self._create_parser_state([
            self._create_token("BOOLEAN", "true"),
            self._create_token("OPERATOR", "||"),
            self._create_token("BOOLEAN", "false")
        ])
        expected_ast = {
            "type": "BINARY_OP",
            "operator": "||",
            "left": {"type": "LITERAL", "value": True},
            "right": {"type": "LITERAL", "value": False},
            "line": 1,
            "column": 1
        }
        mock_parse_or_expr.return_value = expected_ast

        # Act
        result = _parse_expression(parser_state)

        # Assert
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["operator"], "||")

    @patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_expression_package._parse_or_expr_package._parse_or_expr_src._parse_or_expr")
    def test_parse_expression_with_comparison_operators(self, mock_parse_or_expr: MagicMock):
        """测试比较运算符表达式"""
        # Arrange
        parser_state = self._create_parser_state([
            self._create_token("NUMBER", "10"),
            self._create_token("OPERATOR", ">"),
            self._create_token("NUMBER", "5")
        ])
        expected_ast = {
            "type": "BINARY_OP",
            "operator": ">",
            "left": {"type": "LITERAL", "value": 10},
            "right": {"type": "LITERAL", "value": 5},
            "line": 1,
            "column": 1
        }
        mock_parse_or_expr.return_value = expected_ast

        # Act
        result = _parse_expression(parser_state)

        # Assert
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["operator"], ">")


if __name__ == "__main__":
    unittest.main()

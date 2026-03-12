# === std / third-party imports ===
import unittest
from unittest.mock import patch
from typing import Dict, Any

# === relative imports ===
from ._parse_expression_statement_src import _parse_expression_statement


class TestParseExpressionStatement(unittest.TestCase):
    """单元测试：_parse_expression_statement 函数"""

    def _create_parser_state(
        self,
        tokens: list,
        pos: int = 0,
        filename: str = "test.c"
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
        value: str = "",
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

    @patch("compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_expression_statement_package._parse_expression_statement_src._parse_expression")
    def test_happy_path_simple_expression(self, mock_parse_expression):
        """测试：简单表达式语句（表达式 + 分号）"""
        # 准备：表达式 AST 和 tokens
        expression_ast = {
            "type": "BINARY_EXPR",
            "line": 1,
            "column": 1,
            "children": [
                {"type": "IDENTIFIER", "value": "x"},
                {"type": "NUMBER", "value": "5"}
            ]
        }
        mock_parse_expression.return_value = expression_ast

        tokens = [
            self._create_token("IDENTIFIER", "x", 1, 1),
            self._create_token("NUMBER", "5", 1, 3),
            self._create_token("SEMICOLON", ";", 1, 5)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        # 执行
        result = _parse_expression_statement(parser_state)

        # 验证
        self.assertEqual(result["type"], "EXPRESSION_STMT")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0], expression_ast)
        self.assertEqual(parser_state["pos"], 3)  # pos 应前进到分号之后
        mock_parse_expression.assert_called_once()

    @patch("compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_expression_statement_package._parse_expression_statement_src._parse_expression")
    def test_happy_path_complex_expression(self, mock_parse_expression):
        """测试：复杂表达式语句"""
        expression_ast = {
            "type": "CALL_EXPR",
            "line": 5,
            "column": 10,
            "children": [
                {"type": "IDENTIFIER", "value": "printf"},
                {"type": "STRING", "value": "hello"}
            ]
        }
        mock_parse_expression.return_value = expression_ast

        tokens = [
            self._create_token("IDENTIFIER", "printf", 5, 10),
            self._create_token("LPAREN", "(", 5, 16),
            self._create_token("STRING", "hello", 5, 17),
            self._create_token("RPAREN", ")", 5, 24),
            self._create_token("SEMICOLON", ";", 5, 25)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        # 执行
        result = _parse_expression_statement(parser_state)

        # 验证
        self.assertEqual(result["type"], "EXPRESSION_STMT")
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 10)
        self.assertEqual(result["children"][0], expression_ast)
        self.assertEqual(parser_state["pos"], 5)

    @patch("compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_expression_statement_package._parse_expression_statement_src._parse_expression")
    def test_boundary_empty_tokens(self, mock_parse_expression):
        """测试：边界情况 - 空 tokens 列表"""
        parser_state = self._create_parser_state(tokens=[], pos=0)

        # 执行并验证异常
        with self.assertRaises(SyntaxError) as context:
            _parse_expression_statement(parser_state)

        self.assertIn("Unexpected end of file", str(context.exception))
        self.assertIn("expected expression", str(context.exception))
        mock_parse_expression.assert_not_called()

    @patch("compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_expression_statement_package._parse_expression_statement_src._parse_expression")
    def test_boundary_pos_at_end(self, mock_parse_expression):
        """测试：边界情况 - pos 已在 tokens 末尾"""
        tokens = [
            self._create_token("IDENTIFIER", "x", 1, 1)
        ]
        parser_state = self._create_parser_state(tokens, pos=1)

        # 执行并验证异常
        with self.assertRaises(SyntaxError) as context:
            _parse_expression_statement(parser_state)

        self.assertIn("Unexpected end of file", str(context.exception))
        mock_parse_expression.assert_not_called()

    @patch("compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_expression_statement_package._parse_expression_statement_src._parse_expression")
    def test_error_missing_semicolon(self, mock_parse_expression):
        """测试：错误情况 - 缺少分号"""
        expression_ast = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        mock_parse_expression.return_value = expression_ast

        tokens = [
            self._create_token("IDENTIFIER", "x", 1, 1)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        # 执行并验证异常
        with self.assertRaises(SyntaxError) as context:
            _parse_expression_statement(parser_state)

        self.assertIn("Expected ';'", str(context.exception))
        self.assertIn("line 1", str(context.exception))
        mock_parse_expression.assert_called_once()

    @patch("compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_expression_statement_package._parse_expression_statement_src._parse_expression")
    def test_error_wrong_token_after_expression(self, mock_parse_expression):
        """测试：错误情况 - 表达式后是错误 token（非分号）"""
        expression_ast = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        mock_parse_expression.return_value = expression_ast

        tokens = [
            self._create_token("IDENTIFIER", "x", 1, 1),
            self._create_token("COMMA", ",", 1, 2)  # 应该是分号，但这里是逗号
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        # 执行并验证异常
        with self.assertRaises(SyntaxError) as context:
            _parse_expression_statement(parser_state)

        self.assertIn("Expected ';'", str(context.exception))
        self.assertIn("line 1", str(context.exception))
        self.assertEqual(parser_state["pos"], 1)  # pos 应停在分号位置（未消费）
        mock_parse_expression.assert_called_once()

    @patch("compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_expression_statement_package._parse_expression_statement_src._parse_expression")
    def test_error_parse_expression_raises(self, mock_parse_expression):
        """测试：错误情况 - _parse_expression 抛出 SyntaxError"""
        mock_parse_expression.side_effect = SyntaxError("Invalid expression syntax")

        tokens = [
            self._create_token("INVALID", "???", 3, 5)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        # 执行并验证异常传播
        with self.assertRaises(SyntaxError) as context:
            _parse_expression_statement(parser_state)

        self.assertEqual(str(context.exception), "Invalid expression syntax")
        mock_parse_expression.assert_called_once()
        self.assertEqual(parser_state["pos"], 0)  # pos 不应改变

    @patch("compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_expression_statement_package._parse_expression_statement_src._parse_expression")
    def test_state_pos_updated_correctly(self, mock_parse_expression):
        """测试：状态变化 - pos 正确更新"""
        expression_ast = {"type": "NUMBER", "value": "42", "line": 2, "column": 1}
        mock_parse_expression.return_value = expression_ast

        # _parse_expression 会消费 1 个 token
        def mock_parse_side_effect(state):
            state["pos"] += 1
            return expression_ast

        mock_parse_expression.side_effect = mock_parse_side_effect

        tokens = [
            self._create_token("NUMBER", "42", 2, 1),
            self._create_token("SEMICOLON", ";", 2, 3)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        # 执行
        result = _parse_expression_statement(parser_state)

        # 验证 pos 更新：从 0 -> 1 (表达式) -> 2 (分号)
        self.assertEqual(parser_state["pos"], 2)
        self.assertIsNotNone(result)

    @patch("compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_expression_statement_package._parse_expression_statement_src._parse_expression")
    def test_multiple_semicolons(self, mock_parse_expression):
        """测试：多个分号场景（只消费第一个）"""
        expression_ast = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        mock_parse_expression.return_value = expression_ast

        tokens = [
            self._create_token("IDENTIFIER", "x", 1, 1),
            self._create_token("SEMICOLON", ";", 1, 2),
            self._create_token("SEMICOLON", ";", 1, 3)  # 额外的分号
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        # 执行
        result = _parse_expression_statement(parser_state)

        # 验证：只消费到第一个分号
        self.assertEqual(result["type"], "EXPRESSION_STMT")
        self.assertEqual(parser_state["pos"], 2)  # 停在第二个分号之前

    @patch("compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_expression_statement_package._parse_expression_statement_src._parse_expression")
    def test_different_line_numbers(self, mock_parse_expression):
        """测试：不同行号的表达式语句"""
        expression_ast = {"type": "IDENTIFIER", "value": "y", "line": 10, "column": 5}
        mock_parse_expression.return_value = expression_ast

        tokens = [
            self._create_token("IDENTIFIER", "y", 10, 5),
            self._create_token("SEMICOLON", ";", 10, 6)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        # 执行
        result = _parse_expression_statement(parser_state)

        # 验证行号信息
        self.assertEqual(result["line"], 10)
        self.assertEqual(result["column"], 5)


if __name__ == "__main__":
    unittest.main()

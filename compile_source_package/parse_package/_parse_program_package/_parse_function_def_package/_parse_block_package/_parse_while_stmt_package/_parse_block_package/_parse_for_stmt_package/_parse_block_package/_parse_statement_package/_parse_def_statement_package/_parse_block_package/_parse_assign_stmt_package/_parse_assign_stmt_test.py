# -*- coding: utf-8 -*-
"""单元测试：_parse_assign_stmt 函数"""

import unittest
from unittest.mock import patch
from typing import Dict, Any, List

# 相对导入被测模块
from ._parse_assign_stmt_src import _parse_assign_stmt, _expect_token


class TestParseAssignStmt(unittest.TestCase):
    """_parse_assign_stmt 函数的单元测试类"""

    def _create_parser_state(self, tokens: List[Dict[str, Any]], pos: int = 0) -> Dict[str, Any]:
        """辅助函数：创建 parser_state"""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": "test.let",
            "error": ""
        }

    def _create_token(self, token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """辅助函数：创建 token"""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def test_happy_path_simple_assignment(self):
        """测试：正常路径 - 简单赋值语句 LET x = 5;"""
        tokens = [
            self._create_token("LET", "LET", 1, 1),
            self._create_token("IDENTIFIER", "x", 1, 5),
            self._create_token("EQUALS", "=", 1, 7),
            self._create_token("NUMBER", "5", 1, 9),
            self._create_token("SEMICOLON", ";", 1, 10),
        ]
        parser_state = self._create_parser_state(tokens)

        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_def_statement_package._parse_block_package._parse_assign_stmt_package._parse_expression_package._parse_expression_src._parse_expression') as mock_parse_expression:
            mock_parse_expression.return_value = {
                "type": "NUMBER",
                "value": "5",
                "line": 1,
                "column": 9,
                "children": []
            }

            result = _parse_assign_stmt(parser_state)

            # 验证返回的 AST 结构
            self.assertEqual(result["type"], "ASSIGN")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            self.assertEqual(len(result["children"]), 2)

            # 验证标识符子节点
            ident_node = result["children"][0]
            self.assertEqual(ident_node["type"], "IDENTIFIER")
            self.assertEqual(ident_node["value"], "x")
            self.assertEqual(ident_node["line"], 1)
            self.assertEqual(ident_node["column"], 5)

            # 验证表达式子节点
            expr_node = result["children"][1]
            self.assertEqual(expr_node["type"], "NUMBER")
            self.assertEqual(expr_node["value"], "5")

            # 验证 pos 已更新（消费了 5 个 token）
            self.assertEqual(parser_state["pos"], 5)

    def test_happy_path_assignment_with_expression(self):
        """测试：正常路径 - 带复杂表达式的赋值 LET y = a + b;"""
        tokens = [
            self._create_token("LET", "LET", 2, 1),
            self._create_token("IDENTIFIER", "y", 2, 5),
            self._create_token("EQUALS", "=", 2, 7),
            self._create_token("IDENTIFIER", "a", 2, 9),
            self._create_token("PLUS", "+", 2, 11),
            self._create_token("IDENTIFIER", "b", 2, 13),
            self._create_token("SEMICOLON", ";", 2, 14),
        ]
        parser_state = self._create_parser_state(tokens)

        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_def_statement_package._parse_block_package._parse_assign_stmt_package._parse_expression_package._parse_expression_src._parse_expression') as mock_parse_expression:
            mock_parse_expression.return_value = {
                "type": "BINARY_OP",
                "value": "+",
                "line": 2,
                "column": 11,
                "children": [
                    {"type": "IDENTIFIER", "value": "a", "line": 2, "column": 9, "children": []},
                    {"type": "IDENTIFIER", "value": "b", "line": 2, "column": 13, "children": []}
                ]
            }

            result = _parse_assign_stmt(parser_state)

            self.assertEqual(result["type"], "ASSIGN")
            self.assertEqual(result["line"], 2)
            self.assertEqual(result["column"], 1)
            self.assertEqual(len(result["children"]), 2)
            self.assertEqual(result["children"][0]["value"], "y")
            self.assertEqual(result["children"][1]["type"], "BINARY_OP")
            self.assertEqual(parser_state["pos"], 7)

    def test_error_missing_let_keyword(self):
        """测试：错误路径 - 缺少 LET 关键字"""
        tokens = [
            self._create_token("IDENTIFIER", "x", 1, 1),
            self._create_token("EQUALS", "=", 1, 3),
            self._create_token("NUMBER", "5", 1, 5),
            self._create_token("SEMICOLON", ";", 1, 6),
        ]
        parser_state = self._create_parser_state(tokens)

        with self.assertRaises(SyntaxError) as context:
            _parse_assign_stmt(parser_state)

        self.assertIn("Expected LET", str(context.exception))
        self.assertIn("got IDENTIFIER", str(context.exception))

    def test_error_missing_identifier(self):
        """测试：错误路径 - 缺少标识符"""
        tokens = [
            self._create_token("LET", "LET", 1, 1),
            self._create_token("EQUALS", "=", 1, 5),
            self._create_token("NUMBER", "5", 1, 7),
            self._create_token("SEMICOLON", ";", 1, 8),
        ]
        parser_state = self._create_parser_state(tokens)

        with self.assertRaises(SyntaxError) as context:
            _parse_assign_stmt(parser_state)

        self.assertIn("Expected IDENTIFIER", str(context.exception))
        self.assertIn("got EQUALS", str(context.exception))

    def test_error_missing_equals(self):
        """测试：错误路径 - 缺少 EQUALS 运算符"""
        tokens = [
            self._create_token("LET", "LET", 1, 1),
            self._create_token("IDENTIFIER", "x", 1, 5),
            self._create_token("NUMBER", "5", 1, 7),
            self._create_token("SEMICOLON", ";", 1, 8),
        ]
        parser_state = self._create_parser_state(tokens)

        with self.assertRaises(SyntaxError) as context:
            _parse_assign_stmt(parser_state)

        self.assertIn("Expected EQUALS", str(context.exception))
        self.assertIn("got NUMBER", str(context.exception))

    def test_error_missing_semicolon(self):
        """测试：错误路径 - 缺少 SEMICOLON 结束符"""
        tokens = [
            self._create_token("LET", "LET", 1, 1),
            self._create_token("IDENTIFIER", "x", 1, 5),
            self._create_token("EQUALS", "=", 1, 7),
            self._create_token("NUMBER", "5", 1, 9),
        ]
        parser_state = self._create_parser_state(tokens)

        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_def_statement_package._parse_block_package._parse_assign_stmt_package._parse_expression_package._parse_expression_src._parse_expression') as mock_parse_expression:
            mock_parse_expression.return_value = {
                "type": "NUMBER",
                "value": "5",
                "line": 1,
                "column": 9,
                "children": []
            }

            with self.assertRaises(SyntaxError) as context:
                _parse_assign_stmt(parser_state)

            self.assertIn("Expected SEMICOLON", str(context.exception))

    def test_error_unexpected_end_of_input(self):
        """测试：错误路径 - 意外的输入结束"""
        tokens = [
            self._create_token("LET", "LET", 1, 1),
            self._create_token("IDENTIFIER", "x", 1, 5),
        ]
        parser_state = self._create_parser_state(tokens)

        with self.assertRaises(SyntaxError) as context:
            _parse_assign_stmt(parser_state)

        self.assertIn("Unexpected end of input", str(context.exception))
        self.assertIn("expected EQUALS", str(context.exception))

    def test_error_expression_parse_failure(self):
        """测试：错误路径 - 表达式解析失败"""
        tokens = [
            self._create_token("LET", "LET", 1, 1),
            self._create_token("IDENTIFIER", "x", 1, 5),
            self._create_token("EQUALS", "=", 1, 7),
            self._create_token("NUMBER", "5", 1, 9),
            self._create_token("SEMICOLON", ";", 1, 10),
        ]
        parser_state = self._create_parser_state(tokens)

        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_def_statement_package._parse_block_package._parse_assign_stmt_package._parse_expression_package._parse_expression_src._parse_expression') as mock_parse_expression:
            mock_parse_expression.side_effect = SyntaxError("Invalid expression syntax")

            with self.assertRaises(SyntaxError) as context:
                _parse_assign_stmt(parser_state)

            self.assertIn("Invalid expression syntax", str(context.exception))
            # 验证在表达式解析失败时，pos 没有继续更新（停在 EQUALS 之后）
            self.assertEqual(parser_state["pos"], 3)

    def test_boundary_single_char_identifier(self):
        """测试：边界值 - 单字符标识符"""
        tokens = [
            self._create_token("LET", "LET", 1, 1),
            self._create_token("IDENTIFIER", "i", 1, 5),
            self._create_token("EQUALS", "=", 1, 7),
            self._create_token("NUMBER", "0", 1, 9),
            self._create_token("SEMICOLON", ";", 1, 10),
        ]
        parser_state = self._create_parser_state(tokens)

        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_def_statement_package._parse_block_package._parse_assign_stmt_package._parse_expression_package._parse_expression_src._parse_expression') as mock_parse_expression:
            mock_parse_expression.return_value = {
                "type": "NUMBER",
                "value": "0",
                "line": 1,
                "column": 9,
                "children": []
            }

            result = _parse_assign_stmt(parser_state)

            self.assertEqual(result["children"][0]["value"], "i")
            self.assertEqual(parser_state["pos"], 5)

    def test_boundary_long_identifier(self):
        """测试：边界值 - 长标识符"""
        long_ident = "very_long_variable_name_123"
        tokens = [
            self._create_token("LET", "LET", 5, 10),
            self._create_token("IDENTIFIER", long_ident, 5, 14),
            self._create_token("EQUALS", "=", 5, 42),
            self._create_token("STRING", '"hello"', 5, 44),
            self._create_token("SEMICOLON", ";", 5, 52),
        ]
        parser_state = self._create_parser_state(tokens)

        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_def_statement_package._parse_block_package._parse_assign_stmt_package._parse_expression_package._parse_expression_src._parse_expression') as mock_parse_expression:
            mock_parse_expression.return_value = {
                "type": "STRING",
                "value": '"hello"',
                "line": 5,
                "column": 44,
                "children": []
            }

            result = _parse_assign_stmt(parser_state)

            self.assertEqual(result["children"][0]["value"], long_ident)
            self.assertEqual(result["line"], 5)
            self.assertEqual(result["column"], 10)

    def test_boundary_multiline_tokens(self):
        """测试：边界值 - 跨多行的 token"""
        tokens = [
            self._create_token("LET", "LET", 10, 1),
            self._create_token("IDENTIFIER", "count", 10, 5),
            self._create_token("EQUALS", "=", 10, 11),
            self._create_token("NUMBER", "42", 11, 5),
            self._create_token("SEMICOLON", ";", 11, 7),
        ]
        parser_state = self._create_parser_state(tokens)

        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_def_statement_package._parse_block_package._parse_assign_stmt_package._parse_expression_package._parse_expression_src._parse_expression') as mock_parse_expression:
            mock_parse_expression.return_value = {
                "type": "NUMBER",
                "value": "42",
                "line": 11,
                "column": 5,
                "children": []
            }

            result = _parse_assign_stmt(parser_state)

            self.assertEqual(result["line"], 10)
            self.assertEqual(result["column"], 1)
            self.assertEqual(result["children"][0]["line"], 10)
            self.assertEqual(result["children"][1]["line"], 11)

    def test_expect_token_helper_success(self):
        """测试：_expect_token 辅助函数 - 成功消费 token"""
        tokens = [
            self._create_token("IDENTIFIER", "x", 1, 1),
            self._create_token("NUMBER", "5", 1, 3),
        ]
        parser_state = self._create_parser_state(tokens)

        result = _expect_token(parser_state, "IDENTIFIER")

        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "x")
        self.assertEqual(parser_state["pos"], 1)

    def test_expect_token_helper_wrong_type(self):
        """测试：_expect_token 辅助函数 - token 类型不匹配"""
        tokens = [
            self._create_token("NUMBER", "5", 1, 1),
        ]
        parser_state = self._create_parser_state(tokens)

        with self.assertRaises(SyntaxError) as context:
            _expect_token(parser_state, "IDENTIFIER")

        self.assertIn("Expected IDENTIFIER", str(context.exception))
        self.assertIn("got NUMBER", str(context.exception))
        # 验证 pos 没有更新
        self.assertEqual(parser_state["pos"], 0)

    def test_expect_token_helper_end_of_input(self):
        """测试：_expect_token 辅助函数 - 输入结束"""
        tokens = []
        parser_state = self._create_parser_state(tokens, pos=0)

        with self.assertRaises(SyntaxError) as context:
            _expect_token(parser_state, "LET")

        self.assertIn("Unexpected end of input", str(context.exception))
        self.assertIn("expected LET", str(context.exception))


if __name__ == "__main__":
    unittest.main()

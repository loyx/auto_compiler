# -*- coding: utf-8 -*-
"""单元测试：_parse_while_stmt 函数"""

import unittest
from unittest.mock import patch
from typing import Any, Dict

from ._parse_while_stmt_src import _parse_while_stmt


class TestParseWhileStmt(unittest.TestCase):
    """_parse_while_stmt 函数的单元测试"""

    def _create_token(self, token_type: str, value: str = "", line: int = 1, column: int = 1) -> Dict[str, Any]:
        """辅助函数：创建 token 字典"""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def _create_parser_state(self, tokens: list, pos: int = 0, filename: str = "test.py") -> Dict[str, Any]:
        """辅助函数：创建 parser_state 字典"""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename
        }

    def test_happy_path_simple_while(self):
        """测试：简单的 while 语句解析"""
        tokens = [
            self._create_token("WHILE", "while", 1, 1),
            self._create_token("LPAREN", "(", 1, 7),
            self._create_token("IDENTIFIER", "x", 1, 8),
            self._create_token("RPAREN", ")", 1, 9),
            self._create_token("LBRACE", "{", 1, 11),
            self._create_token("RBRACE", "}", 1, 12),
        ]
        parser_state = self._create_parser_state(tokens, 0)

        mock_condition_ast = {"type": "EXPR", "value": "x"}
        mock_body_ast = {"type": "BLOCK", "children": []}

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_for_stmt_package._parse_block_package._parse_while_stmt_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_for_stmt_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_block_src._parse_block") as mock_parse_block:
                mock_parse_expr.return_value = mock_condition_ast
                mock_parse_block.return_value = mock_body_ast

                result = _parse_while_stmt(parser_state)

                self.assertEqual(result["type"], "WHILE")
                self.assertEqual(result["condition"], mock_condition_ast)
                self.assertEqual(result["body"], mock_body_ast)
                self.assertEqual(result["line"], 1)
                self.assertEqual(result["column"], 1)
                self.assertEqual(parser_state["pos"], 6)

    def test_happy_path_with_nested_expression(self):
        """测试：while 语句包含复杂条件表达式"""
        tokens = [
            self._create_token("WHILE", "while", 2, 5),
            self._create_token("LPAREN", "(", 2, 11),
            self._create_token("IDENTIFIER", "x", 2, 12),
            self._create_token("OPERATOR", ">", 2, 14),
            self._create_token("NUMBER", "0", 2, 16),
            self._create_token("RPAREN", ")", 2, 17),
            self._create_token("LBRACE", "{", 2, 19),
            self._create_token("IDENTIFIER", "x", 2, 20),
            self._create_token("OPERATOR", "-", 2, 22),
            self._create_token("OPERATOR", "-", 2, 24),
            self._create_token("RBRACE", "}", 2, 25),
        ]
        parser_state = self._create_parser_state(tokens, 0)

        mock_condition_ast = {"type": "BINARY_OP", "left": "x", "op": ">", "right": "0"}
        mock_body_ast = {"type": "BLOCK", "children": [{"type": "ASSIGN"}]}

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_for_stmt_package._parse_block_package._parse_while_stmt_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_for_stmt_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_block_src._parse_block") as mock_parse_block:
                mock_parse_expr.return_value = mock_condition_ast
                mock_parse_block.return_value = mock_body_ast

                result = _parse_while_stmt(parser_state)

                self.assertEqual(result["type"], "WHILE")
                self.assertEqual(result["condition"], mock_condition_ast)
                self.assertEqual(result["body"], mock_body_ast)
                self.assertEqual(result["line"], 2)
                self.assertEqual(result["column"], 5)

    def test_error_missing_lparen(self):
        """测试：缺少左括号时抛出 SyntaxError"""
        tokens = [
            self._create_token("WHILE", "while", 3, 1),
            self._create_token("IDENTIFIER", "x", 3, 7),
        ]
        parser_state = self._create_parser_state(tokens, 0)

        with self.assertRaises(SyntaxError) as context:
            _parse_while_stmt(parser_state)

        self.assertIn("test.py:3:1", str(context.exception))
        self.assertIn("expected '(' after 'while'", str(context.exception))

    def test_error_missing_rparen(self):
        """测试：缺少右括号时抛出 SyntaxError"""
        tokens = [
            self._create_token("WHILE", "while", 4, 1),
            self._create_token("LPAREN", "(", 4, 7),
            self._create_token("IDENTIFIER", "x", 4, 8),
            self._create_token("LBRACE", "{", 4, 10),
        ]
        parser_state = self._create_parser_state(tokens, 0)

        mock_condition_ast = {"type": "EXPR", "value": "x"}

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_for_stmt_package._parse_block_package._parse_while_stmt_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = mock_condition_ast

            with self.assertRaises(SyntaxError) as context:
                _parse_while_stmt(parser_state)

            self.assertIn("test.py:4:1", str(context.exception))
            self.assertIn("expected ')' after while condition", str(context.exception))

    def test_error_end_of_tokens_after_while(self):
        """测试：WHILE 后立即结束 tokens 时抛出 SyntaxError"""
        tokens = [
            self._create_token("WHILE", "while", 5, 1),
        ]
        parser_state = self._create_parser_state(tokens, 0)

        with self.assertRaises(SyntaxError) as context:
            _parse_while_stmt(parser_state)

        self.assertIn("test.py:5:1", str(context.exception))
        self.assertIn("expected '(' after 'while'", str(context.exception))

    def test_error_end_of_tokens_after_lparen(self):
        """测试：LPAREN 后立即结束 tokens 时抛出 SyntaxError"""
        tokens = [
            self._create_token("WHILE", "while", 6, 1),
            self._create_token("LPAREN", "(", 6, 7),
        ]
        parser_state = self._create_parser_state(tokens, 0)

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_for_stmt_package._parse_block_package._parse_while_stmt_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = {"type": "EXPR"}

            with self.assertRaises(SyntaxError) as context:
                _parse_while_stmt(parser_state)

            self.assertIn("test.py:6:1", str(context.exception))
            self.assertIn("expected ')' after while condition", str(context.exception))

    def test_parser_state_pos_updated_correctly(self):
        """测试：parser_state 的 pos 正确更新"""
        tokens = [
            self._create_token("WHILE", "while", 1, 1),
            self._create_token("LPAREN", "(", 1, 7),
            self._create_token("IDENTIFIER", "x", 1, 8),
            self._create_token("RPAREN", ")", 1, 9),
            self._create_token("LBRACE", "{", 1, 11),
            self._create_token("RBRACE", "}", 1, 12),
            self._create_token("SEMICOLON", ";", 1, 13),
        ]
        parser_state = self._create_parser_state(tokens, 0)

        mock_condition_ast = {"type": "EXPR"}
        mock_body_ast = {"type": "BLOCK"}

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_for_stmt_package._parse_block_package._parse_while_stmt_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_for_stmt_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_block_src._parse_block") as mock_parse_block:
                def parse_expr_side_effect(state):
                    state["pos"] = 3
                    return mock_condition_ast

                def parse_block_side_effect(state):
                    state["pos"] = 6
                    return mock_body_ast

                mock_parse_expr.side_effect = parse_expr_side_effect
                mock_parse_block.side_effect = parse_block_side_effect

                result = _parse_while_stmt(parser_state)

                self.assertEqual(parser_state["pos"], 6)

    def test_default_filename_when_missing(self):
        """测试：当 filename 缺失时使用默认值"""
        tokens = [
            self._create_token("WHILE", "while", 1, 1),
            self._create_token("IDENTIFIER", "x", 1, 7),
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
        }

        with self.assertRaises(SyntaxError) as context:
            _parse_while_stmt(parser_state)

        self.assertIn("<unknown>:1:1", str(context.exception))

    def test_token_without_line_column_info(self):
        """测试：token 缺少 line/column 信息时使用默认值 0"""
        tokens = [
            {"type": "WHILE", "value": "while"},
            {"type": "IDENTIFIER", "value": "x"},
        ]
        parser_state = self._create_parser_state(tokens, 0)

        with self.assertRaises(SyntaxError) as context:
            _parse_while_stmt(parser_state)

        self.assertIn(":0:0:", str(context.exception))

    def test_mock_parse_expression_called(self):
        """测试：验证 _parse_expression 被正确调用"""
        tokens = [
            self._create_token("WHILE", "while", 1, 1),
            self._create_token("LPAREN", "(", 1, 7),
            self._create_token("IDENTIFIER", "x", 1, 8),
            self._create_token("RPAREN", ")", 1, 9),
            self._create_token("LBRACE", "{", 1, 11),
            self._create_token("RBRACE", "}", 1, 12),
        ]
        parser_state = self._create_parser_state(tokens, 0)

        mock_condition_ast = {"type": "EXPR"}
        mock_body_ast = {"type": "BLOCK"}

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_for_stmt_package._parse_block_package._parse_while_stmt_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_for_stmt_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_block_src._parse_block") as mock_parse_block:
                mock_parse_expr.return_value = mock_condition_ast
                mock_parse_block.return_value = mock_body_ast

                _parse_while_stmt(parser_state)

                mock_parse_expr.assert_called_once()
                mock_parse_block.assert_called_once()

    def test_ast_structure_complete(self):
        """测试：返回的 AST 结构完整且符合预期"""
        tokens = [
            self._create_token("WHILE", "while", 10, 5),
            self._create_token("LPAREN", "(", 10, 11),
            self._create_token("IDENTIFIER", "x", 10, 12),
            self._create_token("RPAREN", ")", 10, 13),
            self._create_token("LBRACE", "{", 10, 15),
            self._create_token("RBRACE", "}", 10, 16),
        ]
        parser_state = self._create_parser_state(tokens, 0)

        mock_condition_ast = {"type": "EXPR", "value": "x", "line": 10, "column": 12}
        mock_body_ast = {"type": "BLOCK", "children": [], "line": 10, "column": 15}

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_for_stmt_package._parse_block_package._parse_while_stmt_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_for_stmt_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_block_src._parse_block") as mock_parse_block:
                mock_parse_expr.return_value = mock_condition_ast
                mock_parse_block.return_value = mock_body_ast

                result = _parse_while_stmt(parser_state)

                self.assertIn("type", result)
                self.assertIn("condition", result)
                self.assertIn("body", result)
                self.assertIn("line", result)
                self.assertIn("column", result)
                self.assertEqual(result["type"], "WHILE")
                self.assertEqual(result["line"], 10)
                self.assertEqual(result["column"], 5)


if __name__ == "__main__":
    unittest.main()

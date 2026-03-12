# === std / third-party imports ===
import unittest
from unittest.mock import patch
from typing import Dict, Any

# === relative imports ===
from ._parse_if_stmt_src import _parse_if_stmt


class TestParseIfStmt(unittest.TestCase):
    """单元测试：_parse_if_stmt 函数"""

    def _create_parser_state(self, tokens: list, pos: int = 0, filename: str = "test.src") -> Dict[str, Any]:
        """辅助方法：创建 parser_state"""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename
        }

    def _create_token(self, token_type: str, value: str = "", line: int = 1, column: int = 1) -> Dict[str, Any]:
        """辅助方法：创建 token"""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def test_if_stmt_without_else(self):
        """测试：if 语句不含 else 分支"""
        tokens = [
            self._create_token("IF", "if", 1, 1),
            self._create_token("LPAREN", "(", 1, 3),
            self._create_token("IDENTIFIER", "x", 1, 4),
            self._create_token("RPAREN", ")", 1, 5),
            self._create_token("EXPR_STMT", "x = 1", 1, 7),
        ]
        parser_state = self._create_parser_state(tokens)

        # Mock 子函数
        mock_condition = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 4}
        mock_then_stmt = {"type": "EXPR_STMT", "value": "x = 1", "line": 1, "column": 7}

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._expect_token_package._expect_token_src._expect_token") as mock_expect, \
             patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr, \
             patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_statement_package._parse_statement_src._parse_statement") as mock_parse_stmt:

            mock_parse_expr.return_value = mock_condition
            mock_parse_stmt.return_value = mock_then_stmt
            # _expect_token 会被调用两次（LPAREN 和 RPAREN）
            mock_expect.side_effect = [
                self._create_token("LPAREN", "(", 1, 3),
                self._create_token("RPAREN", ")", 1, 5)
            ]

            result = _parse_if_stmt(parser_state)

            # 验证返回的 AST 节点
            self.assertEqual(result["type"], "IF_STMT")
            self.assertEqual(len(result["children"]), 2)
            self.assertEqual(result["children"][0], mock_condition)
            self.assertEqual(result["children"][1], mock_then_stmt)
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            self.assertIsNone(result["value"])

            # 验证 pos 更新到语句结束
            self.assertEqual(parser_state["pos"], 5)

            # 验证子函数调用
            self.assertEqual(mock_expect.call_count, 2)
            mock_parse_expr.assert_called_once()
            self.assertEqual(mock_parse_stmt.call_count, 1)

    def test_if_stmt_with_else(self):
        """测试：if 语句含 else 分支"""
        tokens = [
            self._create_token("IF", "if", 1, 1),
            self._create_token("LPAREN", "(", 1, 3),
            self._create_token("IDENTIFIER", "x", 1, 4),
            self._create_token("RPAREN", ")", 1, 5),
            self._create_token("EXPR_STMT", "x = 1", 1, 7),
            self._create_token("ELSE", "else", 2, 1),
            self._create_token("EXPR_STMT", "x = 2", 2, 6),
        ]
        parser_state = self._create_parser_state(tokens)

        mock_condition = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 4}
        mock_then_stmt = {"type": "EXPR_STMT", "value": "x = 1", "line": 1, "column": 7}
        mock_else_stmt = {"type": "EXPR_STMT", "value": "x = 2", "line": 2, "column": 6}

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._expect_token_package._expect_token_src._expect_token") as mock_expect, \
             patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr, \
             patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_statement_package._parse_statement_src._parse_statement") as mock_parse_stmt:

            mock_parse_expr.return_value = mock_condition
            mock_parse_stmt.side_effect = [mock_then_stmt, mock_else_stmt]
            mock_expect.side_effect = [
                self._create_token("LPAREN", "(", 1, 3),
                self._create_token("RPAREN", ")", 1, 5)
            ]

            result = _parse_if_stmt(parser_state)

            # 验证返回的 AST 节点
            self.assertEqual(result["type"], "IF_STMT")
            self.assertEqual(len(result["children"]), 3)
            self.assertEqual(result["children"][0], mock_condition)
            self.assertEqual(result["children"][1], mock_then_stmt)
            self.assertEqual(result["children"][2], mock_else_stmt)
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)

            # 验证 pos 更新到语句结束
            self.assertEqual(parser_state["pos"], 7)

            # 验证子函数调用次数
            self.assertEqual(mock_expect.call_count, 2)
            mock_parse_expr.assert_called_once()
            self.assertEqual(mock_parse_stmt.call_count, 2)

    def test_if_stmt_with_block_statement(self):
        """测试：if 语句的 then 分支为代码块"""
        tokens = [
            self._create_token("IF", "if", 1, 1),
            self._create_token("LPAREN", "(", 1, 3),
            self._create_token("IDENTIFIER", "x", 1, 4),
            self._create_token("RPAREN", ")", 1, 5),
            self._create_token("BLOCK", "{...}", 1, 7),
        ]
        parser_state = self._create_parser_state(tokens)

        mock_condition = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 4}
        mock_block_stmt = {"type": "BLOCK", "value": "{...}", "line": 1, "column": 7}

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._expect_token_package._expect_token_src._expect_token") as mock_expect, \
             patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr, \
             patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_statement_package._parse_statement_src._parse_statement") as mock_parse_stmt:

            mock_parse_expr.return_value = mock_condition
            mock_parse_stmt.return_value = mock_block_stmt
            mock_expect.side_effect = [
                self._create_token("LPAREN", "(", 1, 3),
                self._create_token("RPAREN", ")", 1, 5)
            ]

            result = _parse_if_stmt(parser_state)

            self.assertEqual(result["type"], "IF_STMT")
            self.assertEqual(len(result["children"]), 2)
            self.assertEqual(result["children"][1]["type"], "BLOCK")

    def test_if_stmt_complex_condition(self):
        """测试：if 语句含复杂条件表达式"""
        tokens = [
            self._create_token("IF", "if", 1, 1),
            self._create_token("LPAREN", "(", 1, 3),
            self._create_token("IDENTIFIER", "x", 1, 4),
            self._create_token("BINARY_OP", ">", 1, 6),
            self._create_token("LITERAL", "0", 1, 8),
            self._create_token("RPAREN", ")", 1, 9),
            self._create_token("EXPR_STMT", "print(x)", 1, 11),
        ]
        parser_state = self._create_parser_state(tokens)

        mock_condition = {
            "type": "BINARY_OP",
            "value": ">",
            "children": [
                {"type": "IDENTIFIER", "value": "x"},
                {"type": "LITERAL", "value": "0"}
            ],
            "line": 1,
            "column": 4
        }
        mock_then_stmt = {"type": "EXPR_STMT", "value": "print(x)", "line": 1, "column": 11}

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._expect_token_package._expect_token_src._expect_token") as mock_expect, \
             patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr, \
             patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_statement_package._parse_statement_src._parse_statement") as mock_parse_stmt:

            mock_parse_expr.return_value = mock_condition
            mock_parse_stmt.return_value = mock_then_stmt
            mock_expect.side_effect = [
                self._create_token("LPAREN", "(", 1, 3),
                self._create_token("RPAREN", ")", 1, 9)
            ]

            result = _parse_if_stmt(parser_state)

            self.assertEqual(result["type"], "IF_STMT")
            self.assertEqual(result["children"][0]["type"], "BINARY_OP")
            self.assertEqual(len(result["children"][0]["children"]), 2)

    def test_if_stmt_at_different_position(self):
        """测试：if 语句在 token 列表的不同位置"""
        tokens = [
            self._create_token("VAR_DECL", "var x", 1, 1),
            self._create_token("IF", "if", 1, 10),
            self._create_token("LPAREN", "(", 1, 12),
            self._create_token("IDENTIFIER", "x", 1, 13),
            self._create_token("RPAREN", ")", 1, 14),
            self._create_token("EXPR_STMT", "x++", 1, 16),
        ]
        parser_state = self._create_parser_state(tokens, pos=1)

        mock_condition = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 13}
        mock_then_stmt = {"type": "EXPR_STMT", "value": "x++", "line": 1, "column": 16}

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._expect_token_package._expect_token_src._expect_token") as mock_expect, \
             patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr, \
             patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_statement_package._parse_statement_src._parse_statement") as mock_parse_stmt:

            mock_parse_expr.return_value = mock_condition
            mock_parse_stmt.return_value = mock_then_stmt
            mock_expect.side_effect = [
                self._create_token("LPAREN", "(", 1, 12),
                self._create_token("RPAREN", ")", 1, 14)
            ]

            result = _parse_if_stmt(parser_state)

            self.assertEqual(result["type"], "IF_STMT")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 10)
            self.assertEqual(parser_state["pos"], 5)

    def test_if_stmt_no_else_when_next_token_not_else(self):
        """测试：当下一 token 不是 ELSE 时不解析 else 分支"""
        tokens = [
            self._create_token("IF", "if", 1, 1),
            self._create_token("LPAREN", "(", 1, 3),
            self._create_token("IDENTIFIER", "x", 1, 4),
            self._create_token("RPAREN", ")", 1, 5),
            self._create_token("EXPR_STMT", "x = 1", 1, 7),
            self._create_token("IDENTIFIER", "y", 2, 1),  # 不是 ELSE
        ]
        parser_state = self._create_parser_state(tokens)

        mock_condition = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 4}
        mock_then_stmt = {"type": "EXPR_STMT", "value": "x = 1", "line": 1, "column": 7}

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._expect_token_package._expect_token_src._expect_token") as mock_expect, \
             patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr, \
             patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_statement_package._parse_statement_src._parse_statement") as mock_parse_stmt:

            mock_parse_expr.return_value = mock_condition
            mock_parse_stmt.return_value = mock_then_stmt
            mock_expect.side_effect = [
                self._create_token("LPAREN", "(", 1, 3),
                self._create_token("RPAREN", ")", 1, 5)
            ]

            result = _parse_if_stmt(parser_state)

            self.assertEqual(result["type"], "IF_STMT")
            self.assertEqual(len(result["children"]), 2)  # 只有 condition 和 then_stmt
            self.assertEqual(parser_state["pos"], 5)  # pos 不消耗非 ELSE token
            mock_parse_stmt.assert_called_once()  # 只调用一次解析 then 分支

    def test_if_stmt_at_end_of_tokens(self):
        """测试：if 语句在 token 列表末尾（无后续 token）"""
        tokens = [
            self._create_token("IF", "if", 1, 1),
            self._create_token("LPAREN", "(", 1, 3),
            self._create_token("IDENTIFIER", "x", 1, 4),
            self._create_token("RPAREN", ")", 1, 5),
            self._create_token("EXPR_STMT", "x = 1", 1, 7),
        ]
        parser_state = self._create_parser_state(tokens)

        mock_condition = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 4}
        mock_then_stmt = {"type": "EXPR_STMT", "value": "x = 1", "line": 1, "column": 7}

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._expect_token_package._expect_token_src._expect_token") as mock_expect, \
             patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr, \
             patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_statement_package._parse_statement_src._parse_statement") as mock_parse_stmt:

            mock_parse_expr.return_value = mock_condition
            mock_parse_stmt.return_value = mock_then_stmt
            mock_expect.side_effect = [
                self._create_token("LPAREN", "(", 1, 3),
                self._create_token("RPAREN", ")", 1, 5)
            ]

            result = _parse_if_stmt(parser_state)

            self.assertEqual(result["type"], "IF_STMT")
            self.assertEqual(len(result["children"]), 2)
            self.assertEqual(parser_state["pos"], 5)


if __name__ == "__main__":
    unittest.main()

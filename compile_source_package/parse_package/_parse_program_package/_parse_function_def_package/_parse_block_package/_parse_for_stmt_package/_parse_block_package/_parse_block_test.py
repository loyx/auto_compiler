# === std / third-party imports ===
import unittest
from typing import Any, Dict
from unittest.mock import patch

# === relative imports ===
from ._parse_block_src import _parse_block

# === type aliases ===
Token = Dict[str, Any]
AST = Dict[str, Any]
ParserState = Dict[str, Any]


class TestParseBlock(unittest.TestCase):
    """单元测试：_parse_block 函数"""

    def _create_token(self, token_type: str, value: str = "", line: int = 1, column: int = 1) -> Token:
        """辅助函数：创建 token"""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def _create_parser_state(self, tokens: list, pos: int = 0, filename: str = "test.py") -> ParserState:
        """辅助函数：创建 parser_state"""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename
        }

    def test_happy_path_single_statement(self):
        """测试：正常路径 - 单个语句的块"""
        tokens = [
            self._create_token("INDENT", "", 1, 1),
            self._create_token("IDENTIFIER", "x", 2, 5),
            self._create_token("DEDENT", "", 3, 1),
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        mock_stmt = {"type": "EXPR_STMT", "children": [], "value": "x", "line": 2, "column": 5}

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_block_src._parse_statement") as mock_parse_statement:
            mock_parse_statement.return_value = mock_stmt

            result = _parse_block(parser_state)

        # 验证返回的 BLOCK 节点
        self.assertEqual(result["type"], "BLOCK")
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0], mock_stmt)
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)

        # 验证 pos 更新到 DEDENT 之后
        self.assertEqual(parser_state["pos"], 3)

        # 验证 _parse_statement 被调用
        mock_parse_statement.assert_called_once()

    def test_happy_path_multiple_statements(self):
        """测试：正常路径 - 多个语句的块"""
        tokens = [
            self._create_token("INDENT", "", 1, 1),
            self._create_token("IDENTIFIER", "x", 2, 5),
            self._create_token("IDENTIFIER", "y", 3, 5),
            self._create_token("IDENTIFIER", "z", 4, 5),
            self._create_token("DEDENT", "", 5, 1),
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        mock_stmt1 = {"type": "EXPR_STMT", "children": [], "value": "x", "line": 2, "column": 5}
        mock_stmt2 = {"type": "EXPR_STMT", "children": [], "value": "y", "line": 3, "column": 5}
        mock_stmt3 = {"type": "EXPR_STMT", "children": [], "value": "z", "line": 4, "column": 5}

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_block_src._parse_statement") as mock_parse_statement:
            mock_parse_statement.side_effect = [mock_stmt1, mock_stmt2, mock_stmt3]

            result = _parse_block(parser_state)

        # 验证返回的 BLOCK 节点
        self.assertEqual(result["type"], "BLOCK")
        self.assertEqual(len(result["children"]), 3)
        self.assertEqual(result["children"][0], mock_stmt1)
        self.assertEqual(result["children"][1], mock_stmt2)
        self.assertEqual(result["children"][2], mock_stmt3)
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)

        # 验证 pos 更新到 DEDENT 之后
        self.assertEqual(parser_state["pos"], 5)

        # 验证 _parse_statement 被调用 3 次
        self.assertEqual(mock_parse_statement.call_count, 3)

    def test_happy_path_empty_block(self):
        """测试：正常路径 - 空块（INDENT 后立即 DEDENT）"""
        tokens = [
            self._create_token("INDENT", "", 1, 1),
            self._create_token("DEDENT", "", 2, 1),
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        result = _parse_block(parser_state)

        # 验证返回的 BLOCK 节点
        self.assertEqual(result["type"], "BLOCK")
        self.assertEqual(len(result["children"]), 0)
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)

        # 验证 pos 更新到 DEDENT 之后
        self.assertEqual(parser_state["pos"], 2)

    def test_error_eof_before_indent(self):
        """测试：错误情况 - 输入在 INDENT 前结束"""
        tokens = []
        parser_state = self._create_parser_state(tokens, pos=0)

        with self.assertRaises(SyntaxError) as context:
            _parse_block(parser_state)

        self.assertIn("Unexpected end of input", str(context.exception))
        self.assertIn("INDENT", str(context.exception))

    def test_error_first_token_not_indent(self):
        """测试：错误情况 - 第一个 token 不是 INDENT"""
        tokens = [
            self._create_token("IDENTIFIER", "x", 1, 1),
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        with self.assertRaises(SyntaxError) as context:
            _parse_block(parser_state)

        self.assertIn("Expected INDENT", str(context.exception))
        self.assertIn("line 1", str(context.exception))

    def test_error_eof_before_dedent(self):
        """测试：错误情况 - 语句后没有 DEDENT 就结束"""
        tokens = [
            self._create_token("INDENT", "", 1, 1),
            self._create_token("IDENTIFIER", "x", 2, 5),
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        mock_stmt = {"type": "EXPR_STMT", "children": [], "value": "x", "line": 2, "column": 5}

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_block_src._parse_statement") as mock_parse_statement:
            mock_parse_statement.return_value = mock_stmt

            with self.assertRaises(SyntaxError) as context:
                _parse_block(parser_state)

        self.assertIn("Unexpected end of input", str(context.exception))
        self.assertIn("DEDENT", str(context.exception))

    def test_error_token_after_statements_not_dedent(self):
        """测试：错误情况 - 语句后的 token 不是 DEDENT"""
        tokens = [
            self._create_token("INDENT", "", 1, 1),
            self._create_token("IDENTIFIER", "x", 2, 5),
            self._create_token("IDENTIFIER", "y", 3, 5),  # 应该是 DEDENT 但却是其他 token
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        mock_stmt = {"type": "EXPR_STMT", "children": [], "value": "x", "line": 2, "column": 5}

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_statement_src._parse_statement") as mock_parse_statement:
            mock_parse_statement.return_value = mock_stmt

            with self.assertRaises(SyntaxError) as context:
                _parse_block(parser_state)

        self.assertIn("Expected DEDENT", str(context.exception))
        self.assertIn("line 3", str(context.exception))

    def test_pos_updated_correctly_after_dedent(self):
        """测试：验证 pos 正确更新到 DEDENT 之后的位置"""
        tokens = [
            self._create_token("INDENT", "", 1, 1),
            self._create_token("IDENTIFIER", "x", 2, 5),
            self._create_token("DEDENT", "", 3, 1),
            self._create_token("IDENTIFIER", "y", 4, 1),  # DEDENT 之后的 token
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        mock_stmt = {"type": "EXPR_STMT", "children": [], "value": "x", "line": 2, "column": 5}

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_statement_src._parse_statement") as mock_parse_statement:
            mock_parse_statement.return_value = mock_stmt

            result = _parse_block(parser_state)

        # 验证 pos 指向 DEDENT 之后的 token（索引 3）
        self.assertEqual(parser_state["pos"], 3)

    def test_block_line_column_from_indent_token(self):
        """测试：验证 BLOCK 节点的 line/column 来自 INDENT token"""
        tokens = [
            self._create_token("INDENT", "", 5, 10),  # 第 5 行，第 10 列
            self._create_token("IDENTIFIER", "x", 6, 5),
            self._create_token("DEDENT", "", 7, 1),
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        mock_stmt = {"type": "EXPR_STMT", "children": [], "value": "x", "line": 6, "column": 5}

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_statement_src._parse_statement") as mock_parse_statement:
            mock_parse_statement.return_value = mock_stmt

            result = _parse_block(parser_state)

        # 验证 BLOCK 节点的 line/column 来自 INDENT token
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 10)

    def test_parse_statement_called_with_correct_parser_state(self):
        """测试：验证 _parse_statement 被调用时传入正确的 parser_state"""
        tokens = [
            self._create_token("INDENT", "", 1, 1),
            self._create_token("IDENTIFIER", "x", 2, 5),
            self._create_token("DEDENT", "", 3, 1),
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        mock_stmt = {"type": "EXPR_STMT", "children": [], "value": "x", "line": 2, "column": 5}

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_statement_src._parse_statement") as mock_parse_statement:
            mock_parse_statement.return_value = mock_stmt
            mock_parse_statement.side_effect = lambda state: state.update({"pos": 2}) or mock_stmt

            result = _parse_block(parser_state)

        # 验证 _parse_statement 被调用
        mock_parse_statement.assert_called_once()
        # 验证传入的是同一个 parser_state 对象
        self.assertIs(mock_parse_statement.call_args[0][0], parser_state)


if __name__ == "__main__":
    unittest.main()

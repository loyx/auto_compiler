"""单元测试：_parse_block 函数"""
import unittest
from unittest.mock import patch, MagicMock

from ._parse_block_src import _parse_block


class TestParseBlock(unittest.TestCase):
    """测试 _parse_block 函数的各种场景"""

    def setUp(self):
        """每个测试前的准备工作"""
        self.mock_return_stmt = MagicMock()
        self.mock_assign_stmt = MagicMock()
        self.mock_if_stmt = MagicMock()
        self.mock_while_stmt = MagicMock()
        self.mock_for_stmt = MagicMock()
        self.mock_def_stmt = MagicMock()
        self.mock_expr_stmt = MagicMock()

    def _create_parser_state(self, tokens, pos=0):
        """创建 parser_state 辅助函数"""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": "test.py",
            "error": ""
        }

    def _create_token(self, token_type, value, line=1, column=1):
        """创建 token 辅助函数"""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def _create_ast_node(self, node_type, line=1, column=1, children=None, value=None):
        """创建 AST 节点辅助函数"""
        return {
            "type": node_type,
            "line": line,
            "column": column,
            "children": children if children is not None else [],
            "value": value
        }

    @patch('._parse_block_src._parse_return_stmt')
    @patch('._parse_block_src._parse_assign_stmt')
    @patch('._parse_block_src._parse_if_stmt')
    @patch('._parse_block_src._parse_while_stmt')
    @patch('._parse_block_src._parse_for_stmt')
    @patch('._parse_block_src._parse_def_stmt')
    @patch('._parse_block_src._parse_expr_stmt')
    def test_empty_block_immediate_semicolon(
        self, mock_expr, mock_def, mock_for, mock_while, mock_if, mock_assign, mock_return
    ):
        """测试空块：立即遇到 SEMICOLON"""
        tokens = [self._create_token("SEMICOLON", ";", 1, 10)]
        parser_state = self._create_parser_state(tokens, pos=0)

        result = _parse_block(parser_state)

        self.assertEqual(result["type"], "BODY")
        self.assertEqual(result["line"], 0)
        self.assertEqual(result["column"], 0)
        self.assertEqual(result["children"], [])
        self.assertEqual(parser_state["pos"], 0)

    @patch('._parse_block_src._parse_return_stmt')
    @patch('._parse_block_src._parse_assign_stmt')
    @patch('._parse_block_src._parse_if_stmt')
    @patch('._parse_block_src._parse_while_stmt')
    @patch('._parse_block_src._parse_for_stmt')
    @patch('._parse_block_src._parse_def_stmt')
    @patch('._parse_block_src._parse_expr_stmt')
    def test_single_return_statement(
        self, mock_expr, mock_def, mock_for, mock_while, mock_if, mock_assign, mock_return
    ):
        """测试单个 return 语句"""
        tokens = [
            self._create_token("RETURN", "return", 1, 1),
            self._create_token("SEMICOLON", ";", 1, 15)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        return_ast = self._create_ast_node("RETURN", 1, 1)
        mock_return.return_value = return_ast

        result = _parse_block(parser_state)

        self.assertEqual(result["type"], "BODY")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0]["type"], "RETURN")
        self.assertEqual(parser_state["pos"], 1)
        mock_return.assert_called_once()

    @patch('._parse_block_src._parse_return_stmt')
    @patch('._parse_block_src._parse_assign_stmt')
    @patch('._parse_block_src._parse_if_stmt')
    @patch('._parse_block_src._parse_while_stmt')
    @patch('._parse_block_src._parse_for_stmt')
    @patch('._parse_block_src._parse_def_stmt')
    @patch('._parse_block_src._parse_expr_stmt')
    def test_multiple_statements(
        self, mock_expr, mock_def, mock_for, mock_while, mock_if, mock_assign, mock_return
    ):
        """测试多个语句"""
        tokens = [
            self._create_token("LET", "let", 1, 1),
            self._create_token("RETURN", "return", 2, 1),
            self._create_token("SEMICOLON", ";", 3, 1)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        assign_ast = self._create_ast_node("ASSIGN", 1, 1)
        return_ast = self._create_ast_node("RETURN", 2, 1)
        mock_assign.return_value = assign_ast
        mock_return.return_value = return_ast

        result = _parse_block(parser_state)

        self.assertEqual(result["type"], "BODY")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(len(result["children"]), 2)
        self.assertEqual(result["children"][0]["type"], "ASSIGN")
        self.assertEqual(result["children"][1]["type"], "RETURN")
        self.assertEqual(parser_state["pos"], 2)
        mock_assign.assert_called_once()
        mock_return.assert_called_once()

    @patch('._parse_block_src._parse_return_stmt')
    @patch('._parse_block_src._parse_assign_stmt')
    @patch('._parse_block_src._parse_if_stmt')
    @patch('._parse_block_src._parse_while_stmt')
    @patch('._parse_block_src._parse_for_stmt')
    @patch('._parse_block_src._parse_def_stmt')
    @patch('._parse_block_src._parse_expr_stmt')
    def test_if_statement_dispatch(
        self, mock_expr, mock_def, mock_for, mock_while, mock_if, mock_assign, mock_return
    ):
        """测试 IF 语句分发"""
        tokens = [
            self._create_token("IF", "if", 1, 1),
            self._create_token("SEMICOLON", ";", 1, 10)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        if_ast = self._create_ast_node("IF", 1, 1)
        mock_if.return_value = if_ast

        result = _parse_block(parser_state)

        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0]["type"], "IF")
        mock_if.assert_called_once()

    @patch('._parse_block_src._parse_return_stmt')
    @patch('._parse_block_src._parse_assign_stmt')
    @patch('._parse_block_src._parse_if_stmt')
    @patch('._parse_block_src._parse_while_stmt')
    @patch('._parse_block_src._parse_for_stmt')
    @patch('._parse_block_src._parse_def_stmt')
    @patch('._parse_block_src._parse_expr_stmt')
    def test_while_statement_dispatch(
        self, mock_expr, mock_def, mock_for, mock_while, mock_if, mock_assign, mock_return
    ):
        """测试 WHILE 语句分发"""
        tokens = [
            self._create_token("WHILE", "while", 1, 1),
            self._create_token("SEMICOLON", ";", 1, 10)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        while_ast = self._create_ast_node("WHILE", 1, 1)
        mock_while.return_value = while_ast

        result = _parse_block(parser_state)

        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0]["type"], "WHILE")
        mock_while.assert_called_once()

    @patch('._parse_block_src._parse_return_stmt')
    @patch('._parse_block_src._parse_assign_stmt')
    @patch('._parse_block_src._parse_if_stmt')
    @patch('._parse_block_src._parse_while_stmt')
    @patch('._parse_block_src._parse_for_stmt')
    @patch('._parse_block_src._parse_def_stmt')
    @patch('._parse_block_src._parse_expr_stmt')
    def test_for_statement_dispatch(
        self, mock_expr, mock_def, mock_for, mock_while, mock_if, mock_assign, mock_return
    ):
        """测试 FOR 语句分发"""
        tokens = [
            self._create_token("FOR", "for", 1, 1),
            self._create_token("SEMICOLON", ";", 1, 10)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        for_ast = self._create_ast_node("FOR", 1, 1)
        mock_for.return_value = for_ast

        result = _parse_block(parser_state)

        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0]["type"], "FOR")
        mock_for.assert_called_once()

    @patch('._parse_block_src._parse_return_stmt')
    @patch('._parse_block_src._parse_assign_stmt')
    @patch('._parse_block_src._parse_if_stmt')
    @patch('._parse_block_src._parse_while_stmt')
    @patch('._parse_block_src._parse_for_stmt')
    @patch('._parse_block_src._parse_def_stmt')
    @patch('._parse_block_src._parse_expr_stmt')
    def test_def_statement_dispatch(
        self, mock_expr, mock_def, mock_for, mock_while, mock_if, mock_assign, mock_return
    ):
        """测试 DEF 语句分发"""
        tokens = [
            self._create_token("DEF", "def", 1, 1),
            self._create_token("SEMICOLON", ";", 1, 10)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        def_ast = self._create_ast_node("DEF", 1, 1)
        mock_def.return_value = def_ast

        result = _parse_block(parser_state)

        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0]["type"], "DEF")
        mock_def.assert_called_once()

    @patch('._parse_block_src._parse_return_stmt')
    @patch('._parse_block_src._parse_assign_stmt')
    @patch('._parse_block_src._parse_if_stmt')
    @patch('._parse_block_src._parse_while_stmt')
    @patch('._parse_block_src._parse_for_stmt')
    @patch('._parse_block_src._parse_def_stmt')
    @patch('._parse_block_src._parse_expr_stmt')
    def test_expr_statement_dispatch(
        self, mock_expr, mock_def, mock_for, mock_while, mock_if, mock_assign, mock_return
    ):
        """测试表达式语句分发（未知 token 类型）"""
        tokens = [
            self._create_token("IDENTIFIER", "x", 1, 1),
            self._create_token("SEMICOLON", ";", 1, 10)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        expr_ast = self._create_ast_node("EXPR", 1, 1)
        mock_expr.return_value = expr_ast

        result = _parse_block(parser_state)

        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0]["type"], "EXPR")
        mock_expr.assert_called_once()

    @patch('._parse_block_src._parse_return_stmt')
    @patch('._parse_block_src._parse_assign_stmt')
    @patch('._parse_block_src._parse_if_stmt')
    @patch('._parse_block_src._parse_while_stmt')
    @patch('._parse_block_src._parse_for_stmt')
    @patch('._parse_block_src._parse_def_stmt')
    @patch('._parse_block_src._parse_expr_stmt')
    def test_pos_updates_correctly(
        self, mock_expr, mock_def, mock_for, mock_while, mock_if, mock_assign, mock_return
    ):
        """测试 parser_state pos 正确更新"""
        tokens = [
            self._create_token("LET", "let", 1, 1),
            self._create_token("RETURN", "return", 2, 1),
            self._create_token("IF", "if", 3, 1),
            self._create_token("SEMICOLON", ";", 4, 1)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        def side_effect(ps):
            ps["pos"] = ps["pos"] + 1
            return self._create_ast_node("STMT", ps["pos"], 1)

        mock_assign.side_effect = side_effect
        mock_return.side_effect = side_effect
        mock_if.side_effect = side_effect

        result = _parse_block(parser_state)

        self.assertEqual(len(result["children"]), 3)
        self.assertEqual(parser_state["pos"], 3)

    @patch('._parse_block_src._parse_return_stmt')
    @patch('._parse_block_src._parse_assign_stmt')
    @patch('._parse_block_src._parse_if_stmt')
    @patch('._parse_block_src._parse_while_stmt')
    @patch('._parse_block_src._parse_for_stmt')
    @patch('._parse_block_src._parse_def_stmt')
    @patch('._parse_block_src._parse_expr_stmt')
    def test_line_column_from_first_statement(
        self, mock_expr, mock_def, mock_for, mock_while, mock_if, mock_assign, mock_return
    ):
        """测试 BODY 节点的 line/column 来自第一个语句"""
        tokens = [
            self._create_token("LET", "let", 5, 10),
            self._create_token("RETURN", "return", 10, 20),
            self._create_token("SEMICOLON", ";", 11, 1)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        assign_ast = self._create_ast_node("ASSIGN", 5, 10)
        return_ast = self._create_ast_node("RETURN", 10, 20)
        mock_assign.return_value = assign_ast
        mock_return.return_value = return_ast

        result = _parse_block(parser_state)

        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 10)

    @patch('._parse_block_src._parse_return_stmt')
    @patch('._parse_block_src._parse_assign_stmt')
    @patch('._parse_block_src._parse_if_stmt')
    @patch('._parse_block_src._parse_while_stmt')
    @patch('._parse_block_src._parse_for_stmt')
    @patch('._parse_block_src._parse_def_stmt')
    @patch('._parse_block_src._parse_expr_stmt')
    def test_mixed_statement_types(
        self, mock_expr, mock_def, mock_for, mock_while, mock_if, mock_assign, mock_return
    ):
        """测试混合不同类型的语句"""
        tokens = [
            self._create_token("LET", "let", 1, 1),
            self._create_token("IF", "if", 2, 1),
            self._create_token("WHILE", "while", 3, 1),
            self._create_token("FOR", "for", 4, 1),
            self._create_token("DEF", "def", 5, 1),
            self._create_token("RETURN", "return", 6, 1),
            self._create_token("IDENTIFIER", "x", 7, 1),
            self._create_token("SEMICOLON", ";", 8, 1)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)

        mock_assign.return_value = self._create_ast_node("ASSIGN", 1, 1)
        mock_if.return_value = self._create_ast_node("IF", 2, 1)
        mock_while.return_value = self._create_ast_node("WHILE", 3, 1)
        mock_for.return_value = self._create_ast_node("FOR", 4, 1)
        mock_def.return_value = self._create_ast_node("DEF", 5, 1)
        mock_return.return_value = self._create_ast_node("RETURN", 6, 1)
        mock_expr.return_value = self._create_ast_node("EXPR", 7, 1)

        result = _parse_block(parser_state)

        self.assertEqual(len(result["children"]), 7)
        expected_types = ["ASSIGN", "IF", "WHILE", "FOR", "DEF", "RETURN", "EXPR"]
        for i, expected_type in enumerate(expected_types):
            self.assertEqual(result["children"][i]["type"], expected_type)


if __name__ == "__main__":
    unittest.main()

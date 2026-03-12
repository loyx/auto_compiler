import unittest
from unittest.mock import patch
from ._parse_if_stmt_src import _parse_if_stmt


class TestParseIfStmt(unittest.TestCase):
    """测试 _parse_if_stmt 函数"""

    def test_if_without_else(self):
        """测试只有 then_block 的 IF 语句"""
        parser_state = {
            "tokens": [
                {"type": "IF", "value": "if", "line": 1, "column": 1},
                {"type": "LPAREN", "value": "(", "line": 1, "column": 4},
                {"type": "RPAREN", "value": ")", "line": 1, "column": 10},
                {"type": "LBRACE", "value": "{", "line": 1, "column": 12},
                {"type": "RBRACE", "value": "}", "line": 1, "column": 15},
            ],
            "filename": "test.txt",
            "pos": 0
        }

        with patch("._consume_token_package._consume_token_src._consume_token") as mock_consume:
            with patch("._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
                with patch("._parse_block_package._parse_block_src._parse_block") as mock_parse_block:
                    mock_parse_expr.return_value = {"type": "EXPR", "value": "x > 0", "line": 1, "column": 5}
                    mock_parse_block.return_value = {"type": "BLOCK", "statements": [], "line": 1, "column": 12}

                    result = _parse_if_stmt(parser_state)

                    self.assertEqual(result["type"], "IF")
                    self.assertEqual(result["condition"], {"type": "EXPR", "value": "x > 0", "line": 1, "column": 5})
                    self.assertEqual(result["then_block"], {"type": "BLOCK", "statements": [], "line": 1, "column": 12})
                    self.assertIsNone(result["else_block"])
                    self.assertEqual(result["line"], 1)
                    self.assertEqual(result["column"], 1)
                    self.assertEqual(parser_state["pos"], 4)

    def test_if_with_else(self):
        """测试带有 else_block 的 IF 语句"""
        parser_state = {
            "tokens": [
                {"type": "IF", "value": "if", "line": 1, "column": 1},
                {"type": "LPAREN", "value": "(", "line": 1, "column": 4},
                {"type": "RPAREN", "value": ")", "line": 1, "column": 10},
                {"type": "LBRACE", "value": "{", "line": 1, "column": 12},
                {"type": "RBRACE", "value": "}", "line": 1, "column": 15},
                {"type": "ELSE", "value": "else", "line": 2, "column": 1},
                {"type": "LBRACE", "value": "{", "line": 2, "column": 6},
                {"type": "RBRACE", "value": "}", "line": 2, "column": 9},
            ],
            "filename": "test.txt",
            "pos": 0
        }

        with patch("._consume_token_package._consume_token_src._consume_token") as mock_consume:
            with patch("._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
                with patch("._parse_block_package._parse_block_src._parse_block") as mock_parse_block:
                    mock_parse_expr.return_value = {"type": "EXPR", "value": "x > 0", "line": 1, "column": 5}
                    mock_parse_block.side_effect = [
                        {"type": "BLOCK", "statements": [], "line": 1, "column": 12},
                        {"type": "BLOCK", "statements": [], "line": 2, "column": 6}
                    ]

                    result = _parse_if_stmt(parser_state)

                    self.assertEqual(result["type"], "IF")
                    self.assertEqual(result["condition"], {"type": "EXPR", "value": "x > 0", "line": 1, "column": 5})
                    self.assertEqual(result["then_block"], {"type": "BLOCK", "statements": [], "line": 1, "column": 12})
                    self.assertEqual(result["else_block"], {"type": "BLOCK", "statements": [], "line": 2, "column": 6})
                    self.assertEqual(result["line"], 1)
                    self.assertEqual(result["column"], 1)
                    self.assertEqual(parser_state["pos"], 7)

    def test_empty_token_list(self):
        """测试空 token 列表时抛出 SyntaxError"""
        parser_state = {
            "tokens": [],
            "filename": "test.txt",
            "pos": 0
        }

        with self.assertRaises(SyntaxError) as context:
            _parse_if_stmt(parser_state)

        self.assertIn("期望 IF 语句", str(context.exception))
        self.assertIn("已到达文件末尾", str(context.exception))

    def test_pos_at_end(self):
        """测试 pos 已到 token 列表末尾时抛出 SyntaxError"""
        parser_state = {
            "tokens": [
                {"type": "IF", "value": "if", "line": 1, "column": 1}
            ],
            "filename": "test.txt",
            "pos": 1
        }

        with self.assertRaises(SyntaxError) as context:
            _parse_if_stmt(parser_state)

        self.assertIn("期望 IF 语句", str(context.exception))
        self.assertIn("已到达文件末尾", str(context.exception))

    def test_else_token_consumed(self):
        """测试 ELSE token 被正确消费（pos 增加）"""
        parser_state = {
            "tokens": [
                {"type": "IF", "value": "if", "line": 1, "column": 1},
                {"type": "LPAREN", "value": "(", "line": 1, "column": 4},
                {"type": "RPAREN", "value": ")", "line": 1, "column": 10},
                {"type": "LBRACE", "value": "{", "line": 1, "column": 12},
                {"type": "RBRACE", "value": "}", "line": 1, "column": 15},
                {"type": "ELSE", "value": "else", "line": 2, "column": 1},
                {"type": "LBRACE", "value": "{", "line": 2, "column": 6},
                {"type": "RBRACE", "value": "}", "line": 2, "column": 9},
            ],
            "filename": "test.txt",
            "pos": 0
        }

        with patch("._consume_token_package._consume_token_src._consume_token"):
            with patch("._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
                with patch("._parse_block_package._parse_block_src._parse_block") as mock_parse_block:
                    mock_parse_expr.return_value = {"type": "EXPR", "value": "x > 0", "line": 1, "column": 5}
                    mock_parse_block.side_effect = [
                        {"type": "BLOCK", "statements": [], "line": 1, "column": 12},
                        {"type": "BLOCK", "statements": [], "line": 2, "column": 6}
                    ]

                    _parse_if_stmt(parser_state)

                    self.assertEqual(parser_state["pos"], 7)

    def test_no_else_when_next_token_not_else(self):
        """测试下一个 token 不是 ELSE 时 else_block 为 None"""
        parser_state = {
            "tokens": [
                {"type": "IF", "value": "if", "line": 1, "column": 1},
                {"type": "LPAREN", "value": "(", "line": 1, "column": 4},
                {"type": "RPAREN", "value": ")", "line": 1, "column": 10},
                {"type": "LBRACE", "value": "{", "line": 1, "column": 12},
                {"type": "RBRACE", "value": "}", "line": 1, "column": 15},
                {"type": "SEMICOLON", "value": ";", "line": 2, "column": 1},
            ],
            "filename": "test.txt",
            "pos": 0
        }

        with patch("._consume_token_package._consume_token_src._consume_token"):
            with patch("._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
                with patch("._parse_block_package._parse_block_src._parse_block") as mock_parse_block:
                    mock_parse_expr.return_value = {"type": "EXPR", "value": "x > 0", "line": 1, "column": 5}
                    mock_parse_block.return_value = {"type": "BLOCK", "statements": [], "line": 1, "column": 12}

                    result = _parse_if_stmt(parser_state)

                    self.assertIsNone(result["else_block"])
                    self.assertEqual(parser_state["pos"], 4)

    def test_nested_if(self):
        """测试嵌套 IF 语句"""
        parser_state = {
            "tokens": [
                {"type": "IF", "value": "if", "line": 1, "column": 1},
                {"type": "LPAREN", "value": "(", "line": 1, "column": 4},
                {"type": "RPAREN", "value": ")", "line": 1, "column": 10},
                {"type": "LBRACE", "value": "{", "line": 1, "column": 12},
                {"type": "IF", "value": "if", "line": 2, "column": 2},
                {"type": "LPAREN", "value": "(", "line": 2, "column": 5},
                {"type": "RPAREN", "value": ")", "line": 2, "column": 11},
                {"type": "LBRACE", "value": "{", "line": 2, "column": 13},
                {"type": "RBRACE", "value": "}", "line": 2, "column": 16},
                {"type": "RBRACE", "value": "}", "line": 3, "column": 1},
            ],
            "filename": "test.txt",
            "pos": 0
        }

        with patch("._consume_token_package._consume_token_src._consume_token"):
            with patch("._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
                with patch("._parse_block_package._parse_block_src._parse_block") as mock_parse_block:
                    mock_parse_expr.return_value = {"type": "EXPR", "value": "x > 0", "line": 1, "column": 5}
                    inner_if = {
                        "type": "IF",
                        "condition": {"type": "EXPR", "value": "y > 0", "line": 2, "column": 6},
                        "then_block": {"type": "BLOCK", "statements": [], "line": 2, "column": 13},
                        "else_block": None,
                        "line": 2,
                        "column": 2
                    }
                    mock_parse_block.return_value = {"type": "BLOCK", "statements": [inner_if], "line": 1, "column": 12}

                    result = _parse_if_stmt(parser_state)

                    self.assertEqual(result["type"], "IF")
                    self.assertEqual(len(result["then_block"]["statements"]), 1)
                    self.assertEqual(result["then_block"]["statements"][0]["type"], "IF")

    def test_line_column_preserved(self):
        """测试 IF token 的行号和列号被正确保存"""
        parser_state = {
            "tokens": [
                {"type": "IF", "value": "if", "line": 10, "column": 25},
                {"type": "LPAREN", "value": "(", "line": 10, "column": 28},
                {"type": "RPAREN", "value": ")", "line": 10, "column": 34},
                {"type": "LBRACE", "value": "{", "line": 10, "column": 36},
                {"type": "RBRACE", "value": "}", "line": 10, "column": 39},
            ],
            "filename": "test.txt",
            "pos": 0
        }

        with patch("._consume_token_package._consume_token_src._consume_token"):
            with patch("._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
                with patch("._parse_block_package._parse_block_src._parse_block") as mock_parse_block:
                    mock_parse_expr.return_value = {"type": "EXPR", "value": "x > 0", "line": 10, "column": 29}
                    mock_parse_block.return_value = {"type": "BLOCK", "statements": [], "line": 10, "column": 36}

                    result = _parse_if_stmt(parser_state)

                    self.assertEqual(result["line"], 10)
                    self.assertEqual(result["column"], 25)

    def test_ast_structure_complete(self):
        """测试返回的 AST 结构包含所有必需字段"""
        parser_state = {
            "tokens": [
                {"type": "IF", "value": "if", "line": 1, "column": 1},
                {"type": "LPAREN", "value": "(", "line": 1, "column": 4},
                {"type": "RPAREN", "value": ")", "line": 1, "column": 10},
                {"type": "LBRACE", "value": "{", "line": 1, "column": 12},
                {"type": "RBRACE", "value": "}", "line": 1, "column": 15},
            ],
            "filename": "test.txt",
            "pos": 0
        }

        with patch("._consume_token_package._consume_token_src._consume_token"):
            with patch("._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
                with patch("._parse_block_package._parse_block_src._parse_block") as mock_parse_block:
                    mock_parse_expr.return_value = {"type": "EXPR", "value": "x > 0", "line": 1, "column": 5}
                    mock_parse_block.return_value = {"type": "BLOCK", "statements": [], "line": 1, "column": 12}

                    result = _parse_if_stmt(parser_state)

                    self.assertIn("type", result)
                    self.assertIn("condition", result)
                    self.assertIn("then_block", result)
                    self.assertIn("else_block", result)
                    self.assertIn("line", result)
                    self.assertIn("column", result)
                    self.assertEqual(result["type"], "IF")


if __name__ == "__main__":
    unittest.main()

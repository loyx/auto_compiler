# === std / third-party imports ===
import unittest
from unittest.mock import patch
from typing import Dict, Any

# === sub function imports ===
from ._parse_tuple_literal_src import _parse_tuple_literal


# === Type aliases for clarity ===
ParserState = Dict[str, Any]
AST = Dict[str, Any]
Token = Dict[str, Any]


class TestParseTupleLiteral(unittest.TestCase):
    """单元测试：_parse_tuple_literal 函数"""

    def test_empty_tuple(self):
        """测试空元组 () 的解析"""
        tokens = [
            {"type": "LEFT_PAREN", "value": "(", "line": 1, "column": 1},
            {"type": "RIGHT_PAREN", "value": ")", "line": 1, "column": 2},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "filename": "test.py",
            "pos": 0,
        }

        result = _parse_tuple_literal(parser_state)

        self.assertEqual(result["type"], "TUPLE_LITERAL")
        self.assertEqual(result["children"], [])
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 2)

    def test_single_element_tuple_with_trailing_comma(self):
        """测试单元素元组 (expr,) 的解析"""
        tokens = [
            {"type": "LEFT_PAREN", "value": "(", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 2},
            {"type": "COMMA", "value": ",", "line": 1, "column": 3},
            {"type": "RIGHT_PAREN", "value": ")", "line": 1, "column": 4},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "filename": "test.py",
            "pos": 0,
        }

        mock_ast: AST = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 2}

        with patch(
            "._parse_tuple_literal_src._parse_expression",
            return_value=mock_ast,
        ) as mock_parse_expr:
            result = _parse_tuple_literal(parser_state)

        self.assertEqual(result["type"], "TUPLE_LITERAL")
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0], mock_ast)
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 4)
        mock_parse_expr.assert_called_once()

    def test_multi_element_tuple(self):
        """测试多元素元组 (expr1, expr2, expr3) 的解析"""
        tokens = [
            {"type": "LEFT_PAREN", "value": "(", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 2},
            {"type": "COMMA", "value": ",", "line": 1, "column": 3},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
            {"type": "COMMA", "value": ",", "line": 1, "column": 6},
            {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 8},
            {"type": "RIGHT_PAREN", "value": ")", "line": 1, "column": 9},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "filename": "test.py",
            "pos": 0,
        }

        mock_ast_a: AST = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 2}
        mock_ast_b: AST = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
        mock_ast_c: AST = {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 8}

        with patch(
            "._parse_tuple_literal_src._parse_expression",
            side_effect=[mock_ast_a, mock_ast_b, mock_ast_c],
        ) as mock_parse_expr:
            result = _parse_tuple_literal(parser_state)

        self.assertEqual(result["type"], "TUPLE_LITERAL")
        self.assertEqual(len(result["children"]), 3)
        self.assertEqual(result["children"][0], mock_ast_a)
        self.assertEqual(result["children"][1], mock_ast_b)
        self.assertEqual(result["children"][2], mock_ast_c)
        self.assertEqual(parser_state["pos"], 7)
        self.assertEqual(mock_parse_expr.call_count, 3)

    def test_tuple_with_trailing_comma_multi_element(self):
        """测试带尾随逗号的多元素元组 (expr1, expr2,) 的解析"""
        tokens = [
            {"type": "LEFT_PAREN", "value": "(", "line": 2, "column": 5},
            {"type": "NUMBER", "value": "1", "line": 2, "column": 6},
            {"type": "COMMA", "value": ",", "line": 2, "column": 7},
            {"type": "NUMBER", "value": "2", "line": 2, "column": 9},
            {"type": "COMMA", "value": ",", "line": 2, "column": 10},
            {"type": "RIGHT_PAREN", "value": ")", "line": 2, "column": 11},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "filename": "test.py",
            "pos": 0,
        }

        mock_ast_1: AST = {"type": "NUMBER", "value": "1", "line": 2, "column": 6}
        mock_ast_2: AST = {"type": "NUMBER", "value": "2", "line": 2, "column": 9}

        with patch(
            "._parse_tuple_literal_src._parse_expression",
            side_effect=[mock_ast_1, mock_ast_2],
        ) as mock_parse_expr:
            result = _parse_tuple_literal(parser_state)

        self.assertEqual(result["type"], "TUPLE_LITERAL")
        self.assertEqual(len(result["children"]), 2)
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 5)
        self.assertEqual(parser_state["pos"], 6)
        self.assertEqual(mock_parse_expr.call_count, 2)

    def test_missing_left_paren_raises_syntax_error(self):
        """测试缺少 LEFT_PAREN 时抛出 SyntaxError"""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            {"type": "RIGHT_PAREN", "value": ")", "line": 1, "column": 2},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "filename": "test.py",
            "pos": 0,
        }

        with self.assertRaises(SyntaxError) as context:
            _parse_tuple_literal(parser_state)

        self.assertIn("Expected LEFT_PAREN", str(context.exception))
        self.assertIn("test.py", str(context.exception))

    def test_missing_right_paren_raises_syntax_error(self):
        """测试缺少 RIGHT_PAREN 时抛出 SyntaxError"""
        tokens = [
            {"type": "LEFT_PAREN", "value": "(", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 2},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "filename": "test.py",
            "pos": 0,
        }

        mock_ast: AST = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 2}

        with patch(
            "._parse_tuple_literal_src._parse_expression",
            return_value=mock_ast,
        ):
            with self.assertRaises(SyntaxError) as context:
                _parse_tuple_literal(parser_state)

        self.assertIn("Expected RIGHT_PAREN", str(context.exception))
        self.assertIn("test.py", str(context.exception))

    def test_unexpected_eof_at_start_raises_syntax_error(self):
        """测试在开始时遇到文件结尾抛出 SyntaxError"""
        tokens: list = []
        parser_state: ParserState = {
            "tokens": tokens,
            "filename": "test.py",
            "pos": 0,
        }

        with self.assertRaises(SyntaxError) as context:
            _parse_tuple_literal(parser_state)

        self.assertIn("Unexpected end of file", str(context.exception))
        self.assertIn("test.py", str(context.exception))

    def test_unexpected_eof_while_parsing_raises_syntax_error(self):
        """测试在解析过程中遇到文件结尾抛出 SyntaxError"""
        tokens = [
            {"type": "LEFT_PAREN", "value": "(", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 2},
            {"type": "COMMA", "value": ",", "line": 1, "column": 3},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "filename": "test.py",
            "pos": 0,
        }

        mock_ast: AST = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 2}

        with patch(
            "._parse_tuple_literal_src._parse_expression",
            return_value=mock_ast,
        ):
            with self.assertRaises(SyntaxError) as context:
                _parse_tuple_literal(parser_state)

        self.assertIn("Unexpected end of file", str(context.exception))

    def test_default_filename_when_missing(self):
        """测试当 filename 缺失时使用默认值 'unknown'"""
        tokens = [
            {"type": "LEFT_PAREN", "value": "(", "line": 1, "column": 1},
            {"type": "RIGHT_PAREN", "value": ")", "line": 1, "column": 2},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
        }

        result = _parse_tuple_literal(parser_state)

        self.assertEqual(result["type"], "TUPLE_LITERAL")
        self.assertEqual(parser_state["pos"], 2)

    def test_nested_tuple_structure(self):
        """测试嵌套元组结构的解析"""
        tokens = [
            {"type": "LEFT_PAREN", "value": "(", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 2},
            {"type": "COMMA", "value": ",", "line": 1, "column": 3},
            {"type": "IDENTIFIER", "value": "y", "line": 1, "column": 5},
            {"type": "RIGHT_PAREN", "value": ")", "line": 1, "column": 6},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "filename": "test.py",
            "pos": 0,
        }

        # 模拟 _parse_expression 返回一个嵌套元组 AST
        inner_tuple_ast: AST = {
            "type": "TUPLE_LITERAL",
            "children": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 2},
                {"type": "IDENTIFIER", "value": "y", "line": 1, "column": 5},
            ],
            "line": 1,
            "column": 2,
        }

        with patch(
            "._parse_tuple_literal_src._parse_expression",
            return_value=inner_tuple_ast,
        ) as mock_parse_expr:
            result = _parse_tuple_literal(parser_state)

        self.assertEqual(result["type"], "TUPLE_LITERAL")
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0]["type"], "TUPLE_LITERAL")
        self.assertEqual(len(result["children"][0]["children"]), 2)
        mock_parse_expr.assert_called_once()

    def test_pos_advancement_correct(self):
        """测试 pos 正确推进到 RIGHT_PAREN 之后"""
        tokens = [
            {"type": "LEFT_PAREN", "value": "(", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 2},
            {"type": "COMMA", "value": ",", "line": 1, "column": 3},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
            {"type": "RIGHT_PAREN", "value": ")", "line": 1, "column": 6},
            {"type": "SEMICOLON", "value": ";", "line": 1, "column": 7},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "filename": "test.py",
            "pos": 0,
        }

        mock_ast_a: AST = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 2}
        mock_ast_b: AST = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}

        with patch(
            "._parse_tuple_literal_src._parse_expression",
            side_effect=[mock_ast_a, mock_ast_b],
        ):
            result = _parse_tuple_literal(parser_state)

        # pos 应该指向 SEMICOLON (index 5)
        self.assertEqual(parser_state["pos"], 5)
        self.assertEqual(tokens[parser_state["pos"]]["type"], "SEMICOLON")


if __name__ == "__main__":
    unittest.main()

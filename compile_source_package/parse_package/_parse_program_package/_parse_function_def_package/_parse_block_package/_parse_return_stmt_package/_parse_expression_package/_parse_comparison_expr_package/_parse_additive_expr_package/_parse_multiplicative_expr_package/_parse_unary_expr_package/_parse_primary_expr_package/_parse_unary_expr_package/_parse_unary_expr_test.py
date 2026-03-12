# -*- coding: utf-8 -*-
"""单元测试文件：_parse_unary_expr"""

import unittest
from unittest.mock import patch
from typing import Any, Dict

from ._parse_unary_expr_src import _parse_unary_expr, UNARY_OPERATORS


ParserState = Dict[str, Any]
AST = Dict[str, Any]


class TestParseUnaryExpr(unittest.TestCase):
    """_parse_unary_expr 函数的单元测试类"""

    def setUp(self) -> None:
        """每个测试前的准备工作"""
        pass

    def tearDown(self) -> None:
        """每个测试后的清理工作"""
        pass

    def test_unary_minus_operator(self) -> None:
        """测试一元减号运算符 -x"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "OPERATOR", "value": "-", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 2},
            ],
            "pos": 0,
            "filename": "test.py",
        }

        with patch(
            "._parse_unary_expr_package._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr"
        ) as mock_primary:
            mock_primary.return_value = {
                "type": "IDENTIFIER",
                "children": [],
                "value": "x",
                "line": 1,
                "column": 2,
            }

            result = _parse_unary_expr(parser_state)

            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "-")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(result["children"][0]["type"], "IDENTIFIER")
            self.assertEqual(parser_state["pos"], 1)
            self.assertNotIn("error", parser_state)

    def test_unary_plus_operator(self) -> None:
        """测试一元加号运算符 +x"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "OPERATOR", "value": "+", "line": 1, "column": 1},
                {"type": "NUMBER", "value": "42", "line": 1, "column": 2},
            ],
            "pos": 0,
            "filename": "test.py",
        }

        with patch(
            "._parse_unary_expr_package._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr"
        ) as mock_primary:
            mock_primary.return_value = {
                "type": "LITERAL",
                "children": [],
                "value": 42,
                "line": 1,
                "column": 2,
            }

            result = _parse_unary_expr(parser_state)

            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "+")
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(parser_state["pos"], 1)

    def test_unary_not_operator(self) -> None:
        """测试逻辑非运算符 !x"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "OPERATOR", "value": "!", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "flag", "line": 1, "column": 2},
            ],
            "pos": 0,
            "filename": "test.py",
        }

        with patch(
            "._parse_unary_expr_package._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr"
        ) as mock_primary:
            mock_primary.return_value = {
                "type": "IDENTIFIER",
                "children": [],
                "value": "flag",
                "line": 1,
                "column": 2,
            }

            result = _parse_unary_expr(parser_state)

            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "!")
            self.assertEqual(len(result["children"]), 1)

    def test_unary_bitwise_not_operator(self) -> None:
        """测试按位取反运算符 ~x"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "OPERATOR", "value": "~", "line": 1, "column": 1},
                {"type": "NUMBER", "value": "5", "line": 1, "column": 2},
            ],
            "pos": 0,
            "filename": "test.py",
        }

        with patch(
            "._parse_unary_expr_package._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr"
        ) as mock_primary:
            mock_primary.return_value = {
                "type": "LITERAL",
                "children": [],
                "value": 5,
                "line": 1,
                "column": 2,
            }

            result = _parse_unary_expr(parser_state)

            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "~")

    def test_nested_unary_operators(self) -> None:
        """测试嵌套一元运算符 --x"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "OPERATOR", "value": "-", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "-", "line": 1, "column": 2},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 3},
            ],
            "pos": 0,
            "filename": "test.py",
        }

        with patch(
            "._parse_unary_expr_package._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr"
        ) as mock_primary:
            mock_primary.return_value = {
                "type": "IDENTIFIER",
                "children": [],
                "value": "x",
                "line": 1,
                "column": 3,
            }

            result = _parse_unary_expr(parser_state)

            # 外层 UNARY_OP
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "-")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            self.assertEqual(len(result["children"]), 1)

            # 内层 UNARY_OP
            inner_node = result["children"][0]
            self.assertEqual(inner_node["type"], "UNARY_OP")
            self.assertEqual(inner_node["value"], "-")
            self.assertEqual(inner_node["line"], 1)
            self.assertEqual(inner_node["column"], 2)
            self.assertEqual(len(inner_node["children"]), 1)

            # 最内层 IDENTIFIER
            self.assertEqual(inner_node["children"][0]["type"], "IDENTIFIER")
            self.assertEqual(parser_state["pos"], 2)

    def test_mixed_unary_operators(self) -> None:
        """测试混合一元运算符 !+x"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "OPERATOR", "value": "!", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "+", "line": 1, "column": 2},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 3},
            ],
            "pos": 0,
            "filename": "test.py",
        }

        with patch(
            "._parse_unary_expr_package._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr"
        ) as mock_primary:
            mock_primary.return_value = {
                "type": "IDENTIFIER",
                "children": [],
                "value": "x",
                "line": 1,
                "column": 3,
            }

            result = _parse_unary_expr(parser_state)

            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "!")
            self.assertEqual(result["children"][0]["type"], "UNARY_OP")
            self.assertEqual(result["children"][0]["value"], "+")
            self.assertEqual(parser_state["pos"], 2)

    def test_delegates_to_primary_expr_for_non_unary_token(self) -> None:
        """测试非一元运算符 token 时委托给 _parse_primary_expr"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            ],
            "pos": 0,
            "filename": "test.py",
        }

        with patch(
            "._parse_unary_expr_package._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr"
        ) as mock_primary:
            expected_result: AST = {
                "type": "IDENTIFIER",
                "children": [],
                "value": "x",
                "line": 1,
                "column": 1,
            }
            mock_primary.return_value = expected_result

            result = _parse_unary_expr(parser_state)

            self.assertEqual(result, expected_result)
            self.assertEqual(parser_state["pos"], 0)  # pos 不应改变
            mock_primary.assert_called_once_with(parser_state)

    def test_delegates_for_number_literal(self) -> None:
        """测试数字字面量时委托给 _parse_primary_expr"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "NUMBER", "value": "42", "line": 1, "column": 1},
            ],
            "pos": 0,
            "filename": "test.py",
        }

        with patch(
            "._parse_unary_expr_package._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr"
        ) as mock_primary:
            mock_primary.return_value = {
                "type": "LITERAL",
                "children": [],
                "value": 42,
                "line": 1,
                "column": 1,
            }

            result = _parse_unary_expr(parser_state)

            self.assertEqual(result["type"], "LITERAL")
            mock_primary.assert_called_once()

    def test_delegates_for_string_literal(self) -> None:
        """测试字符串字面量时委托给 _parse_primary_expr"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "STRING", "value": '"hello"', "line": 1, "column": 1},
            ],
            "pos": 0,
            "filename": "test.py",
        }

        with patch(
            "._parse_unary_expr_package._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr"
        ) as mock_primary:
            mock_primary.return_value = {
                "type": "LITERAL",
                "children": [],
                "value": "hello",
                "line": 1,
                "column": 1,
            }

            result = _parse_unary_expr(parser_state)

            self.assertEqual(result["type"], "LITERAL")

    def test_end_of_input_error(self) -> None:
        """测试 tokens 末尾时的错误处理"""
        parser_state: ParserState = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py",
        }

        result = _parse_unary_expr(parser_state)

        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], None)
        self.assertEqual(result["line"], -1)
        self.assertEqual(result["column"], -1)
        self.assertEqual(len(result["children"]), 0)
        self.assertIn("error", parser_state)
        self.assertIn("Unexpected end of input", parser_state["error"])
        self.assertEqual(parser_state["pos"], 0)  # pos 不应改变

    def test_end_of_input_after_operator(self) -> None:
        """测试一元运算符后无操作数的错误"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "OPERATOR", "value": "-", "line": 1, "column": 1},
            ],
            "pos": 0,
            "filename": "test.py",
        }

        with patch(
            "._parse_unary_expr_package._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr"
        ) as mock_primary:
            mock_primary.return_value = {
                "type": "ERROR",
                "children": [],
                "value": None,
                "line": -1,
                "column": -1,
            }
            parser_state["error"] = "Unexpected end of input while parsing unary expression"

            result = _parse_unary_expr(parser_state)

            self.assertEqual(result["type"], "ERROR")
            self.assertIn("error", parser_state)

    def test_error_propagation_from_recursive_call(self) -> None:
        """测试递归调用中的错误传播"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "OPERATOR", "value": "-", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 2},
            ],
            "pos": 0,
            "filename": "test.py",
        }

        with patch(
            "._parse_unary_expr_package._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr"
        ) as mock_primary:
            error_result: AST = {
                "type": "ERROR",
                "children": [],
                "value": None,
                "line": -1,
                "column": -1,
            }
            mock_primary.return_value = error_result
            parser_state["error"] = "Some parsing error"

            result = _parse_unary_expr(parser_state)

            self.assertEqual(result["type"], "ERROR")
            self.assertEqual(parser_state["pos"], 1)  # 运算符已被消费

    def test_unknown_operator_delegates_to_primary(self) -> None:
        """测试未知运算符时委托给 _parse_primary_expr"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "OPERATOR", "value": "*", "line": 1, "column": 1},
            ],
            "pos": 0,
            "filename": "test.py",
        }

        with patch(
            "._parse_unary_expr_package._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr"
        ) as mock_primary:
            mock_primary.return_value = {
                "type": "ERROR",
                "children": [],
                "value": None,
                "line": -1,
                "column": -1,
            }

            result = _parse_unary_expr(parser_state)

            mock_primary.assert_called_once()
            self.assertEqual(parser_state["pos"], 0)  # pos 不应改变

    def test_position_advances_correctly(self) -> None:
        """测试位置正确前进"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "OPERATOR", "value": "-", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 2},
                {"type": "OPERATOR", "value": "+", "line": 1, "column": 3},
            ],
            "pos": 0,
            "filename": "test.py",
        }

        with patch(
            "._parse_unary_expr_package._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr"
        ) as mock_primary:
            mock_primary.return_value = {
                "type": "IDENTIFIER",
                "children": [],
                "value": "x",
                "line": 1,
                "column": 2,
            }

            result = _parse_unary_expr(parser_state)

            self.assertEqual(parser_state["pos"], 1)

    def test_preserves_line_column_info(self) -> None:
        """测试保留行号和列号信息"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "OPERATOR", "value": "!", "line": 10, "column": 25},
                {"type": "IDENTIFIER", "value": "x", "line": 10, "column": 26},
            ],
            "pos": 0,
            "filename": "test.py",
        }

        with patch(
            "._parse_unary_expr_package._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr"
        ) as mock_primary:
            mock_primary.return_value = {
                "type": "IDENTIFIER",
                "children": [],
                "value": "x",
                "line": 10,
                "column": 26,
            }

            result = _parse_unary_expr(parser_state)

            self.assertEqual(result["line"], 10)
            self.assertEqual(result["column"], 25)

    def test_all_unary_operators_in_set(self) -> None:
        """测试 UNARY_OPERATORS 集合包含所有预期运算符"""
        self.assertIn("-", UNARY_OPERATORS)
        self.assertIn("+", UNARY_OPERATORS)
        self.assertIn("!", UNARY_OPERATORS)
        self.assertIn("~", UNARY_OPERATORS)
        self.assertEqual(len(UNARY_OPERATORS), 4)


if __name__ == "__main__":
    unittest.main()

"""单元测试：_parse_binop_tail 函数"""
import unittest
from unittest.mock import patch

from ._parse_binop_tail_src import _parse_binop_tail


class TestParseBinopTail(unittest.TestCase):
    """测试 _parse_binop_tail 函数的各种场景"""

    def setUp(self):
        """每个测试前的准备工作"""
        pass

    def tearDown(self):
        """每个测试后的清理工作"""
        pass

    def test_no_binary_operator(self):
        """测试：没有二元运算符时直接返回 left"""
        parser_state = {
            "tokens": [
                {"type": "SEMICOLON", "value": ";", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.c",
            "error": ""
        }
        left = {
            "type": "NUMBER_EXPR",
            "value": "42",
            "line": 1,
            "column": 1,
            "children": []
        }

        result = _parse_binop_tail(parser_state, left)

        self.assertEqual(result, left)
        self.assertEqual(parser_state["pos"], 0)
        self.assertEqual(parser_state["error"], "")

    def test_single_plus_operator(self):
        """测试：单个 PLUS 运算符"""
        parser_state = {
            "tokens": [
                {"type": "PLUS", "value": "+", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "5", "line": 1, "column": 5},
                {"type": "SEMICOLON", "value": ";", "line": 1, "column": 6}
            ],
            "pos": 0,
            "filename": "test.c",
            "error": ""
        }
        left = {
            "type": "NUMBER_EXPR",
            "value": "3",
            "line": 1,
            "column": 1,
            "children": []
        }

        with patch("._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr") as mock_parse:
            mock_parse.return_value = {
                "type": "NUMBER_EXPR",
                "value": "5",
                "line": 1,
                "column": 5,
                "children": []
            }

            result = _parse_binop_tail(parser_state, left)

        self.assertEqual(result["type"], "BINOP_EXPR")
        self.assertEqual(result["operator"], "+")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 3)
        self.assertEqual(len(result["children"]), 2)
        self.assertEqual(result["children"][0], left)
        self.assertEqual(result["children"][1]["type"], "NUMBER_EXPR")
        self.assertEqual(result["children"][1]["value"], "5")
        self.assertEqual(parser_state["pos"], 1)
        self.assertEqual(parser_state["error"], "")
        mock_parse.assert_called_once()

    def test_single_minus_operator(self):
        """测试：单个 MINUS 运算符"""
        parser_state = {
            "tokens": [
                {"type": "MINUS", "value": "-", "line": 2, "column": 4},
                {"type": "NUMBER", "value": "10", "line": 2, "column": 6}
            ],
            "pos": 0,
            "filename": "test.c",
            "error": ""
        }
        left = {
            "type": "NUMBER_EXPR",
            "value": "20",
            "line": 2,
            "column": 1,
            "children": []
        }

        with patch("._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr") as mock_parse:
            mock_parse.return_value = {
                "type": "NUMBER_EXPR",
                "value": "10",
                "line": 2,
                "column": 6,
                "children": []
            }

            result = _parse_binop_tail(parser_state, left)

        self.assertEqual(result["type"], "BINOP_EXPR")
        self.assertEqual(result["operator"], "-")
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 4)

    def test_multiple_operators_left_associative(self):
        """测试：多个运算符，验证左结合性"""
        parser_state = {
            "tokens": [
                {"type": "PLUS", "value": "+", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 5},
                {"type": "MULTIPLY", "value": "*", "line": 1, "column": 7},
                {"type": "NUMBER", "value": "3", "line": 1, "column": 9},
                {"type": "SEMICOLON", "value": ";", "line": 1, "column": 10}
            ],
            "pos": 0,
            "filename": "test.c",
            "error": ""
        }
        left = {
            "type": "NUMBER_EXPR",
            "value": "1",
            "line": 1,
            "column": 1,
            "children": []
        }

        with patch("._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr") as mock_parse:
            mock_parse.side_effect = [
                {
                    "type": "NUMBER_EXPR",
                    "value": "2",
                    "line": 1,
                    "column": 5,
                    "children": []
                },
                {
                    "type": "NUMBER_EXPR",
                    "value": "3",
                    "line": 1,
                    "column": 9,
                    "children": []
                }
            ]

            result = _parse_binop_tail(parser_state, left)

        # 验证左结合：(1 + 2) * 3
        self.assertEqual(result["type"], "BINOP_EXPR")
        self.assertEqual(result["operator"], "*")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 7)
        self.assertEqual(len(result["children"]), 2)

        # 左子节点应该是 (1 + 2)
        left_child = result["children"][0]
        self.assertEqual(left_child["type"], "BINOP_EXPR")
        self.assertEqual(left_child["operator"], "+")
        self.assertEqual(left_child["children"][0]["value"], "1")
        self.assertEqual(left_child["children"][1]["value"], "2")

        # 右子节点应该是 3
        right_child = result["children"][1]
        self.assertEqual(right_child["type"], "NUMBER_EXPR")
        self.assertEqual(right_child["value"], "3")

        self.assertEqual(parser_state["pos"], 4)
        self.assertEqual(mock_parse.call_count, 2)

    def test_all_binary_operators(self):
        """测试：所有支持的二元运算符"""
        operators = [
            ("PLUS", "+"), ("MINUS", "-"), ("MULTIPLY", "*"), ("DIVIDE", "/"),
            ("MODULO", "%"), ("EQ", "=="), ("NEQ", "!="), ("LT", "<"),
            ("GT", ">"), ("LTE", "<="), ("GTE", ">="), ("AND", "and"), ("OR", "or")
        ]

        for op_type, op_symbol in operators:
            with self.subTest(operator=op_type):
                parser_state = {
                    "tokens": [
                        {"type": op_type, "value": op_symbol, "line": 1, "column": 2},
                        {"type": "NUMBER", "value": "1", "line": 1, "column": 4}
                    ],
                    "pos": 0,
                    "filename": "test.c",
                    "error": ""
                }
                left = {
                    "type": "NUMBER_EXPR",
                    "value": "0",
                    "line": 1,
                    "column": 1,
                    "children": []
                }

                with patch("._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr") as mock_parse:
                    mock_parse.return_value = {
                        "type": "NUMBER_EXPR",
                        "value": "1",
                        "line": 1,
                        "column": 4,
                        "children": []
                    }

                    result = _parse_binop_tail(parser_state, left)

                self.assertEqual(result["type"], "BINOP_EXPR")
                self.assertEqual(result["operator"], op_symbol)

    def test_parse_primary_expr_error(self):
        """测试：_parse_primary_expr 解析失败时返回 ERROR 节点"""
        parser_state = {
            "tokens": [
                {"type": "PLUS", "value": "+", "line": 1, "column": 3},
                {"type": "INVALID", "value": "?", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.c",
            "error": ""
        }
        left = {
            "type": "NUMBER_EXPR",
            "value": "5",
            "line": 1,
            "column": 1,
            "children": []
        }

        with patch("._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr") as mock_parse:
            def set_error(state):
                state["error"] = "Invalid expression"
                return {
                    "type": "ERROR",
                    "value": None,
                    "line": 1,
                    "column": 5,
                    "children": []
                }
            mock_parse.side_effect = set_error

            result = _parse_binop_tail(parser_state, left)

        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], None)
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 3)
        self.assertEqual(parser_state["error"], "Invalid expression")

    def test_pos_at_end_of_tokens(self):
        """测试：pos 已经在 tokens 末尾"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1}
            ],
            "pos": 1,
            "filename": "test.c",
            "error": ""
        }
        left = {
            "type": "NUMBER_EXPR",
            "value": "1",
            "line": 1,
            "column": 1,
            "children": []
        }

        result = _parse_binop_tail(parser_state, left)

        self.assertEqual(result, left)
        self.assertEqual(parser_state["pos"], 1)

    def test_empty_tokens(self):
        """测试：tokens 为空列表"""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.c",
            "error": ""
        }
        left = {
            "type": "IDENTIFIER_EXPR",
            "value": "x",
            "line": 1,
            "column": 1,
            "children": []
        }

        result = _parse_binop_tail(parser_state, left)

        self.assertEqual(result, left)
        self.assertEqual(parser_state["pos"], 0)

    def test_non_binary_operator_token(self):
        """测试：遇到非二元运算符的 token"""
        parser_state = {
            "tokens": [
                {"type": "LPAREN", "value": "(", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "5", "line": 1, "column": 4}
            ],
            "pos": 0,
            "filename": "test.c",
            "error": ""
        }
        left = {
            "type": "NUMBER_EXPR",
            "value": "3",
            "line": 1,
            "column": 1,
            "children": []
        }

        result = _parse_binop_tail(parser_state, left)

        self.assertEqual(result, left)
        self.assertEqual(parser_state["pos"], 0)

    def test_operator_with_complex_right_operand(self):
        """测试：运算符后跟复杂的右操作数"""
        parser_state = {
            "tokens": [
                {"type": "MULTIPLY", "value": "*", "line": 1, "column": 3},
                {"type": "LPAREN", "value": "(", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.c",
            "error": ""
        }
        left = {
            "type": "NUMBER_EXPR",
            "value": "2",
            "line": 1,
            "column": 1,
            "children": []
        }

        right_operand = {
            "type": "BINOP_EXPR",
            "operator": "+",
            "children": [
                {"type": "NUMBER_EXPR", "value": "3", "line": 1, "column": 6, "children": []},
                {"type": "NUMBER_EXPR", "value": "4", "line": 1, "column": 8, "children": []}
            ],
            "line": 1,
            "column": 5,
            "children": []
        }

        with patch("._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr") as mock_parse:
            mock_parse.return_value = right_operand

            result = _parse_binop_tail(parser_state, left)

        self.assertEqual(result["type"], "BINOP_EXPR")
        self.assertEqual(result["operator"], "*")
        self.assertEqual(result["children"][0], left)
        self.assertEqual(result["children"][1], right_operand)
        self.assertEqual(parser_state["pos"], 1)


if __name__ == "__main__":
    unittest.main()

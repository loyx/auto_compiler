# -*- coding: utf-8 -*-
"""单元测试：_parse_multiplicative 函数"""

import unittest
from unittest.mock import patch
from typing import Any, Dict

from ._parse_multiplicative_src import _parse_multiplicative, _get_current_token

Token = Dict[str, Any]
AST = Dict[str, Any]
ParserState = Dict[str, Any]


class TestParseMultiplicative(unittest.TestCase):
    """测试 _parse_multiplicative 函数"""

    def test_single_unary_no_operator(self):
        """测试：没有运算符，仅返回一元表达式"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "NUMBER", "value": "5", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        unary_result: AST = {
            "type": "NUMBER",
            "value": "5",
            "line": 1,
            "column": 1
        }
        
        with patch("._parse_multiplicative_src._parse_unary") as mock_unary:
            mock_unary.return_value = unary_result
            
            result = _parse_multiplicative(parser_state)
            
            self.assertEqual(result, unary_result)
            self.assertEqual(parser_state["pos"], 0)
            mock_unary.assert_called_once_with(parser_state)

    def test_multiplication_operator(self):
        """测试：乘法运算符 *"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "NUMBER", "value": "3", "line": 1, "column": 1},
                {"type": "STAR", "value": "*", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "4", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        left_unary: AST = {"type": "NUMBER", "value": "3", "line": 1, "column": 1}
        right_unary: AST = {"type": "NUMBER", "value": "4", "line": 1, "column": 5}
        
        with patch("._parse_multiplicative_src._parse_unary") as mock_unary:
            mock_unary.side_effect = [left_unary, right_unary]
            
            result = _parse_multiplicative(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["operator"], "*")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 3)
            self.assertEqual(len(result["children"]), 2)
            self.assertEqual(result["children"][0], left_unary)
            self.assertEqual(result["children"][1], right_unary)
            self.assertEqual(parser_state["pos"], 3)

    def test_division_operator(self):
        """测试：除法运算符 /"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "NUMBER", "value": "10", "line": 2, "column": 1},
                {"type": "SLASH", "value": "/", "line": 2, "column": 4},
                {"type": "NUMBER", "value": "2", "line": 2, "column": 6}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        left_unary: AST = {"type": "NUMBER", "value": "10", "line": 2, "column": 1}
        right_unary: AST = {"type": "NUMBER", "value": "2", "line": 2, "column": 6}
        
        with patch("._parse_multiplicative_src._parse_unary") as mock_unary:
            mock_unary.side_effect = [left_unary, right_unary]
            
            result = _parse_multiplicative(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["operator"], "/")
            self.assertEqual(result["line"], 2)
            self.assertEqual(result["column"], 4)

    def test_modulo_operator(self):
        """测试：取模运算符 %"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "NUMBER", "value": "7", "line": 1, "column": 1},
                {"type": "PERCENT", "value": "%", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "3", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        left_unary: AST = {"type": "NUMBER", "value": "7", "line": 1, "column": 1}
        right_unary: AST = {"type": "NUMBER", "value": "3", "line": 1, "column": 5}
        
        with patch("._parse_multiplicative_src._parse_unary") as mock_unary:
            mock_unary.side_effect = [left_unary, right_unary]
            
            result = _parse_multiplicative(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["operator"], "%")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 3)

    def test_left_associativity(self):
        """测试：左结合性 - 多个运算符"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "NUMBER", "value": "2", "line": 1, "column": 1},
                {"type": "STAR", "value": "*", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "3", "line": 1, "column": 5},
                {"type": "SLASH", "value": "/", "line": 1, "column": 7},
                {"type": "NUMBER", "value": "4", "line": 1, "column": 9}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        unary_2: AST = {"type": "NUMBER", "value": "2", "line": 1, "column": 1}
        unary_3: AST = {"type": "NUMBER", "value": "3", "line": 1, "column": 5}
        unary_4: AST = {"type": "NUMBER", "value": "4", "line": 1, "column": 9}
        
        with patch("._parse_multiplicative_src._parse_unary") as mock_unary:
            mock_unary.side_effect = [unary_2, unary_3, unary_4]
            
            result = _parse_multiplicative(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["operator"], "/")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 7)
            
            left_child = result["children"][0]
            self.assertEqual(left_child["type"], "BINARY_OP")
            self.assertEqual(left_child["operator"], "*")
            self.assertEqual(left_child["children"][0], unary_2)
            self.assertEqual(left_child["children"][1], unary_3)
            
            self.assertEqual(result["children"][1], unary_4)
            self.assertEqual(parser_state["pos"], 5)

    def test_error_from_first_unary(self):
        """测试：第一个 _parse_unary 返回错误"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "NUMBER", "value": "5", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.c",
            "error": "unary parse error"
        }
        
        error_result: AST = {"type": "ERROR", "value": "unary parse error"}
        
        with patch("._parse_multiplicative_src._parse_unary") as mock_unary:
            mock_unary.return_value = error_result
            
            result = _parse_multiplicative(parser_state)
            
            self.assertEqual(result, error_result)
            mock_unary.assert_called_once_with(parser_state)

    def test_error_from_second_unary(self):
        """测试：第二个 _parse_unary 返回错误"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "NUMBER", "value": "3", "line": 1, "column": 1},
                {"type": "STAR", "value": "*", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "4", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        left_unary: AST = {"type": "NUMBER", "value": "3", "line": 1, "column": 1}
        error_result: AST = {"type": "ERROR", "value": "second unary error"}
        
        with patch("._parse_multiplicative_src._parse_unary") as mock_unary:
            mock_unary.side_effect = [left_unary, error_result]
            
            result = _parse_multiplicative(parser_state)
            
            self.assertEqual(result, error_result)
            self.assertEqual(parser_state["pos"], 1)

    def test_empty_tokens(self):
        """测试：空 token 列表"""
        parser_state: ParserState = {
            "tokens": [],
            "pos": 0,
            "filename": "test.c"
        }
        
        empty_result: AST = {"type": "EMPTY", "value": None}
        
        with patch("._parse_multiplicative_src._parse_unary") as mock_unary:
            mock_unary.return_value = empty_result
            
            result = _parse_multiplicative(parser_state)
            
            self.assertEqual(result, empty_result)
            mock_unary.assert_called_once_with(parser_state)

    def test_operator_at_end_no_right_operand(self):
        """测试：运算符在末尾，没有右操作数"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "NUMBER", "value": "5", "line": 1, "column": 1},
                {"type": "STAR", "value": "*", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        left_unary: AST = {"type": "NUMBER", "value": "5", "line": 1, "column": 1}
        right_unary: AST = {"type": "EMPTY", "value": None}
        
        with patch("._parse_multiplicative_src._parse_unary") as mock_unary:
            mock_unary.side_effect = [left_unary, right_unary]
            
            result = _parse_multiplicative(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["operator"], "*")
            self.assertEqual(result["children"][0], left_unary)
            self.assertEqual(result["children"][1], right_unary)
            self.assertEqual(parser_state["pos"], 2)

    def test_mixed_operators(self):
        """测试：混合使用 *, /, % 运算符"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "NUMBER", "value": "12", "line": 1, "column": 1},
                {"type": "STAR", "value": "*", "line": 1, "column": 4},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 6},
                {"type": "PERCENT", "value": "%", "line": 1, "column": 8},
                {"type": "NUMBER", "value": "3", "line": 1, "column": 10},
                {"type": "SLASH", "value": "/", "line": 1, "column": 12},
                {"type": "NUMBER", "value": "4", "line": 1, "column": 14}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        unaries = [
            {"type": "NUMBER", "value": "12", "line": 1, "column": 1},
            {"type": "NUMBER", "value": "2", "line": 1, "column": 6},
            {"type": "NUMBER", "value": "3", "line": 1, "column": 10},
            {"type": "NUMBER", "value": "4", "line": 1, "column": 14}
        ]
        
        with patch("._parse_multiplicative_src._parse_unary") as mock_unary:
            mock_unary.side_effect = unaries
            
            result = _parse_multiplicative(parser_state)
            
            self.assertEqual(result["operator"], "/")
            self.assertEqual(result["column"], 12)
            
            left_part = result["children"][0]
            self.assertEqual(left_part["operator"], "%")
            
            leftmost = left_part["children"][0]
            self.assertEqual(leftmost["operator"], "*")
            
            self.assertEqual(parser_state["pos"], 7)


class TestGetCurrentToken(unittest.TestCase):
    """测试 _get_current_token 辅助函数"""

    def test_get_token_at_position(self):
        """测试：获取当前位置的 token"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "STAR", "value": "*", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 5}
            ],
            "pos": 1
        }
        
        result = _get_current_token(parser_state)
        
        self.assertEqual(result["type"], "STAR")
        self.assertEqual(result["value"], "*")

    def test_get_token_beyond_length(self):
        """测试：位置超出 token 列表长度"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1}
            ],
            "pos": 5
        }
        
        result = _get_current_token(parser_state)
        
        self.assertIsNone(result)

    def test_get_token_empty_list(self):
        """测试：空 token 列表"""
        parser_state: ParserState = {
            "tokens": [],
            "pos": 0
        }
        
        result = _get_current_token(parser_state)
        
        self.assertIsNone(result)

    def test_get_token_missing_pos(self):
        """测试：parser_state 缺少 pos 字段"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1}
            ]
        }
        
        result = _get_current_token(parser_state)
        
        self.assertEqual(result["type"], "NUMBER")

    def test_get_token_missing_tokens(self):
        """测试：parser_state 缺少 tokens 字段"""
        parser_state: ParserState = {
            "pos": 0
        }
        
        result = _get_current_token(parser_state)
        
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()

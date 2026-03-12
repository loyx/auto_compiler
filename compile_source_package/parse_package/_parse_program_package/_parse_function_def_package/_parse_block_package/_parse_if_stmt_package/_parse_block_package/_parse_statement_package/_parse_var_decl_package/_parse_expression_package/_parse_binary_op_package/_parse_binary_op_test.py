# -*- coding: utf-8 -*-
"""单元测试：_parse_binary_op 函数"""

import unittest
from unittest.mock import patch

from ._parse_binary_op_src import _parse_binary_op


class TestParseBinaryOp(unittest.TestCase):
    """_parse_binary_op 函数测试用例"""

    def test_no_operator_token(self):
        """测试：没有运算符 token 时直接返回左操作数"""
        parser_state = {
            "tokens": [{"type": "IDENTIFIER", "value": "b", "line": 1, "column": 3}],
            "pos": 0,
            "filename": "test.c"
        }
        left = {"type": "identifier", "value": "a", "line": 1, "column": 0}
        
        result = _parse_binary_op(parser_state, left, 0)
        
        self.assertEqual(result, left)
        self.assertEqual(parser_state["pos"], 0)

    def test_single_addition(self):
        """测试：解析单个加法运算 a + b"""
        tokens = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 0},
            {"type": "OPERATOR", "value": "+", "line": 1, "column": 2},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 4}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 1,
            "filename": "test.c"
        }
        left = {"type": "identifier", "value": "a", "line": 1, "column": 0}
        right = {"type": "identifier", "value": "b", "line": 1, "column": 4}
        
        with patch("._parse_primary_package._parse_primary_src._parse_primary") as mock_parse_primary:
            mock_parse_primary.return_value = right
            
            result = _parse_binary_op(parser_state, left, 0)
        
        self.assertEqual(result["type"], "binary_op")
        self.assertEqual(result["value"], "+")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 2)
        self.assertEqual(len(result["children"]), 2)
        self.assertEqual(result["children"][0], left)
        self.assertEqual(result["children"][1], right)
        self.assertEqual(parser_state["pos"], 2)
        mock_parse_primary.assert_called_once()

    def test_single_subtraction(self):
        """测试：解析单个减法运算 a - b"""
        tokens = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 0},
            {"type": "OPERATOR", "value": "-", "line": 1, "column": 2},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 4}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 1,
            "filename": "test.c"
        }
        left = {"type": "identifier", "value": "a", "line": 1, "column": 0}
        right = {"type": "identifier", "value": "b", "line": 1, "column": 4}
        
        with patch("._parse_primary_package._parse_primary_src._parse_primary") as mock_parse_primary:
            mock_parse_primary.return_value = right
            
            result = _parse_binary_op(parser_state, left, 0)
        
        self.assertEqual(result["type"], "binary_op")
        self.assertEqual(result["value"], "-")
        self.assertEqual(result["children"][0], left)
        self.assertEqual(result["children"][1], right)

    def test_single_multiplication(self):
        """测试：解析单个乘法运算 a * b"""
        tokens = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 0},
            {"type": "OPERATOR", "value": "*", "line": 1, "column": 2},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 4}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 1,
            "filename": "test.c"
        }
        left = {"type": "identifier", "value": "a", "line": 1, "column": 0}
        right = {"type": "identifier", "value": "b", "line": 1, "column": 4}
        
        with patch("._parse_primary_package._parse_primary_src._parse_primary") as mock_parse_primary:
            mock_parse_primary.return_value = right
            
            result = _parse_binary_op(parser_state, left, 0)
        
        self.assertEqual(result["type"], "binary_op")
        self.assertEqual(result["value"], "*")

    def test_single_division(self):
        """测试：解析单个除法运算 a / b"""
        tokens = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 0},
            {"type": "OPERATOR", "value": "/", "line": 1, "column": 2},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 4}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 1,
            "filename": "test.c"
        }
        left = {"type": "identifier", "value": "a", "line": 1, "column": 0}
        right = {"type": "identifier", "value": "b", "line": 1, "column": 4}
        
        with patch("._parse_primary_package._parse_primary_src._parse_primary") as mock_parse_primary:
            mock_parse_primary.return_value = right
            
            result = _parse_binary_op(parser_state, left, 0)
        
        self.assertEqual(result["type"], "binary_op")
        self.assertEqual(result["value"], "/")

    def test_chained_same_precedence(self):
        """测试：解析链式同优先级运算 a + b + c"""
        tokens = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 0},
            {"type": "OPERATOR", "value": "+", "line": 1, "column": 2},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 4},
            {"type": "OPERATOR", "value": "+", "line": 1, "column": 6},
            {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 8}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 1,
            "filename": "test.c"
        }
        left = {"type": "identifier", "value": "a", "line": 1, "column": 0}
        right_b = {"type": "identifier", "value": "b", "line": 1, "column": 4}
        right_c = {"type": "identifier", "value": "c", "line": 1, "column": 8}
        
        with patch("._parse_primary_package._parse_primary_src._parse_primary") as mock_parse_primary:
            mock_parse_primary.side_effect = [right_b, right_c]
            
            result = _parse_binary_op(parser_state, left, 0)
        
        self.assertEqual(result["type"], "binary_op")
        self.assertEqual(result["value"], "+")
        self.assertEqual(result["column"], 6)
        self.assertEqual(len(result["children"]), 2)
        inner_op = result["children"][0]
        self.assertEqual(inner_op["type"], "binary_op")
        self.assertEqual(inner_op["value"], "+")
        self.assertEqual(inner_op["column"], 2)
        self.assertEqual(result["children"][1], right_c)

    def test_mixed_precedence_add_then_mul(self):
        """测试：混合优先级 a + b * c，乘法优先级更高"""
        tokens = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 0},
            {"type": "OPERATOR", "value": "+", "line": 1, "column": 2},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 4},
            {"type": "OPERATOR", "value": "*", "line": 1, "column": 6},
            {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 8}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 1,
            "filename": "test.c"
        }
        left = {"type": "identifier", "value": "a", "line": 1, "column": 0}
        right_b = {"type": "identifier", "value": "b", "line": 1, "column": 4}
        right_c = {"type": "identifier", "value": "c", "line": 1, "column": 8}
        
        with patch("._parse_primary_package._parse_primary_src._parse_primary") as mock_parse_primary:
            mock_parse_primary.side_effect = [right_b, right_c]
            
            result = _parse_binary_op(parser_state, left, 0)
        
        self.assertEqual(result["type"], "binary_op")
        self.assertEqual(result["value"], "+")
        self.assertEqual(result["column"], 2)
        right_side = result["children"][1]
        self.assertEqual(right_side["type"], "binary_op")
        self.assertEqual(right_side["value"], "*")
        self.assertEqual(right_side["column"], 6)

    def test_mixed_precedence_mul_then_add(self):
        """测试：混合优先级 a * b + c，乘法先结合"""
        tokens = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 0},
            {"type": "OPERATOR", "value": "*", "line": 1, "column": 2},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 4},
            {"type": "OPERATOR", "value": "+", "line": 1, "column": 6},
            {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 8}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 1,
            "filename": "test.c"
        }
        left = {"type": "identifier", "value": "a", "line": 1, "column": 0}
        right_b = {"type": "identifier", "value": "b", "line": 1, "column": 4}
        right_c = {"type": "identifier", "value": "c", "line": 1, "column": 8}
        
        with patch("._parse_primary_package._parse_primary_src._parse_primary") as mock_parse_primary:
            mock_parse_primary.side_effect = [right_b, right_c]
            
            result = _parse_binary_op(parser_state, left, 0)
        
        self.assertEqual(result["type"], "binary_op")
        self.assertEqual(result["value"], "+")
        self.assertEqual(result["column"], 6)
        left_side = result["children"][0]
        self.assertEqual(left_side["type"], "binary_op")
        self.assertEqual(left_side["value"], "*")
        self.assertEqual(left_side["column"], 2)

    def test_min_precedence_filter(self):
        """测试：min_precedence 参数过滤低优先级运算符"""
        tokens = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 0},
            {"type": "OPERATOR", "value": "+", "line": 1, "column": 2},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 4}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 1,
            "filename": "test.c"
        }
        left = {"type": "identifier", "value": "a", "line": 1, "column": 0}
        
        with patch("._parse_primary_package._parse_primary_src._parse_primary") as mock_parse_primary:
            result = _parse_binary_op(parser_state, left, 2)
        
        self.assertEqual(result, left)
        self.assertEqual(parser_state["pos"], 1)
        mock_parse_primary.assert_not_called()

    def test_end_of_tokens(self):
        """测试：pos 超出 tokens 长度时停止解析"""
        tokens = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 0}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 1,
            "filename": "test.c"
        }
        left = {"type": "identifier", "value": "a", "line": 1, "column": 0}
        
        result = _parse_binary_op(parser_state, left, 0)
        
        self.assertEqual(result, left)
        self.assertEqual(parser_state["pos"], 1)

    def test_non_operator_token(self):
        """测试：遇到非运算符 token 时停止解析"""
        tokens = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 0},
            {"type": "SEMICOLON", "value": ";", "line": 1, "column": 2}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 1,
            "filename": "test.c"
        }
        left = {"type": "identifier", "value": "a", "line": 1, "column": 0}
        
        result = _parse_binary_op(parser_state, left, 0)
        
        self.assertEqual(result, left)
        self.assertEqual(parser_state["pos"], 1)

    def test_complex_expression(self):
        """测试：复杂表达式 a + b * c - d / e"""
        tokens = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 0},
            {"type": "OPERATOR", "value": "+", "line": 1, "column": 2},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 4},
            {"type": "OPERATOR", "value": "*", "line": 1, "column": 6},
            {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 8},
            {"type": "OPERATOR", "value": "-", "line": 1, "column": 10},
            {"type": "IDENTIFIER", "value": "d", "line": 1, "column": 12},
            {"type": "OPERATOR", "value": "/", "line": 1, "column": 14},
            {"type": "IDENTIFIER", "value": "e", "line": 1, "column": 16}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 1,
            "filename": "test.c"
        }
        left = {"type": "identifier", "value": "a", "line": 1, "column": 0}
        
        identifiers = [
            {"type": "identifier", "value": "b", "line": 1, "column": 4},
            {"type": "identifier", "value": "c", "line": 1, "column": 8},
            {"type": "identifier", "value": "d", "line": 1, "column": 12},
            {"type": "identifier", "value": "e", "line": 1, "column": 16}
        ]
        
        with patch("._parse_primary_package._parse_primary_src._parse_primary") as mock_parse_primary:
            mock_parse_primary.side_effect = identifiers
            
            result = _parse_binary_op(parser_state, left, 0)
        
        self.assertEqual(result["type"], "binary_op")
        self.assertEqual(result["value"], "-")
        self.assertEqual(parser_state["pos"], 9)
        mock_parse_primary.assert_called()


if __name__ == "__main__":
    unittest.main()

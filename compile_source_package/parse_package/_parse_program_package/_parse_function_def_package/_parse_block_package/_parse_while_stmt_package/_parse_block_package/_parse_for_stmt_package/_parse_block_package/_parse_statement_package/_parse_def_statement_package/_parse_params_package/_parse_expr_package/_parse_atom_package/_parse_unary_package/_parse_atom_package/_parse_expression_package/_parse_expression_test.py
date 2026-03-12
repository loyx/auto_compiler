# -*- coding: utf-8 -*-
"""单元测试：_parse_expression 函数"""

import unittest
from unittest.mock import patch

# 相对导入被测模块
from ._parse_expression_src import _parse_expression, _current_token_type


class TestParseExpression(unittest.TestCase):
    """_parse_expression 函数的单元测试"""

    def test_parse_expression_delegates_to_parse_or(self):
        """测试 _parse_expression 委托给 _parse_or 处理"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "42", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.cc"
        }
        
        expected_ast = {
            "type": "NUMBER",
            "value": "42",
            "line": 1,
            "column": 1
        }
        
        with patch("._parse_or_package._parse_or_src._parse_or") as mock_parse_or:
            mock_parse_or.return_value = expected_ast
            
            result = _parse_expression(parser_state)
            
            mock_parse_or.assert_called_once_with(parser_state)
            self.assertEqual(result, expected_ast)

    def test_parse_expression_with_simple_number(self):
        """测试解析简单数字表达式"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "123", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.cc"
        }
        
        expected_ast = {
            "type": "NUMBER",
            "value": "123",
            "line": 1,
            "column": 1
        }
        
        with patch("._parse_or_package._parse_or_src._parse_or") as mock_parse_or:
            mock_parse_or.return_value = expected_ast
            
            result = _parse_expression(parser_state)
            
            self.assertEqual(result["type"], "NUMBER")
            self.assertEqual(result["value"], "123")

    def test_parse_expression_with_identifier(self):
        """测试解析标识符表达式"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.cc"
        }
        
        expected_ast = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 1
        }
        
        with patch("._parse_or_package._parse_or_src._parse_or") as mock_parse_or:
            mock_parse_or.return_value = expected_ast
            
            result = _parse_expression(parser_state)
            
            self.assertEqual(result["type"], "IDENTIFIER")
            self.assertEqual(result["value"], "x")

    def test_parse_expression_with_binary_operation(self):
        """测试解析二元运算表达式"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.cc"
        }
        
        expected_ast = {
            "type": "BINARY_OP",
            "op": "+",
            "left": {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
            "right": {"type": "NUMBER", "value": "2", "line": 1, "column": 5}
        }
        
        with patch("._parse_or_package._parse_or_src._parse_or") as mock_parse_or:
            mock_parse_or.return_value = expected_ast
            
            result = _parse_expression(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["op"], "+")

    def test_parse_expression_with_parentheses(self):
        """测试解析带括号的表达式"""
        parser_state = {
            "tokens": [
                {"type": "LPAREN", "value": "(", "line": 1, "column": 1},
                {"type": "NUMBER", "value": "5", "line": 1, "column": 2},
                {"type": "RPAREN", "value": ")", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.cc"
        }
        
        expected_ast = {
            "type": "NUMBER",
            "value": "5",
            "line": 1,
            "column": 2
        }
        
        with patch("._parse_or_package._parse_or_src._parse_or") as mock_parse_or:
            mock_parse_or.return_value = expected_ast
            
            result = _parse_expression(parser_state)
            
            self.assertEqual(result["type"], "NUMBER")
            self.assertEqual(result["value"], "5")

    def test_parse_expression_with_logical_or(self):
        """测试解析逻辑或表达式"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "OR", "value": "||", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 6}
            ],
            "pos": 0,
            "filename": "test.cc"
        }
        
        expected_ast = {
            "type": "LOGICAL_OR",
            "left": {"type": "IDENTIFIER", "value": "a"},
            "right": {"type": "IDENTIFIER", "value": "b"}
        }
        
        with patch("._parse_or_package._parse_or_src._parse_or") as mock_parse_or:
            mock_parse_or.return_value = expected_ast
            
            result = _parse_expression(parser_state)
            
            self.assertEqual(result["type"], "LOGICAL_OR")

    def test_parse_expression_with_comparison(self):
        """测试解析比较表达式"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "10", "line": 1, "column": 1},
                {"type": "GREATER", "value": ">", "line": 1, "column": 4},
                {"type": "NUMBER", "value": "5", "line": 1, "column": 6}
            ],
            "pos": 0,
            "filename": "test.cc"
        }
        
        expected_ast = {
            "type": "COMPARISON",
            "op": ">",
            "left": {"type": "NUMBER", "value": "10"},
            "right": {"type": "NUMBER", "value": "5"}
        }
        
        with patch("._parse_or_package._parse_or_src._parse_or") as mock_parse_or:
            mock_parse_or.return_value = expected_ast
            
            result = _parse_expression(parser_state)
            
            self.assertEqual(result["type"], "COMPARISON")
            self.assertEqual(result["op"], ">")

    def test_parse_expression_with_unary_minus(self):
        """测试解析一元负号表达式"""
        parser_state = {
            "tokens": [
                {"type": "MINUS", "value": "-", "line": 1, "column": 1},
                {"type": "NUMBER", "value": "42", "line": 1, "column": 2}
            ],
            "pos": 0,
            "filename": "test.cc"
        }
        
        expected_ast = {
            "type": "UNARY_OP",
            "op": "-",
            "operand": {"type": "NUMBER", "value": "42"}
        }
        
        with patch("._parse_or_package._parse_or_src._parse_or") as mock_parse_or:
            mock_parse_or.return_value = expected_ast
            
            result = _parse_expression(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["op"], "-")

    def test_parse_expression_with_unary_not(self):
        """测试解析逻辑非表达式"""
        parser_state = {
            "tokens": [
                {"type": "NOT", "value": "!", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "flag", "line": 1, "column": 2}
            ],
            "pos": 0,
            "filename": "test.cc"
        }
        
        expected_ast = {
            "type": "UNARY_OP",
            "op": "!",
            "operand": {"type": "IDENTIFIER", "value": "flag"}
        }
        
        with patch("._parse_or_package._parse_or_src._parse_or") as mock_parse_or:
            mock_parse_or.return_value = expected_ast
            
            result = _parse_expression(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["op"], "!")

    def test_parse_expression_empty_tokens(self):
        """测试空 token 列表的边界情况"""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.cc"
        }
        
        expected_ast = {
            "type": "EMPTY",
            "value": None
        }
        
        with patch("._parse_or_package._parse_or_src._parse_or") as mock_parse_or:
            mock_parse_or.return_value = expected_ast
            
            result = _parse_expression(parser_state)
            
            mock_parse_or.assert_called_once_with(parser_state)
            self.assertEqual(result["type"], "EMPTY")

    def test_parse_expression_pos_at_end(self):
        """测试 pos 已在 token 列表末尾的边界情况"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1}
            ],
            "pos": 1,
            "filename": "test.cc"
        }
        
        expected_ast = {
            "type": "EMPTY",
            "value": None
        }
        
        with patch("._parse_or_package._parse_or_src._parse_or") as mock_parse_or:
            mock_parse_or.return_value = expected_ast
            
            result = _parse_expression(parser_state)
            
            self.assertEqual(result["type"], "EMPTY")

    def test_parse_expression_with_string_literal(self):
        """测试解析字符串字面量"""
        parser_state = {
            "tokens": [
                {"type": "STRING", "value": '"hello"', "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.cc"
        }
        
        expected_ast = {
            "type": "STRING",
            "value": '"hello"',
            "line": 1,
            "column": 1
        }
        
        with patch("._parse_or_package._parse_or_src._parse_or") as mock_parse_or:
            mock_parse_or.return_value = expected_ast
            
            result = _parse_expression(parser_state)
            
            self.assertEqual(result["type"], "STRING")

    def test_parse_expression_with_function_call(self):
        """测试解析函数调用表达式"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "func", "line": 1, "column": 1},
                {"type": "LPAREN", "value": "(", "line": 1, "column": 5},
                {"type": "RPAREN", "value": ")", "line": 1, "column": 6}
            ],
            "pos": 0,
            "filename": "test.cc"
        }
        
        expected_ast = {
            "type": "CALL",
            "function": {"type": "IDENTIFIER", "value": "func"},
            "arguments": []
        }
        
        with patch("._parse_or_package._parse_or_src._parse_or") as mock_parse_or:
            mock_parse_or.return_value = expected_ast
            
            result = _parse_expression(parser_state)
            
            self.assertEqual(result["type"], "CALL")

    def test_parse_expression_complex_nested(self):
        """测试复杂嵌套表达式"""
        parser_state = {
            "tokens": [
                {"type": "LPAREN", "value": "(", "line": 1, "column": 1},
                {"type": "NUMBER", "value": "1", "line": 1, "column": 2},
                {"type": "PLUS", "value": "+", "line": 1, "column": 4},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 6},
                {"type": "RPAREN", "value": ")", "line": 1, "column": 7},
                {"type": "STAR", "value": "*", "line": 1, "column": 9},
                {"type": "NUMBER", "value": "3", "line": 1, "column": 11}
            ],
            "pos": 0,
            "filename": "test.cc"
        }
        
        expected_ast = {
            "type": "BINARY_OP",
            "op": "*",
            "left": {
                "type": "BINARY_OP",
                "op": "+",
                "left": {"type": "NUMBER", "value": "1"},
                "right": {"type": "NUMBER", "value": "2"}
            },
            "right": {"type": "NUMBER", "value": "3"}
        }
        
        with patch("._parse_or_package._parse_or_src._parse_or") as mock_parse_or:
            mock_parse_or.return_value = expected_ast
            
            result = _parse_expression(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["op"], "*")

    def test_parse_expression_preserves_parser_state_reference(self):
        """测试 parser_state 作为引用传递"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "42", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.cc"
        }
        
        expected_ast = {"type": "NUMBER", "value": "42"}
        
        def side_effect(state):
            state["pos"] = 1
            return expected_ast
        
        with patch("._parse_or_package._parse_or_src._parse_or") as mock_parse_or:
            mock_parse_or.side_effect = side_effect
            
            result = _parse_expression(parser_state)
            
            self.assertEqual(parser_state["pos"], 1)
            self.assertEqual(result, expected_ast)


class TestCurrentTokenType(unittest.TestCase):
    """_current_token_type 辅助函数的单元测试"""

    def test_current_token_type_returns_type_when_valid(self):
        """测试在有效位置返回 token 类型"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "42", "line": 1, "column": 1}
            ],
            "pos": 0
        }
        
        result = _current_token_type(parser_state)
        
        self.assertEqual(result, "NUMBER")

    def test_current_token_type_returns_none_at_end(self):
        """测试在 token 列表末尾返回 None"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "42", "line": 1, "column": 1}
            ],
            "pos": 1
        }
        
        result = _current_token_type(parser_state)
        
        self.assertIsNone(result)

    def test_current_token_type_returns_none_empty_tokens(self):
        """测试空 token 列表返回 None"""
        parser_state = {
            "tokens": [],
            "pos": 0
        }
        
        result = _current_token_type(parser_state)
        
        self.assertIsNone(result)

    def test_current_token_type_returns_none_negative_pos(self):
        """测试负数 pos 返回 None"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "42", "line": 1, "column": 1}
            ],
            "pos": -1
        }
        
        result = _current_token_type(parser_state)
        
        self.assertIsNone(result)

    def test_current_token_type_middle_position(self):
        """测试在 token 列表中间位置"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 5}
            ],
            "pos": 1
        }
        
        result = _current_token_type(parser_state)
        
        self.assertEqual(result, "PLUS")

    def test_current_token_type_last_token(self):
        """测试在最后一个 token 位置"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 5}
            ],
            "pos": 2
        }
        
        result = _current_token_type(parser_state)
        
        self.assertEqual(result, "NUMBER")


if __name__ == "__main__":
    unittest.main()

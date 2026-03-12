# -*- coding: utf-8 -*-
"""
单元测试：_parse_unary 函数
测试一元表达式解析器（标识符、字面量、一元运算符、括号表达式）
"""

import unittest
from unittest.mock import patch

from ._parse_unary_src import _parse_unary


class TestParseUnary(unittest.TestCase):
    """_parse_unary 函数测试用例"""

    def test_parse_identifier(self):
        """测试解析标识符"""
        parser_state = {
            "tokens": [{"type": "IDENTIFIER", "value": "x", "line": 1, "column": 5}],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("._get_current_token_package._get_current_token_src._get_current_token") as mock_get_token, \
             patch("._advance_parser_package._advance_parser_src._advance_parser") as mock_advance:
            mock_get_token.return_value = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 5}
            
            result = _parse_unary(parser_state)
            
            self.assertEqual(result["type"], "IDENTIFIER")
            self.assertEqual(result["value"], "x")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 5)
            mock_advance.assert_called_once_with(parser_state)

    def test_parse_number_literal(self):
        """测试解析数字字面量"""
        parser_state = {
            "tokens": [{"type": "NUMBER", "value": "42", "line": 1, "column": 10}],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("._get_current_token_package._get_current_token_src._get_current_token") as mock_get_token, \
             patch("._advance_parser_package._advance_parser_src._advance_parser") as mock_advance, \
             patch("._extract_literal_value_package._extract_literal_value_src._extract_literal_value") as mock_extract:
            mock_get_token.return_value = {"type": "NUMBER", "value": "42", "line": 1, "column": 10}
            mock_extract.return_value = 42
            
            result = _parse_unary(parser_state)
            
            self.assertEqual(result["type"], "LITERAL")
            self.assertEqual(result["value"], 42)
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 10)
            mock_advance.assert_called_once_with(parser_state)
            mock_extract.assert_called_once_with({"type": "NUMBER", "value": "42", "line": 1, "column": 10})

    def test_parse_string_literal(self):
        """测试解析字符串字面量"""
        parser_state = {
            "tokens": [{"type": "STRING", "value": '"hello"', "line": 2, "column": 3}],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("._get_current_token_package._get_current_token_src._get_current_token") as mock_get_token, \
             patch("._advance_parser_package._advance_parser_src._advance_parser") as mock_advance, \
             patch("._extract_literal_value_package._extract_literal_value_src._extract_literal_value") as mock_extract:
            mock_get_token.return_value = {"type": "STRING", "value": '"hello"', "line": 2, "column": 3}
            mock_extract.return_value = "hello"
            
            result = _parse_unary(parser_state)
            
            self.assertEqual(result["type"], "LITERAL")
            self.assertEqual(result["value"], "hello")
            self.assertEqual(result["line"], 2)
            self.assertEqual(result["column"], 3)

    def test_parse_unary_minus(self):
        """测试解析一元减号运算符"""
        parser_state = {
            "tokens": [
                {"type": "MINUS", "value": "-", "line": 1, "column": 1},
                {"type": "NUMBER", "value": "5", "line": 1, "column": 2}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("._get_current_token_package._get_current_token_src._get_current_token") as mock_get_token, \
             patch("._advance_parser_package._advance_parser_src._advance_parser") as mock_advance, \
             patch("._check_unary_op_package._check_unary_op_src._check_unary_op") as mock_check_unary, \
             patch("._parse_unary_package._parse_unary_src._parse_unary") as mock_parse_unary_recursive:
            # 第一次调用返回 MINUS，第二次调用返回操作数
            mock_get_token.side_effect = [
                {"type": "MINUS", "value": "-", "line": 1, "column": 1},
                {"type": "NUMBER", "value": "5", "line": 1, "column": 2}
            ]
            mock_check_unary.return_value = True
            mock_parse_unary_recursive.return_value = {
                "type": "LITERAL",
                "value": 5,
                "line": 1,
                "column": 2
            }
            
            result = _parse_unary(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], {"operator": "-"})
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(result["children"][0]["type"], "LITERAL")
            self.assertEqual(mock_advance.call_count, 1)

    def test_parse_unary_plus(self):
        """测试解析一元加号运算符"""
        parser_state = {
            "tokens": [
                {"type": "PLUS", "value": "+", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 2}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("._get_current_token_package._get_current_token_src._get_current_token") as mock_get_token, \
             patch("._advance_parser_package._advance_parser_src._advance_parser") as mock_advance, \
             patch("._check_unary_op_package._check_unary_op_src._check_unary_op") as mock_check_unary, \
             patch("._parse_unary_package._parse_unary_src._parse_unary") as mock_parse_unary_recursive:
            mock_get_token.side_effect = [
                {"type": "PLUS", "value": "+", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 2}
            ]
            mock_check_unary.return_value = True
            mock_parse_unary_recursive.return_value = {
                "type": "IDENTIFIER",
                "value": "x",
                "line": 1,
                "column": 2
            }
            
            result = _parse_unary(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], {"operator": "+"})
            self.assertEqual(len(result["children"]), 1)

    def test_parse_unary_not(self):
        """测试解析逻辑非运算符"""
        parser_state = {
            "tokens": [
                {"type": "NOT", "value": "not", "line": 3, "column": 5},
                {"type": "IDENTIFIER", "value": "flag", "line": 3, "column": 9}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("._get_current_token_package._get_current_token_src._get_current_token") as mock_get_token, \
             patch("._advance_parser_package._advance_parser_src._advance_parser") as mock_advance, \
             patch("._check_unary_op_package._check_unary_op_src._check_unary_op") as mock_check_unary, \
             patch("._parse_unary_package._parse_unary_src._parse_unary") as mock_parse_unary_recursive:
            mock_get_token.side_effect = [
                {"type": "NOT", "value": "not", "line": 3, "column": 5},
                {"type": "IDENTIFIER", "value": "flag", "line": 3, "column": 9}
            ]
            mock_check_unary.return_value = True
            mock_parse_unary_recursive.return_value = {
                "type": "IDENTIFIER",
                "value": "flag",
                "line": 3,
                "column": 9
            }
            
            result = _parse_unary(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], {"operator": "not"})

    def test_parse_unary_tilde(self):
        """测试解析按位取反运算符"""
        parser_state = {
            "tokens": [
                {"type": "TILDE", "value": "~", "line": 1, "column": 1},
                {"type": "NUMBER", "value": "10", "line": 1, "column": 2}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("._get_current_token_package._get_current_token_src._get_current_token") as mock_get_token, \
             patch("._advance_parser_package._advance_parser_src._advance_parser") as mock_advance, \
             patch("._check_unary_op_package._check_unary_op_src._check_unary_op") as mock_check_unary, \
             patch("._parse_unary_package._parse_unary_src._parse_unary") as mock_parse_unary_recursive:
            mock_get_token.side_effect = [
                {"type": "TILDE", "value": "~", "line": 1, "column": 1},
                {"type": "NUMBER", "value": "10", "line": 1, "column": 2}
            ]
            mock_check_unary.return_value = True
            mock_parse_unary_recursive.return_value = {
                "type": "LITERAL",
                "value": 10,
                "line": 1,
                "column": 2
            }
            
            result = _parse_unary(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], {"operator": "~"})

    def test_parse_nested_unary(self):
        """测试嵌套一元运算符（如 --x）"""
        parser_state = {
            "tokens": [
                {"type": "MINUS", "value": "-", "line": 1, "column": 1},
                {"type": "MINUS", "value": "-", "line": 1, "column": 2},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("._get_current_token_package._get_current_token_src._get_current_token") as mock_get_token, \
             patch("._advance_parser_package._advance_parser_src._advance_parser") as mock_advance, \
             patch("._check_unary_op_package._check_unary_op_src._check_unary_op") as mock_check_unary, \
             patch("._parse_unary_package._parse_unary_src._parse_unary") as mock_parse_unary_recursive:
            # 第一次调用返回外层 MINUS，递归调用返回内层 UNARY_OP
            mock_get_token.side_effect = [
                {"type": "MINUS", "value": "-", "line": 1, "column": 1},
                {"type": "MINUS", "value": "-", "line": 1, "column": 2},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 3}
            ]
            mock_check_unary.return_value = True
            # 递归调用返回内层一元表达式
            inner_unary = {
                "type": "UNARY_OP",
                "value": {"operator": "-"},
                "children": [{
                    "type": "IDENTIFIER",
                    "value": "x",
                    "line": 1,
                    "column": 3
                }],
                "line": 1,
                "column": 2
            }
            mock_parse_unary_recursive.return_value = inner_unary
            
            result = _parse_unary(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], {"operator": "-"})
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(result["children"][0]["type"], "UNARY_OP")

    def test_parse_parenthesized_expression(self):
        """测试解析括号表达式"""
        parser_state = {
            "tokens": [
                {"type": "LPAREN", "value": "(", "line": 1, "column": 1},
                {"type": "NUMBER", "value": "3", "line": 1, "column": 2},
                {"type": "RPAREN", "value": ")", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("._get_current_token_package._get_current_token_src._get_current_token") as mock_get_token, \
             patch("._advance_parser_package._advance_parser_src._advance_parser") as mock_advance, \
             patch("._check_unary_op_package._check_unary_op_src._check_unary_op") as mock_check_unary, \
             patch("._parse_binary_package._parse_binary_src._parse_binary") as mock_parse_binary, \
             patch("._expect_token_type_package._expect_token_type_src._expect_token_type") as mock_expect:
            mock_get_token.return_value = {"type": "LPAREN", "value": "(", "line": 1, "column": 1}
            mock_check_unary.return_value = False
            mock_parse_binary.return_value = {
                "type": "LITERAL",
                "value": 3,
                "line": 1,
                "column": 2
            }
            
            result = _parse_unary(parser_state)
            
            self.assertEqual(result["type"], "LITERAL")
            self.assertEqual(result["value"], 3)
            mock_advance.assert_called_once_with(parser_state)
            mock_parse_binary.assert_called_once_with(parser_state, min_precedence=0)
            mock_expect.assert_called_once_with(parser_state, "RPAREN", ")")

    def test_parse_parenthesized_complex_expression(self):
        """测试解析复杂括号表达式（调用 _parse_binary）"""
        parser_state = {
            "tokens": [
                {"type": "LPAREN", "value": "(", "line": 2, "column": 5},
                {"type": "IDENTIFIER", "value": "a", "line": 2, "column": 6},
                {"type": "PLUS", "value": "+", "line": 2, "column": 7},
                {"type": "NUMBER", "value": "1", "line": 2, "column": 8},
                {"type": "RPAREN", "value": ")", "line": 2, "column": 9}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("._get_current_token_package._get_current_token_src._get_current_token") as mock_get_token, \
             patch("._advance_parser_package._advance_parser_src._advance_parser") as mock_advance, \
             patch("._check_unary_op_package._check_unary_op_src._check_unary_op") as mock_check_unary, \
             patch("._parse_binary_package._parse_binary_src._parse_binary") as mock_parse_binary, \
             patch("._expect_token_type_package._expect_token_type_src._expect_token_type") as mock_expect:
            mock_get_token.return_value = {"type": "LPAREN", "value": "(", "line": 2, "column": 5}
            mock_check_unary.return_value = False
            binary_result = {
                "type": "BINARY_OP",
                "value": {"operator": "+"},
                "children": [
                    {"type": "IDENTIFIER", "value": "a", "line": 2, "column": 6},
                    {"type": "LITERAL", "value": 1, "line": 2, "column": 8}
                ],
                "line": 2,
                "column": 6
            }
            mock_parse_binary.return_value = binary_result
            
            result = _parse_unary(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], {"operator": "+"})
            mock_parse_binary.assert_called_once_with(parser_state, min_precedence=0)

    def test_invalid_token_raises_syntax_error(self):
        """测试无效 token 抛出 SyntaxError"""
        parser_state = {
            "tokens": [{"type": "RPAREN", "value": ")", "line": 5, "column": 10}],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("._get_current_token_package._get_current_token_src._get_current_token") as mock_get_token, \
             patch("._check_unary_op_package._check_unary_op_src._check_unary_op") as mock_check_unary:
            mock_get_token.return_value = {"type": "RPAREN", "value": ")", "line": 5, "column": 10}
            mock_check_unary.return_value = False
            
            with self.assertRaises(SyntaxError) as context:
                _parse_unary(parser_state)
            
            error_msg = str(context.exception)
            self.assertIn("test.py:5:10", error_msg)
            self.assertIn("期望表达式起始", error_msg)
            self.assertIn("RPAREN", error_msg)

    def test_eof_raises_syntax_error(self):
        """测试 EOF（空 token）抛出 SyntaxError"""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("._get_current_token_package._get_current_token_src._get_current_token") as mock_get_token, \
             patch("._check_unary_op_package._check_unary_op_src._check_unary_op") as mock_check_unary:
            mock_get_token.return_value = None
            mock_check_unary.return_value = False
            
            with self.assertRaises(SyntaxError) as context:
                _parse_unary(parser_state)
            
            error_msg = str(context.exception)
            self.assertIn("test.py:0:0", error_msg)
            self.assertIn("期望表达式起始", error_msg)
            self.assertIn("EOF", error_msg)

    def test_unknown_token_type_raises_syntax_error(self):
        """测试未知 token 类型抛出 SyntaxError"""
        parser_state = {
            "tokens": [{"type": "UNKNOWN", "value": "?", "line": 3, "column": 7}],
            "pos": 0,
            "filename": "main.py"
        }
        
        with patch("._get_current_token_package._get_current_token_src._get_current_token") as mock_get_token, \
             patch("._check_unary_op_package._check_unary_op_src._check_unary_op") as mock_check_unary:
            mock_get_token.return_value = {"type": "UNKNOWN", "value": "?", "line": 3, "column": 7}
            mock_check_unary.return_value = False
            
            with self.assertRaises(SyntaxError) as context:
                _parse_unary(parser_state)
            
            error_msg = str(context.exception)
            self.assertIn("main.py:3:7", error_msg)
            self.assertIn("期望表达式起始", error_msg)
            self.assertIn("UNKNOWN", error_msg)

    def test_unary_operator_consumes_token(self):
        """测试一元运算符解析时消耗 token"""
        parser_state = {
            "tokens": [
                {"type": "MINUS", "value": "-", "line": 1, "column": 1},
                {"type": "NUMBER", "value": "5", "line": 1, "column": 2}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("._get_current_token_package._get_current_token_src._get_current_token") as mock_get_token, \
             patch("._advance_parser_package._advance_parser_src._advance_parser") as mock_advance, \
             patch("._check_unary_op_package._check_unary_op_src._check_unary_op") as mock_check_unary, \
             patch("._parse_unary_package._parse_unary_src._parse_unary") as mock_parse_unary_recursive:
            mock_get_token.return_value = {"type": "MINUS", "value": "-", "line": 1, "column": 1}
            mock_check_unary.return_value = True
            mock_parse_unary_recursive.return_value = {
                "type": "LITERAL",
                "value": 5,
                "line": 1,
                "column": 2
            }
            
            _parse_unary(parser_state)
            
            # 验证 _advance_parser 被调用（消耗一元运算符 token）
            mock_advance.assert_called_once_with(parser_state)

    def test_identifier_consumes_token(self):
        """测试标识符解析时消耗 token"""
        parser_state = {
            "tokens": [{"type": "IDENTIFIER", "value": "foo", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("._get_current_token_package._get_current_token_src._get_current_token") as mock_get_token, \
             patch("._advance_parser_package._advance_parser_src._advance_parser") as mock_advance, \
             patch("._check_unary_op_package._check_unary_op_src._check_unary_op") as mock_check_unary:
            mock_get_token.return_value = {"type": "IDENTIFIER", "value": "foo", "line": 1, "column": 1}
            mock_check_unary.return_value = False
            
            _parse_unary(parser_state)
            
            mock_advance.assert_called_once_with(parser_state)

    def test_literal_consumes_token(self):
        """测试字面量解析时消耗 token"""
        parser_state = {
            "tokens": [{"type": "NUMBER", "value": "123", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("._get_current_token_package._get_current_token_src._get_current_token") as mock_get_token, \
             patch("._advance_parser_package._advance_parser_src._advance_parser") as mock_advance, \
             patch("._check_unary_op_package._check_unary_op_src._check_unary_op") as mock_check_unary, \
             patch("._extract_literal_value_package._extract_literal_value_src._extract_literal_value") as mock_extract:
            mock_get_token.return_value = {"type": "NUMBER", "value": "123", "line": 1, "column": 1}
            mock_check_unary.return_value = False
            mock_extract.return_value = 123
            
            _parse_unary(parser_state)
            
            mock_advance.assert_called_once_with(parser_state)

    def test_parenthesis_consumes_token(self):
        """测试括号表达式解析时消耗 LPAREN token"""
        parser_state = {
            "tokens": [
                {"type": "LPAREN", "value": "(", "line": 1, "column": 1},
                {"type": "NUMBER", "value": "1", "line": 1, "column": 2},
                {"type": "RPAREN", "value": ")", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("._get_current_token_package._get_current_token_src._get_current_token") as mock_get_token, \
             patch("._advance_parser_package._advance_parser_src._advance_parser") as mock_advance, \
             patch("._check_unary_op_package._check_unary_op_src._check_unary_op") as mock_check_unary, \
             patch("._parse_binary_package._parse_binary_src._parse_binary") as mock_parse_binary, \
             patch("._expect_token_type_package._expect_token_type_src._expect_token_type") as mock_expect:
            mock_get_token.return_value = {"type": "LPAREN", "value": "(", "line": 1, "column": 1}
            mock_check_unary.return_value = False
            mock_parse_binary.return_value = {"type": "LITERAL", "value": 1, "line": 1, "column": 2}
            
            _parse_unary(parser_state)
            
            mock_advance.assert_called_once_with(parser_state)


if __name__ == "__main__":
    unittest.main()

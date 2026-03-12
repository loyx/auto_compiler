import unittest
from unittest.mock import patch
import sys
import os

# Add parent directory to path for relative imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ._parse_primary_src import _parse_primary


class TestParsePrimary(unittest.TestCase):
    """测试 _parse_primary 函数解析基础单元的功能。"""

    def test_parse_number_integer(self):
        """测试解析整数字面量。"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "42", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.cc"
        }
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "number_literal")
        self.assertEqual(result["value"], 42)
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_number_float(self):
        """测试解析浮点数字面量。"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "3.14", "line": 2, "column": 5}
            ],
            "pos": 0,
            "filename": "test.cc"
        }
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "number_literal")
        self.assertEqual(result["value"], 3.14)
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 5)
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_string_double_quotes(self):
        """测试解析双引号字符串字面量。"""
        parser_state = {
            "tokens": [
                {"type": "STRING_LITERAL", "value": '"hello world"', "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.cc"
        }
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "string_literal")
        self.assertEqual(result["value"], "hello world")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_string_single_quotes(self):
        """测试解析单引号字符串字面量。"""
        parser_state = {
            "tokens": [
                {"type": "STRING_LITERAL", "value": "'hello world'", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.cc"
        }
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "string_literal")
        self.assertEqual(result["value"], "hello world")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_string_no_quotes(self):
        """测试解析无引号字符串字面量（边界情况）。"""
        parser_state = {
            "tokens": [
                {"type": "STRING_LITERAL", "value": "hello", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.cc"
        }
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "string_literal")
        self.assertEqual(result["value"], "hello")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_true(self):
        """测试解析 TRUE 关键字。"""
        parser_state = {
            "tokens": [
                {"type": "TRUE", "value": "true", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.cc"
        }
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "boolean_literal")
        self.assertEqual(result["value"], True)
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_false(self):
        """测试解析 FALSE 关键字。"""
        parser_state = {
            "tokens": [
                {"type": "FALSE", "value": "false", "line": 3, "column": 10}
            ],
            "pos": 0,
            "filename": "test.cc"
        }
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "boolean_literal")
        self.assertEqual(result["value"], False)
        self.assertEqual(result["line"], 3)
        self.assertEqual(result["column"], 10)
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_identifier(self):
        """测试解析标识符。"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "myVariable", "line": 5, "column": 2}
            ],
            "pos": 0,
            "filename": "test.cc"
        }
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "identifier")
        self.assertEqual(result["value"], "myVariable")
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 2)
        self.assertEqual(parser_state["pos"], 1)

    @patch('._parse_primary_src._parse_expression')
    def test_parse_parenthesized_expression(self, mock_parse_expression):
        """测试解析括号表达式。"""
        mock_parse_expression.return_value = {
            "type": "binary_expression",
            "value": "+",
            "line": 1,
            "column": 2
        }
        
        parser_state = {
            "tokens": [
                {"type": "LPAREN", "value": "(", "line": 1, "column": 1},
                {"type": "NUMBER", "value": "1", "line": 1, "column": 2},
                {"type": "RPAREN", "value": ")", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.cc"
        }
        result = _parse_primary(parser_state)
        
        mock_parse_expression.assert_called_once()
        self.assertEqual(result["type"], "binary_expression")
        self.assertEqual(result["value"], "+")
        self.assertEqual(parser_state["pos"], 3)

    @patch('._parse_primary_src._parse_expression')
    def test_parse_parenthesized_expression_missing_rparen(self, mock_parse_expression):
        """测试括号表达式缺少右括号时抛出 SyntaxError。"""
        mock_parse_expression.return_value = {
            "type": "identifier",
            "value": "x",
            "line": 1,
            "column": 2
        }
        
        parser_state = {
            "tokens": [
                {"type": "LPAREN", "value": "(", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 2}
            ],
            "pos": 0,
            "filename": "test.cc"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_primary(parser_state)
        
        self.assertIn("Expected ')'", str(context.exception))
        self.assertIn("test.cc:1:1", str(context.exception))

    @patch('._parse_primary_src._parse_expression')
    def test_parse_parenthesized_expression_end_of_input(self, mock_parse_expression):
        """测试括号表达式在输入结束时缺少右括号。"""
        mock_parse_expression.return_value = {
            "type": "identifier",
            "value": "x",
            "line": 1,
            "column": 2
        }
        
        parser_state = {
            "tokens": [
                {"type": "LPAREN", "value": "(", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 2}
            ],
            "pos": 0,
            "filename": "test.cc"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_primary(parser_state)
        
        self.assertIn("Expected ')'", str(context.exception))

    def test_parse_empty_input(self):
        """测试空输入时抛出 SyntaxError。"""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.cc"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_primary(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))
        self.assertIn("test.cc:0:0", str(context.exception))

    def test_parse_pos_beyond_tokens(self):
        """测试 pos 超出 tokens 范围时抛出 SyntaxError。"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1}
            ],
            "pos": 5,
            "filename": "test.cc"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_primary(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))

    def test_parse_unexpected_token(self):
        """测试遇到不支持的 token 类型时抛出 SyntaxError。"""
        parser_state = {
            "tokens": [
                {"type": "PLUS", "value": "+", "line": 2, "column": 3}
            ],
            "pos": 0,
            "filename": "test.cc"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_primary(parser_state)
        
        self.assertIn("Unexpected token '+'", str(context.exception))
        self.assertIn("test.cc:2:3", str(context.exception))

    def test_parse_number_negative(self):
        """测试解析负数字面量（带负号的数字）。"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "-123", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.cc"
        }
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "number_literal")
        self.assertEqual(result["value"], -123)
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)

    def test_parse_filename_default(self):
        """测试 filename 缺失时使用默认值。"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "42", "line": 1, "column": 1}
            ],
            "pos": 0
        }
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "number_literal")
        self.assertEqual(result["value"], 42)

    def test_parse_multiple_tokens_only_consumes_one(self):
        """测试解析多个 tokens 时只消费当前 token。"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 2},
                {"type": "NUMBER", "value": "3", "line": 1, "column": 3}
            ],
            "pos": 1,
            "filename": "test.cc"
        }
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["value"], 2)
        self.assertEqual(parser_state["pos"], 2)


if __name__ == "__main__":
    unittest.main()

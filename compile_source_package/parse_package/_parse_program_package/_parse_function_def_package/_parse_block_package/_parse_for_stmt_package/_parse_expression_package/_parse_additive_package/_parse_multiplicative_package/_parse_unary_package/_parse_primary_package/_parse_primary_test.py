import unittest
from unittest.mock import patch
import sys
import os

# 添加父目录到路径以支持相对导入
_current_dir = os.path.dirname(os.path.abspath(__file__))
_parent_dir = os.path.dirname(_current_dir)
if _parent_dir not in sys.path:
    sys.path.insert(0, _parent_dir)

from ._parse_primary_src import _parse_primary


class TestParsePrimary(unittest.TestCase):
    
    def test_parse_identifier(self):
        """测试标识符解析"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "x")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(result["children"], [])
        self.assertEqual(parser_state["pos"], 1)
        self.assertNotIn("error", parser_state)
    
    def test_parse_number_literal(self):
        """测试数字字面量解析"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "42", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "42")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(result["children"], [])
        self.assertEqual(parser_state["pos"], 1)
        self.assertNotIn("error", parser_state)
    
    def test_parse_string_literal(self):
        """测试字符串字面量解析"""
        parser_state = {
            "tokens": [
                {"type": "STRING", "value": '"hello"', "line": 2, "column": 5}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], '"hello"')
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 5)
        self.assertEqual(result["children"], [])
        self.assertEqual(parser_state["pos"], 1)
        self.assertNotIn("error", parser_state)
    
    @patch('._parse_unary_package._parse_unary_src._parse_unary')
    def test_parse_parenthesized_expression(self, mock_parse_unary):
        """测试括号表达式解析"""
        mock_parse_unary.return_value = {
            "type": "IDENTIFIER",
            "value": "y",
            "children": [],
            "line": 1,
            "column": 2
        }
        
        parser_state = {
            "tokens": [
                {"type": "LPAREN", "value": "(", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "y", "line": 1, "column": 2},
                {"type": "RPAREN", "value": ")", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "y")
        self.assertEqual(parser_state["pos"], 3)
        mock_parse_unary.assert_called_once()
        self.assertNotIn("error", parser_state)
    
    @patch('._parse_unary_package._parse_unary_src._parse_unary')
    def test_parenthesized_expression_with_unary_error(self, mock_parse_unary):
        """测试括号内解析错误时的错误传播"""
        mock_parse_unary.return_value = {
            "type": "ERROR",
            "value": "",
            "children": [],
            "line": 0,
            "column": 0
        }
        
        parser_state = {
            "tokens": [
                {"type": "LPAREN", "value": "(", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "y", "line": 1, "column": 2}
            ],
            "pos": 0,
            "filename": "test.py",
            "error": "Inner error"
        }
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(parser_state["error"], "Inner error")
        mock_parse_unary.assert_called_once()
    
    @patch('._parse_unary_package._parse_unary_src._parse_unary')
    def test_missing_closing_parenthesis(self, mock_parse_unary):
        """测试缺少右括号的错误处理"""
        mock_parse_unary.return_value = {
            "type": "IDENTIFIER",
            "value": "z",
            "children": [],
            "line": 1,
            "column": 2
        }
        
        parser_state = {
            "tokens": [
                {"type": "LPAREN", "value": "(", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "z", "line": 1, "column": 2}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], "")
        self.assertEqual(parser_state["error"], "Missing closing parenthesis")
        self.assertEqual(parser_state["pos"], 1)
        mock_parse_unary.assert_called_once()
    
    def test_empty_tokens(self):
        """测试空 token 列表的错误处理"""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], "")
        self.assertEqual(parser_state["error"], "Unexpected end of input")
        self.assertEqual(parser_state["pos"], 0)
    
    def test_pos_at_end(self):
        """测试 pos 在 token 列表末尾的错误处理"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 1,
            "filename": "test.py"
        }
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], "")
        self.assertEqual(parser_state["error"], "Unexpected end of input")
        self.assertEqual(parser_state["pos"], 1)
    
    def test_invalid_token_type(self):
        """测试无效 token 类型的错误处理"""
        parser_state = {
            "tokens": [
                {"type": "UNKNOWN", "value": "?", "line": 3, "column": 7}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], "?")
        self.assertEqual(result["line"], 3)
        self.assertEqual(result["column"], 7)
        self.assertIn("Unexpected token '?'", parser_state["error"])
        self.assertEqual(parser_state["pos"], 0)
    
    def test_operator_token_invalid(self):
        """测试运算符 token 作为 primary 的错误处理"""
        parser_state = {
            "tokens": [
                {"type": "PLUS", "value": "+", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], "+")
        self.assertIn("Unexpected token '+'", parser_state["error"])
        self.assertEqual(parser_state["pos"], 0)
    
    @patch('._parse_unary_package._parse_unary_src._parse_unary')
    def test_nested_parentheses(self, mock_parse_unary):
        """测试嵌套括号表达式（通过 mock 模拟）"""
        mock_parse_unary.return_value = {
            "type": "IDENTIFIER",
            "value": "a",
            "children": [],
            "line": 1,
            "column": 2
        }
        
        parser_state = {
            "tokens": [
                {"type": "LPAREN", "value": "(", "line": 1, "column": 1},
                {"type": "LPAREN", "value": "(", "line": 1, "column": 2},
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 3},
                {"type": "RPAREN", "value": ")", "line": 1, "column": 4},
                {"type": "RPAREN", "value": ")", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "a")
        self.assertEqual(parser_state["pos"], 3)
        mock_parse_unary.assert_called_once()
    
    def test_multiple_tokens_only_consumes_one(self):
        """测试多个 token 时只消耗一个"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "first", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "second", "line": 1, "column": 6}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "first")
        self.assertEqual(parser_state["pos"], 1)


if __name__ == "__main__":
    unittest.main()

# -*- coding: utf-8 -*-
"""单元测试：_expect_token 函数"""

import unittest
from typing import Any, Dict

# 相对导入被测模块
from ._expect_token_src import _expect_token

Token = Dict[str, Any]
ParserState = Dict[str, Any]


class TestExpectToken(unittest.TestCase):
    """_expect_token 函数的单元测试"""

    def test_expect_token_success_basic(self):
        """测试：成功匹配基本 token 类型"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        result = _expect_token(parser_state, "IDENTIFIER")
        
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "x")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 1)

    def test_expect_token_success_multiple_tokens(self):
        """测试：在多个 token 中成功匹配"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "KEYWORD", "value": "for", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "i", "line": 1, "column": 5},
                {"type": "OPERATOR", "value": "in", "line": 1, "column": 7}
            ],
            "pos": 1,
            "filename": "test.py",
            "error": ""
        }
        
        result = _expect_token(parser_state, "IDENTIFIER")
        
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "i")
        self.assertEqual(parser_state["pos"], 2)

    def test_expect_token_success_at_last_position(self):
        """测试：在最后一个 token 位置成功匹配"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "KEYWORD", "value": "if", "line": 1, "column": 1},
                {"type": "LPAREN", "value": "(", "line": 1, "column": 4}
            ],
            "pos": 1,
            "filename": "test.py",
            "error": ""
        }
        
        result = _expect_token(parser_state, "LPAREN")
        
        self.assertEqual(result["type"], "LPAREN")
        self.assertEqual(result["value"], "(")
        self.assertEqual(parser_state["pos"], 2)

    def test_expect_token_failure_end_of_input(self):
        """测试：失败 - 已到达输入末尾"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 1,
            "filename": "test.py",
            "error": ""
        }
        
        with self.assertRaises(SyntaxError) as context:
            _expect_token(parser_state, "IDENTIFIER")
        
        self.assertIn("Unexpected end of input", str(context.exception))
        self.assertIn("expected IDENTIFIER", str(context.exception))
        self.assertEqual(parser_state["pos"], 1)

    def test_expect_token_failure_empty_tokens(self):
        """测试：失败 - token 列表为空"""
        parser_state: ParserState = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        with self.assertRaises(SyntaxError) as context:
            _expect_token(parser_state, "IDENTIFIER")
        
        self.assertIn("Unexpected end of input", str(context.exception))
        self.assertEqual(parser_state["pos"], 0)

    def test_expect_token_failure_type_mismatch(self):
        """测试：失败 - token 类型不匹配"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "KEYWORD", "value": "for", "line": 3, "column": 10}
            ],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        with self.assertRaises(SyntaxError) as context:
            _expect_token(parser_state, "IDENTIFIER")
        
        self.assertIn("Expected IDENTIFIER", str(context.exception))
        self.assertIn("got KEYWORD", str(context.exception))
        self.assertIn("line 3", str(context.exception))
        self.assertIn("column 10", str(context.exception))
        self.assertEqual(parser_state["pos"], 0)

    def test_expect_token_failure_type_mismatch_no_line_column(self):
        """测试：失败 - token 类型不匹配且无线号列号信息"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "OPERATOR", "value": "+"}
            ],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        with self.assertRaises(SyntaxError) as context:
            _expect_token(parser_state, "IDENTIFIER")
        
        self.assertIn("Expected IDENTIFIER", str(context.exception))
        self.assertIn("got OPERATOR", str(context.exception))
        self.assertIn("line ?", str(context.exception))
        self.assertIn("column ?", str(context.exception))
        self.assertEqual(parser_state["pos"], 0)

    def test_expect_token_does_not_consume_on_mismatch(self):
        """测试：类型不匹配时不消耗 token（pos 不变）"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "NUMBER", "value": "42", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 4}
            ],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        with self.assertRaises(SyntaxError):
            _expect_token(parser_state, "IDENTIFIER")
        
        self.assertEqual(parser_state["pos"], 0)

    def test_expect_token_preserves_other_state(self):
        """测试：成功时保留 parser_state 其他字段不变"""
        parser_state: ParserState = {
            "tokens": [
                {"type": "STRING", "value": "hello", "line": 5, "column": 20}
            ],
            "pos": 0,
            "filename": "mymodule.py",
            "error": "some previous error"
        }
        
        _expect_token(parser_state, "STRING")
        
        self.assertEqual(parser_state["filename"], "mymodule.py")
        self.assertEqual(parser_state["error"], "some previous error")
        self.assertEqual(len(parser_state["tokens"]), 1)

    def test_expect_token_various_token_types(self):
        """测试：多种 token 类型的匹配"""
        token_types = ["KEYWORD", "OPERATOR", "LPAREN", "RPAREN", 
                       "LBRACKET", "RBRACKET", "COLON", "COMMA", 
                       "NUMBER", "STRING", "COMMENT"]
        
        for token_type in token_types:
            parser_state: ParserState = {
                "tokens": [
                    {"type": token_type, "value": "test", "line": 1, "column": 1}
                ],
                "pos": 0,
                "filename": "test.py",
                "error": ""
            }
            
            result = _expect_token(parser_state, token_type)
            
            self.assertEqual(result["type"], token_type)
            self.assertEqual(parser_state["pos"], 1)


if __name__ == "__main__":
    unittest.main()

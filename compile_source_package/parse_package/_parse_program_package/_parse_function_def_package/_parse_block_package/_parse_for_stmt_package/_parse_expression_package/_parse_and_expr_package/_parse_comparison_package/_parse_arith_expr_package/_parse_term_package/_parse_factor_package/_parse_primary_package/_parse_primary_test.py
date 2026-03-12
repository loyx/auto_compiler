# -*- coding: utf-8 -*-
"""
单元测试：_parse_primary 函数
测试 primary 表达式解析（标识符、字面量）
"""

import unittest
from typing import Dict, Any, List

# 相对导入被测模块
from ._parse_primary_src import _parse_primary


def _make_parser_state(
    tokens: List[Dict[str, Any]],
    pos: int = 0,
    filename: str = "test.c",
    error: str = ""
) -> Dict[str, Any]:
    """创建 parser_state 测试数据"""
    return {
        "tokens": tokens,
        "pos": pos,
        "filename": filename,
        "error": error
    }


def _make_token(
    token_type: str,
    value: str,
    line: int = 1,
    column: int = 1
) -> Dict[str, Any]:
    """创建 token 测试数据"""
    return {
        "type": token_type,
        "value": value,
        "line": line,
        "column": column
    }


class TestParsePrimary(unittest.TestCase):
    """_parse_primary 函数单元测试"""

    def test_parse_identifier_simple(self):
        """测试解析简单标识符"""
        tokens = [_make_token("IDENTIFIER", "x")]
        parser_state = _make_parser_state(tokens, pos=0)
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "x")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(result["children"], [])
        self.assertEqual(parser_state["pos"], 1)
        self.assertEqual(parser_state["error"], "")

    def test_parse_identifier_with_position(self):
        """测试解析带位置信息的标识符"""
        tokens = [_make_token("IDENTIFIER", "myVar", line=5, column=10)]
        parser_state = _make_parser_state(tokens, pos=0)
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "myVar")
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 10)
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_literal_number(self):
        """测试解析数字字面量"""
        tokens = [_make_token("LITERAL", "42")]
        parser_state = _make_parser_state(tokens, pos=0)
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "42")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 1)
        self.assertEqual(parser_state["error"], "")

    def test_parse_literal_string(self):
        """测试解析字符串字面量"""
        tokens = [_make_token("LITERAL", '"hello"')]
        parser_state = _make_parser_state(tokens, pos=0)
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], '"hello"')
        self.assertEqual(parser_state["pos"], 1)

    def test_parse_literal_with_position(self):
        """测试解析带位置信息的字面量"""
        tokens = [_make_token("LITERAL", "3.14", line=3, column=7)]
        parser_state = _make_parser_state(tokens, pos=0)
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "3.14")
        self.assertEqual(result["line"], 3)
        self.assertEqual(result["column"], 7)
        self.assertEqual(parser_state["pos"], 1)

    def test_empty_tokens_list(self):
        """测试空 tokens 列表"""
        tokens = []
        parser_state = _make_parser_state(tokens, pos=0)
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], "Unexpected end of input")
        self.assertEqual(parser_state["error"], "Unexpected end of input: expected primary")
        self.assertEqual(parser_state["pos"], 0)  # pos 不应改变

    def test_pos_at_end_of_tokens(self):
        """测试 pos 在 tokens 末尾"""
        tokens = [_make_token("IDENTIFIER", "x")]
        parser_state = _make_parser_state(tokens, pos=1)
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], "Unexpected end of input")
        self.assertEqual(parser_state["error"], "Unexpected end of input: expected primary")
        self.assertEqual(parser_state["pos"], 1)

    def test_pos_beyond_tokens_length(self):
        """测试 pos 超出 tokens 长度"""
        tokens = [_make_token("IDENTIFIER", "x")]
        parser_state = _make_parser_state(tokens, pos=5)
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], "Unexpected end of input")
        self.assertEqual(parser_state["error"], "Unexpected end of input: expected primary")

    def test_invalid_token_type_operator(self):
        """测试无效 token 类型（运算符）"""
        tokens = [_make_token("PLUS", "+")]
        parser_state = _make_parser_state(tokens, pos=0)
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], "Unexpected token '+'")
        self.assertIn("expected identifier or literal", parser_state["error"])
        self.assertEqual(parser_state["pos"], 0)  # pos 不应改变

    def test_invalid_token_type_parenthesis(self):
        """测试无效 token 类型（括号）"""
        tokens = [_make_token("LPAREN", "(")]
        parser_state = _make_parser_state(tokens, pos=0)
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], "Unexpected token '('")
        self.assertIn("expected identifier or literal", parser_state["error"])

    def test_invalid_token_type_keyword(self):
        """测试无效 token 类型（关键字）"""
        tokens = [_make_token("IF", "if")]
        parser_state = _make_parser_state(tokens, pos=0)
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], "Unexpected token 'if'")
        self.assertEqual(parser_state["pos"], 0)

    def test_multiple_tokens_only_consumes_one(self):
        """测试多个 tokens 时只消耗一个"""
        tokens = [
            _make_token("IDENTIFIER", "x"),
            _make_token("PLUS", "+"),
            _make_token("LITERAL", "5")
        ]
        parser_state = _make_parser_state(tokens, pos=0)
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "x")
        self.assertEqual(parser_state["pos"], 1)  # 只前进 1 位
        self.assertEqual(parser_state["error"], "")

    def test_parse_from_middle_position(self):
        """测试从中间位置开始解析"""
        tokens = [
            _make_token("PLUS", "+"),
            _make_token("IDENTIFIER", "y"),
            _make_token("MINUS", "-")
        ]
        parser_state = _make_parser_state(tokens, pos=1)
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "y")
        self.assertEqual(parser_state["pos"], 2)

    def test_error_preserves_existing_error(self):
        """测试错误情况下保留已有 error 字段（被覆盖）"""
        tokens = [_make_token("MULTI", "*")]
        parser_state = _make_parser_state(tokens, pos=0, error="previous error")
        
        result = _parse_primary(parser_state)
        
        # 新错误会覆盖旧错误
        self.assertIn("expected identifier or literal", parser_state["error"])
        self.assertNotEqual(parser_state["error"], "previous error")

    def test_literal_zero(self):
        """测试字面量 0"""
        tokens = [_make_token("LITERAL", "0")]
        parser_state = _make_parser_state(tokens, pos=0)
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "0")
        self.assertEqual(parser_state["pos"], 1)

    def test_identifier_underscore(self):
        """测试带下划线的标识符"""
        tokens = [_make_token("IDENTIFIER", "_private_var")]
        parser_state = _make_parser_state(tokens, pos=0)
        
        result = _parse_primary(parser_state)
        
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "_private_var")
        self.assertEqual(parser_state["pos"], 1)


if __name__ == "__main__":
    unittest.main()

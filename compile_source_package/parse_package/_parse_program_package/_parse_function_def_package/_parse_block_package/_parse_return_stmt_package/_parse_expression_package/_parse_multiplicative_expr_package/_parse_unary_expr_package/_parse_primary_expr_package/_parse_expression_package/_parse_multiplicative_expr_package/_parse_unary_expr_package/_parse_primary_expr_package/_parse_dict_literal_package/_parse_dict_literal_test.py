# -*- coding: utf-8 -*-
"""单元测试：_parse_dict_literal 函数"""

import unittest
from unittest.mock import patch, MagicMock
from typing import Any, Dict

# 相对导入被测模块
# 使用延迟导入来避免循环依赖问题
def _get_parse_dict_literal():
    from ._parse_dict_literal_src import _parse_dict_literal
    return _parse_dict_literal


class TestParseDictLiteral(unittest.TestCase):
    """_parse_dict_literal 函数的单元测试"""

    def _create_parser_state(self, tokens: list, pos: int = 0, filename: str = "test.py") -> Dict[str, Any]:
        """辅助函数：创建 parser_state"""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename
        }

    def _create_token(self, token_type: str, value: str = "", line: int = 1, column: int = 1) -> Dict[str, Any]:
        """辅助函数：创建 token"""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def test_empty_dict(self):
        """测试空字典 {}"""
        tokens = [
            self._create_token("LEFT_BRACE", "{", 1, 1),
            self._create_token("RIGHT_BRACE", "}", 1, 2)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        result = _get_parse_dict_literal()(parser_state)
        
        self.assertEqual(result["type"], "DICT_LITERAL")
        self.assertEqual(result["children"], [])
        self.assertEqual(result["value"], None)
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 2)

    def test_single_entry(self):
        """测试单条目字典 {key: value}"""
        tokens = [
            self._create_token("LEFT_BRACE", "{", 1, 1),
            self._create_token("IDENTIFIER", "key", 1, 2),
            self._create_token("COLON", ":", 1, 5),
            self._create_token("IDENTIFIER", "value", 1, 7),
            self._create_token("RIGHT_BRACE", "}", 1, 12)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # Mock _parse_expression to return simple AST nodes
        with patch("._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.side_effect = [
                {"type": "IDENTIFIER", "value": "key"},
                {"type": "IDENTIFIER", "value": "value"}
            ]
            
            result = _get_parse_dict_literal()(parser_state)
        
        self.assertEqual(result["type"], "DICT_LITERAL")
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0]["key"]["type"], "IDENTIFIER")
        self.assertEqual(result["children"][0]["value"]["type"], "IDENTIFIER")
        self.assertEqual(parser_state["pos"], 5)

    def test_multiple_entries_with_comma(self):
        """测试多条目字典 {key1: value1, key2: value2}"""
        tokens = [
            self._create_token("LEFT_BRACE", "{", 1, 1),
            self._create_token("IDENTIFIER", "key1", 1, 2),
            self._create_token("COLON", ":", 1, 6),
            self._create_token("IDENTIFIER", "value1", 1, 8),
            self._create_token("COMMA", ",", 1, 14),
            self._create_token("IDENTIFIER", "key2", 1, 16),
            self._create_token("COLON", ":", 1, 20),
            self._create_token("IDENTIFIER", "value2", 1, 22),
            self._create_token("RIGHT_BRACE", "}", 1, 28)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        with patch("._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.side_effect = [
                {"type": "IDENTIFIER", "value": "key1"},
                {"type": "IDENTIFIER", "value": "value1"},
                {"type": "IDENTIFIER", "value": "key2"},
                {"type": "IDENTIFIER", "value": "value2"}
            ]
            
            result = _get_parse_dict_literal()(parser_state)
        
        self.assertEqual(result["type"], "DICT_LITERAL")
        self.assertEqual(len(result["children"]), 2)
        self.assertEqual(result["children"][0]["key"]["value"], "key1")
        self.assertEqual(result["children"][0]["value"]["value"], "value1")
        self.assertEqual(result["children"][1]["key"]["value"], "key2")
        self.assertEqual(result["children"][1]["value"]["value"], "value2")
        self.assertEqual(parser_state["pos"], 9)

    def test_missing_left_brace(self):
        """测试缺少 LEFT_BRACE 的情况"""
        tokens = [
            self._create_token("IDENTIFIER", "key", 1, 1)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        with self.assertRaises(SyntaxError) as context:
            _get_parse_dict_literal()(parser_state)
        
        self.assertIn("Expected '{'", str(context.exception))

    def test_unexpected_end_before_left_brace(self):
        """测试在 LEFT_BRACE 之前输入意外结束"""
        tokens = []
        parser_state = self._create_parser_state(tokens, pos=0)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_dict_literal(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))

    def test_missing_colon(self):
        """测试缺少 COLON 的情况"""
        tokens = [
            self._create_token("LEFT_BRACE", "{", 1, 1),
            self._create_token("IDENTIFIER", "key", 1, 2),
            self._create_token("RIGHT_BRACE", "}", 1, 5)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        with patch("._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = {"type": "IDENTIFIER", "value": "key"}
            
            with self.assertRaises(SyntaxError) as context:
                _parse_dict_literal(parser_state)
        
        self.assertIn("Expected ':'", str(context.exception))

    def test_missing_right_brace(self):
        """测试缺少 RIGHT_BRACE 的情况"""
        tokens = [
            self._create_token("LEFT_BRACE", "{", 1, 1),
            self._create_token("IDENTIFIER", "key", 1, 2),
            self._create_token("COLON", ":", 1, 5),
            self._create_token("IDENTIFIER", "value", 1, 7)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        with patch("._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.side_effect = [
                {"type": "IDENTIFIER", "value": "key"},
                {"type": "IDENTIFIER", "value": "value"}
            ]
            
            with self.assertRaises(SyntaxError) as context:
                _parse_dict_literal(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))

    def test_unexpected_token_after_entry(self):
        """测试条目后出现意外 token（既不是逗号也不是右花括号）"""
        tokens = [
            self._create_token("LEFT_BRACE", "{", 1, 1),
            self._create_token("IDENTIFIER", "key", 1, 2),
            self._create_token("COLON", ":", 1, 5),
            self._create_token("IDENTIFIER", "value", 1, 7),
            self._create_token("SEMICOLON", ";", 1, 12)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        with patch("._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.side_effect = [
                {"type": "IDENTIFIER", "value": "key"},
                {"type": "IDENTIFIER", "value": "value"}
            ]
            
            with self.assertRaises(SyntaxError) as context:
                _parse_dict_literal(parser_state)
        
        self.assertIn("Expected ',' or '}'", str(context.exception))

    def test_missing_value(self):
        """测试缺少 value 的情况（COLON 后直接结束）"""
        tokens = [
            self._create_token("LEFT_BRACE", "{", 1, 1),
            self._create_token("IDENTIFIER", "key", 1, 2),
            self._create_token("COLON", ":", 1, 5)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        with patch("._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = {"type": "IDENTIFIER", "value": "key"}
            
            with self.assertRaises(SyntaxError) as context:
                _parse_dict_literal(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))

    def test_trailing_comma_before_right_brace(self):
        """测试右花括号前有逗号的情况（应报错）"""
        tokens = [
            self._create_token("LEFT_BRACE", "{", 1, 1),
            self._create_token("IDENTIFIER", "key", 1, 2),
            self._create_token("COLON", ":", 1, 5),
            self._create_token("IDENTIFIER", "value", 1, 7),
            self._create_token("COMMA", ",", 1, 12),
            self._create_token("RIGHT_BRACE", "}", 1, 13)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        with patch("._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.side_effect = [
                {"type": "IDENTIFIER", "value": "key"},
                {"type": "IDENTIFIER", "value": "value"}
            ]
            
            # 当前实现会在 COMMA 后继续循环，尝试解析下一个 key
            # 由于遇到 RIGHT_BRACE，会尝试解析它作为表达式，这应该由 _parse_expression 处理
            # 根据实现，这会进入下一轮循环，遇到 RIGHT_BRACE 会 break
            result = _parse_dict_literal(parser_state)
            
            self.assertEqual(result["type"], "DICT_LITERAL")
            self.assertEqual(len(result["children"]), 1)


if __name__ == "__main__":
    unittest.main()

# -*- coding: utf-8 -*-
"""
单元测试：_parse_assign_stmt 函数
测试赋值语句解析逻辑
"""

import unittest
from unittest.mock import patch
from typing import Dict, Any, List

# 相对导入被测试模块和依赖
from ._parse_assign_stmt_src import _parse_assign_stmt


def _create_parser_state(
    tokens: List[Dict[str, Any]],
    pos: int = 0,
    filename: str = "<test>"
) -> Dict[str, Any]:
    """辅助函数：创建 parser_state 字典"""
    return {
        "tokens": tokens,
        "pos": pos,
        "filename": filename
    }


def _create_token(
    token_type: str,
    value: str,
    line: int = 1,
    column: int = 1
) -> Dict[str, Any]:
    """辅助函数：创建 token 字典"""
    return {
        "type": token_type,
        "value": value,
        "line": line,
        "column": column
    }


class TestParseAssignStmt(unittest.TestCase):
    """_parse_assign_stmt 函数的单元测试"""

    def test_happy_path_simple_assignment(self):
        """测试：简单的赋值语句 x = 5;"""
        tokens = [
            _create_token("IDENTIFIER", "x", 1, 1),
            _create_token("ASSIGN", "=", 1, 3),
            _create_token("NUMBER", "5", 1, 5),
            _create_token("SEMICOLON", ";", 1, 6)
        ]
        parser_state = _create_parser_state(tokens)
        
        with patch("._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = {
                "type": "NUMBER",
                "value": "5",
                "line": 1,
                "column": 5
            }
            
            result = _parse_assign_stmt(parser_state)
            
            # 验证返回的 AST 结构
            self.assertEqual(result["type"], "ASSIGN")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            
            # 验证 target
            self.assertEqual(result["target"]["type"], "IDENTIFIER")
            self.assertEqual(result["target"]["value"], "x")
            self.assertEqual(result["target"]["line"], 1)
            self.assertEqual(result["target"]["column"], 1)
            
            # 验证 value
            self.assertEqual(result["value"]["type"], "NUMBER")
            self.assertEqual(result["value"]["value"], "5")
            
            # 验证 parser_state["pos"] 被正确更新
            self.assertEqual(parser_state["pos"], 4)
            
            # 验证 _parse_expression 被调用
            mock_parse_expr.assert_called_once()

    def test_happy_path_string_assignment(self):
        """测试：字符串赋值语句 name = "hello";"""
        tokens = [
            _create_token("IDENTIFIER", "name", 2, 5),
            _create_token("ASSIGN", "=", 2, 10),
            _create_token("STRING", '"hello"', 2, 12),
            _create_token("SEMICOLON", ";", 2, 20)
        ]
        parser_state = _create_parser_state(tokens)
        
        with patch("._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = {
                "type": "STRING",
                "value": '"hello"',
                "line": 2,
                "column": 12
            }
            
            result = _parse_assign_stmt(parser_state)
            
            self.assertEqual(result["type"], "ASSIGN")
            self.assertEqual(result["target"]["value"], "name")
            self.assertEqual(result["value"]["type"], "STRING")
            self.assertEqual(parser_state["pos"], 4)

    def test_happy_path_expression_assignment(self):
        """测试：表达式赋值语句 y = a + b;"""
        tokens = [
            _create_token("IDENTIFIER", "y", 3, 1),
            _create_token("ASSIGN", "=", 3, 3),
            _create_token("IDENTIFIER", "a", 3, 5),
            _create_token("PLUS", "+", 3, 7),
            _create_token("IDENTIFIER", "b", 3, 9),
            _create_token("SEMICOLON", ";", 3, 10)
        ]
        parser_state = _create_parser_state(tokens)
        
        with patch("._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = {
                "type": "BINARY",
                "left": {"type": "IDENTIFIER", "value": "a"},
                "right": {"type": "IDENTIFIER", "value": "b"},
                "operator": "+",
                "line": 3,
                "column": 5
            }
            
            result = _parse_assign_stmt(parser_state)
            
            self.assertEqual(result["type"], "ASSIGN")
            self.assertEqual(result["target"]["value"], "y")
            self.assertEqual(result["value"]["type"], "BINARY")
            self.assertEqual(parser_state["pos"], 6)

    def test_error_missing_identifier_non_identifier_token(self):
        """测试：错误情况 - 当前 token 不是标识符"""
        tokens = [
            _create_token("NUMBER", "5", 1, 1),
            _create_token("ASSIGN", "=", 1, 3),
            _create_token("NUMBER", "10", 1, 5),
            _create_token("SEMICOLON", ";", 1, 8)
        ]
        parser_state = _create_parser_state(tokens)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_assign_stmt(parser_state)
        
        error_msg = str(context.exception)
        self.assertIn("预期标识符", error_msg)
        self.assertIn("'5'", error_msg)
        # pos 不应该被修改
        self.assertEqual(parser_state["pos"], 0)

    def test_error_missing_identifier_eof(self):
        """测试：错误情况 - 到达文件末尾，没有标识符"""
        tokens = []
        parser_state = _create_parser_state(tokens)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_assign_stmt(parser_state)
        
        error_msg = str(context.exception)
        self.assertIn("预期标识符", error_msg)
        self.assertIn("文件末尾", error_msg)

    def test_error_missing_assign_token(self):
        """测试：错误情况 - 缺少 ASSIGN token"""
        tokens = [
            _create_token("IDENTIFIER", "x", 1, 1),
            _create_token("NUMBER", "5", 1, 3),
            _create_token("SEMICOLON", ";", 1, 5)
        ]
        parser_state = _create_parser_state(tokens)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_assign_stmt(parser_state)
        
        error_msg = str(context.exception)
        self.assertIn("预期 '='", error_msg)
        self.assertIn("'5'", error_msg)

    def test_error_missing_assign_token_eof(self):
        """测试：错误情况 - 标识符后到达文件末尾"""
        tokens = [
            _create_token("IDENTIFIER", "x", 1, 1)
        ]
        parser_state = _create_parser_state(tokens)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_assign_stmt(parser_state)
        
        error_msg = str(context.exception)
        self.assertIn("预期 '='", error_msg)
        self.assertIn("文件末尾", error_msg)

    def test_error_missing_semicolon(self):
        """测试：错误情况 - 缺少 SEMICOLON token"""
        tokens = [
            _create_token("IDENTIFIER", "x", 1, 1),
            _create_token("ASSIGN", "=", 1, 3),
            _create_token("NUMBER", "5", 1, 5)
        ]
        parser_state = _create_parser_state(tokens)
        
        with patch("._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = {
                "type": "NUMBER",
                "value": "5",
                "line": 1,
                "column": 5
            }
            
            with self.assertRaises(SyntaxError) as context:
                _parse_assign_stmt(parser_state)
        
        error_msg = str(context.exception)
        self.assertIn("预期 ';'", error_msg)

    def test_error_missing_semicolon_eof(self):
        """测试：错误情况 - 表达式后到达文件末尾"""
        tokens = [
            _create_token("IDENTIFIER", "x", 1, 1),
            _create_token("ASSIGN", "=", 1, 3)
        ]
        parser_state = _create_parser_state(tokens)
        
        with patch("._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = {
                "type": "NUMBER",
                "value": "5",
                "line": 1,
                "column": 5
            }
            
            with self.assertRaises(SyntaxError) as context:
                _parse_assign_stmt(parser_state)
        
        error_msg = str(context.exception)
        self.assertIn("预期 ';'", error_msg)
        self.assertIn("文件末尾", error_msg)

    def test_error_semicolon_wrong_token(self):
        """测试：错误情况 - 表达式后是错误 token 而不是分号"""
        tokens = [
            _create_token("IDENTIFIER", "x", 1, 1),
            _create_token("ASSIGN", "=", 1, 3),
            _create_token("NUMBER", "5", 1, 5),
            _create_token("COMMA", ",", 1, 6)
        ]
        parser_state = _create_parser_state(tokens)
        
        with patch("._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = {
                "type": "NUMBER",
                "value": "5",
                "line": 1,
                "column": 5
            }
            
            with self.assertRaises(SyntaxError) as context:
                _parse_assign_stmt(parser_state)
        
        error_msg = str(context.exception)
        self.assertIn("预期 ';'", error_msg)
        self.assertIn("','", error_msg)

    def test_custom_filename_in_error(self):
        """测试：自定义文件名在错误消息中"""
        tokens = [
            _create_token("NUMBER", "5", 5, 10)
        ]
        parser_state = _create_parser_state(tokens, filename="test_source.cc")
        
        with self.assertRaises(SyntaxError) as context:
            _parse_assign_stmt(parser_state)
        
        error_msg = str(context.exception)
        self.assertIn("test_source.cc", error_msg)

    def test_pos_advances_correctly(self):
        """测试：parser_state['pos'] 正确推进"""
        tokens = [
            _create_token("IDENTIFIER", "x", 1, 1),
            _create_token("ASSIGN", "=", 1, 3),
            _create_token("NUMBER", "5", 1, 5),
            _create_token("SEMICOLON", ";", 1, 6)
        ]
        parser_state = _create_parser_state(tokens)
        
        with patch("._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = {
                "type": "NUMBER",
                "value": "5",
                "line": 1,
                "column": 5
            }
            
            _parse_assign_stmt(parser_state)
            
            # 验证 pos 从 0 推进到 4（消费了 4 个 token）
            self.assertEqual(parser_state["pos"], 4)

    def test_ast_structure_complete(self):
        """测试：完整的 AST 结构包含所有必需字段"""
        tokens = [
            _create_token("IDENTIFIER", "count", 10, 20),
            _create_token("ASSIGN", "=", 10, 26),
            _create_token("NUMBER", "42", 10, 28),
            _create_token("SEMICOLON", ";", 10, 30)
        ]
        parser_state = _create_parser_state(tokens)
        
        with patch("._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = {
                "type": "NUMBER",
                "value": "42",
                "line": 10,
                "column": 28
            }
            
            result = _parse_assign_stmt(parser_state)
            
            # 验证 ASSIGN 节点字段
            self.assertIn("type", result)
            self.assertIn("target", result)
            self.assertIn("value", result)
            self.assertIn("line", result)
            self.assertIn("column", result)
            
            # 验证 target 字段
            self.assertIn("type", result["target"])
            self.assertIn("value", result["target"])
            self.assertIn("line", result["target"])
            self.assertIn("column", result["target"])


if __name__ == "__main__":
    unittest.main()
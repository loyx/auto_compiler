import unittest
from unittest.mock import patch
from typing import Dict, Any

from ._parse_expression_src import _parse_expression


class TestParseExpression(unittest.TestCase):
    """测试 _parse_expression 函数"""
    
    @patch('_parse_expression_package._parse_or_expr_package._parse_or_expr_src._parse_or_expr')
    def test_parse_expression_delegates_to_or_expr(self, mock_or_expr):
        """测试 _parse_expression 委托给 _parse_or_expr"""
        mock_parser_state = {
            "tokens": [{"type": "NUMBER", "value": "1", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test.cc"
        }
        mock_ast: Dict[str, Any] = {
            "type": "BINARY_OP",
            "operator": "PLUS",
            "left": {"type": "LITERAL", "value": 1},
            "right": {"type": "LITERAL", "value": 2}
        }
        mock_or_expr.return_value = mock_ast
        
        result = _parse_expression(mock_parser_state)
        
        mock_or_expr.assert_called_once_with(mock_parser_state)
        self.assertEqual(result, mock_ast)
    
    @patch('._parse_or_expr_package._parse_or_expr_src._parse_or_expr')
    def test_parse_expression_with_empty_tokens(self, mock_or_expr):
        """测试空 tokens 列表"""
        mock_parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.cc"
        }
        mock_or_expr.return_value = {"type": "LITERAL", "value": None}
        
        result = _parse_expression(mock_parser_state)
        
        mock_or_expr.assert_called_once()
        self.assertIsNotNone(result)
    
    @patch('._parse_or_expr_package._parse_or_expr_src._parse_or_expr')
    def test_parse_expression_preserves_state_reference(self, mock_or_expr):
        """测试 parser_state 对象引用被传递"""
        mock_parser_state = {
            "tokens": [{"type": "NUMBER", "value": "42", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "main.cc"
        }
        mock_or_expr.return_value = {"type": "LITERAL", "value": 42}
        
        _parse_expression(mock_parser_state)
        
        # 验证传入的是同一个 parser_state 对象
        call_args = mock_or_expr.call_args[0][0]
        self.assertIs(call_args, mock_parser_state)
    
    @patch('._parse_or_expr_package._parse_or_expr_src._parse_or_expr')
    def test_parse_expression_with_complex_expression(self, mock_or_expr):
        """测试复杂表达式解析"""
        mock_parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 2},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 3},
                {"type": "STAR", "value": "*", "line": 1, "column": 4},
                {"type": "NUMBER", "value": "3", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "expr.cc"
        }
        expected_ast = {
            "type": "BINARY_OP",
            "operator": "PLUS",
            "left": {"type": "LITERAL", "value": 1},
            "right": {
                "type": "BINARY_OP",
                "operator": "STAR",
                "left": {"type": "LITERAL", "value": 2},
                "right": {"type": "LITERAL", "value": 3}
            }
        }
        mock_or_expr.return_value = expected_ast
        
        result = _parse_expression(mock_parser_state)
        
        mock_or_expr.assert_called_once_with(mock_parser_state)
        self.assertEqual(result, expected_ast)
    
    @patch('._parse_or_expr_package._parse_or_expr_src._parse_or_expr')
    def test_parse_expression_error_propagation(self, mock_or_expr):
        """测试错误从子函数传播"""
        mock_parser_state = {
            "tokens": [{"type": "INVALID", "value": "?", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "error.cc"
        }
        mock_or_expr.side_effect = SyntaxError("Invalid syntax")
        
        with self.assertRaises(SyntaxError):
            _parse_expression(mock_parser_state)
    
    @patch('._parse_or_expr_package._parse_or_expr_src._parse_or_expr')
    def test_parse_expression_with_identifier(self, mock_or_expr):
        """测试标识符表达式"""
        mock_parser_state = {
            "tokens": [{"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test.cc"
        }
        mock_ast = {"type": "IDENTIFIER", "name": "x", "line": 1, "column": 1}
        mock_or_expr.return_value = mock_ast
        
        result = _parse_expression(mock_parser_state)
        
        self.assertEqual(result, mock_ast)
    
    @patch('._parse_or_expr_package._parse_or_expr_src._parse_or_expr')
    def test_parse_expression_with_pos_update(self, mock_or_expr):
        """测试 parser_state 的 pos 被更新"""
        mock_parser_state = {
            "tokens": [{"type": "NUMBER", "value": "1", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test.cc"
        }
        
        def update_pos(state):
            state["pos"] = 1
            return {"type": "LITERAL", "value": 1}
        
        mock_or_expr.side_effect = update_pos
        
        result = _parse_expression(mock_parser_state)
        
        self.assertEqual(mock_parser_state["pos"], 1)
        self.assertEqual(result["type"], "LITERAL")


if __name__ == "__main__":
    unittest.main()

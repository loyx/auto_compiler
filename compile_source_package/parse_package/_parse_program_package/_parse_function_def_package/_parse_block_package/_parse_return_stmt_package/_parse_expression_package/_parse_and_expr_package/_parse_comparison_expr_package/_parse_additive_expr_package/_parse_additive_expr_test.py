#!/usr/bin/env python3
"""单元测试文件：_parse_additive_expr"""

import unittest
from unittest.mock import patch

from ._parse_additive_expr_src import _parse_additive_expr


class TestParseAdditiveExpr(unittest.TestCase):
    """_parse_additive_expr 函数测试类"""
    
    def test_single_expression_no_operator(self):
        """测试：无加法运算符时直接返回乘法表达式结果"""
        parser_state = {
            "tokens": [{"type": "NUMBER", "value": "5", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test.py"
        }
        
        mock_result = {"type": "LITERAL", "value": "5", "line": 1, "column": 1}
        
        with patch("_parse_additive_expr_src._parse_multiplicative_expr") as mock_parse_mult:
            mock_parse_mult.return_value = mock_result
            
            result = _parse_additive_expr(parser_state)
            
            self.assertEqual(result, mock_result)
            mock_parse_mult.assert_called_once_with(parser_state)
    
    def test_single_addition(self):
        """测试：单个加法表达式 a + b"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "5", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "3", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        left_operand = {"type": "LITERAL", "value": "5", "line": 1, "column": 1}
        right_operand = {"type": "LITERAL", "value": "3", "line": 1, "column": 5}
        
        with patch("_parse_additive_expr_src._parse_multiplicative_expr") as mock_parse_mult:
            mock_parse_mult.side_effect = [left_operand, right_operand]
            
            result = _parse_additive_expr(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "+")
            self.assertEqual(result["children"], [left_operand, right_operand])
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 3)
    
    def test_single_subtraction(self):
        """测试：单个减法表达式 a - b"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "10", "line": 2, "column": 1},
                {"type": "MINUS", "value": "-", "line": 2, "column": 4},
                {"type": "NUMBER", "value": "4", "line": 2, "column": 6}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        left_operand = {"type": "LITERAL", "value": "10", "line": 2, "column": 1}
        right_operand = {"type": "LITERAL", "value": "4", "line": 2, "column": 6}
        
        with patch("_parse_additive_expr_src._parse_multiplicative_expr") as mock_parse_mult:
            mock_parse_mult.side_effect = [left_operand, right_operand]
            
            result = _parse_additive_expr(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "-")
            self.assertEqual(result["children"], [left_operand, right_operand])
            self.assertEqual(result["line"], 2)
            self.assertEqual(result["column"], 4)
    
    def test_multiple_additive_operations_left_associative(self):
        """测试：多个加法/减法表达式 a + b - c（左结合）"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "5", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "3", "line": 1, "column": 5},
                {"type": "MINUS", "value": "-", "line": 1, "column": 7},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 9}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        first = {"type": "LITERAL", "value": "5", "line": 1, "column": 1}
        second = {"type": "LITERAL", "value": "3", "line": 1, "column": 5}
        third = {"type": "LITERAL", "value": "2", "line": 1, "column": 9}
        
        with patch("_parse_additive_expr_src._parse_multiplicative_expr") as mock_parse_mult:
            mock_parse_mult.side_effect = [first, second, third]
            
            result = _parse_additive_expr(parser_state)
            
            # 验证左结合性：(5 + 3) - 2
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "-")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 7)
            
            # 左子节点应该是 (5 + 3)
            left_child = result["children"][0]
            self.assertEqual(left_child["type"], "BINARY_OP")
            self.assertEqual(left_child["value"], "+")
            self.assertEqual(left_child["children"], [first, second])
            
            # 右子节点应该是 2
            right_child = result["children"][1]
            self.assertEqual(right_child, third)
    
    def test_mixed_addition_subtraction(self):
        """测试：混合加法和减法 a - b + c"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "MINUS", "value": "-", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
                {"type": "PLUS", "value": "+", "line": 1, "column": 7},
                {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 9}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        first = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        second = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
        third = {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 9}
        
        with patch("_parse_additive_expr_src._parse_multiplicative_expr") as mock_parse_mult:
            mock_parse_mult.side_effect = [first, second, third]
            
            result = _parse_additive_expr(parser_state)
            
            # 验证左结合性：(a - b) + c
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "+")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 7)
            
            # 左子节点应该是 (a - b)
            left_child = result["children"][0]
            self.assertEqual(left_child["type"], "BINARY_OP")
            self.assertEqual(left_child["value"], "-")
            self.assertEqual(left_child["children"], [first, second])
            
            # 右子节点应该是 c
            right_child = result["children"][1]
            self.assertEqual(right_child, third)
    
    def test_empty_tokens(self):
        """测试：空 tokens 列表"""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }
        
        mock_result = {"type": "EMPTY", "value": None}
        
        with patch("_parse_additive_expr_src._parse_multiplicative_expr") as mock_parse_mult:
            mock_parse_mult.return_value = mock_result
            
            result = _parse_additive_expr(parser_state)
            
            self.assertEqual(result, mock_result)
            mock_parse_mult.assert_called_once_with(parser_state)
    
    def test_position_at_end(self):
        """测试：pos 已在 tokens 末尾"""
        parser_state = {
            "tokens": [{"type": "NUMBER", "value": "5", "line": 1, "column": 1}],
            "pos": 1,
            "filename": "test.py"
        }
        
        mock_result = {"type": "LITERAL", "value": "5", "line": 1, "column": 1}
        
        with patch("_parse_additive_expr_src._parse_multiplicative_expr") as mock_parse_mult:
            mock_parse_mult.return_value = mock_result
            
            result = _parse_additive_expr(parser_state)
            
            self.assertEqual(result, mock_result)
    
    def test_parser_state_position_updated(self):
        """测试：解析后 pos 指针正确更新"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "5", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "3", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        left_operand = {"type": "LITERAL", "value": "5", "line": 1, "column": 1}
        right_operand = {"type": "LITERAL", "value": "3", "line": 1, "column": 5}
        
        with patch("_parse_additive_expr_src._parse_multiplicative_expr") as mock_parse_mult:
            mock_parse_mult.side_effect = [left_operand, right_operand]
            
            result = _parse_additive_expr(parser_state)
            
            self.assertIsNotNone(result)
            self.assertEqual(parser_state["pos"], 2)
    
    def test_parse_multiplicative_expr_call_count(self):
        """测试：_parse_multiplicative_expr 调用次数正确"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 5},
                {"type": "MINUS", "value": "-", "line": 1, "column": 7},
                {"type": "NUMBER", "value": "3", "line": 1, "column": 9},
                {"type": "PLUS", "value": "+", "line": 1, "column": 11},
                {"type": "NUMBER", "value": "4", "line": 1, "column": 13}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        operands = [
            {"type": "LITERAL", "value": "1", "line": 1, "column": 1},
            {"type": "LITERAL", "value": "2", "line": 1, "column": 5},
            {"type": "LITERAL", "value": "3", "line": 1, "column": 9},
            {"type": "LITERAL", "value": "4", "line": 1, "column": 13}
        ]
        
        with patch("_parse_additive_expr_src._parse_multiplicative_expr") as mock_parse_mult:
            mock_parse_mult.side_effect = operands
            
            result = _parse_additive_expr(parser_state)
            
            self.assertEqual(mock_parse_mult.call_count, 4)
    
    def test_ast_node_structure(self):
        """测试：AST 节点结构完整性"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 5, "column": 10},
                {"type": "PLUS", "value": "+", "line": 5, "column": 12},
                {"type": "NUMBER", "value": "100", "line": 5, "column": 14}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        left_operand = {"type": "IDENTIFIER", "value": "x", "line": 5, "column": 10}
        right_operand = {"type": "LITERAL", "value": "100", "line": 5, "column": 14}
        
        with patch("_parse_additive_expr_src._parse_multiplicative_expr") as mock_parse_mult:
            mock_parse_mult.side_effect = [left_operand, right_operand]
            
            result = _parse_additive_expr(parser_state)
            
            self.assertIn("type", result)
            self.assertIn("value", result)
            self.assertIn("children", result)
            self.assertIn("line", result)
            self.assertIn("column", result)
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertIsInstance(result["children"], list)
            self.assertEqual(len(result["children"]), 2)


if __name__ == "__main__":
    unittest.main()

# === std / third-party imports ===
import unittest
import sys
import os
from typing import Any, Dict
from unittest.mock import patch, MagicMock

# Get the directory of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Mock the dependency before importing the module
mock_comparison_expr = MagicMock()
mock_comparison_expr.return_value = {
    "type": "COMPARISON",
    "value": "==",
    "children": [],
    "line": 1,
    "column": 0
}

# Patch the import before importing _parse_and_expr_src
sys.modules['_parse_comparison_expr_package'] = MagicMock()
sys.modules['_parse_comparison_expr_package._parse_comparison_expr_src'] = MagicMock()
sys.modules['_parse_comparison_expr_package._parse_comparison_expr_src._parse_comparison_expr'] = mock_comparison_expr

# === relative import for tested module ===
from _parse_and_expr_src import _parse_and_expr

# === ADT defines ===
Token = Dict[str, Any]
AST = Dict[str, Any]
ParserState = Dict[str, Any]

# Patch target path for _parse_comparison_expr
PATCH_TARGET = '_parse_comparison_expr_package._parse_comparison_expr_src._parse_comparison_expr'

# === Test Cases ===
class TestParseAndExpr(unittest.TestCase):
    """测试 _parse_and_expr 函数解析 AND 表达式（&& 运算符）"""
    
    def test_single_comparison_expr_no_and(self):
        """测试：没有 && 运算符，仅单个比较表达式"""
        mock_comparison = MagicMock()
        expected_ast = {
            "type": "COMPARISON",
            "value": "==",
            "children": [],
            "line": 1,
            "column": 0
        }
        mock_comparison.return_value = expected_ast
        
        tokens = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 0},
            {"type": "EQ", "value": "==", "line": 1, "column": 2},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch("._parse_comparison_expr_package._parse_comparison_expr_src._parse_comparison_expr", mock_comparison):
            result = _parse_and_expr(parser_state)
        
        self.assertEqual(result, expected_ast)
        mock_comparison.assert_called_once()
        self.assertEqual(parser_state["pos"], 0)
    
    def test_single_and_operator(self):
        """测试：单个 && 运算符连接两个比较表达式"""
        mock_comparison = MagicMock()
        left_expr = {
            "type": "COMPARISON",
            "value": ">",
            "children": [],
            "line": 1,
            "column": 0
        }
        right_expr = {
            "type": "COMPARISON",
            "value": "<",
            "children": [],
            "line": 1,
            "column": 10
        }
        mock_comparison.side_effect = [left_expr, right_expr]
        
        tokens = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 0},
            {"type": "GT", "value": ">", "line": 1, "column": 2},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 4},
            {"type": "AND", "value": "&&", "line": 1, "column": 6},
            {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 10},
            {"type": "LT", "value": "<", "line": 1, "column": 12},
            {"type": "IDENTIFIER", "value": "d", "line": 1, "column": 14}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch("._parse_comparison_expr_package._parse_comparison_expr_src._parse_comparison_expr", mock_comparison):
            result = _parse_and_expr(parser_state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "&&")
        self.assertEqual(len(result["children"]), 2)
        self.assertEqual(result["children"][0], left_expr)
        self.assertEqual(result["children"][1], right_expr)
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 6)
        self.assertEqual(mock_comparison.call_count, 2)
    
    def test_multiple_and_operators_left_associative(self):
        """测试：多个 && 运算符，验证左结合性"""
        mock_comparison = MagicMock()
        expr1 = {"type": "COMPARISON", "value": "==", "children": [], "line": 1, "column": 0}
        expr2 = {"type": "COMPARISON", "value": "!=", "children": [], "line": 1, "column": 10}
        expr3 = {"type": "COMPARISON", "value": ">=", "children": [], "line": 1, "column": 20}
        mock_comparison.side_effect = [expr1, expr2, expr3]
        
        tokens = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 0},
            {"type": "AND", "value": "&&", "line": 1, "column": 5},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 10},
            {"type": "AND", "value": "&&", "line": 1, "column": 15},
            {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 20}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch("._parse_comparison_expr_package._parse_comparison_expr_src._parse_comparison_expr", mock_comparison):
            result = _parse_and_expr(parser_state)
        
        # 左结合：(a && b) && c
        # 结果应该是：BINARY_OP(&&, BINARY_OP(&&, expr1, expr2), expr3)
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "&&")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 15)  # 第二个 && 的位置
        
        # 左子节点应该是第一个 && 的结果
        left_child = result["children"][0]
        self.assertEqual(left_child["type"], "BINARY_OP")
        self.assertEqual(left_child["value"], "&&")
        self.assertEqual(left_child["column"], 5)  # 第一个 && 的位置
        self.assertEqual(left_child["children"][0], expr1)
        self.assertEqual(left_child["children"][1], expr2)
        
        # 右子节点应该是第三个表达式
        self.assertEqual(result["children"][1], expr3)
        self.assertEqual(mock_comparison.call_count, 3)
    
    def test_empty_tokens(self):
        """测试：空 tokens 列表"""
        mock_comparison = MagicMock()
        empty_expr = {"type": "EMPTY", "value": None, "children": [], "line": 0, "column": 0}
        mock_comparison.return_value = empty_expr
        
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch("._parse_comparison_expr_package._parse_comparison_expr_src._parse_comparison_expr", mock_comparison):
            result = _parse_and_expr(parser_state)
        
        self.assertEqual(result, empty_expr)
        mock_comparison.assert_called_once()
    
    def test_pos_at_end_of_tokens(self):
        """测试：pos 已经在 tokens 末尾"""
        mock_comparison = MagicMock()
        expr = {"type": "COMPARISON", "value": "==", "children": [], "line": 1, "column": 0}
        mock_comparison.return_value = expr
        
        tokens = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 0}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 1,  # pos 已经在末尾
            "filename": "test.c"
        }
        
        with patch("._parse_comparison_expr_package._parse_comparison_expr_src._parse_comparison_expr", mock_comparison):
            result = _parse_and_expr(parser_state)
        
        self.assertEqual(result, expr)
        mock_comparison.assert_called_once()
    
    def test_and_at_end_no_right_operand(self):
        """测试：&& 在末尾，没有右操作数"""
        mock_comparison = MagicMock()
        left_expr = {"type": "COMPARISON", "value": ">", "children": [], "line": 1, "column": 0}
        right_expr = {"type": "COMPARISON", "value": "==", "children": [], "line": 1, "column": 10}
        mock_comparison.side_effect = [left_expr, right_expr]
        
        tokens = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 0},
            {"type": "AND", "value": "&&", "line": 1, "column": 5}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch("._parse_comparison_expr_package._parse_comparison_expr_src._parse_comparison_expr", mock_comparison):
            result = _parse_and_expr(parser_state)
        
        # && 后没有内容，_parse_comparison_expr 会返回某种默认值
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "&&")
        self.assertEqual(result["children"][0], left_expr)
        self.assertEqual(mock_comparison.call_count, 2)
    
    def test_non_and_token_after_first_expr(self):
        """测试：第一个表达式后是非 && 运算符"""
        mock_comparison = MagicMock()
        expr = {"type": "COMPARISON", "value": "==", "children": [], "line": 1, "column": 0}
        mock_comparison.return_value = expr
        
        tokens = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 0},
            {"type": "PLUS", "value": "+", "line": 1, "column": 2},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 4}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch("._parse_comparison_expr_package._parse_comparison_expr_src._parse_comparison_expr", mock_comparison):
            result = _parse_and_expr(parser_state)
        
        self.assertEqual(result, expr)
        mock_comparison.assert_called_once()
        self.assertEqual(parser_state["pos"], 0)  # pos 不应该改变
    
    def test_and_token_with_line_column_info(self):
        """测试：&& 运算符的行号列号信息正确传递"""
        mock_comparison = MagicMock()
        left_expr = {"type": "COMPARISON", "value": "==", "children": [], "line": 5, "column": 10}
        right_expr = {"type": "COMPARISON", "value": "!=", "children": [], "line": 5, "column": 25}
        mock_comparison.side_effect = [left_expr, right_expr]
        
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 5, "column": 10},
            {"type": "AND", "value": "&&", "line": 5, "column": 15},
            {"type": "IDENTIFIER", "value": "y", "line": 5, "column": 25}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch("._parse_comparison_expr_package._parse_comparison_expr_src._parse_comparison_expr", mock_comparison):
            result = _parse_and_expr(parser_state)
        
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 15)
        self.assertEqual(result["value"], "&&")
    
    def test_pos_advances_correctly(self):
        """测试：pos 在解析 && 后正确前进"""
        mock_comparison = MagicMock()
        expr = {"type": "COMPARISON", "value": "==", "children": [], "line": 1, "column": 0}
        mock_comparison.return_value = expr
        
        tokens = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 0},
            {"type": "AND", "value": "&&", "line": 1, "column": 2},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch("._parse_comparison_expr_package._parse_comparison_expr_src._parse_comparison_expr", mock_comparison):
            result = _parse_and_expr(parser_state)
        
        # 解析完 && 后，pos 应该前进到 2（&& 之后的位置）
        self.assertEqual(parser_state["pos"], 2)


# === Test Runner ===
if __name__ == "__main__":
    unittest.main()

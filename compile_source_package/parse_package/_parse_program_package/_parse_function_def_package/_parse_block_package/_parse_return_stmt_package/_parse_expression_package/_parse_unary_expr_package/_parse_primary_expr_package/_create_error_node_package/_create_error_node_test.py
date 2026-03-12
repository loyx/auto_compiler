# -*- coding: utf-8 -*-
"""
单元测试：_create_error_node 函数
测试文件路径：/Users/loyx/projects/autoapp_workspace/workspace/projects/cc/files/main_package/compile_source_package/parse_package/_parse_program_package/_parse_function_def_package/_parse_block_package/_parse_return_stmt_package/_parse_expression_package/_parse_unary_expr_package/_parse_primary_expr_package/_create_error_node_package/test_create_error_node.py
"""

import unittest
from ._create_error_node_src import _create_error_node


class TestCreateErrorNode(unittest.TestCase):
    """测试 _create_error_node 函数"""

    def test_valid_pos_with_line_column(self):
        """测试：pos 有效，token 包含 line 和 column"""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 5, "column": 10},
            {"type": "OPERATOR", "value": "+", "line": 5, "column": 12},
        ]
        result = _create_error_node(0, tokens)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertIsNone(result["value"])
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 10)
        self.assertEqual(result["children"], [])

    def test_valid_pos_last_token(self):
        """测试：pos 指向最后一个 token"""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            {"type": "OPERATOR", "value": "+", "line": 2, "column": 5},
        ]
        result = _create_error_node(1, tokens)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 5)

    def test_pos_out_of_bounds(self):
        """测试：pos 超出 tokens 范围"""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 5, "column": 10},
        ]
        result = _create_error_node(5, tokens)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["line"], 0)
        self.assertEqual(result["column"], 0)

    def test_pos_equals_length(self):
        """测试：pos 等于 tokens 长度（边界情况）"""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 3, "column": 7},
        ]
        result = _create_error_node(1, tokens)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["line"], 0)
        self.assertEqual(result["column"], 0)

    def test_empty_tokens(self):
        """测试：tokens 为空列表"""
        tokens = []
        result = _create_error_node(0, tokens)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["line"], 0)
        self.assertEqual(result["column"], 0)
        self.assertEqual(result["children"], [])

    def test_token_missing_line_column(self):
        """测试：token 缺少 line 和 column 字段"""
        tokens = [
            {"type": "IDENTIFIER", "value": "x"},
        ]
        result = _create_error_node(0, tokens)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["line"], 0)
        self.assertEqual(result["column"], 0)

    def test_token_missing_line_only(self):
        """测试：token 缺少 line 字段但有 column"""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "column": 15},
        ]
        result = _create_error_node(0, tokens)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["line"], 0)
        self.assertEqual(result["column"], 15)

    def test_token_missing_column_only(self):
        """测试：token 缺少 column 字段但有 line"""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 20},
        ]
        result = _create_error_node(0, tokens)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["line"], 20)
        self.assertEqual(result["column"], 0)

    def test_negative_pos(self):
        """测试：pos 为负数"""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 5, "column": 10},
        ]
        result = _create_error_node(-1, tokens)
        
        # 负数索引在 Python 中是合法的，会访问最后一个元素
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 10)

    def test_return_structure_integrity(self):
        """测试：返回结构完整性（所有必需字段）"""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 100, "column": 200},
        ]
        result = _create_error_node(0, tokens)
        
        # 验证所有必需字段存在
        self.assertIn("type", result)
        self.assertIn("value", result)
        self.assertIn("line", result)
        self.assertIn("column", result)
        self.assertIn("children", result)
        
        # 验证字段类型
        self.assertIsInstance(result["children"], list)
        self.assertEqual(len(result["children"]), 0)

    def test_no_side_effects(self):
        """测试：函数是纯函数，不修改输入"""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 5, "column": 10},
        ]
        tokens_copy = [token.copy() for token in tokens]
        
        _create_error_node(0, tokens)
        
        # 验证 tokens 未被修改
        self.assertEqual(tokens, tokens_copy)

    def test_multiple_calls_independence(self):
        """测试：多次调用相互独立"""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            {"type": "OPERATOR", "value": "+", "line": 2, "column": 2},
        ]
        
        result1 = _create_error_node(0, tokens)
        result2 = _create_error_node(1, tokens)
        
        self.assertEqual(result1["line"], 1)
        self.assertEqual(result1["column"], 1)
        self.assertEqual(result2["line"], 2)
        self.assertEqual(result2["column"], 2)
        # 验证是两个不同的对象
        self.assertIsNot(result1, result2)


if __name__ == "__main__":
    unittest.main()

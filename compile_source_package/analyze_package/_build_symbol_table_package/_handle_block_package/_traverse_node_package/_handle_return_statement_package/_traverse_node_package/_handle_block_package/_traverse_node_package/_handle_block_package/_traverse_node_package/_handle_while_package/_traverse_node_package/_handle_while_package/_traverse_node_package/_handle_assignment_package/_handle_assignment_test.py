#!/usr/bin/env python3
"""
单元测试文件：_handle_assignment 函数测试
"""

import unittest

# 相对导入被测函数
from ._handle_assignment_src import _handle_assignment


class TestHandleAssignment(unittest.TestCase):
    """_handle_assignment 函数的单元测试类"""
    
    def test_happy_path_types_match_int(self):
        """测试 happy path: 变量已声明且类型匹配 (int)"""
        node = {
            "type": "assignment",
            "children": [
                {"type": "identifier", "value": "x", "line": 1, "column": 5},
                {"type": "literal", "value": 10, "data_type": "int", "line": 1, "column": 9}
            ],
            "line": 1,
            "column": 5
        }
        
        symbol_table = {
            "variables": {
                "x": {"data_type": "int", "is_declared": True, "line": 0, "column": 0, "scope_level": 0}
            },
            "errors": []
        }
        
        _handle_assignment(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 0)
    
    def test_happy_path_types_match_char(self):
        """测试 happy path: 变量已声明且类型匹配 (char)"""
        node = {
            "type": "assignment",
            "children": [
                {"type": "identifier", "value": "c", "line": 1, "column": 5},
                {"type": "literal", "value": "a", "data_type": "char", "line": 1, "column": 9}
            ],
            "line": 1,
            "column": 5
        }
        
        symbol_table = {
            "variables": {
                "c": {"data_type": "char", "is_declared": True, "line": 0, "column": 0, "scope_level": 0}
            },
            "errors": []
        }
        
        _handle_assignment(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 0)
    
    def test_variable_not_declared(self):
        """测试变量未声明的情况"""
        node = {
            "type": "assignment",
            "children": [
                {"type": "identifier", "value": "y", "line": 2, "column": 3},
                {"type": "literal", "value": 5, "data_type": "int", "line": 2, "column": 7}
            ],
            "line": 2,
            "column": 3
        }
        
        symbol_table = {
            "variables": {
                "x": {"data_type": "int", "is_declared": True, "line": 0, "column": 0, "scope_level": 0}
            },
            "errors": []
        }
        
        _handle_assignment(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("变量未声明", symbol_table["errors"][0])
        self.assertIn("y", symbol_table["errors"][0])
        self.assertIn("line 2", symbol_table["errors"][0])
    
    def test_type_mismatch_int_to_char(self):
        """测试类型不匹配：变量是 int，赋值是 char"""
        node = {
            "type": "assignment",
            "children": [
                {"type": "identifier", "value": "x", "line": 3, "column": 1},
                {"type": "literal", "value": "b", "data_type": "char", "line": 3, "column": 5}
            ],
            "line": 3,
            "column": 1
        }
        
        symbol_table = {
            "variables": {
                "x": {"data_type": "int", "is_declared": True, "line": 0, "column": 0, "scope_level": 0}
            },
            "errors": []
        }
        
        _handle_assignment(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("类型不匹配", symbol_table["errors"][0])
        self.assertIn("x", symbol_table["errors"][0])
        self.assertIn("int", symbol_table["errors"][0])
        self.assertIn("char", symbol_table["errors"][0])
    
    def test_type_mismatch_char_to_int(self):
        """测试类型不匹配：变量是 char，赋值是 int"""
        node = {
            "type": "assignment",
            "children": [
                {"type": "identifier", "value": "c", "line": 4, "column": 2},
                {"type": "literal", "value": 42, "data_type": "int", "line": 4, "column": 6}
            ],
            "line": 4,
            "column": 2
        }
        
        symbol_table = {
            "variables": {
                "c": {"data_type": "char", "is_declared": True, "line": 0, "column": 0, "scope_level": 0}
            },
            "errors": []
        }
        
        _handle_assignment(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("类型不匹配", symbol_table["errors"][0])
        self.assertIn("c", symbol_table["errors"][0])
    
    def test_expr_type_inference_from_int(self):
        """测试表达式类型从 int 值推断"""
        node = {
            "type": "assignment",
            "children": [
                {"type": "identifier", "value": "x", "line": 5, "column": 1},
                {"type": "literal", "value": 100}
            ],
            "line": 5,
            "column": 1
        }
        
        symbol_table = {
            "variables": {
                "x": {"data_type": "int", "is_declared": True, "line": 0, "column": 0, "scope_level": 0}
            },
            "errors": []
        }
        
        _handle_assignment(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 0)
    
    def test_expr_type_inference_from_char(self):
        """测试表达式类型从 char 值推断"""
        node = {
            "type": "assignment",
            "children": [
                {"type": "identifier", "value": "c", "line": 6, "column": 1},
                {"type": "literal", "value": "z"}
            ],
            "line": 6,
            "column": 1
        }
        
        symbol_table = {
            "variables": {
                "c": {"data_type": "char", "is_declared": True, "line": 0, "column": 0, "scope_level": 0}
            },
            "errors": []
        }
        
        _handle_assignment(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 0)
    
    def test_errors_list_initialization(self):
        """测试 errors 列表自动初始化"""
        node = {
            "type": "assignment",
            "children": [
                {"type": "identifier", "value": "undeclared", "line": 7, "column": 1},
                {"type": "literal", "value": 1, "data_type": "int", "line": 7, "column": 15}
            ],
            "line": 7,
            "column": 1
        }
        
        symbol_table = {
            "variables": {}
        }
        
        _handle_assignment(node, symbol_table)
        
        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)
    
    def test_type_mismatch_with_inferred_type(self):
        """测试类型不匹配：使用推断的类型"""
        node = {
            "type": "assignment",
            "children": [
                {"type": "identifier", "value": "c", "line": 8, "column": 1},
                {"type": "literal", "value": 999}
            ],
            "line": 8,
            "column": 1
        }
        
        symbol_table = {
            "variables": {
                "c": {"data_type": "char", "is_declared": True, "line": 0, "column": 0, "scope_level": 0}
            },
            "errors": []
        }
        
        _handle_assignment(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("类型不匹配", symbol_table["errors"][0])
    
    def test_string_value_longer_than_one_char(self):
        """测试字符串值长度大于 1 时不推断为 char"""
        node = {
            "type": "assignment",
            "children": [
                {"type": "identifier", "value": "c", "line": 9, "column": 1},
                {"type": "literal", "value": "ab"}
            ],
            "line": 9,
            "column": 1
        }
        
        symbol_table = {
            "variables": {
                "c": {"data_type": "char", "is_declared": True, "line": 0, "column": 0, "scope_level": 0}
            },
            "errors": []
        }
        
        _handle_assignment(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 0)
    
    def test_multiple_errors_accumulation(self):
        """测试多个错误累积"""
        node1 = {
            "type": "assignment",
            "children": [
                {"type": "identifier", "value": "undeclared1", "line": 10, "column": 1},
                {"type": "literal", "value": 1, "data_type": "int", "line": 10, "column": 15}
            ],
            "line": 10,
            "column": 1
        }
        
        node2 = {
            "type": "assignment",
            "children": [
                {"type": "identifier", "value": "x", "line": 11, "column": 1},
                {"type": "literal", "value": "a", "data_type": "char", "line": 11, "column": 5}
            ],
            "line": 11,
            "column": 1
        }
        
        symbol_table = {
            "variables": {
                "x": {"data_type": "int", "is_declared": True, "line": 0, "column": 0, "scope_level": 0}
            },
            "errors": []
        }
        
        _handle_assignment(node1, symbol_table)
        _handle_assignment(node2, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 2)
    
    def test_empty_variables_dict(self):
        """测试空的 variables 字典"""
        node = {
            "type": "assignment",
            "children": [
                {"type": "identifier", "value": "any", "line": 12, "column": 1},
                {"type": "literal", "value": 1, "data_type": "int", "line": 12, "column": 7}
            ],
            "line": 12,
            "column": 1
        }
        
        symbol_table = {
            "variables": {},
            "errors": []
        }
        
        _handle_assignment(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("变量未声明", symbol_table["errors"][0])
    
    def test_missing_line_column_in_target(self):
        """测试目标节点缺少 line/column 时使用 node 的值"""
        node = {
            "type": "assignment",
            "children": [
                {"type": "identifier", "value": "x"},
                {"type": "literal", "value": 1, "data_type": "int"}
            ],
            "line": 15,
            "column": 10
        }
        
        symbol_table = {
            "variables": {
                "x": {"data_type": "int", "is_declared": True, "line": 0, "column": 0, "scope_level": 0}
            },
            "errors": []
        }
        
        _handle_assignment(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 0)
    
    def test_none_declared_type(self):
        """测试变量声明类型为 None 的情况"""
        node = {
            "type": "assignment",
            "children": [
                {"type": "identifier", "value": "x", "line": 16, "column": 1},
                {"type": "literal", "value": 1, "data_type": "int", "line": 16, "column": 5}
            ],
            "line": 16,
            "column": 1
        }
        
        symbol_table = {
            "variables": {
                "x": {"data_type": None, "is_declared": True, "line": 0, "column": 0, "scope_level": 0}
            },
            "errors": []
        }
        
        _handle_assignment(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 0)
    
    def test_none_expr_type(self):
        """测试表达式类型为 None 且无法推断的情况"""
        node = {
            "type": "assignment",
            "children": [
                {"type": "identifier", "value": "x", "line": 17, "column": 1},
                {"type": "literal", "value": None, "data_type": None, "line": 17, "column": 5}
            ],
            "line": 17,
            "column": 1
        }
        
        symbol_table = {
            "variables": {
                "x": {"data_type": "int", "is_declared": True, "line": 0, "column": 0, "scope_level": 0}
            },
            "errors": []
        }
        
        _handle_assignment(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 0)
    
    def test_missing_variables_key(self):
        """测试 symbol_table 缺少 variables 键的情况"""
        node = {
            "type": "assignment",
            "children": [
                {"type": "identifier", "value": "x", "line": 18, "column": 1},
                {"type": "literal", "value": 1, "data_type": "int", "line": 18, "column": 5}
            ],
            "line": 18,
            "column": 1
        }
        
        symbol_table = {
            "errors": []
        }
        
        _handle_assignment(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("变量未声明", symbol_table["errors"][0])


if __name__ == "__main__":
    unittest.main()

# -*- coding: utf-8 -*-
"""单元测试：_verify_literal 函数"""

import unittest
from typing import Any, Dict

# 相对导入被测模块
from ._verify_literal_src import _verify_literal


class TestVerifyLiteral(unittest.TestCase):
    """_verify_literal 函数的单元测试类"""

    def test_int_literal_sets_data_type_to_int(self):
        """测试 int_literal 类型节点正确设置 data_type 为 'int'"""
        node: Dict[str, Any] = {
            "type": "int_literal",
            "value": 42,
            "line": 1,
            "column": 5
        }
        filename = "test.py"
        
        _verify_literal(node, filename)
        
        self.assertEqual(node["data_type"], "int")
        self.assertEqual(node["type"], "int_literal")
        self.assertEqual(node["value"], 42)

    def test_char_literal_sets_data_type_to_char(self):
        """测试 char_literal 类型节点正确设置 data_type 为 'char'"""
        node: Dict[str, Any] = {
            "type": "char_literal",
            "value": "a",
            "line": 2,
            "column": 10
        }
        filename = "test.py"
        
        _verify_literal(node, filename)
        
        self.assertEqual(node["data_type"], "char")
        self.assertEqual(node["type"], "char_literal")
        self.assertEqual(node["value"], "a")

    def test_unknown_type_does_not_set_data_type(self):
        """测试未知类型节点不会设置 data_type"""
        node: Dict[str, Any] = {
            "type": "string_literal",
            "value": "hello",
            "line": 3,
            "column": 1
        }
        filename = "test.py"
        
        _verify_literal(node, filename)
        
        self.assertNotIn("data_type", node)
        self.assertEqual(node["type"], "string_literal")

    def test_node_without_type_key_does_not_set_data_type(self):
        """测试没有 type 键的节点不会设置 data_type"""
        node: Dict[str, Any] = {
            "value": 100,
            "line": 4,
            "column": 2
        }
        filename = "test.py"
        
        _verify_literal(node, filename)
        
        self.assertNotIn("data_type", node)
        self.assertNotIn("type", node)

    def test_empty_node_does_not_raise_error(self):
        """测试空节点不会抛出错误"""
        node: Dict[str, Any] = {}
        filename = "test.py"
        
        # 不应抛出任何异常
        _verify_literal(node, filename)
        
        self.assertNotIn("data_type", node)

    def test_none_type_value_does_not_set_data_type(self):
        """测试 type 为 None 的节点不会设置 data_type"""
        node: Dict[str, Any] = {
            "type": None,
            "value": None,
            "line": 5,
            "column": 3
        }
        filename = "test.py"
        
        _verify_literal(node, filename)
        
        self.assertNotIn("data_type", node)

    def test_in_place_modification(self):
        """测试函数是原地修改节点，而非返回新对象"""
        node: Dict[str, Any] = {
            "type": "int_literal",
            "value": 999,
            "line": 6,
            "column": 4
        }
        filename = "test.py"
        original_id = id(node)
        
        result = _verify_literal(node, filename)
        
        # 函数应返回 None
        self.assertIsNone(result)
        # 节点对象本身未被替换
        self.assertEqual(id(node), original_id)
        # 但节点内容被修改
        self.assertEqual(node["data_type"], "int")

    def test_filename_parameter_accepted_but_not_used(self):
        """测试 filename 参数可接受但不影响行为"""
        node: Dict[str, Any] = {
            "type": "char_literal",
            "value": "x",
            "line": 7,
            "column": 5
        }
        
        # 不同的 filename 不应影响结果
        _verify_literal(node, "file1.py")
        self.assertEqual(node["data_type"], "char")
        
        node2: Dict[str, Any] = {
            "type": "char_literal",
            "value": "y",
            "line": 8,
            "column": 6
        }
        _verify_literal(node2, "/absolute/path/to/file2.py")
        self.assertEqual(node2["data_type"], "char")

    def test_preserves_other_node_fields(self):
        """测试函数保留节点的其他字段"""
        node: Dict[str, Any] = {
            "type": "int_literal",
            "value": 12345,
            "line": 9,
            "column": 7,
            "extra_field": "should_be_preserved",
            "another_field": {"nested": "data"}
        }
        filename = "test.py"
        
        _verify_literal(node, filename)
        
        self.assertEqual(node["data_type"], "int")
        self.assertEqual(node["value"], 12345)
        self.assertEqual(node["line"], 9)
        self.assertEqual(node["column"], 7)
        self.assertEqual(node["extra_field"], "should_be_preserved")
        self.assertEqual(node["another_field"], {"nested": "data"})


if __name__ == "__main__":
    unittest.main()

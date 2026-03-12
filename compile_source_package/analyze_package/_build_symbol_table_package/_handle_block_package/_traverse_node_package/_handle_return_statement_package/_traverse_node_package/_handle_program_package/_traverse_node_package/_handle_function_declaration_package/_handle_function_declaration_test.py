#!/usr/bin/env python3
"""
单元测试文件：_handle_function_declaration 函数测试
"""

import unittest
from typing import Any, Dict, List

# 相对导入被测模块
from ._handle_function_declaration_src import _handle_function_declaration


class TestHandleFunctionDeclaration(unittest.TestCase):
    """_handle_function_declaration 函数的单元测试类"""
    
    def _create_function_node(
        self,
        func_name: str = None,
        data_type: str = "int",
        line: int = 1,
        column: int = 1,
        params: List[Dict[str, Any]] = None,
        parameters: List[Dict[str, Any]] = None,
        children: List[Dict[str, Any]] = None,
        body: List[Dict[str, Any]] = None,
        name: str = None,
        value: str = None
    ) -> Dict[str, Any]:
        """辅助函数：创建 function_declaration 类型的 AST 节点"""
        node = {
            "type": "function_declaration",
            "data_type": data_type,
            "line": line,
            "column": column
        }
        if func_name:
            node["value"] = func_name
        if name:
            node["name"] = name
        if value:
            node["value"] = value
        if params is not None:
            node["params"] = params
        if parameters is not None:
            node["parameters"] = parameters
        if children is not None:
            node["children"] = children
        if body is not None:
            node["body"] = body
        return node
    
    def _create_symbol_table(self, current_scope: int = 0) -> Dict[str, Any]:
        """辅助函数：创建符号表"""
        return {
            "variables": {},
            "functions": {},
            "current_scope": current_scope,
            "scope_stack": [0],
            "errors": []
        }
    
    def test_happy_path_valid_function_declaration(self):
        """测试 happy path：有效的函数声明"""
        node = self._create_function_node(func_name="test_func")
        symbol_table = self._create_symbol_table()
        
        _handle_function_declaration(node, symbol_table)
        
        self.assertIn("test_func", symbol_table["functions"])
        self.assertEqual(symbol_table["functions"]["test_func"]["return_type"], "int")
        self.assertEqual(symbol_table["functions"]["test_func"]["params"], [])
        self.assertEqual(symbol_table["functions"]["test_func"]["line"], 1)
        self.assertEqual(symbol_table["functions"]["test_func"]["column"], 1)
        self.assertEqual(symbol_table["functions"]["test_func"]["scope_level"], 0)
        self.assertEqual(symbol_table["current_function"], "test_func")
        self.assertEqual(len(symbol_table["errors"]), 0)
    
    def test_function_with_name_field(self):
        """测试从 name 字段提取函数名"""
        node = self._create_function_node(name="my_func")
        symbol_table = self._create_symbol_table()
        
        _handle_function_declaration(node, symbol_table)
        
        self.assertIn("my_func", symbol_table["functions"])
        self.assertEqual(symbol_table["current_function"], "my_func")
    
    def test_function_with_value_field(self):
        """测试从 value 字段提取函数名"""
        node = self._create_function_node(value="my_func")
        symbol_table = self._create_symbol_table()
        
        _handle_function_declaration(node, symbol_table)
        
        self.assertIn("my_func", symbol_table["functions"])
        self.assertEqual(symbol_table["current_function"], "my_func")
    
    def test_function_name_priority_value_over_name(self):
        """测试 value 字段优先于 name 字段"""
        node = self._create_function_node(name="name_func", value="value_func")
        symbol_table = self._create_symbol_table()
        
        _handle_function_declaration(node, symbol_table)
        
        self.assertIn("value_func", symbol_table["functions"])
        self.assertNotIn("name_func", symbol_table["functions"])
    
    def test_missing_function_name(self):
        """测试缺少函数名时添加错误"""
        node = {
            "type": "function_declaration",
            "data_type": "int",
            "line": 5,
            "column": 10
        }
        symbol_table = self._create_symbol_table()
        
        _handle_function_declaration(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertEqual(symbol_table["errors"][0]["message"], "无法提取函数名")
        self.assertEqual(symbol_table["errors"][0]["line"], 5)
        self.assertEqual(symbol_table["errors"][0]["column"], 10)
        self.assertNotIn("current_function", symbol_table)
    
    def test_valid_return_type_int(self):
        """测试有效的 int 返回类型"""
        node = self._create_function_node(func_name="test", data_type="int")
        symbol_table = self._create_symbol_table()
        
        _handle_function_declaration(node, symbol_table)
        
        self.assertEqual(symbol_table["functions"]["test"]["return_type"], "int")
        self.assertEqual(len(symbol_table["errors"]), 0)
    
    def test_valid_return_type_char(self):
        """测试有效的 char 返回类型"""
        node = self._create_function_node(func_name="test", data_type="char")
        symbol_table = self._create_symbol_table()
        
        _handle_function_declaration(node, symbol_table)
        
        self.assertEqual(symbol_table["functions"]["test"]["return_type"], "char")
        self.assertEqual(len(symbol_table["errors"]), 0)
    
    def test_invalid_return_type(self):
        """测试无效的返回类型"""
        node = self._create_function_node(func_name="test", data_type="void")
        symbol_table = self._create_symbol_table()
        
        _handle_function_declaration(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("无效的返回类型", symbol_table["errors"][0]["message"])
        self.assertEqual(symbol_table["functions"]["test"]["return_type"], "int")
    
    def test_missing_return_type_defaults_to_int(self):
        """测试缺少返回类型时默认为 int"""
        node = self._create_function_node(func_name="test")
        symbol_table = self._create_symbol_table()
        
        _handle_function_declaration(node, symbol_table)
        
        self.assertEqual(symbol_table["functions"]["test"]["return_type"], "int")
    
    def test_duplicate_function_declaration(self):
        """测试重复声明函数"""
        symbol_table = self._create_symbol_table()
        symbol_table["functions"] = {
            "existing_func": {
                "return_type": "int",
                "params": [],
                "line": 1,
                "column": 1,
                "scope_level": 0
            }
        }
        
        node = self._create_function_node(func_name="existing_func", line=5, column=10)
        _handle_function_declaration(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertEqual(symbol_table["errors"][0]["message"], "函数 'existing_func' 重复声明")
        self.assertEqual(symbol_table["errors"][0]["line"], 5)
        self.assertEqual(symbol_table["errors"][0]["column"], 10)
    
    def test_function_with_params(self):
        """测试带参数的函数"""
        params = [
            {"name": "x", "data_type": "int"},
            {"name": "y", "data_type": "char"}
        ]
        node = self._create_function_node(func_name="test", params=params)
        symbol_table = self._create_symbol_table()
        
        _handle_function_declaration(node, symbol_table)
        
        self.assertEqual(symbol_table["functions"]["test"]["params"], params)
    
    def test_function_with_parameters_field(self):
        """测试使用 parameters 字段的参数"""
        params = [{"name": "x", "data_type": "int"}]
        node = self._create_function_node(func_name="test", parameters=params)
        symbol_table = self._create_symbol_table()
        
        _handle_function_declaration(node, symbol_table)
        
        self.assertEqual(symbol_table["functions"]["test"]["params"], params)
    
    def test_function_with_children_body(self):
        """测试处理带有 children 的函数体"""
        children = [
            {"type": "variable_declaration", "value": "x"},
            {"type": "assignment", "value": "x = 1"}
        ]
        node = self._create_function_node(func_name="test", children=children)
        symbol_table = self._create_symbol_table()
        
        _handle_function_declaration(node, symbol_table)
        
        self.assertIn("test", symbol_table["functions"])
    
    def test_function_with_body_field(self):
        """测试处理带有 body 字段的函数体"""
        body = [{"type": "statement"}]
        node = self._create_function_node(func_name="test", body=body)
        symbol_table = self._create_symbol_table()
        
        _handle_function_declaration(node, symbol_table)
        
        self.assertIn("test", symbol_table["functions"])
    
    def test_scope_level_captured(self):
        """测试捕获当前作用域层级"""
        node = self._create_function_node(func_name="test")
        symbol_table = self._create_symbol_table(current_scope=3)
        
        _handle_function_declaration(node, symbol_table)
        
        self.assertEqual(symbol_table["functions"]["test"]["scope_level"], 3)
    
    def test_line_column_captured(self):
        """测试捕获行号和列号"""
        node = self._create_function_node(func_name="test", line=10, column=20)
        symbol_table = self._create_symbol_table()
        
        _handle_function_declaration(node, symbol_table)
        
        self.assertEqual(symbol_table["functions"]["test"]["line"], 10)
        self.assertEqual(symbol_table["functions"]["test"]["column"], 20)
    
    def test_missing_line_column_defaults_to_zero(self):
        """测试缺少行号列号时默认为 0"""
        # 直接创建节点，不设置 line 和 column 字段
        node = {
            "type": "function_declaration",
            "value": "test",
            "data_type": "int"
        }
        symbol_table = self._create_symbol_table()
        
        _handle_function_declaration(node, symbol_table)
        
        self.assertEqual(symbol_table["functions"]["test"]["line"], 0)
        self.assertEqual(symbol_table["functions"]["test"]["column"], 0)
    
    def test_error_structure(self):
        """测试错误信息结构"""
        node = {
            "type": "function_declaration",
            "line": 5,
            "column": 10
        }
        symbol_table = self._create_symbol_table()
        
        _handle_function_declaration(node, symbol_table)
        
        error = symbol_table["errors"][0]
        self.assertEqual(error["type"], "declaration_error")
        self.assertIn("message", error)
        self.assertEqual(error["line"], 5)
        self.assertEqual(error["column"], 10)
    
    def test_multiple_functions(self):
        """测试注册多个不同函数"""
        symbol_table = self._create_symbol_table()
        
        node1 = self._create_function_node(func_name="func1")
        _handle_function_declaration(node1, symbol_table)
        
        node2 = self._create_function_node(func_name="func2", data_type="char")
        _handle_function_declaration(node2, symbol_table)
        
        self.assertIn("func1", symbol_table["functions"])
        self.assertIn("func2", symbol_table["functions"])
        self.assertEqual(symbol_table["functions"]["func1"]["return_type"], "int")
        self.assertEqual(symbol_table["functions"]["func2"]["return_type"], "char")
        self.assertEqual(len(symbol_table["errors"]), 0)
    
    def test_empty_params_list(self):
        """测试空参数列表"""
        node = self._create_function_node(func_name="test", params=[])
        symbol_table = self._create_symbol_table()
        
        _handle_function_declaration(node, symbol_table)
        
        self.assertEqual(symbol_table["functions"]["test"]["params"], [])
    
    def test_symbol_table_initialized_if_empty(self):
        """测试符号表 functions 字段自动初始化"""
        node = self._create_function_node(func_name="test")
        symbol_table = {}
        
        _handle_function_declaration(node, symbol_table)
        
        self.assertIn("functions", symbol_table)
        self.assertIn("test", symbol_table["functions"])


if __name__ == "__main__":
    unittest.main()

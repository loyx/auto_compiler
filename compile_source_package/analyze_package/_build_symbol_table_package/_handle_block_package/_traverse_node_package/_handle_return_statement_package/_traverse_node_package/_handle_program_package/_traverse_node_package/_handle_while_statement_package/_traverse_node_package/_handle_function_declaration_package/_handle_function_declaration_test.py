# -*- coding: utf-8 -*-
"""
单元测试：_handle_function_declaration 函数
测试 function_declaration 类型 AST 节点的处理逻辑
"""

import unittest

# 相对导入被测模块
from ._handle_function_declaration_src import (
    _handle_function_declaration,
    _extract_parameters
)


class TestHandleFunctionDeclaration(unittest.TestCase):
    """测试 _handle_function_declaration 函数"""
    
    def setUp(self):
        """每个测试前的准备工作"""
        self.symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
            "errors": []
        }
    
    def test_normal_function_declaration(self):
        """测试正常的函数声明"""
        node = {
            "type": "function_declaration",
            "value": "myFunction",
            "data_type": "int",
            "line": 10,
            "column": 5,
            "children": []
        }
        
        _handle_function_declaration(node, self.symbol_table)
        
        # 验证函数已注册
        self.assertIn("myFunction", self.symbol_table["functions"])
        func_info = self.symbol_table["functions"]["myFunction"]
        self.assertEqual(func_info["return_type"], "int")
        self.assertEqual(func_info["params"], [])
        self.assertEqual(func_info["line"], 10)
        self.assertEqual(func_info["column"], 5)
        
        # 验证当前函数已设置
        self.assertEqual(self.symbol_table["current_function"], "myFunction")
        
        # 验证没有错误
        self.assertEqual(len(self.symbol_table["errors"]), 0)
    
    def test_function_declaration_with_parameters(self):
        """测试带参数的函数声明"""
        node = {
            "type": "function_declaration",
            "value": "add",
            "data_type": "int",
            "line": 1,
            "column": 1,
            "children": [
                {
                    "type": "variable_declaration",
                    "value": "a",
                    "data_type": "int",
                    "line": 1,
                    "column": 10
                },
                {
                    "type": "variable_declaration",
                    "value": "b",
                    "data_type": "int",
                    "line": 1,
                    "column": 20
                }
            ]
        }
        
        _handle_function_declaration(node, self.symbol_table)
        
        func_info = self.symbol_table["functions"]["add"]
        self.assertEqual(len(func_info["params"]), 2)
        self.assertEqual(func_info["params"][0]["name"], "a")
        self.assertEqual(func_info["params"][0]["data_type"], "int")
        self.assertEqual(func_info["params"][1]["name"], "b")
        self.assertEqual(func_info["params"][1]["data_type"], "int")
    
    def test_duplicate_function_declaration(self):
        """测试重复函数声明"""
        # 第一次声明
        node1 = {
            "type": "function_declaration",
            "value": "duplicateFunc",
            "data_type": "void",
            "line": 1,
            "column": 1,
            "children": []
        }
        _handle_function_declaration(node1, self.symbol_table)
        
        # 第二次声明（重复）
        node2 = {
            "type": "function_declaration",
            "value": "duplicateFunc",
            "data_type": "int",
            "line": 5,
            "column": 1,
            "children": []
        }
        _handle_function_declaration(node2, self.symbol_table)
        
        # 验证记录了错误
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        self.assertIn("重复声明", self.symbol_table["errors"][0])
        
        # 验证函数信息没有被覆盖（保持第一次声明的信息）
        func_info = self.symbol_table["functions"]["duplicateFunc"]
        self.assertEqual(func_info["return_type"], "void")
        self.assertEqual(func_info["line"], 1)
    
    def test_empty_function_name(self):
        """测试函数名为空的情况"""
        node = {
            "type": "function_declaration",
            "value": "",
            "data_type": "int",
            "line": 1,
            "column": 1,
            "children": []
        }
        
        _handle_function_declaration(node, self.symbol_table)
        
        # 验证记录了错误
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        self.assertIn("函数名", self.symbol_table["errors"][0])
        
        # 验证没有注册函数
        self.assertEqual(len(self.symbol_table["functions"]), 0)
        
        # 验证 current_function 未设置
        self.assertNotIn("current_function", self.symbol_table)
    
    def test_missing_function_name(self):
        """测试缺少函数名字段的情况"""
        node = {
            "type": "function_declaration",
            "data_type": "int",
            "line": 1,
            "column": 1,
            "children": []
        }
        
        _handle_function_declaration(node, self.symbol_table)
        
        # 验证记录了错误
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        
        # 验证没有注册函数
        self.assertEqual(len(self.symbol_table["functions"]), 0)
    
    def test_default_return_type(self):
        """测试缺少 data_type 时使用默认值 void"""
        node = {
            "type": "function_declaration",
            "value": "testFunc",
            "line": 1,
            "column": 1,
            "children": []
        }
        
        _handle_function_declaration(node, self.symbol_table)
        
        func_info = self.symbol_table["functions"]["testFunc"]
        self.assertEqual(func_info["return_type"], "void")
    
    def test_function_with_no_children(self):
        """测试没有 children 字段的函数声明"""
        node = {
            "type": "function_declaration",
            "value": "testFunc",
            "data_type": "int"
        }
        
        _handle_function_declaration(node, self.symbol_table)
        
        self.assertIn("testFunc", self.symbol_table["functions"])
        func_info = self.symbol_table["functions"]["testFunc"]
        self.assertEqual(func_info["params"], [])
    
    def test_missing_line_column(self):
        """测试缺少行号列号时使用默认值 -1"""
        node = {
            "type": "function_declaration",
            "value": "testFunc",
            "data_type": "int",
            "children": []
        }
        
        _handle_function_declaration(node, self.symbol_table)
        
        func_info = self.symbol_table["functions"]["testFunc"]
        self.assertEqual(func_info["line"], -1)
        self.assertEqual(func_info["column"], -1)
    
    def test_symbol_table_initialized_on_demand(self):
        """测试符号表字段按需初始化"""
        symbol_table = {}
        
        node = {
            "type": "function_declaration",
            "value": "testFunc",
            "data_type": "int"
        }
        
        _handle_function_declaration(node, symbol_table)
        
        self.assertIn("functions", symbol_table)
        self.assertIn("errors", symbol_table)
        self.assertIn("testFunc", symbol_table["functions"])
    
    def test_function_declaration_preserves_existing_data(self):
        """测试函数声明不破坏符号表已有数据"""
        self.symbol_table["variables"]["existing_var"] = {
            "data_type": "int",
            "is_declared": True
        }
        self.symbol_table["current_scope"] = 2
        
        node = {
            "type": "function_declaration",
            "value": "newFunc",
            "data_type": "void"
        }
        
        _handle_function_declaration(node, self.symbol_table)
        
        # 验证已有数据未被破坏
        self.assertIn("existing_var", self.symbol_table["variables"])
        self.assertEqual(self.symbol_table["current_scope"], 2)
        self.assertIn("newFunc", self.symbol_table["functions"])


class TestExtractParameters(unittest.TestCase):
    """测试 _extract_parameters 辅助函数"""
    
    def test_extract_parameters_normal(self):
        """测试正常参数提取"""
        children = [
            {
                "type": "variable_declaration",
                "value": "param1",
                "data_type": "int",
                "line": 1,
                "column": 1
            },
            {
                "type": "variable_declaration",
                "value": "param2",
                "data_type": "char",
                "line": 2,
                "column": 2
            }
        ]
        
        params = _extract_parameters(children)
        
        self.assertEqual(len(params), 2)
        self.assertEqual(params[0]["name"], "param1")
        self.assertEqual(params[0]["data_type"], "int")
        self.assertEqual(params[0]["line"], 1)
        self.assertEqual(params[0]["column"], 1)
        self.assertEqual(params[1]["name"], "param2")
        self.assertEqual(params[1]["data_type"], "char")
    
    def test_extract_parameters_mixed_nodes(self):
        """测试混合节点类型的参数提取"""
        children = [
            {
                "type": "variable_declaration",
                "value": "param1",
                "data_type": "int"
            },
            {
                "type": "expression",
                "value": "some_expr"
            },
            {
                "type": "variable_declaration",
                "value": "param2",
                "data_type": "char"
            },
            {
                "type": "block",
                "value": "block1"
            }
        ]
        
        params = _extract_parameters(children)
        
        self.assertEqual(len(params), 2)
        self.assertEqual(params[0]["name"], "param1")
        self.assertEqual(params[1]["name"], "param2")
    
    def test_extract_parameters_empty(self):
        """测试空参数列表"""
        params = _extract_parameters([])
        self.assertEqual(params, [])
    
    def test_extract_parameters_no_variable_declarations(self):
        """测试没有 variable_declaration 类型的子节点"""
        children = [
            {"type": "expression", "value": "expr1"},
            {"type": "block", "value": "block1"}
        ]
        
        params = _extract_parameters(children)
        self.assertEqual(params, [])
    
    def test_extract_parameters_missing_value(self):
        """测试参数缺少 value 字段"""
        children = [
            {
                "type": "variable_declaration",
                "data_type": "int"
            }
        ]
        
        params = _extract_parameters(children)
        self.assertEqual(params, [])
    
    def test_extract_parameters_default_type(self):
        """测试参数缺少 data_type 时使用默认值 int"""
        children = [
            {
                "type": "variable_declaration",
                "value": "param1"
            }
        ]
        
        params = _extract_parameters(children)
        
        self.assertEqual(len(params), 1)
        self.assertEqual(params[0]["name"], "param1")
        self.assertEqual(params[0]["data_type"], "int")
    
    def test_extract_parameters_missing_line_column(self):
        """测试参数缺少行号列号时使用默认值 -1"""
        children = [
            {
                "type": "variable_declaration",
                "value": "param1",
                "data_type": "int"
            }
        ]
        
        params = _extract_parameters(children)
        
        self.assertEqual(params[0]["line"], -1)
        self.assertEqual(params[0]["column"], -1)


if __name__ == "__main__":
    unittest.main()

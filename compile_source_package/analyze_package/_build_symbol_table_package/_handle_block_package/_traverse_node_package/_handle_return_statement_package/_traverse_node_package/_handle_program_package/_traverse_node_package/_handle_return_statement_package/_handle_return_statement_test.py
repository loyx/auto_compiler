# -*- coding: utf-8 -*-
"""单元测试文件：_handle_return_statement 函数的测试用例"""

import unittest
from unittest.mock import patch
from typing import Any, Dict

# 相对导入被测试模块
from ._handle_return_statement_src import _handle_return_statement

# 类型定义
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleReturnStatement(unittest.TestCase):
    """_handle_return_statement 函数的测试类"""

    def setUp(self):
        """每个测试前的准备工作"""
        pass

    def tearDown(self):
        """每个测试后的清理工作"""
        pass

    def test_return_type_matches(self):
        """测试返回值类型匹配的情况（Happy Path）"""
        node: AST = {
            "type": "return_statement",
            "line": 10,
            "column": 5,
            "expression": {
                "type": "literal",
                "value": 42,
                "data_type": "int",
                "line": 10,
                "column": 12
            }
        }
        
        symbol_table: SymbolTable = {
            "current_function": "main",
            "functions": {
                "main": {
                    "return_type": "int",
                    "params": [],
                    "line": 1,
                    "column": 0
                }
            },
            "errors": []
        }
        
        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_return_statement(node, symbol_table)
            
            # 验证 _traverse_node 被调用
            mock_traverse.assert_called_once_with(node["expression"], symbol_table)
            # 验证没有错误
            self.assertEqual(len(symbol_table["errors"]), 0)

    def test_return_type_mismatch(self):
        """测试返回值类型不匹配的情况"""
        node: AST = {
            "type": "return_statement",
            "line": 15,
            "column": 5,
            "expression": {
                "type": "literal",
                "value": "hello",
                "data_type": "char",
                "line": 15,
                "column": 12
            }
        }
        
        symbol_table: SymbolTable = {
            "current_function": "foo",
            "functions": {
                "foo": {
                    "return_type": "int",
                    "params": [],
                    "line": 1,
                    "column": 0
                }
            },
            "errors": []
        }
        
        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_return_statement(node, symbol_table)
            
            # 验证 _traverse_node 被调用
            mock_traverse.assert_called_once()
            # 验证有类型不匹配错误
            self.assertEqual(len(symbol_table["errors"]), 1)
            self.assertEqual(symbol_table["errors"][0]["type"], "return_type_mismatch")
            self.assertIn("expected 'int' but got 'char'", symbol_table["errors"][0]["message"])
            self.assertEqual(symbol_table["errors"][0]["line"], 15)
            self.assertEqual(symbol_table["errors"][0]["column"], 5)

    def test_return_outside_function(self):
        """测试在函数外使用 return 的情况"""
        node: AST = {
            "type": "return_statement",
            "line": 20,
            "column": 1,
            "expression": {
                "type": "literal",
                "value": 0,
                "data_type": "int",
                "line": 20,
                "column": 8
            }
        }
        
        symbol_table: SymbolTable = {
            "current_function": None,
            "functions": {},
            "errors": []
        }
        
        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_return_statement(node, symbol_table)
            
            # 验证 _traverse_node 没有被调用（因为提前返回了）
            mock_traverse.assert_not_called()
            # 验证有错误
            self.assertEqual(len(symbol_table["errors"]), 1)
            self.assertEqual(symbol_table["errors"][0]["type"], "return_outside_function")
            self.assertEqual(symbol_table["errors"][0]["message"], "Return statement outside function")
            self.assertEqual(symbol_table["errors"][0]["line"], 20)
            self.assertEqual(symbol_table["errors"][0]["column"], 1)

    def test_void_return_when_function_expects_type(self):
        """测试函数期望返回类型但 return 无返回值的情况"""
        node: AST = {
            "type": "return_statement",
            "line": 25,
            "column": 5,
            "expression": None  # 无返回值
        }
        
        symbol_table: SymbolTable = {
            "current_function": "bar",
            "functions": {
                "bar": {
                    "return_type": "int",
                    "params": [],
                    "line": 1,
                    "column": 0
                }
            },
            "errors": []
        }
        
        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_return_statement(node, symbol_table)
            
            # 验证 _traverse_node 没有被调用（因为 expression_node 是 None）
            mock_traverse.assert_not_called()
            # 验证有类型不匹配错误
            self.assertEqual(len(symbol_table["errors"]), 1)
            self.assertEqual(symbol_table["errors"][0]["type"], "return_type_mismatch")
            self.assertIn("expected 'int' but got 'void'", symbol_table["errors"][0]["message"])

    def test_void_return_when_function_expects_void(self):
        """测试函数期望 void 返回类型且 return 无返回值的情况"""
        node: AST = {
            "type": "return_statement",
            "line": 30,
            "column": 5,
            "expression": None  # 无返回值
        }
        
        symbol_table: SymbolTable = {
            "current_function": "baz",
            "functions": {
                "baz": {
                    "return_type": "void",
                    "params": [],
                    "line": 1,
                    "column": 0
                }
            },
            "errors": []
        }
        
        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_return_statement(node, symbol_table)
            
            # 验证 _traverse_node 没有被调用
            mock_traverse.assert_not_called()
            # 验证没有错误
            self.assertEqual(len(symbol_table["errors"]), 0)

    def test_void_return_when_function_has_no_return_type(self):
        """测试函数没有定义返回类型且 return 无返回值的情况"""
        node: AST = {
            "type": "return_statement",
            "line": 35,
            "column": 5,
            "expression": None  # 无返回值
        }
        
        symbol_table: SymbolTable = {
            "current_function": "qux",
            "functions": {
                "qux": {
                    "params": [],
                    "line": 1,
                    "column": 0
                }
            },
            "errors": []
        }
        
        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_return_statement(node, symbol_table)
            
            # 验证 _traverse_node 没有被调用
            mock_traverse.assert_not_called()
            # 验证没有错误
            self.assertEqual(len(symbol_table["errors"]), 0)

    def test_symbol_table_without_errors_key(self):
        """测试 symbol_table 初始没有 errors 键的情况"""
        node: AST = {
            "type": "return_statement",
            "line": 40,
            "column": 5,
            "expression": {
                "type": "literal",
                "value": 42,
                "data_type": "int",
                "line": 40,
                "column": 12
            }
        }
        
        symbol_table: SymbolTable = {
            "current_function": "main",
            "functions": {
                "main": {
                    "return_type": "int",
                    "params": [],
                    "line": 1,
                    "column": 0
                }
            }
            # 没有 errors 键
        }
        
        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_return_statement(node, symbol_table)
            
            # 验证 errors 键被创建
            self.assertIn("errors", symbol_table)
            self.assertIsInstance(symbol_table["errors"], list)
            # 验证没有错误
            self.assertEqual(len(symbol_table["errors"]), 0)

    def test_return_type_mismatch_char_vs_int(self):
        """测试 char 和 int 类型不匹配的情况"""
        node: AST = {
            "type": "return_statement",
            "line": 45,
            "column": 5,
            "expression": {
                "type": "literal",
                "value": 65,
                "data_type": "char",
                "line": 45,
                "column": 12
            }
        }
        
        symbol_table: SymbolTable = {
            "current_function": "test",
            "functions": {
                "test": {
                    "return_type": "int",
                    "params": [],
                    "line": 1,
                    "column": 0
                }
            },
            "errors": []
        }
        
        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_return_statement(node, symbol_table)
            
            # 验证有类型不匹配错误
            self.assertEqual(len(symbol_table["errors"]), 1)
            self.assertEqual(symbol_table["errors"][0]["type"], "return_type_mismatch")
            self.assertIn("expected 'int' but got 'char'", symbol_table["errors"][0]["message"])

    def test_return_type_mismatch_int_vs_char(self):
        """测试 int 和 char 类型不匹配的情况（反向）"""
        node: AST = {
            "type": "return_statement",
            "line": 50,
            "column": 5,
            "expression": {
                "type": "literal",
                "value": 42,
                "data_type": "int",
                "line": 50,
                "column": 12
            }
        }
        
        symbol_table: SymbolTable = {
            "current_function": "test",
            "functions": {
                "test": {
                    "return_type": "char",
                    "params": [],
                    "line": 1,
                    "column": 0
                }
            },
            "errors": []
        }
        
        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_return_statement(node, symbol_table)
            
            # 验证有类型不匹配错误
            self.assertEqual(len(symbol_table["errors"]), 1)
            self.assertEqual(symbol_table["errors"][0]["type"], "return_type_mismatch")
            self.assertIn("expected 'char' but got 'int'", symbol_table["errors"][0]["message"])

    def test_function_not_in_symbol_table(self):
        """测试当前函数不在 symbol_table 的 functions 中的情况"""
        node: AST = {
            "type": "return_statement",
            "line": 55,
            "column": 5,
            "expression": {
                "type": "literal",
                "value": 42,
                "data_type": "int",
                "line": 55,
                "column": 12
            }
        }
        
        symbol_table: SymbolTable = {
            "current_function": "unknown_func",
            "functions": {
                "other_func": {
                    "return_type": "int",
                    "params": [],
                    "line": 1,
                    "column": 0
                }
            },
            "errors": []
        }
        
        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_return_statement(node, symbol_table)
            
            # 验证 _traverse_node 被调用
            mock_traverse.assert_called_once()
            # 因为没有 expected_return_type，所以不应该有类型不匹配错误
            self.assertEqual(len(symbol_table["errors"]), 0)

    def test_expression_without_data_type(self):
        """测试表达式没有 data_type 字段的情况"""
        node: AST = {
            "type": "return_statement",
            "line": 60,
            "column": 5,
            "expression": {
                "type": "literal",
                "value": 42,
                # 没有 data_type 字段
                "line": 60,
                "column": 12
            }
        }
        
        symbol_table: SymbolTable = {
            "current_function": "main",
            "functions": {
                "main": {
                    "return_type": "int",
                    "params": [],
                    "line": 1,
                    "column": 0
                }
            },
            "errors": []
        }
        
        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_return_statement(node, symbol_table)
            
            # 验证 _traverse_node 被调用
            mock_traverse.assert_called_once()
            # 因为 actual_return_type 是 None，所以不应该有类型不匹配错误
            self.assertEqual(len(symbol_table["errors"]), 0)

    def test_node_without_line_column(self):
        """测试节点没有 line 和 column 字段的情况（边界值）"""
        node: AST = {
            "type": "return_statement",
            "expression": None
        }
        
        symbol_table: SymbolTable = {
            "current_function": None,
            "functions": {},
            "errors": []
        }
        
        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_return_statement(node, symbol_table)
            
            # 验证有错误，且 line 和 column 默认为 0
            self.assertEqual(len(symbol_table["errors"]), 1)
            self.assertEqual(symbol_table["errors"][0]["line"], 0)
            self.assertEqual(symbol_table["errors"][0]["column"], 0)

    def test_empty_symbol_table(self):
        """测试空的 symbol_table 的情况"""
        node: AST = {
            "type": "return_statement",
            "line": 1,
            "column": 1,
            "expression": None
        }
        
        symbol_table: SymbolTable = {}
        
        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_return_statement(node, symbol_table)
            
            # 验证 errors 被创建
            self.assertIn("errors", symbol_table)
            # 因为 current_function 是 None，应该有错误
            self.assertEqual(len(symbol_table["errors"]), 1)
            self.assertEqual(symbol_table["errors"][0]["type"], "return_outside_function")


if __name__ == "__main__":
    unittest.main()

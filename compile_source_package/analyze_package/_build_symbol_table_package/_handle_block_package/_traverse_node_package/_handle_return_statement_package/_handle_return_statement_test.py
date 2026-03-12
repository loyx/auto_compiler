# -*- coding: utf-8 -*-
"""
单元测试文件：_handle_return_statement
测试目标：验证 return_statement 节点处理逻辑，包括返回值类型检查
"""

import unittest
from unittest.mock import patch

# 相对导入被测试模块
import sys
import os
# 添加当前目录到路径以支持相对导入
_current_dir = os.path.dirname(os.path.abspath(__file__))
if _current_dir not in sys.path:
    sys.path.insert(0, _current_dir)

from _handle_return_statement_src import (
    _handle_return_statement,
    _extract_return_expression,
    _validate_return_type,
    AST,
    SymbolTable
)


class TestHandleReturnStatement(unittest.TestCase):
    """测试 _handle_return_statement 函数"""

    def setUp(self) -> None:
        """每个测试前的准备工作"""
        self.base_symbol_table: SymbolTable = {
            "variables": {},
            "functions": {
                "main": {
                    "return_type": "int",
                    "params": [],
                    "line": 1,
                    "column": 0
                }
            },
            "current_scope": 1,
            "scope_stack": [1],
            "current_function": "main",
            "errors": []
        }

    def test_happy_path_valid_return_type(self) -> None:
        """测试：返回值类型与函数声明匹配"""
        node: AST = {
            "type": "return_statement",
            "children": [
                {
                    "type": "literal",
                    "value": 42,
                    "data_type": "int",
                    "line": 5,
                    "column": 10
                }
            ],
            "line": 5,
            "column": 5
        }
        symbol_table = self.base_symbol_table.copy()
        symbol_table["errors"] = []

        with patch('_handle_return_statement_src._traverse_node') as mock_traverse_node:
            _handle_return_statement(node, symbol_table)
            
            # 验证 _traverse_node 被调用
            mock_traverse_node.assert_called_once()
            # 验证没有记录错误
            self.assertEqual(len(symbol_table.get("errors", [])), 0)

    def test_type_mismatch_error(self) -> None:
        """测试：返回值类型不匹配时记录错误"""
        node: AST = {
            "type": "return_statement",
            "children": [
                {
                    "type": "literal",
                    "value": "hello",
                    "data_type": "char",
                    "line": 5,
                    "column": 10
                }
            ],
            "line": 5,
            "column": 5
        }
        symbol_table = self.base_symbol_table.copy()
        symbol_table["errors"] = []

        with patch('_handle_return_statement_src._traverse_node') as mock_traverse_node:
            _handle_return_statement(node, symbol_table)
            
            # 验证记录了类型不匹配错误
            errors = symbol_table.get("errors", [])
            self.assertEqual(len(errors), 1)
            error = errors[0]
            self.assertEqual(error["type"], "return_type_mismatch")
            self.assertEqual(error["expected"], "int")
            self.assertEqual(error["actual"], "char")
            self.assertEqual(error["function"], "main")
            self.assertEqual(error["line"], 5)
            self.assertEqual(error["column"], 5)

    def test_void_return_no_expression(self) -> None:
        """测试：void return（无返回值）情况"""
        node: AST = {
            "type": "return_statement",
            "children": [],
            "line": 5,
            "column": 5
        }
        symbol_table = self.base_symbol_table.copy()
        symbol_table["errors"] = []

        with patch(
            'main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._handle_return_statement_src._traverse_node'
        ) as mock_traverse_node:
            _handle_return_statement(node, symbol_table)
            
            # 验证 _traverse_node 未被调用（没有返回值表达式）
            mock_traverse_node.assert_not_called()
            # 验证没有记录错误
            self.assertEqual(len(symbol_table.get("errors", [])), 0)

    def test_no_current_function(self) -> None:
        """测试：没有当前函数时不验证类型"""
        node: AST = {
            "type": "return_statement",
            "children": [
                {
                    "type": "literal",
                    "value": 42,
                    "data_type": "int",
                    "line": 5,
                    "column": 10
                }
            ],
            "line": 5,
            "column": 5
        }
        symbol_table = self.base_symbol_table.copy()
        symbol_table["current_function"] = None
        symbol_table["errors"] = []

        with patch('_handle_return_statement_src._traverse_node') as mock_traverse_node:
            _handle_return_statement(node, symbol_table)
            
            # 验证 _traverse_node 仍被调用（遍历表达式）
            mock_traverse_node.assert_called_once()
            # 但没有记录错误（因为没有 current_function）
            self.assertEqual(len(symbol_table.get("errors", [])), 0)

    def test_function_not_in_symbol_table(self) -> None:
        """测试：函数不在符号表中时不验证类型"""
        node: AST = {
            "type": "return_statement",
            "children": [
                {
                    "type": "literal",
                    "value": 42,
                    "data_type": "int",
                    "line": 5,
                    "column": 10
                }
            ],
            "line": 5,
            "column": 5
        }
        symbol_table = self.base_symbol_table.copy()
        symbol_table["current_function"] = "unknown_func"
        symbol_table["errors"] = []

        with patch('_handle_return_statement_src._traverse_node') as mock_traverse_node:
            _handle_return_statement(node, symbol_table)
            
            # 验证 _traverse_node 仍被调用
            mock_traverse_node.assert_called_once()
            # 但没有记录错误（因为函数不在符号表中）
            self.assertEqual(len(symbol_table.get("errors", [])), 0)

    def test_return_expression_from_value_field(self) -> None:
        """测试：从 value 字段获取返回值表达式"""
        node: AST = {
            "type": "return_statement",
            "value": {
                "type": "identifier",
                "value": "x",
                "data_type": "int",
                "line": 5,
                "column": 10
            },
            "line": 5,
            "column": 5
        }
        symbol_table = self.base_symbol_table.copy()
        symbol_table["errors"] = []

        with patch('_handle_return_statement_src._traverse_node') as mock_traverse_node:
            _handle_return_statement(node, symbol_table)
            
            # 验证 _traverse_node 被调用
            mock_traverse_node.assert_called_once()
            # 验证没有记录错误
            self.assertEqual(len(symbol_table.get("errors", [])), 0)

    def test_position_info_extraction(self) -> None:
        """测试：正确提取位置信息用于错误报告"""
        node: AST = {
            "type": "return_statement",
            "children": [
                {
                    "type": "literal",
                    "value": "test",
                    "data_type": "char",
                    "line": 10,
                    "column": 20
                }
            ],
            "line": 15,
            "column": 25
        }
        symbol_table = self.base_symbol_table.copy()
        symbol_table["errors"] = []

        with patch('_handle_return_statement_src._traverse_node') as mock_traverse_node:
            _handle_return_statement(node, symbol_table)
            
            errors = symbol_table.get("errors", [])
            self.assertEqual(len(errors), 1)
            # 错误位置应该是 return_statement 节点的位置
            self.assertEqual(errors[0]["line"], 15)
            self.assertEqual(errors[0]["column"], 25)

    def test_missing_line_column_defaults(self) -> None:
        """测试：缺少 line/column 时使用默认值"""
        node: AST = {
            "type": "return_statement",
            "children": [
                {
                    "type": "literal",
                    "value": "test",
                    "data_type": "char"
                }
            ]
        }
        symbol_table = self.base_symbol_table.copy()
        symbol_table["errors"] = []

        with patch('_handle_return_statement_src._traverse_node') as mock_traverse_node:
            _handle_return_statement(node, symbol_table)
            
            errors = symbol_table.get("errors", [])
            self.assertEqual(len(errors), 1)
            # 验证使用默认值 0
            self.assertEqual(errors[0]["line"], 0)
            self.assertEqual(errors[0]["column"], 0)


class TestExtractReturnExpression(unittest.TestCase):
    """测试 _extract_return_expression 辅助函数"""

    def test_extract_from_children_list(self) -> None:
        """测试：从 children 列表提取表达式"""
        node: AST = {
            "type": "return_statement",
            "children": [
                {
                    "type": "binary_expression",
                    "value": "+",
                    "data_type": "int"
                }
            ]
        }
        result = _extract_return_expression(node)
        self.assertIsNotNone(result)
        self.assertEqual(result["type"], "binary_expression")

    def test_extract_from_value_field(self) -> None:
        """测试：从 value 字段提取表达式"""
        node: AST = {
            "type": "return_statement",
            "value": {
                "type": "identifier",
                "value": "x"
            }
        }
        result = _extract_return_expression(node)
        self.assertIsNotNone(result)
        self.assertEqual(result["type"], "identifier")

    def test_children_priority_over_value(self) -> None:
        """测试：children 优先级高于 value"""
        node: AST = {
            "type": "return_statement",
            "children": [
                {
                    "type": "literal",
                    "value": 42
                }
            ],
            "value": {
                "type": "identifier",
                "value": "x"
            }
        }
        result = _extract_return_expression(node)
        self.assertIsNotNone(result)
        self.assertEqual(result["type"], "literal")

    def test_skip_void_type(self) -> None:
        """测试：跳过 void 类型的子节点"""
        node: AST = {
            "type": "return_statement",
            "children": [
                {"type": "void"},
                {
                    "type": "literal",
                    "value": 42
                }
            ]
        }
        result = _extract_return_expression(node)
        self.assertIsNotNone(result)
        self.assertEqual(result["type"], "literal")

    def test_empty_children_returns_none(self) -> None:
        """测试：空 children 且无 value 时返回 None"""
        node: AST = {
            "type": "return_statement",
            "children": []
        }
        result = _extract_return_expression(node)
        self.assertIsNone(result)

    def test_no_children_no_value_returns_none(self) -> None:
        """测试：无 children 和 value 时返回 None"""
        node: AST = {
            "type": "return_statement"
        }
        result = _extract_return_expression(node)
        self.assertIsNone(result)

    def test_non_dict_child_ignored(self) -> None:
        """测试：忽略非字典类型的子节点"""
        node: AST = {
            "type": "return_statement",
            "children": ["string", 123, None]
        }
        result = _extract_return_expression(node)
        # 应该返回 None 或第一个非 dict 元素（取决于实现）
        # 根据实现，会返回 children[0] 如果不是 dict 则返回 None
        self.assertIsNone(result)


class TestValidateReturnType(unittest.TestCase):
    """测试 _validate_return_type 辅助函数"""

    def setUp(self) -> None:
        """每个测试前的准备工作"""
        self.base_symbol_table: SymbolTable = {
            "variables": {},
            "functions": {
                "test_func": {
                    "return_type": "int",
                    "params": [],
                    "line": 1,
                    "column": 0
                }
            },
            "current_scope": 1,
            "scope_stack": [1],
            "current_function": "test_func",
            "errors": []
        }

    def test_matching_types_no_error(self) -> None:
        """测试：类型匹配时不记录错误"""
        return_expr: AST = {
            "type": "literal",
            "value": 42,
            "data_type": "int"
        }
        node: AST = {"type": "return_statement", "line": 5, "column": 10}
        symbol_table = self.base_symbol_table.copy()
        symbol_table["errors"] = []

        _validate_return_type(return_expr, node, symbol_table, 5, 10)
        self.assertEqual(len(symbol_table.get("errors", [])), 0)

    def test_mismatching_types_records_error(self) -> None:
        """测试：类型不匹配时记录错误"""
        return_expr: AST = {
            "type": "literal",
            "value": "hello",
            "data_type": "char"
        }
        node: AST = {"type": "return_statement", "line": 5, "column": 10}
        symbol_table = self.base_symbol_table.copy()
        symbol_table["errors"] = []

        _validate_return_type(return_expr, node, symbol_table, 5, 10)
        
        errors = symbol_table.get("errors", [])
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0]["type"], "return_type_mismatch")
        self.assertEqual(errors[0]["expected"], "int")
        self.assertEqual(errors[0]["actual"], "char")

    def test_no_data_type_in_expression(self) -> None:
        """测试：表达式没有 data_type 时不记录错误"""
        return_expr: AST = {
            "type": "literal",
            "value": 42
        }
        node: AST = {"type": "return_statement"}
        symbol_table = self.base_symbol_table.copy()
        symbol_table["errors"] = []

        _validate_return_type(return_expr, node, symbol_table, 5, 10)
        self.assertEqual(len(symbol_table.get("errors", [])), 0)

    def test_no_return_type_in_function(self) -> None:
        """测试：函数没有 return_type 时不记录错误"""
        return_expr: AST = {
            "type": "literal",
            "value": 42,
            "data_type": "int"
        }
        node: AST = {"type": "return_statement"}
        symbol_table = self.base_symbol_table.copy()
        symbol_table["functions"]["test_func"]["return_type"] = None
        symbol_table["errors"] = []

        _validate_return_type(return_expr, node, symbol_table, 5, 10)
        self.assertEqual(len(symbol_table.get("errors", [])), 0)

    def test_no_current_function(self) -> None:
        """测试：没有 current_function 时不记录错误"""
        return_expr: AST = {
            "type": "literal",
            "value": 42,
            "data_type": "int"
        }
        node: AST = {"type": "return_statement"}
        symbol_table = self.base_symbol_table.copy()
        symbol_table["current_function"] = None
        symbol_table["errors"] = []

        _validate_return_type(return_expr, node, symbol_table, 5, 10)
        self.assertEqual(len(symbol_table.get("errors", [])), 0)

    def test_error_appends_to_existing_list(self) -> None:
        """测试：错误追加到现有错误列表"""
        return_expr: AST = {
            "type": "literal",
            "value": "test",
            "data_type": "char"
        }
        node: AST = {"type": "return_statement"}
        symbol_table = self.base_symbol_table.copy()
        symbol_table["errors"] = [{"type": "existing_error"}]

        _validate_return_type(return_expr, node, symbol_table, 5, 10)
        
        errors = symbol_table.get("errors", [])
        self.assertEqual(len(errors), 2)
        self.assertEqual(errors[0]["type"], "existing_error")
        self.assertEqual(errors[1]["type"], "return_type_mismatch")


if __name__ == "__main__":
    unittest.main()

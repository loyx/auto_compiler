# -*- coding: utf-8 -*-
"""单元测试文件：_traverse_node 函数测试"""

import unittest
from unittest.mock import patch, MagicMock
from typing import Any, Dict

# 相对导入被测试模块
from ._traverse_node_src import _traverse_node

# 类型别名（与源文件保持一致）
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestTraverseNode(unittest.TestCase):
    """_traverse_node 函数单元测试类"""

    def setUp(self) -> None:
        """每个测试前的准备工作"""
        pass

    def tearDown(self) -> None:
        """每个测试后的清理工作"""
        pass

    def _create_symbol_table(self) -> SymbolTable:
        """创建标准符号表"""
        return {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
            "current_function": None,
            "errors": []
        }

    def test_block_node_with_children(self) -> None:
        """测试 block 类型节点，包含多个子节点"""
        symbol_table = self._create_symbol_table()
        node: AST = {
            "type": "block",
            "children": [
                {"type": "literal", "value": 1, "line": 1, "column": 1},
                {"type": "literal", "value": 2, "line": 2, "column": 1}
            ],
            "line": 0,
            "column": 0
        }

        # 不应抛出异常
        _traverse_node(node, symbol_table)

        # block 节点不应产生错误
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_block_node_empty_children(self) -> None:
        """测试 block 类型节点，空子节点列表"""
        symbol_table = self._create_symbol_table()
        node: AST = {
            "type": "block",
            "children": [],
            "line": 0,
            "column": 0
        }

        _traverse_node(node, symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_block_node_missing_children(self) -> None:
        """测试 block 类型节点，缺少 children 字段"""
        symbol_table = self._create_symbol_table()
        node: AST = {
            "type": "block",
            "line": 0,
            "column": 0
        }

        _traverse_node(node, symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 0)

    @patch("_traverse_node_src._handle_var_decl")
    def test_var_decl_node(self, mock_handle_var_decl: MagicMock) -> None:
        """测试 var_decl 类型节点，调用 _handle_var_decl"""
        symbol_table = self._create_symbol_table()
        node: AST = {
            "type": "var_decl",
            "name": "x",
            "data_type": "int",
            "line": 1,
            "column": 1
        }

        _traverse_node(node, symbol_table)

        # 验证 _handle_var_decl 被调用
        mock_handle_var_decl.assert_called_once_with(node, symbol_table)

    @patch("_traverse_node_src._handle_assignment")
    def test_assignment_node(self, mock_handle_assignment: MagicMock) -> None:
        """测试 assignment 类型节点，调用 _handle_assignment"""
        symbol_table = self._create_symbol_table()
        node: AST = {
            "type": "assignment",
            "target": "x",
            "value": {"type": "literal", "value": 10},
            "line": 1,
            "column": 1
        }

        _traverse_node(node, symbol_table)

        # 验证 _handle_assignment 被调用
        mock_handle_assignment.assert_called_once_with(node, symbol_table)

    def test_if_node_with_condition_and_body(self) -> None:
        """测试 if 类型节点，包含 condition 和 body"""
        symbol_table = self._create_symbol_table()
        condition_node: AST = {
            "type": "identifier",
            "name": "flag",
            "line": 1,
            "column": 1
        }
        body_node: AST = {
            "type": "literal",
            "value": 1,
            "line": 2,
            "column": 1
        }
        node: AST = {
            "type": "if",
            "condition": condition_node,
            "body": [body_node],
            "line": 0,
            "column": 0
        }

        _traverse_node(node, symbol_table)

        # condition 中的 identifier 未定义，应产生错误
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertEqual(symbol_table["errors"][0]["message"], "Undefined variable: flag")

    def test_if_node_missing_condition(self) -> None:
        """测试 if 类型节点，缺少 condition 字段"""
        symbol_table = self._create_symbol_table()
        node: AST = {
            "type": "if",
            "body": [{"type": "literal", "value": 1, "line": 1, "column": 1}],
            "line": 0,
            "column": 0
        }

        # 不应抛出异常
        _traverse_node(node, symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_if_node_missing_body(self) -> None:
        """测试 if 类型节点，缺少 body 字段"""
        symbol_table = self._create_symbol_table()
        node: AST = {
            "type": "if",
            "condition": {"type": "literal", "value": 1, "line": 1, "column": 1},
            "line": 0,
            "column": 0
        }

        # 不应抛出异常
        _traverse_node(node, symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_while_node_with_condition_and_body(self) -> None:
        """测试 while 类型节点，包含 condition 和 body"""
        symbol_table = self._create_symbol_table()
        condition_node: AST = {
            "type": "identifier",
            "name": "count",
            "line": 1,
            "column": 1
        }
        body_node: AST = {
            "type": "literal",
            "value": 1,
            "line": 2,
            "column": 1
        }
        node: AST = {
            "type": "while",
            "condition": condition_node,
            "body": [body_node],
            "line": 0,
            "column": 0
        }

        _traverse_node(node, symbol_table)

        # condition 中的 identifier 未定义，应产生错误
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertEqual(symbol_table["errors"][0]["message"], "Undefined variable: count")

    def test_while_node_missing_condition(self) -> None:
        """测试 while 类型节点，缺少 condition 字段"""
        symbol_table = self._create_symbol_table()
        node: AST = {
            "type": "while",
            "body": [{"type": "literal", "value": 1, "line": 1, "column": 1}],
            "line": 0,
            "column": 0
        }

        # 不应抛出异常
        _traverse_node(node, symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_while_node_missing_body(self) -> None:
        """测试 while 类型节点，缺少 body 字段"""
        symbol_table = self._create_symbol_table()
        node: AST = {
            "type": "while",
            "condition": {"type": "literal", "value": 1, "line": 1, "column": 1},
            "line": 0,
            "column": 0
        }

        # 不应抛出异常
        _traverse_node(node, symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 0)

    @patch("_traverse_node_src._handle_function_call")
    def test_function_call_node(self, mock_handle_function_call: MagicMock) -> None:
        """测试 function_call 类型节点，调用 _handle_function_call"""
        symbol_table = self._create_symbol_table()
        node: AST = {
            "type": "function_call",
            "name": "print",
            "args": [],
            "line": 1,
            "column": 1
        }

        _traverse_node(node, symbol_table)

        # 验证 _handle_function_call 被调用
        mock_handle_function_call.assert_called_once_with(node, symbol_table)

    def test_literal_node(self) -> None:
        """测试 literal 类型节点，无需特殊处理"""
        symbol_table = self._create_symbol_table()
        node: AST = {
            "type": "literal",
            "value": 42,
            "line": 1,
            "column": 1
        }

        _traverse_node(node, symbol_table)

        # literal 节点不应产生错误
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_identifier_node_undefined_variable(self) -> None:
        """测试 identifier 类型节点，变量未定义"""
        symbol_table = self._create_symbol_table()
        node: AST = {
            "type": "identifier",
            "name": "undefined_var",
            "line": 5,
            "column": 10
        }

        _traverse_node(node, symbol_table)

        # 应产生未定义变量错误
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["type"], "error")
        self.assertEqual(error["message"], "Undefined variable: undefined_var")
        self.assertEqual(error["line"], 5)
        self.assertEqual(error["column"], 10)

    def test_identifier_node_defined_variable(self) -> None:
        """测试 identifier 类型节点，变量已定义"""
        symbol_table = self._create_symbol_table()
        symbol_table["variables"]["defined_var"] = {
            "data_type": "int",
            "is_declared": True,
            "line": 1,
            "column": 1,
            "scope_level": 0
        }
        node: AST = {
            "type": "identifier",
            "name": "defined_var",
            "line": 5,
            "column": 10
        }

        _traverse_node(node, symbol_table)

        # 不应产生错误
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_identifier_node_missing_name(self) -> None:
        """测试 identifier 类型节点，缺少 name 字段"""
        symbol_table = self._create_symbol_table()
        node: AST = {
            "type": "identifier",
            "line": 1,
            "column": 1
        }

        # 不应抛出异常
        _traverse_node(node, symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_unknown_node_type_with_children(self) -> None:
        """测试未知类型节点，包含子节点"""
        symbol_table = self._create_symbol_table()
        node: AST = {
            "type": "unknown_type",
            "children": [
                {"type": "literal", "value": 1, "line": 1, "column": 1},
                {"type": "identifier", "name": "x", "line": 2, "column": 1}
            ],
            "line": 0,
            "column": 0
        }

        _traverse_node(node, symbol_table)

        # 子节点中的 identifier 未定义，应产生错误
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertEqual(symbol_table["errors"][0]["message"], "Undefined variable: x")

    def test_unknown_node_type_empty_children(self) -> None:
        """测试未知类型节点，空子节点列表"""
        symbol_table = self._create_symbol_table()
        node: AST = {
            "type": "unknown_type",
            "children": [],
            "line": 0,
            "column": 0
        }

        _traverse_node(node, symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_node_missing_type_field(self) -> None:
        """测试节点缺少 type 字段"""
        symbol_table = self._create_symbol_table()
        node: AST = {
            "line": 0,
            "column": 0
        }

        # 不应抛出异常，应进入 else 分支处理 children
        _traverse_node(node, symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_nested_block_structure(self) -> None:
        """测试嵌套 block 结构"""
        symbol_table = self._create_symbol_table()
        node: AST = {
            "type": "block",
            "children": [
                {
                    "type": "block",
                    "children": [
                        {"type": "identifier", "name": "inner_var", "line": 3, "column": 1}
                    ],
                    "line": 2,
                    "column": 0
                },
                {"type": "identifier", "name": "outer_var", "line": 4, "column": 1}
            ],
            "line": 0,
            "column": 0
        }

        _traverse_node(node, symbol_table)

        # 两个 identifier 都未定义，应产生两个错误
        self.assertEqual(len(symbol_table["errors"]), 2)
        messages = [err["message"] for err in symbol_table["errors"]]
        self.assertIn("Undefined variable: inner_var", messages)
        self.assertIn("Undefined variable: outer_var", messages)

    def test_mixed_node_types(self) -> None:
        """测试混合多种节点类型"""
        symbol_table = self._create_symbol_table()
        symbol_table["variables"]["declared_var"] = {
            "data_type": "int",
            "is_declared": True,
            "line": 1,
            "column": 1,
            "scope_level": 0
        }
        node: AST = {
            "type": "block",
            "children": [
                {"type": "literal", "value": 10, "line": 1, "column": 1},
                {"type": "identifier", "name": "declared_var", "line": 2, "column": 1},
                {"type": "identifier", "name": "undefined_var", "line": 3, "column": 1}
            ],
            "line": 0,
            "column": 0
        }

        _traverse_node(node, symbol_table)

        # 只有 undefined_var 应产生错误
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertEqual(symbol_table["errors"][0]["message"], "Undefined variable: undefined_var")

    def test_recursive_traversal_depth(self) -> None:
        """测试递归遍历深度"""
        symbol_table = self._create_symbol_table()
        # 构建深层嵌套结构
        node: AST = {"type": "literal", "value": 0, "line": 0, "column": 0}
        for i in range(10):
            node = {
                "type": "block",
                "children": [node],
                "line": i + 1,
                "column": 0
            }

        # 不应抛出异常
        _traverse_node(node, symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 0)


if __name__ == "__main__":
    unittest.main()

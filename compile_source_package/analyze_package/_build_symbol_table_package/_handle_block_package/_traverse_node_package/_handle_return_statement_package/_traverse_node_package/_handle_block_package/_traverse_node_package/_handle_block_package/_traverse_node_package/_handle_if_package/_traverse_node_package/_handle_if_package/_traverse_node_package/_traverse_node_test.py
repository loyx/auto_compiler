# -*- coding: utf-8 -*-
"""单元测试文件：_traverse_node 函数测试"""

import unittest
from unittest.mock import patch, MagicMock, call
from typing import Any, Dict

# 相对导入被测模块
from ._traverse_node_src import _traverse_node, _traverse_children, _record_unknown_node_error, _record_traversal_error


class TestTraverseNode(unittest.TestCase):
    """_traverse_node 函数的单元测试类"""

    def setUp(self) -> None:
        """每个测试前的准备工作"""
        self.symbol_table: Dict[str, Any] = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
            "current_function": None,
            "errors": []
        }

    def _create_node(self, node_type: str, **kwargs) -> Dict[str, Any]:
        """辅助函数：创建 AST 节点"""
        node = {"type": node_type}
        node.update(kwargs)
        return node

    # ==================== Happy Path 测试 ====================

    @patch('._traverse_node_src._handle_if')
    def test_traverse_node_if_type(self, mock_handle_if: MagicMock) -> None:
        """测试 if 类型节点分发到 _handle_if"""
        node = self._create_node("if", line=1, column=0)
        _traverse_node(node, self.symbol_table)
        mock_handle_if.assert_called_once_with(node, self.symbol_table)

    @patch('._traverse_node_src._handle_while')
    def test_traverse_node_while_type(self, mock_handle_while: MagicMock) -> None:
        """测试 while 类型节点分发到 _handle_while"""
        node = self._create_node("while", line=5, column=4)
        _traverse_node(node, self.symbol_table)
        mock_handle_while.assert_called_once_with(node, self.symbol_table)

    @patch('._traverse_node_src._handle_for')
    def test_traverse_node_for_type(self, mock_handle_for: MagicMock) -> None:
        """测试 for 类型节点分发到 _handle_for"""
        node = self._create_node("for", line=10, column=0)
        _traverse_node(node, self.symbol_table)
        mock_handle_for.assert_called_once_with(node, self.symbol_table)

    @patch('._traverse_node_src._handle_function_def')
    def test_traverse_node_function_def_type(self, mock_handle_function_def: MagicMock) -> None:
        """测试 function_def 类型节点分发到 _handle_function_def"""
        node = self._create_node("function_def", line=15, column=0)
        _traverse_node(node, self.symbol_table)
        mock_handle_function_def.assert_called_once_with(node, self.symbol_table)

    @patch('._traverse_node_src._handle_variable_def')
    def test_traverse_node_variable_def_type(self, mock_handle_variable_def: MagicMock) -> None:
        """测试 variable_def 类型节点分发到 _handle_variable_def"""
        node = self._create_node("variable_def", line=20, column=4, value=42)
        _traverse_node(node, self.symbol_table)
        mock_handle_variable_def.assert_called_once_with(node, self.symbol_table)

    @patch('._traverse_node_src._traverse_children')
    def test_traverse_node_block_type(self, mock_traverse_children: MagicMock) -> None:
        """测试 block 类型节点调用 _traverse_children"""
        node = self._create_node("block", line=0, column=0)
        _traverse_node(node, self.symbol_table)
        mock_traverse_children.assert_called_once_with(node, self.symbol_table)

    @patch('._traverse_node_src._traverse_children')
    def test_traverse_node_program_type(self, mock_traverse_children: MagicMock) -> None:
        """测试 program 类型节点调用 _traverse_children"""
        node = self._create_node("program", line=0, column=0)
        _traverse_node(node, self.symbol_table)
        mock_traverse_children.assert_called_once_with(node, self.symbol_table)

    def test_traverse_node_break_type(self) -> None:
        """测试 break 类型节点无需特殊处理"""
        node = self._create_node("break", line=25, column=8)
        _traverse_node(node, self.symbol_table)
        # 不应有任何副作用
        self.assertEqual(len(self.symbol_table["errors"]), 0)

    def test_traverse_node_continue_type(self) -> None:
        """测试 continue 类型节点无需特殊处理"""
        node = self._create_node("continue", line=26, column=8)
        _traverse_node(node, self.symbol_table)
        self.assertEqual(len(self.symbol_table["errors"]), 0)

    def test_traverse_node_return_type(self) -> None:
        """测试 return 类型节点无需特殊处理"""
        node = self._create_node("return", line=27, column=8, value=100)
        _traverse_node(node, self.symbol_table)
        self.assertEqual(len(self.symbol_table["errors"]), 0)

    @patch('._traverse_node_src._traverse_children')
    def test_traverse_node_binary_op_type(self, mock_traverse_children: MagicMock) -> None:
        """测试 binary_op 类型节点调用 _traverse_children"""
        node = self._create_node("binary_op", line=30, column=0, value="+")
        _traverse_node(node, self.symbol_table)
        mock_traverse_children.assert_called_once_with(node, self.symbol_table)

    @patch('._traverse_node_src._traverse_children')
    def test_traverse_node_unary_op_type(self, mock_traverse_children: MagicMock) -> None:
        """测试 unary_op 类型节点调用 _traverse_children"""
        node = self._create_node("unary_op", line=31, column=0, value="-")
        _traverse_node(node, self.symbol_table)
        mock_traverse_children.assert_called_once_with(node, self.symbol_table)

    @patch('._traverse_node_src._traverse_children')
    def test_traverse_node_call_type(self, mock_traverse_children: MagicMock) -> None:
        """测试 call 类型节点调用 _traverse_children"""
        node = self._create_node("call", line=32, column=0)
        _traverse_node(node, self.symbol_table)
        mock_traverse_children.assert_called_once_with(node, self.symbol_table)

    def test_traverse_node_literal_type(self) -> None:
        """测试 literal 类型节点无需遍历"""
        node = self._create_node("literal", line=33, column=0, value=42)
        _traverse_node(node, self.symbol_table)
        self.assertEqual(len(self.symbol_table["errors"]), 0)

    def test_traverse_node_identifier_type(self) -> None:
        """测试 identifier 类型节点无需遍历"""
        node = self._create_node("identifier", line=34, column=0, value="x")
        _traverse_node(node, self.symbol_table)
        self.assertEqual(len(self.symbol_table["errors"]), 0)

    # ==================== 未知节点类型测试 ====================

    @patch('._traverse_node_src._record_unknown_node_error')
    @patch('._traverse_node_src._traverse_children')
    def test_traverse_node_unknown_type(self, mock_traverse_children: MagicMock, 
                                         mock_record_error: MagicMock) -> None:
        """测试未知节点类型记录错误并遍历 children"""
        node = self._create_node("unknown_type", line=40, column=0)
        _traverse_node(node, self.symbol_table)
        mock_record_error.assert_called_once_with(node, self.symbol_table)
        mock_traverse_children.assert_called_once_with(node, self.symbol_table)

    @patch('._traverse_node_src._traverse_children')
    def test_traverse_node_unknown_type_records_error(self, mock_traverse_children: MagicMock) -> None:
        """测试未知节点类型实际记录错误到 symbol_table"""
        node = self._create_node("custom_node", line=41, column=5)
        _traverse_node(node, self.symbol_table)
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        error = self.symbol_table["errors"][0]
        self.assertEqual(error["type"], "unknown_node_type")
        self.assertIn("custom_node", error["message"])
        self.assertEqual(error["line"], 41)
        self.assertEqual(error["column"], 5)

    # ==================== 边界值测试 ====================

    def test_traverse_node_missing_type_field(self) -> None:
        """测试节点缺少 type 字段时的处理"""
        node: Dict[str, Any] = {"line": 50, "column": 0}
        _traverse_node(node, self.symbol_table)
        # 空字符串 type 应被视为未知类型
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        error = self.symbol_table["errors"][0]
        self.assertEqual(error["type"], "unknown_node_type")

    def test_traverse_node_empty_dict(self) -> None:
        """测试空字典节点的处理"""
        node: Dict[str, Any] = {}
        _traverse_node(node, self.symbol_table)
        # 应记录未知类型错误
        self.assertEqual(len(self.symbol_table["errors"]), 1)

    @patch('._traverse_node_src._handle_if')
    def test_traverse_node_with_children(self, mock_handle_if: MagicMock) -> None:
        """测试带有 children 的节点"""
        child1 = self._create_node("literal", value=1)
        child2 = self._create_node("identifier", value="x")
        node = self._create_node("if", line=1, column=0, children=[child1, child2])
        _traverse_node(node, self.symbol_table)
        mock_handle_if.assert_called_once_with(node, self.symbol_table)

    def test_traverse_node_none_value(self) -> None:
        """测试节点 value 为 None 的情况"""
        node = self._create_node("literal", line=60, column=0, value=None)
        _traverse_node(node, self.symbol_table)
        self.assertEqual(len(self.symbol_table["errors"]), 0)

    # ==================== 异常处理测试 ====================

    @patch('._traverse_node_src._handle_if', side_effect=RuntimeError("Mocked error"))
    def test_traverse_node_handler_exception(self, mock_handle_if: MagicMock) -> None:
        """测试处理函数抛出异常时的错误记录"""
        node = self._create_node("if", line=70, column=0)
        _traverse_node(node, self.symbol_table)
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        error = self.symbol_table["errors"][0]
        self.assertEqual(error["type"], "traversal_error")
        self.assertEqual(error["message"], "Mocked error")
        self.assertEqual(error["line"], 70)
        self.assertEqual(error["column"], 0)

    @patch('._traverse_node_src._traverse_children', side_effect=ValueError("Children error"))
    def test_traverse_node_traverse_children_exception(self, mock_traverse_children: MagicMock) -> None:
        """测试 _traverse_children 抛出异常时的错误记录"""
        node = self._create_node("block", line=71, column=4)
        _traverse_node(node, self.symbol_table)
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        error = self.symbol_table["errors"][0]
        self.assertEqual(error["type"], "traversal_error")
        self.assertEqual(error["message"], "Children error")

    # ==================== 递归遍历测试 ====================

    @patch('._traverse_node_src._handle_variable_def')
    @patch('._traverse_node_src._handle_if')
    def test_traverse_node_recursive_traversal(self, mock_handle_if: MagicMock, 
                                                mock_handle_variable_def: MagicMock) -> None:
        """测试嵌套节点的递归遍历"""
        # 创建嵌套结构：program -> block -> [variable_def, if]
        var_node = self._create_node("variable_def", line=80, column=4)
        if_node = self._create_node("if", line=81, column=4)
        block_node = self._create_node("block", line=79, column=0, children=[var_node, if_node])
        program_node = self._create_node("program", line=0, column=0, children=[block_node])

        _traverse_node(program_node, self.symbol_table)

        # 验证递归调用
        self.assertEqual(mock_handle_variable_def.call_count, 1)
        self.assertEqual(mock_handle_if.call_count, 1)

    # ==================== SymbolTable 副作用测试 ====================

    def test_traverse_node_error_accumulation(self) -> None:
        """测试多个错误能够累积到 symbol_table"""
        node1 = self._create_node("unknown1", line=90, column=0)
        node2 = self._create_node("unknown2", line=91, column=0)
        node3 = self._create_node("unknown3", line=92, column=0)

        _traverse_node(node1, self.symbol_table)
        _traverse_node(node2, self.symbol_table)
        _traverse_node(node3, self.symbol_table)

        self.assertEqual(len(self.symbol_table["errors"]), 3)

    def test_traverse_node_symbol_table_not_modified_for_known_types(self) -> None:
        """测试已知类型节点不修改 symbol_table（除了 errors）"""
        original_scope = self.symbol_table["current_scope"]
        original_vars = len(self.symbol_table["variables"])
        original_funcs = len(self.symbol_table["functions"])

        node = self._create_node("literal", line=100, column=0, value=42)
        _traverse_node(node, self.symbol_table)

        self.assertEqual(self.symbol_table["current_scope"], original_scope)
        self.assertEqual(len(self.symbol_table["variables"]), original_vars)
        self.assertEqual(len(self.symbol_table["functions"]), original_funcs)


class TestTraverseChildren(unittest.TestCase):
    """_traverse_children 辅助函数的单元测试"""

    def setUp(self) -> None:
        self.symbol_table: Dict[str, Any] = {"errors": []}

    @patch('._traverse_node_src._traverse_node')
    def test_traverse_children_empty_list(self, mock_traverse_node: MagicMock) -> None:
        """测试空 children 列表"""
        node = {"type": "block", "children": []}
        _traverse_children(node, self.symbol_table)
        mock_traverse_node.assert_not_called()

    @patch('._traverse_node_src._traverse_node')
    def test_traverse_children_single_child(self, mock_traverse_node: MagicMock) -> None:
        """测试单个 child"""
        child = {"type": "literal", "value": 1}
        node = {"type": "block", "children": [child]}
        _traverse_children(node, self.symbol_table)
        mock_traverse_node.assert_called_once_with(child, self.symbol_table)

    @patch('._traverse_node_src._traverse_node')
    def test_traverse_children_multiple_children(self, mock_traverse_node: MagicMock) -> None:
        """测试多个 children"""
        child1 = {"type": "literal", "value": 1}
        child2 = {"type": "identifier", "value": "x"}
        child3 = {"type": "binary_op", "value": "+"}
        node = {"type": "block", "children": [child1, child2, child3]}
        _traverse_children(node, self.symbol_table)
        self.assertEqual(mock_traverse_node.call_count, 3)
        mock_traverse_node.assert_has_calls([
            call(child1, self.symbol_table),
            call(child2, self.symbol_table),
            call(child3, self.symbol_table)
        ])

    @patch('._traverse_node_src._traverse_node')
    def test_traverse_children_missing_children_field(self, mock_traverse_node: MagicMock) -> None:
        """测试节点缺少 children 字段"""
        node = {"type": "block"}
        _traverse_children(node, self.symbol_table)
        mock_traverse_node.assert_not_called()


class TestRecordUnknownNodeError(unittest.TestCase):
    """_record_unknown_node_error 辅助函数的单元测试"""

    def test_record_unknown_node_error_basic(self) -> None:
        """测试基本错误记录"""
        symbol_table: Dict[str, Any] = {"errors": []}
        node = {"type": "custom_type", "line": 10, "column": 5}
        _record_unknown_node_error(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["type"], "unknown_node_type")
        self.assertIn("custom_type", error["message"])
        self.assertEqual(error["line"], 10)
        self.assertEqual(error["column"], 5)
        self.assertEqual(error["node_type"], "custom_type")

    def test_record_unknown_node_error_missing_fields(self) -> None:
        """测试节点缺少 line/column 字段"""
        symbol_table: Dict[str, Any] = {"errors": []}
        node = {"type": "unknown"}
        _record_unknown_node_error(node, symbol_table)

        error = symbol_table["errors"][0]
        self.assertIsNone(error["line"])
        self.assertIsNone(error["column"])

    def test_record_unknown_node_error_creates_errors_list(self) -> None:
        """测试 symbol_table 没有 errors 字段时自动创建"""
        symbol_table: Dict[str, Any] = {}
        node = {"type": "unknown", "line": 1, "column": 0}
        _record_unknown_node_error(node, symbol_table)

        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)


class TestRecordTraversalError(unittest.TestCase):
    """_record_traversal_error 辅助函数的单元测试"""

    def test_record_traversal_error_basic(self) -> None:
        """测试基本错误记录"""
        symbol_table: Dict[str, Any] = {"errors": []}
        node = {"type": "if", "line": 20, "column": 4}
        _record_traversal_error(node, symbol_table, "Something went wrong")

        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["type"], "traversal_error")
        self.assertEqual(error["message"], "Something went wrong")
        self.assertEqual(error["line"], 20)
        self.assertEqual(error["column"], 4)
        self.assertEqual(error["node_type"], "if")

    def test_record_traversal_error_empty_message(self) -> None:
        """测试空错误消息"""
        symbol_table: Dict[str, Any] = {"errors": []}
        node = {"type": "block", "line": 0, "column": 0}
        _record_traversal_error(node, symbol_table, "")

        error = symbol_table["errors"][0]
        self.assertEqual(error["message"], "")

    def test_record_traversal_error_creates_errors_list(self) -> None:
        """测试 symbol_table 没有 errors 字段时自动创建"""
        symbol_table: Dict[str, Any] = {}
        node = {"type": "for"}
        _record_traversal_error(node, symbol_table, "Error")

        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)


if __name__ == "__main__":
    unittest.main()

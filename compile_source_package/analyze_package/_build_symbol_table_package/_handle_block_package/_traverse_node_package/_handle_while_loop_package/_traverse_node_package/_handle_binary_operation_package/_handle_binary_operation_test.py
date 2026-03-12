"""
单元测试文件：_handle_binary_operation 函数测试
"""
import unittest
from unittest.mock import patch, MagicMock
from typing import Dict, Any

# 相对导入被测试模块
from ._handle_binary_operation_src import _handle_binary_operation

# 类型别名（与被测模块保持一致）
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleBinaryOperation(unittest.TestCase):
    """_handle_binary_operation 函数的单元测试类"""

    def setUp(self) -> None:
        """测试前准备"""
        self.symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }

    @patch("projects.cc.files.main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._handle_binary_operation_package._handle_binary_operation_src._traverse_node")
    def test_both_left_and_right_exist(self, mock_traverse_node: MagicMock) -> None:
        """测试 left 和 right 都存在的正常情况"""
        node: AST = {
            "type": "binary_operation",
            "operator": "+",
            "left": {"type": "number", "value": 1},
            "right": {"type": "number", "value": 2}
        }

        _handle_binary_operation(node, self.symbol_table)

        # 验证 _traverse_node 被调用了两次
        self.assertEqual(mock_traverse_node.call_count, 2)
        # 验证第一次调用使用 left 节点
        mock_traverse_node.assert_any_call(node["left"], self.symbol_table)
        # 验证第二次调用使用 right 节点
        mock_traverse_node.assert_any_call(node["right"], self.symbol_table)

    @patch("projects.cc.files.main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._handle_binary_operation_package._handle_binary_operation_src._traverse_node")
    def test_left_is_none(self, mock_traverse_node: MagicMock) -> None:
        """测试 left 为 None 的情况"""
        node: AST = {
            "type": "binary_operation",
            "operator": "+",
            "left": None,
            "right": {"type": "number", "value": 2}
        }

        _handle_binary_operation(node, self.symbol_table)

        # 验证 _traverse_node 只被调用了一次（仅 right）
        self.assertEqual(mock_traverse_node.call_count, 1)
        mock_traverse_node.assert_called_once_with(node["right"], self.symbol_table)

    @patch("projects.cc.files.main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._handle_binary_operation_package._handle_binary_operation_src._traverse_node")
    def test_right_is_none(self, mock_traverse_node: MagicMock) -> None:
        """测试 right 为 None 的情况"""
        node: AST = {
            "type": "binary_operation",
            "operator": "+",
            "left": {"type": "number", "value": 1},
            "right": None
        }

        _handle_binary_operation(node, self.symbol_table)

        # 验证 _traverse_node 只被调用了一次（仅 left）
        self.assertEqual(mock_traverse_node.call_count, 1)
        mock_traverse_node.assert_called_once_with(node["left"], self.symbol_table)

    @patch("projects.cc.files.main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._handle_binary_operation_package._handle_binary_operation_src._traverse_node")
    def test_both_left_and_right_are_none(self, mock_traverse_node: MagicMock) -> None:
        """测试 left 和 right 都为 None 的边界情况"""
        node: AST = {
            "type": "binary_operation",
            "operator": "+",
            "left": None,
            "right": None
        }

        _handle_binary_operation(node, self.symbol_table)

        # 验证 _traverse_node 没有被调用
        self.assertEqual(mock_traverse_node.call_count, 0)

    @patch("projects.cc.files.main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._handle_binary_operation_package._handle_binary_operation_src._traverse_node")
    def test_missing_left_key(self, mock_traverse_node: MagicMock) -> None:
        """测试 node 中缺少 left 键的情况"""
        node: AST = {
            "type": "binary_operation",
            "operator": "+",
            "right": {"type": "number", "value": 2}
        }

        _handle_binary_operation(node, self.symbol_table)

        # 验证 _traverse_node 只被调用了一次（仅 right）
        self.assertEqual(mock_traverse_node.call_count, 1)
        mock_traverse_node.assert_called_once_with(node["right"], self.symbol_table)

    @patch("projects.cc.files.main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._handle_binary_operation_package._handle_binary_operation_src._traverse_node")
    def test_missing_right_key(self, mock_traverse_node: MagicMock) -> None:
        """测试 node 中缺少 right 键的情况"""
        node: AST = {
            "type": "binary_operation",
            "operator": "+",
            "left": {"type": "number", "value": 1}
        }

        _handle_binary_operation(node, self.symbol_table)

        # 验证 _traverse_node 只被调用了一次（仅 left）
        self.assertEqual(mock_traverse_node.call_count, 1)
        mock_traverse_node.assert_called_once_with(node["left"], self.symbol_table)

    @patch("projects.cc.files.main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._handle_binary_operation_package._handle_binary_operation_src._traverse_node")
    def test_empty_node(self, mock_traverse_node: MagicMock) -> None:
        """测试空节点的情况"""
        node: AST = {}

        _handle_binary_operation(node, self.symbol_table)

        # 验证 _traverse_node 没有被调用
        self.assertEqual(mock_traverse_node.call_count, 0)

    @patch("projects.cc.files.main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._handle_binary_operation_package._handle_binary_operation_src._traverse_node")
    def test_nested_binary_operation(self, mock_traverse_node: MagicMock) -> None:
        """测试嵌套的 binary_operation 节点"""
        nested_node: AST = {
            "type": "binary_operation",
            "operator": "*",
            "left": {"type": "number", "value": 3},
            "right": {"type": "number", "value": 4}
        }
        node: AST = {
            "type": "binary_operation",
            "operator": "+",
            "left": nested_node,
            "right": {"type": "number", "value": 2}
        }

        _handle_binary_operation(node, self.symbol_table)

        # 验证 _traverse_node 被调用了两次
        self.assertEqual(mock_traverse_node.call_count, 2)
        # 验证调用参数
        mock_traverse_node.assert_any_call(nested_node, self.symbol_table)
        mock_traverse_node.assert_any_call(node["right"], self.symbol_table)

    @patch("projects.cc.files.main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._handle_binary_operation_package._handle_binary_operation_src._traverse_node")
    def test_symbol_table_passed_correctly(self, mock_traverse_node: MagicMock) -> None:
        """验证 symbol_table 正确传递给 _traverse_node"""
        node: AST = {
            "type": "binary_operation",
            "operator": "+",
            "left": {"type": "number", "value": 1},
            "right": {"type": "number", "value": 2}
        }

        custom_symbol_table: SymbolTable = {
            "variables": {"x": {"value": 10}},
            "functions": {},
            "current_scope": 1,
            "scope_stack": [0, 1]
        }

        _handle_binary_operation(node, custom_symbol_table)

        # 验证两次调用都使用了同一个 symbol_table 对象
        calls = mock_traverse_node.call_args_list
        self.assertEqual(len(calls), 2)
        self.assertIs(calls[0][0][1], custom_symbol_table)
        self.assertIs(calls[1][0][1], custom_symbol_table)

    @patch("_handle_binary_operation_package._handle_binary_operation_src._traverse_node")
    def test_call_order_left_then_right(self, mock_traverse_node: MagicMock) -> None:
        """验证调用顺序：先 left 后 right"""
        node: AST = {
            "type": "binary_operation",
            "operator": "+",
            "left": {"type": "number", "value": 1},
            "right": {"type": "number", "value": 2}
        }

        _handle_binary_operation(node, self.symbol_table)

        # 验证调用顺序
        calls = mock_traverse_node.call_args_list
        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[0][0][0], node["left"])
        self.assertEqual(calls[1][0][0], node["right"])


if __name__ == "__main__":
    unittest.main()

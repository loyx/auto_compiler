"""
单元测试文件：_handle_program 函数测试
"""
import unittest
from unittest.mock import patch
from typing import Dict, Any

# 相对导入被测函数
from ._handle_program_src import _handle_program

# 类型定义（与被测模块保持一致）
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleProgram(unittest.TestCase):
    """_handle_program 函数的单元测试类"""

    def setUp(self):
        """每个测试前的准备工作"""
        self.symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
        }

    @patch("._traverse_node_package._traverse_node_src._traverse_node")
    def test_handle_program_with_children(self, mock_traverse_node):
        """测试 program 节点包含子节点的情况"""
        # 准备测试数据
        child1: AST = {"type": "function_declaration", "value": "func1"}
        child2: AST = {"type": "variable_declaration", "value": "var1"}
        child3: AST = {"type": "block", "value": "block1"}
        
        node: AST = {
            "type": "program",
            "children": [child1, child2, child3]
        }
        
        # 执行测试
        _handle_program(node, self.symbol_table)
        
        # 验证 _traverse_node 被调用了 3 次
        self.assertEqual(mock_traverse_node.call_count, 3)
        
        # 验证每次调用的参数
        mock_traverse_node.assert_any_call(child1, self.symbol_table)
        mock_traverse_node.assert_any_call(child2, self.symbol_table)
        mock_traverse_node.assert_any_call(child3, self.symbol_table)

    @patch("._traverse_node_package._traverse_node_src._traverse_node")
    def test_handle_program_with_empty_children(self, mock_traverse_node):
        """测试 program 节点包含空 children 列表的情况"""
        node: AST = {
            "type": "program",
            "children": []
        }
        
        # 执行测试
        _handle_program(node, self.symbol_table)
        
        # 验证 _traverse_node 没有被调用
        mock_traverse_node.assert_not_called()

    @patch("._traverse_node_package._traverse_node_src._traverse_node")
    def test_handle_program_without_children_key(self, mock_traverse_node):
        """测试 program 节点没有 children 键的情况"""
        node: AST = {
            "type": "program"
        }
        
        # 执行测试
        _handle_program(node, self.symbol_table)
        
        # 验证 _traverse_node 没有被调用
        mock_traverse_node.assert_not_called()

    @patch("._traverse_node_package._traverse_node_src._traverse_node")
    def test_handle_program_with_single_child(self, mock_traverse_node):
        """测试 program 节点只有一个子节点的情况"""
        child: AST = {"type": "function_declaration", "value": "main"}
        
        node: AST = {
            "type": "program",
            "children": [child]
        }
        
        # 执行测试
        _handle_program(node, self.symbol_table)
        
        # 验证 _traverse_node 被调用了 1 次
        self.assertEqual(mock_traverse_node.call_count, 1)
        mock_traverse_node.assert_called_once_with(child, self.symbol_table)

    @patch("._traverse_node_package._traverse_node_src._traverse_node")
    def test_handle_program_symbol_table_passed_unchanged(self, mock_traverse_node):
        """测试 symbol_table 被原样传递给 _traverse_node"""
        child: AST = {"type": "function_declaration", "value": "func1"}
        node: AST = {
            "type": "program",
            "children": [child]
        }
        
        # 创建一个特殊的 symbol_table 用于验证
        special_symbol_table: SymbolTable = {
            "variables": {"x": {"data_type": "int"}},
            "functions": {},
            "current_scope": 1,
            "scope_stack": [0, 1],
            "custom_key": "custom_value"
        }
        
        # 执行测试
        _handle_program(node, special_symbol_table)
        
        # 验证 symbol_table 被原样传递（同一个对象引用）
        mock_traverse_node.assert_called_once()
        called_args = mock_traverse_node.call_args
        self.assertIs(called_args[0][1], special_symbol_table)

    @patch("._traverse_node_package._traverse_node_src._traverse_node")
    def test_handle_program_preserves_child_node_structure(self, mock_traverse_node):
        """测试子节点结构被完整传递给 _traverse_node"""
        child: AST = {
            "type": "function_declaration",
            "name": "test_func",
            "params": [{"name": "a", "type": "int"}],
            "body": {"type": "block", "children": []},
            "line": 10,
            "column": 5
        }
        node: AST = {
            "type": "program",
            "children": [child]
        }
        
        # 执行测试
        _handle_program(node, self.symbol_table)
        
        # 验证子节点被完整传递
        mock_traverse_node.assert_called_once()
        called_args = mock_traverse_node.call_args
        passed_child = called_args[0][0]
        self.assertEqual(passed_child, child)


if __name__ == "__main__":
    unittest.main()

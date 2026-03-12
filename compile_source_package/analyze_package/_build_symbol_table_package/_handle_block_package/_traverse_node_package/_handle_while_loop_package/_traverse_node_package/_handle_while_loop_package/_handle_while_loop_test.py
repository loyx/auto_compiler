import unittest
from unittest.mock import patch, call
from typing import Dict, Any

# Import the function under test using relative import
from ._handle_while_loop_src import _handle_while_loop


class TestHandleWhileLoop(unittest.TestCase):
    """单元测试：_handle_while_loop 函数"""

    def setUp(self):
        """每个测试前的准备工作"""
        self.mock_symbol_table: Dict[str, Any] = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }

    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._handle_while_loop_package._handle_while_loop_src._traverse_node')
    def test_handle_while_loop_with_condition_and_body(self, mock_traverse_node):
        """测试：while_loop 节点同时包含 condition 和 body"""
        node = {
            "type": "while_loop",
            "condition": {"type": "binary_op", "value": "x < 10"},
            "body": {"type": "block", "children": []}
        }
        
        _handle_while_loop(node, self.mock_symbol_table)
        
        # 验证 _traverse_node 被调用了两次
        self.assertEqual(mock_traverse_node.call_count, 2)
        
        # 验证调用顺序和参数
        expected_calls = [
            call({"type": "binary_op", "value": "x < 10"}, self.mock_symbol_table),
            call({"type": "block", "children": []}, self.mock_symbol_table)
        ]
        mock_traverse_node.assert_has_calls(expected_calls)

    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._handle_while_loop_package._handle_while_loop_src._traverse_node')
    def test_handle_while_loop_with_only_condition(self, mock_traverse_node):
        """测试：while_loop 节点只有 condition，没有 body"""
        node = {
            "type": "while_loop",
            "condition": {"type": "binary_op", "value": "x > 0"},
            "body": None
        }
        
        _handle_while_loop(node, self.mock_symbol_table)
        
        # 验证 _traverse_node 只被调用了一次（仅 condition）
        self.assertEqual(mock_traverse_node.call_count, 1)
        mock_traverse_node.assert_called_once_with(
            {"type": "binary_op", "value": "x > 0"},
            self.mock_symbol_table
        )

    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._handle_while_loop_package._handle_while_loop_src._traverse_node')
    def test_handle_while_loop_with_only_body(self, mock_traverse_node):
        """测试：while_loop 节点只有 body，没有 condition"""
        node = {
            "type": "while_loop",
            "condition": None,
            "body": {"type": "block", "children": []}
        }
        
        _handle_while_loop(node, self.mock_symbol_table)
        
        # 验证 _traverse_node 只被调用了一次（仅 body）
        self.assertEqual(mock_traverse_node.call_count, 1)
        mock_traverse_node.assert_called_once_with(
            {"type": "block", "children": []},
            self.mock_symbol_table
        )

    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._handle_while_loop_package._handle_while_loop_src._traverse_node')
    def test_handle_while_loop_with_neither_condition_nor_body(self, mock_traverse_node):
        """测试：while_loop 节点既没有 condition 也没有 body"""
        node = {
            "type": "while_loop",
            "condition": None,
            "body": None
        }
        
        _handle_while_loop(node, self.mock_symbol_table)
        
        # 验证 _traverse_node 没有被调用
        self.assertEqual(mock_traverse_node.call_count, 0)

    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._handle_while_loop_package._handle_while_loop_src._traverse_node')
    def test_handle_while_loop_with_missing_fields(self, mock_traverse_node):
        """测试：while_loop 节点缺少 condition 和 body 字段（使用 get 默认 None）"""
        node = {
            "type": "while_loop"
        }
        
        _handle_while_loop(node, self.mock_symbol_table)
        
        # 验证 _traverse_node 没有被调用
        self.assertEqual(mock_traverse_node.call_count, 0)

    @patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._handle_while_loop_package._handle_while_loop_src._traverse_node')
    def test_handle_while_loop_with_complex_nested_structure(self, mock_traverse_node):
        """测试：while_loop 节点包含复杂的嵌套结构"""
        node = {
            "type": "while_loop",
            "condition": {
                "type": "binary_op",
                "left": {"type": "identifier", "value": "x"},
                "right": {"type": "literal", "value": 10},
                "operator": "<"
            },
            "body": {
                "type": "block",
                "children": [
                    {"type": "assignment", "target": "x", "value": {"type": "literal", "value": 1}},
                    {"type": "print", "argument": {"type": "identifier", "value": "x"}}
                ]
            }
        }
        
        _handle_while_loop(node, self.mock_symbol_table)
        
        # 验证 _traverse_node 被调用了两次
        self.assertEqual(mock_traverse_node.call_count, 2)
        
        # 验证传递的是完整的嵌套结构
        calls = mock_traverse_node.call_args_list
        self.assertEqual(len(calls), 2)
        
        # 第一个调用是 condition
        self.assertEqual(calls[0][0][0]["type"], "binary_op")
        self.assertEqual(calls[0][0][0]["left"]["type"], "identifier")
        
        # 第二个调用是 body
        self.assertEqual(calls[1][0][0]["type"], "block")
        self.assertEqual(len(calls[1][0][0]["children"]), 2)

    @patch('._handle_while_loop_src._traverse_node')
    def test_handle_while_loop_symbol_table_unchanged_structure(self, mock_traverse_node):
        """测试：symbol_table 的结构在调用前后保持一致"""
        original_symbol_table = {
            "variables": {"x": {"data_type": "int", "is_declared": True}},
            "functions": {},
            "current_scope": 1,
            "scope_stack": [0, 1]
        }
        node = {
            "type": "while_loop",
            "condition": {"type": "binary_op"},
            "body": {"type": "block"}
        }
        
        _handle_while_loop(node, original_symbol_table)
        
        # 验证 symbol_table 的顶层键保持不变
        self.assertIn("variables", original_symbol_table)
        self.assertIn("functions", original_symbol_table)
        self.assertIn("current_scope", original_symbol_table)
        self.assertIn("scope_stack", original_symbol_table)

    @patch('._handle_while_loop_src._traverse_node')
    def test_handle_while_loop_empty_dict_node(self, mock_traverse_node):
        """测试：空字典作为 node 输入"""
        node = {}
        
        _handle_while_loop(node, self.mock_symbol_table)
        
        # 验证 _traverse_node 没有被调用（get 返回 None）
        self.assertEqual(mock_traverse_node.call_count, 0)


if __name__ == "__main__":
    unittest.main()

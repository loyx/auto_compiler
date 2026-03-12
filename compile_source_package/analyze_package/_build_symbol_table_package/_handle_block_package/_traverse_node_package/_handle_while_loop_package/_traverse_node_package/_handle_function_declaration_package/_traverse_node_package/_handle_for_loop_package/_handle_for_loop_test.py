import unittest
from unittest.mock import patch, call
from typing import Dict, Any

# 相对导入被测模块
from ._handle_for_loop_src import _handle_for_loop

AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleForLoop(unittest.TestCase):
    """测试 _handle_for_loop 函数"""
    
    def setUp(self):
        """设置测试夹具"""
        self.symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }
    
    @patch('_handle_for_loop_package._handle_for_loop_src._traverse_node')
    def test_handle_for_loop_normal(self, mock_traverse):
        """测试正常 for 循环节点处理"""
        node = {
            "type": "for_loop",
            "iterator": "i",
            "iterable": {"type": "list", "value": [1, 2, 3]},
            "body": {"type": "block", "statements": []}
        }
        
        _handle_for_loop(node, self.symbol_table)
        
        # 验证 _traverse_node 被调用两次：一次处理 iterable，一次处理 body
        self.assertEqual(mock_traverse.call_count, 2)
        mock_traverse.assert_has_calls([
            call({"type": "list", "value": [1, 2, 3]}, self.symbol_table),
            call({"type": "block", "statements": []}, self.symbol_table)
        ])
    
    @patch('_handle_for_loop_package._handle_for_loop_src._traverse_node')
    def test_handle_for_loop_no_iterable(self, mock_traverse):
        """测试 iterable 为 None 的情况"""
        node = {
            "type": "for_loop",
            "iterator": "i",
            "iterable": None,
            "body": {"type": "block", "statements": []}
        }
        
        _handle_for_loop(node, self.symbol_table)
        
        # 只调用一次，处理 body
        self.assertEqual(mock_traverse.call_count, 1)
        mock_traverse.assert_called_with({"type": "block", "statements": []}, self.symbol_table)
    
    @patch('_handle_for_loop_package._handle_for_loop_src._traverse_node')
    def test_handle_for_loop_no_body(self, mock_traverse):
        """测试 body 为 None 的情况"""
        node = {
            "type": "for_loop",
            "iterator": "i",
            "iterable": {"type": "list", "value": [1, 2, 3]},
            "body": None
        }
        
        _handle_for_loop(node, self.symbol_table)
        
        # 只调用一次，处理 iterable
        self.assertEqual(mock_traverse.call_count, 1)
        mock_traverse.assert_called_with({"type": "list", "value": [1, 2, 3]}, self.symbol_table)
    
    @patch('_handle_for_loop_package._handle_for_loop_src._traverse_node')
    def test_handle_for_loop_empty_node(self, mock_traverse):
        """测试空节点（缺少所有字段）"""
        node = {
            "type": "for_loop"
        }
        
        _handle_for_loop(node, self.symbol_table)
        
        # 不应该调用 _traverse_node
        self.assertEqual(mock_traverse.call_count, 0)
    
    @patch('_handle_for_loop_package._handle_for_loop_src._traverse_node')
    def test_handle_for_loop_iterable_not_dict(self, mock_traverse):
        """测试 iterable 不是 dict 的情况"""
        node = {
            "type": "for_loop",
            "iterator": "i",
            "iterable": [1, 2, 3],  # list 而不是 dict
            "body": {"type": "block", "statements": []}
        }
        
        _handle_for_loop(node, self.symbol_table)
        
        # 只调用一次，处理 body
        self.assertEqual(mock_traverse.call_count, 1)
        mock_traverse.assert_called_with({"type": "block", "statements": []}, self.symbol_table)
    
    @patch('_handle_for_loop_package._handle_for_loop_src._traverse_node')
    def test_handle_for_loop_body_not_dict(self, mock_traverse):
        """测试 body 不是 dict 的情况"""
        node = {
            "type": "for_loop",
            "iterator": "i",
            "iterable": {"type": "list", "value": [1, 2, 3]},
            "body": "some_string"  # string 而不是 dict
        }
        
        _handle_for_loop(node, self.symbol_table)
        
        # 只调用一次，处理 iterable
        self.assertEqual(mock_traverse.call_count, 1)
        mock_traverse.assert_called_with({"type": "list", "value": [1, 2, 3]}, self.symbol_table)
    
    @patch('_handle_for_loop_package._handle_for_loop_src._traverse_node')
    def test_handle_for_loop_traverse_raises_exception(self, mock_traverse):
        """测试 _traverse_node 抛出异常时的行为"""
        node = {
            "type": "for_loop",
            "iterator": "i",
            "iterable": {"type": "list", "value": [1, 2, 3]},
            "body": {"type": "block", "statements": []}
        }
        
        mock_traverse.side_effect = ValueError("Traversal error")
        
        with self.assertRaises(ValueError):
            _handle_for_loop(node, self.symbol_table)
        
        # 验证异常在第一次调用时抛出
        mock_traverse.assert_called_once_with({"type": "list", "value": [1, 2, 3]}, self.symbol_table)
    
    @patch('_handle_for_loop_package._handle_for_loop_src._traverse_node')
    def test_handle_for_loop_symbol_table_modified(self, mock_traverse):
        """测试 symbol_table 被传递给 _traverse_node"""
        node = {
            "type": "for_loop",
            "iterator": "i",
            "iterable": {"type": "list", "value": [1, 2, 3]},
            "body": {"type": "block", "statements": []}
        }
        
        _handle_for_loop(node, self.symbol_table)
        
        # 验证 symbol_table 被正确传递
        for call_args in mock_traverse.call_args_list:
            self.assertEqual(call_args[0][1], self.symbol_table)
    
    @patch('_handle_for_loop_package._handle_for_loop_src._traverse_node')
    def test_handle_for_loop_nested_structure(self, mock_traverse):
        """测试嵌套 for 循环结构"""
        nested_for = {
            "type": "for_loop",
            "iterator": "j",
            "iterable": {"type": "list", "value": [4, 5, 6]},
            "body": {"type": "block", "statements": []}
        }
        
        node = {
            "type": "for_loop",
            "iterator": "i",
            "iterable": {"type": "list", "value": [1, 2, 3]},
            "body": nested_for
        }
        
        _handle_for_loop(node, self.symbol_table)
        
        # 验证 _traverse_node 被调用两次
        self.assertEqual(mock_traverse.call_count, 2)
    
    def test_handle_for_loop_returns_none(self):
        """测试函数返回 None"""
        node = {
            "type": "for_loop",
            "iterator": "i",
            "iterable": {"type": "list", "value": [1, 2, 3]},
            "body": {"type": "block", "statements": []}
        }
        
        result = _handle_for_loop(node, self.symbol_table)
        
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()

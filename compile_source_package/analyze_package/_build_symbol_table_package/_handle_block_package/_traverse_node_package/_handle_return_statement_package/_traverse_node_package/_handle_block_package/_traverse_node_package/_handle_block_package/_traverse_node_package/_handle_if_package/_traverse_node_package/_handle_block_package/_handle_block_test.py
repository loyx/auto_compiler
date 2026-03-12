import unittest
from unittest.mock import patch, call

from ._handle_block_src import _handle_block


class TestHandleBlock(unittest.TestCase):
    """Test cases for _handle_block function."""
    
    def test_handle_block_with_valid_children(self):
        """测试 block 节点包含有效的 children 列表"""
        node = {
            "type": "block",
            "children": [
                {"type": "statement1"},
                {"type": "statement2"},
                {"type": "statement3"}
            ],
            "line": 10,
            "column": 5
        }
        symbol_table = {}
        
        with patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_if_package._traverse_node_package._handle_block_package._traverse_node") as mock_traverse:
            _handle_block(node, symbol_table)
            
            self.assertEqual(mock_traverse.call_count, 3)
            mock_traverse.assert_has_calls([
                call({"type": "statement1"}, symbol_table),
                call({"type": "statement2"}, symbol_table),
                call({"type": "statement3"}, symbol_table)
            ])
            self.assertNotIn("errors", symbol_table)
    
    def test_handle_block_with_empty_children(self):
        """测试 block 节点包含空的 children 列表"""
        node = {
            "type": "block",
            "children": [],
            "line": 10,
            "column": 5
        }
        symbol_table = {}
        
        with patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_if_package._traverse_node_package._handle_block_package._traverse_node") as mock_traverse:
            _handle_block(node, symbol_table)
            
            mock_traverse.assert_not_called()
            self.assertNotIn("errors", symbol_table)
    
    def test_handle_block_with_non_list_children(self):
        """测试 block 节点 children 不是 list 类型时记录警告"""
        node = {
            "type": "block",
            "children": "not_a_list",
            "line": 10,
            "column": 5
        }
        symbol_table = {}
        
        with patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_if_package._traverse_node_package._handle_block_package._traverse_node") as mock_traverse:
            _handle_block(node, symbol_table)
            
            mock_traverse.assert_not_called()
            self.assertIn("errors", symbol_table)
            self.assertEqual(len(symbol_table["errors"]), 1)
            error = symbol_table["errors"][0]
            self.assertEqual(error["type"], "warning")
            self.assertIn("invalid children type", error["message"])
            self.assertEqual(error["line"], 10)
            self.assertEqual(error["column"], 5)
    
    def test_handle_block_with_missing_children_key(self):
        """测试 block 节点缺少 children 键时使用默认空列表"""
        node = {
            "type": "block",
            "line": 10,
            "column": 5
        }
        symbol_table = {}
        
        with patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_if_package._traverse_node_package._handle_block_package._traverse_node") as mock_traverse:
            _handle_block(node, symbol_table)
            
            mock_traverse.assert_not_called()
            self.assertNotIn("errors", symbol_table)
    
    def test_handle_block_preserves_existing_errors(self):
        """测试 block 处理时保留 symbol_table 中已有的 errors"""
        node = {
            "type": "block",
            "children": [{"type": "stmt"}],
            "line": 10,
            "column": 5
        }
        symbol_table = {
            "errors": [{"type": "error", "message": "pre-existing error"}]
        }
        
        with patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_if_package._traverse_node_package._handle_block_package._traverse_node") as mock_traverse:
            _handle_block(node, symbol_table)
            
            self.assertEqual(len(symbol_table["errors"]), 1)
            self.assertEqual(symbol_table["errors"][0]["message"], "pre-existing error")
    
    def test_handle_block_non_list_children_preserves_existing_errors(self):
        """测试 block 节点 children 类型错误时，追加警告到已有 errors"""
        node = {
            "type": "block",
            "children": {"not": "list"},
            "line": 10,
            "column": 5
        }
        symbol_table = {
            "errors": [{"type": "error", "message": "pre-existing error"}]
        }
        
        with patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_if_package._traverse_node_package._handle_block_package._traverse_node") as mock_traverse:
            _handle_block(node, symbol_table)
            
            self.assertEqual(len(symbol_table["errors"]), 2)
            self.assertEqual(symbol_table["errors"][0]["message"], "pre-existing error")
            self.assertEqual(symbol_table["errors"][1]["type"], "warning")
    
    def test_handle_block_with_various_child_types(self):
        """测试 block 节点包含不同类型的子节点"""
        node = {
            "type": "block",
            "children": [
                {"type": "if", "condition": "x > 0"},
                {"type": "while", "condition": "True"},
                {"type": "return", "value": "42"},
                {"type": "assignment", "target": "x", "value": "10"}
            ],
            "line": 1,
            "column": 1
        }
        symbol_table = {"variables": {}, "current_scope": 1}
        
        with patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_if_package._traverse_node_package._handle_block_package._traverse_node") as mock_traverse:
            _handle_block(node, symbol_table)
            
            self.assertEqual(mock_traverse.call_count, 4)
            self.assertEqual(symbol_table["variables"], {})
            self.assertEqual(symbol_table["current_scope"], 1)
    
    def test_handle_block_without_line_column_info(self):
        """测试 block 节点缺少 line/column 信息时的处理"""
        node = {
            "type": "block",
            "children": "invalid"
        }
        symbol_table = {}
        
        with patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_if_package._traverse_node_package._handle_block_package._traverse_node") as mock_traverse:
            _handle_block(node, symbol_table)
            
            self.assertIn("errors", symbol_table)
            error = symbol_table["errors"][0]
            self.assertEqual(error["line"], "?")
            self.assertEqual(error["column"], "?")
    
    def test_handle_block_with_none_children(self):
        """测试 block 节点 children 为 None 时的处理"""
        node = {
            "type": "block",
            "children": None,
            "line": 5,
            "column": 10
        }
        symbol_table = {}
        
        with patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_if_package._traverse_node_package._handle_block_package._traverse_node") as mock_traverse:
            _handle_block(node, symbol_table)
            
            mock_traverse.assert_not_called()
            self.assertIn("errors", symbol_table)
            self.assertEqual(len(symbol_table["errors"]), 1)
            self.assertIn("NoneType", symbol_table["errors"][0]["message"])
    
    def test_handle_block_does_not_create_scope(self):
        """验证 block 处理不创建新作用域"""
        node = {
            "type": "block",
            "children": [{"type": "stmt"}],
            "line": 1,
            "column": 1
        }
        symbol_table = {
            "current_scope": 1,
            "scope_stack": [0, 1],
            "variables": {"x": {"scope": 1}}
        }
        
        with patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_if_package._traverse_node_package._handle_block_package._traverse_node") as mock_traverse:
            _handle_block(node, symbol_table)
            
            self.assertEqual(symbol_table["current_scope"], 1)
            self.assertEqual(symbol_table["scope_stack"], [0, 1])
            self.assertEqual(symbol_table["variables"], {"x": {"scope": 1}})


if __name__ == "__main__":
    unittest.main()

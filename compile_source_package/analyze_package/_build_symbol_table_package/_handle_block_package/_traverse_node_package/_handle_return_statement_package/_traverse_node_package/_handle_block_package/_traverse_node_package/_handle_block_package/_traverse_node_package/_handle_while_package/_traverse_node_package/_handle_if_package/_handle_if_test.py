"""单元测试文件：测试 _handle_if 函数"""
import unittest
from unittest.mock import patch

from ._handle_if_src import _handle_if, _record_error


class TestHandleIf(unittest.TestCase):
    """测试 _handle_if 函数的各种场景"""

    @patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_while_package._traverse_node_package._handle_if_package._handle_if_src._traverse_node")
    def test_handle_if_with_two_children(self, mock_traverse_node):
        """测试有效的 if 节点（只有 condition 和 then_branch）"""
        node = {
            "type": "if",
            "children": [
                {"type": "condition", "value": "x > 0", "line": 1, "column": 5},
                {"type": "block", "children": [], "line": 1, "column": 15}
            ],
            "line": 1,
            "column": 5
        }
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
            "errors": []
        }
        
        _handle_if(node, symbol_table)
        
        # 验证 _traverse_node 被调用了 2 次（condition 和 then_branch）
        self.assertEqual(mock_traverse_node.call_count, 2)
        # 验证调用参数
        mock_traverse_node.assert_any_call(node["children"][0], symbol_table)
        mock_traverse_node.assert_any_call(node["children"][1], symbol_table)
        # 验证没有记录错误
        self.assertEqual(len(symbol_table["errors"]), 0)

    @patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_while_package._traverse_node_package._handle_if_package._handle_if_src._traverse_node")
    def test_handle_if_with_three_children(self, mock_traverse_node):
        """测试有效的 if 节点（包含 condition、then_branch 和 else_branch）"""
        node = {
            "type": "if",
            "children": [
                {"type": "condition", "value": "x > 0", "line": 1, "column": 5},
                {"type": "block", "children": [], "line": 1, "column": 15},
                {"type": "block", "children": [], "line": 2, "column": 5}
            ],
            "line": 1,
            "column": 5
        }
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
            "errors": []
        }
        
        _handle_if(node, symbol_table)
        
        # 验证 _traverse_node 被调用了 3 次
        self.assertEqual(mock_traverse_node.call_count, 3)
        # 验证所有分支都被处理
        mock_traverse_node.assert_any_call(node["children"][0], symbol_table)
        mock_traverse_node.assert_any_call(node["children"][1], symbol_table)
        mock_traverse_node.assert_any_call(node["children"][2], symbol_table)
        # 验证没有记录错误
        self.assertEqual(len(symbol_table["errors"]), 0)

    @patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_while_package._traverse_node_package._handle_if_package._handle_if_src._traverse_node")
    def test_handle_if_with_no_children(self, mock_traverse_node):
        """测试无效的 if 节点（没有 children）"""
        node = {
            "type": "if",
            "children": [],
            "line": 1,
            "column": 5
        }
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
            "errors": []
        }
        
        _handle_if(node, symbol_table)
        
        # 验证 _traverse_node 没有被调用
        mock_traverse_node.assert_not_called()
        # 验证记录了错误
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertEqual(symbol_table["errors"][0]["type"], "invalid_syntax")
        self.assertEqual(symbol_table["errors"][0]["line"], 1)
        self.assertEqual(symbol_table["errors"][0]["column"], 5)

    @patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_while_package._traverse_node_package._handle_if_package._handle_if_src._traverse_node")
    def test_handle_if_with_one_child(self, mock_traverse_node):
        """测试无效的 if 节点（只有一个 child）"""
        node = {
            "type": "if",
            "children": [
                {"type": "condition", "value": "x > 0", "line": 1, "column": 5}
            ],
            "line": 2,
            "column": 10
        }
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
            "errors": []
        }
        
        _handle_if(node, symbol_table)
        
        # 验证 _traverse_node 没有被调用
        mock_traverse_node.assert_not_called()
        # 验证记录了错误
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertEqual(symbol_table["errors"][0]["type"], "invalid_syntax")
        self.assertEqual(symbol_table["errors"][0]["message"], "if node must have at least condition and then_branch")
        self.assertEqual(symbol_table["errors"][0]["line"], 2)
        self.assertEqual(symbol_table["errors"][0]["column"], 10)

    def test_handle_if_without_errors_list(self):
        """测试 symbol_table 没有 errors 列表时的处理"""
        node = {
            "type": "if",
            "children": [],
            "line": 1,
            "column": 5
        }
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }
        
        _handle_if(node, symbol_table)
        
        # 验证 errors 列表被创建并记录了错误
        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)

    @patch("main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_while_package._traverse_node_package._handle_if_package._handle_if_src._traverse_node")
    def test_handle_if_missing_line_column(self, mock_traverse_node):
        """测试 if 节点缺少 line/column 信息时的错误处理"""
        node = {
            "type": "if",
            "children": []
        }
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
            "errors": []
        }
        
        _handle_if(node, symbol_table)
        
        # 验证 _traverse_node 没有被调用
        mock_traverse_node.assert_not_called()
        # 验证记录了错误，使用默认值 0
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertEqual(symbol_table["errors"][0]["line"], 0)
        self.assertEqual(symbol_table["errors"][0]["column"], 0)


class TestRecordError(unittest.TestCase):
    """测试 _record_error 辅助函数"""

    def test_record_error_creates_errors_list(self):
        """测试 _record_error 在 symbol_table 没有 errors 时创建列表"""
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0
        }
        
        _record_error(symbol_table, "test_error", "test message", 10, 20)
        
        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertEqual(symbol_table["errors"][0]["type"], "test_error")
        self.assertEqual(symbol_table["errors"][0]["message"], "test message")
        self.assertEqual(symbol_table["errors"][0]["line"], 10)
        self.assertEqual(symbol_table["errors"][0]["column"], 20)

    def test_record_error_appends_to_existing_list(self):
        """测试 _record_error 追加到已有的 errors 列表"""
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "errors": [{"type": "existing", "message": "existing error", "line": 1, "column": 1}]
        }
        
        _record_error(symbol_table, "new_error", "new message", 5, 6)
        
        self.assertEqual(len(symbol_table["errors"]), 2)
        self.assertEqual(symbol_table["errors"][1]["type"], "new_error")
        self.assertEqual(symbol_table["errors"][1]["message"], "new message")
        self.assertEqual(symbol_table["errors"][1]["line"], 5)
        self.assertEqual(symbol_table["errors"][1]["column"], 6)


if __name__ == "__main__":
    unittest.main()

# === std / third-party imports ===
import unittest
from unittest.mock import patch

# === sub function imports ===
from ._handle_return_statement_src import _handle_return_statement


class TestHandleReturnStatement(unittest.TestCase):
    """测试 _handle_return_statement 函数"""

    def setUp(self):
        """测试前准备"""
        self.symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }

    @patch("projects.cc.files.main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._traverse_node_src._traverse_node")
    def test_return_with_value(self, mock_traverse_node):
        """测试 return 语句包含返回值的情况"""
        node = {
            "type": "return_statement",
            "value": {
                "type": "binary_expression",
                "left": {"type": "identifier", "name": "x"},
                "operator": "+",
                "right": {"type": "literal", "value": 1}
            }
        }
        
        _handle_return_statement(node, self.symbol_table)
        
        mock_traverse_node.assert_called_once_with(node["value"], self.symbol_table)

    @patch("projects.cc.files.main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._traverse_node_src._traverse_node")
    def test_return_without_value(self, mock_traverse_node):
        """测试 return 语句不包含返回值的情况（value 为 None）"""
        node = {
            "type": "return_statement",
            "value": None
        }
        
        _handle_return_statement(node, self.symbol_table)
        
        mock_traverse_node.assert_not_called()

    @patch("projects.cc.files.main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._traverse_node_src._traverse_node")
    def test_return_missing_value_key(self, mock_traverse_node):
        """测试 return 语句缺少 value 字段的情况"""
        node = {
            "type": "return_statement"
        }
        
        _handle_return_statement(node, self.symbol_table)
        
        mock_traverse_node.assert_not_called()

    @patch("projects.cc.files.main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._traverse_node_src._traverse_node")
    def test_return_with_complex_expression(self, mock_traverse_node):
        """测试 return 语句包含复杂表达式的情况"""
        node = {
            "type": "return_statement",
            "value": {
                "type": "function_call",
                "function": {"type": "identifier", "name": "compute"},
                "arguments": [
                    {"type": "literal", "value": 10},
                    {"type": "identifier", "name": "y"}
                ]
            }
        }
        
        _handle_return_statement(node, self.symbol_table)
        
        mock_traverse_node.assert_called_once_with(node["value"], self.symbol_table)

    @patch("projects.cc.files.main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._traverse_node_src._traverse_node")
    def test_return_with_literal_value(self, mock_traverse_node):
        """测试 return 语句包含字面量值的情况"""
        node = {
            "type": "return_statement",
            "value": {
                "type": "literal",
                "value": 42
            }
        }
        
        _handle_return_statement(node, self.symbol_table)
        
        mock_traverse_node.assert_called_once_with(node["value"], self.symbol_table)

    @patch("projects.cc.files.main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._traverse_node_src._traverse_node")
    def test_symbol_table_unchanged_when_no_value(self, mock_traverse_node):
        """测试当没有 value 时 symbol_table 不被修改"""
        node = {
            "type": "return_statement",
            "value": None
        }
        
        original_symbol_table = {
            "variables": {"x": {"type": "int"}},
            "functions": {},
            "current_scope": 1,
            "scope_stack": [0, 1]
        }
        
        _handle_return_statement(node, original_symbol_table)
        
        mock_traverse_node.assert_not_called()
        # 验证 symbol_table 未被修改
        self.assertEqual(original_symbol_table["variables"], {"x": {"type": "int"}})
        self.assertEqual(original_symbol_table["current_scope"], 1)


if __name__ == "__main__":
    unittest.main()

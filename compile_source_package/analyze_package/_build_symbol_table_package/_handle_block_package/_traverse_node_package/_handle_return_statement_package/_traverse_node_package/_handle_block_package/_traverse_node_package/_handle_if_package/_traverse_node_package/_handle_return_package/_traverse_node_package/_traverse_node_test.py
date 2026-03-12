"""单元测试文件：_traverse_node 函数的测试用例。"""
import unittest
from unittest.mock import patch

from ._traverse_node_src import _traverse_node


class TestTraverseNode(unittest.TestCase):
    """_traverse_node 函数的测试用例类。"""

    def setUp(self):
        """每个测试前的准备工作。"""
        self.symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
            "errors": []
        }

    def test_handle_literal_int(self):
        """测试处理 int 字面量节点。"""
        node = {
            "type": "literal_int",
            "value": 42,
            "line": 1,
            "column": 5
        }
        
        with patch("._handle_literal_package._handle_literal_src._handle_literal") as mock_handle:
            mock_handle.return_value = "int"
            result = _traverse_node(node, self.symbol_table)
            
            mock_handle.assert_called_once_with(node, self.symbol_table)
            self.assertEqual(result, "int")

    def test_handle_literal_int_alt_type(self):
        """测试处理 int_literal 类型字面量节点。"""
        node = {
            "type": "int_literal",
            "value": 100,
            "line": 2,
            "column": 3
        }
        
        with patch("._handle_literal_package._handle_literal_src._handle_literal") as mock_handle:
            mock_handle.return_value = "int"
            result = _traverse_node(node, self.symbol_table)
            
            mock_handle.assert_called_once_with(node, self.symbol_table)
            self.assertEqual(result, "int")

    def test_handle_literal_char(self):
        """测试处理 char 字面量节点。"""
        node = {
            "type": "literal_char",
            "value": "a",
            "line": 3,
            "column": 7
        }
        
        with patch("._handle_literal_package._handle_literal_src._handle_literal") as mock_handle:
            mock_handle.return_value = "char"
            result = _traverse_node(node, self.symbol_table)
            
            mock_handle.assert_called_once_with(node, self.symbol_table)
            self.assertEqual(result, "char")

    def test_handle_literal_char_alt_type(self):
        """测试处理 char_literal 类型字面量节点。"""
        node = {
            "type": "char_literal",
            "value": "x",
            "line": 4,
            "column": 2
        }
        
        with patch("._handle_literal_package._handle_literal_src._handle_literal") as mock_handle:
            mock_handle.return_value = "char"
            result = _traverse_node(node, self.symbol_table)
            
            mock_handle.assert_called_once_with(node, self.symbol_table)
            self.assertEqual(result, "char")

    def test_handle_identifier(self):
        """测试处理标识符节点。"""
        node = {
            "type": "identifier",
            "value": "x",
            "line": 5,
            "column": 1
        }
        
        with patch("._handle_identifier_package._handle_identifier_src._handle_identifier") as mock_handle:
            mock_handle.return_value = "int"
            result = _traverse_node(node, self.symbol_table)
            
            mock_handle.assert_called_once_with(node, self.symbol_table)
            self.assertEqual(result, "int")

    def test_handle_identifier_alt_type(self):
        """测试处理 variable 类型标识符节点。"""
        node = {
            "type": "variable",
            "value": "y",
            "line": 6,
            "column": 4
        }
        
        with patch("._handle_identifier_package._handle_identifier_src._handle_identifier") as mock_handle:
            mock_handle.return_value = "char"
            result = _traverse_node(node, self.symbol_table)
            
            mock_handle.assert_called_once_with(node, self.symbol_table)
            self.assertEqual(result, "char")

    def test_handle_binary_op(self):
        """测试处理二元运算符节点。"""
        node = {
            "type": "binary_op",
            "left": {"type": "identifier", "value": "a"},
            "right": {"type": "literal_int", "value": 5},
            "operator": "+",
            "line": 7,
            "column": 10
        }
        
        with patch("._handle_binary_op_package._handle_binary_op_src._handle_binary_op") as mock_handle:
            mock_handle.return_value = "int"
            result = _traverse_node(node, self.symbol_table)
            
            mock_handle.assert_called_once_with(node, self.symbol_table)
            self.assertEqual(result, "int")

    def test_handle_binary_op_alt_type(self):
        """测试处理 operation 类型二元运算符节点。"""
        node = {
            "type": "operation",
            "left": {"type": "identifier", "value": "b"},
            "right": {"type": "identifier", "value": "c"},
            "operator": "-",
            "line": 8,
            "column": 5
        }
        
        with patch("._handle_binary_op_package._handle_binary_op_src._handle_binary_op") as mock_handle:
            mock_handle.return_value = "int"
            result = _traverse_node(node, self.symbol_table)
            
            mock_handle.assert_called_once_with(node, self.symbol_table)
            self.assertEqual(result, "int")

    def test_handle_function_call(self):
        """测试处理函数调用节点。"""
        node = {
            "type": "function_call",
            "function_name": "foo",
            "arguments": [],
            "line": 9,
            "column": 1
        }
        
        with patch("._handle_function_call_package._handle_function_call_src._handle_function_call") as mock_handle:
            mock_handle.return_value = "int"
            result = _traverse_node(node, self.symbol_table)
            
            mock_handle.assert_called_once_with(node, self.symbol_table)
            self.assertEqual(result, "int")

    def test_handle_assignment(self):
        """测试处理赋值节点。"""
        node = {
            "type": "assignment",
            "target": {"type": "identifier", "value": "x"},
            "value": {"type": "literal_int", "value": 10},
            "line": 10,
            "column": 3
        }
        
        with patch("._handle_assignment_package._handle_assignment_src._handle_assignment") as mock_handle:
            mock_handle.return_value = "int"
            result = _traverse_node(node, self.symbol_table)
            
            mock_handle.assert_called_once_with(node, self.symbol_table)
            self.assertEqual(result, "int")

    def test_handle_block(self):
        """测试处理代码块节点。"""
        node = {
            "type": "block",
            "children": [
                {"type": "var_decl", "data_type": "int"},
                {"type": "assignment", "target": {"type": "identifier", "value": "x"}, "value": {"type": "literal_int", "value": 5}}
            ],
            "line": 11,
            "column": 1
        }
        
        with patch("._handle_block_package._handle_block_src._handle_block") as mock_handle:
            mock_handle.return_value = "int"
            result = _traverse_node(node, self.symbol_table)
            
            mock_handle.assert_called_once_with(node, self.symbol_table)
            self.assertEqual(result, "int")

    def test_handle_var_decl(self):
        """测试处理变量声明节点。"""
        node = {
            "type": "var_decl",
            "data_type": "int",
            "line": 12,
            "column": 1
        }
        
        result = _traverse_node(node, self.symbol_table)
        
        self.assertEqual(result, "int")

    def test_handle_var_decl_char(self):
        """测试处理 char 类型变量声明节点。"""
        node = {
            "type": "var_decl",
            "data_type": "char",
            "line": 13,
            "column": 1
        }
        
        result = _traverse_node(node, self.symbol_table)
        
        self.assertEqual(result, "char")

    def test_handle_var_decl_missing_data_type(self):
        """测试处理缺少 data_type 的变量声明节点。"""
        node = {
            "type": "var_decl",
            "line": 14,
            "column": 1
        }
        
        result = _traverse_node(node, self.symbol_table)
        
        self.assertEqual(result, "void")

    def test_handle_if_statement(self):
        """测试处理 if 条件语句节点。"""
        then_branch = {
            "type": "block",
            "children": [{"type": "literal_int", "value": 1}],
            "line": 15,
            "column": 5
        }
        node = {
            "type": "if",
            "condition": {"type": "binary_op", "operator": ">", "left": {"type": "identifier", "value": "x"}, "right": {"type": "literal_int", "value": 0}},
            "then_branch": then_branch,
            "line": 15,
            "column": 1
        }
        
        with patch("._handle_block_package._handle_block_src._handle_block") as mock_handle:
            mock_handle.return_value = "int"
            result = _traverse_node(node, self.symbol_table)
            
            mock_handle.assert_called_once_with(then_branch, self.symbol_table)
            self.assertEqual(result, "int")

    def test_handle_if_statement_missing_then_branch(self):
        """测试处理缺少 then_branch 的 if 语句节点。"""
        node = {
            "type": "if",
            "condition": {"type": "binary_op", "operator": ">", "left": {"type": "identifier", "value": "x"}, "right": {"type": "literal_int", "value": 0}},
            "line": 16,
            "column": 1
        }
        
        with patch("._handle_block_package._handle_block_src._handle_block") as mock_handle:
            mock_handle.return_value = "void"
            result = _traverse_node(node, self.symbol_table)
            
            mock_handle.assert_called_once_with({}, self.symbol_table)
            self.assertEqual(result, "void")

    def test_handle_while_statement(self):
        """测试处理 while 循环语句节点。"""
        body = {
            "type": "block",
            "children": [{"type": "assignment", "target": {"type": "identifier", "value": "i"}, "value": {"type": "binary_op", "operator": "+", "left": {"type": "identifier", "value": "i"}, "right": {"type": "literal_int", "value": 1}}}],
            "line": 17,
            "column": 5
        }
        node = {
            "type": "while",
            "condition": {"type": "binary_op", "operator": "<", "left": {"type": "identifier", "value": "i"}, "right": {"type": "literal_int", "value": 10}},
            "body": body,
            "line": 17,
            "column": 1
        }
        
        with patch("._handle_block_package._handle_block_src._handle_block") as mock_handle:
            mock_handle.return_value = "int"
            result = _traverse_node(node, self.symbol_table)
            
            mock_handle.assert_called_once_with(body, self.symbol_table)
            self.assertEqual(result, "int")

    def test_handle_while_statement_missing_body(self):
        """测试处理缺少 body 的 while 语句节点。"""
        node = {
            "type": "while",
            "condition": {"type": "binary_op", "operator": "<", "left": {"type": "identifier", "value": "i"}, "right": {"type": "literal_int", "value": 10}},
            "line": 18,
            "column": 1
        }
        
        with patch("._handle_block_package._handle_block_src._handle_block") as mock_handle:
            mock_handle.return_value = "void"
            result = _traverse_node(node, self.symbol_table)
            
            mock_handle.assert_called_once_with({}, self.symbol_table)
            self.assertEqual(result, "void")

    def test_handle_return_statement(self):
        """测试处理 return 返回语句节点。"""
        node = {
            "type": "return",
            "value": {"type": "literal_int", "value": 42},
            "line": 19,
            "column": 5
        }
        
        result = _traverse_node(node, self.symbol_table)
        
        self.assertEqual(result, "void")

    def test_handle_return_statement_no_value(self):
        """测试处理没有返回值的 return 语句节点。"""
        node = {
            "type": "return",
            "line": 20,
            "column": 5
        }
        
        result = _traverse_node(node, self.symbol_table)
        
        self.assertEqual(result, "void")

    def test_handle_unknown_node_type(self):
        """测试处理未知节点类型。"""
        node = {
            "type": "unknown_type",
            "line": 21,
            "column": 1
        }
        
        result = _traverse_node(node, self.symbol_table)
        
        self.assertEqual(result, "void")
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        self.assertIn("unknown node type 'unknown_type' at line 21", self.symbol_table["errors"])

    def test_handle_unknown_node_type_missing_line(self):
        """测试处理未知节点类型且缺少行号。"""
        node = {
            "type": "another_unknown",
            "column": 5
        }
        
        result = _traverse_node(node, self.symbol_table)
        
        self.assertEqual(result, "void")
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        self.assertIn("unknown node type 'another_unknown' at line 0", self.symbol_table["errors"])

    def test_handle_unknown_node_type_errors_not_initialized(self):
        """测试处理未知节点类型时 symbol_table 没有 errors 字段。"""
        symbol_table_no_errors = {
            "variables": {},
            "functions": {},
            "current_scope": 0
        }
        node = {
            "type": "mystery_node",
            "line": 22,
            "column": 1
        }
        
        result = _traverse_node(node, symbol_table_no_errors)
        
        self.assertEqual(result, "void")
        self.assertEqual(len(symbol_table_no_errors["errors"]), 1)
        self.assertIn("unknown node type 'mystery_node' at line 22", symbol_table_no_errors["errors"])

    def test_handle_node_missing_type(self):
        """测试处理缺少 type 字段的节点。"""
        node = {
            "line": 23,
            "column": 1
        }
        
        result = _traverse_node(node, self.symbol_table)
        
        self.assertEqual(result, "void")
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        self.assertIn("unknown node type '' at line 23", self.symbol_table["errors"])

    def test_handle_node_empty_dict(self):
        """测试处理空字典节点。"""
        node = {}
        
        result = _traverse_node(node, self.symbol_table)
        
        self.assertEqual(result, "void")
        self.assertEqual(len(self.symbol_table["errors"]), 1)
        self.assertIn("unknown node type '' at line 0", self.symbol_table["errors"])


if __name__ == "__main__":
    unittest.main()

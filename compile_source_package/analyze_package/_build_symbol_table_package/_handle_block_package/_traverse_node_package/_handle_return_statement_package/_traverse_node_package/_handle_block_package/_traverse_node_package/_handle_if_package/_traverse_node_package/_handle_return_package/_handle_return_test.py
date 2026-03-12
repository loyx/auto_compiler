# === std / third-party imports ===
import unittest
from unittest.mock import patch
from typing import Dict, Any

# === sub function imports ===
from ._handle_return_src import _handle_return

# === Type aliases ===
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleReturn(unittest.TestCase):
    """测试 _handle_return 函数的各种场景。"""

    def setUp(self):
        """每个测试前的准备工作。"""
        pass

    def tearDown(self):
        """每个测试后的清理工作。"""
        pass

    def test_return_outside_function(self):
        """测试在函数外部使用 return 语句的情况。"""
        node: AST = {
            "type": "return",
            "children": [],
            "line": 10,
            "column": 5
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 1,
            "errors": []
        }

        _handle_return(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("return statement outside function at line 10", symbol_table["errors"][0])

    def test_return_function_not_found(self):
        """测试函数声明在符号表中不存在的情况。"""
        node: AST = {
            "type": "return",
            "children": [],
            "line": 15,
            "column": 8
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 1,
            "current_function": "nonexistent_func",
            "errors": []
        }

        _handle_return(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("function 'nonexistent_func' not found in symbol table at line 15", symbol_table["errors"][0])

    @patch("._handle_return_src._traverse_node")
    def test_return_with_matching_type(self, mock_traverse_node):
        """测试返回值类型与函数声明匹配的情况。"""
        node: AST = {
            "type": "return",
            "children": [{"type": "literal", "value": 42, "data_type": "int"}],
            "line": 20,
            "column": 10
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {
                "my_func": {
                    "return_type": "int",
                    "params": [],
                    "line": 5,
                    "column": 1
                }
            },
            "current_scope": 1,
            "current_function": "my_func",
            "errors": []
        }

        mock_traverse_node.return_value = "int"

        _handle_return(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 0)
        mock_traverse_node.assert_called_once()

    @patch("._handle_return_src._traverse_node")
    def test_return_with_mismatched_type(self, mock_traverse_node):
        """测试返回值类型与函数声明不匹配的情况。"""
        node: AST = {
            "type": "return",
            "children": [{"type": "literal", "value": 42, "data_type": "int"}],
            "line": 25,
            "column": 12
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {
                "my_func": {
                    "return_type": "char",
                    "params": [],
                    "line": 5,
                    "column": 1
                }
            },
            "current_scope": 1,
            "current_function": "my_func",
            "errors": []
        }

        mock_traverse_node.return_value = "int"

        _handle_return(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("type mismatch in return statement at line 25, column 12", symbol_table["errors"][0])
        self.assertIn("expected 'char', got 'int'", symbol_table["errors"][0])

    def test_return_void_for_void_function(self):
        """测试 void 函数无返回值的情况。"""
        node: AST = {
            "type": "return",
            "children": [],
            "line": 30,
            "column": 15
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {
                "void_func": {
                    "return_type": "void",
                    "params": [],
                    "line": 5,
                    "column": 1
                }
            },
            "current_scope": 1,
            "current_function": "void_func",
            "errors": []
        }

        _handle_return(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_return_void_for_non_void_function(self):
        """测试非 void 函数缺少返回值的情况。"""
        node: AST = {
            "type": "return",
            "children": [],
            "line": 35,
            "column": 18
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {
                "int_func": {
                    "return_type": "int",
                    "params": [],
                    "line": 5,
                    "column": 1
                }
            },
            "current_scope": 1,
            "current_function": "int_func",
            "errors": []
        }

        _handle_return(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("missing return value at line 35, column 18", symbol_table["errors"][0])
        self.assertIn("function 'int_func' expects 'int'", symbol_table["errors"][0])

    @patch("._handle_return_src._traverse_node")
    def test_return_char_type_matching(self, mock_traverse_node):
        """测试 char 类型返回值匹配的情况。"""
        node: AST = {
            "type": "return",
            "children": [{"type": "literal", "value": "a", "data_type": "char"}],
            "line": 40,
            "column": 20
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {
                "char_func": {
                    "return_type": "char",
                    "params": [],
                    "line": 5,
                    "column": 1
                }
            },
            "current_scope": 1,
            "current_function": "char_func",
            "errors": []
        }

        mock_traverse_node.return_value = "char"

        _handle_return(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 0)
        mock_traverse_node.assert_called_once()

    def test_symbol_table_without_errors_list(self):
        """测试符号表初始没有 errors 列表的情况。"""
        node: AST = {
            "type": "return",
            "children": [],
            "line": 45,
            "column": 22
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 1
        }

        _handle_return(node, symbol_table)

        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)

    @patch("._handle_return_src._traverse_node")
    def test_return_with_default_return_type(self, mock_traverse_node):
        """测试函数没有明确指定返回类型（默认 void）的情况。"""
        node: AST = {
            "type": "return",
            "children": [{"type": "literal", "value": 42, "data_type": "int"}],
            "line": 50,
            "column": 25
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {
                "default_func": {
                    "params": [],
                    "line": 5,
                    "column": 1
                }
            },
            "current_scope": 1,
            "current_function": "default_func",
            "errors": []
        }

        mock_traverse_node.return_value = "int"

        _handle_return(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("expected 'void', got 'int'", symbol_table["errors"][0])

    def test_node_without_line_column(self):
        """测试节点没有 line 和 column 信息的情况。"""
        node: AST = {
            "type": "return",
            "children": []
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 1,
            "errors": []
        }

        _handle_return(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("return statement outside function at line 0", symbol_table["errors"][0])


if __name__ == "__main__":
    unittest.main()

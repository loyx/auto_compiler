# -*- coding: utf-8 -*-
"""单元测试文件：_handle_while 函数测试"""
import unittest
from typing import Any, Dict
from unittest.mock import patch

from ._handle_while_src import _handle_while


AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleWhile(unittest.TestCase):
    """_handle_while 函数的单元测试类"""

    def setUp(self) -> None:
        """每个测试前的准备工作"""
        self.mock_traverse_node_patcher = patch(
            "main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_if_package._traverse_node_package._handle_while_package._handle_while_src._traverse_node"
        )
        self.mock_traverse_node = self.mock_traverse_node_patcher.start()

    def tearDown(self) -> None:
        """每个测试后的清理工作"""
        self.mock_traverse_node_patcher.stop()

    def _create_valid_while_node(self, line: int = 10, column: int = 5) -> AST:
        """创建一个有效的 while 节点"""
        return {
            "type": "while",
            "children": [
                {"type": "expression", "value": "condition", "line": line, "column": column},
                {"type": "block", "children": [], "line": line, "column": column}
            ],
            "line": line,
            "column": column
        }

    def _create_symbol_table(self) -> SymbolTable:
        """创建一个初始符号表"""
        return {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [],
            "current_function": None,
            "errors": []
        }

    def test_happy_path_valid_while_node(self) -> None:
        """测试用例：有效的 while 节点，正常作用域管理"""
        node = self._create_valid_while_node()
        symbol_table = self._create_symbol_table()

        _handle_while(node, symbol_table)

        # 验证作用域被正确恢复
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])
        # 验证没有错误
        self.assertEqual(len(symbol_table["errors"]), 0)
        # 验证 _traverse_node 被调用了两次（条件和循环体）
        self.assertEqual(self.mock_traverse_node.call_count, 2)

    def test_scope_management_increment_and_restore(self) -> None:
        """测试用例：作用域递增和恢复逻辑"""
        node = self._create_valid_while_node()
        symbol_table = self._create_symbol_table()
        symbol_table["current_scope"] = 2

        _handle_while(node, symbol_table)

        # 验证作用域最终恢复到原始值
        self.assertEqual(symbol_table["current_scope"], 2)
        self.assertEqual(symbol_table["scope_stack"], [])

    def test_nested_scope_stack(self) -> None:
        """测试用例：嵌套作用域栈操作"""
        node = self._create_valid_while_node()
        symbol_table = self._create_symbol_table()
        symbol_table["current_scope"] = 1
        symbol_table["scope_stack"] = [0]

        _handle_while(node, symbol_table)

        # 验证作用域恢复到栈中的值
        self.assertEqual(symbol_table["current_scope"], 0)
        self.assertEqual(symbol_table["scope_stack"], [])

    def test_error_less_than_two_children(self) -> None:
        """测试用例：children 数量少于 2 个，记录错误"""
        node: AST = {
            "type": "while",
            "children": [{"type": "expression"}],
            "line": 15,
            "column": 8
        }
        symbol_table = self._create_symbol_table()

        _handle_while(node, symbol_table)

        # 验证错误被记录
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["type"], "error")
        self.assertIn("at least 2 children", error["message"])
        self.assertEqual(error["line"], 15)
        self.assertEqual(error["column"], 8)
        # 验证没有调用 _traverse_node
        self.mock_traverse_node.assert_not_called()

    def test_error_empty_children(self) -> None:
        """测试用例：children 为空列表，记录错误"""
        node: AST = {
            "type": "while",
            "children": [],
            "line": 20,
            "column": 3
        }
        symbol_table = self._create_symbol_table()

        _handle_while(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertIn("at least 2 children", error["message"])

    def test_error_none_child_node(self) -> None:
        """测试用例：子节点为 None，记录错误"""
        node: AST = {
            "type": "while",
            "children": [
                {"type": "expression"},
                None
            ],
            "line": 25,
            "column": 10
        }
        symbol_table = self._create_symbol_table()

        _handle_while(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["type"], "error")
        self.assertIn("invalid child node", error["message"])
        self.assertEqual(error["line"], 25)
        self.assertEqual(error["column"], 10)

    def test_error_first_child_none(self) -> None:
        """测试用例：第一个子节点为 None，记录错误"""
        node: AST = {
            "type": "while",
            "children": [
                None,
                {"type": "block"}
            ],
            "line": 30,
            "column": 5
        }
        symbol_table = self._create_symbol_table()

        _handle_while(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertIn("invalid child node", error["message"])

    def test_traverse_node_called_with_correct_args(self) -> None:
        """测试用例：验证 _traverse_node 被正确的参数调用"""
        node = self._create_valid_while_node()
        symbol_table = self._create_symbol_table()

        _handle_while(node, symbol_table)

        # 验证调用次数
        self.assertEqual(self.mock_traverse_node.call_count, 2)
        # 验证第一次调用是条件节点
        first_call_args = self.mock_traverse_node.call_args_list[0]
        self.assertEqual(first_call_args[0][0]["type"], "expression")
        # 验证第二次调用是循环体节点
        second_call_args = self.mock_traverse_node.call_args_list[1]
        self.assertEqual(second_call_args[0][0]["type"], "block")

    def test_missing_line_column_info(self) -> None:
        """测试用例：节点缺少 line/column 信息，错误记录使用默认值"""
        node: AST = {
            "type": "while",
            "children": [{"type": "expression"}]
        }
        symbol_table = self._create_symbol_table()

        _handle_while(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["line"], "?")
        self.assertEqual(error["column"], "?")

    def test_multiple_errors_accumulated(self) -> None:
        """测试用例：多个错误累积到 errors 列表"""
        node: AST = {
            "type": "while",
            "children": [],
            "line": 40,
            "column": 1
        }
        symbol_table = self._create_symbol_table()
        # 预先添加一个错误
        symbol_table["errors"] = [{"type": "error", "message": "pre-existing", "line": 1, "column": 1}]

        _handle_while(node, symbol_table)

        # 验证错误累积
        self.assertEqual(len(symbol_table["errors"]), 2)
        self.assertEqual(symbol_table["errors"][1]["message"], "While loop requires at least 2 children: condition and body")

    def test_scope_stack_not_empty_after_while(self) -> None:
        """测试用例：while 执行后 scope_stack 正确恢复"""
        node = self._create_valid_while_node()
        symbol_table = self._create_symbol_table()
        symbol_table["current_scope"] = 3
        symbol_table["scope_stack"] = [0, 1, 2]

        _handle_while(node, symbol_table)

        # 验证 scope 恢复到栈顶值
        self.assertEqual(symbol_table["current_scope"], 2)
        self.assertEqual(symbol_table["scope_stack"], [0, 1])

    def test_symbol_table_initialization(self) -> None:
        """测试用例：符号表缺少 errors 字段时自动初始化"""
        node = self._create_valid_while_node()
        symbol_table: SymbolTable = {
            "variables": {},
            "current_scope": 0
        }

        _handle_while(node, symbol_table)

        # 验证 errors 被自动创建
        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_more_than_two_children(self) -> None:
        """测试用例：超过 2 个 children，仍然正常处理"""
        node: AST = {
            "type": "while",
            "children": [
                {"type": "expression"},
                {"type": "block"},
                {"type": "extra"}
            ],
            "line": 50,
            "column": 5
        }
        symbol_table = self._create_symbol_table()

        _handle_while(node, symbol_table)

        # 验证没有错误
        self.assertEqual(len(symbol_table["errors"]), 0)
        # 验证只处理前两个子节点
        self.assertEqual(self.mock_traverse_node.call_count, 2)


if __name__ == "__main__":
    unittest.main()

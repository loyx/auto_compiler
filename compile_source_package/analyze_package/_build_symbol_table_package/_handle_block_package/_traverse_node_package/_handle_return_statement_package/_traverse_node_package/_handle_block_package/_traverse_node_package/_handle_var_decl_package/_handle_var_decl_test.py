# -*- coding: utf-8 -*-
"""
单元测试文件：_handle_var_decl 函数测试
测试变量声明节点处理逻辑
"""

import unittest
from typing import Any, Dict

# 相对导入被测函数
from ._handle_var_decl_src import _handle_var_decl


# 类型别名（与被测文件保持一致）
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleVarDecl(unittest.TestCase):
    """_handle_var_decl 函数测试类"""

    def setUp(self) -> None:
        """每个测试前的准备工作"""
        pass

    def tearDown(self) -> None:
        """每个测试后的清理工作"""
        pass

    def _create_symbol_table(self, current_scope: int = 0) -> SymbolTable:
        """辅助方法：创建符号表"""
        return {
            "variables": {},
            "functions": {},
            "current_scope": current_scope,
            "scope_stack": [],
            "errors": []
        }

    def _create_var_decl_node(
        self,
        var_name: str,
        data_type: str,
        line: int,
        column: int
    ) -> AST:
        """辅助方法：创建变量声明节点"""
        return {
            "type": "var_decl",
            "value": var_name,
            "data_type": data_type,
            "line": line,
            "column": column
        }

    # ==================== Happy Path 测试 ====================

    def test_declare_new_variable_int_type(self):
        """测试：声明一个新的 int 类型变量"""
        symbol_table = self._create_symbol_table(current_scope=0)
        node = self._create_var_decl_node("x", "int", 1, 5)

        _handle_var_decl(node, symbol_table)

        # 验证变量已添加到符号表
        self.assertIn("x", symbol_table["variables"])
        self.assertEqual(symbol_table["variables"]["x"]["data_type"], "int")
        self.assertEqual(symbol_table["variables"]["x"]["is_declared"], True)
        self.assertEqual(symbol_table["variables"]["x"]["line"], 1)
        self.assertEqual(symbol_table["variables"]["x"]["column"], 5)
        self.assertEqual(symbol_table["variables"]["x"]["scope_level"], 0)
        # 验证没有错误
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_declare_new_variable_char_type(self):
        """测试：声明一个新的 char 类型变量"""
        symbol_table = self._create_symbol_table(current_scope=0)
        node = self._create_var_decl_node("c", "char", 2, 10)

        _handle_var_decl(node, symbol_table)

        # 验证变量已添加到符号表
        self.assertIn("c", symbol_table["variables"])
        self.assertEqual(symbol_table["variables"]["c"]["data_type"], "char")
        self.assertEqual(symbol_table["variables"]["c"]["line"], 2)
        self.assertEqual(symbol_table["variables"]["c"]["column"], 10)
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_declare_multiple_variables(self):
        """测试：声明多个不同变量"""
        symbol_table = self._create_symbol_table(current_scope=0)
        node1 = self._create_var_decl_node("x", "int", 1, 5)
        node2 = self._create_var_decl_node("y", "char", 2, 5)
        node3 = self._create_var_decl_node("z", "int", 3, 5)

        _handle_var_decl(node1, symbol_table)
        _handle_var_decl(node2, symbol_table)
        _handle_var_decl(node3, symbol_table)

        # 验证所有变量都已添加
        self.assertEqual(len(symbol_table["variables"]), 3)
        self.assertIn("x", symbol_table["variables"])
        self.assertIn("y", symbol_table["variables"])
        self.assertIn("z", symbol_table["variables"])
        self.assertEqual(len(symbol_table["errors"]), 0)

    # ==================== 边界值测试 ====================

    def test_declare_variable_at_scope_boundary(self):
        """测试：在不同作用域边界声明变量"""
        # 在作用域 0 声明变量
        symbol_table = self._create_symbol_table(current_scope=0)
        node1 = self._create_var_decl_node("x", "int", 1, 5)
        _handle_var_decl(node1, symbol_table)

        # 切换到作用域 1
        symbol_table["current_scope"] = 1
        node2 = self._create_var_decl_node("y", "int", 2, 5)
        _handle_var_decl(node2, symbol_table)

        # 验证两个变量都存在
        self.assertIn("x", symbol_table["variables"])
        self.assertIn("y", symbol_table["variables"])
        self.assertEqual(symbol_table["variables"]["x"]["scope_level"], 0)
        self.assertEqual(symbol_table["variables"]["y"]["scope_level"], 1)
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_declare_variable_with_special_name(self):
        """测试：声明特殊名称的变量（单字符、下划线等）"""
        symbol_table = self._create_symbol_table(current_scope=0)
        node = self._create_var_decl_node("_temp", "int", 1, 5)

        _handle_var_decl(node, symbol_table)

        self.assertIn("_temp", symbol_table["variables"])
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_declare_variable_at_line_column_zero(self):
        """测试：在行号列号为 0 的位置声明变量"""
        symbol_table = self._create_symbol_table(current_scope=0)
        node = self._create_var_decl_node("x", "int", 0, 0)

        _handle_var_decl(node, symbol_table)

        self.assertIn("x", symbol_table["variables"])
        self.assertEqual(symbol_table["variables"]["x"]["line"], 0)
        self.assertEqual(symbol_table["variables"]["x"]["column"], 0)

    # ==================== 重复声明测试（错误路径） ====================

    def test_duplicate_declaration_same_scope(self):
        """测试：同一作用域内重复声明变量（应记录错误）"""
        symbol_table = self._create_symbol_table(current_scope=0)
        node1 = self._create_var_decl_node("x", "int", 1, 5)
        node2 = self._create_var_decl_node("x", "char", 2, 10)

        _handle_var_decl(node1, symbol_table)
        _handle_var_decl(node2, symbol_table)

        # 验证记录了错误
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("Variable 'x' already declared", symbol_table["errors"][0])
        self.assertIn("line 2", symbol_table["errors"][0])
        self.assertIn("column 10", symbol_table["errors"][0])
        # 验证符号表中的变量仍是第一次声明的信息
        self.assertEqual(symbol_table["variables"]["x"]["data_type"], "int")
        self.assertEqual(symbol_table["variables"]["x"]["line"], 1)

    def test_duplicate_declaration_same_scope_multiple_times(self):
        """测试：同一作用域内多次重复声明变量"""
        symbol_table = self._create_symbol_table(current_scope=0)
        node1 = self._create_var_decl_node("x", "int", 1, 5)
        node2 = self._create_var_decl_node("x", "char", 2, 10)
        node3 = self._create_var_decl_node("x", "int", 3, 15)

        _handle_var_decl(node1, symbol_table)
        _handle_var_decl(node2, symbol_table)
        _handle_var_decl(node3, symbol_table)

        # 验证记录了两条错误
        self.assertEqual(len(symbol_table["errors"]), 2)
        # 验证符号表中的变量仍是第一次声明的信息
        self.assertEqual(symbol_table["variables"]["x"]["data_type"], "int")
        self.assertEqual(symbol_table["variables"]["x"]["line"], 1)

    # ==================== 不同作用域测试 ====================

    def test_same_name_different_scope_no_error(self):
        """测试：不同作用域内同名变量不应报错"""
        symbol_table = self._create_symbol_table(current_scope=0)
        node1 = self._create_var_decl_node("x", "int", 1, 5)
        _handle_var_decl(node1, symbol_table)

        # 切换到作用域 1
        symbol_table["current_scope"] = 1
        node2 = self._create_var_decl_node("x", "char", 2, 10)
        _handle_var_decl(node2, symbol_table)

        # 验证没有错误
        self.assertEqual(len(symbol_table["errors"]), 0)
        # 验证变量信息被更新为新作用域的声明
        self.assertEqual(symbol_table["variables"]["x"]["data_type"], "char")
        self.assertEqual(symbol_table["variables"]["x"]["line"], 2)
        self.assertEqual(symbol_table["variables"]["x"]["scope_level"], 1)

    def test_variable_declared_in_inner_scope_then_outer_scope(self):
        """测试：先在内层作用域声明，再在外层作用域声明同名变量"""
        symbol_table = self._create_symbol_table(current_scope=2)
        node1 = self._create_var_decl_node("x", "int", 1, 5)
        _handle_var_decl(node1, symbol_table)

        # 切换到作用域 1
        symbol_table["current_scope"] = 1
        node2 = self._create_var_decl_node("x", "char", 2, 10)
        _handle_var_decl(node2, symbol_table)

        # 验证没有错误（不同作用域）
        self.assertEqual(len(symbol_table["errors"]), 0)
        # 验证变量信息被更新
        self.assertEqual(symbol_table["variables"]["x"]["scope_level"], 1)

    # ==================== 副作用测试 ====================

    def test_symbol_table_variables_modified_in_place(self):
        """测试：符号表 variables 被原地修改"""
        symbol_table = self._create_symbol_table(current_scope=0)
        original_variables = symbol_table["variables"]
        node = self._create_var_decl_node("x", "int", 1, 5)

        _handle_var_decl(node, symbol_table)

        # 验证是同一个字典对象
        self.assertIs(symbol_table["variables"], original_variables)
        self.assertIn("x", symbol_table["variables"])

    def test_symbol_table_errors_modified_in_place(self):
        """测试：符号表 errors 被原地修改"""
        symbol_table = self._create_symbol_table(current_scope=0)
        original_errors = symbol_table["errors"]
        node1 = self._create_var_decl_node("x", "int", 1, 5)
        node2 = self._create_var_decl_node("x", "char", 2, 10)

        _handle_var_decl(node1, symbol_table)
        _handle_var_decl(node2, symbol_table)

        # 验证是同一个列表对象
        self.assertIs(symbol_table["errors"], original_errors)
        self.assertEqual(len(symbol_table["errors"]), 1)

    def test_return_value_is_none(self):
        """测试：函数返回值为 None"""
        symbol_table = self._create_symbol_table(current_scope=0)
        node = self._create_var_decl_node("x", "int", 1, 5)

        result = _handle_var_decl(node, symbol_table)

        self.assertIsNone(result)

    # ==================== 复杂场景测试 ====================

    def test_mixed_declarations_with_duplicates(self):
        """测试：混合场景 - 多个变量声明包含重复"""
        symbol_table = self._create_symbol_table(current_scope=0)
        nodes = [
            self._create_var_decl_node("a", "int", 1, 5),
            self._create_var_decl_node("b", "char", 2, 5),
            self._create_var_decl_node("a", "char", 3, 5),  # 重复
            self._create_var_decl_node("c", "int", 4, 5),
            self._create_var_decl_node("b", "int", 5, 5),   # 重复
        ]

        for node in nodes:
            _handle_var_decl(node, symbol_table)

        # 验证有 3 个不同变量
        self.assertEqual(len(symbol_table["variables"]), 3)
        self.assertIn("a", symbol_table["variables"])
        self.assertIn("b", symbol_table["variables"])
        self.assertIn("c", symbol_table["variables"])
        # 验证有 2 条错误
        self.assertEqual(len(symbol_table["errors"]), 2)

    def test_error_message_format(self):
        """测试：错误消息格式正确"""
        symbol_table = self._create_symbol_table(current_scope=0)
        node1 = self._create_var_decl_node("myVar", "int", 10, 20)
        node2 = self._create_var_decl_node("myVar", "char", 15, 25)

        _handle_var_decl(node1, symbol_table)
        _handle_var_decl(node2, symbol_table)

        error_msg = symbol_table["errors"][0]
        self.assertIn("myVar", error_msg)
        self.assertIn("line 15", error_msg)
        self.assertIn("column 25", error_msg)


class TestHandleVarDeclEdgeCases(unittest.TestCase):
    """_handle_var_decl 边界情况测试类"""

    def _create_symbol_table(self, current_scope: int = 0) -> SymbolTable:
        """辅助方法：创建符号表"""
        return {
            "variables": {},
            "functions": {},
            "current_scope": current_scope,
            "scope_stack": [],
            "errors": []
        }

    def _create_var_decl_node(
        self,
        var_name: str,
        data_type: str,
        line: int,
        column: int
    ) -> AST:
        """辅助方法：创建变量声明节点"""
        return {
            "type": "var_decl",
            "value": var_name,
            "data_type": data_type,
            "line": line,
            "column": column
        }

    def test_empty_variable_name(self):
        """测试：空变量名"""
        symbol_table = self._create_symbol_table(current_scope=0)
        node = self._create_var_decl_node("", "int", 1, 5)

        _handle_var_decl(node, symbol_table)

        self.assertIn("", symbol_table["variables"])
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_large_line_column_numbers(self):
        """测试：大行号列号"""
        symbol_table = self._create_symbol_table(current_scope=0)
        node = self._create_var_decl_node("x", "int", 99999, 88888)

        _handle_var_decl(node, symbol_table)

        self.assertIn("x", symbol_table["variables"])
        self.assertEqual(symbol_table["variables"]["x"]["line"], 99999)
        self.assertEqual(symbol_table["variables"]["x"]["column"], 88888)

    def test_high_scope_level(self):
        """测试：高作用域层级"""
        symbol_table = self._create_symbol_table(current_scope=100)
        node = self._create_var_decl_node("x", "int", 1, 5)

        _handle_var_decl(node, symbol_table)

        self.assertEqual(symbol_table["variables"]["x"]["scope_level"], 100)


if __name__ == "__main__":
    unittest.main()

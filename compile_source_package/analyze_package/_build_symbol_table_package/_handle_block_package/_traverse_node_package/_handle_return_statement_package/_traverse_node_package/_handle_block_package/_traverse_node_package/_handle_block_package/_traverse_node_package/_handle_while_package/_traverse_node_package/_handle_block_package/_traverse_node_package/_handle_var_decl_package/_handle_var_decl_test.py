# -*- coding: utf-8 -*-
"""单元测试文件：_handle_var_decl 函数的测试用例"""

import unittest

# 相对导入被测模块
from ._handle_var_decl_src import _handle_var_decl, AST, SymbolTable


class TestHandleVarDecl(unittest.TestCase):
    """_handle_var_decl 函数的单元测试类"""

    def setUp(self) -> None:
        """每个测试用例前的准备工作"""
        pass

    def tearDown(self) -> None:
        """每个测试用例后的清理工作"""
        pass

    def _create_symbol_table(self, current_scope: int = 0) -> SymbolTable:
        """创建初始化的符号表"""
        return {
            "variables": {},
            "functions": {},
            "current_scope": current_scope,
            "scope_stack": [],
            "errors": []
        }

    def _create_var_decl_node(
        self,
        value: str,
        data_type: str,
        line: int,
        column: int
    ) -> AST:
        """创建变量声明节点"""
        return {
            "type": "var_decl",
            "value": value,
            "data_type": data_type,
            "line": line,
            "column": column
        }

    # ========== Happy Path 测试 ==========

    def test_handle_var_decl_new_variable_int(self) -> None:
        """测试：声明一个新的 int 类型变量"""
        symbol_table = self._create_symbol_table(current_scope=0)
        node = self._create_var_decl_node(
            value="x",
            data_type="int",
            line=1,
            column=5
        )

        _handle_var_decl(node, symbol_table)

        # 验证变量已添加到符号表
        self.assertIn("x", symbol_table["variables"])
        var_info = symbol_table["variables"]["x"]
        self.assertEqual(var_info["data_type"], "int")
        self.assertTrue(var_info["is_declared"])
        self.assertEqual(var_info["line"], 1)
        self.assertEqual(var_info["column"], 5)
        self.assertEqual(var_info["scope_level"], 0)
        # 验证没有错误
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_handle_var_decl_new_variable_char(self) -> None:
        """测试：声明一个新的 char 类型变量"""
        symbol_table = self._create_symbol_table(current_scope=0)
        node = self._create_var_decl_node(
            value="c",
            data_type="char",
            line=2,
            column=10
        )

        _handle_var_decl(node, symbol_table)

        # 验证变量已添加到符号表
        self.assertIn("c", symbol_table["variables"])
        var_info = symbol_table["variables"]["c"]
        self.assertEqual(var_info["data_type"], "char")
        self.assertTrue(var_info["is_declared"])
        self.assertEqual(var_info["line"], 2)
        self.assertEqual(var_info["column"], 10)
        self.assertEqual(var_info["scope_level"], 0)
        # 验证没有错误
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_handle_var_decl_new_variable_in_nested_scope(self) -> None:
        """测试：在嵌套作用域中声明新变量"""
        symbol_table = self._create_symbol_table(current_scope=2)
        node = self._create_var_decl_node(
            value="nested_var",
            data_type="int",
            line=5,
            column=3
        )

        _handle_var_decl(node, symbol_table)

        # 验证变量已添加到符号表，并记录正确的 scope_level
        self.assertIn("nested_var", symbol_table["variables"])
        var_info = symbol_table["variables"]["nested_var"]
        self.assertEqual(var_info["scope_level"], 2)
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_handle_var_decl_multiple_variables(self) -> None:
        """测试：连续声明多个不同的变量"""
        symbol_table = self._create_symbol_table(current_scope=0)

        node1 = self._create_var_decl_node("a", "int", 1, 1)
        node2 = self._create_var_decl_node("b", "char", 2, 2)
        node3 = self._create_var_decl_node("c", "int", 3, 3)

        _handle_var_decl(node1, symbol_table)
        _handle_var_decl(node2, symbol_table)
        _handle_var_decl(node3, symbol_table)

        # 验证所有变量都已添加
        self.assertEqual(len(symbol_table["variables"]), 3)
        self.assertIn("a", symbol_table["variables"])
        self.assertIn("b", symbol_table["variables"])
        self.assertIn("c", symbol_table["variables"])
        # 验证没有错误
        self.assertEqual(len(symbol_table["errors"]), 0)

    # ========== 边界值测试 ==========

    def test_handle_var_decl_variable_with_special_name(self) -> None:
        """测试：声明带有特殊字符的变量名"""
        symbol_table = self._create_symbol_table(current_scope=0)
        node = self._create_var_decl_node(
            value="_private_var",
            data_type="int",
            line=1,
            column=1
        )

        _handle_var_decl(node, symbol_table)

        self.assertIn("_private_var", symbol_table["variables"])
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_handle_var_decl_variable_at_line_zero(self) -> None:
        """测试：变量声明在第 0 行"""
        symbol_table = self._create_symbol_table(current_scope=0)
        node = self._create_var_decl_node(
            value="x",
            data_type="int",
            line=0,
            column=0
        )

        _handle_var_decl(node, symbol_table)

        self.assertIn("x", symbol_table["variables"])
        var_info = symbol_table["variables"]["x"]
        self.assertEqual(var_info["line"], 0)
        self.assertEqual(var_info["column"], 0)

    def test_handle_var_decl_variable_at_large_line_column(self) -> None:
        """测试：变量声明在很大的行号和列号"""
        symbol_table = self._create_symbol_table(current_scope=0)
        node = self._create_var_decl_node(
            value="x",
            data_type="int",
            line=9999,
            column=8888
        )

        _handle_var_decl(node, symbol_table)

        self.assertIn("x", symbol_table["variables"])
        var_info = symbol_table["variables"]["x"]
        self.assertEqual(var_info["line"], 9999)
        self.assertEqual(var_info["column"], 8888)

    # ========== 重复声明测试（错误路径） ==========

    def test_handle_var_decl_duplicate_variable(self) -> None:
        """测试：重复声明同一个变量"""
        symbol_table = self._create_symbol_table(current_scope=0)

        # 先声明一次
        node1 = self._create_var_decl_node("x", "int", 1, 1)
        _handle_var_decl(node1, symbol_table)

        # 再次声明同一个变量
        node2 = self._create_var_decl_node("x", "char", 2, 2)
        _handle_var_decl(node2, symbol_table)

        # 验证只记录了一个变量
        self.assertEqual(len(symbol_table["variables"]), 1)
        self.assertIn("x", symbol_table["variables"])
        # 验证第一次声明的信息保持不变
        var_info = symbol_table["variables"]["x"]
        self.assertEqual(var_info["data_type"], "int")
        self.assertEqual(var_info["line"], 1)
        self.assertEqual(var_info["column"], 1)
        # 验证记录了错误
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("重复声明变量 'x' (line 2, column 2)", symbol_table["errors"])

    def test_handle_var_decl_multiple_duplicate_declarations(self) -> None:
        """测试：多次重复声明同一个变量"""
        symbol_table = self._create_symbol_table(current_scope=0)

        # 先声明一次
        node1 = self._create_var_decl_node("x", "int", 1, 1)
        _handle_var_decl(node1, symbol_table)

        # 重复声明两次
        node2 = self._create_var_decl_node("x", "char", 2, 2)
        node3 = self._create_var_decl_node("x", "int", 3, 3)
        _handle_var_decl(node2, symbol_table)
        _handle_var_decl(node3, symbol_table)

        # 验证记录了两个错误
        self.assertEqual(len(symbol_table["errors"]), 2)
        self.assertIn("重复声明变量 'x' (line 2, column 2)", symbol_table["errors"])
        self.assertIn("重复声明变量 'x' (line 3, column 3)", symbol_table["errors"])

    def test_handle_var_decl_duplicate_in_different_scope(self) -> None:
        """测试：在不同作用域中重复声明变量（仍然报错）"""
        symbol_table = self._create_symbol_table(current_scope=0)

        # 在 scope 0 声明
        node1 = self._create_var_decl_node("x", "int", 1, 1)
        _handle_var_decl(node1, symbol_table)

        # 切换到 scope 1
        symbol_table["current_scope"] = 1

        # 在 scope 1 重复声明
        node2 = self._create_var_decl_node("x", "char", 2, 2)
        _handle_var_decl(node2, symbol_table)

        # 验证记录了错误
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("重复声明变量 'x' (line 2, column 2)", symbol_table["errors"])

    # ========== 非法输入/异常输入测试 ==========

    def test_handle_var_decl_node_with_missing_value(self) -> None:
        """测试：节点缺少 value 字段"""
        symbol_table = self._create_symbol_table(current_scope=0)
        node: AST = {
            "type": "var_decl",
            "data_type": "int",
            "line": 1,
            "column": 1
        }

        # 不应该抛出异常，但会添加 None 作为变量名
        _handle_var_decl(node, symbol_table)

        # 验证添加了 None 作为变量名
        self.assertIn(None, symbol_table["variables"])

    def test_handle_var_decl_node_with_missing_data_type(self) -> None:
        """测试：节点缺少 data_type 字段"""
        symbol_table = self._create_symbol_table(current_scope=0)
        node: AST = {
            "type": "var_decl",
            "value": "x",
            "line": 1,
            "column": 1
        }

        _handle_var_decl(node, symbol_table)

        # 验证变量已添加，data_type 为 None
        self.assertIn("x", symbol_table["variables"])
        var_info = symbol_table["variables"]["x"]
        self.assertIsNone(var_info["data_type"])

    def test_handle_var_decl_node_with_missing_line(self) -> None:
        """测试：节点缺少 line 字段"""
        symbol_table = self._create_symbol_table(current_scope=0)
        node: AST = {
            "type": "var_decl",
            "value": "x",
            "data_type": "int",
            "column": 1
        }

        _handle_var_decl(node, symbol_table)

        # 验证变量已添加，line 为 None
        self.assertIn("x", symbol_table["variables"])
        var_info = symbol_table["variables"]["x"]
        self.assertIsNone(var_info["line"])

    def test_handle_var_decl_node_with_missing_column(self) -> None:
        """测试：节点缺少 column 字段"""
        symbol_table = self._create_symbol_table(current_scope=0)
        node: AST = {
            "type": "var_decl",
            "value": "x",
            "data_type": "int",
            "line": 1
        }

        _handle_var_decl(node, symbol_table)

        # 验证变量已添加，column 为 None
        self.assertIn("x", symbol_table["variables"])
        var_info = symbol_table["variables"]["x"]
        self.assertIsNone(var_info["column"])

    def test_handle_var_decl_empty_node(self) -> None:
        """测试：空节点"""
        symbol_table = self._create_symbol_table(current_scope=0)
        node: AST = {}

        _handle_var_decl(node, symbol_table)

        # 验证添加了 None 作为变量名
        self.assertIn(None, symbol_table["variables"])

    def test_handle_var_decl_symbol_table_without_current_scope(self) -> None:
        """测试：符号表缺少 current_scope 字段"""
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "errors": []
        }
        node = self._create_var_decl_node("x", "int", 1, 1)

        _handle_var_decl(node, symbol_table)

        # 验证变量已添加，scope_level 默认为 0
        self.assertIn("x", symbol_table["variables"])
        var_info = symbol_table["variables"]["x"]
        self.assertEqual(var_info["scope_level"], 0)

    def test_handle_var_decl_symbol_table_without_errors_list(self) -> None:
        """测试：符号表缺少 errors 字段（应该抛出异常）"""
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0
        }
        node = self._create_var_decl_node("x", "int", 1, 1)

        # 第一次声明应该成功
        _handle_var_decl(node, symbol_table)

        # 重复声明时，尝试访问 errors 会抛出 KeyError
        node2 = self._create_var_decl_node("x", "char", 2, 2)
        with self.assertRaises(KeyError):
            _handle_var_decl(node2, symbol_table)

    # ========== 副作用测试 ==========

    def test_handle_var_decl_does_not_modify_node(self) -> None:
        """测试：函数不会修改输入节点"""
        symbol_table = self._create_symbol_table(current_scope=0)
        node = self._create_var_decl_node("x", "int", 1, 1)
        original_node = node.copy()

        _handle_var_decl(node, symbol_table)

        # 验证节点未被修改
        self.assertEqual(node, original_node)

    def test_handle_var_decl_preserves_existing_variables(self) -> None:
        """测试：添加新变量时不影响已有变量"""
        symbol_table = self._create_symbol_table(current_scope=0)
        # 预先添加一个变量
        symbol_table["variables"]["existing"] = {
            "data_type": "int",
            "is_declared": True,
            "line": 0,
            "column": 0,
            "scope_level": 0
        }

        node = self._create_var_decl_node("new_var", "char", 1, 1)
        _handle_var_decl(node, symbol_table)

        # 验证已有变量仍然存在
        self.assertIn("existing", symbol_table["variables"])
        self.assertIn("new_var", symbol_table["variables"])
        self.assertEqual(len(symbol_table["variables"]), 2)


if __name__ == "__main__":
    unittest.main()

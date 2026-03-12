# -*- coding: utf-8 -*-
"""
单元测试：_handle_var_decl 函数
测试变量声明的语义分析逻辑
"""

import unittest

# 相对导入被测模块
from ._handle_var_decl_src import _handle_var_decl


class TestHandleVarDecl(unittest.TestCase):
    """测试 _handle_var_decl 函数的各种场景"""

    def setUp(self):
        """每个测试前的准备工作"""
        pass

    def tearDown(self):
        """每个测试后的清理工作"""
        pass

    def _create_mock_symbol_table(self, current_scope=0):
        """创建模拟符号表"""
        return {
            "variables": {},
            "functions": {},
            "current_scope": current_scope,
            "scope_stack": [],
            "errors": []
        }

    def _create_var_decl_node(self, name, data_type="int", line=1, column=1):
        """创建模拟 var_decl AST 节点"""
        return {
            "type": "var_decl",
            "name": name,
            "data_type": data_type,
            "line": line,
            "column": column
        }

    # ==================== Happy Path 测试 ====================

    def test_register_new_variable_successfully(self):
        """测试成功注册新变量"""
        symbol_table = self._create_mock_symbol_table(current_scope=0)
        node = self._create_var_decl_node(name="x", data_type="int", line=1, column=1)

        _handle_var_decl(node, symbol_table)

        # 验证变量已注册
        self.assertIn("x", symbol_table["variables"])
        var_info = symbol_table["variables"]["x"]
        self.assertEqual(var_info["data_type"], "int")
        self.assertEqual(var_info["is_declared"], True)
        self.assertEqual(var_info["line"], 1)
        self.assertEqual(var_info["column"], 1)
        self.assertEqual(var_info["scope_level"], 0)
        # 验证没有错误
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_register_variable_with_char_type(self):
        """测试注册 char 类型变量"""
        symbol_table = self._create_mock_symbol_table(current_scope=0)
        node = self._create_var_decl_node(name="c", data_type="char", line=5, column=10)

        _handle_var_decl(node, symbol_table)

        var_info = symbol_table["variables"]["c"]
        self.assertEqual(var_info["data_type"], "char")
        self.assertEqual(var_info["line"], 5)
        self.assertEqual(var_info["column"], 10)

    def test_register_multiple_variables_in_same_scope(self):
        """测试在同一作用域注册多个不同名称的变量"""
        symbol_table = self._create_mock_symbol_table(current_scope=0)
        node1 = self._create_var_decl_node(name="x", line=1, column=1)
        node2 = self._create_var_decl_node(name="y", line=2, column=1)
        node3 = self._create_var_decl_node(name="z", line=3, column=1)

        _handle_var_decl(node1, symbol_table)
        _handle_var_decl(node2, symbol_table)
        _handle_var_decl(node3, symbol_table)

        self.assertEqual(len(symbol_table["variables"]), 3)
        self.assertIn("x", symbol_table["variables"])
        self.assertIn("y", symbol_table["variables"])
        self.assertIn("z", symbol_table["variables"])
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_register_variable_in_different_scope(self):
        """测试在不同作用域注册同名变量（允许）"""
        symbol_table = self._create_mock_symbol_table(current_scope=0)
        node1 = self._create_var_decl_node(name="x", line=1, column=1)

        _handle_var_decl(node1, symbol_table)

        # 切换到不同作用域
        symbol_table["current_scope"] = 1
        node2 = self._create_var_decl_node(name="x", line=5, column=1)
        _handle_var_decl(node2, symbol_table)

        # 同名变量在不同作用域应该被更新（或允许）
        # 根据实现逻辑，不同作用域允许同名变量
        self.assertIn("x", symbol_table["variables"])
        var_info = symbol_table["variables"]["x"]
        # 应该是新作用域的变量信息
        self.assertEqual(var_info["scope_level"], 1)
        self.assertEqual(var_info["line"], 5)
        self.assertEqual(len(symbol_table["errors"]), 0)

    # ==================== 边界值测试 ====================

    def test_variable_with_empty_name(self):
        """测试空名称变量的处理"""
        symbol_table = self._create_mock_symbol_table(current_scope=0)
        node = self._create_var_decl_node(name="", line=1, column=1)

        _handle_var_decl(node, symbol_table)

        # 空名称也应该被注册（实现没有特殊处理）
        self.assertIn("", symbol_table["variables"])

    def test_variable_with_default_data_type(self):
        """测试未指定数据类型时使用默认值 int"""
        symbol_table = self._create_mock_symbol_table(current_scope=0)
        node = {
            "type": "var_decl",
            "name": "x",
            "line": 1,
            "column": 1
            # 没有 data_type 字段
        }

        _handle_var_decl(node, symbol_table)

        var_info = symbol_table["variables"]["x"]
        self.assertEqual(var_info["data_type"], "int")

    def test_variable_with_missing_line_column(self):
        """测试缺失行号列号时使用默认值 0"""
        symbol_table = self._create_mock_symbol_table(current_scope=0)
        node = {
            "type": "var_decl",
            "name": "x"
            # 没有 line 和 column 字段
        }

        _handle_var_decl(node, symbol_table)

        var_info = symbol_table["variables"]["x"]
        self.assertEqual(var_info["line"], 0)
        self.assertEqual(var_info["column"], 0)

    def test_symbol_table_without_current_scope(self):
        """测试符号表缺少 current_scope 字段时使用默认值 0"""
        symbol_table = {
            "variables": {},
            "errors": []
            # 没有 current_scope 字段
        }
        node = self._create_var_decl_node(name="x", line=1, column=1)

        _handle_var_decl(node, symbol_table)

        var_info = symbol_table["variables"]["x"]
        self.assertEqual(var_info["scope_level"], 0)

    def test_symbol_table_without_variables_field(self):
        """测试符号表缺少 variables 字段时自动初始化"""
        symbol_table = {
            "current_scope": 0,
            "errors": []
        }
        node = self._create_var_decl_node(name="x", line=1, column=1)

        _handle_var_decl(node, symbol_table)

        self.assertIn("variables", symbol_table)
        self.assertIn("x", symbol_table["variables"])

    def test_symbol_table_without_errors_field(self):
        """测试符号表缺少 errors 字段时自动初始化"""
        symbol_table = {
            "current_scope": 0,
            "variables": {}
        }
        node = self._create_var_decl_node(name="x", line=1, column=1)

        _handle_var_decl(node, symbol_table)

        self.assertIn("errors", symbol_table)
        self.assertIsInstance(symbol_table["errors"], list)

    # ==================== 错误场景测试 ====================

    def test_duplicate_declaration_same_scope_records_error(self):
        """测试同一作用域重复声明记录错误"""
        symbol_table = self._create_mock_symbol_table(current_scope=0)
        node1 = self._create_var_decl_node(name="x", line=1, column=1)
        node2 = self._create_var_decl_node(name="x", line=5, column=10)

        _handle_var_decl(node1, symbol_table)
        _handle_var_decl(node2, symbol_table)

        # 验证记录了错误
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["type"], "error")
        self.assertEqual(error["message"], "Variable 'x' already declared")
        self.assertEqual(error["line"], 5)
        self.assertEqual(error["column"], 10)

    def test_duplicate_declaration_does_not_update_variable(self):
        """测试重复声明时不更新原有变量信息"""
        symbol_table = self._create_mock_symbol_table(current_scope=0)
        node1 = self._create_var_decl_node(name="x", data_type="int", line=1, column=1)
        node2 = self._create_var_decl_node(name="x", data_type="char", line=5, column=10)

        _handle_var_decl(node1, symbol_table)
        _handle_var_decl(node2, symbol_table)

        # 验证变量信息保持第一次声明的值
        var_info = symbol_table["variables"]["x"]
        self.assertEqual(var_info["data_type"], "int")
        self.assertEqual(var_info["line"], 1)
        self.assertEqual(var_info["column"], 1)
        self.assertEqual(var_info["scope_level"], 0)

    def test_multiple_duplicate_declarations_record_multiple_errors(self):
        """测试多次重复声明记录多个错误"""
        symbol_table = self._create_mock_symbol_table(current_scope=0)
        node1 = self._create_var_decl_node(name="x", line=1, column=1)
        node2 = self._create_var_decl_node(name="x", line=2, column=1)
        node3 = self._create_var_decl_node(name="x", line=3, column=1)

        _handle_var_decl(node1, symbol_table)
        _handle_var_decl(node2, symbol_table)
        _handle_var_decl(node3, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 2)
        self.assertEqual(symbol_table["errors"][0]["line"], 2)
        self.assertEqual(symbol_table["errors"][1]["line"], 3)

    def test_duplicate_declaration_different_scope_no_error(self):
        """测试不同作用域的同名变量不记录错误"""
        symbol_table = self._create_mock_symbol_table(current_scope=0)
        node1 = self._create_var_decl_node(name="x", line=1, column=1)

        _handle_var_decl(node1, symbol_table)

        # 切换到不同作用域
        symbol_table["current_scope"] = 1
        node2 = self._create_var_decl_node(name="x", line=5, column=1)
        _handle_var_decl(node2, symbol_table)

        # 不同作用域允许同名，不记录错误
        self.assertEqual(len(symbol_table["errors"]), 0)
        # 变量信息被更新为新作用域的
        var_info = symbol_table["variables"]["x"]
        self.assertEqual(var_info["scope_level"], 1)
        self.assertEqual(var_info["line"], 5)

    # ==================== 副作用测试 ====================

    def test_function_modifies_passed_symbol_table(self):
        """测试函数修改传入的符号表对象"""
        symbol_table = self._create_mock_symbol_table(current_scope=0)
        original_id = id(symbol_table)
        node = self._create_var_decl_node(name="x", line=1, column=1)

        _handle_var_decl(node, symbol_table)

        # 验证是同一个对象被修改
        self.assertEqual(id(symbol_table), original_id)
        self.assertIn("x", symbol_table["variables"])

    def test_function_returns_none(self):
        """测试函数返回 None"""
        symbol_table = self._create_mock_symbol_table(current_scope=0)
        node = self._create_var_decl_node(name="x", line=1, column=1)

        result = _handle_var_decl(node, symbol_table)

        self.assertIsNone(result)

    def test_error_does_not_append_when_no_duplicate(self):
        """测试没有重复声明时不追加错误"""
        symbol_table = self._create_mock_symbol_table(current_scope=0)
        symbol_table["errors"] = [{"type": "warning", "message": "pre-existing"}]
        node = self._create_var_decl_node(name="x", line=1, column=1)

        _handle_var_decl(node, symbol_table)

        # 错误列表长度不变
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertEqual(symbol_table["errors"][0]["message"], "pre-existing")


class TestHandleVarDeclEdgeCases(unittest.TestCase):
    """测试边界和特殊情况"""

    def test_node_with_extra_fields(self):
        """测试节点包含额外字段时的处理"""
        symbol_table = {
            "variables": {},
            "current_scope": 0,
            "errors": []
        }
        node = {
            "type": "var_decl",
            "name": "x",
            "data_type": "int",
            "line": 1,
            "column": 1,
            "extra_field": "should_be_ignored",
            "children": []
        }

        _handle_var_decl(node, symbol_table)

        self.assertIn("x", symbol_table["variables"])
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_node_is_empty_dict(self):
        """测试空节点字典的处理"""
        symbol_table = self._create_mock_symbol_table(current_scope=0)
        node = {}

        _handle_var_decl(node, symbol_table)

        # 空名称也会被注册
        self.assertIn("", symbol_table["variables"])
        var_info = symbol_table["variables"][""]
        self.assertEqual(var_info["data_type"], "int")
        self.assertEqual(var_info["line"], 0)
        self.assertEqual(var_info["column"], 0)

    def test_special_characters_in_variable_name(self):
        """测试变量名包含特殊字符"""
        symbol_table = self._create_mock_symbol_table(current_scope=0)
        node = self._create_var_decl_node(name="_private_var", line=1, column=1)

        _handle_var_decl(node, symbol_table)

        self.assertIn("_private_var", symbol_table["variables"])

    def test_numeric_string_as_variable_name(self):
        """测试数字字符串作为变量名"""
        symbol_table = self._create_mock_symbol_table(current_scope=0)
        node = self._create_var_decl_node(name="var123", line=1, column=1)

        _handle_var_decl(node, symbol_table)

        self.assertIn("var123", symbol_table["variables"])


if __name__ == "__main__":
    unittest.main()

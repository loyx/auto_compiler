# -*- coding: utf-8 -*-
"""
单元测试文件：_handle_literal 函数测试
测试字面量 AST 节点处理逻辑
"""

import unittest
from typing import Any, Dict

# 相对导入被测模块
from ._handle_literal_src import _handle_literal


# 类型别名（与被测模块保持一致）
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleLiteral(unittest.TestCase):
    """_handle_literal 函数测试用例"""

    def test_valid_int_literal(self):
        """测试有效的 int 类型字面量 - 不应产生警告"""
        node: AST = {
            "type": "literal",
            "value": 42,
            "data_type": "int",
            "line": 10,
            "column": 5
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 1,
            "errors": []
        }

        result = _handle_literal(node, symbol_table)

        self.assertIsNone(result)
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_valid_char_literal(self):
        """测试有效的 char 类型字面量 - 不应产生警告"""
        node: AST = {
            "type": "literal",
            "value": 'A',
            "data_type": "char",
            "line": 15,
            "column": 8
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 1,
            "errors": []
        }

        result = _handle_literal(node, symbol_table)

        self.assertIsNone(result)
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_invalid_data_type(self):
        """测试无效的数据类型 - 应产生警告"""
        node: AST = {
            "type": "literal",
            "value": 3.14,
            "data_type": "float",
            "line": 20,
            "column": 12
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 1,
            "errors": []
        }

        result = _handle_literal(node, symbol_table)

        self.assertIsNone(result)
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertEqual(symbol_table["errors"][0]["type"], "warning")
        self.assertEqual(
            symbol_table["errors"][0]["message"],
            "Invalid data type 'float' for literal"
        )
        self.assertEqual(symbol_table["errors"][0]["line"], 20)
        self.assertEqual(symbol_table["errors"][0]["column"], 12)

    def test_missing_data_type(self):
        """测试缺失 data_type 字段 - 应产生警告（默认为空字符串）"""
        node: AST = {
            "type": "literal",
            "value": 100,
            "line": 25,
            "column": 3
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 1,
            "errors": []
        }

        result = _handle_literal(node, symbol_table)

        self.assertIsNone(result)
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertEqual(
            symbol_table["errors"][0]["message"],
            "Invalid data type '' for literal"
        )

    def test_empty_symbol_table_errors(self):
        """测试 symbol_table 中 errors 字段为空列表"""
        node: AST = {
            "type": "literal",
            "value": 'X',
            "data_type": "string",
            "line": 30,
            "column": 7
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 1,
            "errors": []
        }

        result = _handle_literal(node, symbol_table)

        self.assertIsNone(result)
        self.assertEqual(len(symbol_table["errors"]), 1)

    def test_none_errors_in_symbol_table(self):
        """测试 symbol_table 中 errors 字段为 None - 应 gracefully 处理"""
        node: AST = {
            "type": "literal",
            "value": 999,
            "data_type": "unknown",
            "line": 35,
            "column": 10
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 1,
            "errors": None
        }

        # 不应抛出异常
        result = _handle_literal(node, symbol_table)

        self.assertIsNone(result)
        # errors 为 None 时不应添加警告
        self.assertIsNone(symbol_table["errors"])

    def test_missing_errors_in_symbol_table(self):
        """测试 symbol_table 中不存在 errors 字段 - 应 gracefully 处理"""
        node: AST = {
            "type": "literal",
            "value": 123,
            "data_type": "bool",
            "line": 40,
            "column": 15
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 1
        }

        # 不应抛出异常
        result = _handle_literal(node, symbol_table)

        self.assertIsNone(result)

    def test_multiple_invalid_literals(self):
        """测试多个无效字面量 - 应累积警告"""
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 1,
            "errors": []
        }

        nodes = [
            {"type": "literal", "value": 1.0, "data_type": "float", "line": 1, "column": 1},
            {"type": "literal", "value": "test", "data_type": "string", "line": 2, "column": 2},
            {"type": "literal", "value": True, "data_type": "bool", "line": 3, "column": 3},
        ]

        for node in nodes:
            _handle_literal(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 3)

    def test_valid_literal_after_invalid(self):
        """测试有效字面量在无效字面量之后 - 不应添加额外警告"""
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 1,
            "errors": []
        }

        # 先处理无效字面量
        invalid_node: AST = {
            "type": "literal",
            "value": 2.5,
            "data_type": "double",
            "line": 5,
            "column": 5
        }
        _handle_literal(invalid_node, symbol_table)

        # 再处理有效字面量
        valid_node: AST = {
            "type": "literal",
            "value": 42,
            "data_type": "int",
            "line": 6,
            "column": 6
        }
        _handle_literal(valid_node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)

    def test_minimal_node(self):
        """测试最小化节点（仅包含必要字段）"""
        node: AST = {
            "type": "literal"
        }
        symbol_table: SymbolTable = {
            "errors": []
        }

        result = _handle_literal(node, symbol_table)

        self.assertIsNone(result)
        # data_type 默认为空字符串，应产生警告
        self.assertEqual(len(symbol_table["errors"]), 1)

    def test_empty_string_data_type(self):
        """测试 data_type 为空字符串 - 应产生警告"""
        node: AST = {
            "type": "literal",
            "value": 0,
            "data_type": "",
            "line": 50,
            "column": 1
        }
        symbol_table: SymbolTable = {
            "errors": []
        }

        result = _handle_literal(node, symbol_table)

        self.assertIsNone(result)
        self.assertEqual(len(symbol_table["errors"]), 1)

    def test_case_sensitive_data_type(self):
        """测试数据类型大小写敏感 - INT 和 Char 应视为无效"""
        symbol_table: SymbolTable = {
            "errors": []
        }

        # 测试大写 INT
        node_int: AST = {
            "type": "literal",
            "value": 1,
            "data_type": "INT",
            "line": 1,
            "column": 1
        }
        _handle_literal(node_int, symbol_table)

        # 测试混合大小写 Char
        node_char: AST = {
            "type": "literal",
            "value": 'B',
            "data_type": "Char",
            "line": 2,
            "column": 2
        }
        _handle_literal(node_char, symbol_table)

        # 两者都应产生警告
        self.assertEqual(len(symbol_table["errors"]), 2)


if __name__ == "__main__":
    unittest.main()

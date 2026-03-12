# === imports ===
import unittest
from typing import Any, Dict

# === relative import for UUT ===
from ._handle_var_decl_src import _handle_var_decl


# === test class ===
class TestHandleVarDecl(unittest.TestCase):
    """测试 _handle_var_decl 函数"""

    def test_happy_path_declare_new_variable_with_name_field(self):
        """成功路径：使用 name 字段声明新变量"""
        node: Dict[str, Any] = {
            "type": "var_decl",
            "name": "x",
            "data_type": "int",
            "line": 10,
            "column": 5,
        }
        symbol_table: Dict[str, Any] = {
            "variables": {},
            "current_scope": 0,
            "errors": [],
        }

        _handle_var_decl(node, symbol_table)

        self.assertIn("x", symbol_table["variables"])
        self.assertEqual(symbol_table["variables"]["x"]["data_type"], "int")
        self.assertTrue(symbol_table["variables"]["x"]["is_declared"])
        self.assertEqual(symbol_table["variables"]["x"]["line"], 10)
        self.assertEqual(symbol_table["variables"]["x"]["column"], 5)
        self.assertEqual(symbol_table["variables"]["x"]["scope_level"], 0)
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_happy_path_declare_new_variable_with_value_field(self):
        """成功路径：使用 value 字段（fallback）声明新变量"""
        node: Dict[str, Any] = {
            "type": "var_decl",
            "value": "y",
            "data_type": "char",
            "line": 15,
            "column": 8,
        }
        symbol_table: Dict[str, Any] = {
            "variables": {},
            "current_scope": 1,
            "errors": [],
        }

        _handle_var_decl(node, symbol_table)

        self.assertIn("y", symbol_table["variables"])
        self.assertEqual(symbol_table["variables"]["y"]["data_type"], "char")
        self.assertTrue(symbol_table["variables"]["y"]["is_declared"])
        self.assertEqual(symbol_table["variables"]["y"]["line"], 15)
        self.assertEqual(symbol_table["variables"]["y"]["column"], 8)
        self.assertEqual(symbol_table["variables"]["y"]["scope_level"], 1)

    def test_happy_path_default_data_type_is_int(self):
        """成功路径：未指定 data_type 时默认为 int"""
        node: Dict[str, Any] = {
            "type": "var_decl",
            "name": "z",
            "line": 20,
            "column": 3,
        }
        symbol_table: Dict[str, Any] = {
            "variables": {},
            "current_scope": 0,
        }

        _handle_var_decl(node, symbol_table)

        self.assertIn("z", symbol_table["variables"])
        self.assertEqual(symbol_table["variables"]["z"]["data_type"], "int")

    def test_error_cannot_extract_variable_name(self):
        """错误路径：无法提取变量名时记录错误"""
        node: Dict[str, Any] = {
            "type": "var_decl",
            "data_type": "int",
            "line": 25,
            "column": 10,
        }
        symbol_table: Dict[str, Any] = {
            "variables": {},
            "current_scope": 0,
            "errors": [],
        }

        _handle_var_decl(node, symbol_table)

        self.assertNotIn("variables", symbol_table)
        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("Cannot extract variable name", symbol_table["errors"][0])
        self.assertIn("line 25", symbol_table["errors"][0])
        self.assertIn("column 10", symbol_table["errors"][0])

    def test_error_duplicate_variable_declaration(self):
        """错误路径：重复声明变量时记录错误"""
        node1: Dict[str, Any] = {
            "type": "var_decl",
            "name": "dup_var",
            "data_type": "int",
            "line": 30,
            "column": 5,
        }
        node2: Dict[str, Any] = {
            "type": "var_decl",
            "name": "dup_var",
            "data_type": "char",
            "line": 35,
            "column": 8,
        }
        symbol_table: Dict[str, Any] = {
            "variables": {},
            "current_scope": 0,
            "errors": [],
        }

        # 第一次声明
        _handle_var_decl(node1, symbol_table)
        # 第二次声明（重复）
        _handle_var_decl(node2, symbol_table)

        # 变量仍只记录一次（第一次声明的信息）
        self.assertIn("dup_var", symbol_table["variables"])
        self.assertEqual(symbol_table["variables"]["dup_var"]["line"], 30)
        self.assertEqual(symbol_table["variables"]["dup_var"]["column"], 5)
        self.assertEqual(symbol_table["variables"]["dup_var"]["data_type"], "int")
        
        # 记录重复声明错误
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("Variable 'dup_var' already declared", symbol_table["errors"][0])
        self.assertIn("line 30", symbol_table["errors"][0])
        self.assertIn("column 5", symbol_table["errors"][0])

    def test_initialization_variables_key_not_exists(self):
        """边界值：symbol_table 中不存在 variables 键时自动初始化"""
        node: Dict[str, Any] = {
            "type": "var_decl",
            "name": "auto_init",
            "data_type": "int",
            "line": 40,
            "column": 2,
        }
        symbol_table: Dict[str, Any] = {
            "current_scope": 0,
        }

        _handle_var_decl(node, symbol_table)

        self.assertIn("variables", symbol_table)
        self.assertIn("auto_init", symbol_table["variables"])

    def test_initialization_errors_key_not_exists(self):
        """边界值：symbol_table 中不存在 errors 键时自动初始化（错误场景）"""
        node: Dict[str, Any] = {
            "type": "var_decl",
            "line": 45,
            "column": 7,
        }
        symbol_table: Dict[str, Any] = {
            "variables": {},
            "current_scope": 0,
        }

        _handle_var_decl(node, symbol_table)

        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)

    def test_scope_level_tracking(self):
        """状态变化：不同作用域层级的变量声明"""
        node: Dict[str, Any] = {
            "type": "var_decl",
            "name": "scoped_var",
            "data_type": "int",
            "line": 50,
            "column": 4,
        }
        symbol_table: Dict[str, Any] = {
            "variables": {},
            "current_scope": 3,
            "errors": [],
        }

        _handle_var_decl(node, symbol_table)

        self.assertEqual(symbol_table["variables"]["scoped_var"]["scope_level"], 3)

    def test_missing_line_column_defaults(self):
        """边界值：节点缺少 line/column 时使用默认值"""
        node: Dict[str, Any] = {
            "type": "var_decl",
            "name": "no_pos",
        }
        symbol_table: Dict[str, Any] = {
            "variables": {},
            "current_scope": 0,
            "errors": [],
        }

        _handle_var_decl(node, symbol_table)

        self.assertIn("no_pos", symbol_table["variables"])
        self.assertEqual(symbol_table["variables"]["no_pos"]["line"], 0)
        self.assertEqual(symbol_table["variables"]["no_pos"]["column"], 0)

    def test_name_field_takes_priority_over_value(self):
        """多分支逻辑：name 字段优先于 value 字段"""
        node: Dict[str, Any] = {
            "type": "var_decl",
            "name": "priority_name",
            "value": "fallback_value",
            "data_type": "int",
            "line": 55,
            "column": 6,
        }
        symbol_table: Dict[str, Any] = {
            "variables": {},
            "current_scope": 0,
            "errors": [],
        }

        _handle_var_decl(node, symbol_table)

        self.assertIn("priority_name", symbol_table["variables"])
        self.assertNotIn("fallback_value", symbol_table["variables"])


# === main entry ===
if __name__ == "__main__":
    unittest.main()

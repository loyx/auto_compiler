# === std / third-party imports ===
import unittest
from unittest.mock import patch

# === relative imports ===
from ._handle_assignment_src import _handle_assignment


class TestHandleAssignment(unittest.TestCase):
    """单元测试：_handle_assignment 函数"""

    def setUp(self):
        """每个测试前的准备工作"""
        pass

    def tearDown(self):
        """每个测试后的清理工作"""
        pass

    def test_happy_path_variable_declared_type_match(self):
        """Happy Path: 变量已声明且类型匹配"""
        node = {
            "type": "assignment",
            "target": "x",
            "value": {"type": "literal", "value": 10, "data_type": "int"},
            "line": 5,
            "column": 10
        }
        symbol_table = {
            "variables": {
                "x": {"data_type": "int", "is_declared": True, "line": 1, "column": 1, "scope_level": 0}
            },
            "errors": []
        }

        with patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_function_call_package._traverse_node_package._handle_function_decl_package._traverse_node_package._handle_assignment_package._handle_assignment_src._process_ast_node') as mock_process:
            _handle_assignment(node, symbol_table)

        # 验证没有添加错误
        self.assertEqual(len(symbol_table["errors"]), 0)
        # 验证递归处理了 value 节点
        mock_process.assert_called_once_with(node["value"], symbol_table)

    def test_undeclared_variable_adds_error(self):
        """边界值：变量未声明，应添加 undeclared_variable 错误"""
        node = {
            "type": "assignment",
            "target": "y",
            "value": {"type": "literal", "value": 20, "data_type": "int"},
            "line": 10,
            "column": 5
        }
        symbol_table = {
            "variables": {
                "x": {"data_type": "int", "is_declared": True, "line": 1, "column": 1, "scope_level": 0}
            },
            "errors": []
        }

        _handle_assignment(node, symbol_table)

        # 验证添加了错误
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["type"], "undeclared_variable")
        self.assertIn("y", error["message"])
        self.assertEqual(error["line"], 10)
        self.assertEqual(error["column"], 5)

    def test_type_mismatch_adds_error(self):
        """边界值：类型不匹配，应添加 type_mismatch 错误"""
        node = {
            "type": "assignment",
            "target": "x",
            "value": {"type": "literal", "value": "hello", "data_type": "char"},
            "line": 15,
            "column": 8
        }
        symbol_table = {
            "variables": {
                "x": {"data_type": "int", "is_declared": True, "line": 1, "column": 1, "scope_level": 0}
            },
            "errors": []
        }

        with patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_function_call_package._traverse_node_package._handle_function_decl_package._traverse_node_package._handle_assignment_package._handle_assignment_src._process_ast_node') as mock_process:
            _handle_assignment(node, symbol_table)

        # 验证添加了类型不匹配错误
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["type"], "type_mismatch")
        self.assertIn("char", error["message"])
        self.assertIn("int", error["message"])
        self.assertIn("x", error["message"])
        # 即使类型不匹配，仍应递归处理 value 节点
        mock_process.assert_called_once()

    def test_undeclared_variable_returns_early_no_recursive_process(self):
        """多分支逻辑：变量未声明时应提前返回，不递归处理 value"""
        node = {
            "type": "assignment",
            "target": "undeclared_var",
            "value": {"type": "literal", "value": 42, "data_type": "int"},
            "line": 20,
            "column": 3
        }
        symbol_table = {
            "variables": {},
            "errors": []
        }

        with patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_function_call_package._traverse_node_package._handle_function_decl_package._traverse_node_package._handle_assignment_package._handle_assignment_src._process_ast_node') as mock_process:
            _handle_assignment(node, symbol_table)

        # 验证没有调用递归处理
        mock_process.assert_not_called()
        # 验证添加了错误
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertEqual(symbol_table["errors"][0]["type"], "undeclared_variable")

    def test_value_is_list_processes_all_children(self):
        """副作用：value 是列表时，应递归处理所有子节点"""
        node = {
            "type": "assignment",
            "target": "x",
            "value": [
                {"type": "literal", "value": 1, "data_type": "int"},
                {"type": "literal", "value": 2, "data_type": "int"},
                {"type": "literal", "value": 3, "data_type": "int"}
            ],
            "line": 25,
            "column": 12
        }
        symbol_table = {
            "variables": {
                "x": {"data_type": "int", "is_declared": True, "line": 1, "column": 1, "scope_level": 0}
            },
            "errors": []
        }

        with patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_function_call_package._traverse_node_package._handle_function_decl_package._traverse_node_package._handle_assignment_package._handle_assignment_src._process_ast_node') as mock_process:
            _handle_assignment(node, symbol_table)

        # 验证调用了 3 次递归处理
        self.assertEqual(mock_process.call_count, 3)

    def test_value_not_dict_or_list_no_recursive_process(self):
        """边界值：value 不是 dict 或 list 时，不递归处理"""
        node = {
            "type": "assignment",
            "target": "x",
            "value": 42,  # 直接是字面量，不是 dict
            "line": 30,
            "column": 7
        }
        symbol_table = {
            "variables": {
                "x": {"data_type": "int", "is_declared": True, "line": 1, "column": 1, "scope_level": 0}
            },
            "errors": []
        }

        with patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_function_call_package._traverse_node_package._handle_function_decl_package._traverse_node_package._handle_assignment_package._handle_assignment_src._process_ast_node') as mock_process:
            _handle_assignment(node, symbol_table)

        # 验证没有调用递归处理
        mock_process.assert_not_called()
        # 验证没有错误
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_uses_name_field_when_target_missing(self):
        """边界值：没有 target 字段时使用 name 字段"""
        node = {
            "type": "assignment",
            "name": "z",  # 使用 name 而非 target
            "value": {"type": "literal", "value": 100, "data_type": "int"},
            "line": 35,
            "column": 9
        }
        symbol_table = {
            "variables": {
                "z": {"data_type": "int", "is_declared": True, "line": 1, "column": 1, "scope_level": 0}
            },
            "errors": []
        }

        with patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_function_call_package._traverse_node_package._handle_function_decl_package._traverse_node_package._handle_assignment_package._handle_assignment_src._process_ast_node') as mock_process:
            _handle_assignment(node, symbol_table)

        # 验证没有错误（变量 z 已声明）
        self.assertEqual(len(symbol_table["errors"]), 0)
        mock_process.assert_called_once()

    def test_empty_symbol_table_creates_errors_list(self):
        """副作用：symbol_table 没有 errors 字段时应自动创建"""
        node = {
            "type": "assignment",
            "target": "a",
            "value": {"type": "literal", "value": 5, "data_type": "int"},
            "line": 40,
            "column": 1
        }
        symbol_table = {
            "variables": {}
            # 没有 errors 字段
        }

        _handle_assignment(node, symbol_table)

        # 验证 errors 字段被创建
        self.assertIn("errors", symbol_table)
        self.assertIsInstance(symbol_table["errors"], list)
        self.assertEqual(len(symbol_table["errors"]), 1)

    def test_no_data_type_no_type_check(self):
        """边界值：变量或 value 没有 data_type 时，不进行类型检查"""
        node = {
            "type": "assignment",
            "target": "x",
            "value": {"type": "literal", "value": 10},  # 没有 data_type
            "line": 45,
            "column": 6
        }
        symbol_table = {
            "variables": {
                "x": {"data_type": "int", "is_declared": True, "line": 1, "column": 1, "scope_level": 0}
            },
            "errors": []
        }

        with patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_function_call_package._traverse_node_package._handle_function_decl_package._traverse_node_package._handle_assignment_package._handle_assignment_src._process_ast_node') as mock_process:
            _handle_assignment(node, symbol_table)

        # 验证没有类型不匹配错误
        self.assertEqual(len(symbol_table["errors"]), 0)
        mock_process.assert_called_once()

    def test_variable_no_data_type_no_type_check(self):
        """边界值：变量没有 data_type 时，不进行类型检查"""
        node = {
            "type": "assignment",
            "target": "x",
            "value": {"type": "literal", "value": 10, "data_type": "int"},
            "line": 50,
            "column": 4
        }
        symbol_table = {
            "variables": {
                "x": {"is_declared": True, "line": 1, "column": 1, "scope_level": 0}
                # 没有 data_type
            },
            "errors": []
        }

        with patch('main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_return_statement_package._traverse_node_package._handle_block_package._traverse_node_package._handle_block_package._traverse_node_package._handle_function_call_package._traverse_node_package._handle_function_decl_package._traverse_node_package._handle_assignment_package._handle_assignment_src._process_ast_node') as mock_process:
            _handle_assignment(node, symbol_table)

        # 验证没有类型不匹配错误
        self.assertEqual(len(symbol_table["errors"]), 0)
        mock_process.assert_called_once()

    def test_missing_line_column_defaults_to_zero(self):
        """边界值：没有 line/column 字段时默认为 0"""
        node = {
            "type": "assignment",
            "target": "missing_info",
            "value": {"type": "literal", "value": 0, "data_type": "int"}
            # 没有 line 和 column
        }
        symbol_table = {
            "variables": {},
            "errors": []
        }

        _handle_assignment(node, symbol_table)

        # 验证错误中的 line 和 column 为 0
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["line"], 0)
        self.assertEqual(error["column"], 0)

    def test_preserves_existing_errors(self):
        """状态变化：不应清除已有错误"""
        node = {
            "type": "assignment",
            "target": "b",
            "value": {"type": "literal", "value": 20, "data_type": "int"},
            "line": 55,
            "column": 11
        }
        symbol_table = {
            "variables": {},
            "errors": [
                {"type": "previous_error", "message": "Existing error", "line": 1, "column": 1}
            ]
        }

        _handle_assignment(node, symbol_table)

        # 验证原有错误保留，新增错误追加
        self.assertEqual(len(symbol_table["errors"]), 2)
        self.assertEqual(symbol_table["errors"][0]["type"], "previous_error")
        self.assertEqual(symbol_table["errors"][1]["type"], "undeclared_variable")


if __name__ == "__main__":
    unittest.main()

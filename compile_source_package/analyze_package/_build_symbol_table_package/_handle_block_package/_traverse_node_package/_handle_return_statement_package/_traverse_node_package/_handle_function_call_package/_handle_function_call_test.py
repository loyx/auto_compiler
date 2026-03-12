# === std / third-party imports ===
import unittest

# === sub function imports ===
from ._handle_function_call_src import (
    _handle_function_call,
    _get_line_column,
    _extract_arguments,
)


class TestHandleFunctionCall(unittest.TestCase):
    """测试 _handle_function_call 函数的各种场景"""

    def setUp(self):
        """每个测试前的准备工作"""
        pass

    def tearDown(self):
        """每个测试后的清理工作"""
        pass

    # ==================== Happy Path 测试 ====================

    def test_valid_function_call_no_errors(self):
        """测试有效的函数调用，无错误"""
        node = {
            "type": "function_call",
            "name": "my_func",
            "line": 10,
            "column": 5,
            "arguments": [
                {"data_type": "int", "value": 1},
                {"data_type": "char", "value": "a"},
            ],
        }
        symbol_table = {
            "functions": {
                "my_func": {
                    "return_type": "int",
                    "params": [
                        {"data_type": "int"},
                        {"data_type": "char"},
                    ],
                    "line": 1,
                    "column": 1,
                }
            },
            "errors": [],
        }

        _handle_function_call(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_valid_function_call_creates_errors_list(self):
        """测试符号表没有 errors 列表时会自动创建"""
        node = {
            "type": "function_call",
            "name": "my_func",
            "line": 10,
            "column": 5,
            "arguments": [],
        }
        symbol_table = {
            "functions": {
                "my_func": {
                    "return_type": "void",
                    "params": [],
                    "line": 1,
                    "column": 1,
                }
            },
        }

        _handle_function_call(node, symbol_table)

        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 0)

    # ==================== 函数未声明测试 ====================

    def test_function_not_declared(self):
        """测试调用未声明的函数"""
        node = {
            "type": "function_call",
            "name": "unknown_func",
            "line": 15,
            "column": 8,
            "arguments": [],
        }
        symbol_table = {
            "functions": {
                "other_func": {
                    "return_type": "void",
                    "params": [],
                    "line": 1,
                    "column": 1,
                }
            },
            "errors": [],
        }

        _handle_function_call(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("unknown_func", symbol_table["errors"][0])
        self.assertIn("line 15", symbol_table["errors"][0])
        self.assertIn("column 8", symbol_table["errors"][0])

    def test_function_not_declared_empty_functions_dict(self):
        """测试符号表中 functions 为空字典"""
        node = {
            "type": "function_call",
            "name": "any_func",
            "line": 20,
            "column": 3,
            "arguments": [],
        }
        symbol_table = {
            "functions": {},
            "errors": [],
        }

        _handle_function_call(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("any_func", symbol_table["errors"][0])

    def test_function_not_declared_no_functions_key(self):
        """测试符号表中没有 functions 键"""
        node = {
            "type": "function_call",
            "name": "any_func",
            "line": 20,
            "column": 3,
            "arguments": [],
        }
        symbol_table = {
            "errors": [],
        }

        _handle_function_call(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)

    # ==================== 参数数量不匹配测试 ====================

    def test_parameter_count_mismatch_too_many(self):
        """测试参数数量过多"""
        node = {
            "type": "function_call",
            "name": "my_func",
            "line": 25,
            "column": 10,
            "arguments": [
                {"data_type": "int", "value": 1},
                {"data_type": "int", "value": 2},
                {"data_type": "int", "value": 3},
            ],
        }
        symbol_table = {
            "functions": {
                "my_func": {
                    "return_type": "void",
                    "params": [
                        {"data_type": "int"},
                        {"data_type": "int"},
                    ],
                    "line": 1,
                    "column": 1,
                }
            },
            "errors": [],
        }

        _handle_function_call(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("expects 2 arguments", symbol_table["errors"][0])
        self.assertIn("got 3", symbol_table["errors"][0])

    def test_parameter_count_mismatch_too_few(self):
        """测试参数数量过少"""
        node = {
            "type": "function_call",
            "name": "my_func",
            "line": 30,
            "column": 12,
            "arguments": [
                {"data_type": "int", "value": 1},
            ],
        }
        symbol_table = {
            "functions": {
                "my_func": {
                    "return_type": "void",
                    "params": [
                        {"data_type": "int"},
                        {"data_type": "int"},
                        {"data_type": "int"},
                    ],
                    "line": 1,
                    "column": 1,
                }
            },
            "errors": [],
        }

        _handle_function_call(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("expects 3 arguments", symbol_table["errors"][0])
        self.assertIn("got 1", symbol_table["errors"][0])

    # ==================== 参数类型不匹配测试 ====================

    def test_parameter_type_mismatch(self):
        """测试参数类型不匹配"""
        node = {
            "type": "function_call",
            "name": "my_func",
            "line": 35,
            "column": 7,
            "arguments": [
                {"data_type": "char", "value": "a"},
                {"data_type": "char", "value": "b"},
            ],
        }
        symbol_table = {
            "functions": {
                "my_func": {
                    "return_type": "void",
                    "params": [
                        {"data_type": "int"},
                        {"data_type": "char"},
                    ],
                    "line": 1,
                    "column": 1,
                }
            },
            "errors": [],
        }

        _handle_function_call(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("Type mismatch", symbol_table["errors"][0])
        self.assertIn("argument 1", symbol_table["errors"][0])
        self.assertIn("expected 'int'", symbol_table["errors"][0])
        self.assertIn("got 'char'", symbol_table["errors"][0])

    def test_parameter_type_mismatch_second_arg(self):
        """测试第二个参数类型不匹配"""
        node = {
            "type": "function_call",
            "name": "my_func",
            "line": 40,
            "column": 7,
            "arguments": [
                {"data_type": "int", "value": 1},
                {"data_type": "int", "value": 2},
            ],
        }
        symbol_table = {
            "functions": {
                "my_func": {
                    "return_type": "void",
                    "params": [
                        {"data_type": "int"},
                        {"data_type": "char"},
                    ],
                    "line": 1,
                    "column": 1,
                }
            },
            "errors": [],
        }

        _handle_function_call(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("argument 2", symbol_table["errors"][0])
        self.assertIn("expected 'char'", symbol_table["errors"][0])
        self.assertIn("got 'int'", symbol_table["errors"][0])

    def test_multiple_type_mismatches(self):
        """测试多个参数类型不匹配"""
        node = {
            "type": "function_call",
            "name": "my_func",
            "line": 45,
            "column": 7,
            "arguments": [
                {"data_type": "char", "value": "a"},
                {"data_type": "char", "value": "b"},
            ],
        }
        symbol_table = {
            "functions": {
                "my_func": {
                    "return_type": "void",
                    "params": [
                        {"data_type": "int"},
                        {"data_type": "int"},
                    ],
                    "line": 1,
                    "column": 1,
                }
            },
            "errors": [],
        }

        _handle_function_call(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 2)
        self.assertIn("argument 1", symbol_table["errors"][0])
        self.assertIn("argument 2", symbol_table["errors"][1])

    # ==================== 边界值测试 ====================

    def test_missing_function_name(self):
        """测试节点没有函数名"""
        node = {
            "type": "function_call",
            "line": 50,
            "column": 5,
            "arguments": [],
        }
        symbol_table = {
            "functions": {},
            "errors": [],
        }

        _handle_function_call(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_empty_function_name(self):
        """测试函数名为空字符串"""
        node = {
            "type": "function_call",
            "name": "",
            "line": 50,
            "column": 5,
            "arguments": [],
        }
        symbol_table = {
            "functions": {},
            "errors": [],
        }

        _handle_function_call(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_no_arguments_field(self):
        """测试节点没有 arguments 字段"""
        node = {
            "type": "function_call",
            "name": "my_func",
            "line": 55,
            "column": 5,
        }
        symbol_table = {
            "functions": {
                "my_func": {
                    "return_type": "void",
                    "params": [],
                    "line": 1,
                    "column": 1,
                }
            },
            "errors": [],
        }

        _handle_function_call(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_arguments_not_list(self):
        """测试 arguments 不是列表"""
        node = {
            "type": "function_call",
            "name": "my_func",
            "line": 60,
            "column": 5,
            "arguments": "not_a_list",
        }
        symbol_table = {
            "functions": {
                "my_func": {
                    "return_type": "void",
                    "params": [],
                    "line": 1,
                    "column": 1,
                }
            },
            "errors": [],
        }

        _handle_function_call(node, symbol_table)

        # 应该使用 children 提取参数
        self.assertEqual(len(symbol_table["errors"]), 0)

    # ==================== 从 children 提取信息测试 ====================

    def test_function_name_from_children(self):
        """测试从 children[0] 提取函数名"""
        node = {
            "type": "function_call",
            "children": [
                {"type": "identifier", "value": "my_func"},
            ],
            "line": 65,
            "column": 5,
            "arguments": [],
        }
        symbol_table = {
            "functions": {
                "my_func": {
                    "return_type": "void",
                    "params": [],
                    "line": 1,
                    "column": 1,
                }
            },
            "errors": [],
        }

        _handle_function_call(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_arguments_from_children(self):
        """测试从 children[1:] 提取参数"""
        node = {
            "type": "function_call",
            "children": [
                {"type": "identifier", "value": "my_func"},
                {"data_type": "int", "value": 1},
                {"data_type": "char", "value": "a"},
            ],
            "line": 70,
            "column": 5,
        }
        symbol_table = {
            "functions": {
                "my_func": {
                    "return_type": "void",
                    "params": [
                        {"data_type": "int"},
                        {"data_type": "char"},
                    ],
                    "line": 1,
                    "column": 1,
                }
            },
            "errors": [],
        }

        _handle_function_call(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_function_name_from_children_empty_children(self):
        """测试 children 为空时函数名为 None"""
        node = {
            "type": "function_call",
            "children": [],
            "line": 75,
            "column": 5,
        }
        symbol_table = {
            "functions": {},
            "errors": [],
        }

        _handle_function_call(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_line_column_from_children(self):
        """测试从 children[0] 提取 line/column"""
        node = {
            "type": "function_call",
            "name": "my_func",
            "children": [
                {"type": "identifier", "value": "my_func", "line": 80, "column": 10},
            ],
            "arguments": [],
        }
        symbol_table = {
            "functions": {},
            "errors": [],
        }

        _handle_function_call(node, symbol_table)

        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("line 80", symbol_table["errors"][0])
        self.assertIn("column 10", symbol_table["errors"][0])


class TestGetLineColumn(unittest.TestCase):
    """测试 _get_line_column 辅助函数"""

    def test_get_line_from_node(self):
        """测试从节点直接获取 line"""
        node = {"line": 100, "column": 5}
        result = _get_line_column(node, "line")
        self.assertEqual(result, 100)

    def test_get_column_from_node(self):
        """测试从节点直接获取 column"""
        node = {"line": 100, "column": 5}
        result = _get_line_column(node, "column")
        self.assertEqual(result, 5)

    def test_get_line_from_children(self):
        """测试从 children[0] 获取 line"""
        node = {
            "children": [
                {"line": 200, "column": 15},
            ]
        }
        result = _get_line_column(node, "line")
        self.assertEqual(result, 200)

    def test_get_column_from_children(self):
        """测试从 children[0] 获取 column"""
        node = {
            "children": [
                {"line": 200, "column": 15},
            ]
        }
        result = _get_line_column(node, "column")
        self.assertEqual(result, 15)

    def test_node_priority_over_children(self):
        """测试节点自身字段优先于 children"""
        node = {
            "line": 100,
            "children": [
                {"line": 200},
            ]
        }
        result = _get_line_column(node, "line")
        self.assertEqual(result, 100)

    def test_no_line_column_returns_question_mark(self):
        """测试没有 line/column 时返回 '?'"""
        node = {"type": "function_call"}
        result = _get_line_column(node, "line")
        self.assertEqual(result, "?")

    def test_empty_children_returns_question_mark(self):
        """测试 children 为空时返回 '?'"""
        node = {"children": []}
        result = _get_line_column(node, "line")
        self.assertEqual(result, "?")

    def test_children_without_field_returns_question_mark(self):
        """测试 children 没有对应字段时返回 '?'"""
        node = {
            "children": [
                {"value": "test"},
            ]
        }
        result = _get_line_column(node, "line")
        self.assertEqual(result, "?")


class TestExtractArguments(unittest.TestCase):
    """测试 _extract_arguments 辅助函数"""

    def test_extract_from_arguments_field(self):
        """测试从 arguments 字段提取"""
        node = {
            "arguments": [
                {"data_type": "int", "value": 1},
                {"data_type": "char", "value": "a"},
            ]
        }
        result = _extract_arguments(node)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["data_type"], "int")
        self.assertEqual(result[1]["data_type"], "char")

    def test_extract_from_children(self):
        """测试从 children[1:] 提取"""
        node = {
            "children": [
                {"type": "identifier", "value": "func"},
                {"data_type": "int", "value": 1},
                {"data_type": "char", "value": "a"},
            ]
        }
        result = _extract_arguments(node)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["data_type"], "int")
        self.assertEqual(result[1]["data_type"], "char")

    def test_arguments_field_priority(self):
        """测试 arguments 字段优先于 children"""
        node = {
            "arguments": [
                {"data_type": "int", "value": 1},
            ],
            "children": [
                {"type": "identifier"},
                {"data_type": "char", "value": "a"},
                {"data_type": "char", "value": "b"},
            ]
        }
        result = _extract_arguments(node)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["data_type"], "int")

    def test_no_arguments_no_children(self):
        """测试没有 arguments 和 children 时返回空列表"""
        node = {"type": "function_call"}
        result = _extract_arguments(node)
        self.assertEqual(result, [])

    def test_empty_children(self):
        """测试 children 为空时返回空列表"""
        node = {"children": []}
        result = _extract_arguments(node)
        self.assertEqual(result, [])

    def test_single_child_no_arguments(self):
        """测试只有一个 child 时返回空列表"""
        node = {
            "children": [
                {"type": "identifier", "value": "func"},
            ]
        }
        result = _extract_arguments(node)
        self.assertEqual(result, [])

    def test_arguments_not_list_falls_back_to_children(self):
        """测试 arguments 不是列表时使用 children"""
        node = {
            "arguments": "not_a_list",
            "children": [
                {"type": "identifier"},
                {"data_type": "int", "value": 1},
            ]
        }
        result = _extract_arguments(node)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["data_type"], "int")


if __name__ == "__main__":
    unittest.main()

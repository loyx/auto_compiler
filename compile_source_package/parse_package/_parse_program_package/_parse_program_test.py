import unittest
from unittest.mock import patch

from ._parse_program_src import _parse_program

# 模块路径用于 patch
MODULE_PATH = "main_package.compile_source_package.parse_package._parse_program_package._parse_program_src"


class TestParseProgram(unittest.TestCase):
    """测试 _parse_program 函数：解析整个程序（零个或多个函数定义）"""

    def test_empty_program_no_functions(self):
        """测试空程序：没有函数定义"""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.src"
        }

        with patch(MODULE_PATH + "._is_at_end") as mock_is_at_end:
            mock_is_at_end.return_value = True

            result = _parse_program(parser_state)

            self.assertEqual(result["type"], "PROGRAM")
            self.assertEqual(result["children"], [])
            self.assertIsNone(result["value"])
            self.assertEqual(result["line"], 0)
            self.assertEqual(result["column"], 0)
            mock_is_at_end.assert_called_once_with(parser_state)

    def test_single_function_definition(self):
        """测试单个函数定义的程序"""
        parser_state = {
            "tokens": [{"type": "INT", "value": "int", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test.src"
        }

        mock_func_def = {
            "type": "FUNCTION_DEF",
            "children": [],
            "value": "test_func",
            "line": 1,
            "column": 1
        }

        with patch(MODULE_PATH + "._is_at_end") as mock_is_at_end, \
             patch(MODULE_PATH + "._parse_function_def") as mock_parse_func:
            mock_is_at_end.side_effect = [False, True]
            mock_parse_func.return_value = mock_func_def

            result = _parse_program(parser_state)

            self.assertEqual(result["type"], "PROGRAM")
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(result["children"][0], mock_func_def)
            self.assertIsNone(result["value"])

            mock_is_at_end.assert_called_with(parser_state)
            self.assertEqual(mock_is_at_end.call_count, 2)
            mock_parse_func.assert_called_once_with(parser_state)

    def test_multiple_function_definitions(self):
        """测试多个函数定义的程序"""
        parser_state = {
            "tokens": [
                {"type": "INT", "value": "int", "line": 1, "column": 1},
                {"type": "VOID", "value": "void", "line": 3, "column": 1},
                {"type": "FLOAT", "value": "float", "line": 5, "column": 1}
            ],
            "pos": 0,
            "filename": "test.src"
        }

        mock_func_def_1 = {
            "type": "FUNCTION_DEF",
            "children": [],
            "value": "func1",
            "line": 1,
            "column": 1
        }
        mock_func_def_2 = {
            "type": "FUNCTION_DEF",
            "children": [],
            "value": "func2",
            "line": 3,
            "column": 1
        }
        mock_func_def_3 = {
            "type": "FUNCTION_DEF",
            "children": [],
            "value": "func3",
            "line": 5,
            "column": 1
        }

        with patch(MODULE_PATH + "._is_at_end") as mock_is_at_end, \
             patch(MODULE_PATH + "._parse_function_def") as mock_parse_func:
            mock_is_at_end.side_effect = [False, False, False, True]
            mock_parse_func.side_effect = [mock_func_def_1, mock_func_def_2, mock_func_def_3]

            result = _parse_program(parser_state)

            self.assertEqual(result["type"], "PROGRAM")
            self.assertEqual(len(result["children"]), 3)
            self.assertEqual(result["children"], [mock_func_def_1, mock_func_def_2, mock_func_def_3])

            self.assertEqual(mock_is_at_end.call_count, 4)
            self.assertEqual(mock_parse_func.call_count, 3)

    def test_parser_state_passed_to_dependencies(self):
        """测试 parser_state 正确传递给依赖函数"""
        parser_state = {
            "tokens": [{"type": "INT", "value": "int", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "my_file.src"
        }

        mock_func_def = {
            "type": "FUNCTION_DEF",
            "children": [],
            "value": "test",
            "line": 1,
            "column": 1
        }

        with patch(MODULE_PATH + "._is_at_end") as mock_is_at_end, \
             patch(MODULE_PATH + "._parse_function_def") as mock_parse_func:
            mock_is_at_end.side_effect = [False, True]
            mock_parse_func.return_value = mock_func_def

            _parse_program(parser_state)

            for call_args in mock_is_at_end.call_args_list:
                self.assertIs(call_args[0][0], parser_state)

            for call_args in mock_parse_func.call_args_list:
                self.assertIs(call_args[0][0], parser_state)

    def test_function_def_exception_propagation(self):
        """测试 _parse_function_def 抛出异常时的传播行为"""
        parser_state = {
            "tokens": [{"type": "INT", "value": "int", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test.src"
        }

        with patch(MODULE_PATH + "._is_at_end") as mock_is_at_end, \
             patch(MODULE_PATH + "._parse_function_def") as mock_parse_func:
            mock_is_at_end.return_value = False
            mock_parse_func.side_effect = SyntaxError("Invalid function definition")

            with self.assertRaises(SyntaxError) as context:
                _parse_program(parser_state)

            self.assertEqual(str(context.exception), "Invalid function definition")

    def test_return_structure_consistency(self):
        """测试返回的 PROGRAM 节点结构一致性"""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.src"
        }

        with patch(MODULE_PATH + "._is_at_end") as mock_is_at_end:
            mock_is_at_end.return_value = True

            result = _parse_program(parser_state)

            self.assertIn("type", result)
            self.assertIn("children", result)
            self.assertIn("value", result)
            self.assertIn("line", result)
            self.assertIn("column", result)

            self.assertEqual(result["type"], "PROGRAM")
            self.assertIsInstance(result["children"], list)
            self.assertIsInstance(result["line"], int)
            self.assertIsInstance(result["column"], int)


if __name__ == "__main__":
    unittest.main()

import unittest
from unittest.mock import patch, call
from .generate_code_src import generate_code


class TestGenerateCode(unittest.TestCase):
    """单元测试：generate_code 函数"""

    def test_valid_program_with_single_function(self):
        """Happy path: 有效的 PROGRAM AST，包含单个函数定义。"""
        ast = {
            "type": "PROGRAM",
            "children": [
                {"type": "FUNCTION_DEF", "name": "main"}
            ]
        }

        with patch("main_package.compile_source_package.generate_code_package.generate_code_src.generate_function_code") as mock_gen_func:
            mock_gen_func.return_value = "    mov x0, #0\n    ret"

            result = generate_code(ast)

            self.assertEqual(result, "    mov x0, #0\n    ret")
            mock_gen_func.assert_called_once()
            call_args = mock_gen_func.call_args
            self.assertEqual(call_args[0][0], {"type": "FUNCTION_DEF", "name": "main"})
            self.assertIsInstance(call_args[0][1], dict)
            self.assertIn("if_else", call_args[0][1])

    def test_valid_program_with_multiple_functions(self):
        """Happy path: 有效的 PROGRAM AST，包含多个函数定义。"""
        ast = {
            "type": "PROGRAM",
            "children": [
                {"type": "FUNCTION_DEF", "name": "func1"},
                {"type": "FUNCTION_DEF", "name": "func2"},
                {"type": "FUNCTION_DEF", "name": "func3"}
            ]
        }

        with patch("main_package.compile_source_package.generate_code_package.generate_code_src.generate_function_code") as mock_gen_func:
            mock_gen_func.side_effect = [
                "func1_code",
                "func2_code",
                "func3_code"
            ]

            result = generate_code(ast)

            self.assertEqual(result, "func1_code\nfunc2_code\nfunc3_code")
            self.assertEqual(mock_gen_func.call_count, 3)
            expected_calls = [
                call({"type": "FUNCTION_DEF", "name": "func1"}, unittest.mock.ANY),
                call({"type": "FUNCTION_DEF", "name": "func2"}, unittest.mock.ANY),
                call({"type": "FUNCTION_DEF", "name": "func3"}, unittest.mock.ANY)
            ]
            mock_gen_func.assert_has_calls(expected_calls)

    def test_program_with_empty_children(self):
        """边界值：PROGRAM 节点存在但 children 为空列表。"""
        ast = {
            "type": "PROGRAM",
            "children": []
        }

        result = generate_code(ast)

        self.assertEqual(result, "")

    def test_program_without_children_key(self):
        """边界值：PROGRAM 节点存在但缺少 children 键。"""
        ast = {
            "type": "PROGRAM"
        }

        result = generate_code(ast)

        self.assertEqual(result, "")

    def test_non_program_root_raises_valueerror(self):
        """非法输入：根节点类型不是 PROGRAM，应抛出 ValueError。"""
        ast = {
            "type": "MODULE",
            "children": []
        }

        with self.assertRaises(ValueError) as context:
            generate_code(ast)

        self.assertEqual(str(context.exception), "Root node must be PROGRAM")

    def test_invalid_root_type_none(self):
        """非法输入：根节点 type 为 None。"""
        ast = {
            "type": None,
            "children": []
        }

        with self.assertRaises(ValueError):
            generate_code(ast)

    def test_invalid_root_type_missing(self):
        """非法输入：根节点缺少 type 字段。"""
        ast = {
            "children": []
        }

        with self.assertRaises(ValueError):
            generate_code(ast)

    def test_label_counter_initialization(self):
        """验证标签计数器正确初始化所有必需字段。"""
        ast = {
            "type": "PROGRAM",
            "children": [
                {"type": "FUNCTION_DEF", "name": "test"}
            ]
        }

        with patch("main_package.compile_source_package.generate_code_package.generate_code_src.generate_function_code") as mock_gen_func:
            mock_gen_func.return_value = "test_code"

            generate_code(ast)

            call_args = mock_gen_func.call_args
            label_counter = call_args[0][1]

            expected_keys = ["if_else", "if_end", "while_cond", "while_end",
                           "for_cond", "for_end", "for_update"]
            for key in expected_keys:
                self.assertIn(key, label_counter)
                self.assertEqual(label_counter[key], 0)

    def test_label_counter_passed_by_reference(self):
        """验证标签计数器作为引用传递给 generate_function_code。"""
        ast = {
            "type": "PROGRAM",
            "children": [
                {"type": "FUNCTION_DEF", "name": "func1"},
                {"type": "FUNCTION_DEF", "name": "func2"}
            ]
        }

        with patch("main_package.compile_source_package.generate_code_package.generate_code_src.generate_function_code") as mock_gen_func:
            mock_gen_func.side_effect = [
                "code1",
                "code2"
            ]

            generate_code(ast)

            calls = mock_gen_func.call_args_list
            self.assertEqual(len(calls), 2)
            label_counter_1 = calls[0][0][1]
            label_counter_2 = calls[1][0][1]
            self.assertIs(label_counter_1, label_counter_2)

    def test_output_format_newline_separated(self):
        """验证多个函数代码之间使用换行符分隔。"""
        ast = {
            "type": "PROGRAM",
            "children": [
                {"type": "FUNCTION_DEF", "name": "f1"},
                {"type": "FUNCTION_DEF", "name": "f2"}
            ]
        }

        with patch("main_package.compile_source_package.generate_code_package.generate_code_src.generate_function_code") as mock_gen_func:
            mock_gen_func.side_effect = ["line1", "line2", "line3"]

            result = generate_code(ast)

            self.assertEqual(result, "line1\nline2")
            self.assertNotIn("line3", result)

    def test_complex_ast_structure(self):
        """复杂场景：AST 包含完整的函数定义结构。"""
        ast = {
            "type": "PROGRAM",
            "children": [
                {
                    "type": "FUNCTION_DEF",
                    "name": "add",
                    "params": ["a", "b"],
                    "return_type": "int",
                    "body": [
                        {"type": "RETURN", "value": {"type": "BINARY_OP", "op": "+", "left": "a", "right": "b"}}
                    ]
                },
                {
                    "type": "FUNCTION_DEF",
                    "name": "main",
                    "params": [],
                    "return_type": "int",
                    "body": [
                        {"type": "CALL", "function": "add", "args": [1, 2]}
                    ]
                }
            ]
        }

        with patch("main_package.compile_source_package.generate_code_package.generate_code_src.generate_function_code") as mock_gen_func:
            mock_gen_func.side_effect = ["add_asm", "main_asm"]

            result = generate_code(ast)

            self.assertEqual(result, "add_asm\nmain_asm")
            self.assertEqual(mock_gen_func.call_count, 2)


if __name__ == "__main__":
    unittest.main()

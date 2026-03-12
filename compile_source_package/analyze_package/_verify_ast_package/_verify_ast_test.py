# test_verify_ast.py
"""单元测试：_verify_ast 函数"""
import unittest
from unittest.mock import patch

from ._verify_ast_src import _verify_ast


# 注意：由于 _verify_ast 内部延迟导入 _verify_node，
# 测试需要 patch _verify_ast_src 模块中的 _verify_node 引用
MOCK_PATH = "main_package.compile_source_package.analyze_package._verify_ast_package._verify_ast_src._verify_node"


class TestVerifyAst(unittest.TestCase):
    """测试 _verify_ast 函数"""

    def test_happy_path_calls_verify_node(self):
        """测试正常路径：验证 _verify_node 被正确调用"""
        ast = {"type": "program", "children": []}
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }
        context_stack = []
        filename = "test.c"

        with patch(MOCK_PATH) as mock_verify_node:
            _verify_ast(ast, symbol_table, context_stack, filename)
            mock_verify_node.assert_called_once_with(ast, symbol_table, context_stack, filename)

    def test_empty_ast(self):
        """测试边界值：空 AST"""
        ast = {}
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }
        context_stack = []
        filename = "test.c"

        with patch(MOCK_PATH) as mock_verify_node:
            _verify_ast(ast, symbol_table, context_stack, filename)
            mock_verify_node.assert_called_once_with(ast, symbol_table, context_stack, filename)

    def test_empty_symbol_table(self):
        """测试边界值：空符号表"""
        ast = {"type": "program", "children": []}
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }
        context_stack = []
        filename = "test.c"

        with patch(MOCK_PATH) as mock_verify_node:
            _verify_ast(ast, symbol_table, context_stack, filename)
            mock_verify_node.assert_called_once_with(ast, symbol_table, context_stack, filename)

    def test_empty_context_stack(self):
        """测试边界值：空上下文栈"""
        ast = {"type": "program", "children": []}
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }
        context_stack = []
        filename = "test.c"

        with patch(MOCK_PATH) as mock_verify_node:
            _verify_ast(ast, symbol_table, context_stack, filename)
            mock_verify_node.assert_called_once_with(ast, symbol_table, context_stack, filename)

    def test_complex_ast_structure(self):
        """测试复杂 AST 结构"""
        ast = {
            "type": "program",
            "children": [
                {
                    "type": "function_def",
                    "name": "main",
                    "children": [
                        {"type": "return_stmt", "value": 0}
                    ]
                }
            ]
        }
        symbol_table = {
            "variables": {},
            "functions": {
                "main": {"return_type": "int", "params": [], "line": 1, "column": 0}
            },
            "current_scope": 0,
            "scope_stack": [0]
        }
        context_stack = ["function:main"]
        filename = "main.c"

        with patch(MOCK_PATH) as mock_verify_node:
            _verify_ast(ast, symbol_table, context_stack, filename)
            mock_verify_node.assert_called_once_with(ast, symbol_table, context_stack, filename)

    def test_verify_node_raises_value_error_propagates(self):
        """测试异常传播：_verify_node 抛出 ValueError 时正确传播"""
        ast = {"type": "identifier", "value": "undefined_var", "line": 5, "column": 10}
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }
        context_stack = []
        filename = "test.c"

        with patch(MOCK_PATH) as mock_verify_node:
            mock_verify_node.side_effect = ValueError("Undefined variable 'undefined_var' at line 5")

            with self.assertRaises(ValueError) as context:
                _verify_ast(ast, symbol_table, context_stack, filename)

            self.assertEqual(str(context.exception), "Undefined variable 'undefined_var' at line 5")
            mock_verify_node.assert_called_once_with(ast, symbol_table, context_stack, filename)

    def test_verify_node_raises_with_line_info(self):
        """测试异常传播：包含行号信息的语义错误"""
        ast = {"type": "function_call", "name": "undefined_func", "line": 10, "column": 5}
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }
        context_stack = []
        filename = "test.c"

        with patch(MOCK_PATH) as mock_verify_node:
            error_msg = "Undefined function 'undefined_func' at line 10, column 5"
            mock_verify_node.side_effect = ValueError(error_msg)

            with self.assertRaises(ValueError) as context:
                _verify_ast(ast, symbol_table, context_stack, filename)

            self.assertEqual(str(context.exception), error_msg)

    def test_context_stack_mutation(self):
        """测试副作用：context_stack 可能被修改"""
        ast = {"type": "program", "children": []}
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }
        context_stack = []
        filename = "test.c"

        def modify_context_side_effect(node, sym_table, ctx_stack, fname):
            ctx_stack.append("modified")

        with patch(MOCK_PATH) as mock_verify_node:
            mock_verify_node.side_effect = modify_context_side_effect

            _verify_ast(ast, symbol_table, context_stack, filename)

            self.assertEqual(context_stack, ["modified"])
            mock_verify_node.assert_called_once()

    def test_symbol_table_with_variables(self):
        """测试带有变量定义的符号表"""
        ast = {"type": "program", "children": []}
        symbol_table = {
            "variables": {
                "x": {"data_type": "int", "is_declared": True, "line": 1, "column": 0, "scope_level": 0},
                "y": {"data_type": "char", "is_declared": True, "line": 2, "column": 0, "scope_level": 0}
            },
            "functions": {},
            "current_scope": 0,
            "scope_stack": [0]
        }
        context_stack = []
        filename = "test.c"

        with patch(MOCK_PATH) as mock_verify_node:
            _verify_ast(ast, symbol_table, context_stack, filename)
            mock_verify_node.assert_called_once_with(ast, symbol_table, context_stack, filename)

    def test_symbol_table_with_functions(self):
        """测试带有函数定义的符号表"""
        ast = {"type": "program", "children": []}
        symbol_table = {
            "variables": {},
            "functions": {
                "foo": {"return_type": "int", "params": ["int", "char"], "line": 1, "column": 0},
                "bar": {"return_type": "void", "params": [], "line": 5, "column": 0}
            },
            "current_scope": 0,
            "scope_stack": [0]
        }
        context_stack = []
        filename = "test.c"

        with patch(MOCK_PATH) as mock_verify_node:
            _verify_ast(ast, symbol_table, context_stack, filename)
            mock_verify_node.assert_called_once_with(ast, symbol_table, context_stack, filename)

    def test_multiple_scopes_in_symbol_table(self):
        """测试多作用域符号表"""
        ast = {"type": "program", "children": []}
        symbol_table = {
            "variables": {
                "global_var": {"data_type": "int", "is_declared": True, "line": 1, "column": 0, "scope_level": 0}
            },
            "functions": {},
            "current_scope": 1,
            "scope_stack": [0, 1]
        }
        context_stack = ["function:main"]
        filename = "test.c"

        with patch(MOCK_PATH) as mock_verify_node:
            _verify_ast(ast, symbol_table, context_stack, filename)
            mock_verify_node.assert_called_once_with(ast, symbol_table, context_stack, filename)

    def test_nested_context_stack(self):
        """测试嵌套上下文栈（循环嵌套）"""
        ast = {"type": "program", "children": []}
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }
        context_stack = ["loop:for", "loop:while", "function:main"]
        filename = "test.c"

        with patch(MOCK_PATH) as mock_verify_node:
            _verify_ast(ast, symbol_table, context_stack, filename)
            mock_verify_node.assert_called_once_with(ast, symbol_table, context_stack, filename)

    def test_different_filename_paths(self):
        """测试不同文件名路径"""
        ast = {"type": "program", "children": []}
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }
        context_stack = []

        test_filenames = [
            "test.c",
            "/absolute/path/to/file.c",
            "./relative/path/file.c",
            "main_package/source.c"
        ]

        for filename in test_filenames:
            with patch(MOCK_PATH) as mock_verify_node:
                _verify_ast(ast, symbol_table, context_stack, filename)
                mock_verify_node.assert_called_once_with(ast, symbol_table, context_stack, filename)
                mock_verify_node.reset_mock()

    def test_ast_with_data_type_annotation(self):
        """测试带有类型标注的 AST 节点"""
        ast = {
            "type": "identifier",
            "value": "x",
            "data_type": "int",
            "line": 1,
            "column": 0
        }
        symbol_table = {
            "variables": {
                "x": {"data_type": "int", "is_declared": True, "line": 1, "column": 0, "scope_level": 0}
            },
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }
        context_stack = []
        filename = "test.c"

        with patch(MOCK_PATH) as mock_verify_node:
            _verify_ast(ast, symbol_table, context_stack, filename)
            mock_verify_node.assert_called_once_with(ast, symbol_table, context_stack, filename)

    def test_verify_node_called_with_correct_parameters(self):
        """测试参数传递的正确性：所有参数原样传递"""
        ast = {"type": "test", "id": 123}
        symbol_table = {"variables": {"a": 1}, "functions": {}, "current_scope": 0, "scope_stack": []}
        context_stack = ["ctx1", "ctx2"]
        filename = "specific_file.c"

        with patch(MOCK_PATH) as mock_verify_node:
            _verify_ast(ast, symbol_table, context_stack, filename)

            call_args = mock_verify_node.call_args
            self.assertEqual(call_args[0][0], ast)
            self.assertEqual(call_args[0][1], symbol_table)
            self.assertEqual(call_args[0][2], context_stack)
            self.assertEqual(call_args[0][3], filename)
            self.assertEqual(len(call_args[0]), 4)

    def test_return_value_is_none(self):
        """测试返回值：函数应返回 None"""
        ast = {"type": "program", "children": []}
        symbol_table = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }
        context_stack = []
        filename = "test.c"

        with patch(MOCK_PATH) as mock_verify_node:
            result = _verify_ast(ast, symbol_table, context_stack, filename)
            self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
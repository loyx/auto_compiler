"""
单元测试：parse 函数
语法分析器入口：将 token 流构建为抽象语法树 (AST)
"""
import unittest
import sys
from unittest.mock import MagicMock, patch

# Pre-register mock modules to avoid import errors from deep dependency chains
# This allows patching to work even when submodules have unimplemented dependencies
def _setup_mock_modules():
    """Setup mock modules for dependencies that may not exist yet"""
    mock_modules = [
        "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package",
        "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_function_def_src",
        "main_package.compile_source_package.parse_package._parse_program_package._is_at_end_package",
        "main_package.compile_source_package.parse_package._parse_program_package._is_at_end_package._is_at_end_src",
    ]
    for mod_name in mock_modules:
        if mod_name not in sys.modules:
            sys.modules[mod_name] = MagicMock()

_setup_mock_modules()

from .parse_src import parse


class TestParse(unittest.TestCase):
    """测试 parse 函数的各种场景"""

    def test_parse_happy_path_single_function(self):
        """测试 happy path：解析单个函数定义的 token 流"""
        tokens = [
            {"type": "DEF", "value": "def", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "main", "line": 1, "column": 5},
            {"type": "LPAREN", "value": "(", "line": 1, "column": 9},
            {"type": "RPAREN", "value": ")", "line": 1, "column": 10},
            {"type": "LBRACE", "value": "{", "line": 1, "column": 12},
            {"type": "RBRACE", "value": "}", "line": 1, "column": 13},
        ]
        filename = "test.src"
        
        expected_ast = {
            "type": "PROGRAM",
            "children": [
                {
                    "type": "FUNCTION_DEF",
                    "value": "main",
                    "children": [],
                    "line": 1,
                    "column": 1
                }
            ],
            "line": 1,
            "column": 1
        }
        
        with patch("main_package.compile_source_package.parse_package._init_parser_state_package._init_parser_state_src._init_parser_state") as mock_init, \
             patch("main_package.compile_source_package.parse_package._parse_program_package._parse_program_src._parse_program") as mock_parse:
            
            mock_state = {"tokens": tokens, "pos": 0, "filename": filename}
            mock_init.return_value = mock_state
            mock_parse.return_value = expected_ast
            
            result = parse(tokens, filename)
            
            mock_init.assert_called_once_with(tokens, filename)
            mock_parse.assert_called_once_with(mock_state)
            self.assertEqual(result, expected_ast)

    def test_parse_empty_token_list(self):
        """测试边界情况：空 token 列表"""
        tokens = []
        filename = "empty.src"
        
        expected_ast = {
            "type": "PROGRAM",
            "children": [],
            "line": 0,
            "column": 0
        }
        
        with patch("main_package.compile_source_package.parse_package._init_parser_state_package._init_parser_state_src._init_parser_state") as mock_init, \
             patch("main_package.compile_source_package.parse_package._parse_program_package._parse_program_src._parse_program") as mock_parse:
            
            mock_state = {"tokens": tokens, "pos": 0, "filename": filename}
            mock_init.return_value = mock_state
            mock_parse.return_value = expected_ast
            
            result = parse(tokens, filename)
            
            mock_init.assert_called_once_with(tokens, filename)
            mock_parse.assert_called_once_with(mock_state)
            self.assertEqual(result, expected_ast)

    def test_parse_multiple_functions(self):
        """测试解析多个函数定义"""
        tokens = [
            {"type": "DEF", "value": "def", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "func1", "line": 1, "column": 5},
            {"type": "LPAREN", "value": "(", "line": 1, "column": 10},
            {"type": "RPAREN", "value": ")", "line": 1, "column": 11},
            {"type": "LBRACE", "value": "{", "line": 1, "column": 13},
            {"type": "RBRACE", "value": "}", "line": 1, "column": 14},
            {"type": "DEF", "value": "def", "line": 2, "column": 1},
            {"type": "IDENTIFIER", "value": "func2", "line": 2, "column": 5},
            {"type": "LPAREN", "value": "(", "line": 2, "column": 10},
            {"type": "RPAREN", "value": ")", "line": 2, "column": 11},
            {"type": "LBRACE", "value": "{", "line": 2, "column": 13},
            {"type": "RBRACE", "value": "}", "line": 2, "column": 14},
        ]
        filename = "multi_func.src"
        
        expected_ast = {
            "type": "PROGRAM",
            "children": [
                {"type": "FUNCTION_DEF", "value": "func1", "children": [], "line": 1, "column": 1},
                {"type": "FUNCTION_DEF", "value": "func2", "children": [], "line": 2, "column": 1}
            ],
            "line": 1,
            "column": 1
        }
        
        with patch("main_package.compile_source_package.parse_package._init_parser_state_package._init_parser_state_src._init_parser_state") as mock_init, \
             patch("main_package.compile_source_package.parse_package._parse_program_package._parse_program_src._parse_program") as mock_parse:
            
            mock_state = {"tokens": tokens, "pos": 0, "filename": filename}
            mock_init.return_value = mock_state
            mock_parse.return_value = expected_ast
            
            result = parse(tokens, filename)
            
            self.assertEqual(result, expected_ast)

    def test_parse_with_variable_declaration(self):
        """测试包含变量声明的解析"""
        tokens = [
            {"type": "VAR", "value": "var", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 5},
            {"type": "ASSIGN", "value": "=", "line": 1, "column": 7},
            {"type": "NUMBER", "value": "42", "line": 1, "column": 9},
            {"type": "SEMICOLON", "value": ";", "line": 1, "column": 11},
        ]
        filename = "var_decl.src"
        
        expected_ast = {
            "type": "PROGRAM",
            "children": [
                {"type": "VAR_DECL", "value": "x", "children": [], "line": 1, "column": 1}
            ],
            "line": 1,
            "column": 1
        }
        
        with patch("main_package.compile_source_package.parse_package._init_parser_state_package._init_parser_state_src._init_parser_state") as mock_init, \
             patch("main_package.compile_source_package.parse_package._parse_program_package._parse_program_src._parse_program") as mock_parse:
            
            mock_state = {"tokens": tokens, "pos": 0, "filename": filename}
            mock_init.return_value = mock_state
            mock_parse.return_value = expected_ast
            
            result = parse(tokens, filename)
            
            self.assertEqual(result, expected_ast)

    def test_parse_with_control_structures(self):
        """测试包含控制结构（if/while/for）的解析"""
        tokens = [
            {"type": "IF", "value": "if", "line": 1, "column": 1},
            {"type": "LPAREN", "value": "(", "line": 1, "column": 4},
            {"type": "IDENTIFIER", "value": "cond", "line": 1, "column": 5},
            {"type": "RPAREN", "value": ")", "line": 1, "column": 9},
            {"type": "LBRACE", "value": "{", "line": 1, "column": 11},
            {"type": "RBRACE", "value": "}", "line": 1, "column": 12},
        ]
        filename = "control.src"
        
        expected_ast = {
            "type": "PROGRAM",
            "children": [
                {"type": "IF_STMT", "value": None, "children": [], "line": 1, "column": 1}
            ],
            "line": 1,
            "column": 1
        }
        
        with patch("main_package.compile_source_package.parse_package._init_parser_state_package._init_parser_state_src._init_parser_state") as mock_init, \
             patch("main_package.compile_source_package.parse_package._parse_program_package._parse_program_src._parse_program") as mock_parse:
            
            mock_state = {"tokens": tokens, "pos": 0, "filename": filename}
            mock_init.return_value = mock_state
            mock_parse.return_value = expected_ast
            
            result = parse(tokens, filename)
            
            self.assertEqual(result, expected_ast)

    def test_parse_with_return_statement(self):
        """测试包含 return 语句的解析"""
        tokens = [
            {"type": "RETURN", "value": "return", "line": 1, "column": 1},
            {"type": "NUMBER", "value": "0", "line": 1, "column": 8},
            {"type": "SEMICOLON", "value": ";", "line": 1, "column": 9},
        ]
        filename = "return.src"
        
        expected_ast = {
            "type": "PROGRAM",
            "children": [
                {"type": "RETURN_STMT", "value": None, "children": [], "line": 1, "column": 1}
            ],
            "line": 1,
            "column": 1
        }
        
        with patch("main_package.compile_source_package.parse_package._init_parser_state_package._init_parser_state_src._init_parser_state") as mock_init, \
             patch("main_package.compile_source_package.parse_package._parse_program_package._parse_program_src._parse_program") as mock_parse:
            
            mock_state = {"tokens": tokens, "pos": 0, "filename": filename}
            mock_init.return_value = mock_state
            mock_parse.return_value = expected_ast
            
            result = parse(tokens, filename)
            
            self.assertEqual(result, expected_ast)

    def test_parse_with_break_continue(self):
        """测试包含 break/continue 语句的解析"""
        tokens = [
            {"type": "BREAK", "value": "break", "line": 1, "column": 1},
            {"type": "SEMICOLON", "value": ";", "line": 1, "column": 6},
            {"type": "CONTINUE", "value": "continue", "line": 2, "column": 1},
            {"type": "SEMICOLON", "value": ";", "line": 2, "column": 9},
        ]
        filename = "loop_control.src"
        
        expected_ast = {
            "type": "PROGRAM",
            "children": [
                {"type": "BREAK_STMT", "value": None, "children": [], "line": 1, "column": 1},
                {"type": "CONTINUE_STMT", "value": None, "children": [], "line": 2, "column": 1}
            ],
            "line": 1,
            "column": 1
        }
        
        with patch("main_package.compile_source_package.parse_package._init_parser_state_package._init_parser_state_src._init_parser_state") as mock_init, \
             patch("main_package.compile_source_package.parse_package._parse_program_package._parse_program_src._parse_program") as mock_parse:
            
            mock_state = {"tokens": tokens, "pos": 0, "filename": filename}
            mock_init.return_value = mock_state
            mock_parse.return_value = expected_ast
            
            result = parse(tokens, filename)
            
            self.assertEqual(result, expected_ast)

    def test_parse_syntax_error_propagation(self):
        """测试语法错误异常传播"""
        tokens = [
            {"type": "DEF", "value": "def", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "incomplete", "line": 1, "column": 5},
            # 缺少 LPAREN，应该触发语法错误
        ]
        filename = "error.src"
        
        with patch("main_package.compile_source_package.parse_package._init_parser_state_package._init_parser_state_src._init_parser_state") as mock_init, \
             patch("main_package.compile_source_package.parse_package._parse_program_package._parse_program_src._parse_program") as mock_parse:
            
            mock_state = {"tokens": tokens, "pos": 0, "filename": filename}
            mock_init.return_value = mock_state
            
            # 模拟 _parse_program 抛出语法错误
            mock_parse.side_effect = SyntaxError("Expected '(' after function name at line 1, column 5")
            
            with self.assertRaises(SyntaxError) as context:
                parse(tokens, filename)
            
            self.assertIn("line 1", str(context.exception))
            mock_init.assert_called_once_with(tokens, filename)
            mock_parse.assert_called_once_with(mock_state)

    def test_parse_init_parser_state_called_first(self):
        """测试 _init_parser_state 在 _parse_program 之前被调用"""
        tokens = [{"type": "IDENTIFIER", "value": "test", "line": 1, "column": 1}]
        filename = "order.src"
        
        call_order = []
        
        def mock_init_side_effect(*args, **kwargs):
            call_order.append("init")
            return {"tokens": tokens, "pos": 0, "filename": filename}
        
        def mock_parse_side_effect(*args, **kwargs):
            call_order.append("parse")
            return {"type": "PROGRAM", "children": [], "line": 1, "column": 1}
        
        with patch("main_package.compile_source_package.parse_package._init_parser_state_package._init_parser_state_src._init_parser_state") as mock_init, \
             patch("main_package.compile_source_package.parse_package._parse_program_package._parse_program_src._parse_program") as mock_parse:
            
            mock_init.side_effect = mock_init_side_effect
            mock_parse.side_effect = mock_parse_side_effect
            
            parse(tokens, filename)
            
            self.assertEqual(call_order, ["init", "parse"])

    def test_parse_return_value_is_ast_from_parse_program(self):
        """测试 parse 返回值直接来自 _parse_program 的结果"""
        tokens = [{"type": "NUMBER", "value": "123", "line": 1, "column": 1}]
        filename = "return_test.src"
        
        unique_ast_id = object()  # 使用唯一对象确保返回的是同一个引用
        
        with patch("main_package.compile_source_package.parse_package._init_parser_state_package._init_parser_state_src._init_parser_state") as mock_init, \
             patch("main_package.compile_source_package.parse_package._parse_program_package._parse_program_src._parse_program") as mock_parse:
            
            mock_init.return_value = {"tokens": tokens, "pos": 0, "filename": filename}
            mock_parse.return_value = unique_ast_id
            
            result = parse(tokens, filename)
            
            self.assertIs(result, unique_ast_id)

    def test_parse_complex_expression(self):
        """测试复杂表达式解析"""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            {"type": "ASSIGN", "value": "=", "line": 1, "column": 3},
            {"type": "NUMBER", "value": "10", "line": 1, "column": 5},
            {"type": "PLUS", "value": "+", "line": 1, "column": 8},
            {"type": "NUMBER", "value": "20", "line": 1, "column": 10},
            {"type": "SEMICOLON", "value": ";", "line": 1, "column": 12},
        ]
        filename = "expr.src"
        
        expected_ast = {
            "type": "PROGRAM",
            "children": [
                {
                    "type": "EXPR_STMT",
                    "children": [
                        {
                            "type": "BINARY_OP",
                            "value": "+",
                            "children": [
                                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                                {"type": "NUMBER", "value": "10", "line": 1, "column": 5},
                                {"type": "NUMBER", "value": "20", "line": 1, "column": 10}
                            ],
                            "line": 1,
                            "column": 1
                        }
                    ],
                    "line": 1,
                    "column": 1
                }
            ],
            "line": 1,
            "column": 1
        }
        
        with patch("main_package.compile_source_package.parse_package._init_parser_state_package._init_parser_state_src._init_parser_state") as mock_init, \
             patch("main_package.compile_source_package.parse_package._parse_program_package._parse_program_src._parse_program") as mock_parse:
            
            mock_state = {"tokens": tokens, "pos": 0, "filename": filename}
            mock_init.return_value = mock_state
            mock_parse.return_value = expected_ast
            
            result = parse(tokens, filename)
            
            self.assertEqual(result, expected_ast)

    def test_parse_filename_preserved_in_state(self):
        """测试文件名正确传递给解析器状态"""
        tokens = [{"type": "DEF", "value": "def", "line": 1, "column": 1}]
        filename = "my_custom_file.src"
        
        captured_state = {}
        
        def capture_state(tokens_arg, filename_arg):
            captured_state["tokens"] = tokens_arg
            captured_state["filename"] = filename_arg
            return {"tokens": tokens_arg, "pos": 0, "filename": filename_arg}
        
        with patch("main_package.compile_source_package.parse_package._init_parser_state_package._init_parser_state_src._init_parser_state") as mock_init, \
             patch("main_package.compile_source_package.parse_package._parse_program_package._parse_program_src._parse_program") as mock_parse:
            
            mock_init.side_effect = capture_state
            mock_parse.return_value = {"type": "PROGRAM", "children": [], "line": 1, "column": 1}
            
            parse(tokens, filename)
            
            self.assertEqual(captured_state["filename"], filename)
            self.assertEqual(captured_state["tokens"], tokens)


if __name__ == "__main__":
    unittest.main()

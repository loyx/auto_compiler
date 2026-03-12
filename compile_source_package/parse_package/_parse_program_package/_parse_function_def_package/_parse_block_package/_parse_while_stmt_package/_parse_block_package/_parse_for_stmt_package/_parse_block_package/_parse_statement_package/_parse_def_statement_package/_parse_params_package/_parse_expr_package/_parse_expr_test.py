"""
单元测试：_parse_expr 函数
测试表达式解析功能（字面量、标识符、简单二元运算）
"""

import unittest
from unittest.mock import patch
from typing import Any, Dict

# 相对导入被测试模块
from ._parse_expr_src import _parse_expr


class TestParseExpr(unittest.TestCase):
    """_parse_expr 函数测试用例"""

    def _create_parser_state(self, tokens: list, pos: int = 0, filename: str = "test.py") -> Dict[str, Any]:
        """辅助函数：创建 parser_state"""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename
        }

    def _create_token(self, token_type: str, value: Any, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """辅助函数：创建 token"""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def test_parse_simple_literal(self):
        """测试：解析简单字面量（无二元运算）"""
        tokens = [self._create_token("NUMBER", "42")]
        parser_state = self._create_parser_state(tokens)

        # Mock _parse_atom 返回字面量 AST
        mock_atom = {
            "type": "NUMBER",
            "value": "42",
            "line": 1,
            "column": 1
        }

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_def_statement_package._parse_params_package._parse_expr_package._parse_atom_package._parse_atom_src._parse_atom") as mock_parse_atom:
            mock_parse_atom.return_value = mock_atom
            mock_parse_atom.side_effect = lambda state: state.update({"pos": 1}) or mock_atom

            result = _parse_expr(parser_state)

            # 验证返回的是原子 AST（非二元运算）
            self.assertEqual(result["type"], "NUMBER")
            self.assertEqual(result["value"], "42")
            # 验证 pos 已更新
            self.assertEqual(parser_state["pos"], 1)

    def test_parse_simple_identifier(self):
        """测试：解析简单标识符（无二元运算）"""
        tokens = [self._create_token("IDENT", "x")]
        parser_state = self._create_parser_state(tokens)

        mock_atom = {
            "type": "IDENT",
            "value": "x",
            "line": 1,
            "column": 1
        }

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_def_statement_package._parse_params_package._parse_expr_package._parse_atom_package._parse_atom_src._parse_atom") as mock_parse_atom:
            mock_parse_atom.return_value = mock_atom
            mock_parse_atom.side_effect = lambda state: state.update({"pos": 1}) or mock_atom

            result = _parse_expr(parser_state)

            self.assertEqual(result["type"], "IDENT")
            self.assertEqual(result["value"], "x")
            self.assertEqual(parser_state["pos"], 1)

    def test_parse_binary_operation(self):
        """测试：解析二元运算表达式"""
        tokens = [
            self._create_token("IDENT", "a", column=1),
            self._create_token("OP", "+", column=3),
            self._create_token("NUMBER", "5", column=5)
        ]
        parser_state = self._create_parser_state(tokens)

        left_atom = {
            "type": "IDENT",
            "value": "a",
            "line": 1,
            "column": 1
        }
        right_atom = {
            "type": "NUMBER",
            "value": "5",
            "line": 1,
            "column": 5
        }

        call_count = [0]

        def mock_atom_func(state):
            call_count[0] += 1
            if call_count[0] == 1:
                state["pos"] = 1
                return left_atom
            else:
                state["pos"] = 3
                return right_atom

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_def_statement_package._parse_params_package._parse_expr_package._parse_atom_package._parse_atom_src._parse_atom") as mock_parse_atom:
            mock_parse_atom.side_effect = mock_atom_func

            result = _parse_expr(parser_state)

            # 验证返回的是二元运算 AST
            self.assertEqual(result["type"], "BINOP")
            self.assertEqual(result["op"], "+")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            self.assertEqual(len(result["children"]), 2)
            self.assertEqual(result["children"][0]["type"], "IDENT")
            self.assertEqual(result["children"][1]["type"], "NUMBER")
            # 验证 pos 已更新到表达式后
            self.assertEqual(parser_state["pos"], 3)

    def test_parse_binary_operation_with_different_ops(self):
        """测试：解析不同运算符的二元运算"""
        for op in ["-", "*", "/", "==", "<", ">"]:
            tokens = [
                self._create_token("NUMBER", "10", column=1),
                self._create_token("OP", op, column=3),
                self._create_token("NUMBER", "5", column=5)
            ]
            parser_state = self._create_parser_state(tokens)

            left_atom = {"type": "NUMBER", "value": "10", "line": 1, "column": 1}
            right_atom = {"type": "NUMBER", "value": "5", "line": 1, "column": 5}

            call_count = [0]

            def mock_atom_func(state):
                call_count[0] += 1
                if call_count[0] == 1:
                    state["pos"] = 1
                    return left_atom
                else:
                    state["pos"] = 3
                    return right_atom

            with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_def_statement_package._parse_params_package._parse_expr_package._parse_atom_package._parse_atom_src._parse_atom") as mock_parse_atom:
                mock_parse_atom.side_effect = mock_atom_func
                call_count[0] = 0

                result = _parse_expr(parser_state)

                self.assertEqual(result["type"], "BINOP")
                self.assertEqual(result["op"], op)

    def test_parse_empty_tokens_raises_error(self):
        """测试：空 tokens 列表应抛出 SyntaxError"""
        parser_state = self._create_parser_state([])

        with self.assertRaises(SyntaxError) as context:
            _parse_expr(parser_state)

        self.assertIn("Incomplete expression", str(context.exception))

    def test_parse_pos_at_end_raises_error(self):
        """测试：pos 已在 tokens 末尾应抛出 SyntaxError"""
        tokens = [self._create_token("NUMBER", "42")]
        parser_state = self._create_parser_state(tokens, pos=1)

        with self.assertRaises(SyntaxError) as context:
            _parse_expr(parser_state)

        self.assertIn("Incomplete expression", str(context.exception))

    def test_parse_atom_only_no_operator(self):
        """测试：只有原子表达式，后面没有运算符"""
        tokens = [self._create_token("STRING", '"hello"')]
        parser_state = self._create_parser_state(tokens)

        mock_atom = {
            "type": "STRING",
            "value": '"hello"',
            "line": 1,
            "column": 1
        }

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_def_statement_package._parse_params_package._parse_expr_package._parse_atom_package._parse_atom_src._parse_atom") as mock_parse_atom:
            mock_parse_atom.return_value = mock_atom
            mock_parse_atom.side_effect = lambda state: state.update({"pos": 1}) or mock_atom

            result = _parse_expr(parser_state)

            # 应直接返回原子 AST，不构建 BINOP
            self.assertEqual(result["type"], "STRING")
            self.assertNotEqual(result["type"], "BINOP")
            self.assertEqual(parser_state["pos"], 1)

    def test_parse_preserves_line_column_info(self):
        """测试：保留行号和列号信息"""
        tokens = [
            self._create_token("IDENT", "x", line=5, column=10),
            self._create_token("OP", "+", line=5, column=12),
            self._create_token("NUMBER", "1", line=5, column=14)
        ]
        parser_state = self._create_parser_state(tokens)

        left_atom = {"type": "IDENT", "value": "x", "line": 5, "column": 10}
        right_atom = {"type": "NUMBER", "value": "1", "line": 5, "column": 14}

        call_count = [0]

        def mock_atom_func(state):
            call_count[0] += 1
            if call_count[0] == 1:
                state["pos"] = 1
                return left_atom
            else:
                state["pos"] = 3
                return right_atom

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_def_statement_package._parse_params_package._parse_expr_package._parse_atom_package._parse_atom_src._parse_atom") as mock_parse_atom:
            mock_parse_atom.side_effect = mock_atom_func

            result = _parse_expr(parser_state)

            self.assertEqual(result["line"], 5)
            self.assertEqual(result["column"], 10)

    def test_parse_multiple_expressions_stops_after_one(self):
        """测试：多个表达式时只解析第一个（用于参数默认值的单表达式场景）"""
        tokens = [
            self._create_token("NUMBER", "1", column=1),
            self._create_token("OP", "+", column=3),
            self._create_token("NUMBER", "2", column=5),
            self._create_token("OP", "*", column=7),
            self._create_token("NUMBER", "3", column=9)
        ]
        parser_state = self._create_parser_state(tokens)

        left_atom = {"type": "NUMBER", "value": "1", "line": 1, "column": 1}
        right_atom = {"type": "NUMBER", "value": "2", "line": 1, "column": 5}

        call_count = [0]

        def mock_atom_func(state):
            call_count[0] += 1
            if call_count[0] == 1:
                state["pos"] = 1
                return left_atom
            else:
                state["pos"] = 3
                return right_atom

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_def_statement_package._parse_params_package._parse_expr_package._parse_atom_package._parse_atom_src._parse_atom") as mock_parse_atom:
            mock_parse_atom.side_effect = mock_atom_func

            result = _parse_expr(parser_state)

            # 只解析了一个二元运算，pos 停在 3（第三个 token 前）
            self.assertEqual(result["type"], "BINOP")
            self.assertEqual(result["op"], "+")
            self.assertEqual(parser_state["pos"], 3)


if __name__ == "__main__":
    unittest.main()

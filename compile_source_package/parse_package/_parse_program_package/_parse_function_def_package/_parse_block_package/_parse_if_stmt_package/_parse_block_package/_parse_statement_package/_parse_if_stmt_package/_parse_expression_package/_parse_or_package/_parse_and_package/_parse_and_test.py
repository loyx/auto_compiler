# -*- coding: utf-8 -*-
"""单元测试文件：_parse_and 函数测试"""

import unittest
from unittest.mock import patch

from ._parse_and_src import _parse_and


class TestParseAnd(unittest.TestCase):
    """测试 _parse_and 函数解析 AND 表达式（&& 运算符）"""

    def test_single_comparison_no_and(self):
        """测试单个比较表达式，没有 && 运算符"""
        mock_comparison = {
            "type": "BINARY_OP",
            "operator": ">",
            "left": {"type": "IDENTIFIER", "name": "x"},
            "right": {"type": "LITERAL", "value": 5},
            "line": 1,
            "column": 1
        }
        
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "GT", "value": ">", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "5", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_expression_package._parse_or_package._parse_and_package._parse_comparison_package._parse_comparison_src._parse_comparison") as mock_parse_comparison:
            mock_parse_comparison.return_value = mock_comparison
            
            result = _parse_and(parser_state)
            
            self.assertEqual(result, mock_comparison)
            mock_parse_comparison.assert_called_once()

    def test_multiple_and_operators_left_associative(self):
        """测试多个 && 运算符，验证左结合性"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "AND", "value": "&&", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 6},
                {"type": "AND", "value": "&&", "line": 1, "column": 8},
                {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 11}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        call_count = [0]
        comparison_nodes = [
            {"type": "IDENTIFIER", "name": "a", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "name": "b", "line": 1, "column": 6},
            {"type": "IDENTIFIER", "name": "c", "line": 1, "column": 11}
        ]
        
        def side_effect(state):
            node = comparison_nodes[call_count[0]]
            call_count[0] += 1
            return node
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_expression_package._parse_or_package._parse_and_package._parse_comparison_package._parse_comparison_src._parse_comparison") as mock_parse_comparison:
            mock_parse_comparison.side_effect = side_effect
            
            result = _parse_and(parser_state)
            
            # 验证左结合性：(a && b) && c
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["operator"], "&&")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 8)
            
            # 左边应该是 (a && b)
            left = result["left"]
            self.assertEqual(left["type"], "BINARY_OP")
            self.assertEqual(left["operator"], "&&")
            self.assertEqual(left["line"], 1)
            self.assertEqual(left["column"], 3)
            self.assertEqual(left["left"]["name"], "a")
            self.assertEqual(left["right"]["name"], "b")
            
            # 右边应该是 c
            self.assertEqual(result["right"]["name"], "c")
            
            # _parse_comparison 应该被调用 3 次
            self.assertEqual(mock_parse_comparison.call_count, 3)

    def test_and_operator_with_complex_comparisons(self):
        """测试 && 运算符连接复杂比较表达式"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 2, "column": 5},
                {"type": "GT", "value": ">", "line": 2, "column": 7},
                {"type": "NUMBER", "value": "0", "line": 2, "column": 9},
                {"type": "AND", "value": "&&", "line": 2, "column": 11},
                {"type": "IDENTIFIER", "value": "x", "line": 2, "column": 14},
                {"type": "LT", "value": "<", "line": 2, "column": 16},
                {"type": "NUMBER", "value": "10", "line": 2, "column": 18}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        call_count = [0]
        comparison_nodes = [
            {
                "type": "BINARY_OP",
                "operator": ">",
                "left": {"type": "IDENTIFIER", "name": "x"},
                "right": {"type": "LITERAL", "value": 0},
                "line": 2,
                "column": 7
            },
            {
                "type": "BINARY_OP",
                "operator": "<",
                "left": {"type": "IDENTIFIER", "name": "x"},
                "right": {"type": "LITERAL", "value": 10},
                "line": 2,
                "column": 16
            }
        ]
        
        def side_effect(state):
            node = comparison_nodes[call_count[0]]
            call_count[0] += 1
            return node
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_expression_package._parse_or_package._parse_and_package._parse_comparison_package._parse_comparison_src._parse_comparison") as mock_parse_comparison:
            mock_parse_comparison.side_effect = side_effect
            
            result = _parse_and(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["operator"], "&&")
            self.assertEqual(result["left"]["operator"], ">")
            self.assertEqual(result["right"]["operator"], "<")
            self.assertEqual(parser_state["pos"], 7)

    def test_empty_tokens(self):
        """测试空 tokens 列表"""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.c"
        }
        
        mock_comparison = {"type": "LITERAL", "value": None, "line": 0, "column": 0}
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_expression_package._parse_or_package._parse_and_package._parse_comparison_package._parse_comparison_src._parse_comparison") as mock_parse_comparison:
            mock_parse_comparison.return_value = mock_comparison
            
            result = _parse_and(parser_state)
            
            self.assertEqual(result, mock_comparison)
            self.assertEqual(parser_state["pos"], 0)

    def test_pos_at_end_of_tokens(self):
        """测试 pos 已在 tokens 末尾"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 1,
            "filename": "test.c"
        }
        
        mock_comparison = {"type": "IDENTIFIER", "name": "x", "line": 1, "column": 1}
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_expression_package._parse_or_package._parse_and_package._parse_comparison_package._parse_comparison_src._parse_comparison") as mock_parse_comparison:
            mock_parse_comparison.return_value = mock_comparison
            
            result = _parse_and(parser_state)
            
            self.assertEqual(result, mock_comparison)
            self.assertEqual(parser_state["pos"], 1)

    def test_and_token_type_mismatch(self):
        """测试 token type 不是 AND 但 value 是 &&"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "BITWISE_AND", "value": "&&", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 6}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        call_count = [0]
        comparison_nodes = [
            {"type": "IDENTIFIER", "name": "a", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "name": "b", "line": 1, "column": 6}
        ]
        
        def side_effect(state):
            node = comparison_nodes[call_count[0]]
            call_count[0] += 1
            return node
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_expression_package._parse_or_package._parse_and_package._parse_comparison_package._parse_comparison_src._parse_comparison") as mock_parse_comparison:
            mock_parse_comparison.side_effect = side_effect
            
            result = _parse_and(parser_state)
            
            # 应该只解析第一个比较表达式，不处理 &&（因为 type 不匹配）
            self.assertEqual(result["name"], "a")
            self.assertEqual(mock_parse_comparison.call_count, 1)

    def test_and_value_mismatch(self):
        """测试 token value 不是 && 但 type 是 AND"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "AND", "value": "&", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        call_count = [0]
        comparison_nodes = [
            {"type": "IDENTIFIER", "name": "a", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "name": "b", "line": 1, "column": 5}
        ]
        
        def side_effect(state):
            node = comparison_nodes[call_count[0]]
            call_count[0] += 1
            return node
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_expression_package._parse_or_package._parse_and_package._parse_comparison_package._parse_comparison_src._parse_comparison") as mock_parse_comparison:
            mock_parse_comparison.side_effect = side_effect
            
            result = _parse_and(parser_state)
            
            # 应该只解析第一个比较表达式，不处理 &（因为 value 不匹配）
            self.assertEqual(result["name"], "a")
            self.assertEqual(mock_parse_comparison.call_count, 1)

    def test_parser_state_pos_updated_correctly(self):
        """测试 parser_state['pos'] 正确更新"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "AND", "value": "&&", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "y", "line": 1, "column": 6}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        call_count = [0]
        comparison_nodes = [
            {"type": "IDENTIFIER", "name": "x", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "name": "y", "line": 1, "column": 6}
        ]
        
        def side_effect(state):
            node = comparison_nodes[call_count[0]]
            call_count[0] += 1
            return node
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_expression_package._parse_or_package._parse_and_package._parse_comparison_package._parse_comparison_src._parse_comparison") as mock_parse_comparison:
            mock_parse_comparison.side_effect = side_effect
            
            result = _parse_and(parser_state)
            
            # pos 应该前进到 2（解析完 x && y）
            self.assertEqual(parser_state["pos"], 2)
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["operator"], "&&")


if __name__ == "__main__":
    unittest.main()

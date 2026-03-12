# -*- coding: utf-8 -*-
"""单元测试文件：_parse_array_literal 函数测试。"""
import unittest
from unittest.mock import patch
from typing import Dict, Any, List

# 使用相对导入导入被测函数
from ._parse_array_literal_src import _parse_array_literal, _parse_array_elements


def create_token(token_type: str, value: str = "", line: int = 1, column: int = 1) -> Dict[str, Any]:
    """辅助函数：创建 token 字典。"""
    return {
        "type": token_type,
        "value": value,
        "line": line,
        "column": column
    }


def create_parser_state(tokens: List[Dict], pos: int = 0, filename: str = "<test>") -> Dict[str, Any]:
    """辅助函数：创建 parser_state 字典。"""
    return {
        "tokens": tokens,
        "pos": pos,
        "filename": filename
    }


class TestParseArrayLiteral(unittest.TestCase):
    """_parse_array_literal 函数的测试用例。"""
    
    def test_empty_array(self):
        """测试解析空数组 []。"""
        tokens = [
            create_token("LEFT_BRACKET", "[", 1, 1),
            create_token("RIGHT_BRACKET", "]", 1, 2)
        ]
        parser_state = create_parser_state(tokens, 0)
        
        result = _parse_array_literal(parser_state)
        
        self.assertEqual(result["type"], "ArrayLiteral")
        self.assertEqual(result["children"], [])
        self.assertIsNone(result["value"])
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 2)
    
    def test_single_element_array(self):
        """测试解析单元素数组 [1]。"""
        tokens = [
            create_token("LEFT_BRACKET", "[", 1, 1),
            create_token("NUMBER", "1", 1, 2),
            create_token("RIGHT_BRACKET", "]", 1, 3)
        ]
        parser_state = create_parser_state(tokens, 0)
        
        mock_element = {
            "type": "NumberLiteral",
            "value": "1",
            "line": 1,
            "column": 2
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_expression_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_array_literal_package._parse_expression_package._parse_array_literal_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            def update_state(state):
                state["pos"] = 1
                return mock_element
            
            mock_parse_expr.side_effect = update_state
            
            result = _parse_array_literal(parser_state)
        
        self.assertEqual(result["type"], "ArrayLiteral")
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0]["type"], "NumberLiteral")
        self.assertEqual(parser_state["pos"], 2)
    
    def test_multiple_elements_array(self):
        """测试解析多元素数组 [1, 2, 3]。"""
        tokens = [
            create_token("LEFT_BRACKET", "[", 1, 1),
            create_token("NUMBER", "1", 1, 2),
            create_token("COMMA", ",", 1, 3),
            create_token("NUMBER", "2", 1, 4),
            create_token("COMMA", ",", 1, 5),
            create_token("NUMBER", "3", 1, 6),
            create_token("RIGHT_BRACKET", "]", 1, 7)
        ]
        parser_state = create_parser_state(tokens, 0)
        
        mock_elements = [
            {"type": "NumberLiteral", "value": "1", "line": 1, "column": 2},
            {"type": "NumberLiteral", "value": "2", "line": 1, "column": 4},
            {"type": "NumberLiteral", "value": "3", "line": 1, "column": 6}
        ]
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_expression_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_array_literal_package._parse_expression_package._parse_array_literal_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            call_count = [0]
            
            def update_state(state):
                idx = call_count[0]
                call_count[0] += 1
                state["pos"] = idx + 1
                return mock_elements[idx]
            
            mock_parse_expr.side_effect = update_state
            
            result = _parse_array_literal(parser_state)
        
        self.assertEqual(result["type"], "ArrayLiteral")
        self.assertEqual(len(result["children"]), 3)
        for i, child in enumerate(result["children"]):
            self.assertEqual(child["type"], "NumberLiteral")
            self.assertEqual(child["value"], str(i + 1))
        self.assertEqual(parser_state["pos"], 6)
    
    def test_missing_left_bracket(self):
        """测试缺少 LEFT_BRACKET 时的错误。"""
        tokens = [
            create_token("NUMBER", "1", 1, 1)
        ]
        parser_state = create_parser_state(tokens, 0)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_array_literal(parser_state)
        
        self.assertIn("Expected '['", str(context.exception))
    
    def test_missing_right_bracket(self):
        """测试缺少 RIGHT_BRACKET 时的错误。"""
        tokens = [
            create_token("LEFT_BRACKET", "[", 1, 1),
            create_token("NUMBER", "1", 1, 2)
        ]
        parser_state = create_parser_state(tokens, 0)
        
        mock_element = {"type": "NumberLiteral", "value": "1", "line": 1, "column": 2}
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_expression_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_array_literal_package._parse_expression_package._parse_array_literal_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            def update_state(state):
                state["pos"] = 1
                return mock_element
            
            mock_parse_expr.side_effect = update_state
            
            with self.assertRaises(SyntaxError) as context:
                _parse_array_literal(parser_state)
        
        self.assertIn("Expected ']'", str(context.exception))
    
    def test_unexpected_token_in_array(self):
        """测试数组中出现意外 token 时的错误。"""
        tokens = [
            create_token("LEFT_BRACKET", "[", 1, 1),
            create_token("NUMBER", "1", 1, 2),
            create_token("SEMICOLON", ";", 1, 3),
            create_token("RIGHT_BRACKET", "]", 1, 4)
        ]
        parser_state = create_parser_state(tokens, 0)
        
        mock_element = {"type": "NumberLiteral", "value": "1", "line": 1, "column": 2}
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_expression_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_array_literal_package._parse_expression_package._parse_array_literal_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            def update_state(state):
                state["pos"] = 1
                return mock_element
            
            mock_parse_expr.side_effect = update_state
            
            with self.assertRaises(SyntaxError) as context:
                _parse_array_literal(parser_state)
        
        self.assertIn("Expected ',' or ']'", str(context.exception))
    
    def test_empty_input(self):
        """测试输入为空时的错误。"""
        tokens = []
        parser_state = create_parser_state(tokens, 0)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_array_literal(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))
    
    def test_position_tracking(self):
        """测试 parser_state 位置正确更新。"""
        tokens = [
            create_token("LEFT_BRACKET", "[", 1, 1),
            create_token("RIGHT_BRACKET", "]", 1, 2)
        ]
        parser_state = create_parser_state(tokens, 0)
        
        result = _parse_array_literal(parser_state)
        
        self.assertEqual(parser_state["pos"], 2)
    
    def test_line_column_tracking(self):
        """测试行号和列号正确跟踪。"""
        tokens = [
            create_token("LEFT_BRACKET", "[", 5, 10),
            create_token("RIGHT_BRACKET", "]", 5, 11)
        ]
        parser_state = create_parser_state(tokens, 0)
        
        result = _parse_array_literal(parser_state)
        
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 10)
    
    def test_with_custom_filename(self):
        """测试使用自定义文件名时的错误消息。"""
        tokens = [
            create_token("NUMBER", "1", 1, 1)
        ]
        parser_state = create_parser_state(tokens, 0, "test.py")
        
        with self.assertRaises(SyntaxError) as context:
            _parse_array_literal(parser_state)
        
        self.assertIn("test.py", str(context.exception))


class TestParseArrayElements(unittest.TestCase):
    """_parse_array_elements 辅助函数的测试用例。"""
    
    def test_empty_elements(self):
        """测试解析空元素列表（直接在 RIGHT_BRACKET 处）。"""
        tokens = [
            create_token("RIGHT_BRACKET", "]", 1, 1)
        ]
        
        elements, pos = _parse_array_elements(tokens, 0, "<test>")
        
        self.assertEqual(elements, [])
        self.assertEqual(pos, 0)
    
    def test_single_element(self):
        """测试解析单个元素。"""
        tokens = [
            create_token("NUMBER", "1", 1, 1),
            create_token("RIGHT_BRACKET", "]", 1, 2)
        ]
        
        mock_element = {"type": "NumberLiteral", "value": "1"}
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_expression_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_array_literal_package._parse_expression_package._parse_array_literal_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            def update_state(state):
                state["pos"] = 1
                return mock_element
            
            mock_parse_expr.side_effect = update_state
            
            elements, pos = _parse_array_elements(tokens, 0, "<test>")
        
        self.assertEqual(len(elements), 1)
        self.assertEqual(pos, 1)
    
    def test_multiple_elements_with_commas(self):
        """测试解析多个带逗号的元素。"""
        tokens = [
            create_token("NUMBER", "1", 1, 1),
            create_token("COMMA", ",", 1, 2),
            create_token("NUMBER", "2", 1, 3),
            create_token("COMMA", ",", 1, 4),
            create_token("NUMBER", "3", 1, 5),
            create_token("RIGHT_BRACKET", "]", 1, 6)
        ]
        
        mock_elements = [
            {"type": "NumberLiteral", "value": "1"},
            {"type": "NumberLiteral", "value": "2"},
            {"type": "NumberLiteral", "value": "3"}
        ]
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_expression_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_array_literal_package._parse_expression_package._parse_array_literal_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            call_count = [0]
            
            def update_state(state):
                idx = call_count[0]
                call_count[0] += 1
                state["pos"] = idx + 1
                return mock_elements[idx]
            
            mock_parse_expr.side_effect = update_state
            
            elements, pos = _parse_array_elements(tokens, 0, "<test>")
        
        self.assertEqual(len(elements), 3)
        self.assertEqual(pos, 5)


if __name__ == "__main__":
    unittest.main()

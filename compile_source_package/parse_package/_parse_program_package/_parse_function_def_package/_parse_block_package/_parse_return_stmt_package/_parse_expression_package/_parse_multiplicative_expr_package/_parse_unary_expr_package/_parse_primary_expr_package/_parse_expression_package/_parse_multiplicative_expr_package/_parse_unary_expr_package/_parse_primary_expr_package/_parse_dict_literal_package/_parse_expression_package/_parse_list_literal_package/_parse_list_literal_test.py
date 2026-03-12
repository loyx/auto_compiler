# === std / third-party imports ===
import unittest
from typing import Any, Dict
from unittest.mock import patch

# === ADT defines ===
Token = Dict[str, Any]
AST = Dict[str, Any]
ParserState = Dict[str, Any]

# === test target import ===
from ._parse_list_literal_src import _parse_list_literal


class TestParseListLiteral(unittest.TestCase):
    """测试 _parse_list_literal 函数"""

    def _create_parser_state(self, tokens: list, pos: int = 0) -> ParserState:
        """创建测试用的 parser_state"""
        return {
            "tokens": tokens,
            "filename": "test.py",
            "pos": pos,
            "error": ""
        }

    def test_empty_list(self):
        """测试空列表 []"""
        tokens = [
            {"type": "LEFT_BRACKET", "value": "[", "line": 1, "column": 1},
            {"type": "RIGHT_BRACKET", "value": "]", "line": 1, "column": 2}
        ]
        parser_state = self._create_parser_state(tokens)
        
        result = _parse_list_literal(parser_state)
        
        self.assertEqual(result["type"], "list_literal")
        self.assertEqual(result["children"], [])
        self.assertEqual(result["value"], None)
        self.assertEqual(parser_state["pos"], 2)

    def test_single_element(self):
        """测试单个元素的列表 [1]"""
        tokens = [
            {"type": "LEFT_BRACKET", "value": "[", "line": 1, "column": 1},
            {"type": "NUMBER", "value": "1", "line": 1, "column": 2},
            {"type": "RIGHT_BRACKET", "value": "]", "line": 1, "column": 3}
        ]
        parser_state = self._create_parser_state(tokens)
        
        mock_element_ast = {"type": "number_literal", "value": 1, "children": []}
        
        with patch.object(__import__(__name__.rsplit('.', 1)[0], fromlist=['_parse_expression']), '_parse_expression', return_value=mock_element_ast) as mock_parse_expr:
            result = _parse_list_literal(parser_state)
        
        self.assertEqual(result["type"], "list_literal")
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0], mock_element_ast)
        self.assertEqual(parser_state["pos"], 3)

    def test_multiple_elements(self):
        """测试多个元素的列表 [1, 2, 3]"""
        tokens = [
            {"type": "LEFT_BRACKET", "value": "[", "line": 1, "column": 1},
            {"type": "NUMBER", "value": "1", "line": 1, "column": 2},
            {"type": "COMMA", "value": ",", "line": 1, "column": 3},
            {"type": "NUMBER", "value": "2", "line": 1, "column": 4},
            {"type": "COMMA", "value": ",", "line": 1, "column": 5},
            {"type": "NUMBER", "value": "3", "line": 1, "column": 6},
            {"type": "RIGHT_BRACKET", "value": "]", "line": 1, "column": 7}
        ]
        parser_state = self._create_parser_state(tokens)
        
        mock_element_ast1 = {"type": "number_literal", "value": 1, "children": []}
        mock_element_ast2 = {"type": "number_literal", "value": 2, "children": []}
        mock_element_ast3 = {"type": "number_literal", "value": 3, "children": []}
        
        with patch.object(__import__(__name__.rsplit('.', 1)[0], fromlist=['_parse_expression']), '_parse_expression', side_effect=[mock_element_ast1, mock_element_ast2, mock_element_ast3]) as mock_parse_expr:
            result = _parse_list_literal(parser_state)
        
        self.assertEqual(result["type"], "list_literal")
        self.assertEqual(len(result["children"]), 3)
        self.assertEqual(result["children"][0], mock_element_ast1)
        self.assertEqual(result["children"][1], mock_element_ast2)
        self.assertEqual(result["children"][2], mock_element_ast3)
        self.assertEqual(parser_state["pos"], 7)

    def test_trailing_comma(self):
        """测试尾随逗号 [1, 2,]"""
        tokens = [
            {"type": "LEFT_BRACKET", "value": "[", "line": 1, "column": 1},
            {"type": "NUMBER", "value": "1", "line": 1, "column": 2},
            {"type": "COMMA", "value": ",", "line": 1, "column": 3},
            {"type": "NUMBER", "value": "2", "line": 1, "column": 4},
            {"type": "COMMA", "value": ",", "line": 1, "column": 5},
            {"type": "RIGHT_BRACKET", "value": "]", "line": 1, "column": 6}
        ]
        parser_state = self._create_parser_state(tokens)
        
        mock_element_ast1 = {"type": "number_literal", "value": 1, "children": []}
        mock_element_ast2 = {"type": "number_literal", "value": 2, "children": []}
        
        with patch.object(__import__(__name__.rsplit('.', 1)[0], fromlist=['_parse_expression']), '_parse_expression', side_effect=[mock_element_ast1, mock_element_ast2]) as mock_parse_expr:
            result = _parse_list_literal(parser_state)
        
        self.assertEqual(result["type"], "list_literal")
        self.assertEqual(len(result["children"]), 2)
        self.assertEqual(parser_state["pos"], 6)

    def test_syntax_error_missing_comma(self):
        """测试语法错误：缺少逗号 [1 2]"""
        tokens = [
            {"type": "LEFT_BRACKET", "value": "[", "line": 1, "column": 1},
            {"type": "NUMBER", "value": "1", "line": 1, "column": 2},
            {"type": "NUMBER", "value": "2", "line": 1, "column": 3},
            {"type": "RIGHT_BRACKET", "value": "]", "line": 1, "column": 4}
        ]
        parser_state = self._create_parser_state(tokens)
        
        mock_element_ast = {"type": "number_literal", "value": 1, "children": []}
        
        with patch.object(__import__(__name__.rsplit('.', 1)[0], fromlist=['_parse_expression']), '_parse_expression', return_value=mock_element_ast):
            with self.assertRaises(SyntaxError) as context:
                _parse_list_literal(parser_state)
            
            self.assertIn("Expected COMMA or RIGHT_BRACKET", str(context.exception))

    def test_nested_list(self):
        """测试嵌套列表 [[1, 2], [3, 4]]"""
        tokens = [
            {"type": "LEFT_BRACKET", "value": "[", "line": 1, "column": 1},
            {"type": "LEFT_BRACKET", "value": "[", "line": 1, "column": 2},
            {"type": "NUMBER", "value": "1", "line": 1, "column": 3},
            {"type": "COMMA", "value": ",", "line": 1, "column": 4},
            {"type": "NUMBER", "value": "2", "line": 1, "column": 5},
            {"type": "RIGHT_BRACKET", "value": "]", "line": 1, "column": 6},
            {"type": "COMMA", "value": ",", "line": 1, "column": 7},
            {"type": "LEFT_BRACKET", "value": "[", "line": 1, "column": 8},
            {"type": "NUMBER", "value": "3", "line": 1, "column": 9},
            {"type": "COMMA", "value": ",", "line": 1, "column": 10},
            {"type": "NUMBER", "value": "4", "line": 1, "column": 11},
            {"type": "RIGHT_BRACKET", "value": "]", "line": 1, "column": 12},
            {"type": "RIGHT_BRACKET", "value": "]", "line": 1, "column": 13}
        ]
        parser_state = self._create_parser_state(tokens)
        
        mock_nested_list1 = {"type": "list_literal", "value": None, "children": []}
        mock_nested_list2 = {"type": "list_literal", "value": None, "children": []}
        
        with patch.object(__import__(__name__.rsplit('.', 1)[0], fromlist=['_parse_expression']), '_parse_expression', side_effect=[mock_nested_list1, mock_nested_list2]) as mock_parse_expr:
            result = _parse_list_literal(parser_state)
        
        self.assertEqual(result["type"], "list_literal")
        self.assertEqual(len(result["children"]), 2)
        self.assertEqual(parser_state["pos"], 13)


if __name__ == "__main__":
    unittest.main()

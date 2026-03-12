# -*- coding: utf-8 -*-
"""单元测试：_parse_block 函数"""

import unittest
from unittest.mock import patch

from ._parse_block_src import _parse_block


class TestParseBlock(unittest.TestCase):
    """测试 _parse_block 函数"""

    def test_parse_block_with_braces_empty(self):
        """测试解析空块（带花括号）"""
        tokens = [
            {"type": "LBRACE", "value": "{", "line": 1, "column": 1},
            {"type": "RBRACE", "value": "}", "line": 1, "column": 2},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.c", "error": ""}
        
        with patch("._parse_block_src._consume_token") as mock_consume:
            with patch("._parse_block_src._parse_statement") as mock_parse_stmt:
                mock_consume.side_effect = lambda state, t: state.update({"pos": state["pos"] + 1}) or True
                mock_parse_stmt.return_value = None
                
                result = _parse_block(parser_state)
        
        self.assertEqual(result["type"], "BLOCK")
        self.assertEqual(result["children"], [])
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 2)

    def test_parse_block_with_braces_single_statement(self):
        """测试解析单个语句的块（带花括号）"""
        tokens = [
            {"type": "LBRACE", "value": "{", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 3},
            {"type": "RBRACE", "value": "}", "line": 1, "column": 5},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.c", "error": ""}
        stmt_ast = {"type": "ASSIGNMENT", "children": [], "line": 1, "column": 3}
        
        with patch("._parse_block_src._consume_token") as mock_consume:
            with patch("._parse_block_src._parse_statement") as mock_parse_stmt:
                mock_consume.side_effect = lambda state, t: state.update({"pos": state["pos"] + 1}) or True
                mock_parse_stmt.return_value = stmt_ast
                
                result = _parse_block(parser_state)
        
        self.assertEqual(result["type"], "BLOCK")
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0], stmt_ast)
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)

    def test_parse_block_with_braces_multiple_statements(self):
        """测试解析多个语句的块（带花括号）"""
        tokens = [
            {"type": "LBRACE", "value": "{", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "x", "line": 2, "column": 2},
            {"type": "IDENTIFIER", "value": "y", "line": 3, "column": 2},
            {"type": "IDENTIFIER", "value": "z", "line": 4, "column": 2},
            {"type": "RBRACE", "value": "}", "line": 5, "column": 1},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.c", "error": ""}
        
        stmts = [
            {"type": "ASSIGNMENT", "children": [], "line": 2, "column": 2},
            {"type": "ASSIGNMENT", "children": [], "line": 3, "column": 2},
            {"type": "ASSIGNMENT", "children": [], "line": 4, "column": 2},
        ]
        
        with patch("._parse_block_src._consume_token") as mock_consume:
            with patch("._parse_block_src._parse_statement") as mock_parse_stmt:
                mock_consume.side_effect = lambda state, t: state.update({"pos": state["pos"] + 1}) or True
                mock_parse_stmt.side_effect = stmts
                
                result = _parse_block(parser_state)
        
        self.assertEqual(result["type"], "BLOCK")
        self.assertEqual(len(result["children"]), 3)
        self.assertEqual(result["children"], stmts)

    def test_parse_block_without_braces(self):
        """测试解析不带花括号的块"""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "y", "line": 2, "column": 1},
            {"type": "RBRACE", "value": "}", "line": 3, "column": 1},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.c", "error": ""}
        
        stmts = [
            {"type": "ASSIGNMENT", "children": [], "line": 1, "column": 1},
            {"type": "ASSIGNMENT", "children": [], "line": 2, "column": 1},
        ]
        
        with patch("._parse_block_src._consume_token") as mock_consume:
            with patch("._parse_block_src._parse_statement") as mock_parse_stmt:
                mock_consume.side_effect = lambda state, t: state.update({"pos": state["pos"] + 1}) or True
                mock_parse_stmt.side_effect = stmts
                
                result = _parse_block(parser_state)
        
        self.assertEqual(result["type"], "BLOCK")
        self.assertEqual(len(result["children"]), 2)
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)

    def test_parse_block_stops_at_rbrace(self):
        """测试解析块时在 RBRACE 处停止"""
        tokens = [
            {"type": "LBRACE", "value": "{", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 3},
            {"type": "RBRACE", "value": "}", "line": 1, "column": 5},
            {"type": "IDENTIFIER", "value": "y", "line": 2, "column": 1},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.c", "error": ""}
        stmt_ast = {"type": "ASSIGNMENT", "children": [], "line": 1, "column": 3}
        
        with patch("._parse_block_src._consume_token") as mock_consume:
            with patch("._parse_block_src._parse_statement") as mock_parse_stmt:
                mock_consume.side_effect = lambda state, t: state.update({"pos": state["pos"] + 1}) or True
                mock_parse_stmt.return_value = stmt_ast
                
                result = _parse_block(parser_state)
        
        self.assertEqual(result["type"], "BLOCK")
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(parser_state["pos"], 2)

    def test_parse_block_prevents_infinite_loop(self):
        """测试解析块时防止无限循环（pos 未前进时退出）"""
        tokens = [
            {"type": "LBRACE", "value": "{", "line": 1, "column": 1},
            {"type": "UNKNOWN", "value": "?", "line": 1, "column": 3},
            {"type": "RBRACE", "value": "}", "line": 1, "column": 5},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.c", "error": ""}
        
        with patch("._parse_block_src._consume_token") as mock_consume:
            with patch("._parse_block_src._parse_statement") as mock_parse_stmt:
                mock_consume.side_effect = lambda state, t: state.update({"pos": state["pos"] + 1}) or True
                mock_parse_stmt.return_value = None
                
                result = _parse_block(parser_state)
        
        self.assertEqual(result["type"], "BLOCK")
        self.assertEqual(result["children"], [])

    def test_parse_block_position_not_advanced_before_loop(self):
        """测试 pos 在循环前被正确保存用于检测无限循环"""
        tokens = [
            {"type": "LBRACE", "value": "{", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 3},
            {"type": "RBRACE", "value": "}", "line": 1, "column": 5},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.c", "error": ""}
        stmt_ast = {"type": "ASSIGNMENT", "children": [], "line": 1, "column": 3}
        
        call_count = [0]
        
        def parse_statement_side_effect(state):
            call_count[0] += 1
            if call_count[0] == 1:
                state["pos"] += 1
                return stmt_ast
            return None
        
        with patch("._parse_block_src._consume_token") as mock_consume:
            with patch("._parse_block_src._parse_statement") as mock_parse_stmt:
                mock_consume.side_effect = lambda state, t: state.update({"pos": state["pos"] + 1}) or True
                mock_parse_stmt.side_effect = parse_statement_side_effect
                
                result = _parse_block(parser_state)
        
        self.assertEqual(result["type"], "BLOCK")
        self.assertEqual(len(result["children"]), 1)


if __name__ == "__main__":
    unittest.main()

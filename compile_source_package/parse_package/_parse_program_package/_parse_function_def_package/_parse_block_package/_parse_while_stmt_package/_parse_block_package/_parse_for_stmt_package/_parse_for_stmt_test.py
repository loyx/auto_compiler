# -*- coding: utf-8 -*-
"""单元测试：_parse_for_stmt 函数"""

import sys
import unittest
from unittest.mock import MagicMock, patch

# 预先 mock 依赖模块，避免导入时的循环依赖问题
_mock_module = MagicMock()
sys.modules['._expect_token_package._expect_token_src'] = _mock_module
sys.modules['._parse_identifier_package._parse_identifier_src'] = _mock_module
sys.modules['._parse_expression_package._parse_expression_src'] = _mock_module
sys.modules['._parse_block_package._parse_block_src'] = _mock_module

from ._parse_for_stmt_src import _parse_for_stmt


class TestParseForStmt(unittest.TestCase):
    """_parse_for_stmt 函数测试类"""

    def test_happy_path_valid_for_statement(self):
        """测试成功解析有效的 for 语句"""
        # 准备测试数据
        for_token = {"type": "KEYWORD", "value": "for", "line": 1, "column": 0}
        in_token = {"type": "KEYWORD", "value": "in", "line": 1, "column": 10}
        tokens = [for_token, in_token]
        
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        # 准备 mock 返回值
        mock_iterator_node = {"type": "IDENTIFIER", "value": "i", "line": 1, "column": 4}
        mock_iterable_node = {"type": "CALL_EXPR", "value": "range(10)", "line": 1, "column": 7}
        mock_body_node = {"type": "BLOCK", "children": [], "line": 1, "column": 20}
        
        # 执行测试
        with patch("._expect_token_package._expect_token_src._expect_token") as mock_expect:
            with patch("._parse_identifier_package._parse_identifier_src._parse_identifier") as mock_parse_id:
                with patch("._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
                    with patch("._parse_block_package._parse_block_src._parse_block") as mock_parse_block:
                        mock_parse_id.return_value = mock_iterator_node
                        mock_parse_expr.return_value = mock_iterable_node
                        mock_parse_block.return_value = mock_body_node
                        
                        result = _parse_for_stmt(parser_state)
        
        # 验证结果
        self.assertEqual(result["type"], "FOR_STMT")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 0)
        self.assertEqual(len(result["children"]), 3)
        self.assertEqual(result["children"][0], mock_iterator_node)
        self.assertEqual(result["children"][1], mock_iterable_node)
        self.assertEqual(result["children"][2], mock_body_node)
        
        # 验证依赖调用
        self.assertEqual(mock_expect.call_count, 2)
        mock_expect.assert_any_call(parser_state, "KEYWORD", "for")
        mock_expect.assert_any_call(parser_state, "KEYWORD", "in")
        mock_parse_id.assert_called_once_with(parser_state)
        mock_parse_expr.assert_called_once_with(parser_state)
        mock_parse_block.assert_called_once_with(parser_state)

    def test_empty_tokens_raises_syntax_error(self):
        """测试空 tokens 列表抛出 SyntaxError"""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_for_stmt(parser_state)
        
        self.assertIn("Unexpected end of file", str(context.exception))

    def test_pos_beyond_tokens_length_raises_syntax_error(self):
        """测试 pos 超出 tokens 长度抛出 SyntaxError"""
        for_token = {"type": "KEYWORD", "value": "for", "line": 1, "column": 0}
        tokens = [for_token]
        
        parser_state = {
            "tokens": tokens,
            "pos": 5,  # pos 超出 tokens 长度
            "filename": "test.py",
            "error": ""
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_for_stmt(parser_state)
        
        self.assertIn("Unexpected end of file", str(context.exception))

    def test_for_token_without_line_column_defaults_to_zero(self):
        """测试 for token 缺少 line/column 时默认为 0"""
        for_token = {"type": "KEYWORD", "value": "for"}
        tokens = [for_token]
        
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        mock_iterator_node = {"type": "IDENTIFIER", "value": "x"}
        mock_iterable_node = {"type": "LIST", "value": "[]"}
        mock_body_node = {"type": "BLOCK", "children": []}
        
        with patch("._expect_token_package._expect_token_src._expect_token"):
            with patch("._parse_identifier_package._parse_identifier_src._parse_identifier") as mock_parse_id:
                with patch("._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
                    with patch("._parse_block_package._parse_block_src._parse_block") as mock_parse_block:
                        mock_parse_id.return_value = mock_iterator_node
                        mock_parse_expr.return_value = mock_iterable_node
                        mock_parse_block.return_value = mock_body_node
                        
                        result = _parse_for_stmt(parser_state)
        
        self.assertEqual(result["line"], 0)
        self.assertEqual(result["column"], 0)

    def test_expect_token_for_raises_syntax_error(self):
        """测试 _expect_token 消费 FOR 失败时抛出 SyntaxError"""
        for_token = {"type": "KEYWORD", "value": "for", "line": 1, "column": 0}
        tokens = [for_token]
        
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        with patch("._expect_token_package._expect_token_src._expect_token") as mock_expect:
            mock_expect.side_effect = SyntaxError("Expected 'for' keyword")
            
            with self.assertRaises(SyntaxError) as context:
                _parse_for_stmt(parser_state)
            
            self.assertIn("Expected 'for' keyword", str(context.exception))

    def test_expect_token_in_raises_syntax_error(self):
        """测试 _expect_token 消费 IN 失败时抛出 SyntaxError"""
        for_token = {"type": "KEYWORD", "value": "for", "line": 1, "column": 0}
        tokens = [for_token]
        
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        mock_iterator_node = {"type": "IDENTIFIER", "value": "i"}
        
        def expect_token_side_effect(state, token_type, token_value=None):
            if token_value == "for":
                return for_token
            elif token_value == "in":
                raise SyntaxError("Expected 'in' keyword")
        
        with patch("._expect_token_package._expect_token_src._expect_token") as mock_expect:
            mock_expect.side_effect = expect_token_side_effect
            with patch("._parse_identifier_package._parse_identifier_src._parse_identifier") as mock_parse_id:
                mock_parse_id.return_value = mock_iterator_node
                
                with self.assertRaises(SyntaxError) as context:
                    _parse_for_stmt(parser_state)
                
                self.assertIn("Expected 'in' keyword", str(context.exception))

    def test_parse_identifier_raises_syntax_error(self):
        """测试 _parse_identifier 失败时抛出 SyntaxError"""
        for_token = {"type": "KEYWORD", "value": "for", "line": 1, "column": 0}
        tokens = [for_token]
        
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        with patch("._expect_token_package._expect_token_src._expect_token"):
            with patch("._parse_identifier_package._parse_identifier_src._parse_identifier") as mock_parse_id:
                mock_parse_id.side_effect = SyntaxError("Expected identifier")
                
                with self.assertRaises(SyntaxError) as context:
                    _parse_for_stmt(parser_state)
                
                self.assertIn("Expected identifier", str(context.exception))

    def test_parse_expression_raises_syntax_error(self):
        """测试 _parse_expression 失败时抛出 SyntaxError"""
        for_token = {"type": "KEYWORD", "value": "for", "line": 1, "column": 0}
        tokens = [for_token]
        
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        mock_iterator_node = {"type": "IDENTIFIER", "value": "i"}
        
        with patch("._expect_token_package._expect_token_src._expect_token"):
            with patch("._parse_identifier_package._parse_identifier_src._parse_identifier") as mock_parse_id:
                mock_parse_id.return_value = mock_iterator_node
                with patch("._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
                    mock_parse_expr.side_effect = SyntaxError("Expected expression")
                    
                    with self.assertRaises(SyntaxError) as context:
                        _parse_for_stmt(parser_state)
                    
                    self.assertIn("Expected expression", str(context.exception))

    def test_parse_block_raises_syntax_error(self):
        """测试 _parse_block 失败时抛出 SyntaxError"""
        for_token = {"type": "KEYWORD", "value": "for", "line": 1, "column": 0}
        tokens = [for_token]
        
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        mock_iterator_node = {"type": "IDENTIFIER", "value": "i"}
        mock_iterable_node = {"type": "CALL_EXPR", "value": "range(5)"}
        
        with patch("._expect_token_package._expect_token_src._expect_token"):
            with patch("._parse_identifier_package._parse_identifier_src._parse_identifier") as mock_parse_id:
                mock_parse_id.return_value = mock_iterator_node
                with patch("._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
                    mock_parse_expr.return_value = mock_iterable_node
                    with patch("._parse_block_package._parse_block_src._parse_block") as mock_parse_block:
                        mock_parse_block.side_effect = SyntaxError("Expected block")
                        
                        with self.assertRaises(SyntaxError) as context:
                            _parse_for_stmt(parser_state)
                        
                        self.assertIn("Expected block", str(context.exception))

    def test_complex_for_statement_with_nested_structure(self):
        """测试复杂 for 语句（带嵌套结构）"""
        for_token = {"type": "KEYWORD", "value": "for", "line": 5, "column": 4}
        tokens = [for_token]
        
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "complex.py",
            "error": ""
        }
        
        mock_iterator_node = {
            "type": "IDENTIFIER",
            "value": "item",
            "line": 5,
            "column": 8
        }
        mock_iterable_node = {
            "type": "LIST_COMPREHENSION",
            "value": "[x for x in data]",
            "line": 5,
            "column": 13,
            "children": []
        }
        mock_body_node = {
            "type": "BLOCK",
            "line": 5,
            "column": 35,
            "children": [
                {"type": "IF_STMT", "children": []},
                {"type": "ASSIGN_STMT", "children": []}
            ]
        }
        
        with patch("._expect_token_package._expect_token_src._expect_token"):
            with patch("._parse_identifier_package._parse_identifier_src._parse_identifier") as mock_parse_id:
                mock_parse_id.return_value = mock_iterator_node
                with patch("._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
                    mock_parse_expr.return_value = mock_iterable_node
                    with patch("._parse_block_package._parse_block_src._parse_block") as mock_parse_block:
                        mock_parse_block.return_value = mock_body_node
                        
                        result = _parse_for_stmt(parser_state)
        
        self.assertEqual(result["type"], "FOR_STMT")
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 4)
        self.assertEqual(len(result["children"]), 3)
        self.assertEqual(result["children"][2]["type"], "BLOCK")
        self.assertEqual(len(result["children"][2]["children"]), 2)


if __name__ == "__main__":
    unittest.main()

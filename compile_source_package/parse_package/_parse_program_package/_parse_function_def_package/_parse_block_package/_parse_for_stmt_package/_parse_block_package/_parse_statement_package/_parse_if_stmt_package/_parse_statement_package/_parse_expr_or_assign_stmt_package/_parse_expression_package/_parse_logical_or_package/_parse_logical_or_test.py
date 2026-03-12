# -*- coding: utf-8 -*-
"""单元测试：_parse_logical_or 函数"""

import unittest
from unittest.mock import patch
from typing import Any, Dict

# 相对导入被测试模块
from ._parse_logical_or_src import _parse_logical_or


class TestParseLogicalOr(unittest.TestCase):
    """测试 _parse_logical_or 函数的各种场景"""

    def _create_parser_state(self, tokens: list, pos: int = 0, filename: str = "test.txt") -> Dict[str, Any]:
        """辅助函数：创建 parser_state"""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename
        }

    def _create_token(self, token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """辅助函数：创建 token"""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def _create_ast_node(self, node_type: str, value: Any = None, children: list = None, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """辅助函数：创建 AST 节点"""
        return {
            "type": node_type,
            "value": value,
            "children": children if children is not None else [],
            "line": line,
            "column": column
        }

    def test_single_operand_no_or(self):
        """测试：单个操作数，没有 || 运算符"""
        tokens = [self._create_token("IDENTIFIER", "x")]
        parser_state = self._create_parser_state(tokens)
        
        mock_ast = self._create_ast_node("IDENTIFIER", "x")
        
        with patch("._parse_logical_or_src._parse_logical_and", return_value=mock_ast) as mock_and:
            result = _parse_logical_or(parser_state)
            
            self.assertEqual(result, mock_ast)
            self.assertEqual(parser_state["pos"], 1)
            mock_and.assert_called_once()

    def test_single_or_operator(self):
        """测试：单个 || 运算符连接两个操作数"""
        tokens = [
            self._create_token("IDENTIFIER", "a", column=1),
            self._create_token("OPERATOR", "||", column=3),
            self._create_token("IDENTIFIER", "b", column=6)
        ]
        parser_state = self._create_parser_state(tokens)
        
        mock_left = self._create_ast_node("IDENTIFIER", "a", line=1, column=1)
        mock_right = self._create_ast_node("IDENTIFIER", "b", line=1, column=6)
        
        with patch("._parse_logical_or_src._parse_logical_and", side_effect=[mock_left, mock_right]) as mock_and:
            result = _parse_logical_or(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "||")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 3)
            self.assertEqual(len(result["children"]), 2)
            self.assertEqual(result["children"][0], mock_left)
            self.assertEqual(result["children"][1], mock_right)
            self.assertEqual(parser_state["pos"], 3)
            self.assertEqual(mock_and.call_count, 2)

    def test_multiple_or_operators_left_associative(self):
        """测试：多个 || 运算符，验证左结合性"""
        tokens = [
            self._create_token("IDENTIFIER", "a", column=1),
            self._create_token("OPERATOR", "||", column=3),
            self._create_token("IDENTIFIER", "b", column=6),
            self._create_token("OPERATOR", "||", column=8),
            self._create_token("IDENTIFIER", "c", column=11)
        ]
        parser_state = self._create_parser_state(tokens)
        
        mock_a = self._create_ast_node("IDENTIFIER", "a", line=1, column=1)
        mock_b = self._create_ast_node("IDENTIFIER", "b", line=1, column=6)
        mock_c = self._create_ast_node("IDENTIFIER", "c", line=1, column=11)
        
        with patch("._parse_logical_or_src._parse_logical_and", side_effect=[mock_a, mock_b, mock_c]) as mock_and:
            result = _parse_logical_or(parser_state)
            
            # 验证左结合性：(a || b) || c
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "||")
            self.assertEqual(result["column"], 8)  # 第二个 || 的位置
            
            # 右子节点应该是 c
            self.assertEqual(result["children"][1], mock_c)
            
            # 左子节点应该是 (a || b)
            left_child = result["children"][0]
            self.assertEqual(left_child["type"], "BINARY_OP")
            self.assertEqual(left_child["value"], "||")
            self.assertEqual(left_child["column"], 3)  # 第一个 || 的位置
            self.assertEqual(left_child["children"][0], mock_a)
            self.assertEqual(left_child["children"][1], mock_b)
            
            self.assertEqual(parser_state["pos"], 5)
            self.assertEqual(mock_and.call_count, 3)

    def test_empty_tokens(self):
        """测试：空 tokens 列表"""
        parser_state = self._create_parser_state([])
        
        mock_ast = self._create_ast_node("LITERAL", None)
        
        with patch("._parse_logical_or_src._parse_logical_and", return_value=mock_ast) as mock_and:
            result = _parse_logical_or(parser_state)
            
            self.assertEqual(result, mock_ast)
            self.assertEqual(parser_state["pos"], 0)
            mock_and.assert_called_once()

    def test_or_at_end_without_right_operand(self):
        """测试：|| 在末尾，缺少右操作数（应抛出 SyntaxError）"""
        tokens = [
            self._create_token("IDENTIFIER", "a", column=1),
            self._create_token("OPERATOR", "||", column=3)
        ]
        parser_state = self._create_parser_state(tokens)
        
        mock_left = self._create_ast_node("IDENTIFIER", "a", line=1, column=1)
        
        with patch("._parse_logical_or_src._parse_logical_and", side_effect=[mock_left, SyntaxError("Unexpected end of input")]) as mock_and:
            with self.assertRaises(SyntaxError) as context:
                _parse_logical_or(parser_state)
            
            self.assertEqual(str(context.exception), "Unexpected end of input")
            self.assertEqual(mock_and.call_count, 2)

    def test_non_or_operator(self):
        """测试：其他运算符（不是 ||），应停止解析"""
        tokens = [
            self._create_token("IDENTIFIER", "a", column=1),
            self._create_token("OPERATOR", "&&", column=3),
            self._create_token("IDENTIFIER", "b", column=6)
        ]
        parser_state = self._create_parser_state(tokens)
        
        mock_ast = self._create_ast_node("IDENTIFIER", "a", line=1, column=1)
        
        with patch("._parse_logical_or_src._parse_logical_and", return_value=mock_ast) as mock_and:
            result = _parse_logical_or(parser_state)
            
            self.assertEqual(result, mock_ast)
            self.assertEqual(parser_state["pos"], 1)  # 只消耗了第一个 token
            mock_and.assert_called_once()

    def test_different_token_type_with_or_value(self):
        """测试：token 值为 || 但类型不是 OPERATOR"""
        tokens = [
            self._create_token("IDENTIFIER", "a", column=1),
            self._create_token("KEYWORD", "||", column=3),
            self._create_token("IDENTIFIER", "b", column=6)
        ]
        parser_state = self._create_parser_state(tokens)
        
        mock_ast = self._create_ast_node("IDENTIFIER", "a", line=1, column=1)
        
        with patch("._parse_logical_or_src._parse_logical_and", return_value=mock_ast) as mock_and:
            result = _parse_logical_or(parser_state)
            
            self.assertEqual(result, mock_ast)
            self.assertEqual(parser_state["pos"], 1)  # 不应消耗 KEYWORD 类型的 ||
            mock_and.assert_called_once()

    def test_or_with_complex_operands(self):
        """测试：|| 连接复杂操作数（由 _parse_logical_and 返回的复杂 AST）"""
        tokens = [
            self._create_token("IDENTIFIER", "x", column=1),
            self._create_token("OPERATOR", "||", column=3),
            self._create_token("NUMBER", "42", column=6)
        ]
        parser_state = self._create_parser_state(tokens)
        
        mock_complex_left = self._create_ast_node("BINARY_OP", "&&", children=[
            self._create_ast_node("IDENTIFIER", "x"),
            self._create_ast_node("IDENTIFIER", "y")
        ])
        mock_complex_right = self._create_ast_node("LITERAL", 42)
        
        with patch("._parse_logical_or_src._parse_logical_and", side_effect=[mock_complex_left, mock_complex_right]) as mock_and:
            result = _parse_logical_or(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "||")
            self.assertEqual(result["children"][0], mock_complex_left)
            self.assertEqual(result["children"][1], mock_complex_right)
            self.assertEqual(parser_state["pos"], 3)
            self.assertEqual(mock_and.call_count, 2)

    def test_parser_state_pos_updated_correctly(self):
        """测试：parser_state['pos'] 正确更新"""
        tokens = [
            self._create_token("IDENTIFIER", "a", column=1),
            self._create_token("OPERATOR", "||", column=3),
            self._create_token("IDENTIFIER", "b", column=6),
            self._create_token("OPERATOR", "||", column=8),
            self._create_token("IDENTIFIER", "c", column=11),
            self._create_token("SEMICOLON", ";", column=13)
        ]
        parser_state = self._create_parser_state(tokens)
        
        mock_a = self._create_ast_node("IDENTIFIER", "a")
        mock_b = self._create_ast_node("IDENTIFIER", "b")
        mock_c = self._create_ast_node("IDENTIFIER", "c")
        
        with patch("._parse_logical_or_src._parse_logical_and", side_effect=[mock_a, mock_b, mock_c]):
            result = _parse_logical_or(parser_state)
            
            # 应该停在分号之前
            self.assertEqual(parser_state["pos"], 5)
            # 下一个 token 应该是分号
            self.assertEqual(tokens[parser_state["pos"]]["type"], "SEMICOLON")

    def test_line_column_preserved_in_ast(self):
        """测试：AST 节点保留正确的行号和列号"""
        tokens = [
            self._create_token("IDENTIFIER", "a", line=5, column=10),
            self._create_token("OPERATOR", "||", line=5, column=12),
            self._create_token("IDENTIFIER", "b", line=5, column=15)
        ]
        parser_state = self._create_parser_state(tokens)
        
        mock_left = self._create_ast_node("IDENTIFIER", "a", line=5, column=10)
        mock_right = self._create_ast_node("IDENTIFIER", "b", line=5, column=15)
        
        with patch("._parse_logical_or_src._parse_logical_and", side_effect=[mock_left, mock_right]):
            result = _parse_logical_or(parser_state)
            
            self.assertEqual(result["line"], 5)
            self.assertEqual(result["column"], 12)  # || 的列号


if __name__ == "__main__":
    unittest.main()

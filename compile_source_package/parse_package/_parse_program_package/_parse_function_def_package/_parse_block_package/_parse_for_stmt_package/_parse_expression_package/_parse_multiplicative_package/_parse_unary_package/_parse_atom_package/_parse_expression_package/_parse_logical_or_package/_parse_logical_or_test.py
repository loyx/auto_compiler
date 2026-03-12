# -*- coding: utf-8 -*-
"""单元测试文件：_parse_logical_or 函数测试"""

import unittest
from unittest.mock import patch
from typing import Dict, Any

# 相对导入被测模块
from ._parse_logical_or_src import _parse_logical_or


class TestParseLogicalOr(unittest.TestCase):
    """测试 _parse_logical_or 函数的解析逻辑或表达式功能"""

    def _create_parser_state(
        self,
        tokens: list = None,
        pos: int = 0,
        filename: str = "test.py"
    ) -> Dict[str, Any]:
        """创建测试用的 parser_state"""
        return {
            "tokens": tokens if tokens is not None else [],
            "pos": pos,
            "filename": filename
        }

    def _create_token(self, token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """创建测试用的 token"""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def _create_ast_node(
        self,
        node_type: str,
        children: list = None,
        value: Any = None,
        line: int = 1,
        column: int = 1
    ) -> Dict[str, Any]:
        """创建测试用的 AST 节点"""
        return {
            "type": node_type,
            "children": children if children is not None else [],
            "value": value,
            "line": line,
            "column": column
        }

    def test_no_or_operator_single_expression(self):
        """测试：没有 OR 运算符，只有一个表达式"""
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1)
        ]
        parser_state = self._create_parser_state(tokens=tokens, pos=0)
        
        left_node = self._create_ast_node("IDENTIFIER", value="a", line=1, column=1)
        
        with patch("._parse_logical_or_src._parse_logical_and") as mock_and:
            mock_and.return_value = left_node
            # 模拟 _current_token_is_or 返回 False（没有 OR）
            with patch("._parse_logical_or_src._current_token_is_or") as mock_is_or:
                mock_is_or.return_value = False
                
                result = _parse_logical_or(parser_state)
                
                self.assertEqual(result, left_node)
                mock_and.assert_called_once_with(parser_state)
                mock_is_or.assert_called_once_with(parser_state)

    def test_single_or_operator(self):
        """测试：单个 OR 运算符 (a or b)"""
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("OR", "or", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 6)
        ]
        parser_state = self._create_parser_state(tokens=tokens, pos=0)
        
        left_node = self._create_ast_node("IDENTIFIER", value="a", line=1, column=1)
        right_node = self._create_ast_node("IDENTIFIER", value="b", line=1, column=6)
        
        with patch("._parse_logical_or_src._parse_logical_and") as mock_and:
            mock_and.side_effect = [left_node, right_node]
            
            with patch("._parse_logical_or_src._current_token_is_or") as mock_is_or:
                mock_is_or.side_effect = [True, False]  # 第一次是 OR，第二次不是
                
                with patch("._parse_logical_or_src._consume_current_token") as mock_consume:
                    or_token = self._create_token("OR", "or", 1, 3)
                    mock_consume.return_value = or_token
                    
                    result = _parse_logical_or(parser_state)
                    
                    self.assertEqual(result["type"], "BINARY_OP")
                    self.assertEqual(result["value"], "OR")
                    self.assertEqual(result["line"], 1)
                    self.assertEqual(result["column"], 3)
                    self.assertEqual(len(result["children"]), 2)
                    self.assertEqual(result["children"][0], left_node)
                    self.assertEqual(result["children"][1], right_node)
                    
                    self.assertEqual(mock_and.call_count, 2)
                    self.assertEqual(mock_is_or.call_count, 2)
                    mock_consume.assert_called_once_with(parser_state)

    def test_multiple_or_operators_left_associative(self):
        """测试：多个 OR 运算符，左结合 (a or b or c)"""
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("OR", "or", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 6),
            self._create_token("OR", "or", 1, 8),
            self._create_token("IDENTIFIER", "c", 1, 11)
        ]
        parser_state = self._create_parser_state(tokens=tokens, pos=0)
        
        node_a = self._create_ast_node("IDENTIFIER", value="a", line=1, column=1)
        node_b = self._create_ast_node("IDENTIFIER", value="b", line=1, column=6)
        node_c = self._create_ast_node("IDENTIFIER", value="c", line=1, column=11)
        
        with patch("._parse_logical_or_src._parse_logical_and") as mock_and:
            mock_and.side_effect = [node_a, node_b, node_c]
            
            with patch("._parse_logical_or_src._current_token_is_or") as mock_is_or:
                mock_is_or.side_effect = [True, True, False]  # 两个 OR，然后结束
                
                with patch("._parse_logical_or_src._consume_current_token") as mock_consume:
                    or_token1 = self._create_token("OR", "or", 1, 3)
                    or_token2 = self._create_token("OR", "or", 1, 8)
                    mock_consume.side_effect = [or_token1, or_token2]
                    
                    result = _parse_logical_or(parser_state)
                    
                    # 验证左结合：(a or b) or c
                    self.assertEqual(result["type"], "BINARY_OP")
                    self.assertEqual(result["value"], "OR")
                    self.assertEqual(result["line"], 1)
                    self.assertEqual(result["column"], 8)  # 第二个 OR 的位置
                    
                    # 左子节点应该是 (a or b)
                    left_child = result["children"][0]
                    self.assertEqual(left_child["type"], "BINARY_OP")
                    self.assertEqual(left_child["value"], "OR")
                    self.assertEqual(left_child["line"], 1)
                    self.assertEqual(left_child["column"], 3)
                    self.assertEqual(left_child["children"][0], node_a)
                    self.assertEqual(left_child["children"][1], node_b)
                    
                    # 右子节点应该是 c
                    self.assertEqual(result["children"][1], node_c)
                    
                    self.assertEqual(mock_and.call_count, 3)
                    self.assertEqual(mock_is_or.call_count, 3)
                    self.assertEqual(mock_consume.call_count, 2)

    def test_empty_tokens(self):
        """测试：空 tokens 列表"""
        parser_state = self._create_parser_state(tokens=[], pos=0)
        
        empty_node = self._create_ast_node("EMPTY")
        
        with patch("._parse_logical_or_src._parse_logical_and") as mock_and:
            mock_and.return_value = empty_node
            
            with patch("._parse_logical_or_src._current_token_is_or") as mock_is_or:
                mock_is_or.return_value = False
                
                result = _parse_logical_or(parser_state)
                
                self.assertEqual(result, empty_node)
                mock_and.assert_called_once_with(parser_state)

    def test_error_from_logical_and_first_call(self):
        """测试：第一次调用 _parse_logical_and 时出错"""
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1)
        ]
        parser_state = self._create_parser_state(tokens=tokens, pos=0)
        parser_state["error"] = "Parse error in AND"
        
        error_node = self._create_ast_node("ERROR", value="Parse error in AND")
        
        with patch("._parse_logical_or_src._parse_logical_and") as mock_and:
            mock_and.return_value = error_node
            
            result = _parse_logical_or(parser_state)
            
            self.assertEqual(result, error_node)
            mock_and.assert_called_once_with(parser_state)

    def test_error_from_logical_and_second_call(self):
        """测试：第二次调用 _parse_logical_and（解析右侧）时出错"""
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("OR", "or", 1, 3)
        ]
        parser_state = self._create_parser_state(tokens=tokens, pos=0)
        
        left_node = self._create_ast_node("IDENTIFIER", value="a", line=1, column=1)
        error_node = self._create_ast_node("ERROR", value="Right side parse error")
        parser_state["error"] = "Right side parse error"
        
        with patch("._parse_logical_or_src._parse_logical_and") as mock_and:
            mock_and.side_effect = [left_node, error_node]
            
            with patch("._parse_logical_or_src._current_token_is_or") as mock_is_or:
                mock_is_or.return_value = True
                
                with patch("._parse_logical_or_src._consume_current_token") as mock_consume:
                    or_token = self._create_token("OR", "or", 1, 3)
                    mock_consume.return_value = or_token
                    
                    result = _parse_logical_or(parser_state)
                    
                    self.assertEqual(result, error_node)
                    self.assertEqual(mock_and.call_count, 2)

    def test_or_operator_by_value_lowercase(self):
        """测试：OR 运算符通过 value='or' 识别（小写）"""
        tokens = [
            self._create_token("KEYWORD", "or", 1, 1),
            self._create_token("IDENTIFIER", "b", 1, 4)
        ]
        parser_state = self._create_parser_state(tokens=tokens, pos=0)
        
        left_node = self._create_ast_node("IDENTIFIER", value="a", line=1, column=0)
        right_node = self._create_ast_node("IDENTIFIER", value="b", line=1, column=4)
        
        with patch("._parse_logical_or_src._parse_logical_and") as mock_and:
            mock_and.side_effect = [left_node, right_node]
            
            with patch("._parse_logical_or_src._current_token_is_or") as mock_is_or:
                mock_is_or.side_effect = [True, False]
                
                with patch("._parse_logical_or_src._consume_current_token") as mock_consume:
                    or_token = self._create_token("KEYWORD", "or", 1, 1)
                    mock_consume.return_value = or_token
                    
                    result = _parse_logical_or(parser_state)
                    
                    self.assertEqual(result["type"], "BINARY_OP")
                    self.assertEqual(result["value"], "OR")
                    self.assertEqual(result["line"], 1)
                    self.assertEqual(result["column"], 1)

    def test_or_operator_by_type(self):
        """测试：OR 运算符通过 type='OR' 识别"""
        tokens = [
            self._create_token("OR", "OR", 1, 1),
            self._create_token("IDENTIFIER", "b", 1, 4)
        ]
        parser_state = self._create_parser_state(tokens=tokens, pos=0)
        
        left_node = self._create_ast_node("IDENTIFIER", value="a", line=1, column=0)
        right_node = self._create_ast_node("IDENTIFIER", value="b", line=1, column=4)
        
        with patch("._parse_logical_or_src._parse_logical_and") as mock_and:
            mock_and.side_effect = [left_node, right_node]
            
            with patch("._parse_logical_or_src._current_token_is_or") as mock_is_or:
                mock_is_or.side_effect = [True, False]
                
                with patch("._parse_logical_or_src._consume_current_token") as mock_consume:
                    or_token = self._create_token("OR", "OR", 1, 1)
                    mock_consume.return_value = or_token
                    
                    result = _parse_logical_or(parser_state)
                    
                    self.assertEqual(result["type"], "BINARY_OP")
                    self.assertEqual(result["value"], "OR")

    def test_position_advances_after_consume(self):
        """测试：消费 token 后位置前进"""
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("OR", "or", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 6)
        ]
        parser_state = self._create_parser_state(tokens=tokens, pos=0)
        
        left_node = self._create_ast_node("IDENTIFIER", value="a", line=1, column=1)
        right_node = self._create_ast_node("IDENTIFIER", value="b", line=1, column=6)
        
        with patch("._parse_logical_or_src._parse_logical_and") as mock_and:
            mock_and.side_effect = [left_node, right_node]
            
            with patch("._parse_logical_or_src._current_token_is_or") as mock_is_or:
                mock_is_or.side_effect = [True, False]
                
                with patch("._parse_logical_or_src._consume_current_token") as mock_consume:
                    or_token = self._create_token("OR", "or", 1, 3)
                    mock_consume.return_value = or_token
                    
                    _parse_logical_or(parser_state)
                    
                    # 验证位置前进到 2（消费了一个 OR token）
                    self.assertEqual(parser_state["pos"], 2)

    def test_no_error_field_in_parser_state(self):
        """测试：parser_state 中没有 error 字段时正常处理"""
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1)
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
            # 没有 error 字段
        }
        
        left_node = self._create_ast_node("IDENTIFIER", value="a", line=1, column=1)
        
        with patch("._parse_logical_or_src._parse_logical_and") as mock_and:
            mock_and.return_value = left_node
            
            with patch("._parse_logical_or_src._current_token_is_or") as mock_is_or:
                mock_is_or.return_value = False
                
                result = _parse_logical_or(parser_state)
                
                self.assertEqual(result, left_node)
                self.assertNotIn("error", parser_state)


if __name__ == "__main__":
    unittest.main()

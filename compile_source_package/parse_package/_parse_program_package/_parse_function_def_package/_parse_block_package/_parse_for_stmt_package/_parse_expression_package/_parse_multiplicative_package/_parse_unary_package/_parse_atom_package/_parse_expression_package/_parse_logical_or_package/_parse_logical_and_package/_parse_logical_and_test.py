# -*- coding: utf-8 -*-
"""
单元测试文件：_parse_logical_and
测试目标：解析逻辑与表达式（AND 运算符）的功能
"""

import unittest
from unittest.mock import patch
from typing import Dict, Any, List

# 相对导入被测模块
from ._parse_logical_and_src import _parse_logical_and


class TestParseLogicalAnd(unittest.TestCase):
    """测试 _parse_logical_and 函数"""

    def _create_token(self, token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """辅助函数：创建 token"""
        return {
            'type': token_type,
            'value': value,
            'line': line,
            'column': column
        }

    def _create_parser_state(self, tokens: List[Dict[str, Any]], pos: int = 0, filename: str = "test.py") -> Dict[str, Any]:
        """辅助函数：创建 parser_state"""
        return {
            'tokens': tokens,
            'pos': pos,
            'filename': filename
        }

    def _create_ast_node(self, node_type: str, value: Any, children: List = None, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """辅助函数：创建 AST 节点"""
        return {
            'type': node_type,
            'value': value,
            'children': children if children is not None else [],
            'line': line,
            'column': column
        }

    def test_no_and_operator(self):
        """测试：没有 AND 运算符，直接返回左侧表达式"""
        tokens = [self._create_token('IDENTIFIER', 'x')]
        parser_state = self._create_parser_state(tokens)
        
        left_node = self._create_ast_node('IDENTIFIER', 'x')
        
        with patch('._parse_logical_and_src._parse_logical_not', return_value=left_node) as mock_not:
            result = _parse_logical_and(parser_state)
            
            # 应该只调用一次 _parse_logical_not
            self.assertEqual(mock_not.call_count, 1)
            # 返回左侧节点
            self.assertEqual(result, left_node)
            # pos 不应该改变
            self.assertEqual(parser_state['pos'], 0)

    def test_single_and_operator(self):
        """测试：单个 AND 运算符"""
        tokens = [
            self._create_token('IDENTIFIER', 'a', column=1),
            self._create_token('AND', 'and', column=3),
            self._create_token('IDENTIFIER', 'b', column=7)
        ]
        parser_state = self._create_parser_state(tokens)
        
        left_node = self._create_ast_node('IDENTIFIER', 'a', line=1, column=1)
        right_node = self._create_ast_node('IDENTIFIER', 'b', line=1, column=7)
        
        call_count = [0]
        def mock_parse_not(ps):
            node = left_node if call_count[0] == 0 else right_node
            call_count[0] += 1
            return node
        
        with patch('._parse_logical_and_src._parse_logical_not', side_effect=mock_parse_not) as mock_not:
            result = _parse_logical_and(parser_state)
            
            # 应该调用两次 _parse_logical_not
            self.assertEqual(mock_not.call_count, 2)
            # 返回 BINARY_OP 节点
            self.assertEqual(result['type'], 'BINARY_OP')
            self.assertEqual(result['value'], 'AND')
            self.assertEqual(result['line'], 1)
            self.assertEqual(result['column'], 3)
            self.assertEqual(len(result['children']), 2)
            self.assertEqual(result['children'][0], left_node)
            self.assertEqual(result['children'][1], right_node)
            # pos 应该前进到 2（消费了 AND token）
            self.assertEqual(parser_state['pos'], 2)

    def test_multiple_and_operators_left_associative(self):
        """测试：多个 AND 运算符（左结合）"""
        tokens = [
            self._create_token('IDENTIFIER', 'a', column=1),
            self._create_token('AND', 'and', column=3),
            self._create_token('IDENTIFIER', 'b', column=7),
            self._create_token('AND', 'and', column=9),
            self._create_token('IDENTIFIER', 'c', column=13)
        ]
        parser_state = self._create_parser_state(tokens)
        
        # 模拟三次 _parse_logical_not 调用返回不同的节点
        call_sequence = [
            self._create_ast_node('IDENTIFIER', 'a', line=1, column=1),
            self._create_ast_node('IDENTIFIER', 'b', line=1, column=7),
            self._create_ast_node('IDENTIFIER', 'c', line=1, column=13)
        ]
        call_count = [0]
        
        def mock_parse_not(ps):
            node = call_sequence[call_count[0]]
            call_count[0] += 1
            return node
        
        with patch('._parse_logical_and_src._parse_logical_not', side_effect=mock_parse_not) as mock_not:
            result = _parse_logical_and(parser_state)
            
            # 应该调用三次 _parse_logical_not
            self.assertEqual(mock_not.call_count, 3)
            # 返回嵌套的 BINARY_OP 节点（左结合：(a AND b) AND c）
            self.assertEqual(result['type'], 'BINARY_OP')
            self.assertEqual(result['value'], 'AND')
            self.assertEqual(result['line'], 1)
            self.assertEqual(result['column'], 9)  # 第二个 AND 的位置
            self.assertEqual(len(result['children']), 2)
            
            # 左子节点应该是第一个 BINARY_OP (a AND b)
            left_child = result['children'][0]
            self.assertEqual(left_child['type'], 'BINARY_OP')
            self.assertEqual(left_child['value'], 'AND')
            self.assertEqual(left_child['column'], 3)  # 第一个 AND 的位置
            self.assertEqual(left_child['children'][0]['value'], 'a')
            self.assertEqual(left_child['children'][1]['value'], 'b')
            
            # 右子节点应该是 c
            right_child = result['children'][1]
            self.assertEqual(right_child['value'], 'c')
            
            # pos 应该前进到 5（消费了所有 token）
            self.assertEqual(parser_state['pos'], 5)

    def test_and_by_value_lowercase(self):
        """测试：AND 运算符通过 value='and' 识别（小写）"""
        tokens = [
            self._create_token('KEYWORD', 'and', column=1),
            self._create_token('IDENTIFIER', 'b', column=5)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        left_node = self._create_ast_node('LITERAL', True, line=1, column=0)
        right_node = self._create_ast_node('IDENTIFIER', 'b', line=1, column=5)
        
        call_count = [0]
        def mock_parse_not(ps):
            node = left_node if call_count[0] == 0 else right_node
            call_count[0] += 1
            return node
        
        with patch('._parse_logical_and_src._parse_logical_not', side_effect=mock_parse_not):
            result = _parse_logical_and(parser_state)
            
            self.assertEqual(result['type'], 'BINARY_OP')
            self.assertEqual(result['value'], 'AND')
            self.assertEqual(parser_state['pos'], 2)

    def test_empty_tokens(self):
        """测试：空 token 列表"""
        parser_state = self._create_parser_state([])
        
        empty_node = self._create_ast_node('EMPTY', None)
        
        with patch('._parse_logical_and_src._parse_logical_not', return_value=empty_node):
            result = _parse_logical_and(parser_state)
            
            self.assertEqual(result, empty_node)
            self.assertEqual(parser_state['pos'], 0)

    def test_error_in_left_operand(self):
        """测试：左侧表达式解析出错"""
        tokens = [self._create_token('AND', 'and')]
        parser_state = self._create_parser_state(tokens)
        parser_state['error'] = 'Parse error in left operand'
        
        error_node = self._create_ast_node('ERROR', 'Parse error')
        
        with patch('._parse_logical_and_src._parse_logical_not', return_value=error_node):
            result = _parse_logical_and(parser_state)
            
            # 应该直接返回错误节点，不继续解析 AND
            self.assertEqual(result, error_node)
            self.assertEqual(parser_state['pos'], 0)

    def test_error_in_right_operand(self):
        """测试：右侧表达式解析出错"""
        tokens = [
            self._create_token('IDENTIFIER', 'a', column=1),
            self._create_token('AND', 'and', column=3)
        ]
        parser_state = self._create_parser_state(tokens)
        
        left_node = self._create_ast_node('IDENTIFIER', 'a', line=1, column=1)
        error_node = self._create_ast_node('ERROR', 'Parse error')
        
        call_count = [0]
        def mock_parse_not(ps):
            node = left_node if call_count[0] == 0 else error_node
            call_count[0] += 1
            if call_count[0] > 1:
                parser_state['error'] = 'Parse error in right operand'
            return node
        
        with patch('._parse_logical_and_src._parse_logical_not', side_effect=mock_parse_not):
            result = _parse_logical_and(parser_state)
            
            # 应该返回左侧节点（因为右侧出错）
            self.assertEqual(result, left_node)
            self.assertEqual(parser_state['error'], 'Parse error in right operand')
            # pos 应该已经前进了（消费了 AND token）
            self.assertEqual(parser_state['pos'], 2)

    def test_and_followed_by_non_and(self):
        """测试：AND 后面跟着非 AND token，正常结束"""
        tokens = [
            self._create_token('IDENTIFIER', 'a', column=1),
            self._create_token('AND', 'and', column=3),
            self._create_token('IDENTIFIER', 'b', column=7),
            self._create_token('OR', 'or', column=9)
        ]
        parser_state = self._create_parser_state(tokens)
        
        call_sequence = [
            self._create_ast_node('IDENTIFIER', 'a', line=1, column=1),
            self._create_ast_node('IDENTIFIER', 'b', line=1, column=7)
        ]
        call_count = [0]
        
        def mock_parse_not(ps):
            node = call_sequence[call_count[0]]
            call_count[0] += 1
            return node
        
        with patch('._parse_logical_and_src._parse_logical_not', side_effect=mock_parse_not):
            result = _parse_logical_and(parser_state)
            
            self.assertEqual(result['type'], 'BINARY_OP')
            self.assertEqual(result['value'], 'AND')
            # pos 应该停在 2（消费了 a 和 and 和 b），不消费 OR
            self.assertEqual(parser_state['pos'], 2)

    def test_and_token_type_variations(self):
        """测试：AND token 的不同 type 表示"""
        # 测试 type='AND'
        tokens1 = [
            self._create_token('IDENTIFIER', 'a'),
            self._create_token('AND', 'and'),
            self._create_token('IDENTIFIER', 'b')
        ]
        parser_state1 = self._create_parser_state(tokens1)
        
        call_sequence = [
            self._create_ast_node('IDENTIFIER', 'a'),
            self._create_ast_node('IDENTIFIER', 'b')
        ]
        call_count = [0]
        
        def mock_parse_not(ps):
            node = call_sequence[call_count[0] % 2]
            call_count[0] += 1
            return node
        
        with patch('._parse_logical_and_src._parse_logical_not', side_effect=mock_parse_not):
            result = _parse_logical_and(parser_state1)
            self.assertEqual(result['type'], 'BINARY_OP')
            self.assertEqual(parser_state1['pos'], 2)
        
        # 重置
        call_count[0] = 0
        
        # 测试 type 不是 AND 但 value 是 'and'
        tokens2 = [
            self._create_token('KEYWORD', 'and'),
            self._create_token('IDENTIFIER', 'b')
        ]
        parser_state2 = self._create_parser_state(tokens2)
        
        left_node = self._create_ast_node('LITERAL', True)
        
        def mock_parse_not2(ps):
            node = left_node if call_count[0] == 0 else self._create_ast_node('IDENTIFIER', 'b')
            call_count[0] += 1
            return node
        
        with patch('._parse_logical_and_src._parse_logical_not', side_effect=mock_parse_not2):
            result = _parse_logical_and(parser_state2)
            self.assertEqual(result['type'], 'BINARY_OP')
            self.assertEqual(parser_state2['pos'], 2)

    def test_position_at_end_after_parsing(self):
        """测试：解析完成后位置在正确位置"""
        tokens = [
            self._create_token('IDENTIFIER', 'x', column=1),
            self._create_token('AND', 'and', column=3),
            self._create_token('IDENTIFIER', 'y', column=7),
            self._create_token('AND', 'and', column=9),
            self._create_token('IDENTIFIER', 'z', column=13),
            self._create_token('SEMICOLON', ';', column=15)
        ]
        parser_state = self._create_parser_state(tokens)
        
        call_sequence = [
            self._create_ast_node('IDENTIFIER', 'x', line=1, column=1),
            self._create_ast_node('IDENTIFIER', 'y', line=1, column=7),
            self._create_ast_node('IDENTIFIER', 'z', line=1, column=13)
        ]
        call_count = [0]
        
        def mock_parse_not(ps):
            node = call_sequence[call_count[0]]
            call_count[0] += 1
            return node
        
        with patch('._parse_logical_and_src._parse_logical_not', side_effect=mock_parse_not):
            result = _parse_logical_and(parser_state)
            
            self.assertEqual(result['type'], 'BINARY_OP')
            # 应该消费了 5 个 token (x, and, y, and, z)，停在 SEMICOLON 前
            self.assertEqual(parser_state['pos'], 5)


class TestParseLogicalAndEdgeCases(unittest.TestCase):
    """测试边界情况"""

    def _create_token(self, token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
        return {
            'type': token_type,
            'value': value,
            'line': line,
            'column': column
        }

    def _create_parser_state(self, tokens: List[Dict[str, Any]], pos: int = 0, filename: str = "test.py") -> Dict[str, Any]:
        return {
            'tokens': tokens,
            'pos': pos,
            'filename': filename
        }

    def test_starting_position_not_zero(self):
        """测试：从非零位置开始解析"""
        tokens = [
            self._create_token('SEMICOLON', ';'),
            self._create_token('SEMICOLON', ';'),
            self._create_token('IDENTIFIER', 'a', column=5),
            self._create_token('AND', 'and', column=7),
            self._create_token('IDENTIFIER', 'b', column=11)
        ]
        parser_state = self._create_parser_state(tokens, pos=2)
        
        call_sequence = [
            self._create_ast_node('IDENTIFIER', 'a', line=1, column=5),
            self._create_ast_node('IDENTIFIER', 'b', line=1, column=11)
        ]
        call_count = [0]
        
        def mock_parse_not(ps):
            node = call_sequence[call_count[0]]
            call_count[0] += 1
            return node
        
        with patch('._parse_logical_and_src._parse_logical_not', side_effect=mock_parse_not):
            result = _parse_logical_and(parser_state)
            
            self.assertEqual(result['type'], 'BINARY_OP')
            # pos 应该从 2 前进到 4
            self.assertEqual(parser_state['pos'], 4)

    def test_missing_line_column_info(self):
        """测试：token 缺少 line/column 信息时的容错"""
        tokens = [
            {'type': 'IDENTIFIER', 'value': 'a'},
            {'type': 'AND', 'value': 'and'},
            {'type': 'IDENTIFIER', 'value': 'b'}
        ]
        parser_state = self._create_parser_state(tokens)
        
        call_sequence = [
            {'type': 'IDENTIFIER', 'value': 'a'},
            {'type': 'IDENTIFIER', 'value': 'b'}
        ]
        call_count = [0]
        
        def mock_parse_not(ps):
            node = call_sequence[call_count[0]]
            call_count[0] += 1
            return node
        
        with patch('._parse_logical_and_src._parse_logical_not', side_effect=mock_parse_not):
            result = _parse_logical_and(parser_state)
            
            self.assertEqual(result['type'], 'BINARY_OP')
            self.assertEqual(result['value'], 'AND')
            # 缺少 line/column 时应该使用默认值 0
            self.assertEqual(result.get('line', 0), 0)
            self.assertEqual(result.get('column', 0), 0)

    def test_parser_state_missing_pos(self):
        """测试：parser_state 缺少 pos 字段时的容错"""
        tokens = [
            self._create_token('IDENTIFIER', 'a'),
            self._create_token('AND', 'and'),
            self._create_token('IDENTIFIER', 'b')
        ]
        parser_state = {
            'tokens': tokens,
            'filename': 'test.py'
            # 没有 pos 字段
        }
        
        call_sequence = [
            self._create_ast_node('IDENTIFIER', 'a'),
            self._create_ast_node('IDENTIFIER', 'b')
        ]
        call_count = [0]
        
        def mock_parse_not(ps):
            node = call_sequence[call_count[0]]
            call_count[0] += 1
            return node
        
        with patch('._parse_logical_and_src._parse_logical_not', side_effect=mock_parse_not):
            result = _parse_logical_and(parser_state)
            
            self.assertEqual(result['type'], 'BINARY_OP')
            # pos 应该被设置为 2
            self.assertEqual(parser_state['pos'], 2)

    def test_parser_state_missing_tokens(self):
        """测试：parser_state 缺少 tokens 字段时的容错"""
        parser_state = {
            'pos': 0,
            'filename': 'test.py'
            # 没有 tokens 字段
        }
        
        empty_node = self._create_ast_node('EMPTY', None)
        
        with patch('._parse_logical_and_src._parse_logical_not', return_value=empty_node):
            result = _parse_logical_and(parser_state)
            
            # 应该返回左侧节点，不进入循环
            self.assertEqual(result, empty_node)


if __name__ == '__main__':
    unittest.main()

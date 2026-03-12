# === std / third-party imports ===
import unittest
from unittest.mock import patch
from typing import Dict, Any, List

# === relative imports ===
from ._parse_unary_src import _parse_unary


class TestParseUnary(unittest.TestCase):
    """单元测试：_parse_unary 函数"""

    def _create_token(self, token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """辅助函数：创建 token"""
        return {
            'type': token_type,
            'value': value,
            'line': line,
            'column': column
        }

    def _create_parser_state(self, tokens: List[Dict[str, Any]], pos: int = 0, filename: str = 'test.py') -> Dict[str, Any]:
        """辅助函数：创建 parser_state"""
        return {
            'tokens': tokens,
            'pos': pos,
            'filename': filename
        }

    def test_single_plus_operator(self):
        """测试：单个 PLUS 运算符 +x"""
        tokens = [
            self._create_token('PLUS', '+', 1, 1),
            self._create_token('IDENTIFIER', 'x', 1, 2)
        ]
        parser_state = self._create_parser_state(tokens)

        with patch('._parse_unary_package._parse_primary_package._parse_primary_src._parse_primary') as mock_primary:
            mock_primary.return_value = {
                'type': 'IDENTIFIER',
                'value': 'x',
                'children': [],
                'line': 1,
                'column': 2
            }

            result = _parse_unary(parser_state)

            self.assertEqual(result['type'], 'UNARY_OP')
            self.assertEqual(result['value'], '+')
            self.assertEqual(len(result['children']), 1)
            self.assertEqual(result['line'], 1)
            self.assertEqual(result['column'], 1)
            self.assertEqual(parser_state['pos'], 2)
            mock_primary.assert_called_once()

    def test_single_minus_operator(self):
        """测试：单个 MINUS 运算符 -x"""
        tokens = [
            self._create_token('MINUS', '-', 2, 5),
            self._create_token('IDENTIFIER', 'y', 2, 6)
        ]
        parser_state = self._create_parser_state(tokens)

        with patch('._parse_unary_package._parse_primary_package._parse_primary_src._parse_primary') as mock_primary:
            mock_primary.return_value = {
                'type': 'IDENTIFIER',
                'value': 'y',
                'children': [],
                'line': 2,
                'column': 6
            }

            result = _parse_unary(parser_state)

            self.assertEqual(result['type'], 'UNARY_OP')
            self.assertEqual(result['value'], '-')
            self.assertEqual(result['line'], 2)
            self.assertEqual(result['column'], 5)
            self.assertEqual(parser_state['pos'], 2)

    def test_single_not_operator(self):
        """测试：单个 NOT 运算符 not x"""
        tokens = [
            self._create_token('NOT', 'not', 3, 10),
            self._create_token('IDENTIFIER', 'flag', 3, 14)
        ]
        parser_state = self._create_parser_state(tokens)

        with patch('._parse_unary_package._parse_primary_package._parse_primary_src._parse_primary') as mock_primary:
            mock_primary.return_value = {
                'type': 'IDENTIFIER',
                'value': 'flag',
                'children': [],
                'line': 3,
                'column': 14
            }

            result = _parse_unary(parser_state)

            self.assertEqual(result['type'], 'UNARY_OP')
            self.assertEqual(result['value'], 'not')
            self.assertEqual(result['line'], 3)
            self.assertEqual(result['column'], 10)
            self.assertEqual(parser_state['pos'], 2)

    def test_chained_unary_operators(self):
        """测试：链式一元运算符 ---x"""
        tokens = [
            self._create_token('MINUS', '-', 1, 1),
            self._create_token('MINUS', '-', 1, 2),
            self._create_token('MINUS', '-', 1, 3),
            self._create_token('IDENTIFIER', 'x', 1, 4)
        ]
        parser_state = self._create_parser_state(tokens)

        with patch('._parse_unary_package._parse_primary_package._parse_primary_src._parse_primary') as mock_primary:
            mock_primary.return_value = {
                'type': 'IDENTIFIER',
                'value': 'x',
                'children': [],
                'line': 1,
                'column': 4
            }

            result = _parse_unary(parser_state)

            # 最外层是第一个 MINUS
            self.assertEqual(result['type'], 'UNARY_OP')
            self.assertEqual(result['value'], '-')
            self.assertEqual(result['line'], 1)
            self.assertEqual(result['column'], 1)
            self.assertEqual(parser_state['pos'], 4)

            # 检查嵌套结构
            operand1 = result['children'][0]
            self.assertEqual(operand1['type'], 'UNARY_OP')
            self.assertEqual(operand1['value'], '-')
            self.assertEqual(operand1['line'], 1)
            self.assertEqual(operand1['column'], 2)

            operand2 = operand1['children'][0]
            self.assertEqual(operand2['type'], 'UNARY_OP')
            self.assertEqual(operand2['value'], '-')
            self.assertEqual(operand2['line'], 1)
            self.assertEqual(operand2['column'], 3)

            operand3 = operand2['children'][0]
            self.assertEqual(operand3['type'], 'IDENTIFIER')
            self.assertEqual(operand3['value'], 'x')

    def test_chained_mixed_operators(self):
        """测试：混合链式一元运算符 +-not x"""
        tokens = [
            self._create_token('PLUS', '+', 1, 1),
            self._create_token('MINUS', '-', 1, 2),
            self._create_token('NOT', 'not', 1, 3),
            self._create_token('IDENTIFIER', 'x', 1, 7)
        ]
        parser_state = self._create_parser_state(tokens)

        with patch('._parse_unary_package._parse_primary_package._parse_primary_src._parse_primary') as mock_primary:
            mock_primary.return_value = {
                'type': 'IDENTIFIER',
                'value': 'x',
                'children': [],
                'line': 1,
                'column': 7
            }

            result = _parse_unary(parser_state)

            self.assertEqual(result['type'], 'UNARY_OP')
            self.assertEqual(result['value'], '+')
            self.assertEqual(result['line'], 1)
            self.assertEqual(result['column'], 1)
            self.assertEqual(parser_state['pos'], 4)

            # 检查第二层
            operand1 = result['children'][0]
            self.assertEqual(operand1['type'], 'UNARY_OP')
            self.assertEqual(operand1['value'], '-')

            # 检查第三层
            operand2 = operand1['children'][0]
            self.assertEqual(operand2['type'], 'UNARY_OP')
            self.assertEqual(operand2['value'], 'not')

            # 检查最内层
            operand3 = operand2['children'][0]
            self.assertEqual(operand3['type'], 'IDENTIFIER')

    def test_not_not_operator(self):
        """测试：not not x"""
        tokens = [
            self._create_token('NOT', 'not', 5, 1),
            self._create_token('NOT', 'not', 5, 5),
            self._create_token('IDENTIFIER', 'x', 5, 9)
        ]
        parser_state = self._create_parser_state(tokens)

        with patch('._parse_unary_package._parse_primary_package._parse_primary_src._parse_primary') as mock_primary:
            mock_primary.return_value = {
                'type': 'IDENTIFIER',
                'value': 'x',
                'children': [],
                'line': 5,
                'column': 9
            }

            result = _parse_unary(parser_state)

            self.assertEqual(result['type'], 'UNARY_OP')
            self.assertEqual(result['value'], 'not')
            self.assertEqual(result['line'], 5)
            self.assertEqual(result['column'], 1)
            self.assertEqual(parser_state['pos'], 3)

            operand = result['children'][0]
            self.assertEqual(operand['type'], 'UNARY_OP')
            self.assertEqual(operand['value'], 'not')
            self.assertEqual(operand['line'], 5)
            self.assertEqual(operand['column'], 5)

    def test_no_unary_operator_delegates_to_primary(self):
        """测试：没有一元运算符时委托给 _parse_primary"""
        tokens = [
            self._create_token('IDENTIFIER', 'x', 1, 1),
            self._create_token('PLUS', '+', 1, 2)
        ]
        parser_state = self._create_parser_state(tokens)

        expected_primary_result = {
            'type': 'IDENTIFIER',
            'value': 'x',
            'children': [],
            'line': 1,
            'column': 1
        }

        with patch('._parse_unary_package._parse_primary_package._parse_primary_src._parse_primary') as mock_primary:
            mock_primary.return_value = expected_primary_result

            result = _parse_unary(parser_state)

            self.assertEqual(result, expected_primary_result)
            self.assertEqual(parser_state['pos'], 0)  # pos 不应改变
            mock_primary.assert_called_once_with(parser_state)

    def test_literal_delegates_to_primary(self):
        """测试：字面量委托给 _parse_primary"""
        tokens = [
            self._create_token('NUMBER', '42', 1, 1)
        ]
        parser_state = self._create_parser_state(tokens)

        expected_primary_result = {
            'type': 'LITERAL',
            'value': 42,
            'children': [],
            'line': 1,
            'column': 1
        }

        with patch('._parse_unary_package._parse_primary_package._parse_primary_src._parse_primary') as mock_primary:
            mock_primary.return_value = expected_primary_result

            result = _parse_unary(parser_state)

            self.assertEqual(result, expected_primary_result)
            mock_primary.assert_called_once()

    def test_empty_token_list_error(self):
        """测试：空 token 列表返回 ERROR"""
        parser_state = self._create_parser_state([])

        result = _parse_unary(parser_state)

        self.assertEqual(result['type'], 'ERROR')
        self.assertEqual(result['value'], '')
        self.assertEqual(result['children'], [])
        self.assertEqual(result['line'], 0)
        self.assertEqual(result['column'], 0)
        self.assertEqual(parser_state['error'], 'Unexpected end of input')
        self.assertEqual(parser_state['pos'], 0)  # pos 不应改变

    def test_pos_at_end_of_tokens_error(self):
        """测试：pos 在 token 列表末尾返回 ERROR"""
        tokens = [
            self._create_token('IDENTIFIER', 'x', 1, 1)
        ]
        parser_state = self._create_parser_state(tokens, pos=1)

        result = _parse_unary(parser_state)

        self.assertEqual(result['type'], 'ERROR')
        self.assertEqual(result['value'], '')
        self.assertEqual(result['children'], [])
        self.assertEqual(result['line'], 0)
        self.assertEqual(result['column'], 0)
        self.assertEqual(parser_state['error'], 'Unexpected end of input')
        self.assertEqual(parser_state['pos'], 1)  # pos 不应改变

    def test_line_column_from_operator_token(self):
        """测试：UNARY_OP 节点的 line/column 来自运算符 token"""
        tokens = [
            self._create_token('MINUS', '-', 10, 25),
            self._create_token('IDENTIFIER', 'x', 10, 26)
        ]
        parser_state = self._create_parser_state(tokens)

        with patch('._parse_unary_package._parse_primary_package._parse_primary_src._parse_primary') as mock_primary:
            mock_primary.return_value = {
                'type': 'IDENTIFIER',
                'value': 'x',
                'children': [],
                'line': 10,
                'column': 26
            }

            result = _parse_unary(parser_state)

            # 验证 line/column 来自运算符 token，而不是操作数
            self.assertEqual(result['line'], 10)
            self.assertEqual(result['column'], 25)
            self.assertNotEqual(result['column'], 26)

    def test_pos_updated_after_parsing(self):
        """测试：解析后 parser_state['pos'] 正确更新"""
        tokens = [
            self._create_token('PLUS', '+', 1, 1),
            self._create_token('IDENTIFIER', 'x', 1, 2)
        ]
        parser_state = self._create_parser_state(tokens)

        with patch('._parse_unary_package._parse_primary_package._parse_primary_src._parse_primary') as mock_primary:
            mock_primary.return_value = {
                'type': 'IDENTIFIER',
                'value': 'x',
                'children': [],
                'line': 1,
                'column': 2
            }

            initial_pos = parser_state['pos']
            result = _parse_unary(parser_state)

            # pos 应该从 0 更新到 2（越过运算符和操作数）
            self.assertEqual(initial_pos, 0)
            self.assertEqual(parser_state['pos'], 2)

    def test_error_not_set_on_success(self):
        """测试：成功解析时不设置 error 字段"""
        tokens = [
            self._create_token('MINUS', '-', 1, 1),
            self._create_token('NUMBER', '5', 1, 2)
        ]
        parser_state = self._create_parser_state(tokens)

        with patch('._parse_unary_package._parse_primary_package._parse_primary_src._parse_primary') as mock_primary:
            mock_primary.return_value = {
                'type': 'LITERAL',
                'value': 5,
                'children': [],
                'line': 1,
                'column': 2
            }

            result = _parse_unary(parser_state)

            self.assertEqual(result['type'], 'UNARY_OP')
            self.assertNotIn('error', parser_state)

    def test_complex_expression_with_multiple_chained_operators(self):
        """测试：复杂表达式 + - + - x"""
        tokens = [
            self._create_token('PLUS', '+', 1, 1),
            self._create_token('MINUS', '-', 1, 3),
            self._create_token('PLUS', '+', 1, 5),
            self._create_token('MINUS', '-', 1, 7),
            self._create_token('IDENTIFIER', 'x', 1, 9)
        ]
        parser_state = self._create_parser_state(tokens)

        with patch('._parse_unary_package._parse_primary_package._parse_primary_src._parse_primary') as mock_primary:
            mock_primary.return_value = {
                'type': 'IDENTIFIER',
                'value': 'x',
                'children': [],
                'line': 1,
                'column': 9
            }

            result = _parse_unary(parser_state)

            # 验证有 4 层嵌套的 UNARY_OP
            self.assertEqual(result['type'], 'UNARY_OP')
            self.assertEqual(result['value'], '+')
            self.assertEqual(result['column'], 1)

            current = result
            expected_ops = ['+', '-', '+', '-']
            for i, expected_op in enumerate(expected_ops):
                self.assertEqual(current['type'], 'UNARY_OP')
                self.assertEqual(current['value'], expected_op)
                self.assertEqual(current['column'], 1 + i * 2)
                if i < len(expected_ops) - 1:
                    current = current['children'][0]

            # 最内层应该是 IDENTIFIER
            self.assertEqual(current['children'][0]['type'], 'IDENTIFIER')
            self.assertEqual(parser_state['pos'], 5)


if __name__ == '__main__':
    unittest.main()

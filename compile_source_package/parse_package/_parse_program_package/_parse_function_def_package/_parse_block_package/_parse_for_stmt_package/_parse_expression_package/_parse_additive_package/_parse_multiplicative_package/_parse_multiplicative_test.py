import unittest
from unittest.mock import patch

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from _parse_multiplicative_src import _parse_multiplicative


class TestParseMultiplicative(unittest.TestCase):
    """Test cases for _parse_multiplicative function."""

    def test_simple_multiplication(self):
        """Test parsing simple multiplication: a * b"""
        tokens = [
            {'type': 'IDENT', 'value': 'a', 'line': 1, 'column': 1},
            {'type': 'STAR', 'value': '*', 'line': 1, 'column': 3},
            {'type': 'IDENT', 'value': 'b', 'line': 1, 'column': 5}
        ]
        parser_state = {
            'tokens': tokens,
            'pos': 0,
            'filename': 'test.c'
        }
        
        unary_node_a = {'type': 'IDENT', 'value': 'a', 'line': 1, 'column': 1}
        unary_node_b = {'type': 'IDENT', 'value': 'b', 'line': 1, 'column': 5}
        
        with patch('_parse_unary_package._parse_unary_src._parse_unary') as mock_unary:
            mock_unary.side_effect = [unary_node_a, unary_node_b]
            
            result = _parse_multiplicative(parser_state)
            
            self.assertEqual(mock_unary.call_count, 2)
            self.assertEqual(result['type'], 'BINARY_OP')
            self.assertEqual(result['value'], '*')
            self.assertEqual(len(result['children']), 2)
            self.assertEqual(result['children'][0], unary_node_a)
            self.assertEqual(result['children'][1], unary_node_b)
            self.assertEqual(parser_state['pos'], 3)

    def test_simple_division(self):
        """Test parsing simple division: a / b"""
        tokens = [
            {'type': 'IDENT', 'value': 'a', 'line': 1, 'column': 1},
            {'type': 'SLASH', 'value': '/', 'line': 1, 'column': 3},
            {'type': 'IDENT', 'value': 'b', 'line': 1, 'column': 5}
        ]
        parser_state = {
            'tokens': tokens,
            'pos': 0,
            'filename': 'test.c'
        }
        
        unary_node_a = {'type': 'IDENT', 'value': 'a', 'line': 1, 'column': 1}
        unary_node_b = {'type': 'IDENT', 'value': 'b', 'line': 1, 'column': 5}
        
        with patch('_parse_unary_package._parse_unary_src._parse_unary') as mock_unary:
            mock_unary.side_effect = [unary_node_a, unary_node_b]
            
            result = _parse_multiplicative(parser_state)
            
            self.assertEqual(mock_unary.call_count, 2)
            self.assertEqual(result['type'], 'BINARY_OP')
            self.assertEqual(result['value'], '/')
            self.assertEqual(len(result['children']), 2)
            self.assertEqual(result['children'][0], unary_node_a)
            self.assertEqual(result['children'][1], unary_node_b)
            self.assertEqual(parser_state['pos'], 3)

    def test_multiple_multiplicative_operators_left_associative(self):
        """Test left-associativity: a * b / c should be ((a * b) / c)"""
        tokens = [
            {'type': 'IDENT', 'value': 'a', 'line': 1, 'column': 1},
            {'type': 'STAR', 'value': '*', 'line': 1, 'column': 3},
            {'type': 'IDENT', 'value': 'b', 'line': 1, 'column': 5},
            {'type': 'SLASH', 'value': '/', 'line': 1, 'column': 7},
            {'type': 'IDENT', 'value': 'c', 'line': 1, 'column': 9}
        ]
        parser_state = {
            'tokens': tokens,
            'pos': 0,
            'filename': 'test.c'
        }
        
        unary_node_a = {'type': 'IDENT', 'value': 'a', 'line': 1, 'column': 1}
        unary_node_b = {'type': 'IDENT', 'value': 'b', 'line': 1, 'column': 5}
        unary_node_c = {'type': 'IDENT', 'value': 'c', 'line': 1, 'column': 9}
        
        with patch('_parse_unary_package._parse_unary_src._parse_unary') as mock_unary:
            mock_unary.side_effect = [unary_node_a, unary_node_b, unary_node_c]
            
            result = _parse_multiplicative(parser_state)
            
            self.assertEqual(mock_unary.call_count, 3)
            self.assertEqual(result['type'], 'BINARY_OP')
            self.assertEqual(result['value'], '/')
            self.assertEqual(len(result['children']), 2)
            
            left_child = result['children'][0]
            self.assertEqual(left_child['type'], 'BINARY_OP')
            self.assertEqual(left_child['value'], '*')
            self.assertEqual(left_child['children'][0], unary_node_a)
            self.assertEqual(left_child['children'][1], unary_node_b)
            
            self.assertEqual(result['children'][1], unary_node_c)
            self.assertEqual(parser_state['pos'], 5)

    def test_single_unary_no_multiplicative(self):
        """Test when there's only a unary expression, no multiplicative operators."""
        tokens = [
            {'type': 'IDENT', 'value': 'a', 'line': 1, 'column': 1}
        ]
        parser_state = {
            'tokens': tokens,
            'pos': 0,
            'filename': 'test.c'
        }
        
        unary_node = {'type': 'IDENT', 'value': 'a', 'line': 1, 'column': 1}
        
        with patch('_parse_unary_package._parse_unary_src._parse_unary') as mock_unary:
            mock_unary.return_value = unary_node
            
            result = _parse_multiplicative(parser_state)
            
            mock_unary.assert_called_once()
            self.assertEqual(result, unary_node)
            self.assertEqual(parser_state['pos'], 0)

    def test_empty_tokens(self):
        """Test edge case with empty tokens list."""
        parser_state = {
            'tokens': [],
            'pos': 0,
            'filename': 'test.c'
        }
        
        unary_node = {'type': 'IDENT', 'value': 'a', 'line': 1, 'column': 1}
        
        with patch('_parse_unary_package._parse_unary_src._parse_unary') as mock_unary:
            mock_unary.return_value = unary_node
            
            result = _parse_multiplicative(parser_state)
            
            mock_unary.assert_called_once()
            self.assertEqual(result, unary_node)
            self.assertEqual(parser_state['pos'], 0)

    def test_non_multiplicative_token_stops_loop(self):
        """Test that non-multiplicative tokens break the loop."""
        tokens = [
            {'type': 'IDENT', 'value': 'a', 'line': 1, 'column': 1},
            {'type': 'PLUS', 'value': '+', 'line': 1, 'column': 3},
            {'type': 'IDENT', 'value': 'b', 'line': 1, 'column': 5}
        ]
        parser_state = {
            'tokens': tokens,
            'pos': 0,
            'filename': 'test.c'
        }
        
        unary_node_a = {'type': 'IDENT', 'value': 'a', 'line': 1, 'column': 1}
        
        with patch('_parse_unary_package._parse_unary_src._parse_unary') as mock_unary:
            mock_unary.return_value = unary_node_a
            
            result = _parse_multiplicative(parser_state)
            
            mock_unary.assert_called_once()
            self.assertEqual(result, unary_node_a)
            self.assertEqual(parser_state['pos'], 0)

    def test_position_at_end_of_tokens(self):
        """Test when position is already at end of tokens."""
        tokens = [
            {'type': 'IDENT', 'value': 'a', 'line': 1, 'column': 1}
        ]
        parser_state = {
            'tokens': tokens,
            'pos': 1,
            'filename': 'test.c'
        }
        
        unary_node = {'type': 'IDENT', 'value': 'a', 'line': 1, 'column': 1}
        
        with patch('_parse_unary_package._parse_unary_src._parse_unary') as mock_unary:
            mock_unary.return_value = unary_node
            
            result = _parse_multiplicative(parser_state)
            
            mock_unary.assert_called_once()
            self.assertEqual(result, unary_node)
            self.assertEqual(parser_state['pos'], 1)

    def test_ast_node_line_column_preserved(self):
        """Test that AST node preserves line and column from left operand."""
        tokens = [
            {'type': 'IDENT', 'value': 'a', 'line': 2, 'column': 10},
            {'type': 'STAR', 'value': '*', 'line': 2, 'column': 12},
            {'type': 'IDENT', 'value': 'b', 'line': 2, 'column': 14}
        ]
        parser_state = {
            'tokens': tokens,
            'pos': 0,
            'filename': 'test.c'
        }
        
        unary_node_a = {'type': 'IDENT', 'value': 'a', 'line': 2, 'column': 10}
        unary_node_b = {'type': 'IDENT', 'value': 'b', 'line': 2, 'column': 14}
        
        with patch('_parse_unary_package._parse_unary_src._parse_unary') as mock_unary:
            mock_unary.side_effect = [unary_node_a, unary_node_b]
            
            result = _parse_multiplicative(parser_state)
            
            self.assertEqual(result['line'], 2)
            self.assertEqual(result['column'], 10)


if __name__ == '__main__':
    unittest.main()
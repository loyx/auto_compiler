# -*- coding: utf-8 -*-
"""Unit tests for _advance function."""

import unittest
from typing import Any, Dict

# Relative import from the same package
from ._advance_src import _advance


class TestAdvance(unittest.TestCase):
    """Test cases for _advance function."""

    def test_advance_from_zero(self):
        """Test advancing parser position from 0."""
        parser_state: Dict[str, Any] = {
            'tokens': ['token1', 'token2'],
            'pos': 0,
            'filename': 'test.py'
        }
        result = _advance(parser_state)
        self.assertIsNone(result)
        self.assertEqual(parser_state['pos'], 1)

    def test_advance_from_middle(self):
        """Test advancing parser position from middle of tokens."""
        parser_state: Dict[str, Any] = {
            'tokens': ['t1', 't2', 't3', 't4', 't5'],
            'pos': 2,
            'filename': 'test.py'
        }
        result = _advance(parser_state)
        self.assertIsNone(result)
        self.assertEqual(parser_state['pos'], 3)

    def test_advance_multiple_times(self):
        """Test advancing parser position multiple times."""
        parser_state: Dict[str, Any] = {
            'tokens': ['t1', 't2', 't3', 't4', 't5'],
            'pos': 0,
            'filename': 'test.py'
        }
        for i in range(5):
            _advance(parser_state)
            self.assertEqual(parser_state['pos'], i + 1)

    def test_advance_minimal_state(self):
        """Test advancing with minimal parser state (only pos key)."""
        parser_state: Dict[str, Any] = {'pos': 5}
        result = _advance(parser_state)
        self.assertIsNone(result)
        self.assertEqual(parser_state['pos'], 6)

    def test_advance_large_position(self):
        """Test advancing from a large position value."""
        parser_state: Dict[str, Any] = {
            'tokens': [],
            'pos': 1000,
            'filename': 'test.py'
        }
        result = _advance(parser_state)
        self.assertIsNone(result)
        self.assertEqual(parser_state['pos'], 1001)

    def test_advance_in_place_modification(self):
        """Test that _advance modifies the dict in-place."""
        parser_state: Dict[str, Any] = {'pos': 10}
        original_id = id(parser_state)
        _advance(parser_state)
        self.assertEqual(id(parser_state), original_id)
        self.assertEqual(parser_state['pos'], 11)

    def test_advance_preserves_other_fields(self):
        """Test that other fields in parser_state are preserved."""
        parser_state: Dict[str, Any] = {
            'tokens': ['t1', 't2'],
            'pos': 0,
            'filename': 'test.py',
            'error': None,
            'custom_field': 'value'
        }
        _advance(parser_state)
        self.assertEqual(parser_state['pos'], 1)
        self.assertEqual(parser_state['tokens'], ['t1', 't2'])
        self.assertEqual(parser_state['filename'], 'test.py')
        self.assertEqual(parser_state['error'], None)
        self.assertEqual(parser_state['custom_field'], 'value')


if __name__ == '__main__':
    unittest.main()

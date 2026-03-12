"""
Unit tests for _match function.
Tests the token matching and consumption logic in the parser.
"""
from ._match_src import _match


class TestMatch:
    """Test cases for _match function"""

    def test_match_success(self):
        """Test successful token match and consumption"""
        parser_state = {
            'tokens': [
                {'type': 'NAME', 'value': 'x', 'line': 1, 'column': 1}
            ],
            'pos': 0
        }
        result = _match(parser_state, 'NAME')
        assert result is True
        assert parser_state['pos'] == 1

    def test_match_failure_different_type(self):
        """Test match fails when token type doesn't match"""
        parser_state = {
            'tokens': [
                {'type': 'NAME', 'value': 'x', 'line': 1, 'column': 1}
            ],
            'pos': 0
        }
        result = _match(parser_state, 'NUMBER')
        assert result is False
        assert parser_state['pos'] == 0  # pos should not change

    def test_match_empty_tokens(self):
        """Test match with empty tokens list"""
        parser_state = {
            'tokens': [],
            'pos': 0
        }
        result = _match(parser_state, 'NAME')
        assert result is False
        assert parser_state['pos'] == 0

    def test_match_pos_at_end(self):
        """Test match when position is at end of tokens"""
        parser_state = {
            'tokens': [
                {'type': 'NAME', 'value': 'x', 'line': 1, 'column': 1}
            ],
            'pos': 1
        }
        result = _match(parser_state, 'NAME')
        assert result is False
        assert parser_state['pos'] == 1

    def test_match_pos_beyond_end(self):
        """Test match when position is beyond tokens"""
        parser_state = {
            'tokens': [
                {'type': 'NAME', 'value': 'x', 'line': 1, 'column': 1}
            ],
            'pos': 5
        }
        result = _match(parser_state, 'NAME')
        assert result is False
        assert parser_state['pos'] == 5

    def test_match_multiple_consecutive(self):
        """Test multiple consecutive matches"""
        parser_state = {
            'tokens': [
                {'type': 'NAME', 'value': 'x', 'line': 1, 'column': 1},
                {'type': 'NUMBER', 'value': '42', 'line': 1, 'column': 3},
                {'type': 'OP', 'value': '+', 'line': 1, 'column': 5}
            ],
            'pos': 0
        }
        assert _match(parser_state, 'NAME') is True
        assert parser_state['pos'] == 1
        assert _match(parser_state, 'NUMBER') is True
        assert parser_state['pos'] == 2
        assert _match(parser_state, 'OP') is True
        assert parser_state['pos'] == 3
        assert _match(parser_state, 'NAME') is False  # No more tokens

    def test_match_middle_position(self):
        """Test match from middle position in tokens"""
        parser_state = {
            'tokens': [
                {'type': 'NAME', 'value': 'x', 'line': 1, 'column': 1},
                {'type': 'NUMBER', 'value': '42', 'line': 1, 'column': 3},
                {'type': 'OP', 'value': '+', 'line': 1, 'column': 5}
            ],
            'pos': 1
        }
        result = _match(parser_state, 'NUMBER')
        assert result is True
        assert parser_state['pos'] == 2

    def test_match_preserves_other_state_fields(self):
        """Test that match doesn't modify other parser_state fields"""
        parser_state = {
            'tokens': [
                {'type': 'NAME', 'value': 'x', 'line': 1, 'column': 1}
            ],
            'pos': 0,
            'filename': 'test.py',
            'error': None
        }
        _match(parser_state, 'NAME')
        assert parser_state['filename'] == 'test.py'
        assert parser_state['error'] is None

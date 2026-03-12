# -*- coding: utf-8 -*-
"""Unit tests for _raise_error function."""

import pytest
from ._raise_error_src import _raise_error


class TestRaiseError:
    """Test cases for _raise_error function."""

    def test_raise_error_with_full_location_info(self):
        """Test error message with filename, line, and column."""
        parser_state = {
            "filename": "test.py",
            "pos": 0,
            "tokens": [
                {"type": "NAME", "value": "x", "line": 5, "column": 10}
            ]
        }
        message = "Invalid syntax"
        
        with pytest.raises(SyntaxError) as exc_info:
            _raise_error(parser_state, message)
        
        assert str(exc_info.value) == "test.py:5:10: Invalid syntax"

    def test_raise_error_with_filename_and_line_only(self):
        """Test error message with filename and line but no column."""
        parser_state = {
            "filename": "test.py",
            "pos": 0,
            "tokens": [
                {"type": "NAME", "value": "x", "line": 5}
            ]
        }
        message = "Invalid syntax"
        
        with pytest.raises(SyntaxError) as exc_info:
            _raise_error(parser_state, message)
        
        assert str(exc_info.value) == "test.py:5: Invalid syntax"

    def test_raise_error_with_filename_only(self):
        """Test error message with filename but no line/column."""
        parser_state = {
            "filename": "test.py",
            "pos": 0,
            "tokens": [
                {"type": "NAME", "value": "x"}
            ]
        }
        message = "Invalid syntax"
        
        with pytest.raises(SyntaxError) as exc_info:
            _raise_error(parser_state, message)
        
        assert str(exc_info.value) == "test.py: Invalid syntax"

    def test_raise_error_with_no_location_info(self):
        """Test error message with no location information."""
        parser_state = {
            "pos": 0,
            "tokens": [
                {"type": "NAME", "value": "x"}
            ]
        }
        message = "Invalid syntax"
        
        with pytest.raises(SyntaxError) as exc_info:
            _raise_error(parser_state, message)
        
        assert str(exc_info.value) == "Invalid syntax"

    def test_raise_error_with_empty_tokens(self):
        """Test error message when tokens list is empty."""
        parser_state = {
            "filename": "test.py",
            "pos": 0,
            "tokens": []
        }
        message = "Invalid syntax"
        
        with pytest.raises(SyntaxError) as exc_info:
            _raise_error(parser_state, message)
        
        assert str(exc_info.value) == "test.py: Invalid syntax"

    def test_raise_error_with_pos_out_of_bounds(self):
        """Test error message when pos is out of tokens bounds."""
        parser_state = {
            "filename": "test.py",
            "pos": 10,
            "tokens": [
                {"type": "NAME", "value": "x", "line": 5, "column": 10}
            ]
        }
        message = "Invalid syntax"
        
        with pytest.raises(SyntaxError) as exc_info:
            _raise_error(parser_state, message)
        
        assert str(exc_info.value) == "test.py: Invalid syntax"

    def test_raise_error_with_negative_pos(self):
        """Test error message when pos is negative."""
        parser_state = {
            "filename": "test.py",
            "pos": -1,
            "tokens": [
                {"type": "NAME", "value": "x", "line": 5, "column": 10}
            ]
        }
        message = "Invalid syntax"
        
        with pytest.raises(SyntaxError) as exc_info:
            _raise_error(parser_state, message)
        
        assert str(exc_info.value) == "test.py: Invalid syntax"

    def test_raise_error_with_missing_keys_in_parser_state(self):
        """Test error message when parser_state is missing keys."""
        parser_state = {}
        message = "Invalid syntax"
        
        with pytest.raises(SyntaxError) as exc_info:
            _raise_error(parser_state, message)
        
        assert str(exc_info.value) == "Invalid syntax"

    def test_raise_error_with_none_filename(self):
        """Test error message when filename is None."""
        parser_state = {
            "filename": None,
            "pos": 0,
            "tokens": [
                {"type": "NAME", "value": "x", "line": 5, "column": 10}
            ]
        }
        message = "Invalid syntax"
        
        with pytest.raises(SyntaxError) as exc_info:
            _raise_error(parser_state, message)
        
        assert str(exc_info.value) == "Invalid syntax"

    def test_raise_error_with_empty_filename(self):
        """Test error message when filename is empty string."""
        parser_state = {
            "filename": "",
            "pos": 0,
            "tokens": [
                {"type": "NAME", "value": "x", "line": 5, "column": 10}
            ]
        }
        message = "Invalid syntax"
        
        with pytest.raises(SyntaxError) as exc_info:
            _raise_error(parser_state, message)
        
        assert str(exc_info.value) == "Invalid syntax"

    def test_raise_error_preserves_message_content(self):
        """Test that the original message content is preserved."""
        parser_state = {
            "filename": "test.py",
            "pos": 0,
            "tokens": [
                {"type": "NAME", "value": "x", "line": 5, "column": 10}
            ]
        }
        message = "Expected ':' but found '='"
        
        with pytest.raises(SyntaxError) as exc_info:
            _raise_error(parser_state, message)
        
        assert "Expected ':' but found '='" in str(exc_info.value)

    def test_raise_error_with_complex_filename_path(self):
        """Test error message with complex file path."""
        parser_state = {
            "filename": "/path/to/complex/module/test.py",
            "pos": 0,
            "tokens": [
                {"type": "NAME", "value": "x", "line": 100, "column": 50}
            ]
        }
        message = "Invalid syntax"
        
        with pytest.raises(SyntaxError) as exc_info:
            _raise_error(parser_state, message)
        
        assert str(exc_info.value) == "/path/to/complex/module/test.py:100:50: Invalid syntax"

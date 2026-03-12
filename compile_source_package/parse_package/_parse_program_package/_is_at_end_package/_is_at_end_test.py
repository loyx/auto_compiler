import unittest

from ._is_at_end_src import _is_at_end


class TestIsAtEnd(unittest.TestCase):
    """Test cases for _is_at_end function."""

    def test_not_at_end_pos_less_than_length(self):
        """Test when pos is less than tokens length - should return False."""
        parser_state = {
            "tokens": [{"type": "ID", "value": "x", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test.cc"
        }
        result = _is_at_end(parser_state)
        self.assertFalse(result)

    def test_at_end_pos_equals_length(self):
        """Test when pos equals tokens length - should return True."""
        parser_state = {
            "tokens": [{"type": "ID", "value": "x", "line": 1, "column": 1}],
            "pos": 1,
            "filename": "test.cc"
        }
        result = _is_at_end(parser_state)
        self.assertTrue(result)

    def test_past_end_pos_greater_than_length(self):
        """Test when pos is greater than tokens length - should return True."""
        parser_state = {
            "tokens": [{"type": "ID", "value": "x", "line": 1, "column": 1}],
            "pos": 5,
            "filename": "test.cc"
        }
        result = _is_at_end(parser_state)
        self.assertTrue(result)

    def test_empty_tokens_list(self):
        """Test with empty tokens list - should return True (already at end)."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.cc"
        }
        result = _is_at_end(parser_state)
        self.assertTrue(result)

    def test_multiple_tokens_at_start(self):
        """Test with multiple tokens at start position - should return False."""
        parser_state = {
            "tokens": [
                {"type": "ID", "value": "x", "line": 1, "column": 1},
                {"type": "OP", "value": "+", "line": 1, "column": 2},
                {"type": "NUM", "value": "1", "line": 1, "column": 3},
            ],
            "pos": 0,
            "filename": "test.cc"
        }
        result = _is_at_end(parser_state)
        self.assertFalse(result)

    def test_multiple_tokens_in_middle(self):
        """Test with multiple tokens at middle position - should return False."""
        parser_state = {
            "tokens": [
                {"type": "ID", "value": "x", "line": 1, "column": 1},
                {"type": "OP", "value": "+", "line": 1, "column": 2},
                {"type": "NUM", "value": "1", "line": 1, "column": 3},
            ],
            "pos": 1,
            "filename": "test.cc"
        }
        result = _is_at_end(parser_state)
        self.assertFalse(result)

    def test_multiple_tokens_at_end(self):
        """Test with multiple tokens at end position - should return True."""
        parser_state = {
            "tokens": [
                {"type": "ID", "value": "x", "line": 1, "column": 1},
                {"type": "OP", "value": "+", "line": 1, "column": 2},
                {"type": "NUM", "value": "1", "line": 1, "column": 3},
            ],
            "pos": 3,
            "filename": "test.cc"
        }
        result = _is_at_end(parser_state)
        self.assertTrue(result)

    def test_extra_fields_in_parser_state(self):
        """Test that extra fields in parser_state don't affect result."""
        parser_state = {
            "tokens": [{"type": "ID", "value": "x", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test.cc",
            "error": None,
            "extra_field": "ignored"
        }
        result = _is_at_end(parser_state)
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()

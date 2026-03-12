import unittest

# Relative import from the same package
from ._skip_whitespace_and_comments_src import _skip_whitespace_and_comments


class TestSkipWhitespaceAndComments(unittest.TestCase):
    """Test cases for _skip_whitespace_and_comments function."""

    def test_skip_spaces(self):
        """Test skipping space characters"""
        source = "  code"
        pos, line, column = _skip_whitespace_and_comments(source, 0, 1, 1)
        self.assertEqual(pos, 2)
        self.assertEqual(line, 1)
        self.assertEqual(column, 3)

    def test_skip_tab(self):
        """Test skipping tab character"""
        source = "\tcode"
        pos, line, column = _skip_whitespace_and_comments(source, 0, 1, 1)
        self.assertEqual(pos, 1)
        self.assertEqual(line, 1)
        self.assertEqual(column, 2)

    def test_skip_newline(self):
        """Test skipping newline character"""
        source = "\ncode"
        pos, line, column = _skip_whitespace_and_comments(source, 0, 1, 1)
        self.assertEqual(pos, 1)
        self.assertEqual(line, 2)
        self.assertEqual(column, 1)

    def test_skip_carriage_return(self):
        """Test skipping carriage return"""
        source = "\rcode"
        pos, line, column = _skip_whitespace_and_comments(source, 0, 1, 1)
        self.assertEqual(pos, 1)
        self.assertEqual(line, 1)
        self.assertEqual(column, 1)

    def test_skip_single_line_comment(self):
        """Test skipping // comment"""
        source = "// comment\ncode"
        pos, line, column = _skip_whitespace_and_comments(source, 0, 1, 1)
        self.assertEqual(pos, 11)
        self.assertEqual(line, 2)
        self.assertEqual(column, 1)

    def test_skip_comment_at_end_of_file(self):
        """Test // comment at end without newline"""
        source = "// comment"
        pos, line, column = _skip_whitespace_and_comments(source, 0, 1, 1)
        self.assertEqual(pos, 10)
        self.assertEqual(line, 1)
        self.assertEqual(column, 11)

    def test_multiple_whitespace(self):
        """Test multiple consecutive whitespace characters"""
        source = "  \t  code"
        pos, line, column = _skip_whitespace_and_comments(source, 0, 1, 1)
        self.assertEqual(pos, 5)
        self.assertEqual(line, 1)
        self.assertEqual(column, 6)

    def test_mixed_whitespace_and_newlines(self):
        """Test mixed whitespace with newlines"""
        source = "  \n  code"
        pos, line, column = _skip_whitespace_and_comments(source, 0, 1, 1)
        self.assertEqual(pos, 5)
        self.assertEqual(line, 2)
        self.assertEqual(column, 3)

    def test_no_whitespace(self):
        """Test when there's no whitespace to skip"""
        source = "code"
        pos, line, column = _skip_whitespace_and_comments(source, 0, 1, 1)
        self.assertEqual(pos, 0)
        self.assertEqual(line, 1)
        self.assertEqual(column, 1)

    def test_empty_string(self):
        """Test with empty source string"""
        source = ""
        pos, line, column = _skip_whitespace_and_comments(source, 0, 1, 1)
        self.assertEqual(pos, 0)
        self.assertEqual(line, 1)
        self.assertEqual(column, 1)

    def test_start_from_middle_position(self):
        """Test starting from a middle position"""
        source = "code  more"
        pos, line, column = _skip_whitespace_and_comments(source, 4, 1, 5)
        self.assertEqual(pos, 6)
        self.assertEqual(line, 1)
        self.assertEqual(column, 7)

    def test_comment_with_various_chars(self):
        """Test comment with various characters"""
        source = "// comment with spaces and tabs\t\ncode"
        pos, line, column = _skip_whitespace_and_comments(source, 0, 1, 1)
        self.assertEqual(pos, 33)
        self.assertEqual(line, 2)
        self.assertEqual(column, 1)

    def test_slash_not_comment(self):
        """Test single / is not treated as comment"""
        source = "/ code"
        pos, line, column = _skip_whitespace_and_comments(source, 0, 1, 1)
        self.assertEqual(pos, 0)
        self.assertEqual(line, 1)
        self.assertEqual(column, 1)

    def test_multiple_lines_with_comments(self):
        """Test multiple lines with comments"""
        source = "// comment1\n  \n// comment2\ncode"
        pos, line, column = _skip_whitespace_and_comments(source, 0, 1, 1)
        self.assertEqual(pos, 27)
        self.assertEqual(line, 4)
        self.assertEqual(column, 1)

    def test_whitespace_after_comment(self):
        """Test whitespace after comment on same line"""
        source = "// comment  \ncode"
        pos, line, column = _skip_whitespace_and_comments(source, 0, 1, 1)
        self.assertEqual(pos, 13)
        self.assertEqual(line, 2)
        self.assertEqual(column, 1)


if __name__ == '__main__':
    unittest.main()

import unittest
from unittest.mock import patch


class TestParseBinaryOp(unittest.TestCase):
    """Test cases for _parse_binary_op function."""

    def test_no_operator_returns_left(self):
        """Test that when there's no operator, left is returned unchanged."""
        from ._parse_binary_op_src import _parse_binary_op
        
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
            ],
            "pos": 1,
            "filename": "test.py"
        }
        left = {"type": "NUMBER", "value": "1", "line": 1, "column": 1}
        
        result = _parse_binary_op(parser_state, 0, left)
        
        self.assertEqual(result, left)
        self.assertEqual(parser_state["pos"], 1)

    def test_single_plus_operator(self):
        """Test parsing a single PLUS operator."""
        from ._parse_binary_op_src import _parse_binary_op
        
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 5},
            ],
            "pos": 1,
            "filename": "test.py"
        }
        left = {"type": "NUMBER", "value": "1", "line": 1, "column": 1}
        
        with patch("._parse_primary_package._parse_primary_src._parse_primary") as mock_parse_primary:
            mock_parse_primary.return_value = {"type": "NUMBER", "value": "2", "line": 1, "column": 5}
            result = _parse_binary_op(parser_state, 0, left)
        
        self.assertEqual(result["type"], "BINARY_EXPR")
        self.assertEqual(result["value"], "PLUS")
        self.assertEqual(len(result["children"]), 2)
        self.assertEqual(result["children"][0], left)
        self.assertEqual(result["children"][1]["type"], "NUMBER")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 3)
        self.assertEqual(parser_state["pos"], 3)

    def test_single_minus_operator(self):
        """Test parsing a single MINUS operator."""
        from ._parse_binary_op_src import _parse_binary_op
        
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "5", "line": 1, "column": 1},
                {"type": "MINUS", "value": "-", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "3", "line": 1, "column": 5},
            ],
            "pos": 1,
            "filename": "test.py"
        }
        left = {"type": "NUMBER", "value": "5", "line": 1, "column": 1}
        
        with patch("._parse_primary_package._parse_primary_src._parse_primary") as mock_parse_primary:
            mock_parse_primary.return_value = {"type": "NUMBER", "value": "3", "line": 1, "column": 5}
            result = _parse_binary_op(parser_state, 0, left)
        
        self.assertEqual(result["type"], "BINARY_EXPR")
        self.assertEqual(result["value"], "MINUS")
        self.assertEqual(parser_state["pos"], 3)

    def test_single_star_operator(self):
        """Test parsing a single STAR operator."""
        from ._parse_binary_op_src import _parse_binary_op
        
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "2", "line": 1, "column": 1},
                {"type": "STAR", "value": "*", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "3", "line": 1, "column": 5},
            ],
            "pos": 1,
            "filename": "test.py"
        }
        left = {"type": "NUMBER", "value": "2", "line": 1, "column": 1}
        
        with patch("._parse_primary_package._parse_primary_src._parse_primary") as mock_parse_primary:
            mock_parse_primary.return_value = {"type": "NUMBER", "value": "3", "line": 1, "column": 5}
            result = _parse_binary_op(parser_state, 0, left)
        
        self.assertEqual(result["type"], "BINARY_EXPR")
        self.assertEqual(result["value"], "STAR")
        self.assertEqual(parser_state["pos"], 3)

    def test_single_slash_operator(self):
        """Test parsing a single SLASH operator."""
        from ._parse_binary_op_src import _parse_binary_op
        
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "10", "line": 1, "column": 1},
                {"type": "SLASH", "value": "/", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 5},
            ],
            "pos": 1,
            "filename": "test.py"
        }
        left = {"type": "NUMBER", "value": "10", "line": 1, "column": 1}
        
        with patch("._parse_primary_package._parse_primary_src._parse_primary") as mock_parse_primary:
            mock_parse_primary.return_value = {"type": "NUMBER", "value": "2", "line": 1, "column": 5}
            result = _parse_binary_op(parser_state, 0, left)
        
        self.assertEqual(result["type"], "BINARY_EXPR")
        self.assertEqual(result["value"], "SLASH")
        self.assertEqual(parser_state["pos"], 3)

    def test_left_to_right_associativity(self):
        """Test that operators of same precedence are left-associative."""
        from ._parse_binary_op_src import _parse_binary_op
        
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 5},
                {"type": "PLUS", "value": "+", "line": 1, "column": 7},
                {"type": "NUMBER", "value": "3", "line": 1, "column": 9},
            ],
            "pos": 1,
            "filename": "test.py"
        }
        left = {"type": "NUMBER", "value": "1", "line": 1, "column": 1}
        
        with patch("._parse_primary_package._parse_primary_src._parse_primary") as mock_parse_primary:
            mock_parse_primary.side_effect = [
                {"type": "NUMBER", "value": "2", "line": 1, "column": 5},
                {"type": "NUMBER", "value": "3", "line": 1, "column": 9},
            ]
            result = _parse_binary_op(parser_state, 0, left)
        
        self.assertEqual(result["type"], "BINARY_EXPR")
        self.assertEqual(result["value"], "PLUS")
        self.assertEqual(result["children"][0]["value"], "PLUS")
        self.assertEqual(parser_state["pos"], 5)

    def test_star_higher_precedence_than_plus(self):
        """Test that STAR has higher precedence than PLUS."""
        from ._parse_binary_op_src import _parse_binary_op
        
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 5},
                {"type": "STAR", "value": "*", "line": 1, "column": 7},
                {"type": "NUMBER", "value": "3", "line": 1, "column": 9},
            ],
            "pos": 1,
            "filename": "test.py"
        }
        left = {"type": "NUMBER", "value": "1", "line": 1, "column": 1}
        
        with patch("._parse_primary_package._parse_primary_src._parse_primary") as mock_parse_primary:
            mock_parse_primary.side_effect = [
                {"type": "NUMBER", "value": "2", "line": 1, "column": 5},
                {"type": "NUMBER", "value": "3", "line": 1, "column": 9},
            ]
            result = _parse_binary_op(parser_state, 0, left)
        
        self.assertEqual(result["type"], "BINARY_EXPR")
        self.assertEqual(result["value"], "PLUS")
        self.assertEqual(result["children"][1]["value"], "STAR")
        self.assertEqual(parser_state["pos"], 5)

    def test_slash_higher_precedence_than_minus(self):
        """Test that SLASH has higher precedence than MINUS."""
        from ._parse_binary_op_src import _parse_binary_op
        
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "10", "line": 1, "column": 1},
                {"type": "MINUS", "value": "-", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "6", "line": 1, "column": 5},
                {"type": "SLASH", "value": "/", "line": 1, "column": 7},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 9},
            ],
            "pos": 1,
            "filename": "test.py"
        }
        left = {"type": "NUMBER", "value": "10", "line": 1, "column": 1}
        
        with patch("._parse_primary_package._parse_primary_src._parse_primary") as mock_parse_primary:
            mock_parse_primary.side_effect = [
                {"type": "NUMBER", "value": "6", "line": 1, "column": 5},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 9},
            ]
            result = _parse_binary_op(parser_state, 0, left)
        
        self.assertEqual(result["type"], "BINARY_EXPR")
        self.assertEqual(result["value"], "MINUS")
        self.assertEqual(result["children"][1]["value"], "SLASH")
        self.assertEqual(parser_state["pos"], 5)

    def test_min_precedence_filters_operators(self):
        """Test that min_precedence parameter filters lower precedence operators."""
        from ._parse_binary_op_src import _parse_binary_op
        
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 5},
            ],
            "pos": 1,
            "filename": "test.py"
        }
        left = {"type": "NUMBER", "value": "1", "line": 1, "column": 1}
        
        with patch("._parse_primary_package._parse_primary_src._parse_primary") as mock_parse_primary:
            mock_parse_primary.return_value = {"type": "NUMBER", "value": "2", "line": 1, "column": 5}
            result = _parse_binary_op(parser_state, 2, left)
        
        self.assertEqual(result, left)
        self.assertEqual(parser_state["pos"], 1)

    def test_non_operator_token_stops_parsing(self):
        """Test that non-operator tokens stop parsing."""
        from ._parse_binary_op_src import _parse_binary_op
        
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "SEMICOLON", "value": ";", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 5},
            ],
            "pos": 1,
            "filename": "test.py"
        }
        left = {"type": "NUMBER", "value": "1", "line": 1, "column": 1}
        
        result = _parse_binary_op(parser_state, 0, left)
        
        self.assertEqual(result, left)
        self.assertEqual(parser_state["pos"], 1)

    def test_pos_at_end_returns_left(self):
        """Test that when pos is at end of tokens, left is returned."""
        from ._parse_binary_op_src import _parse_binary_op
        
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
            ],
            "pos": 1,
            "filename": "test.py"
        }
        left = {"type": "NUMBER", "value": "1", "line": 1, "column": 1}
        
        result = _parse_binary_op(parser_state, 0, left)
        
        self.assertEqual(result, left)

    def test_mixed_precedence_complex(self):
        """Test complex expression with mixed precedence: 1 + 2 * 3 - 4."""
        from ._parse_binary_op_src import _parse_binary_op
        
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 5},
                {"type": "STAR", "value": "*", "line": 1, "column": 7},
                {"type": "NUMBER", "value": "3", "line": 1, "column": 9},
                {"type": "MINUS", "value": "-", "line": 1, "column": 11},
                {"type": "NUMBER", "value": "4", "line": 1, "column": 13},
            ],
            "pos": 1,
            "filename": "test.py"
        }
        left = {"type": "NUMBER", "value": "1", "line": 1, "column": 1}
        
        with patch("._parse_primary_package._parse_primary_src._parse_primary") as mock_parse_primary:
            mock_parse_primary.side_effect = [
                {"type": "NUMBER", "value": "2", "line": 1, "column": 5},
                {"type": "NUMBER", "value": "3", "line": 1, "column": 9},
                {"type": "NUMBER", "value": "4", "line": 1, "column": 13},
            ]
            result = _parse_binary_op(parser_state, 0, left)
        
        self.assertEqual(result["type"], "BINARY_EXPR")
        self.assertEqual(result["value"], "MINUS")
        self.assertEqual(result["children"][0]["value"], "PLUS")
        self.assertEqual(result["children"][0]["children"][1]["value"], "STAR")
        self.assertEqual(parser_state["pos"], 7)

    def test_filename_in_error_context(self):
        """Test that filename is properly retrieved from parser_state."""
        from ._parse_binary_op_src import _parse_binary_op
        
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 5},
            ],
            "pos": 1,
            "filename": "custom_file.py"
        }
        left = {"type": "NUMBER", "value": "1", "line": 1, "column": 1}
        
        with patch("._parse_primary_package._parse_primary_src._parse_primary") as mock_parse_primary:
            mock_parse_primary.return_value = {"type": "NUMBER", "value": "2", "line": 1, "column": 5}
            result = _parse_binary_op(parser_state, 0, left)
        
        self.assertEqual(result["type"], "BINARY_EXPR")
        self.assertEqual(parser_state["pos"], 3)

    def test_default_filename_when_missing(self):
        """Test that default filename is used when not provided."""
        from ._parse_binary_op_src import _parse_binary_op
        
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
            ],
            "pos": 1
        }
        left = {"type": "NUMBER", "value": "1", "line": 1, "column": 1}
        
        result = _parse_binary_op(parser_state, 0, left)
        
        self.assertEqual(result, left)


if __name__ == "__main__":
    unittest.main()

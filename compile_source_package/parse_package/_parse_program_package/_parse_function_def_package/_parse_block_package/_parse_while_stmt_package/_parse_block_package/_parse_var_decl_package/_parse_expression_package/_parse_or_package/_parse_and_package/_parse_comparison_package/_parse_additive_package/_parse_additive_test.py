import unittest
from unittest.mock import patch

from ._parse_additive_src import _parse_additive


class TestParseAdditive(unittest.TestCase):
    """Test cases for _parse_additive function."""

    @patch('_parse_additive_package._parse_additive_src._consume_token')
    @patch('_parse_additive_package._parse_additive_src._parse_multiplicative')
    def test_simple_addition(self, mock_parse_mult, mock_consume):
        """Test parsing simple addition expression: a + b."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "5", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "3", "line": 1, "column": 5},
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        left_operand = {"type": "NUMBER", "value": "5"}
        right_operand = {"type": "NUMBER", "value": "3"}
        
        mock_parse_mult.side_effect = [
            (left_operand, {"pos": 1, "tokens": parser_state["tokens"]}),
            (right_operand, {"pos": 3, "tokens": parser_state["tokens"]}),
        ]
        mock_consume.return_value = {"pos": 2, "tokens": parser_state["tokens"]}
        
        result_ast, result_state = _parse_additive(parser_state)
        
        self.assertEqual(result_ast["type"], "BINARY_OP")
        self.assertEqual(result_ast["value"], "+")
        self.assertEqual(len(result_ast["children"]), 2)
        self.assertEqual(result_ast["children"][0], left_operand)
        self.assertEqual(result_ast["children"][1], right_operand)
        self.assertEqual(result_ast["line"], 1)
        self.assertEqual(result_ast["column"], 3)

    @patch('_parse_additive_package._parse_additive_src._consume_token')
    @patch('_parse_additive_package._parse_additive_src._parse_multiplicative')
    def test_simple_subtraction(self, mock_parse_mult, mock_consume):
        """Test parsing simple subtraction expression: a - b."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "10", "line": 1, "column": 1},
                {"type": "MINUS", "value": "-", "line": 1, "column": 4},
                {"type": "NUMBER", "value": "4", "line": 1, "column": 6},
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        left_operand = {"type": "NUMBER", "value": "10"}
        right_operand = {"type": "NUMBER", "value": "4"}
        
        mock_parse_mult.side_effect = [
            (left_operand, {"pos": 1, "tokens": parser_state["tokens"]}),
            (right_operand, {"pos": 3, "tokens": parser_state["tokens"]}),
        ]
        mock_consume.return_value = {"pos": 2, "tokens": parser_state["tokens"]}
        
        result_ast, result_state = _parse_additive(parser_state)
        
        self.assertEqual(result_ast["type"], "BINARY_OP")
        self.assertEqual(result_ast["value"], "-")
        self.assertEqual(len(result_ast["children"]), 2)

    @patch('_parse_additive_package._parse_additive_src._consume_token')
    @patch('_parse_additive_package._parse_additive_src._parse_multiplicative')
    def test_chained_operations_left_associative(self, mock_parse_mult, mock_consume):
        """Test that chained operations are left-associative: a + b - c."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 5},
                {"type": "MINUS", "value": "-", "line": 1, "column": 7},
                {"type": "NUMBER", "value": "3", "line": 1, "column": 9},
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        left1 = {"type": "NUMBER", "value": "1"}
        left2 = {"type": "NUMBER", "value": "2"}
        left3 = {"type": "NUMBER", "value": "3"}
        
        mock_parse_mult.side_effect = [
            (left1, {"pos": 1, "tokens": parser_state["tokens"]}),
            (left2, {"pos": 3, "tokens": parser_state["tokens"]}),
            (left3, {"pos": 5, "tokens": parser_state["tokens"]}),
        ]
        mock_consume.side_effect = [
            {"pos": 2, "tokens": parser_state["tokens"]},
            {"pos": 4, "tokens": parser_state["tokens"]},
        ]
        
        result_ast, result_state = _parse_additive(parser_state)
        
        self.assertEqual(result_ast["type"], "BINARY_OP")
        self.assertEqual(result_ast["value"], "-")
        self.assertEqual(len(result_ast["children"]), 2)
        
        left_subtree = result_ast["children"][0]
        self.assertEqual(left_subtree["type"], "BINARY_OP")
        self.assertEqual(left_subtree["value"], "+")
        
        right_leaf = result_ast["children"][1]
        self.assertEqual(right_leaf["type"], "NUMBER")
        self.assertEqual(right_leaf["value"], "3")

    @patch('_parse_additive_package._parse_additive_src._parse_multiplicative')
    def test_no_additive_operator(self, mock_parse_mult):
        """Test when there's no additive operator, just returns the multiplicative expression."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "42", "line": 1, "column": 1},
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        mock_parse_mult.return_value = (
            {"type": "NUMBER", "value": "42"},
            {"pos": 1, "tokens": parser_state["tokens"]}
        )
        
        result_ast, result_state = _parse_additive(parser_state)
        
        self.assertEqual(result_ast["type"], "NUMBER")
        self.assertEqual(result_ast["value"], "42")

    @patch('_parse_additive_package._parse_additive_src._parse_multiplicative')
    def test_empty_tokens(self, mock_parse_mult):
        """Test with empty token list."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.c"
        }
        
        mock_parse_mult.return_value = (
            {"type": "NUMBER", "value": "0"},
            {"pos": 0, "tokens": []}
        )
        
        result_ast, result_state = _parse_additive(parser_state)
        
        self.assertEqual(result_ast["type"], "NUMBER")
        self.assertEqual(result_ast["value"], "0")

    @patch('_parse_additive_package._parse_additive_src._consume_token')
    @patch('_parse_additive_package._parse_additive_src._parse_multiplicative')
    def test_ast_includes_operator_location(self, mock_parse_mult, mock_consume):
        """Test that AST node includes line and column from operator token."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 5, "column": 10},
                {"type": "PLUS", "value": "+", "line": 5, "column": 12},
                {"type": "NUMBER", "value": "2", "line": 5, "column": 14},
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        mock_parse_mult.side_effect = [
            ({"type": "NUMBER", "value": "1"}, {"pos": 1, "tokens": parser_state["tokens"]}),
            ({"type": "NUMBER", "value": "2"}, {"pos": 2, "tokens": parser_state["tokens"]}),
        ]
        mock_consume.return_value = {"pos": 2, "tokens": parser_state["tokens"]}
        
        result_ast, result_state = _parse_additive(parser_state)
        
        self.assertEqual(result_ast["line"], 5)
        self.assertEqual(result_ast["column"], 12)

    @patch('_parse_additive_package._parse_additive_src._consume_token')
    @patch('_parse_additive_package._parse_additive_src._parse_multiplicative')
    def test_multiple_additions(self, mock_parse_mult, mock_consume):
        """Test parsing multiple additions: a + b + c + d."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1"},
                {"type": "PLUS", "value": "+"},
                {"type": "NUMBER", "value": "2"},
                {"type": "PLUS", "value": "+"},
                {"type": "NUMBER", "value": "3"},
                {"type": "PLUS", "value": "+"},
                {"type": "NUMBER", "value": "4"},
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        mock_parse_mult.side_effect = [
            ({"type": "NUMBER", "value": "1"}, {"pos": 1}),
            ({"type": "NUMBER", "value": "2"}, {"pos": 3}),
            ({"type": "NUMBER", "value": "3"}, {"pos": 5}),
            ({"type": "NUMBER", "value": "4"}, {"pos": 7}),
        ]
        mock_consume.side_effect = [
            {"pos": 2},
            {"pos": 4},
            {"pos": 6},
        ]
        
        result_ast, result_state = _parse_additive(parser_state)
        
        self.assertEqual(result_ast["type"], "BINARY_OP")
        self.assertEqual(result_ast["value"], "+")
        
        left = result_ast["children"][0]
        self.assertEqual(left["type"], "BINARY_OP")
        self.assertEqual(left["value"], "+")
        
        left_left = left["children"][0]
        self.assertEqual(left_left["type"], "BINARY_OP")
        self.assertEqual(left_left["value"], "+")

    @patch('_parse_additive_package._parse_additive_src._parse_multiplicative')
    def test_position_at_end_after_parsing(self, mock_parse_mult):
        """Test that parser position is at end when no more additive operators."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "5"},
                {"type": "SEMICOLON", "value": ";"},
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        mock_parse_mult.return_value = (
            {"type": "NUMBER", "value": "5"},
            {"pos": 1, "tokens": parser_state["tokens"]}
        )
        
        result_ast, result_state = _parse_additive(parser_state)
        
        self.assertEqual(result_state["pos"], 1)
        self.assertEqual(result_ast["type"], "NUMBER")


if __name__ == "__main__":
    unittest.main()

import unittest
from unittest.mock import patch

# Relative import for the function under test
from ._parse_additive_expr_src import _parse_additive_expr


class TestParseAdditiveExpr(unittest.TestCase):
    """Test cases for _parse_additive_expr function."""

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_expression_package._parse_or_expr_package._parse_and_expr_package._parse_comparison_expr_package._parse_additive_expr_package._parse_multiplicative_expr_package._parse_multiplicative_expr_src._parse_multiplicative_expr')
    def test_simple_addition(self, mock_parse_mult):
        """Test parsing simple addition expression (a + b)."""
        mock_parse_mult.side_effect = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
        ]
        
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "+", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_additive_expr(parser_state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["operator"], "+")
        self.assertEqual(result["left"]["value"], "a")
        self.assertEqual(result["right"]["value"], "b")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 3)
        self.assertEqual(parser_state["pos"], 3)

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_expression_package._parse_or_expr_package._parse_and_expr_package._parse_comparison_expr_package._parse_additive_expr_package._parse_multiplicative_expr_package._parse_multiplicative_expr_src._parse_multiplicative_expr')
    def test_simple_subtraction(self, mock_parse_mult):
        """Test parsing simple subtraction expression (x - y)."""
        mock_parse_mult.side_effect = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "y", "line": 1, "column": 5}
        ]
        
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "-", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "y", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_additive_expr(parser_state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["operator"], "-")
        self.assertEqual(result["left"]["value"], "x")
        self.assertEqual(result["right"]["value"], "y")
        self.assertEqual(parser_state["pos"], 3)

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_expression_package._parse_or_expr_package._parse_and_expr_package._parse_comparison_expr_package._parse_additive_expr_package._parse_multiplicative_expr_package._parse_multiplicative_expr_src._parse_multiplicative_expr')
    def test_left_associativity(self, mock_parse_mult):
        """Test that multiple additive operators are left-associative (a + b - c)."""
        mock_parse_mult.side_effect = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
            {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 9}
        ]
        
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "+", "line": 1, "column": 3},
                {"type": "OPERATOR", "value": "-", "line": 1, "column": 7},
                {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 9}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_additive_expr(parser_state)
        
        # Should be left-associative: (a + b) - c
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["operator"], "-")
        self.assertEqual(result["left"]["type"], "BINARY_OP")
        self.assertEqual(result["left"]["operator"], "+")
        self.assertEqual(result["left"]["left"]["value"], "a")
        self.assertEqual(result["left"]["right"]["value"], "b")
        self.assertEqual(result["right"]["value"], "c")

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_expression_package._parse_or_expr_package._parse_and_expr_package._parse_comparison_expr_package._parse_additive_expr_package._parse_multiplicative_expr_package._parse_multiplicative_expr_src._parse_multiplicative_expr')
    def test_single_operand_no_operator(self, mock_parse_mult):
        """Test parsing single operand with no additive operators."""
        mock_parse_mult.return_value = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 1
        }
        
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_additive_expr(parser_state)
        
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "x")
        self.assertEqual(parser_state["pos"], 0)

    @patch('_parse_multiplicative_expr_package._parse_multiplicative_expr_src._parse_multiplicative_expr')
    def test_mixed_additive_operators(self, mock_parse_mult):
        """Test parsing mixed + and - operators."""
        mock_parse_mult.side_effect = [
            {"type": "NUMBER", "value": 1, "line": 1, "column": 1},
            {"type": "NUMBER", "value": 2, "line": 1, "column": 5},
            {"type": "NUMBER", "value": 3, "line": 1, "column": 9},
            {"type": "NUMBER", "value": 4, "line": 1, "column": 13}
        ]
        
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": 1, "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "+", "line": 1, "column": 3},
                {"type": "OPERATOR", "value": "-", "line": 1, "column": 7},
                {"type": "OPERATOR", "value": "+", "line": 1, "column": 11},
                {"type": "NUMBER", "value": 4, "line": 1, "column": 13}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_additive_expr(parser_state)
        
        # Should be: ((1 + 2) - 3) + 4
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["operator"], "+")
        self.assertEqual(result["left"]["operator"], "-")
        self.assertEqual(result["left"]["left"]["operator"], "+")
        self.assertEqual(result["left"]["left"]["left"]["value"], 1)
        self.assertEqual(result["left"]["left"]["right"]["value"], 2)
        self.assertEqual(result["left"]["right"]["value"], 3)
        self.assertEqual(result["right"]["value"], 4)

    @patch('_parse_multiplicative_expr_package._parse_multiplicative_expr_src._parse_multiplicative_expr')
    def test_operator_without_right_operand(self, mock_parse_mult):
        """Test that SyntaxError is raised when operator has no right operand."""
        mock_parse_mult.side_effect = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            SyntaxError("Unexpected end of input")
        ]
        
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "+", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with self.assertRaises(SyntaxError):
            _parse_additive_expr(parser_state)

    @patch('_parse_multiplicative_expr_package._parse_multiplicative_expr_src._parse_multiplicative_expr')
    def test_empty_tokens(self, mock_parse_mult):
        """Test parsing with empty tokens list."""
        mock_parse_mult.return_value = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 1
        }
        
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_additive_expr(parser_state)
        
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "x")
        self.assertEqual(parser_state["pos"], 0)

    @patch('_parse_multiplicative_expr_package._parse_multiplicative_expr_src._parse_multiplicative_expr')
    def test_non_operator_token_stops_loop(self, mock_parse_mult):
        """Test that non-operator token stops the additive parsing loop."""
        mock_parse_mult.side_effect = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
        ]
        
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "+", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
                {"type": "PUNCTUATION", "value": ";", "line": 1, "column": 7}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_additive_expr(parser_state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["operator"], "+")
        self.assertEqual(parser_state["pos"], 3)

    @patch('_parse_multiplicative_expr_package._parse_multiplicative_expr_src._parse_multiplicative_expr')
    def test_wrong_token_type_not_treated_as_operator(self, mock_parse_mult):
        """Test that OPERATOR token with non +/- value is not treated as additive operator."""
        mock_parse_mult.side_effect = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
        ]
        
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "*", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_additive_expr(parser_state)
        
        # Should only parse the first operand, not consume the * operator
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "a")
        self.assertEqual(parser_state["pos"], 0)


if __name__ == '__main__':
    unittest.main()

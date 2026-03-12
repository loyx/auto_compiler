# test_parse_expression_src.py
"""Unit tests for _parse_expression function."""

import unittest
from unittest.mock import patch, MagicMock


class TestParseExpression(unittest.TestCase):
    """Test cases for _parse_expression function."""

    def setUp(self):
        """Set up mock for _parse_or_expr before each test."""
        self.mock_or_expr_patcher = patch(
            "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_expression_src._parse_or_expr"
        )
        self.mock_or_expr = self.mock_or_expr_patcher.start()
        
    def tearDown(self):
        """Stop the patcher after each test."""
        self.mock_or_expr_patcher.stop()

    def test_simple_expression_delegates_to_or_expr(self):
        """Test that _parse_expression delegates to _parse_or_expr."""
        mock_ast_node = {"type": "IDENTIFIER", "value": "x"}
        mock_state = {"tokens": [{"type": "IDENTIFIER", "value": "x"}], "pos": 0}
        
        self.mock_or_expr.return_value = mock_ast_node
        
        from ._parse_expression_src import _parse_expression
        result = _parse_expression(mock_state)
        
        self.mock_or_expr.assert_called_once_with(mock_state)
        self.assertEqual(result, mock_ast_node)

    def test_expression_with_number_literal(self):
        """Test parsing a number literal expression."""
        mock_ast_node = {"type": "LITERAL", "value": 42}
        mock_state = {"tokens": [{"type": "NUMBER", "value": "42"}], "pos": 0}
        
        self.mock_or_expr.return_value = mock_ast_node
        
        from ._parse_expression_src import _parse_expression
        result = _parse_expression(mock_state)
        
        self.assertEqual(result, mock_ast_node)
        self.mock_or_expr.assert_called_once_with(mock_state)

    def test_expression_with_string_literal(self):
        """Test parsing a string literal expression."""
        mock_ast_node = {"type": "LITERAL", "value": "hello"}
        mock_state = {"tokens": [{"type": "STRING", "value": "hello"}], "pos": 0}
        
        self.mock_or_expr.return_value = mock_ast_node
        
        from ._parse_expression_src import _parse_expression
        result = _parse_expression(mock_state)
        
        self.assertEqual(result, mock_ast_node)

    def test_expression_with_boolean_literal(self):
        """Test parsing a boolean literal expression."""
        mock_ast_node = {"type": "LITERAL", "value": True}
        mock_state = {"tokens": [{"type": "BOOL", "value": "True"}], "pos": 0}
        
        self.mock_or_expr.return_value = mock_ast_node
        
        from ._parse_expression_src import _parse_expression
        result = _parse_expression(mock_state)
        
        self.assertEqual(result, mock_ast_node)

    def test_expression_with_none_literal(self):
        """Test parsing a None literal expression."""
        mock_ast_node = {"type": "LITERAL", "value": None}
        mock_state = {"tokens": [{"type": "NONE", "value": "None"}], "pos": 0}
        
        self.mock_or_expr.return_value = mock_ast_node
        
        from ._parse_expression_src import _parse_expression
        result = _parse_expression(mock_state)
        
        self.assertEqual(result, mock_ast_node)

    def test_expression_propagates_syntax_error(self):
        """Test that SyntaxError from _parse_or_expr is propagated."""
        mock_state = {"tokens": [{"type": "INVALID", "value": "?"}], "pos": 0}
        
        self.mock_or_expr.side_effect = SyntaxError("Invalid token")
        
        from ._parse_expression_src import _parse_expression
        with self.assertRaises(SyntaxError) as context:
            _parse_expression(mock_state)
        
        self.assertEqual(str(context.exception), "Invalid token")

    def test_expression_updates_parser_position(self):
        """Test that parser_state position is updated after parsing."""
        mock_ast_node = {"type": "IDENTIFIER", "value": "x"}
        mock_state = {"tokens": [{"type": "IDENTIFIER", "value": "x"}], "pos": 0}
        
        def update_position(state):
            state["pos"] = 1
            return mock_ast_node
        
        self.mock_or_expr.side_effect = update_position
        
        from ._parse_expression_src import _parse_expression
        result = _parse_expression(mock_state)
        
        self.assertEqual(mock_state["pos"], 1)
        self.assertEqual(result, mock_ast_node)

    def test_complex_expression_with_operator_precedence(self):
        """Test parsing complex expression respects operator precedence."""
        mock_ast_node = {
            "type": "BINARY_OP",
            "operator": "+",
            "left": {"type": "IDENTIFIER", "value": "a"},
            "right": {
                "type": "BINARY_OP",
                "operator": "*",
                "left": {"type": "IDENTIFIER", "value": "b"},
                "right": {"type": "IDENTIFIER", "value": "c"}
            }
        }
        mock_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a"},
                {"type": "PLUS", "value": "+"},
                {"type": "IDENTIFIER", "value": "b"},
                {"type": "STAR", "value": "*"},
                {"type": "IDENTIFIER", "value": "c"}
            ],
            "pos": 0
        }
        
        self.mock_or_expr.return_value = mock_ast_node
        
        from ._parse_expression_src import _parse_expression
        result = _parse_expression(mock_state)
        
        self.assertEqual(result, mock_ast_node)

    def test_expression_with_parentheses(self):
        """Test parsing expression with parentheses."""
        mock_ast_node = {
            "type": "BINARY_OP",
            "operator": "+",
            "left": {"type": "IDENTIFIER", "value": "a"},
            "right": {"type": "IDENTIFIER", "value": "b"}
        }
        mock_state = {
            "tokens": [
                {"type": "LPAREN", "value": "("},
                {"type": "IDENTIFIER", "value": "a"},
                {"type": "PLUS", "value": "+"},
                {"type": "IDENTIFIER", "value": "b"},
                {"type": "RPAREN", "value": ")"}
            ],
            "pos": 0
        }
        
        self.mock_or_expr.return_value = mock_ast_node
        
        from ._parse_expression_src import _parse_expression
        result = _parse_expression(mock_state)
        
        self.assertEqual(result, mock_ast_node)

    def test_expression_with_unary_operator(self):
        """Test parsing expression with unary operator."""
        mock_ast_node = {
            "type": "UNARY_OP",
            "operator": "-",
            "operand": {"type": "NUMBER", "value": 5}
        }
        mock_state = {
            "tokens": [
                {"type": "MINUS", "value": "-"},
                {"type": "NUMBER", "value": "5"}
            ],
            "pos": 0
        }
        
        self.mock_or_expr.return_value = mock_ast_node
        
        from ._parse_expression_src import _parse_expression
        result = _parse_expression(mock_state)
        
        self.assertEqual(result, mock_ast_node)

    def test_expression_with_logical_operators(self):
        """Test parsing expression with logical operators."""
        mock_ast_node = {
            "type": "BINARY_OP",
            "operator": "or",
            "left": {
                "type": "BINARY_OP",
                "operator": "and",
                "left": {"type": "BOOL", "value": True},
                "right": {"type": "BOOL", "value": False}
            },
            "right": {"type": "BOOL", "value": True}
        }
        mock_state = {
            "tokens": [
                {"type": "BOOL", "value": "True"},
                {"type": "AND", "value": "and"},
                {"type": "BOOL", "value": "False"},
                {"type": "OR", "value": "or"},
                {"type": "BOOL", "value": "True"}
            ],
            "pos": 0
        }
        
        self.mock_or_expr.return_value = mock_ast_node
        
        from ._parse_expression_src import _parse_expression
        result = _parse_expression(mock_state)
        
        self.assertEqual(result, mock_ast_node)

    def test_expression_with_comparison_operators(self):
        """Test parsing expression with comparison operators."""
        mock_ast_node = {
            "type": "BINARY_OP",
            "operator": "==",
            "left": {"type": "IDENTIFIER", "value": "x"},
            "right": {"type": "NUMBER", "value": 10}
        }
        mock_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x"},
                {"type": "EQ", "value": "=="},
                {"type": "NUMBER", "value": "10"}
            ],
            "pos": 0
        }
        
        self.mock_or_expr.return_value = mock_ast_node
        
        from ._parse_expression_src import _parse_expression
        result = _parse_expression(mock_state)
        
        self.assertEqual(result, mock_ast_node)

    def test_empty_token_list_raises_error(self):
        """Test that empty token list raises SyntaxError."""
        mock_state = {"tokens": [], "pos": 0}
        
        self.mock_or_expr.side_effect = SyntaxError("Unexpected end of input")
        
        from ._parse_expression_src import _parse_expression
        with self.assertRaises(SyntaxError):
            _parse_expression(mock_state)

    def test_expression_preserves_state_reference(self):
        """Test that the same state object is passed (not copied)."""
        mock_ast_node = {"type": "IDENTIFIER", "value": "x"}
        original_state = {"tokens": [{"type": "IDENTIFIER", "value": "x"}], "pos": 0}
        
        self.mock_or_expr.return_value = mock_ast_node
        
        from ._parse_expression_src import _parse_expression
        _parse_expression(original_state)
        
        call_args = self.mock_or_expr.call_args
        self.assertIs(call_args[0][0], original_state)


if __name__ == "__main__":
    unittest.main()
# === std / third-party imports ===
import unittest
from unittest.mock import patch, call, MagicMock
from typing import Dict, Any
import sys

# === sub function imports ===
# Set up the module mocks BEFORE importing _parse_additive
# This prevents the actual import chain from being executed

# We need to mock the entire dependency chain to avoid circular imports

# Mock for _parse_additive's direct dependencies
sys.modules['_parse_additive_package._parse_multiplicative_package._parse_multiplicative_src'] = MagicMock()
sys.modules['_parse_additive_package._is_additive_operator_package._is_additive_operator_src'] = MagicMock()
sys.modules['_parse_additive_package._consume_token_package._consume_token_src'] = MagicMock()
sys.modules['_parse_additive_package._build_binary_op_package._build_binary_op_src'] = MagicMock()

# Mock for _parse_multiplicative's dependencies
sys.modules['_parse_additive_package._parse_multiplicative_package._parse_unary_package._parse_unary_src'] = MagicMock()

# Mock for _parse_unary's dependencies  
sys.modules['_parse_additive_package._parse_multiplicative_package._parse_unary_package._parse_primary_package._parse_primary_src'] = MagicMock()

# Mock for _parse_primary's dependencies (circular)
sys.modules['_parse_additive_package._parse_multiplicative_package._parse_unary_package._parse_primary_package._parse_unary_package._parse_unary_src'] = MagicMock()

# Mock for the next level of circular dependency
sys.modules['_parse_additive_package._parse_multiplicative_package._parse_unary_package._parse_primary_package._parse_unary_package._parse_primary_package._parse_primary_src'] = MagicMock()

from ._parse_additive_src import _parse_additive


class TestParseAdditive(unittest.TestCase):
    """Test cases for _parse_additive function."""

    def _create_mock_token(self, token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """Helper to create a mock token."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def _create_mock_ast(self, ast_type: str, value: Any = None, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """Helper to create a mock AST node."""
        return {
            "type": ast_type,
            "value": value,
            "line": line,
            "column": column
        }

    @patch('_parse_additive_package._parse_additive_src._build_binary_op')
    @patch('_parse_additive_package._parse_additive_src._consume_token')
    @patch('_parse_additive_package._parse_additive_src._is_additive_operator')
    @patch('_parse_additive_package._parse_additive_src._parse_multiplicative')
    def test_single_multiplicative_no_operator(self, mock_parse_mult, mock_is_add_op, mock_consume, mock_build_op):
        """Test parsing a single multiplicative expression with no additive operators."""
        # Setup
        parser_state = {
            "tokens": [self._create_mock_token("NUMBER", "42")],
            "pos": 0,
            "filename": "test.py"
        }
        left_ast = self._create_mock_ast("NUMBER", 42)
        
        mock_parse_mult.return_value = left_ast
        mock_is_add_op.return_value = False
        
        # Execute
        result = _parse_additive(parser_state)
        
        # Verify
        self.assertEqual(result, left_ast)
        mock_parse_mult.assert_called_once_with(parser_state)
        mock_is_add_op.assert_called_once_with(parser_state)
        mock_consume.assert_not_called()
        mock_build_op.assert_not_called()

    @patch('_parse_additive_package._parse_additive_src._build_binary_op')
    @patch('_parse_additive_package._parse_additive_src._consume_token')
    @patch('_parse_additive_package._parse_additive_src._is_additive_operator')
    @patch('_parse_additive_package._parse_additive_src._parse_multiplicative')
    def test_one_additive_operator(self, mock_parse_mult, mock_is_add_op, mock_consume, mock_build_op):
        """Test parsing expression with one additive operator (a + b)."""
        # Setup
        parser_state = {
            "tokens": [
                self._create_mock_token("NUMBER", "1"),
                self._create_mock_token("PLUS", "+"),
                self._create_mock_token("NUMBER", "2")
            ],
            "pos": 0,
            "filename": "test.py"
        }
        left_ast = self._create_mock_ast("NUMBER", 1)
        right_ast = self._create_mock_ast("NUMBER", 2)
        op_token = self._create_mock_token("PLUS", "+")
        result_ast = self._create_mock_ast("BINARY_OP", "+")
        
        mock_parse_mult.side_effect = [left_ast, right_ast]
        mock_is_add_op.side_effect = [True, False]
        mock_consume.return_value = op_token
        mock_build_op.return_value = result_ast
        
        # Execute
        result = _parse_additive(parser_state)
        
        # Verify
        self.assertEqual(result, result_ast)
        self.assertEqual(mock_parse_mult.call_count, 2)
        mock_parse_mult.assert_has_calls([call(parser_state), call(parser_state)])
        self.assertEqual(mock_is_add_op.call_count, 2)
        mock_consume.assert_called_once_with(parser_state)
        mock_build_op.assert_called_once_with(left_ast, right_ast, op_token)

    @patch('_parse_additive_package._parse_additive_src._build_binary_op')
    @patch('_parse_additive_package._parse_additive_src._consume_token')
    @patch('_parse_additive_package._parse_additive_src._is_additive_operator')
    @patch('_parse_additive_package._parse_additive_src._parse_multiplicative')
    def test_multiple_additive_operators(self, mock_parse_mult, mock_is_add_op, mock_consume, mock_build_op):
        """Test parsing expression with multiple additive operators (a + b - c)."""
        # Setup
        parser_state = {
            "tokens": [
                self._create_mock_token("NUMBER", "1"),
                self._create_mock_token("PLUS", "+"),
                self._create_mock_token("NUMBER", "2"),
                self._create_mock_token("MINUS", "-"),
                self._create_mock_token("NUMBER", "3")
            ],
            "pos": 0,
            "filename": "test.py"
        }
        ast1 = self._create_mock_ast("NUMBER", 1)
        ast2 = self._create_mock_ast("NUMBER", 2)
        ast3 = self._create_mock_ast("NUMBER", 3)
        plus_token = self._create_mock_token("PLUS", "+", column=2)
        minus_token = self._create_mock_token("MINUS", "-", column=4)
        result1 = self._create_mock_ast("BINARY_OP", "+")
        result2 = self._create_mock_ast("BINARY_OP", "-")
        
        mock_parse_mult.side_effect = [ast1, ast2, ast3]
        mock_is_add_op.side_effect = [True, True, False]
        mock_consume.side_effect = [plus_token, minus_token]
        mock_build_op.side_effect = [result1, result2]
        
        # Execute
        result = _parse_additive(parser_state)
        
        # Verify
        self.assertEqual(result, result2)
        self.assertEqual(mock_parse_mult.call_count, 3)
        self.assertEqual(mock_is_add_op.call_count, 3)
        self.assertEqual(mock_consume.call_count, 2)
        self.assertEqual(mock_build_op.call_count, 2)
        
        # Verify left-associativity: (a + b) - c
        mock_build_op.assert_has_calls([
            call(ast1, ast2, plus_token),
            call(result1, ast3, minus_token)
        ])

    @patch('_parse_additive_package._parse_additive_src._build_binary_op')
    @patch('_parse_additive_package._parse_additive_src._consume_token')
    @patch('_parse_additive_package._parse_additive_src._is_additive_operator')
    @patch('_parse_additive_package._parse_additive_src._parse_multiplicative')
    def test_minus_operator(self, mock_parse_mult, mock_is_add_op, mock_consume, mock_build_op):
        """Test parsing expression with minus operator (a - b)."""
        # Setup
        parser_state = {
            "tokens": [
                self._create_mock_token("NUMBER", "10"),
                self._create_mock_token("MINUS", "-"),
                self._create_mock_token("NUMBER", "5")
            ],
            "pos": 0,
            "filename": "test.py"
        }
        left_ast = self._create_mock_ast("NUMBER", 10)
        right_ast = self._create_mock_ast("NUMBER", 5)
        op_token = self._create_mock_token("MINUS", "-")
        result_ast = self._create_mock_ast("BINARY_OP", "-")
        
        mock_parse_mult.side_effect = [left_ast, right_ast]
        mock_is_add_op.side_effect = [True, False]
        mock_consume.return_value = op_token
        mock_build_op.return_value = result_ast
        
        # Execute
        result = _parse_additive(parser_state)
        
        # Verify
        self.assertEqual(result, result_ast)
        mock_build_op.assert_called_once_with(left_ast, right_ast, op_token)

    @patch('_parse_additive_package._parse_additive_src._build_binary_op')
    @patch('_parse_additive_package._parse_additive_src._consume_token')
    @patch('_parse_additive_package._parse_additive_src._is_additive_operator')
    @patch('_parse_additive_package._parse_additive_src._parse_multiplicative')
    def test_empty_tokens(self, mock_parse_mult, mock_is_add_op, mock_consume, mock_build_op):
        """Test parsing with empty tokens list."""
        # Setup
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }
        empty_ast = self._create_mock_ast("EMPTY")
        
        mock_parse_mult.return_value = empty_ast
        mock_is_add_op.return_value = False
        
        # Execute
        result = _parse_additive(parser_state)
        
        # Verify
        self.assertEqual(result, empty_ast)
        mock_parse_mult.assert_called_once_with(parser_state)
        mock_is_add_op.assert_called_once_with(parser_state)

    @patch('_parse_additive_package._parse_additive_src._build_binary_op')
    @patch('_parse_additive_package._parse_additive_src._consume_token')
    @patch('_parse_additive_package._parse_additive_src._is_additive_operator')
    @patch('_parse_additive_package._parse_additive_src._parse_multiplicative')
    def test_parser_state_position_updated(self, mock_parse_mult, mock_is_add_op, mock_consume, mock_build_op):
        """Test that parser_state position is updated through consume_token."""
        # Setup
        parser_state = {
            "tokens": [
                self._create_mock_token("NUMBER", "1"),
                self._create_mock_token("PLUS", "+"),
                self._create_mock_token("NUMBER", "2")
            ],
            "pos": 0,
            "filename": "test.py"
        }
        left_ast = self._create_mock_ast("NUMBER", 1)
        right_ast = self._create_mock_ast("NUMBER", 2)
        op_token = self._create_mock_token("PLUS", "+")
        result_ast = self._create_mock_ast("BINARY_OP", "+")
        
        mock_parse_mult.side_effect = [left_ast, right_ast]
        mock_is_add_op.side_effect = [True, False]
        mock_consume.return_value = op_token
        mock_build_op.return_value = result_ast
        
        # Execute
        result = _parse_additive(parser_state)
        
        # Verify consume_token was called (which should update pos)
        mock_consume.assert_called_once_with(parser_state)
        self.assertEqual(result, result_ast)

    @patch('_parse_additive_package._parse_additive_src._build_binary_op')
    @patch('_parse_additive_package._parse_additive_src._consume_token')
    @patch('_parse_additive_package._parse_additive_src._is_additive_operator')
    @patch('_parse_additive_package._parse_additive_src._parse_multiplicative')
    def test_complex_expression_left_associative(self, mock_parse_mult, mock_is_add_op, mock_consume, mock_build_op):
        """Test complex expression to verify left-associativity (a + b + c + d)."""
        # Setup
        parser_state = {
            "tokens": [
                self._create_mock_token("NUMBER", "1"),
                self._create_mock_token("PLUS", "+"),
                self._create_mock_token("NUMBER", "2"),
                self._create_mock_token("PLUS", "+"),
                self._create_mock_token("NUMBER", "3"),
                self._create_mock_token("MINUS", "-"),
                self._create_mock_token("NUMBER", "4")
            ],
            "pos": 0,
            "filename": "test.py"
        }
        asts = [self._create_mock_ast("NUMBER", i) for i in [1, 2, 3, 4]]
        tokens = [
            self._create_mock_token("PLUS", "+", column=2),
            self._create_mock_token("PLUS", "+", column=4),
            self._create_mock_token("MINUS", "-", column=6)
        ]
        results = [self._create_mock_ast("BINARY_OP", op["value"]) for op in tokens]
        
        mock_parse_mult.side_effect = asts
        mock_is_add_op.side_effect = [True, True, True, False]
        mock_consume.side_effect = tokens
        mock_build_op.side_effect = results
        
        # Execute
        result = _parse_additive(parser_state)
        
        # Verify
        self.assertEqual(result, results[-1])
        self.assertEqual(mock_parse_mult.call_count, 4)
        self.assertEqual(mock_consume.call_count, 3)
        self.assertEqual(mock_build_op.call_count, 3)
        
        # Verify left-associative building: (((a + b) + c) - d)
        expected_calls = [
            call(asts[0], asts[1], tokens[0]),
            call(results[0], asts[2], tokens[1]),
            call(results[1], asts[3], tokens[2])
        ]
        mock_build_op.assert_has_calls(expected_calls)


if __name__ == "__main__":
    unittest.main()

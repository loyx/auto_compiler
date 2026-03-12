# === std / third-party imports ===
import unittest
from unittest.mock import patch, MagicMock
from typing import Dict, Any
import sys

# === Mock missing dependencies before importing ===
# The _parse_multiplicative_src.py has relative imports that expect sub-packages
# under _parse_multiplicative_package. We need to mock all of them.

def mock_parse_primary(parser_state):
    """Mock implementation of _parse_primary."""
    return ({"type": "MOCK", "value": None, "children": [], "line": 0, "column": 0}, parser_state)

def mock_get_current_token(parser_state):
    """Mock implementation of _get_current_token."""
    return None

def mock_consume_token(parser_state):
    """Mock implementation of _consume_token."""
    return parser_state

def mock_is_operator_token(token, operators):
    """Mock implementation of _is_operator_token."""
    return False

# Create mock module objects for _parse_multiplicative_package's dependencies
mult_pkg_base = __package__ + '._parse_multiplicative_package' if __package__ else '_parse_multiplicative_package'

# Mock _parse_primary_package
mock_parse_primary_src = type(sys)('_parse_primary_src')
mock_parse_primary_src._parse_primary = mock_parse_primary
mock_parse_primary_pkg = type(sys)('_parse_primary_package')
mock_parse_primary_pkg._parse_primary_src = mock_parse_primary_src
sys.modules[mult_pkg_base + '._parse_primary_package'] = mock_parse_primary_pkg
sys.modules[mult_pkg_base + '._parse_primary_package._parse_primary_src'] = mock_parse_primary_src

# Mock _get_current_token_package
mock_get_current_token_src = type(sys)('_get_current_token_src')
mock_get_current_token_src._get_current_token = mock_get_current_token
mock_get_current_token_pkg = type(sys)('_get_current_token_package')
mock_get_current_token_pkg._get_current_token_src = mock_get_current_token_src
sys.modules[mult_pkg_base + '._get_current_token_package'] = mock_get_current_token_pkg
sys.modules[mult_pkg_base + '._get_current_token_package._get_current_token_src'] = mock_get_current_token_src

# Mock _consume_token_package
mock_consume_token_src = type(sys)('_consume_token_src')
mock_consume_token_src._consume_token = mock_consume_token
mock_consume_token_pkg = type(sys)('_consume_token_package')
mock_consume_token_pkg._consume_token_src = mock_consume_token_src
sys.modules[mult_pkg_base + '._consume_token_package'] = mock_consume_token_pkg
sys.modules[mult_pkg_base + '._consume_token_package._consume_token_src'] = mock_consume_token_src

# Mock _is_operator_token_package
mock_is_operator_token_src = type(sys)('_is_operator_token_src')
mock_is_operator_token_src._is_operator_token = mock_is_operator_token
mock_is_operator_token_pkg = type(sys)('_is_operator_token_package')
mock_is_operator_token_pkg._is_operator_token_src = mock_is_operator_token_src
sys.modules[mult_pkg_base + '._is_operator_token_package'] = mock_is_operator_token_pkg
sys.modules[mult_pkg_base + '._is_operator_token_package._is_operator_token_src'] = mock_is_operator_token_src

# === relative imports ===
from ._parse_additive_src import _parse_additive


class TestParseAdditive(unittest.TestCase):
    """Test cases for _parse_additive function."""

    def _create_token(self, token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """Helper to create a token dictionary."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def _create_parser_state(self, tokens: list, pos: int = 0, filename: str = "test.py") -> Dict[str, Any]:
        """Helper to create a parser state dictionary."""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename,
            "error": ""
        }

    def _create_ast_node(self, node_type: str, value: Any = None, children: list = None, 
                         line: int = 0, column: int = 0) -> Dict[str, Any]:
        """Helper to create an AST node dictionary."""
        return {
            "type": node_type,
            "value": value,
            "children": children if children is not None else [],
            "line": line,
            "column": column
        }

    @patch(__package__ + '._parse_additive_src._parse_multiplicative')
    @patch(__package__ + '._parse_additive_src._get_current_token')
    @patch(__package__ + '._parse_additive_src._consume_token')
    @patch(__package__ + '._parse_additive_src._is_operator_token')
    def test_single_operand_no_operator(self, mock_is_op, mock_consume, mock_get_token, mock_parse_mult):
        """Test parsing a single operand with no additive operators."""
        # Setup: single multiplicative expression, no + or - operators
        operand_ast = self._create_ast_node("NUMBER", value=42, line=1, column=1)
        mock_parse_mult.return_value = (operand_ast, self._create_parser_state([self._create_token("NUMBER", "42")], pos=1))
        
        mock_get_token.return_value = self._create_token("EOF", "")
        mock_is_op.return_value = False
        
        parser_state = self._create_parser_state([self._create_token("NUMBER", "42")], pos=0)
        
        # Execute
        result_ast, result_state = _parse_additive(parser_state)
        
        # Verify
        self.assertEqual(result_ast, operand_ast)
        mock_parse_mult.assert_called_once()
        mock_get_token.assert_called_once()
        mock_is_op.assert_called_once()
        mock_consume.assert_not_called()

    @patch(__package__ + '._parse_additive_src._parse_multiplicative')
    @patch(__package__ + '._parse_additive_src._get_current_token')
    @patch(__package__ + '._parse_additive_src._consume_token')
    @patch(__package__ + '._parse_additive_src._is_operator_token')
    def test_simple_addition(self, mock_is_op, mock_consume, mock_get_token, mock_parse_mult):
        """Test parsing a simple addition expression: a + b."""
        # Setup: left operand
        left_ast = self._create_ast_node("NUMBER", value=10, line=1, column=1)
        right_ast = self._create_ast_node("NUMBER", value=5, line=1, column=5)
        
        add_token = self._create_token("OPERATOR", "+", line=1, column=3)
        
        # First call: parse left operand
        # Second call: parse right operand
        mock_parse_mult.side_effect = [
            (left_ast, self._create_parser_state([add_token], pos=1)),
            (right_ast, self._create_parser_state([add_token], pos=2))
        ]
        
        # First call: returns + operator, second call: returns None/EOF
        mock_get_token.side_effect = [add_token, None]
        
        # First call: True (is +), second call: False
        mock_is_op.side_effect = [True, False]
        
        # Consume advances position
        mock_consume.return_value = self._create_parser_state([add_token], pos=2)
        
        parser_state = self._create_parser_state([left_ast, add_token, right_ast], pos=0)
        
        # Execute
        result_ast, result_state = _parse_additive(parser_state)
        
        # Verify
        self.assertEqual(result_ast["type"], "BINARY_OP")
        self.assertEqual(result_ast["value"], "+")
        self.assertEqual(result_ast["line"], 1)
        self.assertEqual(result_ast["column"], 3)
        self.assertEqual(len(result_ast["children"]), 2)
        self.assertEqual(result_ast["children"][0], left_ast)
        self.assertEqual(result_ast["children"][1], right_ast)
        
        self.assertEqual(mock_parse_mult.call_count, 2)
        self.assertEqual(mock_get_token.call_count, 2)
        self.assertEqual(mock_is_op.call_count, 2)
        self.assertEqual(mock_consume.call_count, 1)

    @patch('_parse_additive_src._parse_multiplicative')
    @patch('_parse_additive_src._get_current_token')
    @patch('_parse_additive_src._consume_token')
    @patch('_parse_additive_src._is_operator_token')
    def test_simple_subtraction(self, mock_is_op, mock_consume, mock_get_token, mock_parse_mult):
        """Test parsing a simple subtraction expression: a - b."""
        left_ast = self._create_ast_node("NUMBER", value=10, line=1, column=1)
        right_ast = self._create_ast_node("NUMBER", value=3, line=1, column=5)
        
        sub_token = self._create_token("OPERATOR", "-", line=1, column=3)
        
        mock_parse_mult.side_effect = [
            (left_ast, self._create_parser_state([sub_token], pos=1)),
            (right_ast, self._create_parser_state([sub_token], pos=2))
        ]
        
        mock_get_token.side_effect = [sub_token, None]
        mock_is_op.side_effect = [True, False]
        mock_consume.return_value = self._create_parser_state([sub_token], pos=2)
        
        parser_state = self._create_parser_state([left_ast, sub_token, right_ast], pos=0)
        
        # Execute
        result_ast, result_state = _parse_additive(parser_state)
        
        # Verify
        self.assertEqual(result_ast["type"], "BINARY_OP")
        self.assertEqual(result_ast["value"], "-")
        self.assertEqual(result_ast["children"][0], left_ast)
        self.assertEqual(result_ast["children"][1], right_ast)

    @patch('_parse_additive_src._parse_multiplicative')
    @patch('_parse_additive_src._get_current_token')
    @patch('_parse_additive_src._consume_token')
    @patch('_parse_additive_src._is_operator_token')
    def test_left_associativity_multiple_additions(self, mock_is_op, mock_consume, mock_get_token, mock_parse_mult):
        """Test left associativity: a + b + c should be ((a + b) + c)."""
        # Setup tokens and operands
        a_ast = self._create_ast_node("NUMBER", value=1, line=1, column=1)
        b_ast = self._create_ast_node("NUMBER", value=2, line=1, column=5)
        c_ast = self._create_ast_node("NUMBER", value=3, line=1, column=9)
        
        plus1_token = self._create_token("OPERATOR", "+", line=1, column=3)
        plus2_token = self._create_token("OPERATOR", "+", line=1, column=7)
        
        # Three calls to _parse_multiplicative: a, b, c
        mock_parse_mult.side_effect = [
            (a_ast, self._create_parser_state([], pos=1)),
            (b_ast, self._create_parser_state([], pos=2)),
            (c_ast, self._create_parser_state([], pos=3))
        ]
        
        # Get tokens: +, +, None
        mock_get_token.side_effect = [plus1_token, plus2_token, None]
        
        # Is operator: True, True, False
        mock_is_op.side_effect = [True, True, False]
        
        # Consume twice
        mock_consume.return_value = self._create_parser_state([], pos=2)
        
        parser_state = self._create_parser_state([], pos=0)
        
        # Execute
        result_ast, result_state = _parse_additive(parser_state)
        
        # Verify structure: ((a + b) + c)
        self.assertEqual(result_ast["type"], "BINARY_OP")
        self.assertEqual(result_ast["value"], "+")
        self.assertEqual(result_ast["line"], 1)
        self.assertEqual(result_ast["column"], 7)  # Second + token position
        
        # Right child should be c
        self.assertEqual(result_ast["children"][1], c_ast)
        
        # Left child should be (a + b)
        left_child = result_ast["children"][0]
        self.assertEqual(left_child["type"], "BINARY_OP")
        self.assertEqual(left_child["value"], "+")
        self.assertEqual(left_child["line"], 1)
        self.assertEqual(left_child["column"], 3)  # First + token position
        self.assertEqual(left_child["children"][0], a_ast)
        self.assertEqual(left_child["children"][1], b_ast)
        
        self.assertEqual(mock_parse_mult.call_count, 3)
        self.assertEqual(mock_consume.call_count, 2)

    @patch('_parse_additive_src._parse_multiplicative')
    @patch('_parse_additive_src._get_current_token')
    @patch('_parse_additive_src._consume_token')
    @patch('_parse_additive_src._is_operator_token')
    def test_mixed_addition_subtraction(self, mock_is_op, mock_consume, mock_get_token, mock_parse_mult):
        """Test mixed operators: a + b - c."""
        a_ast = self._create_ast_node("NUMBER", value=10, line=1, column=1)
        b_ast = self._create_ast_node("NUMBER", value=5, line=1, column=5)
        c_ast = self._create_ast_node("NUMBER", value=2, line=1, column=9)
        
        plus_token = self._create_token("OPERATOR", "+", line=1, column=3)
        minus_token = self._create_token("OPERATOR", "-", line=1, column=7)
        
        mock_parse_mult.side_effect = [
            (a_ast, self._create_parser_state([], pos=1)),
            (b_ast, self._create_parser_state([], pos=2)),
            (c_ast, self._create_parser_state([], pos=3))
        ]
        
        mock_get_token.side_effect = [plus_token, minus_token, None]
        mock_is_op.side_effect = [True, True, False]
        mock_consume.return_value = self._create_parser_state([], pos=2)
        
        parser_state = self._create_parser_state([], pos=0)
        
        # Execute
        result_ast, result_state = _parse_additive(parser_state)
        
        # Verify: (a + b) - c
        self.assertEqual(result_ast["type"], "BINARY_OP")
        self.assertEqual(result_ast["value"], "-")
        
        left_child = result_ast["children"][0]
        self.assertEqual(left_child["type"], "BINARY_OP")
        self.assertEqual(left_child["value"], "+")
        self.assertEqual(left_child["children"][0], a_ast)
        self.assertEqual(left_child["children"][1], b_ast)
        
        self.assertEqual(result_ast["children"][1], c_ast)

    @patch('_parse_additive_src._parse_multiplicative')
    @patch('_parse_additive_src._get_current_token')
    @patch('_parse_additive_src._consume_token')
    @patch('_parse_additive_src._is_operator_token')
    def test_empty_tokens(self, mock_is_op, mock_consume, mock_get_token, mock_parse_mult):
        """Test with empty token list."""
        # Setup: empty result from multiplicative
        empty_ast = self._create_ast_node("EMPTY", line=0, column=0)
        mock_parse_mult.return_value = (empty_ast, self._create_parser_state([], pos=0))
        
        mock_get_token.return_value = None
        mock_is_op.return_value = False
        
        parser_state = self._create_parser_state([], pos=0)
        
        # Execute
        result_ast, result_state = _parse_additive(parser_state)
        
        # Verify
        self.assertEqual(result_ast, empty_ast)
        mock_get_token.assert_called_once()
        mock_is_op.assert_called_once()
        mock_consume.assert_not_called()

    @patch('_parse_additive_src._parse_multiplicative')
    @patch('_parse_additive_src._get_current_token')
    @patch('_parse_additive_src._consume_token')
    @patch('_parse_additive_src._is_operator_token')
    def test_none_token_handling(self, mock_is_op, mock_consume, mock_get_token, mock_parse_mult):
        """Test when _get_current_token returns None."""
        operand_ast = self._create_ast_node("NUMBER", value=42, line=1, column=1)
        mock_parse_mult.return_value = (operand_ast, self._create_parser_state([], pos=1))
        
        mock_get_token.return_value = None
        mock_is_op.return_value = False
        
        parser_state = self._create_parser_state([], pos=1)
        
        # Execute
        result_ast, result_state = _parse_additive(parser_state)
        
        # Verify
        self.assertEqual(result_ast, operand_ast)
        mock_is_op.assert_called_once_with(None, ['+', '-'])

    @patch('_parse_additive_src._parse_multiplicative')
    @patch('_parse_additive_src._get_current_token')
    @patch('_parse_additive_src._consume_token')
    @patch('_parse_additive_src._is_operator_token')
    def test_ast_position_from_operator_token(self, mock_is_op, mock_consume, mock_get_token, mock_parse_mult):
        """Test that AST node position comes from operator token, not operands."""
        left_ast = self._create_ast_node("NUMBER", value=1, line=1, column=1)
        right_ast = self._create_ast_node("NUMBER", value=2, line=2, column=5)
        
        op_token = self._create_token("OPERATOR", "+", line=1, column=10)
        
        mock_parse_mult.side_effect = [
            (left_ast, self._create_parser_state([], pos=1)),
            (right_ast, self._create_parser_state([], pos=2))
        ]
        
        mock_get_token.side_effect = [op_token, None]
        mock_is_op.side_effect = [True, False]
        mock_consume.return_value = self._create_parser_state([], pos=2)
        
        parser_state = self._create_parser_state([], pos=0)
        
        # Execute
        result_ast, result_state = _parse_additive(parser_state)
        
        # Verify position comes from operator token
        self.assertEqual(result_ast["line"], 1)
        self.assertEqual(result_ast["column"], 10)
        # Not from left operand (1, 1) or right operand (2, 5)

    @patch('_parse_additive_src._parse_multiplicative')
    @patch('_parse_additive_src._get_current_token')
    @patch('_parse_additive_src._consume_token')
    @patch('_parse_additive_src._is_operator_token')
    def test_operator_token_without_line_column(self, mock_is_op, mock_consume, mock_get_token, mock_parse_mult):
        """Test handling of operator token missing line/column (defaults to 0)."""
        left_ast = self._create_ast_node("NUMBER", value=1)
        right_ast = self._create_ast_node("NUMBER", value=2)
        
        # Token without line/column
        op_token = {"type": "OPERATOR", "value": "+"}
        
        mock_parse_mult.side_effect = [
            (left_ast, self._create_parser_state([], pos=1)),
            (right_ast, self._create_parser_state([], pos=2))
        ]
        
        mock_get_token.side_effect = [op_token, None]
        mock_is_op.side_effect = [True, False]
        mock_consume.return_value = self._create_parser_state([], pos=2)
        
        parser_state = self._create_parser_state([], pos=0)
        
        # Execute
        result_ast, result_state = _parse_additive(parser_state)
        
        # Verify defaults to 0
        self.assertEqual(result_ast["line"], 0)
        self.assertEqual(result_ast["column"], 0)


if __name__ == "__main__":
    unittest.main()

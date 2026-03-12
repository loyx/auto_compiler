# === std / third-party imports ===
import sys
import unittest
from typing import Any, Dict
from unittest.mock import patch, MagicMock

# === Mock dependencies before importing _parse_or_expr_src ===
# This prevents the deep import chain from being triggered
_mock_and_expr = MagicMock()
sys.modules['main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_or_expr_package._parse_and_expr_package._parse_and_expr_src'] = _mock_and_expr

# === sub function imports ===
from ._parse_or_expr_src import _parse_or_expr

# === Type Aliases ===
Token = Dict[str, Any]
AST = Dict[str, Any]
ParserState = Dict[str, Any]


class TestParseOrExpr(unittest.TestCase):
    """Test cases for _parse_or_expr function."""

    def test_single_operand_no_or_operator(self):
        """Test parsing a single operand without any || operator."""
        # Setup: Create parser state with a single identifier token
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        # Mock _parse_and_expr to return a simple AST node
        mock_operand = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 1
        }
        
        with patch("._parse_or_expr_package._parse_and_expr_package._parse_and_expr_src._parse_and_expr") as mock_parse_and:
            mock_parse_and.return_value = mock_operand
            mock_parse_and.side_effect = [mock_operand]  # Only called once
            
            result = _parse_or_expr(parser_state)
            
            # Verify result is the operand (no BINARY_OP created)
            self.assertEqual(result["type"], "IDENTIFIER")
            self.assertEqual(result["value"], "x")
            self.assertEqual(parser_state["pos"], 1)  # pos should advance after _parse_and_expr
            mock_parse_and.assert_called_once()

    def test_two_operands_with_or_operator(self):
        """Test parsing two operands connected by || operator."""
        # Setup: Create parser state with two identifiers and an OR token
        tokens = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            {"type": "OR", "value": "||", "line": 1, "column": 3},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 6}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        # Mock _parse_and_expr to return operands
        mock_left = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        mock_right = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 6}
        
        with patch("._parse_or_expr_package._parse_and_expr_package._parse_and_expr_src._parse_and_expr") as mock_parse_and:
            mock_parse_and.side_effect = [mock_left, mock_right]
            
            result = _parse_or_expr(parser_state)
            
            # Verify result is a BINARY_OP node
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "||")
            self.assertEqual(len(result["children"]), 2)
            self.assertEqual(result["children"][0]["value"], "a")
            self.assertEqual(result["children"][1]["value"], "b")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 3)
            self.assertEqual(parser_state["pos"], 3)  # All tokens consumed
            self.assertEqual(mock_parse_and.call_count, 2)

    def test_three_operands_left_associative(self):
        """Test parsing three operands with || operators (left-associative)."""
        # Setup: a || b || c should parse as (a || b) || c
        tokens = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            {"type": "OR", "value": "||", "line": 1, "column": 3},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 6},
            {"type": "OR", "value": "||", "line": 1, "column": 8},
            {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 11}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        # Mock _parse_and_expr to return operands
        mock_a = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        mock_b = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 6}
        mock_c = {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 11}
        
        with patch("._parse_or_expr_package._parse_and_expr_package._parse_and_expr_src._parse_and_expr") as mock_parse_and:
            mock_parse_and.side_effect = [mock_a, mock_b, mock_c]
            
            result = _parse_or_expr(parser_state)
            
            # Verify left-associative structure: (a || b) || c
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "||")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 8)  # Second || operator position
            
            # Left child should be (a || b)
            left_child = result["children"][0]
            self.assertEqual(left_child["type"], "BINARY_OP")
            self.assertEqual(left_child["value"], "||")
            self.assertEqual(left_child["children"][0]["value"], "a")
            self.assertEqual(left_child["children"][1]["value"], "b")
            
            # Right child should be c
            right_child = result["children"][1]
            self.assertEqual(right_child["value"], "c")
            
            self.assertEqual(parser_state["pos"], 5)  # All tokens consumed
            self.assertEqual(mock_parse_and.call_count, 3)

    def test_empty_tokens(self):
        """Test parsing with empty token list."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }
        
        # Mock _parse_and_expr to handle empty case
        mock_empty = {"type": "LITERAL", "value": None, "line": 0, "column": 0}
        
        with patch("._parse_or_expr_package._parse_and_expr_package._parse_and_expr_src._parse_and_expr") as mock_parse_and:
            mock_parse_and.return_value = mock_empty
            
            result = _parse_or_expr(parser_state)
            
            # Should return the result from _parse_and_expr without modification
            self.assertEqual(result["type"], "LITERAL")
            self.assertEqual(parser_state["pos"], 0)
            mock_parse_and.assert_called_once()

    def test_or_operator_at_end_without_right_operand(self):
        """Test parsing when || is at the end (incomplete expression)."""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            {"type": "OR", "value": "||", "line": 1, "column": 3}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        # Mock _parse_and_expr to return operands
        mock_left = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        mock_right = {"type": "LITERAL", "value": None, "line": 0, "column": 0}
        
        with patch("._parse_or_expr_package._parse_and_expr_package._parse_and_expr_src._parse_and_expr") as mock_parse_and:
            mock_parse_and.side_effect = [mock_left, mock_right]
            
            result = _parse_or_expr(parser_state)
            
            # Should still create BINARY_OP node (error handling is not in this function)
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "||")
            self.assertEqual(parser_state["pos"], 2)
            self.assertEqual(mock_parse_and.call_count, 2)

    def test_pos_advances_correctly(self):
        """Test that parser_state pos advances correctly through tokens."""
        tokens = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            {"type": "OR", "value": "||", "line": 1, "column": 3},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 6},
            {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 9}  # Extra token
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        mock_a = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        mock_b = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 6}
        
        with patch("._parse_or_expr_package._parse_and_expr_package._parse_and_expr_src._parse_and_expr") as mock_parse_and:
            mock_parse_and.side_effect = [mock_a, mock_b]
            
            result = _parse_or_expr(parser_state)
            
            # Should stop after parsing a || b, pos should be 2
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(parser_state["pos"], 2)  # Only consumed a, ||, b (pos advances in _parse_and_expr)
            self.assertEqual(mock_parse_and.call_count, 2)

    def test_or_token_with_line_column_info(self):
        """Test that line and column information is preserved from OR token."""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 5, "column": 10},
            {"type": "OR", "value": "||", "line": 5, "column": 12},
            {"type": "IDENTIFIER", "value": "y", "line": 5, "column": 15}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        mock_x = {"type": "IDENTIFIER", "value": "x", "line": 5, "column": 10}
        mock_y = {"type": "IDENTIFIER", "value": "y", "line": 5, "column": 15}
        
        with patch("._parse_or_expr_package._parse_and_expr_package._parse_and_expr_src._parse_and_expr") as mock_parse_and:
            mock_parse_and.side_effect = [mock_x, mock_y]
            
            result = _parse_or_expr(parser_state)
            
            # Verify line and column from OR token
            self.assertEqual(result["line"], 5)
            self.assertEqual(result["column"], 12)

    def test_multiple_consecutive_or_operators(self):
        """Test parsing with multiple consecutive OR operators."""
        tokens = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            {"type": "OR", "value": "||", "line": 1, "column": 3},
            {"type": "OR", "value": "||", "line": 1, "column": 5},  # Consecutive OR
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 8}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        mock_a = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        mock_none1 = {"type": "LITERAL", "value": None, "line": 0, "column": 0}
        mock_b = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 8}
        
        with patch("._parse_or_expr_package._parse_and_expr_package._parse_and_expr_src._parse_and_expr") as mock_parse_and:
            mock_parse_and.side_effect = [mock_a, mock_none1, mock_b]
            
            result = _parse_or_expr(parser_state)
            
            # Should create nested BINARY_OP nodes
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(mock_parse_and.call_count, 3)


if __name__ == "__main__":
    unittest.main()

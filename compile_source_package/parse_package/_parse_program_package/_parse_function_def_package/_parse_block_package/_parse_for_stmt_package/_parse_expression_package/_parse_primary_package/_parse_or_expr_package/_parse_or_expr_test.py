# -*- coding: utf-8 -*-
"""Unit tests for _parse_or_expr function."""

import unittest
from unittest.mock import patch

# Relative import from the same package
from ._parse_or_expr_src import _parse_or_expr


class TestParseOrExpr(unittest.TestCase):
    """Test cases for _parse_or_expr function."""

    def test_single_operand_no_or(self):
        """Test parsing a single operand without OR operator."""
        mock_and_result = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 0
        }
        
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 0}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        call_count = [0]
        def parse_and_side_effect(state):
            call_count[0] += 1
            return mock_and_result
        
        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_primary_package._parse_or_expr_package._parse_or_expr_src._parse_and_expr', side_effect=parse_and_side_effect) as mock_parse_and:
            result = _parse_or_expr(parser_state)
            
            self.assertEqual(result, mock_and_result)
            self.assertEqual(parser_state["pos"], 0)
            mock_parse_and.assert_called_once_with(parser_state)

    def test_single_or_expression(self):
        """Test parsing a simple OR expression: a or b."""
        left_operand = {
            "type": "IDENTIFIER",
            "value": "a",
            "line": 1,
            "column": 0
        }
        right_operand = {
            "type": "IDENTIFIER",
            "value": "b",
            "line": 1,
            "column": 5
        }
        
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 0},
                {"type": "OR", "value": "or", "line": 1, "column": 2},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        call_count = [0]
        def parse_and_side_effect(state):
            result = [left_operand, right_operand][call_count[0]]
            call_count[0] += 1
            return result
        
        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_primary_package._parse_or_expr_package._parse_or_expr_src._parse_and_expr', side_effect=parse_and_side_effect) as mock_parse_and:
            result = _parse_or_expr(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "or")
            self.assertEqual(len(result["children"]), 2)
            self.assertEqual(result["children"][0], left_operand)
            self.assertEqual(result["children"][1], right_operand)
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 2)
            self.assertEqual(parser_state["pos"], 3)
            self.assertEqual(mock_parse_and.call_count, 2)

    def test_multiple_or_expressions_left_associative(self):
        """Test parsing multiple OR expressions with left associativity: a or b or c."""
        operand_a = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 0}
        operand_b = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
        operand_c = {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 10}
        
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 0},
                {"type": "OR", "value": "or", "line": 1, "column": 2},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
                {"type": "OR", "value": "or", "line": 1, "column": 7},
                {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 10}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        call_count = [0]
        def parse_and_side_effect(state):
            result = [operand_a, operand_b, operand_c][call_count[0]]
            call_count[0] += 1
            return result
        
        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_primary_package._parse_or_expr_package._parse_or_expr_src._parse_and_expr', side_effect=parse_and_side_effect) as mock_parse_and:
            result = _parse_or_expr(parser_state)
            
            # Should be left-associative: (a or b) or c
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "or")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 7)
            
            # Left child should be (a or b)
            left_child = result["children"][0]
            self.assertEqual(left_child["type"], "BINARY_OP")
            self.assertEqual(left_child["value"], "or")
            self.assertEqual(left_child["children"][0], operand_a)
            self.assertEqual(left_child["children"][1], operand_b)
            
            # Right child should be c
            self.assertEqual(result["children"][1], operand_c)
            
            self.assertEqual(parser_state["pos"], 5)
            self.assertEqual(mock_parse_and.call_count, 3)

    def test_empty_tokens(self):
        """Test parsing with empty token list."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }
        
        mock_result = {"type": "LITERAL", "value": None, "line": 0, "column": 0}
        
        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_primary_package._parse_or_expr_package._parse_or_expr_src._parse_and_expr', return_value=mock_result) as mock_parse_and:
            result = _parse_or_expr(parser_state)
            
            self.assertEqual(result, mock_result)
            self.assertEqual(parser_state["pos"], 0)
            mock_parse_and.assert_called_once_with(parser_state)

    def test_or_at_end_without_right_operand(self):
        """Test OR operator at end without right operand."""
        left_operand = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 0
        }
        
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 0},
                {"type": "OR", "value": "or", "line": 1, "column": 2}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        call_count = [0]
        def parse_and_side_effect(state):
            call_count[0] += 1
            if call_count[0] == 1:
                return left_operand
            else:
                return {"type": "LITERAL", "value": None, "line": 1, "column": 2}
        
        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_primary_package._parse_or_expr_package._parse_or_expr_src._parse_and_expr', side_effect=parse_and_side_effect) as mock_parse_and:
            result = _parse_or_expr(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "or")
            self.assertEqual(len(result["children"]), 2)
            self.assertEqual(parser_state["pos"], 2)
            self.assertEqual(mock_parse_and.call_count, 2)

    def test_non_or_token_stops_parsing(self):
        """Test that non-OR tokens stop OR expression parsing."""
        left_operand = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 0}
        
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 0},
                {"type": "AND", "value": "and", "line": 1, "column": 2},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_primary_package._parse_or_expr_package._parse_or_expr_src._parse_and_expr', return_value=left_operand) as mock_parse_and:
            result = _parse_or_expr(parser_state)
            
            self.assertEqual(result, left_operand)
            self.assertEqual(parser_state["pos"], 0)
            mock_parse_and.assert_called_once_with(parser_state)

    def test_preserves_line_column_from_or_token(self):
        """Test that line and column are preserved from OR token."""
        left_operand = {"type": "IDENTIFIER", "value": "x", "line": 5, "column": 10}
        right_operand = {"type": "IDENTIFIER", "value": "y", "line": 5, "column": 15}
        
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 5, "column": 10},
                {"type": "OR", "value": "or", "line": 5, "column": 12},
                {"type": "IDENTIFIER", "value": "y", "line": 5, "column": 15}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        call_count = [0]
        def parse_and_side_effect(state):
            result = [left_operand, right_operand][call_count[0]]
            call_count[0] += 1
            return result
        
        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_primary_package._parse_or_expr_package._parse_or_expr_src._parse_and_expr', side_effect=parse_and_side_effect):
            result = _parse_or_expr(parser_state)
            
            self.assertEqual(result["line"], 5)
            self.assertEqual(result["column"], 12)

    def test_parser_state_pos_updated_correctly(self):
        """Test that parser_state pos is updated correctly after parsing."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 0},
                {"type": "OR", "value": "or", "line": 1, "column": 2},
                {"type": "IDENTIFIER", "value": "y", "line": 1, "column": 5},
                {"type": "OR", "value": "or", "line": 1, "column": 7},
                {"type": "IDENTIFIER", "value": "z", "line": 1, "column": 10},
                {"type": "NEWLINE", "value": "\n", "line": 1, "column": 11}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        call_count = [0]
        operands = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 0},
            {"type": "IDENTIFIER", "value": "y", "line": 1, "column": 5},
            {"type": "IDENTIFIER", "value": "z", "line": 1, "column": 10}
        ]
        
        def parse_and_side_effect(state):
            result = operands[call_count[0]]
            call_count[0] += 1
            return result
        
        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_primary_package._parse_or_expr_package._parse_or_expr_src._parse_and_expr', side_effect=parse_and_side_effect):
            result = _parse_or_expr(parser_state)
            
            self.assertEqual(parser_state["pos"], 5)

    def test_missing_tokens_key_in_parser_state(self):
        """Test handling when tokens key is missing from parser_state."""
        parser_state = {
            "pos": 0,
            "filename": "test.py"
        }
        
        mock_result = {"type": "LITERAL", "value": None, "line": 0, "column": 0}
        
        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_primary_package._parse_or_expr_package._parse_or_expr_src._parse_and_expr', return_value=mock_result) as mock_parse_and:
            result = _parse_or_expr(parser_state)
            
            self.assertEqual(result, mock_result)
            mock_parse_and.assert_called_once_with(parser_state)

    def test_missing_pos_key_in_parser_state(self):
        """Test handling when pos key is missing from parser_state."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 0}
            ],
            "filename": "test.py"
        }
        
        mock_result = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 0}
        
        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_primary_package._parse_or_expr_package._parse_or_expr_src._parse_and_expr', return_value=mock_result) as mock_parse_and:
            result = _parse_or_expr(parser_state)
            
            self.assertEqual(result, mock_result)
            self.assertEqual(parser_state["pos"], 1)
            mock_parse_and.assert_called_once_with(parser_state)


if __name__ == "__main__":
    unittest.main()

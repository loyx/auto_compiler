#!/usr/bin/env python3
"""
Unit tests for _parse_logical_and function.
Tests parsing of logical AND (&&) expressions with left associativity.
"""

import unittest
from unittest.mock import patch

# Relative import from the same package
from ._parse_logical_and_src import _parse_logical_and, ParserState


class TestParseLogicalAnd(unittest.TestCase):
    """Test cases for _parse_logical_and function."""

    def test_single_operand_no_and(self):
        """Test parsing a single operand without && operator."""
        mock_comparison_result = {
            "type": "IDENTIFIER",
            "value": "a",
            "children": [],
            "line": 1,
            "column": 1
        }
        
        parser_state: ParserState = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "SEMICOLON", "value": ";", "line": 1, "column": 2}
            ],
            "pos": 0,
            "filename": "test.c",
            "error": ""
        }
        
        with patch("._parse_logical_and_src._parse_comparison", return_value=mock_comparison_result) as mock_parse_comp:
            result = _parse_logical_and(parser_state)
        
        # Should return the single operand without wrapping
        self.assertEqual(result, mock_comparison_result)
        # Position should not change (no && consumed)
        self.assertEqual(parser_state["pos"], 0)
        mock_parse_comp.assert_called_once_with(parser_state)

    def test_two_operands_with_and(self):
        """Test parsing 'a && b' - two operands with one && operator."""
        left_operand = {
            "type": "IDENTIFIER",
            "value": "a",
            "children": [],
            "line": 1,
            "column": 1
        }
        right_operand = {
            "type": "IDENTIFIER",
            "value": "b",
            "children": [],
            "line": 1,
            "column": 5
        }
        
        parser_state: ParserState = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "AND", "value": "&&", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
                {"type": "SEMICOLON", "value": ";", "line": 1, "column": 6}
            ],
            "pos": 0,
            "filename": "test.c",
            "error": ""
        }
        
        call_count = [0]
        def side_effect(state):
            result = left_operand if call_count[0] == 0 else right_operand
            call_count[0] += 1
            return result
        
        with patch("._parse_logical_and_src._parse_comparison", side_effect=side_effect) as mock_parse_comp:
            result = _parse_logical_and(parser_state)
        
        # Should create a BINARY_OP node
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["operator"], "&&")
        self.assertEqual(len(result["children"]), 2)
        self.assertEqual(result["children"][0], left_operand)
        self.assertEqual(result["children"][1], right_operand)
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 3)
        
        # Position should advance past the && token
        self.assertEqual(parser_state["pos"], 2)
        self.assertEqual(mock_parse_comp.call_count, 2)

    def test_left_associative_multiple_and(self):
        """Test parsing 'a && b && c' - left associativity."""
        operand_a = {
            "type": "IDENTIFIER",
            "value": "a",
            "children": [],
            "line": 1,
            "column": 1
        }
        operand_b = {
            "type": "IDENTIFIER",
            "value": "b",
            "children": [],
            "line": 1,
            "column": 5
        }
        operand_c = {
            "type": "IDENTIFIER",
            "value": "c",
            "children": [],
            "line": 1, "column": 9
        }
        
        parser_state: ParserState = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "AND", "value": "&&", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
                {"type": "AND", "value": "&&", "line": 1, "column": 7},
                {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 9},
                {"type": "SEMICOLON", "value": ";", "line": 1, "column": 10}
            ],
            "pos": 0,
            "filename": "test.c",
            "error": ""
        }
        
        call_count = [0]
        def side_effect(state):
            result = [operand_a, operand_b, operand_c][call_count[0]]
            call_count[0] += 1
            return result
        
        with patch("._parse_logical_and_src._parse_comparison", side_effect=side_effect):
            result = _parse_logical_and(parser_state)
        
        # Should be left-associative: (a && b) && c
        # Structure: BINARY_OP(&&, children=[BINARY_OP(&&, children=[a, b]), c])
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["operator"], "&&")
        self.assertEqual(len(result["children"]), 2)
        
        # Left child should be another BINARY_OP (a && b)
        left_child = result["children"][0]
        self.assertEqual(left_child["type"], "BINARY_OP")
        self.assertEqual(left_child["operator"], "&&")
        self.assertEqual(left_child["children"][0], operand_a)
        self.assertEqual(left_child["children"][1], operand_b)
        
        # Right child should be c
        self.assertEqual(result["children"][1], operand_c)
        
        # Position should advance past both && tokens
        self.assertEqual(parser_state["pos"], 4)

    def test_error_from_comparison_parser(self):
        """Test error propagation when _parse_comparison returns an error."""
        error_node = {
            "type": "ERROR",
            "value": "Unexpected token",
            "children": [],
            "line": 1,
            "column": 1
        }
        
        parser_state: ParserState = {
            "tokens": [
                {"type": "INVALID", "value": "@", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.c",
            "error": "Unexpected token"
        }
        
        with patch("._parse_logical_and_src._parse_comparison", return_value=error_node):
            result = _parse_logical_and(parser_state)
        
        # Should return the error node without trying to parse &&
        self.assertEqual(result, error_node)
        self.assertEqual(parser_state["pos"], 0)

    def test_missing_operand_after_and(self):
        """Test error handling when && is followed by missing operand."""
        left_operand = {
            "type": "IDENTIFIER",
            "value": "a",
            "children": [],
            "line": 1,
            "column": 1
        }
        
        parser_state: ParserState = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "AND", "value": "&&", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.c",
            "error": ""
        }
        
        call_count = [0]
        def side_effect(state):
            if call_count[0] == 0:
                call_count[0] += 1
                return left_operand
            else:
                # Second call (after &&) returns error node
                state["error"] = "Missing operand"
                return {
                    "type": "ERROR",
                    "value": "Missing operand",
                    "children": [],
                    "line": 1,
                    "column": 3
                }
        
        with patch("._parse_logical_and_src._parse_comparison", side_effect=side_effect):
            result = _parse_logical_and(parser_state)
        
        # Should return an ERROR node
        self.assertEqual(result["type"], "ERROR")
        self.assertIn("Missing operand", result["value"])
        self.assertEqual(parser_state["error"], "Missing operand after &&")

    def test_empty_token_list(self):
        """Test parsing with empty token list."""
        parser_state: ParserState = {
            "tokens": [],
            "pos": 0,
            "filename": "test.c",
            "error": ""
        }
        
        empty_result = {
            "type": "EOF",
            "value": "",
            "children": [],
            "line": 0,
            "column": 0
        }
        
        with patch("._parse_logical_and_src._parse_comparison", return_value=empty_result):
            result = _parse_logical_and(parser_state)
        
        # Should return the result from _parse_comparison
        self.assertEqual(result, empty_result)
        self.assertEqual(parser_state["pos"], 0)

    def test_and_at_end_of_tokens(self):
        """Test parsing when && is at the end with no following token."""
        left_operand = {
            "type": "IDENTIFIER",
            "value": "a",
            "children": [],
            "line": 1,
            "column": 1
        }
        
        parser_state: ParserState = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "AND", "value": "&&", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.c",
            "error": ""
        }
        
        call_count = [0]
        def side_effect(state):
            if call_count[0] == 0:
                call_count[0] += 1
                return left_operand
            else:
                # Second call at EOF
                state["error"] = "Unexpected end of file"
                return {
                    "type": "ERROR",
                    "value": "Unexpected end of file",
                    "children": [],
                    "line": 0,
                    "column": 0
                }
        
        with patch("._parse_logical_and_src._parse_comparison", side_effect=side_effect):
            result = _parse_logical_and(parser_state)
        
        # Should return an ERROR node
        self.assertEqual(result["type"], "ERROR")

    def test_position_tracking_with_and(self):
        """Test that position is correctly tracked when consuming && tokens."""
        operand = {
            "type": "IDENTIFIER",
            "value": "x",
            "children": [],
            "line": 2,
            "column": 5
        }
        
        parser_state: ParserState = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 2, "column": 5},
                {"type": "AND", "value": "&&", "line": 2, "column": 7},
                {"type": "IDENTIFIER", "value": "y", "line": 2, "column": 9}
            ],
            "pos": 0,
            "filename": "test.c",
            "error": ""
        }
        
        call_count = [0]
        def side_effect(state):
            result = operand.copy()
            call_count[0] += 1
            return result
        
        with patch("._parse_logical_and_src._parse_comparison", side_effect=side_effect):
            result = _parse_logical_and(parser_state)
        
        # After parsing 'x && y', pos should be 2 (past the && token)
        self.assertEqual(parser_state["pos"], 2)
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 7)

    def test_non_and_token_stops_loop(self):
        """Test that non-AND tokens stop the && parsing loop."""
        left_operand = {
            "type": "IDENTIFIER",
            "value": "a",
            "children": [],
            "line": 1,
            "column": 1
        }
        right_operand = {
            "type": "IDENTIFIER",
            "value": "b",
            "children": [],
            "line": 1,
            "column": 3
        }
        
        parser_state: ParserState = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "OR", "value": "||", "line": 1, "column": 2},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.c",
            "error": ""
        }
        
        call_count = [0]
        def side_effect(state):
            result = left_operand if call_count[0] == 0 else right_operand
            call_count[0] += 1
            return result
        
        with patch("._parse_logical_and_src._parse_comparison", side_effect=side_effect):
            result = _parse_logical_and(parser_state)
        
        # Should only parse 'a' and stop at || (not consume it)
        self.assertEqual(result, left_operand)
        self.assertEqual(parser_state["pos"], 0)
        # _parse_comparison should only be called once
        self.assertEqual(call_count[0], 1)


class TestHelperFunctions(unittest.TestCase):
    """Test cases for helper functions."""

    def test_is_current_token_and_true(self):
        """Test _is_current_token_and returns True for AND token."""
        from ._parse_logical_and_src import _is_current_token_and
        
        parser_state: ParserState = {
            "tokens": [
                {"type": "AND", "value": "&&", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.c",
            "error": ""
        }
        
        result = _is_current_token_and(parser_state)
        self.assertTrue(result)

    def test_is_current_token_and_false(self):
        """Test _is_current_token_and returns False for non-AND token."""
        from ._parse_logical_and_src import _is_current_token_and
        
        parser_state: ParserState = {
            "tokens": [
                {"type": "OR", "value": "||", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.c",
            "error": ""
        }
        
        result = _is_current_token_and(parser_state)
        self.assertFalse(result)

    def test_is_current_token_and_eof(self):
        """Test _is_current_token_and returns False at EOF."""
        from ._parse_logical_and_src import _is_current_token_and
        
        parser_state: ParserState = {
            "tokens": [],
            "pos": 0,
            "filename": "test.c",
            "error": ""
        }
        
        result = _is_current_token_and(parser_state)
        self.assertFalse(result)

    def test_is_current_token_and_beyond_length(self):
        """Test _is_current_token_and returns False when pos >= len(tokens)."""
        from ._parse_logical_and_src import _is_current_token_and
        
        parser_state: ParserState = {
            "tokens": [
                {"type": "AND", "value": "&&", "line": 1, "column": 1}
            ],
            "pos": 5,  # Beyond token list
            "filename": "test.c",
            "error": ""
        }
        
        result = _is_current_token_and(parser_state)
        self.assertFalse(result)

    def test_get_current_token_valid(self):
        """Test _get_current_token returns correct token."""
        from ._parse_logical_and_src import _get_current_token
        
        expected_token = {"type": "AND", "value": "&&", "line": 1, "column": 1}
        parser_state: ParserState = {
            "tokens": [expected_token],
            "pos": 0,
            "filename": "test.c",
            "error": ""
        }
        
        result = _get_current_token(parser_state)
        self.assertEqual(result, expected_token)

    def test_get_current_token_eof(self):
        """Test _get_current_token returns EOF token at end."""
        from ._parse_logical_and_src import _get_current_token
        
        parser_state: ParserState = {
            "tokens": [],
            "pos": 0,
            "filename": "test.c",
            "error": ""
        }
        
        result = _get_current_token(parser_state)
        self.assertEqual(result["type"], "EOF")
        self.assertEqual(result["line"], 0)
        self.assertEqual(result["column"], 0)

    def test_create_error_node(self):
        """Test _create_error_node creates proper error AST."""
        from ._parse_logical_and_src import _create_error_node
        
        parser_state: ParserState = {
            "tokens": [
                {"type": "INVALID", "value": "@", "line": 3, "column": 5}
            ],
            "pos": 0,
            "filename": "test.c",
            "error": ""
        }
        
        result = _create_error_node(parser_state, "Test error message")
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], "Test error message")
        self.assertEqual(result["children"], [])
        self.assertEqual(result["line"], 3)
        self.assertEqual(result["column"], 5)
        # Should set error in parser_state
        self.assertEqual(parser_state["error"], "Test error message")

    def test_create_error_node_empty_tokens(self):
        """Test _create_error_node with empty token list."""
        from ._parse_logical_and_src import _create_error_node
        
        parser_state: ParserState = {
            "tokens": [],
            "pos": 0,
            "filename": "test.c",
            "error": ""
        }
        
        result = _create_error_node(parser_state, "Test error")
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["line"], 0)
        self.assertEqual(result["column"], 0)


if __name__ == "__main__":
    unittest.main()

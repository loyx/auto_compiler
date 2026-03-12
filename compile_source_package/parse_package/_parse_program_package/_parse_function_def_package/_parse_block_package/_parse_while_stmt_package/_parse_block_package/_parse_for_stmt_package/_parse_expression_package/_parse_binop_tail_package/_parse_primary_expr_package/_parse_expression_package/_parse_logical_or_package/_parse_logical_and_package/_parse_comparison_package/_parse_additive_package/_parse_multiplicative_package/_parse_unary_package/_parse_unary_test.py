import unittest
from unittest.mock import patch
from typing import Dict, Any

# Relative import for the function under test
from ._parse_unary_src import _parse_unary

# Type aliases (matching the source)
Token = Dict[str, Any]
AST = Dict[str, Any]
ParserState = Dict[str, Any]


class TestParseUnary(unittest.TestCase):
    """Test cases for _parse_unary function"""
    
    def test_unary_minus(self):
        """Test MINUS unary operator"""
        tokens = [
            {"type": "MINUS", "value": "-", "line": 1, "column": 1},
            {"type": "NUMBER", "value": "42", "line": 1, "column": 2}
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.py"}
        
        expected_operand = {
            "type": "NUMBER",
            "value": "42",
            "line": 1,
            "column": 2
        }
        
        with patch("._parse_primary_package._parse_primary_src._parse_primary", return_value=expected_operand) as mock_primary:
            result = _parse_unary(parser_state)
        
        self.assertEqual(result["type"], "UNARY_OP")
        self.assertEqual(result["operator"], "-")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0], expected_operand)
        self.assertEqual(parser_state["pos"], 2)
        mock_primary.assert_called_once()
    
    def test_unary_plus(self):
        """Test PLUS unary operator"""
        tokens = [
            {"type": "PLUS", "value": "+", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 2}
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.py"}
        
        expected_operand = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 2
        }
        
        with patch("._parse_primary_package._parse_primary_src._parse_primary", return_value=expected_operand) as mock_primary:
            result = _parse_unary(parser_state)
        
        self.assertEqual(result["type"], "UNARY_OP")
        self.assertEqual(result["operator"], "+")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0], expected_operand)
        self.assertEqual(parser_state["pos"], 2)
    
    def test_unary_not(self):
        """Test NOT unary operator"""
        tokens = [
            {"type": "NOT", "value": "!", "line": 2, "column": 3},
            {"type": "IDENTIFIER", "value": "flag", "line": 2, "column": 4}
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.py"}
        
        expected_operand = {
            "type": "IDENTIFIER",
            "value": "flag",
            "line": 2,
            "column": 4
        }
        
        with patch("._parse_primary_package._parse_primary_src._parse_primary", return_value=expected_operand) as mock_primary:
            result = _parse_unary(parser_state)
        
        self.assertEqual(result["type"], "UNARY_OP")
        self.assertEqual(result["operator"], "!")
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 3)
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0], expected_operand)
    
    def test_unary_bitwise_not(self):
        """Test BITWISE_NOT unary operator"""
        tokens = [
            {"type": "BITWISE_NOT", "value": "~", "line": 3, "column": 1},
            {"type": "NUMBER", "value": "42", "line": 3, "column": 2}
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.py"}
        
        expected_operand = {
            "type": "NUMBER",
            "value": "42",
            "line": 3,
            "column": 2
        }
        
        with patch("._parse_primary_package._parse_primary_src._parse_primary", return_value=expected_operand) as mock_primary:
            result = _parse_unary(parser_state)
        
        self.assertEqual(result["type"], "UNARY_OP")
        self.assertEqual(result["operator"], "~")
        self.assertEqual(result["line"], 3)
        self.assertEqual(result["column"], 1)
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0], expected_operand)
    
    def test_right_associativity_nested_unary(self):
        """Test right-associativity of unary operators (e.g., --x)"""
        tokens = [
            {"type": "MINUS", "value": "-", "line": 1, "column": 1},
            {"type": "MINUS", "value": "-", "line": 1, "column": 2},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 3}
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.py"}
        
        expected_operand = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 3
        }
        
        def mock_primary_side_effect(state):
            state["pos"] = 3
            return expected_operand
        
        with patch("._parse_primary_package._parse_primary_src._parse_primary", side_effect=mock_primary_side_effect) as mock_primary:
            result = _parse_unary(parser_state)
        
        self.assertEqual(result["type"], "UNARY_OP")
        self.assertEqual(result["operator"], "-")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        
        inner_unary = result["children"][0]
        self.assertEqual(inner_unary["type"], "UNARY_OP")
        self.assertEqual(inner_unary["operator"], "-")
        self.assertEqual(inner_unary["line"], 1)
        self.assertEqual(inner_unary["column"], 2)
        
        self.assertEqual(len(inner_unary["children"]), 1)
        self.assertEqual(inner_unary["children"][0], expected_operand)
        
        self.assertEqual(parser_state["pos"], 3)
        self.assertEqual(mock_primary.call_count, 1)
    
    def test_empty_input_error(self):
        """Test error when no tokens available"""
        tokens = []
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.py"}
        
        result = _parse_unary(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertIsNone(result["value"])
        self.assertEqual(result["line"], -1)
        self.assertEqual(result["column"], -1)
        self.assertEqual(parser_state["error"], "Unexpected end of input while parsing unary expression")
    
    def test_position_at_end_error(self):
        """Test error when pos is at end of tokens"""
        tokens = [
            {"type": "NUMBER", "value": "42", "line": 1, "column": 1}
        ]
        parser_state = {"tokens": tokens, "pos": 1, "filename": "test.py"}
        
        result = _parse_unary(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertIsNone(result["value"])
        self.assertEqual(result["line"], -1)
        self.assertEqual(result["column"], -1)
        self.assertEqual(parser_state["error"], "Unexpected end of input while parsing unary expression")
    
    def test_delegates_to_primary_for_non_unary(self):
        """Test delegation to _parse_primary for non-unary tokens"""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            {"type": "PLUS", "value": "+", "line": 1, "column": 2}
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.py"}
        
        expected_result = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 1
        }
        
        with patch("._parse_primary_package._parse_primary_src._parse_primary", return_value=expected_result) as mock_primary:
            result = _parse_unary(parser_state)
        
        self.assertEqual(result, expected_result)
        mock_primary.assert_called_once_with(parser_state)
        self.assertEqual(parser_state["pos"], 0)
    
    def test_delegates_for_binary_operator(self):
        """Test delegation for binary operators like PLUS in binary context"""
        tokens = [
            {"type": "PLUS", "value": "+", "line": 1, "column": 1},
            {"type": "NUMBER", "value": "5", "line": 1, "column": 2}
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.py"}
        
        expected_result = {
            "type": "NUMBER",
            "value": "5",
            "line": 1,
            "column": 2
        }
        
        with patch("._parse_primary_package._parse_primary_src._parse_primary", return_value=expected_result) as mock_primary:
            result = _parse_unary(parser_state)
        
        self.assertEqual(result, expected_result)
        mock_primary.assert_called_once()
    
    def test_error_propagation_from_primary(self):
        """Test error propagation when _parse_primary sets error"""
        tokens = [
            {"type": "MINUS", "value": "-", "line": 1, "column": 1},
            {"type": "INVALID", "value": "?", "line": 1, "column": 2}
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.py"}
        
        error_node = {
            "type": "ERROR",
            "value": None,
            "line": -1,
            "column": -1
        }
        
        def mock_primary_with_error(state):
            state["error"] = "Invalid token in primary expression"
            state["pos"] = 2
            return error_node
        
        with patch("._parse_primary_package._parse_primary_src._parse_primary", side_effect=mock_primary_with_error):
            result = _parse_unary(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(parser_state["error"], "Invalid token in primary expression")
    
    def test_multiple_different_unary_operators(self):
        """Test chain of different unary operators (!-+x)"""
        tokens = [
            {"type": "NOT", "value": "!", "line": 1, "column": 1},
            {"type": "MINUS", "value": "-", "line": 1, "column": 2},
            {"type": "PLUS", "value": "+", "line": 1, "column": 3},
            {"type": "NUMBER", "value": "5", "line": 1, "column": 4}
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.py"}
        
        expected_operand = {
            "type": "NUMBER",
            "value": "5",
            "line": 1,
            "column": 4
        }
        
        def mock_primary_side_effect(state):
            state["pos"] = 4
            return expected_operand
        
        with patch("._parse_primary_package._parse_primary_src._parse_primary", side_effect=mock_primary_side_effect):
            result = _parse_unary(parser_state)
        
        self.assertEqual(result["type"], "UNARY_OP")
        self.assertEqual(result["operator"], "!")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        
        middle_unary = result["children"][0]
        self.assertEqual(middle_unary["type"], "UNARY_OP")
        self.assertEqual(middle_unary["operator"], "-")
        self.assertEqual(middle_unary["line"], 1)
        self.assertEqual(middle_unary["column"], 2)
        
        inner_unary = middle_unary["children"][0]
        self.assertEqual(inner_unary["type"], "UNARY_OP")
        self.assertEqual(inner_unary["operator"], "+")
        self.assertEqual(inner_unary["line"], 1)
        self.assertEqual(inner_unary["column"], 3)
        
        self.assertEqual(inner_unary["children"][0], expected_operand)
        self.assertEqual(parser_state["pos"], 4)


if __name__ == "__main__":
    unittest.main()

# === std / third-party imports ===
import unittest
from typing import Any, Dict
from unittest.mock import patch

# === sub function imports ===
from ._parse_list_literal_src import _parse_list_literal

# === ADT defines ===
Token = Dict[str, Any]
AST = Dict[str, Any]
ParserState = Dict[str, Any]

# === Test Cases ===
class TestParseListLiteral(unittest.TestCase):
    """Test cases for _parse_list_literal function."""

    def test_empty_list(self):
        """Test parsing empty list []."""
        tokens = [
            {"type": "LBRACKET", "value": "[", "line": 1, "column": 1},
            {"type": "RBRACKET", "value": "]", "line": 1, "column": 2}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 1,
            "filename": "test.py",
            "error": ""
        }
        lbracket_token = tokens[0]
        
        result = _parse_list_literal(parser_state, lbracket_token)
        
        self.assertEqual(result["type"], "LIST")
        self.assertEqual(result["value"], None)
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(result["children"], [])
        self.assertEqual(parser_state["pos"], 2)

    def test_single_element_list(self):
        """Test parsing list with single element [elem]."""
        tokens = [
            {"type": "LBRACKET", "value": "[", "line": 1, "column": 1},
            {"type": "NUMBER", "value": "42", "line": 1, "column": 2},
            {"type": "RBRACKET", "value": "]", "line": 1, "column": 3}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 1,
            "filename": "test.py",
            "error": ""
        }
        lbracket_token = tokens[0]
        
        with patch("._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = {
                "type": "NUMBER",
                "value": "42",
                "line": 1,
                "column": 2,
                "children": []
            }
            
            result = _parse_list_literal(parser_state, lbracket_token)
            
            self.assertEqual(result["type"], "LIST")
            self.assertEqual(result["value"], None)
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(result["children"][0]["type"], "NUMBER")
            self.assertEqual(result["children"][0]["value"], "42")
            self.assertEqual(parser_state["pos"], 3)
            mock_parse_expr.assert_called_once()

    def test_multiple_elements_list(self):
        """Test parsing list with multiple elements [elem1, elem2, elem3]."""
        tokens = [
            {"type": "LBRACKET", "value": "[", "line": 1, "column": 1},
            {"type": "NUMBER", "value": "1", "line": 1, "column": 2},
            {"type": "COMMA", "value": ",", "line": 1, "column": 3},
            {"type": "NUMBER", "value": "2", "line": 1, "column": 4},
            {"type": "COMMA", "value": ",", "line": 1, "column": 5},
            {"type": "NUMBER", "value": "3", "line": 1, "column": 6},
            {"type": "RBRACKET", "value": "]", "line": 1, "column": 7}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 1,
            "filename": "test.py",
            "error": ""
        }
        lbracket_token = tokens[0]
        
        with patch("._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.side_effect = [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 2, "children": []},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 4, "children": []},
                {"type": "NUMBER", "value": "3", "line": 1, "column": 6, "children": []}
            ]
            
            result = _parse_list_literal(parser_state, lbracket_token)
            
            self.assertEqual(result["type"], "LIST")
            self.assertEqual(len(result["children"]), 3)
            self.assertEqual(result["children"][0]["value"], "1")
            self.assertEqual(result["children"][1]["value"], "2")
            self.assertEqual(result["children"][2]["value"], "3")
            self.assertEqual(parser_state["pos"], 7)
            self.assertEqual(mock_parse_expr.call_count, 3)

    def test_expression_returns_error(self):
        """Test when _parse_expression returns ERROR node."""
        tokens = [
            {"type": "LBRACKET", "value": "[", "line": 1, "column": 1},
            {"type": "INVALID", "value": "x", "line": 1, "column": 2}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 1,
            "filename": "test.py",
            "error": ""
        }
        lbracket_token = tokens[0]
        
        with patch("._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = {
                "type": "ERROR",
                "value": "Invalid expression",
                "line": 1,
                "column": 2,
                "children": []
            }
            
            result = _parse_list_literal(parser_state, lbracket_token)
            
            self.assertEqual(result["type"], "ERROR")
            self.assertEqual(result["value"], "Invalid expression")
            mock_parse_expr.assert_called_once()

    def test_unexpected_end_of_input(self):
        """Test when list ends without RBRACKET."""
        tokens = [
            {"type": "LBRACKET", "value": "[", "line": 1, "column": 1},
            {"type": "NUMBER", "value": "42", "line": 1, "column": 2}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 1,
            "filename": "test.py",
            "error": ""
        }
        lbracket_token = tokens[0]
        
        with patch("._parse_list_literal_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = {
                "type": "NUMBER",
                "value": "42",
                "line": 1,
                "column": 2,
                "children": []
            }
            
            result = _parse_list_literal(parser_state, lbracket_token)
            
            self.assertEqual(result["type"], "ERROR")
            self.assertEqual(result["value"], "Unexpected end of input in list literal")
            self.assertEqual(parser_state["error"], "Unexpected end of input in list literal")

    def test_missing_comma_or_rbracket(self):
        """Test when element is followed by unexpected token."""
        tokens = [
            {"type": "LBRACKET", "value": "[", "line": 1, "column": 1},
            {"type": "NUMBER", "value": "1", "line": 1, "column": 2},
            {"type": "SEMICOLON", "value": ";", "line": 1, "column": 3}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 1,
            "filename": "test.py",
            "error": ""
        }
        lbracket_token = tokens[0]
        
        with patch("._parse_list_literal_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = {
                "type": "NUMBER",
                "value": "1",
                "line": 1,
                "column": 2,
                "children": []
            }
            
            result = _parse_list_literal(parser_state, lbracket_token)
            
            self.assertEqual(result["type"], "ERROR")
            self.assertIn("Expected COMMA or RBRACKET", result["value"])
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 3)

    def test_list_at_end_of_tokens(self):
        """Test parsing list when it's at the end of token stream."""
        tokens = [
            {"type": "LBRACKET", "value": "[", "line": 1, "column": 1},
            {"type": "RBRACKET", "value": "]", "line": 1, "column": 2}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 1,
            "filename": "test.py",
            "error": ""
        }
        lbracket_token = tokens[0]
        
        result = _parse_list_literal(parser_state, lbracket_token)
        
        self.assertEqual(result["type"], "LIST")
        self.assertEqual(parser_state["pos"], 2)

    def test_position_updated_correctly(self):
        """Test that parser_state position is updated correctly through parsing."""
        tokens = [
            {"type": "LBRACKET", "value": "[", "line": 1, "column": 1},
            {"type": "NUMBER", "value": "1", "line": 1, "column": 2},
            {"type": "COMMA", "value": ",", "line": 1, "column": 3},
            {"type": "NUMBER", "value": "2", "line": 1, "column": 4},
            {"type": "RBRACKET", "value": "]", "line": 1, "column": 5}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 1,
            "filename": "test.py",
            "error": ""
        }
        lbracket_token = tokens[0]
        
        with patch("._parse_list_literal_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.side_effect = [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 2, "children": []},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 4, "children": []}
            ]
            
            result = _parse_list_literal(parser_state, lbracket_token)
            
            self.assertEqual(result["type"], "LIST")
            self.assertEqual(parser_state["pos"], 5)
            self.assertEqual(len(result["children"]), 2)


if __name__ == "__main__":
    unittest.main()

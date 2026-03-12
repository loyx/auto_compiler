import unittest
from unittest.mock import patch
from typing import Dict, Any

from ._parse_list_literal_package._parse_list_literal_src import _parse_list_literal


class TestParseListLiteral(unittest.TestCase):
    """Test cases for _parse_list_literal function."""
    
    def _create_token(self, token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """Helper to create a token dict."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }
    
    def _create_ast_node(self, node_type: str, children: list = None, value: Any = None, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """Helper to create an AST node dict."""
        return {
            "type": node_type,
            "children": children or [],
            "value": value,
            "line": line,
            "column": column
        }
    
    def test_empty_list(self):
        """Test parsing empty list []."""
        tokens = [
            self._create_token("LBRACKET", "[", 1, 1),
            self._create_token("RBRACKET", "]", 1, 2),
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
            "error": None
        }
        
        result = _parse_list_literal(parser_state)
        
        self.assertEqual(result["type"], "LIST_LITERAL")
        self.assertEqual(result["children"], [])
        self.assertEqual(result["value"], None)
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 2)
        self.assertIsNone(parser_state.get("error"))
    
    def test_single_element_list(self):
        """Test parsing list with single element [expr]."""
        tokens = [
            self._create_token("LBRACKET", "[", 1, 1),
            self._create_token("NUMBER", "42", 1, 3),
            self._create_token("RBRACKET", "]", 1, 5),
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
            "error": None
        }
        
        mock_expr = self._create_ast_node("NUMBER", value=42)
        
        with patch("._parse_list_literal_package._parse_list_literal_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = mock_expr
            
            result = _parse_list_literal(parser_state)
            
            self.assertEqual(result["type"], "LIST_LITERAL")
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(result["children"][0]["type"], "NUMBER")
            self.assertEqual(result["children"][0]["value"], 42)
            self.assertEqual(parser_state["pos"], 2)
            mock_parse_expr.assert_called_once()
    
    def test_multiple_elements_list(self):
        """Test parsing list with multiple elements [expr1, expr2, expr3]."""
        tokens = [
            self._create_token("LBRACKET", "[", 1, 1),
            self._create_token("NUMBER", "42", 1, 3),
            self._create_token("COMMA", ",", 1, 5),
            self._create_token("NUMBER", "100", 1, 7),
            self._create_token("COMMA", ",", 1, 10),
            self._create_token("NUMBER", "200", 1, 12),
            self._create_token("RBRACKET", "]", 1, 15),
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
            "error": None
        }
        
        mock_expr1 = self._create_ast_node("NUMBER", value=42)
        mock_expr2 = self._create_ast_node("NUMBER", value=100)
        mock_expr3 = self._create_ast_node("NUMBER", value=200)
        
        with patch("._parse_list_literal_package._parse_list_literal_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.side_effect = [mock_expr1, mock_expr2, mock_expr3]
            
            result = _parse_list_literal(parser_state)
            
            self.assertEqual(result["type"], "LIST_LITERAL")
            self.assertEqual(len(result["children"]), 3)
            self.assertEqual(result["children"][0]["value"], 42)
            self.assertEqual(result["children"][1]["value"], 100)
            self.assertEqual(result["children"][2]["value"], 200)
            self.assertEqual(parser_state["pos"], 7)
            self.assertEqual(mock_parse_expr.call_count, 3)
    
    def test_unexpected_end_of_input_at_start(self):
        """Test parsing when tokens are exhausted before finding '['."""
        tokens = []
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
            "error": None
        }
        
        result = _parse_list_literal(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertIn("Unexpected end of input", parser_state.get("error", ""))
        self.assertEqual(parser_state["pos"], 0)
    
    def test_wrong_starting_token(self):
        """Test parsing when current token is not '['."""
        tokens = [
            self._create_token("NUMBER", "42", 1, 1),
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
            "error": None
        }
        
        result = _parse_list_literal(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertIn("Expected '['", parser_state.get("error", ""))
        self.assertEqual(parser_state["pos"], 0)
    
    def test_missing_closing_bracket(self):
        """Test parsing list without closing bracket."""
        tokens = [
            self._create_token("LBRACKET", "[", 1, 1),
            self._create_token("NUMBER", "42", 1, 3),
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
            "error": None
        }
        
        mock_expr = self._create_ast_node("NUMBER", value=42)
        
        with patch("._parse_list_literal_package._parse_list_literal_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = mock_expr
            
            result = _parse_list_literal(parser_state)
            
            self.assertEqual(result["type"], "ERROR")
            self.assertIn("Unexpected end of input", parser_state.get("error", ""))
    
    def test_missing_comma_between_elements(self):
        """Test parsing list with missing comma between elements."""
        tokens = [
            self._create_token("LBRACKET", "[", 1, 1),
            self._create_token("NUMBER", "42", 1, 3),
            self._create_token("NUMBER", "100", 1, 6),
            self._create_token("RBRACKET", "]", 1, 9),
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
            "error": None
        }
        
        mock_expr = self._create_ast_node("NUMBER", value=42)
        
        with patch("._parse_list_literal_package._parse_list_literal_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = mock_expr
            
            result = _parse_list_literal(parser_state)
            
            self.assertEqual(result["type"], "ERROR")
            self.assertIn("Expected ',' or ']'", parser_state.get("error", ""))
    
    def test_parse_expression_error_propagation(self):
        """Test that errors from _parse_expression are propagated."""
        tokens = [
            self._create_token("LBRACKET", "[", 1, 1),
            self._create_token("NUMBER", "42", 1, 3),
            self._create_token("RBRACKET", "]", 1, 5),
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
            "error": None
        }
        
        error_node = self._create_ast_node("ERROR", value="Expression parse error")
        
        with patch("._parse_list_literal_package._parse_list_literal_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = error_node
            parser_state["error"] = "Expression parse error"
            
            result = _parse_list_literal(parser_state)
            
            self.assertEqual(result["type"], "ERROR")
            self.assertEqual(parser_state["error"], "Expression parse error")
    
    def test_position_update(self):
        """Test that parser_state position is updated correctly."""
        tokens = [
            self._create_token("LBRACKET", "[", 1, 1),
            self._create_token("NUMBER", "42", 1, 3),
            self._create_token("RBRACKET", "]", 1, 5),
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
            "error": None
        }
        
        mock_expr = self._create_ast_node("NUMBER", value=42)
        
        with patch("._parse_list_literal_package._parse_list_literal_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = mock_expr
            
            result = _parse_list_literal(parser_state)
            
            self.assertEqual(parser_state["pos"], 2)
            self.assertEqual(result["type"], "LIST_LITERAL")
    
    def test_start_position_recorded(self):
        """Test that start line and column are recorded from '[' token."""
        tokens = [
            self._create_token("LBRACKET", "[", 5, 10),
            self._create_token("RBRACKET", "]", 5, 11),
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
            "error": None
        }
        
        result = _parse_list_literal(parser_state)
        
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 10)
    
    def test_trailing_comma(self):
        """Test parsing list with trailing comma before ]."""
        tokens = [
            self._create_token("LBRACKET", "[", 1, 1),
            self._create_token("NUMBER", "42", 1, 3),
            self._create_token("COMMA", ",", 1, 5),
            self._create_token("RBRACKET", "]", 1, 6),
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
            "error": None
        }
        
        mock_expr = self._create_ast_node("NUMBER", value=42)
        
        with patch("._parse_list_literal_package._parse_list_literal_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = mock_expr
            
            result = _parse_list_literal(parser_state)
            
            self.assertEqual(result["type"], "LIST_LITERAL")
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(parser_state["pos"], 4)
    
    def test_empty_tokens_list(self):
        """Test parsing with empty tokens list."""
        tokens = []
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
            "error": None
        }
        
        result = _parse_list_literal(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertIn("Unexpected end of input", parser_state.get("error", ""))


if __name__ == "__main__":
    unittest.main()

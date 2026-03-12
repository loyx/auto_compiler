import unittest
from unittest.mock import patch

from ._parse_unary_op_src import _parse_unary_op


class TestParseUnaryOp(unittest.TestCase):
    """Test cases for _parse_unary_op function."""
    
    def test_parse_minus_operator(self):
        """Test parsing MINUS unary operator."""
        parser_state = {
            "tokens": [
                {"type": "MINUS", "value": "-", "line": 1, "column": 5},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 6}
            ],
            "filename": "test.py",
            "pos": 0
        }
        
        mock_operand = {
            "type": "identifier",
            "name": "x",
            "line": 1,
            "column": 6
        }
        
        with patch("._parse_primary_package._parse_primary_src._parse_primary") as mock_parse_primary:
            mock_parse_primary.return_value = mock_operand
            
            result = _parse_unary_op(parser_state)
            
            self.assertIsNotNone(result)
            self.assertEqual(result["type"], "unary_op")
            self.assertEqual(result["operator"], "-")
            self.assertEqual(result["operand"], mock_operand)
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 5)
            self.assertEqual(parser_state["pos"], 1)
    
    def test_parse_not_operator(self):
        """Test parsing NOT unary operator."""
        parser_state = {
            "tokens": [
                {"type": "NOT", "value": "not", "line": 2, "column": 3},
                {"type": "IDENTIFIER", "value": "flag", "line": 2, "column": 7}
            ],
            "filename": "test.py",
            "pos": 0
        }
        
        mock_operand = {
            "type": "identifier",
            "name": "flag",
            "line": 2,
            "column": 7
        }
        
        with patch("._parse_primary_package._parse_primary_src._parse_primary") as mock_parse_primary:
            mock_parse_primary.return_value = mock_operand
            
            result = _parse_unary_op(parser_state)
            
            self.assertIsNotNone(result)
            self.assertEqual(result["type"], "unary_op")
            self.assertEqual(result["operator"], "not")
            self.assertEqual(result["operand"], mock_operand)
            self.assertEqual(result["line"], 2)
            self.assertEqual(result["column"], 3)
            self.assertEqual(parser_state["pos"], 1)
    
    def test_parse_tilde_operator(self):
        """Test parsing TILDE unary operator."""
        parser_state = {
            "tokens": [
                {"type": "TILDE", "value": "~", "line": 2, "column": 3},
                {"type": "IDENTIFIER", "value": "x", "line": 2, "column": 4}
            ],
            "filename": "test.py",
            "pos": 0
        }
        
        mock_operand = {
            "type": "identifier",
            "name": "x",
            "line": 2,
            "column": 4
        }
        
        with patch("._parse_primary_package._parse_primary_src._parse_primary") as mock_parse_primary:
            mock_parse_primary.return_value = mock_operand
            
            result = _parse_unary_op(parser_state)
            
            self.assertIsNotNone(result)
            self.assertEqual(result["type"], "unary_op")
            self.assertEqual(result["operator"], "~")
            self.assertEqual(result["operand"], mock_operand)
            self.assertEqual(result["line"], 2)
            self.assertEqual(result["column"], 3)
            self.assertEqual(parser_state["pos"], 1)
    
    def test_no_tokens_returns_none(self):
        """Test that empty token list returns None."""
        parser_state = {
            "tokens": [],
            "filename": "test.py",
            "pos": 0
        }
        
        result = _parse_unary_op(parser_state)
        
        self.assertIsNone(result)
        self.assertEqual(parser_state["pos"], 0)
    
    def test_pos_beyond_tokens_returns_none(self):
        """Test that pos beyond token list returns None."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "filename": "test.py",
            "pos": 1
        }
        
        result = _parse_unary_op(parser_state)
        
        self.assertIsNone(result)
        self.assertEqual(parser_state["pos"], 1)
    
    def test_non_unary_operator_returns_none(self):
        """Test that non-unary operator token returns None."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "filename": "test.py",
            "pos": 0
        }
        
        result = _parse_unary_op(parser_state)
        
        self.assertIsNone(result)
        self.assertEqual(parser_state["pos"], 0)
    
    def test_syntax_error_when_operand_parsing_fails(self):
        """Test that SyntaxError is raised when operand parsing fails."""
        parser_state = {
            "tokens": [
                {"type": "MINUS", "value": "-", "line": 1, "column": 5}
            ],
            "filename": "test.py",
            "pos": 0
        }
        
        with patch("._parse_primary_package._parse_primary_src._parse_primary") as mock_parse_primary:
            mock_parse_primary.return_value = None
            
            with self.assertRaises(SyntaxError) as context:
                _parse_unary_op(parser_state)
            
            self.assertIn("test.py:1:5", str(context.exception))
            self.assertIn("Expected expression after unary operator", str(context.exception))
            self.assertEqual(parser_state["pos"], 0)
    
    def test_pos_advanced_after_successful_parse(self):
        """Test that pos is correctly advanced after successful parsing."""
        parser_state = {
            "tokens": [
                {"type": "MINUS", "value": "-", "line": 1, "column": 1},
                {"type": "NUMBER", "value": "42", "line": 1, "column": 2},
                {"type": "PLUS", "value": "+", "line": 1, "column": 3}
            ],
            "filename": "test.py",
            "pos": 0
        }
        
        mock_operand = {"type": "number", "value": 42, "line": 1, "column": 2}
        
        with patch("._parse_primary_package._parse_primary_src._parse_primary") as mock_parse_primary:
            mock_parse_primary.return_value = mock_operand
            
            result = _parse_unary_op(parser_state)
            
            self.assertIsNotNone(result)
            self.assertEqual(parser_state["pos"], 1)
    
    def test_ast_structure_completeness(self):
        """Test that the returned AST has all required fields."""
        parser_state = {
            "tokens": [
                {"type": "NOT", "value": "not", "line": 5, "column": 10}
            ],
            "filename": "test.py",
            "pos": 0
        }
        
        mock_operand = {"type": "identifier", "name": "x", "line": 5, "column": 14}
        
        with patch("._parse_primary_package._parse_primary_src._parse_primary") as mock_parse_primary:
            mock_parse_primary.return_value = mock_operand
            
            result = _parse_unary_op(parser_state)
            
            self.assertIn("type", result)
            self.assertIn("operator", result)
            self.assertIn("operand", result)
            self.assertIn("line", result)
            self.assertIn("column", result)
            
            self.assertEqual(result["type"], "unary_op")
    
    def test_nested_unary_operators(self):
        """Test parsing nested unary operators like --x."""
        parser_state = {
            "tokens": [
                {"type": "MINUS", "value": "-", "line": 1, "column": 1},
                {"type": "MINUS", "value": "-", "line": 1, "column": 2},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 3}
            ],
            "filename": "test.py",
            "pos": 0
        }
        
        inner_unary = {
            "type": "unary_op",
            "operator": "-",
            "operand": {"type": "identifier", "name": "x", "line": 1, "column": 3},
            "line": 1,
            "column": 2
        }
        
        with patch("._parse_primary_package._parse_primary_src._parse_primary") as mock_parse_primary:
            mock_parse_primary.return_value = inner_unary
            
            result = _parse_unary_op(parser_state)
            
            self.assertIsNotNone(result)
            self.assertEqual(result["type"], "unary_op")
            self.assertEqual(result["operator"], "-")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            self.assertEqual(result["operand"], inner_unary)
    
    def test_unknown_token_type_returns_none(self):
        """Test that unknown token types return None."""
        parser_state = {
            "tokens": [
                {"type": "UNKNOWN", "value": "?", "line": 1, "column": 1}
            ],
            "filename": "test.py",
            "pos": 0
        }
        
        result = _parse_unary_op(parser_state)
        
        self.assertIsNone(result)
        self.assertEqual(parser_state["pos"], 0)
    
    def test_binary_operator_returns_none(self):
        """Test that binary operators return None."""
        parser_state = {
            "tokens": [
                {"type": "PLUS", "value": "+", "line": 1, "column": 1}
            ],
            "filename": "test.py",
            "pos": 0
        }
        
        result = _parse_unary_op(parser_state)
        
        self.assertIsNone(result)
        self.assertEqual(parser_state["pos"], 0)
    
    def test_default_filename_in_error(self):
        """Test error message when filename is not provided."""
        parser_state = {
            "tokens": [
                {"type": "MINUS", "value": "-", "line": 1, "column": 5}
            ],
            "pos": 0
        }
        
        with patch("._parse_primary_package._parse_primary_src._parse_primary") as mock_parse_primary:
            mock_parse_primary.return_value = None
            
            with self.assertRaises(SyntaxError) as context:
                _parse_unary_op(parser_state)
            
            self.assertIn("<unknown>:1:5", str(context.exception))


if __name__ == "__main__":
    unittest.main()

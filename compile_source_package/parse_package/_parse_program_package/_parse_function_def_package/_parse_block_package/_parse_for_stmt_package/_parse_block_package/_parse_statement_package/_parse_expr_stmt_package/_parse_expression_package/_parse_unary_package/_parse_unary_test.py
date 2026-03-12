import unittest
from unittest.mock import patch

# Relative import for the function under test
from ._parse_unary_src import _parse_unary


class TestParseUnary(unittest.TestCase):
    """Test cases for _parse_unary function."""
    
    def setUp(self):
        """Set up test fixtures."""
        pass
    
    def tearDown(self):
        """Tear down test fixtures."""
        pass
    
    def test_parse_negative_number(self):
        """Test parsing negative unary operator with a number."""
        tokens = [
            {"type": "OPERATOR", "value": "-", "line": 1, "column": 1},
            {"type": "NUMBER", "value": "42", "line": 1, "column": 2}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.txt"
        }
        
        with patch("._parse_primary_package._parse_primary_src._parse_primary") as mock_parse_primary:
            mock_parse_primary.return_value = {"type": "NUMBER", "value": "42", "line": 1, "column": 2}
            
            result = _parse_unary(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "-")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(parser_state["pos"], 1)
            mock_parse_primary.assert_called_once()
    
    def test_parse_logical_not(self):
        """Test parsing logical not unary operator."""
        tokens = [
            {"type": "OPERATOR", "value": "!", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "flag", "line": 1, "column": 2}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.txt"
        }
        
        with patch("._parse_primary_package._parse_primary_src._parse_primary") as mock_parse_primary:
            mock_parse_primary.return_value = {"type": "IDENTIFIER", "value": "flag", "line": 1, "column": 2}
            
            result = _parse_unary(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "!")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(parser_state["pos"], 1)
    
    def test_parse_chained_negative_ops(self):
        """Test parsing chained unary operators like --x."""
        tokens = [
            {"type": "OPERATOR", "value": "-", "line": 1, "column": 1},
            {"type": "OPERATOR", "value": "-", "line": 1, "column": 2},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 3}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.txt"
        }
        
        with patch("._parse_primary_package._parse_primary_src._parse_primary") as mock_parse_primary:
            mock_parse_primary.return_value = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 3}
            
            result = _parse_unary(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "-")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(result["children"][0]["type"], "UNARY_OP")
            self.assertEqual(result["children"][0]["value"], "-")
            self.assertEqual(parser_state["pos"], 2)
    
    def test_parse_chained_logical_not_ops(self):
        """Test parsing chained logical not operators like !!x."""
        tokens = [
            {"type": "OPERATOR", "value": "!", "line": 1, "column": 1},
            {"type": "OPERATOR", "value": "!", "line": 1, "column": 2},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 3}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.txt"
        }
        
        with patch("._parse_primary_package._parse_primary_src._parse_primary") as mock_parse_primary:
            mock_parse_primary.return_value = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 3}
            
            result = _parse_unary(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "!")
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(result["children"][0]["type"], "UNARY_OP")
            self.assertEqual(result["children"][0]["value"], "!")
            self.assertEqual(parser_state["pos"], 2)
    
    def test_parse_mixed_chained_unary_ops(self):
        """Test parsing mixed chained unary operators like -!x."""
        tokens = [
            {"type": "OPERATOR", "value": "-", "line": 1, "column": 1},
            {"type": "OPERATOR", "value": "!", "line": 1, "column": 2},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 3}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.txt"
        }
        
        with patch("._parse_primary_package._parse_primary_src._parse_primary") as mock_parse_primary:
            mock_parse_primary.return_value = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 3}
            
            result = _parse_unary(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "-")
            self.assertEqual(result["children"][0]["type"], "UNARY_OP")
            self.assertEqual(result["children"][0]["value"], "!")
            self.assertEqual(parser_state["pos"], 2)
    
    def test_parse_non_unary_expression_delegates_to_primary(self):
        """Test parsing non-unary expression delegates to _parse_primary."""
        tokens = [
            {"type": "NUMBER", "value": "42", "line": 1, "column": 1}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.txt"
        }
        
        with patch("._parse_primary_package._parse_primary_src._parse_primary") as mock_parse_primary:
            expected_result = {"type": "NUMBER", "value": "42", "line": 1, "column": 1}
            mock_parse_primary.return_value = expected_result
            
            result = _parse_unary(parser_state)
            
            self.assertEqual(result, expected_result)
            self.assertEqual(parser_state["pos"], 0)
            mock_parse_primary.assert_called_once_with(parser_state)
    
    def test_empty_tokens_raises_syntax_error(self):
        """Test that empty tokens list raises SyntaxError."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.txt"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_unary(parser_state)
        
        self.assertIn("Unexpected end of input while parsing unary expression", str(context.exception))
    
    def test_position_at_end_raises_syntax_error(self):
        """Test that position at end of tokens raises SyntaxError."""
        tokens = [
            {"type": "NUMBER", "value": "42", "line": 1, "column": 1}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 1,
            "filename": "test.txt"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_unary(parser_state)
        
        self.assertIn("Unexpected end of input while parsing unary expression", str(context.exception))
    
    def test_position_beyond_end_raises_syntax_error(self):
        """Test that position beyond end of tokens raises SyntaxError."""
        tokens = [
            {"type": "NUMBER", "value": "42", "line": 1, "column": 1}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 5,
            "filename": "test.txt"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_unary(parser_state)
        
        self.assertIn("Unexpected end of input while parsing unary expression", str(context.exception))
    
    def test_preserves_line_column_info(self):
        """Test that line and column information is preserved in AST."""
        tokens = [
            {"type": "OPERATOR", "value": "-", "line": 5, "column": 10},
            {"type": "NUMBER", "value": "42", "line": 5, "column": 11}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.txt"
        }
        
        with patch("._parse_primary_package._parse_primary_src._parse_primary") as mock_parse_primary:
            mock_parse_primary.return_value = {"type": "NUMBER", "value": "42", "line": 5, "column": 11}
            
            result = _parse_unary(parser_state)
            
            self.assertEqual(result["line"], 5)
            self.assertEqual(result["column"], 10)
    
    def test_other_operator_delegates_to_primary(self):
        """Test that other operators (not - or !) delegate to _parse_primary."""
        tokens = [
            {"type": "OPERATOR", "value": "+", "line": 1, "column": 1},
            {"type": "NUMBER", "value": "42", "line": 1, "column": 2}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.txt"
        }
        
        with patch("._parse_primary_package._parse_primary_src._parse_primary") as mock_parse_primary:
            expected_result = {"type": "NUMBER", "value": "42", "line": 1, "column": 2}
            mock_parse_primary.return_value = expected_result
            
            result = _parse_unary(parser_state)
            
            self.assertEqual(result, expected_result)
            self.assertEqual(parser_state["pos"], 0)
            mock_parse_primary.assert_called_once()
    
    def test_identifier_token_delegates_to_primary(self):
        """Test that identifier token delegates to _parse_primary."""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.txt"
        }
        
        with patch("._parse_primary_package._parse_primary_src._parse_primary") as mock_parse_primary:
            expected_result = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            mock_parse_primary.return_value = expected_result
            
            result = _parse_unary(parser_state)
            
            self.assertEqual(result, expected_result)
            mock_parse_primary.assert_called_once()
    
    def test_string_token_delegates_to_primary(self):
        """Test that string token delegates to _parse_primary."""
        tokens = [
            {"type": "STRING", "value": "hello", "line": 1, "column": 1}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.txt"
        }
        
        with patch("._parse_primary_package._parse_primary_src._parse_primary") as mock_parse_primary:
            expected_result = {"type": "STRING", "value": "hello", "line": 1, "column": 1}
            mock_parse_primary.return_value = expected_result
            
            result = _parse_unary(parser_state)
            
            self.assertEqual(result, expected_result)
            mock_parse_primary.assert_called_once()


if __name__ == "__main__":
    unittest.main()

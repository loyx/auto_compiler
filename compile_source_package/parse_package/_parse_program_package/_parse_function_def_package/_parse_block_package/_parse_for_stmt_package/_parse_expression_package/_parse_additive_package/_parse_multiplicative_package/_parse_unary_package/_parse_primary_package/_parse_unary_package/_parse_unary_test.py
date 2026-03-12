import unittest
from unittest.mock import patch

# Import the function under test using relative import
from ._parse_unary_src import _parse_unary


class TestParseUnary(unittest.TestCase):
    """Test cases for _parse_unary function."""
    
    def test_parse_minus_unary(self):
        """Test parsing a single MINUS unary operator."""
        tokens = [
            {"type": "MINUS", "value": "-", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 2}
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.c"}
        
        with patch('._parse_unary_src._parse_primary') as mock_parse_primary:
            mock_parse_primary.return_value = {
                "type": "IDENTIFIER",
                "value": "x",
                "children": [],
                "line": 1,
                "column": 2
            }
            
            result = _parse_unary(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "-")
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(result["children"][0]["type"], "IDENTIFIER")
            self.assertEqual(parser_state["pos"], 1)
    
    def test_parse_not_unary(self):
        """Test parsing a single NOT unary operator."""
        tokens = [
            {"type": "NOT", "value": "!", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 2}
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.c"}
        
        with patch('._parse_unary_src._parse_primary') as mock_parse_primary:
            mock_parse_primary.return_value = {
                "type": "IDENTIFIER",
                "value": "x",
                "children": [],
                "line": 1,
                "column": 2
            }
            
            result = _parse_unary(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "!")
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(parser_state["pos"], 1)
    
    def test_parse_plus_unary(self):
        """Test parsing a single PLUS unary operator."""
        tokens = [
            {"type": "PLUS", "value": "+", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 2}
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.c"}
        
        with patch('._parse_unary_src._parse_primary') as mock_parse_primary:
            mock_parse_primary.return_value = {
                "type": "IDENTIFIER",
                "value": "x",
                "children": [],
                "line": 1,
                "column": 2
            }
            
            result = _parse_unary(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "+")
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(parser_state["pos"], 1)
    
    def test_parse_nested_unary_double_minus(self):
        """Test parsing nested unary operators (--x)."""
        tokens = [
            {"type": "MINUS", "value": "-", "line": 1, "column": 1},
            {"type": "MINUS", "value": "-", "line": 1, "column": 2},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 3}
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.c"}
        
        with patch('._parse_unary_src._parse_primary') as mock_parse_primary:
            mock_parse_primary.return_value = {
                "type": "IDENTIFIER",
                "value": "x",
                "children": [],
                "line": 1,
                "column": 3
            }
            
            result = _parse_unary(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "-")
            self.assertEqual(len(result["children"]), 1)
            
            inner_unary = result["children"][0]
            self.assertEqual(inner_unary["type"], "UNARY_OP")
            self.assertEqual(inner_unary["value"], "-")
            self.assertEqual(len(inner_unary["children"]), 1)
            self.assertEqual(inner_unary["children"][0]["type"], "IDENTIFIER")
            
            self.assertEqual(parser_state["pos"], 2)
    
    def test_parse_nested_unary_triple(self):
        """Test parsing triple nested unary operators (---x)."""
        tokens = [
            {"type": "MINUS", "value": "-", "line": 1, "column": 1},
            {"type": "MINUS", "value": "-", "line": 1, "column": 2},
            {"type": "MINUS", "value": "-", "line": 1, "column": 3},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 4}
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.c"}
        
        with patch('._parse_unary_src._parse_primary') as mock_parse_primary:
            mock_parse_primary.return_value = {
                "type": "IDENTIFIER",
                "value": "x",
                "children": [],
                "line": 1,
                "column": 4
            }
            
            result = _parse_unary(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "-")
            self.assertEqual(len(result["children"]), 1)
            
            second_unary = result["children"][0]
            self.assertEqual(second_unary["type"], "UNARY_OP")
            self.assertEqual(second_unary["value"], "-")
            
            third_unary = second_unary["children"][0]
            self.assertEqual(third_unary["type"], "UNARY_OP")
            self.assertEqual(third_unary["value"], "-")
            
            self.assertEqual(parser_state["pos"], 3)
    
    def test_parse_non_unary_delegates_to_primary(self):
        """Test that non-unary tokens delegate to _parse_primary."""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.c"}
        
        expected_primary = {
            "type": "IDENTIFIER",
            "value": "x",
            "children": [],
            "line": 1,
            "column": 1
        }
        
        with patch('._parse_unary_src._parse_primary') as mock_parse_primary:
            mock_parse_primary.return_value = expected_primary
            
            result = _parse_unary(parser_state)
            
            mock_parse_primary.assert_called_once_with(parser_state)
            self.assertEqual(result, expected_primary)
            self.assertEqual(parser_state["pos"], 0)
    
    def test_empty_tokens_error(self):
        """Test error handling when tokens list is empty."""
        parser_state = {"tokens": [], "pos": 0, "filename": "test.c"}
        
        result = _parse_unary(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertIn("Unexpected end of input", result["value"])
        self.assertEqual(parser_state.get("error"), "Unexpected end of input while parsing unary expression")
    
    def test_pos_out_of_bounds_error(self):
        """Test error handling when pos is out of bounds."""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        ]
        parser_state = {"tokens": tokens, "pos": 5, "filename": "test.c"}
        
        result = _parse_unary(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertIn("Unexpected end of input", result["value"])
        self.assertEqual(parser_state.get("error"), "Unexpected end of input while parsing unary expression")
    
    def test_error_propagation_from_recursive_call(self):
        """Test that errors from recursive unary parsing are propagated."""
        tokens = [
            {"type": "MINUS", "value": "-", "line": 1, "column": 1}
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.c"}
        
        result = _parse_unary(parser_state)
        
        self.assertEqual(result["type"], "UNARY_OP")
        self.assertEqual(result["value"], "-")
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0]["type"], "ERROR")
        self.assertIsNotNone(parser_state.get("error"))
    
    def test_unary_op_with_line_column_info(self):
        """Test that line and column information is preserved."""
        tokens = [
            {"type": "MINUS", "value": "-", "line": 5, "column": 10},
            {"type": "IDENTIFIER", "value": "x", "line": 5, "column": 11}
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.c"}
        
        with patch('._parse_unary_src._parse_primary') as mock_parse_primary:
            mock_parse_primary.return_value = {
                "type": "IDENTIFIER",
                "value": "x",
                "children": [],
                "line": 5,
                "column": 11
            }
            
            result = _parse_unary(parser_state)
            
            self.assertEqual(result["line"], 5)
            self.assertEqual(result["column"], 10)
    
    def test_missing_token_fields(self):
        """Test handling of tokens with missing fields."""
        tokens = [
            {"type": "MINUS"}
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.c"}
        
        with patch('._parse_unary_src._parse_primary') as mock_parse_primary:
            mock_parse_primary.return_value = {
                "type": "IDENTIFIER",
                "value": "x",
                "children": [],
                "line": 0,
                "column": 0
            }
            
            result = _parse_unary(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "")
            self.assertEqual(result["line"], 0)
            self.assertEqual(result["column"], 0)
    
    def test_mixed_unary_operators(self):
        """Test parsing mixed unary operators (-!+x)."""
        tokens = [
            {"type": "MINUS", "value": "-", "line": 1, "column": 1},
            {"type": "NOT", "value": "!", "line": 1, "column": 2},
            {"type": "PLUS", "value": "+", "line": 1, "column": 3},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 4}
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.c"}
        
        with patch('._parse_unary_src._parse_primary') as mock_parse_primary:
            mock_parse_primary.return_value = {
                "type": "IDENTIFIER",
                "value": "x",
                "children": [],
                "line": 1,
                "column": 4
            }
            
            result = _parse_unary(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "-")
            
            second_op = result["children"][0]
            self.assertEqual(second_op["type"], "UNARY_OP")
            self.assertEqual(second_op["value"], "!")
            
            third_op = second_op["children"][0]
            self.assertEqual(third_op["type"], "UNARY_OP")
            self.assertEqual(third_op["value"], "+")
            
            self.assertEqual(parser_state["pos"], 3)
    
    def test_parser_state_missing_pos(self):
        """Test handling when parser_state is missing pos field."""
        tokens = [
            {"type": "MINUS", "value": "-", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 2}
        ]
        parser_state = {"tokens": tokens, "filename": "test.c"}
        
        with patch('._parse_unary_src._parse_primary') as mock_parse_primary:
            mock_parse_primary.return_value = {
                "type": "IDENTIFIER",
                "value": "x",
                "children": [],
                "line": 1,
                "column": 2
            }
            
            result = _parse_unary(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "-")
            self.assertEqual(parser_state["pos"], 1)
    
    def test_parser_state_missing_tokens(self):
        """Test handling when parser_state is missing tokens field."""
        parser_state = {"pos": 0, "filename": "test.c"}
        
        result = _parse_unary(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertIn("Unexpected end of input", result["value"])


if __name__ == "__main__":
    unittest.main()

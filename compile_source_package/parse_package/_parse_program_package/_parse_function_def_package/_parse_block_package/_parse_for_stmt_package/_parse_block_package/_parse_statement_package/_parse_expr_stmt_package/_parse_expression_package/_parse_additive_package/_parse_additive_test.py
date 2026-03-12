import unittest
from unittest.mock import patch

# Relative import for the function under test
from ._parse_additive_src import _parse_additive


class TestParseAdditive(unittest.TestCase):
    """Test cases for _parse_additive function."""
    
    def test_single_operand_no_operator(self):
        """Test parsing a single operand without any + or - operators."""
        mock_ast = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 1
        }
        
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py",
            "error": None
        }
        
        with patch('._parse_multiplicative_package._parse_multiplicative_src._parse_multiplicative', return_value=mock_ast) as mock_parse_mult:
            result = _parse_additive(parser_state)
            
            self.assertEqual(result, mock_ast)
            self.assertEqual(parser_state["pos"], 0)
            mock_parse_mult.assert_called_once_with(parser_state)
    
    def test_simple_addition(self):
        """Test parsing a simple addition expression: a + b."""
        left_operand = {
            "type": "IDENTIFIER",
            "value": "a",
            "line": 1,
            "column": 1
        }
        right_operand = {
            "type": "IDENTIFIER",
            "value": "b",
            "line": 1,
            "column": 5
        }
        
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.py",
            "error": None
        }
        
        with patch('._parse_multiplicative_package._parse_multiplicative_src._parse_multiplicative', side_effect=[left_operand, right_operand]) as mock_parse_mult:
            result = _parse_additive(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "+")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 3)
            self.assertEqual(len(result["children"]), 2)
            self.assertEqual(result["children"][0], left_operand)
            self.assertEqual(result["children"][1], right_operand)
            self.assertEqual(parser_state["pos"], 2)
            self.assertEqual(mock_parse_mult.call_count, 2)
    
    def test_simple_subtraction(self):
        """Test parsing a simple subtraction expression: a - b."""
        left_operand = {
            "type": "NUMBER",
            "value": "10",
            "line": 1,
            "column": 1
        }
        right_operand = {
            "type": "NUMBER",
            "value": "5",
            "line": 1,
            "column": 5
        }
        
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "10", "line": 1, "column": 1},
                {"type": "MINUS", "value": "-", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "5", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.py",
            "error": None
        }
        
        with patch('._parse_multiplicative_package._parse_multiplicative_src._parse_multiplicative', side_effect=[left_operand, right_operand]) as mock_parse_mult:
            result = _parse_additive(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "-")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 3)
            self.assertEqual(len(result["children"]), 2)
            self.assertEqual(result["children"][0], left_operand)
            self.assertEqual(result["children"][1], right_operand)
            self.assertEqual(parser_state["pos"], 2)
    
    def test_multiple_operators_left_associative(self):
        """Test parsing multiple operators with left associativity: a + b - c."""
        operand_a = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        operand_b = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
        operand_c = {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 9}
        
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
                {"type": "MINUS", "value": "-", "line": 1, "column": 7},
                {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 9}
            ],
            "pos": 0,
            "filename": "test.py",
            "error": None
        }
        
        with patch('._parse_multiplicative_package._parse_multiplicative_src._parse_multiplicative', side_effect=[operand_a, operand_b, operand_c]) as mock_parse_mult:
            result = _parse_additive(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "-")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 7)
            self.assertEqual(len(result["children"]), 2)
            
            right_child = result["children"][1]
            self.assertEqual(right_child, operand_c)
            
            left_child = result["children"][0]
            self.assertEqual(left_child["type"], "BINARY_OP")
            self.assertEqual(left_child["value"], "+")
            self.assertEqual(left_child["children"][0], operand_a)
            self.assertEqual(left_child["children"][1], operand_b)
            
            self.assertEqual(parser_state["pos"], 4)
            self.assertEqual(mock_parse_mult.call_count, 3)
    
    def test_operator_at_end_raises_error(self):
        """Test that operator at end without right operand raises SyntaxError."""
        left_operand = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 1
        }
        
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.py",
            "error": None
        }
        
        def side_effect(state):
            if state["pos"] == 0:
                return left_operand
            else:
                raise SyntaxError("Expected expression after operator")
        
        with patch('._parse_multiplicative_package._parse_multiplicative_src._parse_multiplicative', side_effect=side_effect):
            with self.assertRaises(SyntaxError):
                _parse_additive(parser_state)
            
            self.assertEqual(parser_state["pos"], 1)
    
    def test_non_additive_operator_stops_loop(self):
        """Test that non-additive operators stop the additive parsing loop."""
        left_operand = {
            "type": "IDENTIFIER",
            "value": "a",
            "line": 1,
            "column": 1
        }
        right_operand = {
            "type": "IDENTIFIER",
            "value": "b",
            "line": 1,
            "column": 5
        }
        
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
                {"type": "STAR", "value": "*", "line": 1, "column": 7},
                {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 9}
            ],
            "pos": 0,
            "filename": "test.py",
            "error": None
        }
        
        with patch('._parse_multiplicative_package._parse_multiplicative_src._parse_multiplicative', side_effect=[left_operand, right_operand]) as mock_parse_mult:
            result = _parse_additive(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "+")
            self.assertEqual(parser_state["pos"], 2)
            self.assertEqual(mock_parse_mult.call_count, 2)
    
    def test_empty_tokens_handled_by_multiplicative(self):
        """Test that empty tokens list is handled by _parse_multiplicative."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py",
            "error": None
        }
        
        with patch('._parse_multiplicative_package._parse_multiplicative_src._parse_multiplicative', side_effect=IndexError("Token index out of range")):
            with self.assertRaises(IndexError):
                _parse_additive(parser_state)


if __name__ == '__main__':
    unittest.main()

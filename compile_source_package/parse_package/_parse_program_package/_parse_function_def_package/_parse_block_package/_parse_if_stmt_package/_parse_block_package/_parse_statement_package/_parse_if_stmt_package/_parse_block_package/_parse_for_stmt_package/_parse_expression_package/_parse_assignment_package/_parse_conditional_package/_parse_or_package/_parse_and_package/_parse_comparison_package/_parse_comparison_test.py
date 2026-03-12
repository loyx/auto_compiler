import unittest
from unittest.mock import patch

# Import using relative path
from ._parse_comparison_package._parse_comparison_src import _parse_comparison


class TestParseComparison(unittest.TestCase):
    
    def test_single_comparison_less_than(self):
        """Test single comparison with < operator"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "<", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
            ],
            "filename": "test.py",
            "pos": 0,
            "error": ""
        }
        
        left_operand = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        right_operand = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
        
        with patch("._parse_arithmetic_package._parse_arithmetic_src._parse_arithmetic") as mock_arithmetic:
            mock_arithmetic.side_effect = [left_operand, right_operand]
            
            result = _parse_comparison(parser_state)
            
            self.assertEqual(result["type"], "COMPARE")
            self.assertEqual(result["operator"], "<")
            self.assertEqual(result["left"], left_operand)
            self.assertEqual(result["right"], right_operand)
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 3)
            self.assertEqual(parser_state["pos"], 3)
    
    def test_single_comparison_equal(self):
        """Test single comparison with == operator"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 2, "column": 1},
                {"type": "OPERATOR", "value": "==", "line": 2, "column": 3},
                {"type": "NUMBER", "value": "5", "line": 2, "column": 6}
            ],
            "filename": "test.py",
            "pos": 0,
            "error": ""
        }
        
        left_operand = {"type": "IDENTIFIER", "value": "x", "line": 2, "column": 1}
        right_operand = {"type": "NUMBER", "value": "5", "line": 2, "column": 6}
        
        with patch("._parse_arithmetic_package._parse_arithmetic_src._parse_arithmetic") as mock_arithmetic:
            mock_arithmetic.side_effect = [left_operand, right_operand]
            
            result = _parse_comparison(parser_state)
            
            self.assertEqual(result["type"], "COMPARE")
            self.assertEqual(result["operator"], "==")
            self.assertEqual(result["left"], left_operand)
            self.assertEqual(result["right"], right_operand)
            self.assertEqual(parser_state["pos"], 3)
    
    def test_chained_comparison_left_associative(self):
        """Test chained comparisons are left-associative: a < b < c becomes ((a < b) < c)"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "<", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
                {"type": "OPERATOR", "value": "<", "line": 1, "column": 7},
                {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 9}
            ],
            "filename": "test.py",
            "pos": 0,
            "error": ""
        }
        
        operand_a = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        operand_b = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
        operand_c = {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 9}
        
        with patch("._parse_arithmetic_package._parse_arithmetic_src._parse_arithmetic") as mock_arithmetic:
            mock_arithmetic.side_effect = [operand_a, operand_b, operand_c]
            
            result = _parse_comparison(parser_state)
            
            # Should be left-associative: ((a < b) < c)
            self.assertEqual(result["type"], "COMPARE")
            self.assertEqual(result["operator"], "<")
            self.assertEqual(result["right"], operand_c)
            
            # Left side should be the first comparison (a < b)
            self.assertEqual(result["left"]["type"], "COMPARE")
            self.assertEqual(result["left"]["operator"], "<")
            self.assertEqual(result["left"]["left"], operand_a)
            self.assertEqual(result["left"]["right"], operand_b)
            
            self.assertEqual(parser_state["pos"], 5)
    
    def test_all_comparison_operators(self):
        """Test all comparison operators: ==, !=, <, >, <=, >="""
        operators = ["==", "!=", "<", ">", "<=", ">="]
        
        for op in operators:
            with self.subTest(operator=op):
                parser_state = {
                    "tokens": [
                        {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                        {"type": "OPERATOR", "value": op, "line": 1, "column": 3},
                        {"type": "NUMBER", "value": "2", "line": 1, "column": 6}
                    ],
                    "filename": "test.py",
                    "pos": 0,
                    "error": ""
                }
                
                left = {"type": "NUMBER", "value": "1", "line": 1, "column": 1}
                right = {"type": "NUMBER", "value": "2", "line": 1, "column": 6}
                
                with patch("._parse_arithmetic_package._parse_arithmetic_src._parse_arithmetic") as mock_arithmetic:
                    mock_arithmetic.side_effect = [left, right]
                    
                    result = _parse_comparison(parser_state)
                    
                    self.assertEqual(result["type"], "COMPARE")
                    self.assertEqual(result["operator"], op)
                    self.assertEqual(parser_state["pos"], 3)
    
    def test_no_comparison_operator(self):
        """Test when there's no comparison operator - just return arithmetic result"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "filename": "test.py",
            "pos": 0,
            "error": ""
        }
        
        arithmetic_result = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        
        with patch("._parse_arithmetic_package._parse_arithmetic_src._parse_arithmetic") as mock_arithmetic:
            mock_arithmetic.return_value = arithmetic_result
            
            result = _parse_comparison(parser_state)
            
            # Should return the arithmetic result directly
            self.assertEqual(result, arithmetic_result)
            self.assertEqual(parser_state["pos"], 1)
    
    def test_error_propagation_from_arithmetic(self):
        """Test that errors from _parse_arithmetic are propagated"""
        parser_state = {
            "tokens": [
                {"type": "INVALID", "value": "?", "line": 1, "column": 1}
            ],
            "filename": "test.py",
            "pos": 0,
            "error": ""
        }
        
        error_result = {"type": "ERROR", "value": "invalid token"}
        
        with patch("._parse_arithmetic_package._parse_arithmetic_src._parse_arithmetic") as mock_arithmetic:
            mock_arithmetic.return_value = error_result
            # Simulate error being set in parser_state
            def set_error(state):
                state["error"] = "invalid token"
                return error_result
            mock_arithmetic.side_effect = set_error
            
            result = _parse_comparison(parser_state)
            
            self.assertEqual(result, error_result)
            self.assertEqual(parser_state["error"], "invalid token")
            self.assertEqual(parser_state["pos"], 0)
    
    def test_empty_tokens(self):
        """Test with empty tokens list"""
        parser_state = {
            "tokens": [],
            "filename": "test.py",
            "pos": 0,
            "error": ""
        }
        
        empty_result = {"type": "EMPTY"}
        
        with patch("._parse_arithmetic_package._parse_arithmetic_src._parse_arithmetic") as mock_arithmetic:
            mock_arithmetic.return_value = empty_result
            
            result = _parse_comparison(parser_state)
            
            self.assertEqual(result, empty_result)
            self.assertEqual(parser_state["pos"], 0)
    
    def test_multiple_chained_comparisons(self):
        """Test multiple chained comparisons: a < b < c < d"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "<", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
                {"type": "OPERATOR", "value": "<", "line": 1, "column": 7},
                {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 9},
                {"type": "OPERATOR", "value": "<", "line": 1, "column": 11},
                {"type": "IDENTIFIER", "value": "d", "line": 1, "column": 13}
            ],
            "filename": "test.py",
            "pos": 0,
            "error": ""
        }
        
        operands = [
            {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
            {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 9},
            {"type": "IDENTIFIER", "value": "d", "line": 1, "column": 13}
        ]
        
        with patch("._parse_arithmetic_package._parse_arithmetic_src._parse_arithmetic") as mock_arithmetic:
            mock_arithmetic.side_effect = operands
            
            result = _parse_comparison(parser_state)
            
            # Verify left-associative structure: (((a < b) < c) < d)
            self.assertEqual(result["type"], "COMPARE")
            self.assertEqual(result["operator"], "<")
            self.assertEqual(result["right"], operands[3])  # d
            
            # Second level: ((a < b) < c)
            self.assertEqual(result["left"]["type"], "COMPARE")
            self.assertEqual(result["left"]["operator"], "<")
            self.assertEqual(result["left"]["right"], operands[2])  # c
            
            # Third level: (a < b)
            self.assertEqual(result["left"]["left"]["type"], "COMPARE")
            self.assertEqual(result["left"]["left"]["operator"], "<")
            self.assertEqual(result["left"]["left"]["left"], operands[0])  # a
            self.assertEqual(result["left"]["left"]["right"], operands[1])  # b
            
            self.assertEqual(parser_state["pos"], 7)
    
    def test_comparison_mixed_operators(self):
        """Test chained comparisons with different operators"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "<", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 5},
                {"type": "OPERATOR", "value": "<=", "line": 1, "column": 7},
                {"type": "NUMBER", "value": "3", "line": 1, "column": 10}
            ],
            "filename": "test.py",
            "pos": 0,
            "error": ""
        }
        
        num1 = {"type": "NUMBER", "value": "1", "line": 1, "column": 1}
        num2 = {"type": "NUMBER", "value": "2", "line": 1, "column": 5}
        num3 = {"type": "NUMBER", "value": "3", "line": 1, "column": 10}
        
        with patch("._parse_arithmetic_package._parse_arithmetic_src._parse_arithmetic") as mock_arithmetic:
            mock_arithmetic.side_effect = [num1, num2, num3]
            
            result = _parse_comparison(parser_state)
            
            # Should be: (1 < 2) <= 3
            self.assertEqual(result["type"], "COMPARE")
            self.assertEqual(result["operator"], "<=")
            self.assertEqual(result["right"], num3)
            
            self.assertEqual(result["left"]["type"], "COMPARE")
            self.assertEqual(result["left"]["operator"], "<")
            self.assertEqual(result["left"]["left"], num1)
            self.assertEqual(result["left"]["right"], num2)
            
            self.assertEqual(parser_state["pos"], 5)
    
    def test_comparison_with_non_operator_token(self):
        """Test that parsing stops at non-comparison operator"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "<", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
                {"type": "OPERATOR", "value": "+", "line": 1, "column": 7},
                {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 9}
            ],
            "filename": "test.py",
            "pos": 0,
            "error": ""
        }
        
        operand_a = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        operand_b = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
        
        with patch("._parse_arithmetic_package._parse_arithmetic_src._parse_arithmetic") as mock_arithmetic:
            mock_arithmetic.side_effect = [operand_a, operand_b]
            
            result = _parse_comparison(parser_state)
            
            # Should parse only "a < b", stop at "+"
            self.assertEqual(result["type"], "COMPARE")
            self.assertEqual(result["operator"], "<")
            self.assertEqual(result["left"], operand_a)
            self.assertEqual(result["right"], operand_b)
            self.assertEqual(parser_state["pos"], 3)


if __name__ == "__main__":
    unittest.main()

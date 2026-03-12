import unittest
from unittest.mock import patch

# Relative import from the same package
from ._parse_additive_expr_src import _parse_additive_expr


class TestParseAdditiveExpr(unittest.TestCase):
    """Test cases for _parse_additive_expr function."""
    
    def test_no_additive_operator(self):
        """Test when there's no + or - operator, should return left operand directly."""
        parser_state = {
            "tokens": [{"type": "NUMBER", "value": "5", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test.cc"
        }
        
        with patch("._parse_multiplicative_expr_package._parse_multiplicative_expr_src._parse_multiplicative_expr") as mock_parse_mult:
            mock_parse_mult.return_value = {
                "type": "LITERAL",
                "children": [],
                "value": "5",
                "line": 1,
                "column": 1
            }
            
            result = _parse_additive_expr(parser_state)
            
            self.assertEqual(result["type"], "LITERAL")
            self.assertEqual(result["value"], "5")
            self.assertEqual(parser_state["pos"], 0)
            mock_parse_mult.assert_called_once_with(parser_state)
    
    def test_addition_operator(self):
        """Test parsing expression with + operator."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "3", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "+", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "4", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.cc"
        }
        
        call_count = [0]
        
        def mock_parse_mult_side_effect(state):
            call_count[0] += 1
            if call_count[0] == 1:
                return {
                    "type": "LITERAL",
                    "children": [],
                    "value": "3",
                    "line": 1,
                    "column": 1
                }
            else:
                return {
                    "type": "LITERAL",
                    "children": [],
                    "value": "4",
                    "line": 1,
                    "column": 5
                }
        
        with patch("._parse_multiplicative_expr_package._parse_multiplicative_expr_src._parse_multiplicative_expr") as mock_parse_mult:
            mock_parse_mult.side_effect = mock_parse_mult_side_effect
            
            result = _parse_additive_expr(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "+")
            self.assertEqual(len(result["children"]), 2)
            self.assertEqual(result["children"][0]["value"], "3")
            self.assertEqual(result["children"][1]["value"], "4")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 3)
            self.assertEqual(parser_state["pos"], 2)
            self.assertEqual(mock_parse_mult.call_count, 2)
    
    def test_subtraction_operator(self):
        """Test parsing expression with - operator."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "10", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "-", "line": 1, "column": 4},
                {"type": "NUMBER", "value": "3", "line": 1, "column": 6}
            ],
            "pos": 0,
            "filename": "test.cc"
        }
        
        call_count = [0]
        
        def mock_parse_mult_side_effect(state):
            call_count[0] += 1
            if call_count[0] == 1:
                return {
                    "type": "LITERAL",
                    "children": [],
                    "value": "10",
                    "line": 1,
                    "column": 1
                }
            else:
                return {
                    "type": "LITERAL",
                    "children": [],
                    "value": "3",
                    "line": 1,
                    "column": 6
                }
        
        with patch("._parse_multiplicative_expr_package._parse_multiplicative_expr_src._parse_multiplicative_expr") as mock_parse_mult:
            mock_parse_mult.side_effect = mock_parse_mult_side_effect
            
            result = _parse_additive_expr(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "-")
            self.assertEqual(len(result["children"]), 2)
            self.assertEqual(result["children"][0]["value"], "10")
            self.assertEqual(result["children"][1]["value"], "3")
            self.assertEqual(parser_state["pos"], 2)
    
    def test_error_in_parser_state_initial(self):
        """Test when parser_state already has an error before parsing."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.cc",
            "error": "Previous error occurred"
        }
        
        result = _parse_additive_expr(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], "Previous error occurred")
    
    def test_error_after_parsing_left_operand(self):
        """Test when error occurs after parsing left operand."""
        parser_state = {
            "tokens": [{"type": "NUMBER", "value": "5", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test.cc"
        }
        
        with patch("._parse_multiplicative_expr_package._parse_multiplicative_expr_src._parse_multiplicative_expr") as mock_parse_mult:
            mock_parse_mult.return_value = {
                "type": "ERROR",
                "children": [],
                "value": "Error in multiplicative expr",
                "line": 0,
                "column": 0
            }
            parser_state["error"] = "Error in multiplicative expr"
            
            result = _parse_additive_expr(parser_state)
            
            self.assertEqual(result["type"], "ERROR")
            mock_parse_mult.assert_called_once_with(parser_state)
    
    def test_error_after_parsing_right_operand(self):
        """Test when error occurs after parsing right operand."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "3", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "+", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.cc"
        }
        
        call_count = [0]
        
        def mock_parse_mult_side_effect(state):
            call_count[0] += 1
            if call_count[0] == 1:
                return {
                    "type": "LITERAL",
                    "children": [],
                    "value": "3",
                    "line": 1,
                    "column": 1
                }
            else:
                parser_state["error"] = "Error parsing right operand"
                return {
                    "type": "ERROR",
                    "children": [],
                    "value": "Error parsing right operand",
                    "line": 0,
                    "column": 0
                }
        
        with patch("._parse_multiplicative_expr_package._parse_multiplicative_expr_src._parse_multiplicative_expr") as mock_parse_mult:
            mock_parse_mult.side_effect = mock_parse_mult_side_effect
            
            result = _parse_additive_expr(parser_state)
            
            self.assertEqual(result["type"], "ERROR")
            self.assertEqual(mock_parse_mult.call_count, 2)
    
    def test_empty_tokens(self):
        """Test with empty tokens list."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.cc"
        }
        
        with patch("._parse_multiplicative_expr_package._parse_multiplicative_expr_src._parse_multiplicative_expr") as mock_parse_mult:
            mock_parse_mult.return_value = {
                "type": "ERROR",
                "children": [],
                "value": "No token available",
                "line": 0,
                "column": 0
            }
            
            result = _parse_additive_expr(parser_state)
            
            self.assertEqual(result["type"], "ERROR")
            mock_parse_mult.assert_called_once_with(parser_state)
    
    def test_single_additive_operator_at_end(self):
        """Test when + or - operator is at the end with no right operand."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "5", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "+", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.cc"
        }
        
        call_count = [0]
        
        def mock_parse_mult_side_effect(state):
            call_count[0] += 1
            if call_count[0] == 1:
                return {
                    "type": "LITERAL",
                    "children": [],
                    "value": "5",
                    "line": 1,
                    "column": 1
                }
            else:
                return {
                    "type": "ERROR",
                    "children": [],
                    "value": "Expected operand after operator",
                    "line": 0,
                    "column": 0
                }
        
        with patch("._parse_multiplicative_expr_package._parse_multiplicative_expr_src._parse_multiplicative_expr") as mock_parse_mult:
            mock_parse_mult.side_effect = mock_parse_mult_side_effect
            
            result = _parse_additive_expr(parser_state)
            
            self.assertEqual(result["type"], "ERROR")
            self.assertEqual(parser_state["pos"], 2)
    
    def test_identifier_operands(self):
        """Test with identifier operands instead of literals."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "+", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "y", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.cc"
        }
        
        call_count = [0]
        
        def mock_parse_mult_side_effect(state):
            call_count[0] += 1
            if call_count[0] == 1:
                return {
                    "type": "IDENTIFIER",
                    "children": [],
                    "value": "x",
                    "line": 1,
                    "column": 1
                }
            else:
                return {
                    "type": "IDENTIFIER",
                    "children": [],
                    "value": "y",
                    "line": 1,
                    "column": 5
                }
        
        with patch("._parse_multiplicative_expr_package._parse_multiplicative_expr_src._parse_multiplicative_expr") as mock_parse_mult:
            mock_parse_mult.side_effect = mock_parse_mult_side_effect
            
            result = _parse_additive_expr(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "+")
            self.assertEqual(result["children"][0]["type"], "IDENTIFIER")
            self.assertEqual(result["children"][0]["value"], "x")
            self.assertEqual(result["children"][1]["type"], "IDENTIFIER")
            self.assertEqual(result["children"][1]["value"], "y")
    
    def test_mixed_operators_only_parses_first(self):
        """Test that only the first + or - is parsed (single level)."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "+", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 5},
                {"type": "OPERATOR", "value": "-", "line": 1, "column": 7},
                {"type": "NUMBER", "value": "3", "line": 1, "column": 9}
            ],
            "pos": 0,
            "filename": "test.cc"
        }
        
        call_count = [0]
        
        def mock_parse_mult_side_effect(state):
            call_count[0] += 1
            if call_count[0] == 1:
                return {
                    "type": "LITERAL",
                    "children": [],
                    "value": "1",
                    "line": 1,
                    "column": 1
                }
            else:
                return {
                    "type": "LITERAL",
                    "children": [],
                    "value": "2",
                    "line": 1,
                    "column": 5
                }
        
        with patch("._parse_multiplicative_expr_package._parse_multiplicative_expr_src._parse_multiplicative_expr") as mock_parse_mult:
            mock_parse_mult.side_effect = mock_parse_mult_side_effect
            
            result = _parse_additive_expr(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "+")
            self.assertEqual(parser_state["pos"], 2)


if __name__ == "__main__":
    unittest.main()

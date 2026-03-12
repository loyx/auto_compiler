import unittest
from unittest.mock import patch

from ._parse_expression_src import _parse_expression


class TestParseExpression(unittest.TestCase):
    """Test cases for _parse_expression function."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.sample_token_plus = {
            "type": "PLUS",
            "value": "+",
            "line": 1,
            "column": 5
        }
        self.sample_token_minus = {
            "type": "MINUS",
            "value": "-",
            "line": 1,
            "column": 5
        }
        self.sample_token_identifier = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 1
        }
        self.sample_token_literal = {
            "type": "LITERAL",
            "value": "42",
            "line": 1,
            "column": 1
        }
    
    @patch('._parse_term_package._parse_term_src._parse_term')
    def test_single_term_no_operator(self, mock_parse_term):
        """Test parsing a single term without any PLUS/MINUS operators."""
        mock_parse_term.return_value = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 1
        }
        
        parser_state = {
            "tokens": [self.sample_token_identifier],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_expression(parser_state)
        
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "x")
        mock_parse_term.assert_called_once_with(parser_state)
    
    @patch('._parse_term_package._parse_term_src._parse_term')
    def test_expression_with_plus_operator(self, mock_parse_term):
        """Test parsing expression with one PLUS operator."""
        mock_parse_term.side_effect = [
            {
                "type": "LITERAL",
                "value": "10",
                "line": 1,
                "column": 1
            },
            {
                "type": "LITERAL",
                "value": "5",
                "line": 1,
                "column": 3
            }
        ]
        
        parser_state = {
            "tokens": [
                self.sample_token_literal,
                self.sample_token_plus,
                self.sample_token_literal
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_expression(parser_state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "+")
        self.assertEqual(len(result["children"]), 2)
        self.assertEqual(parser_state["pos"], 2)
    
    @patch('._parse_term_package._parse_term_src._parse_term')
    def test_expression_with_minus_operator(self, mock_parse_term):
        """Test parsing expression with one MINUS operator."""
        mock_parse_term.side_effect = [
            {
                "type": "LITERAL",
                "value": "10",
                "line": 1,
                "column": 1
            },
            {
                "type": "LITERAL",
                "value": "5",
                "line": 1,
                "column": 3
            }
        ]
        
        parser_state = {
            "tokens": [
                self.sample_token_literal,
                self.sample_token_minus,
                self.sample_token_literal
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_expression(parser_state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "-")
        self.assertEqual(len(result["children"]), 2)
    
    @patch('._parse_term_package._parse_term_src._parse_term')
    def test_left_associativity_multiple_operators(self, mock_parse_term):
        """Test that multiple operators are left-associative: (a + b) + c."""
        term_a = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        term_b = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 3}
        term_c = {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 5}
        
        mock_parse_term.side_effect = [term_a, term_b, term_c]
        
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 2},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 3},
                {"type": "PLUS", "value": "+", "line": 1, "column": 4},
                {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_expression(parser_state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "+")
        self.assertEqual(len(result["children"]), 2)
        
        left_child = result["children"][0]
        self.assertEqual(left_child["type"], "BINARY_OP")
        self.assertEqual(left_child["value"], "+")
        
        right_child = result["children"][1]
        self.assertEqual(right_child["type"], "IDENTIFIER")
        self.assertEqual(right_child["value"], "c")
    
    @patch('._parse_term_package._parse_term_src._parse_term')
    def test_error_from_first_term(self, mock_parse_term):
        """Test handling when first _parse_term returns error."""
        error_ast = {"type": "ERROR", "value": "unexpected token", "line": 1, "column": 1}
        mock_parse_term.return_value = error_ast
        
        parser_state = {
            "tokens": [self.sample_token_identifier],
            "pos": 0,
            "filename": "test.py",
            "error": "parse error"
        }
        
        result = _parse_expression(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        mock_parse_term.assert_called_once()
    
    @patch('._parse_term_package._parse_term_src._parse_term')
    def test_error_from_second_term(self, mock_parse_term):
        """Test handling when second _parse_term (right operand) returns error."""
        mock_parse_term.side_effect = [
            {"type": "LITERAL", "value": "10", "line": 1, "column": 1},
            {"type": "ERROR", "value": "expected term", "line": 1, "column": 3}
        ]
        
        parser_state = {
            "tokens": [
                self.sample_token_literal,
                self.sample_token_plus,
                self.sample_token_identifier
            ],
            "pos": 0,
            "filename": "test.py",
            "error": "parse error"
        }
        
        result = _parse_expression(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(mock_parse_term.call_count, 2)
    
    @patch('._parse_term_package._parse_term_src._parse_term')
    def test_mixed_plus_minus_operators(self, mock_parse_term):
        """Test expression with mixed PLUS and MINUS operators."""
        term_1 = {"type": "LITERAL", "value": "10", "line": 1, "column": 1}
        term_2 = {"type": "LITERAL", "value": "5", "line": 1, "column": 3}
        term_3 = {"type": "LITERAL", "value": "3", "line": 1, "column": 5}
        
        mock_parse_term.side_effect = [term_1, term_2, term_3]
        
        parser_state = {
            "tokens": [
                {"type": "LITERAL", "value": "10", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 2},
                {"type": "LITERAL", "value": "5", "line": 1, "column": 3},
                {"type": "MINUS", "value": "-", "line": 1, "column": 4},
                {"type": "LITERAL", "value": "3", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_expression(parser_state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "-")
        
        left_child = result["children"][0]
        self.assertEqual(left_child["type"], "BINARY_OP")
        self.assertEqual(left_child["value"], "+")
        
        right_child = result["children"][1]
        self.assertEqual(right_child["type"], "LITERAL")
        self.assertEqual(right_child["value"], "3")
    
    @patch('._parse_term_package._parse_term_src._parse_term')
    def test_position_advancement(self, mock_parse_term):
        """Test that parser_state['pos'] is correctly advanced."""
        mock_parse_term.side_effect = [
            {"type": "LITERAL", "value": "1", "line": 1, "column": 1},
            {"type": "LITERAL", "value": "2", "line": 1, "column": 3}
        ]
        
        parser_state = {
            "tokens": [
                {"type": "LITERAL", "value": "1", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 2},
                {"type": "LITERAL", "value": "2", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_expression(parser_state)
        
        self.assertEqual(parser_state["pos"], 2)
    
    @patch('._parse_term_package._parse_term_src._parse_term')
    def test_non_plus_minus_token_stops_loop(self, mock_parse_term):
        """Test that non-PLUS/MINUS token stops the operator loop."""
        mock_parse_term.return_value = {"type": "LITERAL", "value": "42", "line": 1, "column": 1}
        
        parser_state = {
            "tokens": [
                {"type": "LITERAL", "value": "42", "line": 1, "column": 1},
                {"type": "MULTI", "value": "*", "line": 1, "column": 2},
                {"type": "LITERAL", "value": "2", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_expression(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "42")
        mock_parse_term.assert_called_once()


if __name__ == '__main__':
    unittest.main()

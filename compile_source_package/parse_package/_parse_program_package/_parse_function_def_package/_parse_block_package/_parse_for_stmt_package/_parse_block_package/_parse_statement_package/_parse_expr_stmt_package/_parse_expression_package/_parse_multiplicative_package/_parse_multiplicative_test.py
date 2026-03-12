import unittest
from unittest.mock import patch

# Relative import for the function under test
from ._parse_multiplicative_src import _parse_multiplicative


class TestParseMultiplicative(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures."""
        self.base_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }
    
    def test_single_operand_no_operator(self):
        """Test parsing a single operand without any multiplicative operators."""
        token = {"type": "NUMBER", "value": "42", "line": 1, "column": 1}
        parser_state = {
            "tokens": [token],
            "pos": 0,
            "filename": "test.py"
        }
        
        expected_ast = {"type": "NUMBER", "value": "42", "line": 1, "column": 1}
        
        with patch('._parse_unary_package._parse_unary_src._parse_unary', return_value=expected_ast) as mock_unary:
            result = _parse_multiplicative(parser_state)
            self.assertEqual(result, expected_ast)
            mock_unary.assert_called_once()
            self.assertEqual(parser_state["pos"], 0)
    
    def test_multiplication_operator(self):
        """Test parsing two operands with multiplication operator."""
        left_token = {"type": "NUMBER", "value": "5", "line": 1, "column": 1}
        op_token = {"type": "OPERATOR", "value": "*", "line": 1, "column": 3}
        right_token = {"type": "NUMBER", "value": "3", "line": 1, "column": 5}
        
        parser_state = {
            "tokens": [left_token, op_token, right_token],
            "pos": 0,
            "filename": "test.py"
        }
        
        left_ast = {"type": "NUMBER", "value": "5", "line": 1, "column": 1}
        right_ast = {"type": "NUMBER", "value": "3", "line": 1, "column": 5}
        
        with patch('._parse_unary_package._parse_unary_src._parse_unary', side_effect=[left_ast, right_ast]) as mock_unary:
            result = _parse_multiplicative(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "*")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 3)
            self.assertEqual(len(result["children"]), 2)
            self.assertEqual(result["children"][0], left_ast)
            self.assertEqual(result["children"][1], right_ast)
            self.assertEqual(parser_state["pos"], 3)
    
    def test_division_operator(self):
        """Test parsing two operands with division operator."""
        left_token = {"type": "NUMBER", "value": "10", "line": 1, "column": 1}
        op_token = {"type": "OPERATOR", "value": "/", "line": 1, "column": 3}
        right_token = {"type": "NUMBER", "value": "2", "line": 1, "column": 5}
        
        parser_state = {
            "tokens": [left_token, op_token, right_token],
            "pos": 0,
            "filename": "test.py"
        }
        
        left_ast = {"type": "NUMBER", "value": "10", "line": 1, "column": 1}
        right_ast = {"type": "NUMBER", "value": "2", "line": 1, "column": 5}
        
        with patch('._parse_unary_package._parse_unary_src._parse_unary', side_effect=[left_ast, right_ast]) as mock_unary:
            result = _parse_multiplicative(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "/")
            self.assertEqual(result["children"][0], left_ast)
            self.assertEqual(result["children"][1], right_ast)
    
    def test_modulo_operator(self):
        """Test parsing two operands with modulo operator."""
        left_token = {"type": "NUMBER", "value": "10", "line": 1, "column": 1}
        op_token = {"type": "OPERATOR", "value": "%", "line": 1, "column": 3}
        right_token = {"type": "NUMBER", "value": "3", "line": 1, "column": 5}
        
        parser_state = {
            "tokens": [left_token, op_token, right_token],
            "pos": 0,
            "filename": "test.py"
        }
        
        left_ast = {"type": "NUMBER", "value": "10", "line": 1, "column": 1}
        right_ast = {"type": "NUMBER", "value": "3", "line": 1, "column": 5}
        
        with patch('._parse_unary_package._parse_unary_src._parse_unary', side_effect=[left_ast, right_ast]) as mock_unary:
            result = _parse_multiplicative(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "%")
    
    def test_multiple_operators_left_associative(self):
        """Test parsing multiple operators with left associativity: a * b / c."""
        tokens = [
            {"type": "NUMBER", "value": "2", "line": 1, "column": 1},
            {"type": "OPERATOR", "value": "*", "line": 1, "column": 3},
            {"type": "NUMBER", "value": "3", "line": 1, "column": 5},
            {"type": "OPERATOR", "value": "/", "line": 1, "column": 7},
            {"type": "NUMBER", "value": "4", "line": 1, "column": 9},
        ]
        
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        # Mock _parse_unary to return different AST nodes for each call
        ast_nodes = [
            {"type": "NUMBER", "value": "2", "line": 1, "column": 1},
            {"type": "NUMBER", "value": "3", "line": 1, "column": 5},
            {"type": "NUMBER", "value": "4", "line": 1, "column": 9},
        ]
        
        with patch('._parse_unary_package._parse_unary_src._parse_unary', side_effect=ast_nodes) as mock_unary:
            result = _parse_multiplicative(parser_state)
            
            # Should build: (2 * 3) / 4
            # First iteration: left = 2 * 3
            # Second iteration: left = (2 * 3) / 4
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "/")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 7)
            
            # Left child should be the first BINARY_OP (2 * 3)
            left_child = result["children"][0]
            self.assertEqual(left_child["type"], "BINARY_OP")
            self.assertEqual(left_child["value"], "*")
            
            # Right child should be 4
            right_child = result["children"][1]
            self.assertEqual(right_child["type"], "NUMBER")
            self.assertEqual(right_child["value"], "4")
            
            # pos should be at the end
            self.assertEqual(parser_state["pos"], 5)
    
    def test_non_operator_token_stops_parsing(self):
        """Test that non-operator tokens stop the multiplicative parsing loop."""
        tokens = [
            {"type": "NUMBER", "value": "5", "line": 1, "column": 1},
            {"type": "OPERATOR", "value": "+", "line": 1, "column": 3},  # Not multiplicative
            {"type": "NUMBER", "value": "3", "line": 1, "column": 5},
        ]
        
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        left_ast = {"type": "NUMBER", "value": "5", "line": 1, "column": 1}
        
        with patch('._parse_unary_package._parse_unary_src._parse_unary', return_value=left_ast) as mock_unary:
            result = _parse_multiplicative(parser_state)
            
            # Should return just the left operand, not consume the + operator
            self.assertEqual(result, left_ast)
            # _parse_unary should only be called once
            mock_unary.assert_called_once()
    
    def test_empty_tokens(self):
        """Test parsing with empty tokens list."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }
        
        # _parse_unary should raise SyntaxError on empty tokens
        with patch('._parse_unary_package._parse_unary_src._parse_unary', side_effect=SyntaxError("Unexpected end of input")) as mock_unary:
            with self.assertRaises(SyntaxError):
                _parse_multiplicative(parser_state)
    
    def test_position_at_end_of_tokens(self):
        """Test when pos is already at the end of tokens."""
        parser_state = {
            "tokens": [{"type": "NUMBER", "value": "1", "line": 1, "column": 1}],
            "pos": 1,  # Already at end
            "filename": "test.py"
        }
        
        ast_node = {"type": "NUMBER", "value": "1", "line": 1, "column": 1}
        
        with patch('._parse_unary_package._parse_unary_src._parse_unary', return_value=ast_node) as mock_unary:
            result = _parse_multiplicative(parser_state)
            self.assertEqual(result, ast_node)
    
    def test_operator_at_end_missing_right_operand(self):
        """Test when operator is at the end with no right operand."""
        tokens = [
            {"type": "NUMBER", "value": "5", "line": 1, "column": 1},
            {"type": "OPERATOR", "value": "*", "line": 1, "column": 3},
        ]
        
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        left_ast = {"type": "NUMBER", "value": "5", "line": 1, "column": 1}
        
        # First call returns left_ast, second call (for right operand) raises error
        with patch('._parse_unary_package._parse_unary_src._parse_unary', side_effect=[left_ast, SyntaxError("Expected operand")]) as mock_unary:
            with self.assertRaises(SyntaxError):
                _parse_multiplicative(parser_state)
    
    def test_mixed_operators(self):
        """Test parsing with mixed multiplicative operators: a * b % c / d."""
        tokens = [
            {"type": "NUMBER", "value": "10", "line": 1, "column": 1},
            {"type": "OPERATOR", "value": "*", "line": 1, "column": 3},
            {"type": "NUMBER", "value": "2", "line": 1, "column": 5},
            {"type": "OPERATOR", "value": "%", "line": 1, "column": 7},
            {"type": "NUMBER", "value": "3", "line": 1, "column": 9},
            {"type": "OPERATOR", "value": "/", "line": 1, "column": 11},
            {"type": "NUMBER", "value": "4", "line": 1, "column": 13},
        ]
        
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        ast_nodes = [
            {"type": "NUMBER", "value": "10", "line": 1, "column": 1},
            {"type": "NUMBER", "value": "2", "line": 1, "column": 5},
            {"type": "NUMBER", "value": "3", "line": 1, "column": 9},
            {"type": "NUMBER", "value": "4", "line": 1, "column": 13},
        ]
        
        with patch('._parse_unary_package._parse_unary_src._parse_unary', side_effect=ast_nodes) as mock_unary:
            result = _parse_multiplicative(parser_state)
            
            # Should build: ((10 * 2) % 3) / 4
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "/")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 11)
            
            # Verify left associativity
            left_child = result["children"][0]
            self.assertEqual(left_child["type"], "BINARY_OP")
            self.assertEqual(left_child["value"], "%")
            
            self.assertEqual(parser_state["pos"], 7)
    
    def test_parser_state_pos_updated_correctly(self):
        """Test that parser_state pos is updated correctly during parsing."""
        tokens = [
            {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
            {"type": "OPERATOR", "value": "*", "line": 1, "column": 3},
            {"type": "NUMBER", "value": "2", "line": 1, "column": 5},
        ]
        
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        ast_nodes = [
            {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
            {"type": "NUMBER", "value": "2", "line": 1, "column": 5},
        ]
        
        with patch('._parse_unary_package._parse_unary_src._parse_unary', side_effect=ast_nodes) as mock_unary:
            result = _parse_multiplicative(parser_state)
            
            # After parsing: pos should be at 3 (after all tokens consumed)
            self.assertEqual(parser_state["pos"], 3)
    
    def test_wrong_operator_type_not_consumed(self):
        """Test that OPERATOR token with non-multiplicative value is not consumed."""
        tokens = [
            {"type": "NUMBER", "value": "5", "line": 1, "column": 1},
            {"type": "OPERATOR", "value": "+", "line": 1, "column": 3},
            {"type": "NUMBER", "value": "3", "line": 1, "column": 5},
        ]
        
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        left_ast = {"type": "NUMBER", "value": "5", "line": 1, "column": 1}
        
        with patch('._parse_unary_package._parse_unary_src._parse_unary', return_value=left_ast) as mock_unary:
            result = _parse_multiplicative(parser_state)
            
            # Should not consume the + operator
            self.assertEqual(result, left_ast)
            self.assertEqual(parser_state["pos"], 0)
    
    def test_non_operator_token_type(self):
        """Test that non-OPERATOR token type stops parsing."""
        tokens = [
            {"type": "NUMBER", "value": "5", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 3},
        ]
        
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        left_ast = {"type": "NUMBER", "value": "5", "line": 1, "column": 1}
        
        with patch('._parse_unary_package._parse_unary_src._parse_unary', return_value=left_ast) as mock_unary:
            result = _parse_multiplicative(parser_state)
            
            self.assertEqual(result, left_ast)
            mock_unary.assert_called_once()


if __name__ == '__main__':
    unittest.main()

import unittest
from unittest.mock import patch

from ._parse_multiplicative_src import _parse_multiplicative


class TestParseMultiplicative(unittest.TestCase):
    """Test cases for _parse_multiplicative function."""
    
    def test_single_unary_expression(self):
        """Test parsing a single unary expression without operators."""
        unary_node = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
        
        parser_state = {
            "tokens": [{"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch('._parse_multiplicative_src._parse_unary') as mock_parse_unary:
            mock_parse_unary.return_value = unary_node
            
            result = _parse_multiplicative(parser_state)
            
            self.assertEqual(result, unary_node)
            mock_parse_unary.assert_called_once_with(parser_state)
            self.assertEqual(parser_state["pos"], 0)
    
    def test_multiplication_operation(self):
        """Test parsing a * b."""
        left_node = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        right_node = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
        
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "STAR", "value": "*", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        call_count = [0]
        def parse_unary_side_effect(state):
            if call_count[0] == 0:
                call_count[0] += 1
                return left_node
            else:
                return right_node
        
        with patch('._parse_multiplicative_src._parse_unary') as mock_parse_unary:
            mock_parse_unary.side_effect = parse_unary_side_effect
            
            result = _parse_multiplicative(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "*")
            self.assertEqual(result["children"], [left_node, right_node])
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            self.assertEqual(parser_state["pos"], 2)
            self.assertEqual(mock_parse_unary.call_count, 2)
    
    def test_division_operation(self):
        """Test parsing a / b."""
        left_node = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        right_node = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
        
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "SLASH", "value": "/", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        call_count = [0]
        def parse_unary_side_effect(state):
            if call_count[0] == 0:
                call_count[0] += 1
                return left_node
            else:
                return right_node
        
        with patch('._parse_multiplicative_src._parse_unary') as mock_parse_unary:
            mock_parse_unary.side_effect = parse_unary_side_effect
            
            result = _parse_multiplicative(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "/")
            self.assertEqual(result["children"], [left_node, right_node])
            self.assertEqual(parser_state["pos"], 2)
    
    def test_modulo_operation(self):
        """Test parsing a % b."""
        left_node = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        right_node = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
        
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "PERCENT", "value": "%", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        call_count = [0]
        def parse_unary_side_effect(state):
            if call_count[0] == 0:
                call_count[0] += 1
                return left_node
            else:
                return right_node
        
        with patch('._parse_unary_package._parse_unary_src._parse_unary') as mock_parse_unary:
            mock_parse_unary.side_effect = parse_unary_side_effect
            
            result = _parse_multiplicative(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "%")
            self.assertEqual(result["children"], [left_node, right_node])
            self.assertEqual(parser_state["pos"], 2)
    
    def test_left_associative(self):
        """Test left-associativity: a * b / c should be ((a * b) / c)."""
        node_a = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        node_b = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
        node_c = {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 9}
        
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "STAR", "value": "*", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
                {"type": "SLASH", "value": "/", "line": 1, "column": 7},
                {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 9}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        nodes = [node_a, node_b, node_c]
        call_count = [0]
        
        def parse_unary_side_effect(state):
            idx = call_count[0]
            call_count[0] += 1
            return nodes[idx]
        
        with patch('._parse_unary_package._parse_unary_src._parse_unary') as mock_parse_unary:
            mock_parse_unary.side_effect = parse_unary_side_effect
            
            result = _parse_multiplicative(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "/")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            
            left_child = result["children"][0]
            self.assertEqual(left_child["type"], "BINARY_OP")
            self.assertEqual(left_child["value"], "*")
            self.assertEqual(left_child["children"][0], node_a)
            self.assertEqual(left_child["children"][1], node_b)
            
            self.assertEqual(result["children"][1], node_c)
            self.assertEqual(parser_state["pos"], 4)
            self.assertEqual(mock_parse_unary.call_count, 3)
    
    def test_mixed_operators(self):
        """Test mixed operators: a * b % c."""
        node_a = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        node_b = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
        node_c = {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 9}
        
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "STAR", "value": "*", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
                {"type": "PERCENT", "value": "%", "line": 1, "column": 7},
                {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 9}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        nodes = [node_a, node_b, node_c]
        call_count = [0]
        
        def parse_unary_side_effect(state):
            idx = call_count[0]
            call_count[0] += 1
            return nodes[idx]
        
        with patch('._parse_unary_package._parse_unary_src._parse_unary') as mock_parse_unary:
            mock_parse_unary.side_effect = parse_unary_side_effect
            
            result = _parse_multiplicative(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "%")
            
            left_child = result["children"][0]
            self.assertEqual(left_child["type"], "BINARY_OP")
            self.assertEqual(left_child["value"], "*")
            
            self.assertEqual(parser_state["pos"], 4)
    
    def test_no_tokens(self):
        """Test with empty token list."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch('._parse_unary_package._parse_unary_src._parse_unary') as mock_parse_unary:
            mock_parse_unary.return_value = {"type": "LITERAL", "value": 0, "line": 0, "column": 0}
            
            result = _parse_multiplicative(parser_state)
            
            self.assertEqual(result["type"], "LITERAL")
            mock_parse_unary.assert_called_once()
    
    def test_position_at_end(self):
        """Test when position is already at end of tokens."""
        parser_state = {
            "tokens": [{"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}],
            "pos": 1,
            "filename": "test.py"
        }
        
        with patch('._parse_unary_package._parse_unary_src._parse_unary') as mock_parse_unary:
            mock_parse_unary.return_value = {"type": "LITERAL", "value": 0, "line": 0, "column": 0}
            
            result = _parse_multiplicative(parser_state)
            
            self.assertEqual(parser_state["pos"], 1)
            mock_parse_unary.assert_called_once()
    
    def test_preserves_line_column_from_left_operand(self):
        """Test that line and column are preserved from left operand."""
        left_node = {"type": "IDENTIFIER", "value": "a", "line": 5, "column": 10}
        right_node = {"type": "IDENTIFIER", "value": "b", "line": 5, "column": 15}
        
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 5, "column": 10},
                {"type": "STAR", "value": "*", "line": 5, "column": 12},
                {"type": "IDENTIFIER", "value": "b", "line": 5, "column": 15}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        call_count = [0]
        def parse_unary_side_effect(state):
            if call_count[0] == 0:
                call_count[0] += 1
                return left_node
            else:
                return right_node
        
        with patch('._parse_unary_package._parse_unary_src._parse_unary') as mock_parse_unary:
            mock_parse_unary.side_effect = parse_unary_side_effect
            
            result = _parse_multiplicative(parser_state)
            
            self.assertEqual(result["line"], 5)
            self.assertEqual(result["column"], 10)
    
    def test_three_consecutive_operations(self):
        """Test parsing a * b / c % d with full left-associativity."""
        node_a = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
        node_b = {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
        node_c = {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 9}
        node_d = {"type": "IDENTIFIER", "value": "d", "line": 1, "column": 13}
        
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "STAR", "value": "*", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
                {"type": "SLASH", "value": "/", "line": 1, "column": 7},
                {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 9},
                {"type": "PERCENT", "value": "%", "line": 1, "column": 11},
                {"type": "IDENTIFIER", "value": "d", "line": 1, "column": 13}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        nodes = [node_a, node_b, node_c, node_d]
        call_count = [0]
        
        def parse_unary_side_effect(state):
            idx = call_count[0]
            call_count[0] += 1
            return nodes[idx]
        
        with patch('._parse_unary_package._parse_unary_src._parse_unary') as mock_parse_unary:
            mock_parse_unary.side_effect = parse_unary_side_effect
            
            result = _parse_multiplicative(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "%")
            
            rightmost = result["children"][1]
            self.assertEqual(rightmost, node_d)
            
            middle = result["children"][0]
            self.assertEqual(middle["value"], "/")
            
            leftmost = middle["children"][0]
            self.assertEqual(leftmost["value"], "*")
            self.assertEqual(leftmost["children"][0], node_a)
            self.assertEqual(leftmost["children"][1], node_b)
            
            self.assertEqual(middle["children"][1], node_c)
            self.assertEqual(parser_state["pos"], 6)
            self.assertEqual(mock_parse_unary.call_count, 4)


if __name__ == '__main__':
    unittest.main()

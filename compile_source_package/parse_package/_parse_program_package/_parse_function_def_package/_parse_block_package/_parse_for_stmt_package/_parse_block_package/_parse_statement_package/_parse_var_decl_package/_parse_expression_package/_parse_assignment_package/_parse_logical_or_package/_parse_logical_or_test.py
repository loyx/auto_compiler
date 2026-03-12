import unittest
from unittest.mock import patch
from typing import Dict, Any

# Relative import for the function under test
from ._parse_logical_or_package._parse_logical_or_src import _parse_logical_or


class TestParseLogicalOr(unittest.TestCase):
    """Test cases for _parse_logical_or function"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.sample_parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.txt"
        }
    
    def _create_literal_node(self, value: Any, line: int = 1, column: int = 1) -> Dict:
        """Helper to create literal AST node"""
        return {
            "type": "LITERAL",
            "value": value,
            "line": line,
            "column": column
        }
    
    def _create_identifier_node(self, name: str, line: int = 1, column: int = 1) -> Dict:
        """Helper to create identifier AST node"""
        return {
            "type": "IDENTIFIER",
            "value": name,
            "line": line,
            "column": column
        }
    
    def test_no_or_operator_returns_left_operand(self):
        """Test parsing when there's no || operator - should return left operand as-is"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
            ],
            "pos": 0,
            "filename": "test.txt"
        }
        
        left_node = self._create_identifier_node("a", 1, 1)
        
        with patch('._parse_logical_and_package._parse_logical_and_src._parse_logical_and') as mock_parse_and, \
             patch('._current_token_package._current_token_src._current_token') as mock_current:
            
            mock_parse_and.return_value = left_node
            mock_current.return_value = None  # No more tokens
            
            result = _parse_logical_or(parser_state)
            
            self.assertEqual(result, left_node)
            mock_parse_and.assert_called_once_with(parser_state)
            mock_current.assert_called_once_with(parser_state)
    
    def test_single_or_operator(self):
        """Test parsing a single || operator"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "||", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 6},
            ],
            "pos": 0,
            "filename": "test.txt"
        }
        
        left_node = self._create_identifier_node("a", 1, 1)
        right_node = self._create_identifier_node("b", 1, 6)
        
        with patch('._parse_logical_and_package._parse_logical_and_src._parse_logical_and') as mock_parse_and, \
             patch('._current_token_package._current_token_src._current_token') as mock_current, \
             patch('._consume_package._consume_src._consume') as mock_consume:
            
            mock_parse_and.side_effect = [left_node, right_node]
            mock_current.return_value = {"type": "OPERATOR", "value": "||", "line": 1, "column": 3}
            mock_consume.return_value = {"type": "OPERATOR", "value": "||", "line": 1, "column": 3}
            
            result = _parse_logical_or(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "||")
            self.assertEqual(len(result["children"]), 2)
            self.assertEqual(result["children"][0], left_node)
            self.assertEqual(result["children"][1], right_node)
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            
            mock_consume.assert_called_once_with(parser_state, "OPERATOR")
    
    def test_multiple_or_operators_left_associative(self):
        """Test parsing multiple || operators (left-associative)"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "||", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 6},
                {"type": "OPERATOR", "value": "||", "line": 1, "column": 8},
                {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 11},
            ],
            "pos": 0,
            "filename": "test.txt"
        }
        
        node_a = self._create_identifier_node("a", 1, 1)
        node_b = self._create_identifier_node("b", 1, 6)
        node_c = self._create_identifier_node("c", 1, 11)
        
        with patch('._parse_logical_and_package._parse_logical_and_src._parse_logical_and') as mock_parse_and, \
             patch('._current_token_package._current_token_src._current_token') as mock_current, \
             patch('._consume_package._consume_src._consume') as mock_consume:
            
            mock_parse_and.side_effect = [node_a, node_b, node_c]
            mock_current.side_effect = [
                {"type": "OPERATOR", "value": "||", "line": 1, "column": 3},
                {"type": "OPERATOR", "value": "||", "line": 1, "column": 8},
                None  # No more operators
            ]
            mock_consume.return_value = {"type": "OPERATOR", "value": "||", "line": 1, "column": 3}
            
            result = _parse_logical_or(parser_state)
            
            # Result should be: (a || b) || c
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "||")
            self.assertEqual(len(result["children"]), 2)
            
            # Right child should be c
            self.assertEqual(result["children"][1], node_c)
            
            # Left child should be (a || b)
            inner_node = result["children"][0]
            self.assertEqual(inner_node["type"], "BINARY_OP")
            self.assertEqual(inner_node["value"], "||")
            self.assertEqual(inner_node["children"][0], node_a)
            self.assertEqual(inner_node["children"][1], node_b)
            
            # Verify _consume was called twice
            self.assertEqual(mock_consume.call_count, 2)
    
    def test_empty_tokens(self):
        """Test parsing with empty tokens list"""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.txt"
        }
        
        empty_node = self._create_literal_node(None, 0, 0)
        
        with patch('._parse_logical_and_package._parse_logical_and_src._parse_logical_and') as mock_parse_and, \
             patch('._current_token_package._current_token_src._current_token') as mock_current:
            
            mock_parse_and.return_value = empty_node
            mock_current.return_value = None
            
            result = _parse_logical_or(parser_state)
            
            self.assertEqual(result, empty_node)
            mock_current.assert_called_once()
    
    def test_token_not_operator_type(self):
        """Test when current token is not OPERATOR type"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "KEYWORD", "value": "if", "line": 1, "column": 3},
            ],
            "pos": 0,
            "filename": "test.txt"
        }
        
        left_node = self._create_identifier_node("a", 1, 1)
        
        with patch('._parse_logical_and_package._parse_logical_and_src._parse_logical_and') as mock_parse_and, \
             patch('._current_token_package._current_token_src._current_token') as mock_current:
            
            mock_parse_and.return_value = left_node
            mock_current.return_value = {"type": "KEYWORD", "value": "if", "line": 1, "column": 3}
            
            result = _parse_logical_or(parser_state)
            
            self.assertEqual(result, left_node)
            mock_current.assert_called_once()
    
    def test_operator_token_but_not_or(self):
        """Test when token is OPERATOR but value is not ||"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "&&", "line": 1, "column": 3},
            ],
            "pos": 0,
            "filename": "test.txt"
        }
        
        left_node = self._create_identifier_node("a", 1, 1)
        
        with patch('._parse_logical_and_package._parse_logical_and_src._parse_logical_and') as mock_parse_and, \
             patch('._current_token_package._current_token_src._current_token') as mock_current:
            
            mock_parse_and.return_value = left_node
            mock_current.return_value = {"type": "OPERATOR", "value": "&&", "line": 1, "column": 3}
            
            result = _parse_logical_or(parser_state)
            
            self.assertEqual(result, left_node)
            mock_current.assert_called_once()
    
    def test_pos_updated_after_consume(self):
        """Test that parser_state pos is updated after consuming || operator"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "||", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 6},
            ],
            "pos": 0,
            "filename": "test.txt"
        }
        
        left_node = self._create_identifier_node("a", 1, 1)
        right_node = self._create_identifier_node("b", 1, 6)
        
        with patch('._parse_logical_and_package._parse_logical_and_src._parse_logical_and') as mock_parse_and, \
             patch('._current_token_package._current_token_src._current_token') as mock_current, \
             patch('._consume_package._consume_src._consume') as mock_consume:
            
            mock_parse_and.side_effect = [left_node, right_node]
            mock_current.return_value = {"type": "OPERATOR", "value": "||", "line": 1, "column": 3}
            
            def consume_side_effect(state, expected_type):
                state["pos"] = 2  # Simulate pos update
                return {"type": "OPERATOR", "value": "||", "line": 1, "column": 3}
            
            mock_consume.side_effect = consume_side_effect
            
            result = _parse_logical_or(parser_state)
            
            # Verify pos was updated
            self.assertEqual(parser_state["pos"], 2)
            self.assertEqual(result["type"], "BINARY_OP")
    
    def test_line_column_from_left_node(self):
        """Test that line and column are taken from left_node when available"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 5, "column": 10},
                {"type": "OPERATOR", "value": "||", "line": 5, "column": 12},
                {"type": "IDENTIFIER", "value": "b", "line": 5, "column": 15},
            ],
            "pos": 0,
            "filename": "test.txt"
        }
        
        left_node = self._create_identifier_node("a", 5, 10)
        right_node = self._create_identifier_node("b", 5, 15)
        
        with patch('._parse_logical_and_package._parse_logical_and_src._parse_logical_and') as mock_parse_and, \
             patch('._current_token_package._current_token_src._current_token') as mock_current, \
             patch('._consume_package._consume_src._consume') as mock_consume:
            
            mock_parse_and.side_effect = [left_node, right_node]
            mock_current.return_value = {"type": "OPERATOR", "value": "||", "line": 5, "column": 12}
            mock_consume.return_value = {"type": "OPERATOR", "value": "||", "line": 5, "column": 12}
            
            result = _parse_logical_or(parser_state)
            
            self.assertEqual(result["line"], 5)
            self.assertEqual(result["column"], 10)
    
    def test_complex_expression_with_literals(self):
        """Test parsing with literal values"""
        parser_state = {
            "tokens": [
                {"type": "LITERAL", "value": "true", "line": 2, "column": 5},
                {"type": "OPERATOR", "value": "||", "line": 2, "column": 10},
                {"type": "LITERAL", "value": "false", "line": 2, "column": 13},
            ],
            "pos": 0,
            "filename": "test.txt"
        }
        
        left_node = self._create_literal_node("true", 2, 5)
        right_node = self._create_literal_node("false", 2, 13)
        
        with patch('._parse_logical_and_package._parse_logical_and_src._parse_logical_and') as mock_parse_and, \
             patch('._current_token_package._current_token_src._current_token') as mock_current, \
             patch('._consume_package._consume_src._consume') as mock_consume:
            
            mock_parse_and.side_effect = [left_node, right_node]
            mock_current.return_value = {"type": "OPERATOR", "value": "||", "line": 2, "column": 10}
            mock_consume.return_value = {"type": "OPERATOR", "value": "||", "line": 2, "column": 10}
            
            result = _parse_logical_or(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["value"], "||")
            self.assertEqual(result["children"][0]["value"], "true")
            self.assertEqual(result["children"][1]["value"], "false")


if __name__ == '__main__':
    unittest.main()

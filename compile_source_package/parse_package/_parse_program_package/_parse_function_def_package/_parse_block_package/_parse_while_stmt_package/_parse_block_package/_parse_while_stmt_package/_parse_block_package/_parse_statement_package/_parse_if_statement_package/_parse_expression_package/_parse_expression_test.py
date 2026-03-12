import unittest
from unittest.mock import patch

# Relative import from the same package
from ._parse_expression_src import _parse_expression


class TestParseExpression(unittest.TestCase):
    """Test cases for _parse_expression function."""
    
    def test_single_identifier(self):
        """Test parsing a single identifier expression."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch("._parse_expression_src._parse_primary") as mock_parse_primary, \
             patch("._parse_expression_src._get_precedence") as mock_get_precedence:
            
            mock_parse_primary.return_value = {
                "type": "IDENTIFIER",
                "value": "x",
                "line": 1,
                "column": 1
            }
            mock_get_precedence.return_value = 0
            
            result = _parse_expression(parser_state)
            
            self.assertEqual(result["type"], "IDENTIFIER")
            self.assertEqual(result["value"], "x")
            self.assertEqual(parser_state["pos"], 1)
    
    def test_single_literal(self):
        """Test parsing a single literal expression."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "42", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch("._parse_expression_src._parse_primary") as mock_parse_primary, \
             patch("._parse_expression_src._get_precedence") as mock_get_precedence:
            
            mock_parse_primary.return_value = {
                "type": "NUMBER",
                "value": "42",
                "line": 1,
                "column": 1
            }
            mock_get_precedence.return_value = 0
            
            result = _parse_expression(parser_state)
            
            self.assertEqual(result["type"], "NUMBER")
            self.assertEqual(result["value"], "42")
            self.assertEqual(parser_state["pos"], 1)
    
    def test_binary_operation(self):
        """Test parsing a binary operation expression."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "+", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "5", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch("._parse_expression_src._parse_primary") as mock_parse_primary, \
             patch("._parse_expression_src._get_precedence") as mock_get_precedence:
            
            # First call returns left operand, second call returns right operand
            mock_parse_primary.side_effect = [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
                {"type": "NUMBER", "value": "5", "line": 1, "column": 5}
            ]
            # First call for '+' returns precedence > 0, second call returns 0 to stop loop
            mock_get_precedence.side_effect = [5, 0]
            
            result = _parse_expression(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["operator"], "+")
            self.assertEqual(result["left"]["type"], "IDENTIFIER")
            self.assertEqual(result["right"]["type"], "NUMBER")
            self.assertEqual(parser_state["pos"], 3)
    
    def test_operator_precedence(self):
        """Test that operator precedence is handled correctly."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "+", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 5},
                {"type": "OPERATOR", "value": "*", "line": 1, "column": 7},
                {"type": "NUMBER", "value": "3", "line": 1, "column": 9}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch("._parse_expression_src._parse_primary") as mock_parse_primary, \
             patch("._parse_expression_src._get_precedence") as mock_get_precedence:
            
            # Mock parse_primary to return NUMBER nodes
            mock_parse_primary.side_effect = [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 5},
                {"type": "NUMBER", "value": "3", "line": 1, "column": 9}
            ]
            # Mock precedence: + has lower precedence than *
            mock_get_precedence.side_effect = [3, 5, 0]  # +, *, end
            
            result = _parse_expression(parser_state)
            
            # Should parse as 1 + (2 * 3), not (1 + 2) * 3
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["operator"], "+")
            self.assertEqual(result["left"]["value"], "1")
            # Right side should be the multiplication
            self.assertEqual(result["right"]["type"], "BINARY_OP")
            self.assertEqual(result["right"]["operator"], "*")
    
    def test_empty_tokens_raises_error(self):
        """Test that empty tokens list raises SyntaxError."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.c"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_expression(parser_state)
        
        self.assertIn("Unexpected end of expression", str(context.exception))
    
    def test_pos_advances_correctly(self):
        """Test that parser_state pos advances correctly."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch("._parse_expression_src._parse_primary") as mock_parse_primary, \
             patch("._parse_expression_src._get_precedence") as mock_get_precedence:
            
            mock_parse_primary.return_value = {
                "type": "IDENTIFIER",
                "value": "x",
                "line": 1,
                "column": 1
            }
            mock_get_precedence.return_value = 0
            
            _parse_expression(parser_state)
            
            self.assertEqual(parser_state["pos"], 1)
    
    def test_multiple_binary_operations(self):
        """Test parsing multiple binary operations in sequence."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "+", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 5},
                {"type": "OPERATOR", "value": "+", "line": 1, "column": 7},
                {"type": "NUMBER", "value": "3", "line": 1, "column": 9}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch("._parse_expression_src._parse_primary") as mock_parse_primary, \
             patch("._parse_expression_src._get_precedence") as mock_get_precedence:
            
            mock_parse_primary.side_effect = [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 5},
                {"type": "NUMBER", "value": "3", "line": 1, "column": 9}
            ]
            # All + operators have same precedence, last returns 0
            mock_get_precedence.side_effect = [3, 3, 0]
            
            result = _parse_expression(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["operator"], "+")
            self.assertEqual(parser_state["pos"], 5)
    
    def test_ast_node_contains_line_column(self):
        """Test that AST nodes contain line and column information."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 5, "column": 10}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch("._parse_expression_src._parse_primary") as mock_parse_primary, \
             patch("._parse_expression_src._get_precedence") as mock_get_precedence:
            
            mock_parse_primary.return_value = {
                "type": "IDENTIFIER",
                "value": "x",
                "line": 5,
                "column": 10
            }
            mock_get_precedence.return_value = 0
            
            result = _parse_expression(parser_state)
            
            self.assertIn("line", result)
            self.assertIn("column", result)
    
    def test_binary_op_preserves_operator_location(self):
        """Test that binary op AST node preserves operator line and column."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "+", "line": 2, "column": 5},
                {"type": "NUMBER", "value": "2", "line": 2, "column": 7}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch("._parse_expression_src._parse_primary") as mock_parse_primary, \
             patch("._parse_expression_src._get_precedence") as mock_get_precedence:
            
            mock_parse_primary.side_effect = [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "NUMBER", "value": "2", "line": 2, "column": 7}
            ]
            mock_get_precedence.side_effect = [5, 0]
            
            result = _parse_expression(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["line"], 2)
            self.assertEqual(result["column"], 5)
    
    def test_non_operator_stops_parsing(self):
        """Test that non-operator token stops binary operation parsing."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "OPERATOR", "value": "+", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 5},
                {"type": "SEMICOLON", "value": ";", "line": 1, "column": 6}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch("._parse_expression_src._parse_primary") as mock_parse_primary, \
             patch("._parse_expression_src._get_precedence") as mock_get_precedence:
            
            mock_parse_primary.side_effect = [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 5}
            ]
            # + has precedence, SEMICOLON has 0 precedence
            mock_get_precedence.side_effect = [5, 0]
            
            result = _parse_expression(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            # Should stop at SEMICOLON, pos should be at 3
            self.assertEqual(parser_state["pos"], 3)


if __name__ == "__main__":
    unittest.main()

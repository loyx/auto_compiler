import unittest
from unittest.mock import patch
from typing import Dict, Any

# Relative import for the function under test
from ._parse_or_expr_src import _parse_or_expr


class TestParseOrExpr(unittest.TestCase):
    """Test cases for _parse_or_expr function."""
    
    def create_token(self, token_type: str, value: str = "", line: int = 1, column: int = 1) -> Dict[str, Any]:
        """Helper to create a token dict."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }
    
    def create_parser_state(self, tokens: list, pos: int = 0, filename: str = "test.py") -> Dict[str, Any]:
        """Helper to create a parser state dict."""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename
        }
    
    def create_ast_node(self, node_type: str, children: list = None, value: Any = None, line: int = 0, column: int = 0) -> Dict[str, Any]:
        """Helper to create an AST node dict."""
        return {
            "type": node_type,
            "children": children if children is not None else [],
            "value": value,
            "line": line,
            "column": column
        }
    
    def test_no_or_operator(self):
        """Test parsing expression without OR operator - should return left side only."""
        parser_state = self.create_parser_state([
            self.create_token("IDENTIFIER", "x")
        ])
        
        left_ast = self.create_ast_node("IDENTIFIER", value="x", line=1, column=1)
        
        with patch('._parse_and_expr_package._parse_and_expr_src._parse_and_expr') as mock_and_expr, \
             patch('._peek_token_package._peek_token_src._peek_token') as mock_peek, \
             patch('._consume_token_package._consume_token_src._consume_token') as mock_consume:
            
            mock_and_expr.return_value = (left_ast, parser_state)
            mock_peek.return_value = None  # No more tokens
            
            result_ast, result_state = _parse_or_expr(parser_state)
            
            mock_and_expr.assert_called_once_with(parser_state)
            mock_peek.assert_called_once()
            mock_consume.assert_not_called()
            
            self.assertEqual(result_ast, left_ast)
            self.assertEqual(result_state, parser_state)
    
    def test_single_or_expression(self):
        """Test parsing single OR expression: expr or expr."""
        parser_state = self.create_parser_state([
            self.create_token("IDENTIFIER", "a"),
            self.create_token("OR", "or", line=1, column=3),
            self.create_token("IDENTIFIER", "b")
        ])
        
        left_ast = self.create_ast_node("IDENTIFIER", value="a", line=1, column=1)
        right_ast = self.create_ast_node("IDENTIFIER", value="b", line=1, column=5)
        
        or_token = self.create_token("OR", "or", line=1, column=3)
        
        with patch('._parse_and_expr_package._parse_and_expr_src._parse_and_expr') as mock_and_expr, \
             patch('._peek_token_package._peek_token_src._peek_token') as mock_peek, \
             patch('._consume_token_package._consume_token_src._consume_token') as mock_consume:
            
            mock_and_expr.side_effect = [
                (left_ast, parser_state),
                (right_ast, parser_state)
            ]
            mock_peek.side_effect = [or_token, None]
            mock_consume.return_value = parser_state
            
            result_ast, result_state = _parse_or_expr(parser_state)
            
            self.assertEqual(mock_and_expr.call_count, 2)
            self.assertEqual(mock_peek.call_count, 2)
            mock_consume.assert_called_once()
            
            self.assertEqual(result_ast["type"], "BINARY_OP")
            self.assertEqual(result_ast["operator"], "or")
            self.assertEqual(result_ast["line"], 1)
            self.assertEqual(result_ast["column"], 3)
            self.assertEqual(len(result_ast["children"]), 2)
            self.assertEqual(result_ast["children"][0], left_ast)
            self.assertEqual(result_ast["children"][1], right_ast)
    
    def test_multiple_or_expressions_left_associative(self):
        """Test parsing multiple OR expressions: expr or expr or expr (left-associative)."""
        parser_state = self.create_parser_state([
            self.create_token("IDENTIFIER", "a"),
            self.create_token("OR", "or", line=1, column=3),
            self.create_token("IDENTIFIER", "b"),
            self.create_token("OR", "or", line=1, column=7),
            self.create_token("IDENTIFIER", "c")
        ])
        
        ast_a = self.create_ast_node("IDENTIFIER", value="a", line=1, column=1)
        ast_b = self.create_ast_node("IDENTIFIER", value="b", line=1, column=5)
        ast_c = self.create_ast_node("IDENTIFIER", value="c", line=1, column=9)
        
        or_token_1 = self.create_token("OR", "or", line=1, column=3)
        or_token_2 = self.create_token("OR", "or", line=1, column=7)
        
        with patch('._parse_and_expr_package._parse_and_expr_src._parse_and_expr') as mock_and_expr, \
             patch('._peek_token_package._peek_token_src._peek_token') as mock_peek, \
             patch('._consume_token_package._consume_token_src._consume_token') as mock_consume:
            
            mock_and_expr.side_effect = [
                (ast_a, parser_state),
                (ast_b, parser_state),
                (ast_c, parser_state)
            ]
            mock_peek.side_effect = [or_token_1, or_token_2, None]
            mock_consume.return_value = parser_state
            
            result_ast, result_state = _parse_or_expr(parser_state)
            
            self.assertEqual(mock_and_expr.call_count, 3)
            self.assertEqual(mock_peek.call_count, 3)
            self.assertEqual(mock_consume.call_count, 2)
            
            # Should be left-associative: (a or b) or c
            self.assertEqual(result_ast["type"], "BINARY_OP")
            self.assertEqual(result_ast["operator"], "or")
            self.assertEqual(result_ast["line"], 1)
            self.assertEqual(result_ast["column"], 7)
            
            # Left child should be (a or b)
            left_child = result_ast["children"][0]
            self.assertEqual(left_child["type"], "BINARY_OP")
            self.assertEqual(left_child["operator"], "or")
            self.assertEqual(left_child["line"], 1)
            self.assertEqual(left_child["column"], 3)
            self.assertEqual(left_child["children"][0], ast_a)
            self.assertEqual(left_child["children"][1], ast_b)
            
            # Right child should be c
            self.assertEqual(result_ast["children"][1], ast_c)
    
    def test_empty_token_list(self):
        """Test parsing with empty token list."""
        parser_state = self.create_parser_state([])
        
        empty_ast = self.create_ast_node("EMPTY")
        
        with patch('._parse_and_expr_package._parse_and_expr_src._parse_and_expr') as mock_and_expr, \
             patch('._peek_token_package._peek_token_src._peek_token') as mock_peek, \
             patch('._consume_token_package._consume_token_src._consume_token') as mock_consume:
            
            mock_and_expr.return_value = (empty_ast, parser_state)
            mock_peek.return_value = None
            
            result_ast, result_state = _parse_or_expr(parser_state)
            
            mock_and_expr.assert_called_once()
            mock_peek.assert_called_once()
            mock_consume.assert_not_called()
            
            self.assertEqual(result_ast, empty_ast)
    
    def test_or_token_preserves_line_column(self):
        """Test that OR token line and column information is preserved in AST."""
        parser_state = self.create_parser_state([
            self.create_token("IDENTIFIER", "x"),
            self.create_token("OR", "or", line=5, column=10),
            self.create_token("IDENTIFIER", "y")
        ])
        
        left_ast = self.create_ast_node("IDENTIFIER", value="x")
        right_ast = self.create_ast_node("IDENTIFIER", value="y")
        
        or_token = self.create_token("OR", "or", line=5, column=10)
        
        with patch('._parse_and_expr_package._parse_and_expr_src._parse_and_expr') as mock_and_expr, \
             patch('._peek_token_package._peek_token_src._peek_token') as mock_peek, \
             patch('._consume_token_package._consume_token_src._consume_token') as mock_consume:
            
            mock_and_expr.side_effect = [
                (left_ast, parser_state),
                (right_ast, parser_state)
            ]
            mock_peek.side_effect = [or_token, None]
            mock_consume.return_value = parser_state
            
            result_ast, result_state = _parse_or_expr(parser_state)
            
            self.assertEqual(result_ast["line"], 5)
            self.assertEqual(result_ast["column"], 10)
    
    def test_non_or_token_stops_parsing(self):
        """Test that non-OR token stops the OR parsing loop."""
        parser_state = self.create_parser_state([
            self.create_token("IDENTIFIER", "a"),
            self.create_token("AND", "and"),
            self.create_token("IDENTIFIER", "b")
        ])
        
        left_ast = self.create_ast_node("IDENTIFIER", value="a")
        
        and_token = self.create_token("AND", "and")
        
        with patch('._parse_and_expr_package._parse_and_expr_src._parse_and_expr') as mock_and_expr, \
             patch('._peek_token_package._peek_token_src._peek_token') as mock_peek, \
             patch('._consume_token_package._consume_token_src._consume_token') as mock_consume:
            
            mock_and_expr.return_value = (left_ast, parser_state)
            mock_peek.return_value = and_token
            
            result_ast, result_state = _parse_or_expr(parser_state)
            
            mock_and_expr.assert_called_once()
            mock_peek.assert_called_once()
            mock_consume.assert_not_called()
            
            self.assertEqual(result_ast, left_ast)


if __name__ == "__main__":
    unittest.main()

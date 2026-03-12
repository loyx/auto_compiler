import unittest
from unittest.mock import patch
from typing import Dict, Any, List

# Relative import from the same package
from ._parse_additive_expr_src import _parse_additive_expr


class TestParseAdditiveExpr(unittest.TestCase):
    """Test cases for _parse_additive_expr function."""

    def _create_parser_state(self, tokens: List[Dict[str, Any]], pos: int = 0, filename: str = "test.py") -> Dict[str, Any]:
        """Helper to create parser state dict."""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename
        }

    def _create_token(self, token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """Helper to create token dict."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def _create_ast_node(self, node_type: str, value: Any = None, children: List = None, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """Helper to create AST node dict."""
        return {
            "type": node_type,
            "value": value,
            "children": children or [],
            "line": line,
            "column": column
        }

    @patch('._parse_additive_expr_src._parse_multiplicative_expr')
    def test_single_multiplicative_expr_no_operator(self, mock_multiplicative):
        """Test parsing when there's no additive operator (just multiplicative expression)."""
        # Setup mock to return a simple AST node
        mock_multiplicative.return_value = self._create_ast_node("IDENTIFIER", "x")
        
        # Create parser state with no additive operators
        tokens = [self._create_token("IDENTIFIER", "x")]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # Call function
        result = _parse_additive_expr(parser_state)
        
        # Verify result
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "x")
        
        # Verify mock was called once
        mock_multiplicative.assert_called_once()
        
        # Position should be advanced by mock (assuming mock consumes one token)
        self.assertEqual(parser_state["pos"], 1)

    @patch('._parse_additive_expr_src._parse_multiplicative_expr')
    def test_simple_addition(self, mock_multiplicative):
        """Test parsing simple addition: a + b."""
        # Setup mock to return different values on successive calls
        left_node = self._create_ast_node("IDENTIFIER", "a", line=1, column=1)
        right_node = self._create_ast_node("IDENTIFIER", "b", line=1, column=5)
        mock_multiplicative.side_effect = [left_node, right_node]
        
        # Create parser state with addition operator
        tokens = [
            self._create_token("IDENTIFIER", "a", line=1, column=1),
            self._create_token("PLUS", "+", line=1, column=3),
            self._create_token("IDENTIFIER", "b", line=1, column=5)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # Call function
        result = _parse_additive_expr(parser_state)
        
        # Verify result is BINARY_OP
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "+")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 3)
        
        # Verify children
        self.assertEqual(len(result["children"]), 2)
        self.assertEqual(result["children"][0]["type"], "IDENTIFIER")
        self.assertEqual(result["children"][0]["value"], "a")
        self.assertEqual(result["children"][1]["type"], "IDENTIFIER")
        self.assertEqual(result["children"][1]["value"], "b")
        
        # Verify mock was called twice (left and right)
        self.assertEqual(mock_multiplicative.call_count, 2)
        
        # Position should be at end (3 tokens consumed)
        self.assertEqual(parser_state["pos"], 3)

    @patch('._parse_additive_expr_src._parse_multiplicative_expr')
    def test_simple_subtraction(self, mock_multiplicative):
        """Test parsing simple subtraction: a - b."""
        # Setup mock to return different values on successive calls
        left_node = self._create_ast_node("IDENTIFIER", "a", line=1, column=1)
        right_node = self._create_ast_node("IDENTIFIER", "b", line=1, column=5)
        mock_multiplicative.side_effect = [left_node, right_node]
        
        # Create parser state with subtraction operator
        tokens = [
            self._create_token("IDENTIFIER", "a", line=1, column=1),
            self._create_token("MINUS", "-", line=1, column=3),
            self._create_token("IDENTIFIER", "b", line=1, column=5)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # Call function
        result = _parse_additive_expr(parser_state)
        
        # Verify result is BINARY_OP with minus
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "-")
        self.assertEqual(result["children"][0]["value"], "a")
        self.assertEqual(result["children"][1]["value"], "b")

    @patch('._parse_additive_expr_src._parse_multiplicative_expr')
    def test_left_associativity(self, mock_multiplicative):
        """Test left associativity: a + b - c should be ((a + b) - c)."""
        # Setup mock to return different values on successive calls
        node_a = self._create_ast_node("IDENTIFIER", "a", line=1, column=1)
        node_b = self._create_ast_node("IDENTIFIER", "b", line=1, column=5)
        node_c = self._create_ast_node("IDENTIFIER", "c", line=1, column=9)
        mock_multiplicative.side_effect = [node_a, node_b, node_c]
        
        # Create parser state with multiple operators
        tokens = [
            self._create_token("IDENTIFIER", "a", line=1, column=1),
            self._create_token("PLUS", "+", line=1, column=3),
            self._create_token("IDENTIFIER", "b", line=1, column=5),
            self._create_token("MINUS", "-", line=1, column=7),
            self._create_token("IDENTIFIER", "c", line=1, column=9)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # Call function
        result = _parse_additive_expr(parser_state)
        
        # Verify outer operation is subtraction (left associative)
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "-")
        
        # Left child should be the addition (a + b)
        left_child = result["children"][0]
        self.assertEqual(left_child["type"], "BINARY_OP")
        self.assertEqual(left_child["value"], "+")
        self.assertEqual(left_child["children"][0]["value"], "a")
        self.assertEqual(left_child["children"][1]["value"], "b")
        
        # Right child should be c
        right_child = result["children"][1]
        self.assertEqual(right_child["type"], "IDENTIFIER")
        self.assertEqual(right_child["value"], "c")
        
        # Verify mock was called three times
        self.assertEqual(mock_multiplicative.call_count, 3)

    @patch('._parse_additive_expr_src._parse_multiplicative_expr')
    def test_multiple_additions(self, mock_multiplicative):
        """Test multiple additions: a + b + c."""
        # Setup mock to return different values on successive calls
        node_a = self._create_ast_node("IDENTIFIER", "a", line=1, column=1)
        node_b = self._create_ast_node("IDENTIFIER", "b", line=1, column=5)
        node_c = self._create_ast_node("IDENTIFIER", "c", line=1, column=9)
        mock_multiplicative.side_effect = [node_a, node_b, node_c]
        
        # Create parser state with multiple plus operators
        tokens = [
            self._create_token("IDENTIFIER", "a", line=1, column=1),
            self._create_token("PLUS", "+", line=1, column=3),
            self._create_token("IDENTIFIER", "b", line=1, column=5),
            self._create_token("PLUS", "+", line=1, column=7),
            self._create_token("IDENTIFIER", "c", line=1, column=9)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # Call function
        result = _parse_additive_expr(parser_state)
        
        # Verify structure
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "+")
        
        # Left associative: (a + b) + c
        self.assertEqual(result["children"][0]["value"], "+")
        self.assertEqual(result["children"][0]["children"][0]["value"], "a")
        self.assertEqual(result["children"][0]["children"][1]["value"], "b")
        self.assertEqual(result["children"][1]["value"], "c")

    @patch('._parse_additive_expr_src._parse_multiplicative_expr')
    def test_empty_tokens(self, mock_multiplicative):
        """Test with empty token list."""
        # Setup mock (should not be called if no tokens)
        mock_multiplicative.return_value = self._create_ast_node("LITERAL", 0)
        
        # Create parser state with empty tokens
        parser_state = self._create_parser_state([], pos=0)
        
        # Call function - should handle gracefully
        result = _parse_additive_expr(parser_state)
        
        # Should return what multiplicative expr returns
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], 0)

    @patch('._parse_additive_expr_src._parse_multiplicative_expr')
    def test_position_at_end(self, mock_multiplicative):
        """Test when position is already at end of tokens."""
        # Setup mock
        mock_multiplicative.return_value = self._create_ast_node("IDENTIFIER", "x")
        
        # Create parser state with pos at end
        tokens = [self._create_token("IDENTIFIER", "x")]
        parser_state = self._create_parser_state(tokens, pos=1)  # Already at end
        
        # Call function
        result = _parse_additive_expr(parser_state)
        
        # Should still call multiplicative expr once
        mock_multiplicative.assert_called_once()
        self.assertEqual(result["type"], "IDENTIFIER")

    @patch('._parse_additive_expr_src._parse_multiplicative_expr')
    def test_complex_expression_with_literals(self, mock_multiplicative):
        """Test expression with numeric literals: 1 + 2 - 3."""
        # Setup mock to return literal nodes
        node_1 = self._create_ast_node("LITERAL", 1, line=1, column=1)
        node_2 = self._create_ast_node("LITERAL", 2, line=1, column=5)
        node_3 = self._create_ast_node("LITERAL", 3, line=1, column=9)
        mock_multiplicative.side_effect = [node_1, node_2, node_3]
        
        # Create parser state
        tokens = [
            self._create_token("LITERAL", "1", line=1, column=1),
            self._create_token("PLUS", "+", line=1, column=3),
            self._create_token("LITERAL", "2", line=1, column=5),
            self._create_token("MINUS", "-", line=1, column=7),
            self._create_token("LITERAL", "3", line=1, column=9)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # Call function
        result = _parse_additive_expr(parser_state)
        
        # Verify structure
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "-")
        self.assertEqual(result["children"][0]["value"], "+")
        
        # Position should be at end
        self.assertEqual(parser_state["pos"], 5)

    @patch('._parse_additive_expr_src._parse_multiplicative_expr')
    def test_operator_token_metadata_preserved(self, mock_multiplicative):
        """Test that operator token metadata (line, column) is preserved in AST."""
        # Setup mock
        left_node = self._create_ast_node("IDENTIFIER", "a", line=2, column=10)
        right_node = self._create_ast_node("IDENTIFIER", "b", line=2, column=15)
        mock_multiplicative.side_effect = [left_node, right_node]
        
        # Create parser state with operator at specific location
        tokens = [
            self._create_token("IDENTIFIER", "a", line=2, column=10),
            self._create_token("PLUS", "+", line=2, column=12),
            self._create_token("IDENTIFIER", "b", line=2, column=15)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # Call function
        result = _parse_additive_expr(parser_state)
        
        # Verify operator metadata is preserved
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 12)


if __name__ == "__main__":
    unittest.main()

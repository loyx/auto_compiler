import unittest
from unittest.mock import patch, MagicMock
from typing import Dict, Any

from ._parse_comparison_src import _parse_comparison


class TestParseComparison(unittest.TestCase):
    """Test cases for _parse_comparison function."""
    
    def _create_token(self, token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """Helper to create a token dictionary."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }
    
    def _create_parser_state(self, tokens: list, pos: int = 0, filename: str = "test.py") -> Dict[str, Any]:
        """Helper to create a parser state dictionary."""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename
        }
    
    def _create_ast_node(self, node_type: str, children: list = None, value: Any = None, 
                         line: int = 1, column: int = 1) -> Dict[str, Any]:
        """Helper to create an AST node dictionary."""
        return {
            "type": node_type,
            "children": children or [],
            "value": value,
            "line": line,
            "column": column
        }
    
    @patch('._parse_comparison_package._parse_additive_package._parse_additive_src._parse_additive')
    def test_no_comparison_operator(self, mock_parse_additive: MagicMock) -> None:
        """Test when there's no comparison operator - should return left operand as-is."""
        left_node = self._create_ast_node("IDENTIFIER", value="x")
        mock_parse_additive.return_value = left_node
        
        tokens = [self._create_token("IDENTIFIER", "x")]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        result = _parse_comparison(parser_state)
        
        self.assertEqual(result, left_node)
        self.assertEqual(parser_state["pos"], 0)
        mock_parse_additive.assert_called_once_with(parser_state)
    
    @patch('._parse_comparison_package._parse_additive_package._parse_additive_src._parse_additive')
    def test_less_than_operator(self, mock_parse_additive: MagicMock) -> None:
        """Test parsing a < b."""
        left_node = self._create_ast_node("IDENTIFIER", value="a")
        right_node = self._create_ast_node("NUMBER", value="5")
        mock_parse_additive.side_effect = [left_node, right_node]
        
        tokens = [
            self._create_token("IDENTIFIER", "a", line=1, column=1),
            self._create_token("OP", "<", line=1, column=3),
            self._create_token("NUMBER", "5", line=1, column=5)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        result = _parse_comparison(parser_state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "<")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 3)
        self.assertEqual(len(result["children"]), 2)
        self.assertEqual(result["children"][0], left_node)
        self.assertEqual(result["children"][1], right_node)
        self.assertEqual(parser_state["pos"], 3)
    
    @patch('._parse_comparison_package._parse_additive_package._parse_additive_src._parse_additive')
    def test_equality_operator(self, mock_parse_additive: MagicMock) -> None:
        """Test parsing a == b."""
        left_node = self._create_ast_node("IDENTIFIER", value="a")
        right_node = self._create_ast_node("IDENTIFIER", value="b")
        mock_parse_additive.side_effect = [left_node, right_node]
        
        tokens = [
            self._create_token("IDENTIFIER", "a", line=2, column=1),
            self._create_token("OP", "==", line=2, column=3),
            self._create_token("IDENTIFIER", "b", line=2, column=6)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        result = _parse_comparison(parser_state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "==")
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 3)
        self.assertEqual(parser_state["pos"], 3)
    
    @patch('._parse_comparison_package._parse_additive_package._parse_additive_src._parse_additive')
    def test_chained_comparisons(self, mock_parse_additive: MagicMock) -> None:
        """Test parsing chained comparisons like a < b <= c."""
        left_node = self._create_ast_node("IDENTIFIER", value="a")
        middle_node = self._create_ast_node("IDENTIFIER", value="b")
        right_node = self._create_ast_node("NUMBER", value="2")
        mock_parse_additive.side_effect = [left_node, middle_node, right_node]
        
        tokens = [
            self._create_token("IDENTIFIER", "a", line=1, column=1),
            self._create_token("OP", "<", line=1, column=3),
            self._create_token("IDENTIFIER", "b", line=1, column=5),
            self._create_token("OP", "<=", line=1, column=7),
            self._create_token("NUMBER", "2", line=1, column=10)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        result = _parse_comparison(parser_state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "<=")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 7)
        self.assertEqual(parser_state["pos"], 5)
        
        left_subtree = result["children"][0]
        self.assertEqual(left_subtree["type"], "BINARY_OP")
        self.assertEqual(left_subtree["value"], "<")
        self.assertEqual(left_subtree["children"][0], left_node)
        self.assertEqual(left_subtree["children"][1], middle_node)
        
        self.assertEqual(result["children"][1], right_node)
    
    @patch('._parse_comparison_package._parse_additive_package._parse_additive_src._parse_additive')
    def test_all_comparison_operators(self, mock_parse_additive: MagicMock) -> None:
        """Test all comparison operators: ==, !=, <, >, <=, >=."""
        comparison_ops = ["==", "!=", "<", ">", "<=", ">="]
        
        for op in comparison_ops:
            with self.subTest(operator=op):
                mock_parse_additive.reset_mock()
                left_node = self._create_ast_node("IDENTIFIER", value="x")
                right_node = self._create_ast_node("NUMBER", value="1")
                mock_parse_additive.side_effect = [left_node, right_node]
                
                tokens = [
                    self._create_token("IDENTIFIER", "x"),
                    self._create_token("OP", op),
                    self._create_token("NUMBER", "1")
                ]
                parser_state = self._create_parser_state(tokens, pos=0)
                
                result = _parse_comparison(parser_state)
                
                self.assertEqual(result["type"], "BINARY_OP")
                self.assertEqual(result["value"], op)
                self.assertEqual(len(result["children"]), 2)
                self.assertEqual(parser_state["pos"], 3)
    
    @patch('._parse_comparison_package._parse_additive_package._parse_additive_src._parse_additive')
    def test_empty_tokens(self, mock_parse_additive: MagicMock) -> None:
        """Test with empty token list."""
        left_node = self._create_ast_node("IDENTIFIER", value="x")
        mock_parse_additive.return_value = left_node
        
        parser_state = self._create_parser_state([], pos=0)
        
        result = _parse_comparison(parser_state)
        
        self.assertEqual(result, left_node)
        self.assertEqual(parser_state["pos"], 0)
    
    @patch('._parse_comparison_package._parse_additive_package._parse_additive_src._parse_additive')
    def test_stops_at_non_comparison_operator(self, mock_parse_additive: MagicMock) -> None:
        """Test that parsing stops at non-comparison operators like +."""
        left_node = self._create_ast_node("IDENTIFIER", value="a")
        right_node = self._create_ast_node("NUMBER", value="1")
        mock_parse_additive.side_effect = [left_node, right_node]
        
        tokens = [
            self._create_token("IDENTIFIER", "a"),
            self._create_token("OP", "+"),
            self._create_token("NUMBER", "1")
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        result = _parse_comparison(parser_state)
        
        self.assertEqual(result, left_node)
        self.assertEqual(parser_state["pos"], 0)
        mock_parse_additive.assert_called_once()
    
    @patch('._parse_comparison_package._parse_additive_package._parse_additive_src._parse_additive')
    def test_preserves_operator_position(self, mock_parse_additive: MagicMock) -> None:
        """Test that line and column from operator token are preserved in AST."""
        left_node = self._create_ast_node("IDENTIFIER", value="a")
        right_node = self._create_ast_node("NUMBER", value="10")
        mock_parse_additive.side_effect = [left_node, right_node]
        
        tokens = [
            self._create_token("IDENTIFIER", "a", line=5, column=10),
            self._create_token("OP", ">=", line=5, column=12),
            self._create_token("NUMBER", "10", line=5, column=15)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        result = _parse_comparison(parser_state)
        
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 12)
    
    @patch('._parse_comparison_package._parse_additive_package._parse_additive_src._parse_additive')
    def test_position_at_end_of_tokens(self, mock_parse_additive: MagicMock) -> None:
        """Test when position is already at end of tokens."""
        left_node = self._create_ast_node("IDENTIFIER", value="x")
        mock_parse_additive.return_value = left_node
        
        tokens = [self._create_token("IDENTIFIER", "x")]
        parser_state = self._create_parser_state(tokens, pos=1)
        
        result = _parse_comparison(parser_state)
        
        self.assertEqual(result, left_node)
        self.assertEqual(parser_state["pos"], 1)


if __name__ == "__main__":
    unittest.main()

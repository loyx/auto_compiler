# === std / third-party imports ===
import unittest
from unittest.mock import patch, MagicMock
from typing import Dict, Any

# === relative imports ===
from ._parse_and_expr_src import _parse_and_expr, _is_and_token, _consume_current_token


class TestParseAndExpr(unittest.TestCase):
    """Test cases for _parse_and_expr function."""

    def _create_parser_state(self, tokens: list, pos: int = 0, filename: str = "test.py") -> Dict[str, Any]:
        """Helper to create parser state."""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename
        }

    def _create_token(self, token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """Helper to create a token."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def _create_ast_node(self, node_type: str, value: Any = None, children: list = None, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """Helper to create an AST node."""
        return {
            "type": node_type,
            "value": value,
            "children": children if children is not None else [],
            "line": line,
            "column": column
        }

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_and_expr_package._parse_and_expr_src._parse_comparison')
    def test_single_comparison_no_and(self, mock_parse_comparison: MagicMock):
        """Test parsing a single comparison expression without 'and'."""
        # Setup
        left_node = self._create_ast_node("IDENTIFIER", "x", line=1, column=1)
        mock_parse_comparison.return_value = left_node
        
        tokens = [self._create_token("IDENTIFIER", "x")]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # Execute
        result = _parse_and_expr(parser_state)
        
        # Verify
        self.assertEqual(result, left_node)
        self.assertEqual(parser_state["pos"], 0)  # pos should not advance since no AND token
        mock_parse_comparison.assert_called_once_with(parser_state)

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_and_expr_package._parse_and_expr_src._parse_comparison')
    def test_one_and_expression(self, mock_parse_comparison: MagicMock):
        """Test parsing 'x and y' expression."""
        # Setup
        left_node = self._create_ast_node("IDENTIFIER", "x", line=1, column=1)
        right_node = self._create_ast_node("IDENTIFIER", "y", line=1, column=5)
        and_token = self._create_token("AND", "and", line=1, column=3)
        
        # First call returns left, second call returns right
        mock_parse_comparison.side_effect = [left_node, right_node]
        
        tokens = [
            self._create_token("IDENTIFIER", "x", line=1, column=1),
            and_token,
            self._create_token("IDENTIFIER", "y", line=1, column=5)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # Execute
        result = _parse_and_expr(parser_state)
        
        # Verify
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "and")
        self.assertEqual(len(result["children"]), 2)
        self.assertEqual(result["children"][0], left_node)
        self.assertEqual(result["children"][1], right_node)
        self.assertEqual(parser_state["pos"], 2)  # Should consume identifier and AND token
        self.assertEqual(mock_parse_comparison.call_count, 2)

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_and_expr_package._parse_and_expr_src._parse_comparison')
    def test_multiple_and_left_associative(self, mock_parse_comparison: MagicMock):
        """Test parsing 'x and y and z' with left-associativity."""
        # Setup
        node_x = self._create_ast_node("IDENTIFIER", "x", line=1, column=1)
        node_y = self._create_ast_node("IDENTIFIER", "y", line=1, column=5)
        node_z = self._create_ast_node("IDENTIFIER", "z", line=1, column=9)
        and_token1 = self._create_token("AND", "and", line=1, column=3)
        and_token2 = self._create_token("AND", "and", line=1, column=7)
        
        # Three calls: x, y, z
        mock_parse_comparison.side_effect = [node_x, node_y, node_z]
        
        tokens = [
            self._create_token("IDENTIFIER", "x", line=1, column=1),
            and_token1,
            self._create_token("IDENTIFIER", "y", line=1, column=5),
            and_token2,
            self._create_token("IDENTIFIER", "z", line=1, column=9)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # Execute
        result = _parse_and_expr(parser_state)
        
        # Verify left-associative: ((x and y) and z)
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "and")
        self.assertEqual(len(result["children"]), 2)
        
        # Right child should be z
        self.assertEqual(result["children"][1], node_z)
        
        # Left child should be (x and y)
        left_child = result["children"][0]
        self.assertEqual(left_child["type"], "BINARY_OP")
        self.assertEqual(left_child["value"], "and")
        self.assertEqual(len(left_child["children"]), 2)
        self.assertEqual(left_child["children"][0], node_x)
        self.assertEqual(left_child["children"][1], node_y)
        
        self.assertEqual(parser_state["pos"], 4)  # Should consume all tokens
        self.assertEqual(mock_parse_comparison.call_count, 3)

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_and_expr_package._parse_and_expr_src._parse_comparison')
    def test_empty_tokens(self, mock_parse_comparison: MagicMock):
        """Test parsing with empty token list."""
        # Setup
        mock_parse_comparison.side_effect = IndexError("No tokens")
        
        tokens = []
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # Execute & Verify
        with self.assertRaises(IndexError):
            _parse_and_expr(parser_state)

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_and_expr_package._parse_and_expr_src._parse_comparison')
    def test_and_at_end_incomplete(self, mock_parse_comparison: MagicMock):
        """Test parsing 'x and' without right operand."""
        # Setup
        left_node = self._create_ast_node("IDENTIFIER", "x", line=1, column=1)
        and_token = self._create_token("AND", "and", line=1, column=3)
        
        mock_parse_comparison.side_effect = [left_node, IndexError("No right operand")]
        
        tokens = [
            self._create_token("IDENTIFIER", "x", line=1, column=1),
            and_token
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # Execute & Verify
        with self.assertRaises(IndexError):
            _parse_and_expr(parser_state)

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_and_expr_package._parse_and_expr_src._parse_comparison')
    def test_preserves_line_column_info(self, mock_parse_comparison: MagicMock):
        """Test that line and column information is preserved in result."""
        # Setup
        left_node = self._create_ast_node("IDENTIFIER", "x", line=5, column=10)
        right_node = self._create_ast_node("IDENTIFIER", "y", line=5, column=15)
        and_token = self._create_token("AND", "and", line=5, column=12)
        
        mock_parse_comparison.side_effect = [left_node, right_node]
        
        tokens = [
            self._create_token("IDENTIFIER", "x", line=5, column=10),
            and_token,
            self._create_token("IDENTIFIER", "y", line=5, column=15)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        # Execute
        result = _parse_and_expr(parser_state)
        
        # Verify
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 10)


class TestIsAndToken(unittest.TestCase):
    """Test cases for _is_and_token helper function."""

    def _create_parser_state(self, tokens: list, pos: int = 0) -> Dict[str, Any]:
        """Helper to create parser state."""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": "test.py"
        }

    def _create_token(self, token_type: str, value: str) -> Dict[str, Any]:
        """Helper to create a token."""
        return {
            "type": token_type,
            "value": value,
            "line": 1,
            "column": 1
        }

    def test_is_and_token_true(self):
        """Test when current token is AND."""
        tokens = [self._create_token("AND", "and")]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        result = _is_and_token(parser_state)
        
        self.assertTrue(result)

    def test_is_and_token_false_different_type(self):
        """Test when current token is not AND."""
        tokens = [self._create_token("IDENTIFIER", "x")]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        result = _is_and_token(parser_state)
        
        self.assertFalse(result)

    def test_is_and_token_false_pos_out_of_bounds(self):
        """Test when pos is beyond token list."""
        tokens = [self._create_token("IDENTIFIER", "x")]
        parser_state = self._create_parser_state(tokens, pos=5)
        
        result = _is_and_token(parser_state)
        
        self.assertFalse(result)

    def test_is_and_token_false_empty_tokens(self):
        """Test when token list is empty."""
        tokens = []
        parser_state = self._create_parser_state(tokens, pos=0)
        
        result = _is_and_token(parser_state)
        
        self.assertFalse(result)


class TestConsumeCurrentToken(unittest.TestCase):
    """Test cases for _consume_current_token helper function."""

    def _create_parser_state(self, tokens: list, pos: int = 0) -> Dict[str, Any]:
        """Helper to create parser state."""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": "test.py"
        }

    def _create_token(self, token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """Helper to create a token."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def test_consume_token_advances_pos(self):
        """Test that consuming token advances pos."""
        token = self._create_token("AND", "and")
        tokens = [token]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        result = _consume_current_token(parser_state)
        
        self.assertEqual(result, token)
        self.assertEqual(parser_state["pos"], 1)

    def test_consume_token_returns_correct_token(self):
        """Test that correct token is returned."""
        token1 = self._create_token("IDENTIFIER", "x")
        token2 = self._create_token("AND", "and")
        tokens = [token1, token2]
        parser_state = self._create_parser_state(tokens, pos=1)
        
        result = _consume_current_token(parser_state)
        
        self.assertEqual(result, token2)
        self.assertEqual(parser_state["pos"], 2)


if __name__ == "__main__":
    unittest.main()

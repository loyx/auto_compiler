import unittest
from unittest.mock import patch
from typing import Dict, Any

from ._parse_comparison_expr_src import _parse_comparison_expr


class TestParseComparisonExpr(unittest.TestCase):
    """Test cases for _parse_comparison_expr function."""
    
    def _create_token(self, token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """Helper to create a token dict."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }
    
    def _create_ast_node(self, node_type: str, value: Any = None, children: list = None, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """Helper to create an AST node dict."""
        return {
            "type": node_type,
            "value": value,
            "children": children or [],
            "line": line,
            "column": column
        }

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_and_expr_package._parse_comparison_expr_package._parse_comparison_expr_src._parse_additive_expr')
    def test_comparison_less_than(self, mock_additive):
        """Test parsing 'a < b' expression."""
        mock_additive.side_effect = [
            self._create_ast_node("IDENTIFIER", "a"),
            self._create_ast_node("IDENTIFIER", "b")
        ]
        
        parser_state = {
            "tokens": [
                self._create_token("LESS", "<", 1, 3)
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_comparison_expr(parser_state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "<")
        self.assertEqual(len(result["children"]), 2)
        self.assertEqual(parser_state["pos"], 1)
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 3)

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_and_expr_package._parse_comparison_expr_package._parse_comparison_expr_src._parse_additive_expr')
    def test_comparison_greater_than(self, mock_additive):
        """Test parsing 'a > b' expression."""
        mock_additive.side_effect = [
            self._create_ast_node("IDENTIFIER", "a"),
            self._create_ast_node("IDENTIFIER", "b")
        ]
        
        parser_state = {
            "tokens": [
                self._create_token("GREATER", ">", 1, 3)
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_comparison_expr(parser_state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], ">")
        self.assertEqual(parser_state["pos"], 1)

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_and_expr_package._parse_comparison_expr_package._parse_comparison_expr_src._parse_additive_expr')
    def test_comparison_less_equal(self, mock_additive):
        """Test parsing 'a <= b' expression."""
        mock_additive.side_effect = [
            self._create_ast_node("IDENTIFIER", "a"),
            self._create_ast_node("IDENTIFIER", "b")
        ]
        
        parser_state = {
            "tokens": [
                self._create_token("LESS_EQ", "<=", 1, 3)
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_comparison_expr(parser_state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "<=")
        self.assertEqual(parser_state["pos"], 1)

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_and_expr_package._parse_comparison_expr_package._parse_comparison_expr_src._parse_additive_expr')
    def test_comparison_greater_equal(self, mock_additive):
        """Test parsing 'a >= b' expression."""
        mock_additive.side_effect = [
            self._create_ast_node("IDENTIFIER", "a"),
            self._create_ast_node("IDENTIFIER", "b")
        ]
        
        parser_state = {
            "tokens": [
                self._create_token("GREATER_EQ", ">=", 1, 3)
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_comparison_expr(parser_state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], ">=")
        self.assertEqual(parser_state["pos"], 1)

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_and_expr_package._parse_comparison_expr_package._parse_comparison_expr_src._parse_additive_expr')
    def test_comparison_equal(self, mock_additive):
        """Test parsing 'a == b' expression."""
        mock_additive.side_effect = [
            self._create_ast_node("IDENTIFIER", "a"),
            self._create_ast_node("IDENTIFIER", "b")
        ]
        
        parser_state = {
            "tokens": [
                self._create_token("EQ", "==", 1, 3)
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_comparison_expr(parser_state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "==")
        self.assertEqual(parser_state["pos"], 1)

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_and_expr_package._parse_comparison_expr_package._parse_comparison_expr_src._parse_additive_expr')
    def test_comparison_not_equal(self, mock_additive):
        """Test parsing 'a != b' expression."""
        mock_additive.side_effect = [
            self._create_ast_node("IDENTIFIER", "a"),
            self._create_ast_node("IDENTIFIER", "b")
        ]
        
        parser_state = {
            "tokens": [
                self._create_token("NEQ", "!=", 1, 3)
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_comparison_expr(parser_state)
        
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "!=")
        self.assertEqual(parser_state["pos"], 1)

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_and_expr_package._parse_comparison_expr_package._parse_comparison_expr_src._parse_additive_expr')
    def test_no_comparison_operator(self, mock_additive):
        """Test when there's no comparison operator - should return left operand."""
        left_node = self._create_ast_node("IDENTIFIER", "a")
        mock_additive.return_value = left_node
        
        parser_state = {
            "tokens": [
                self._create_token("PLUS", "+", 1, 3)
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_comparison_expr(parser_state)
        
        self.assertEqual(result, left_node)
        self.assertEqual(parser_state["pos"], 0)

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_and_expr_package._parse_comparison_expr_package._parse_comparison_expr_src._parse_additive_expr')
    def test_empty_tokens(self, mock_additive):
        """Test with empty tokens list."""
        left_node = self._create_ast_node("IDENTIFIER", "a")
        mock_additive.return_value = left_node
        
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_comparison_expr(parser_state)
        
        self.assertEqual(result, left_node)

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_and_expr_package._parse_comparison_expr_package._parse_comparison_expr_src._parse_additive_expr')
    def test_pos_at_end(self, mock_additive):
        """Test when pos is at or beyond token list length."""
        left_node = self._create_ast_node("IDENTIFIER", "a")
        mock_additive.return_value = left_node
        
        parser_state = {
            "tokens": [
                self._create_token("LESS", "<")
            ],
            "pos": 1,
            "filename": "test.py"
        }
        
        result = _parse_comparison_expr(parser_state)
        
        self.assertEqual(result, left_node)

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_and_expr_package._parse_comparison_expr_package._parse_comparison_expr_src._parse_additive_expr')
    def test_missing_pos_field(self, mock_additive):
        """Test when parser_state missing pos field."""
        left_node = self._create_ast_node("IDENTIFIER", "a")
        mock_additive.return_value = left_node
        
        parser_state = {
            "tokens": [],
            "filename": "test.py"
        }
        
        result = _parse_comparison_expr(parser_state)
        
        self.assertEqual(result, left_node)

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_and_expr_package._parse_comparison_expr_package._parse_comparison_expr_src._parse_additive_expr')
    def test_missing_tokens_field(self, mock_additive):
        """Test when parser_state missing tokens field."""
        left_node = self._create_ast_node("IDENTIFIER", "a")
        mock_additive.return_value = left_node
        
        parser_state = {
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_comparison_expr(parser_state)
        
        self.assertEqual(result, left_node)

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_and_expr_package._parse_comparison_expr_package._parse_comparison_expr_src._parse_additive_expr')
    def test_token_missing_type_field(self, mock_additive):
        """Test when token missing type field."""
        left_node = self._create_ast_node("IDENTIFIER", "a")
        mock_additive.return_value = left_node
        
        parser_state = {
            "tokens": [
                {"value": "<", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_comparison_expr(parser_state)
        
        self.assertEqual(result, left_node)

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_and_expr_package._parse_comparison_expr_package._parse_comparison_expr_src._parse_additive_expr')
    def test_preserves_line_column_info(self, mock_additive):
        """Test that line and column from operator token are preserved."""
        mock_additive.side_effect = [
            self._create_ast_node("IDENTIFIER", "a"),
            self._create_ast_node("IDENTIFIER", "b")
        ]
        
        parser_state = {
            "tokens": [
                self._create_token("LESS", "<", line=5, column=10)
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_comparison_expr(parser_state)
        
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 10)

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_and_expr_package._parse_comparison_expr_package._parse_comparison_expr_src._parse_additive_expr')
    def test_additive_expr_called_twice(self, mock_additive):
        """Test that _parse_additive_expr is called twice for comparison."""
        mock_additive.side_effect = [
            self._create_ast_node("IDENTIFIER", "left"),
            self._create_ast_node("IDENTIFIER", "right")
        ]
        
        parser_state = {
            "tokens": [
                self._create_token("LESS", "<")
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        _parse_comparison_expr(parser_state)
        
        self.assertEqual(mock_additive.call_count, 2)


if __name__ == "__main__":
    unittest.main()

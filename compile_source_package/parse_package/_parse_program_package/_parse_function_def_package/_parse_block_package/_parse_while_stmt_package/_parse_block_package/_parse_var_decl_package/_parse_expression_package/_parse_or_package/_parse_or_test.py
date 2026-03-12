# === std / third-party imports ===
import unittest
from typing import Any, Dict, List
from unittest.mock import patch

# === sub function imports ===
from ._parse_or_src import _parse_or, _is_current_token_or


class TestParseOr(unittest.TestCase):
    """Test cases for _parse_or function."""

    def setUp(self):
        """Set up test fixtures."""
        self.base_parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.c",
            "error": None
        }

    def _create_token(self, token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """Helper to create a token dictionary."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def _create_ast_node(self, node_type: str, value: Any = None, 
                         children: List = None, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """Helper to create an AST node dictionary."""
        return {
            "type": node_type,
            "value": value,
            "children": children or [],
            "line": line,
            "column": column
        }

    # ==================== Happy Path Tests ====================

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_var_decl_package._parse_expression_package._parse_or_package._parse_or_src._parse_and')
    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_var_decl_package._parse_expression_package._parse_or_package._parse_or_src._consume_token')
    def test_parse_or_single_expression_no_or(self, mock_consume_token, mock_parse_and):
        """Test parsing a single expression without OR operator."""
        # Setup: single AND expression, no OR token
        left_ast = self._create_ast_node("IDENTIFIER", "x")
        mock_parse_and.return_value = (left_ast, self.base_parser_state)
        
        parser_state = {
            "tokens": [self._create_token("IDENTIFIER", "x")],
            "pos": 0,
            "filename": "test.c",
            "error": None
        }
        
        # Execute
        result_ast, result_state = _parse_or(parser_state)
        
        # Verify
        self.assertEqual(result_ast, left_ast)
        mock_parse_and.assert_called_once()
        mock_consume_token.assert_not_called()

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_var_decl_package._parse_expression_package._parse_or_package._parse_or_src._parse_and')
    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_var_decl_package._parse_expression_package._parse_or_package._parse_or_src._consume_token')
    def test_parse_or_two_operands(self, mock_consume_token, mock_parse_and):
        """Test parsing OR expression with two operands (a || b)."""
        # Setup: a || b
        left_ast = self._create_ast_node("IDENTIFIER", "a", line=1, column=1)
        right_ast = self._create_ast_node("IDENTIFIER", "b", line=1, column=5)
        or_token = self._create_token("OR", "||", line=1, column=3)
        
        # First _parse_and returns left operand
        # Second _parse_and returns right operand
        mock_parse_and.side_effect = [
            (left_ast, {"tokens": [self._create_token("IDENTIFIER", "a"), or_token, self._create_token("IDENTIFIER", "b")], "pos": 1, "filename": "test.c", "error": None}),
            (right_ast, {"tokens": [self._create_token("IDENTIFIER", "a"), or_token, self._create_token("IDENTIFIER", "b")], "pos": 2, "filename": "test.c", "error": None})
        ]
        
        mock_consume_token.return_value = (or_token, {"tokens": [self._create_token("IDENTIFIER", "a"), or_token, self._create_token("IDENTIFIER", "b")], "pos": 2, "filename": "test.c", "error": None})
        
        parser_state = {
            "tokens": [
                self._create_token("IDENTIFIER", "a", line=1, column=1),
                or_token,
                self._create_token("IDENTIFIER", "b", line=1, column=5)
            ],
            "pos": 0,
            "filename": "test.c",
            "error": None
        }
        
        # Execute
        result_ast, result_state = _parse_or(parser_state)
        
        # Verify
        self.assertEqual(result_ast["type"], "BINARY_OP")
        self.assertEqual(result_ast["value"], "||")
        self.assertEqual(len(result_ast["children"]), 2)
        self.assertEqual(result_ast["line"], 1)
        self.assertEqual(result_ast["column"], 3)
        mock_consume_token.assert_called_once()

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_var_decl_package._parse_expression_package._parse_or_package._parse_or_src._parse_and')
    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_var_decl_package._parse_expression_package._parse_or_package._parse_or_src._consume_token')
    def test_parse_or_left_associative_chaining(self, mock_consume_token, mock_parse_and):
        """Test left-associative OR chaining (a || b || c)."""
        # Setup: a || b || c should parse as ((a || b) || c)
        ast_a = self._create_ast_node("IDENTIFIER", "a", line=1, column=1)
        ast_b = self._create_ast_node("IDENTIFIER", "b", line=1, column=5)
        ast_c = self._create_ast_node("IDENTIFIER", "c", line=1, column=9)
        
        or_token_1 = self._create_token("OR", "||", line=1, column=3)
        or_token_2 = self._create_token("OR", "||", line=1, column=7)
        
        tokens = [
            self._create_token("IDENTIFIER", "a", line=1, column=1),
            or_token_1,
            self._create_token("IDENTIFIER", "b", line=1, column=5),
            or_token_2,
            self._create_token("IDENTIFIER", "c", line=1, column=9)
        ]
        
        # _parse_and called 3 times: for a, b, and c
        mock_parse_and.side_effect = [
            (ast_a, {"tokens": tokens, "pos": 1, "filename": "test.c", "error": None}),
            (ast_b, {"tokens": tokens, "pos": 3, "filename": "test.c", "error": None}),
            (ast_c, {"tokens": tokens, "pos": 4, "filename": "test.c", "error": None})
        ]
        
        # _consume_token called 2 times: for each ||
        mock_consume_token.side_effect = [
            (or_token_1, {"tokens": tokens, "pos": 2, "filename": "test.c", "error": None}),
            (or_token_2, {"tokens": tokens, "pos": 4, "filename": "test.c", "error": None})
        ]
        
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c",
            "error": None
        }
        
        # Execute
        result_ast, result_state = _parse_or(parser_state)
        
        # Verify: should be left-associative ((a || b) || c)
        self.assertEqual(result_ast["type"], "BINARY_OP")
        self.assertEqual(result_ast["value"], "||")
        self.assertEqual(len(result_ast["children"]), 2)
        
        # Left child should be another BINARY_OP (a || b)
        left_child = result_ast["children"][0]
        self.assertEqual(left_child["type"], "BINARY_OP")
        self.assertEqual(left_child["value"], "||")
        
        # Right child should be c
        right_child = result_ast["children"][1]
        self.assertEqual(right_child["type"], "IDENTIFIER")
        self.assertEqual(right_child["value"], "c")
        
        # Verify _consume_token called twice
        self.assertEqual(mock_consume_token.call_count, 2)

    # ==================== Boundary Value Tests ====================

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_var_decl_package._parse_expression_package._parse_or_package._parse_or_src._parse_and')
    def test_parse_or_empty_tokens(self, mock_parse_and):
        """Test parsing with empty token list."""
        # Setup
        empty_ast = self._create_ast_node("EMPTY")
        mock_parse_and.return_value = (empty_ast, self.base_parser_state)
        
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.c",
            "error": None
        }
        
        # Execute
        result_ast, result_state = _parse_or(parser_state)
        
        # Verify
        self.assertEqual(result_ast, empty_ast)

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_var_decl_package._parse_expression_package._parse_or_package._parse_or_src._parse_and')
    def test_parse_or_position_at_end(self, mock_parse_and):
        """Test parsing when position is at end of tokens."""
        # Setup
        ast_node = self._create_ast_node("IDENTIFIER", "x")
        mock_parse_and.return_value = (ast_node, self.base_parser_state)
        
        parser_state = {
            "tokens": [self._create_token("IDENTIFIER", "x")],
            "pos": 1,  # Position at end
            "filename": "test.c",
            "error": None
        }
        
        # Execute
        result_ast, result_state = _parse_or(parser_state)
        
        # Verify
        self.assertEqual(result_ast, ast_node)

    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_var_decl_package._parse_expression_package._parse_or_package._parse_or_src._parse_and')
    def test_parse_or_missing_line_column_info(self, mock_parse_and):
        """Test parsing when tokens lack line/column information."""
        # Setup: tokens without line/column
        left_ast = self._create_ast_node("IDENTIFIER", "x")
        right_ast = self._create_ast_node("IDENTIFIER", "y")
        or_token = {"type": "OR", "value": "||"}  # No line/column
        
        mock_parse_and.side_effect = [
            (left_ast, {"tokens": [or_token, self._create_token("IDENTIFIER", "y")], "pos": 1, "filename": "test.c", "error": None}),
            (right_ast, {"tokens": [or_token, self._create_token("IDENTIFIER", "y")], "pos": 2, "filename": "test.c", "error": None})
        ]
        
        from unittest.mock import patch as inner_patch
        with inner_patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_var_decl_package._parse_expression_package._parse_or_package._parse_or_src._consume_token') as mock_consume:
            mock_consume.return_value = (or_token, {"tokens": [or_token, self._create_token("IDENTIFIER", "y")], "pos": 2, "filename": "test.c", "error": None})
            
            parser_state = {
                "tokens": [or_token, self._create_token("IDENTIFIER", "y")],
                "pos": 0,
                "filename": "test.c",
                "error": None
            }
            
            # Execute
            result_ast, result_state = _parse_or(parser_state)
            
            # Verify: should default to 0 for missing line/column
            self.assertEqual(result_ast["type"], "BINARY_OP")
            self.assertEqual(result_ast["line"], 0)
            self.assertEqual(result_ast["column"], 0)

    # ==================== Helper Function Tests ====================

    def test_is_current_token_or_true(self):
        """Test _is_current_token_or when current token is OR."""
        parser_state = {
            "tokens": [self._create_token("OR", "||")],
            "pos": 0,
            "filename": "test.c",
            "error": None
        }
        
        result = _is_current_token_or(parser_state)
        self.assertTrue(result)

    def test_is_current_token_or_false_different_type(self):
        """Test _is_current_token_or when current token is not OR."""
        parser_state = {
            "tokens": [self._create_token("AND", "&&")],
            "pos": 0,
            "filename": "test.c",
            "error": None
        }
        
        result = _is_current_token_or(parser_state)
        self.assertFalse(result)

    def test_is_current_token_or_false_position_out_of_bounds(self):
        """Test _is_current_token_or when position is out of bounds."""
        parser_state = {
            "tokens": [self._create_token("OR", "||")],
            "pos": 5,  # Beyond token list
            "filename": "test.c",
            "error": None
        }
        
        result = _is_current_token_or(parser_state)
        self.assertFalse(result)

    def test_is_current_token_or_false_empty_tokens(self):
        """Test _is_current_token_or with empty token list."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.c",
            "error": None
        }
        
        result = _is_current_token_or(parser_state)
        self.assertFalse(result)

    def test_is_current_token_or_missing_pos_defaults_to_zero(self):
        """Test _is_current_token_or when pos is missing."""
        parser_state = {
            "tokens": [self._create_token("OR", "||")],
            "filename": "test.c",
            "error": None
        }
        
        result = _is_current_token_or(parser_state)
        self.assertTrue(result)

    def test_is_current_token_or_missing_tokens_defaults_to_empty(self):
        """Test _is_current_token_or when tokens is missing."""
        parser_state = {
            "pos": 0,
            "filename": "test.c",
            "error": None
        }
        
        result = _is_current_token_or(parser_state)
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()

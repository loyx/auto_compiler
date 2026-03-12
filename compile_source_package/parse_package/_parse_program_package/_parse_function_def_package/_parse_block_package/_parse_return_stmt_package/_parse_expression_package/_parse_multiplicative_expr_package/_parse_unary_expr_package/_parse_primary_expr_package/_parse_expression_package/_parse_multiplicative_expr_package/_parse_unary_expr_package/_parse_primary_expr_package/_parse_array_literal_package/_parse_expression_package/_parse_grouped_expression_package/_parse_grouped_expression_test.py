# === std / third-party imports ===
import unittest
from unittest.mock import patch
from typing import Dict, Any

# === sub function imports ===
from ._parse_grouped_expression_src import _parse_grouped_expression


# === Test Helpers ===
def create_token(token_type: str, value: str = "", line: int = 1, column: int = 1) -> Dict[str, Any]:
    """Helper to create a token dictionary."""
    return {
        "type": token_type,
        "value": value,
        "line": line,
        "column": column
    }


def create_parser_state(tokens: list, pos: int = 0, filename: str = "<test>") -> Dict[str, Any]:
    """Helper to create a parser state dictionary."""
    return {
        "tokens": tokens,
        "pos": pos,
        "filename": filename,
        "error": ""
    }


# === Test Cases ===
class TestParseGroupedExpression(unittest.TestCase):
    """Test cases for _parse_grouped_expression function."""

    def test_happy_path_simple_grouped_expression(self):
        """Test parsing a simple grouped expression like (1)."""
        tokens = [
            create_token("LEFT_PAREN", "(", 1, 1),
            create_token("NUMBER", "1", 1, 2),
            create_token("RIGHT_PAREN", ")", 1, 3),
        ]
        parser_state = create_parser_state(tokens, pos=0)
        
        # Mock _parse_expression to return a simple AST
        mock_inner_ast = {
            "type": "NUMBER_LITERAL",
            "value": "1",
            "line": 1,
            "column": 2
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_expression_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_array_literal_package._parse_expression_package._parse_grouped_expression_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.side_effect = lambda state: mock_inner_ast
            
            result = _parse_grouped_expression(parser_state)
            
            # Verify result structure
            self.assertEqual(result["type"], "GROUPED_EXPRESSION")
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(result["children"][0], mock_inner_ast)
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            
            # Verify parser state was updated
            self.assertEqual(parser_state["pos"], 3)  # Should have consumed all 3 tokens
            
            # Verify _parse_expression was called
            mock_parse_expr.assert_called_once()

    def test_happy_path_nested_grouped_expression(self):
        """Test parsing nested grouped expressions like ((1))."""
        tokens = [
            create_token("LEFT_PAREN", "(", 1, 1),
            create_token("LEFT_PAREN", "(", 1, 2),
            create_token("NUMBER", "1", 1, 3),
            create_token("RIGHT_PAREN", ")", 1, 4),
            create_token("RIGHT_PAREN", ")", 1, 5),
        ]
        parser_state = create_parser_state(tokens, pos=0)
        
        # Mock _parse_expression to return another GROUPED_EXPRESSION
        mock_inner_ast = {
            "type": "GROUPED_EXPRESSION",
            "children": [{"type": "NUMBER_LITERAL", "value": "1", "line": 1, "column": 3}],
            "line": 1,
            "column": 2
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_expression_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_array_literal_package._parse_expression_package._parse_grouped_expression_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.side_effect = lambda state: mock_inner_ast
            
            result = _parse_grouped_expression(parser_state)
            
            self.assertEqual(result["type"], "GROUPED_EXPRESSION")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            self.assertEqual(parser_state["pos"], 5)

    def test_happy_path_expression_with_operator(self):
        """Test parsing grouped expression with operator like (1 + 2)."""
        tokens = [
            create_token("LEFT_PAREN", "(", 1, 1),
            create_token("NUMBER", "1", 1, 2),
            create_token("PLUS", "+", 1, 4),
            create_token("NUMBER", "2", 1, 5),
            create_token("RIGHT_PAREN", ")", 1, 6),
        ]
        parser_state = create_parser_state(tokens, pos=0)
        
        mock_inner_ast = {
            "type": "BINARY_EXPRESSION",
            "children": [
                {"type": "NUMBER_LITERAL", "value": "1", "line": 1, "column": 2},
                {"type": "NUMBER_LITERAL", "value": "2", "line": 1, "column": 5}
            ],
            "value": "+",
            "line": 1,
            "column": 2
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_expression_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_array_literal_package._parse_expression_package._parse_grouped_expression_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.side_effect = lambda state: mock_inner_ast
            
            result = _parse_grouped_expression(parser_state)
            
            self.assertEqual(result["type"], "GROUPED_EXPRESSION")
            self.assertEqual(result["children"][0], mock_inner_ast)
            self.assertEqual(parser_state["pos"], 5)

    def test_error_empty_parentheses(self):
        """Test that empty parentheses raise SyntaxError."""
        tokens = [
            create_token("LEFT_PAREN", "(", 1, 1),
            create_token("RIGHT_PAREN", ")", 1, 2),
        ]
        parser_state = create_parser_state(tokens, pos=0)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_grouped_expression(parser_state)
        
        self.assertIn("Empty parentheses", str(context.exception))

    def test_error_missing_right_paren(self):
        """Test that missing right parenthesis raises SyntaxError."""
        tokens = [
            create_token("LEFT_PAREN", "(", 1, 1),
            create_token("NUMBER", "1", 1, 2),
        ]
        parser_state = create_parser_state(tokens, pos=0)
        
        mock_inner_ast = {
            "type": "NUMBER_LITERAL",
            "value": "1",
            "line": 1,
            "column": 2
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_expression_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_array_literal_package._parse_expression_package._parse_grouped_expression_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.side_effect = lambda state: mock_inner_ast
            
            with self.assertRaises(SyntaxError) as context:
                _parse_grouped_expression(parser_state)
            
            self.assertIn("Expected ')'", str(context.exception))
            self.assertIn("end of input", str(context.exception))

    def test_error_wrong_token_instead_of_right_paren(self):
        """Test that wrong token instead of right paren raises SyntaxError."""
        tokens = [
            create_token("LEFT_PAREN", "(", 1, 1),
            create_token("NUMBER", "1", 1, 2),
            create_token("PLUS", "+", 1, 3),
        ]
        parser_state = create_parser_state(tokens, pos=0)
        
        mock_inner_ast = {
            "type": "NUMBER_LITERAL",
            "value": "1",
            "line": 1,
            "column": 2
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_expression_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_array_literal_package._parse_expression_package._parse_grouped_expression_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.side_effect = lambda state: mock_inner_ast
            
            with self.assertRaises(SyntaxError) as context:
                _parse_grouped_expression(parser_state)
            
            self.assertIn("Expected ')'", str(context.exception))
            self.assertIn("PLUS", str(context.exception))

    def test_error_end_of_input_at_start(self):
        """Test that end of input at start raises SyntaxError."""
        tokens = [
            create_token("LEFT_PAREN", "(", 1, 1),
        ]
        parser_state = create_parser_state(tokens, pos=0)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_grouped_expression(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))

    def test_error_end_of_input_during_inner_expression(self):
        """Test that end of input during inner expression parsing raises SyntaxError."""
        tokens = [
            create_token("LEFT_PAREN", "(", 1, 1),
            create_token("NUMBER", "1", 1, 2),
        ]
        parser_state = create_parser_state(tokens, pos=0)
        
        # Mock _parse_expression to consume the NUMBER but not advance past end
        def mock_parse_impl(state):
            state["pos"] = len(state["tokens"])  # Simulate consuming all remaining tokens
            return {
                "type": "NUMBER_LITERAL",
                "value": "1",
                "line": 1,
                "column": 2
            }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_expression_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_array_literal_package._parse_expression_package._parse_grouped_expression_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.side_effect = mock_parse_impl
            
            with self.assertRaises(SyntaxError) as context:
                _parse_grouped_expression(parser_state)
            
            self.assertIn("Expected ')'", str(context.exception))

    def test_position_not_at_left_paren(self):
        """Test behavior when pos doesn't point to LEFT_PAREN (edge case)."""
        tokens = [
            create_token("NUMBER", "1", 1, 1),
            create_token("LEFT_PAREN", "(", 1, 2),
            create_token("NUMBER", "2", 1, 3),
            create_token("RIGHT_PAREN", ")", 1, 4),
        ]
        parser_state = create_parser_state(tokens, pos=1)  # Start at LEFT_PAREN
        
        mock_inner_ast = {
            "type": "NUMBER_LITERAL",
            "value": "2",
            "line": 1,
            "column": 3
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_expression_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_array_literal_package._parse_expression_package._parse_grouped_expression_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.side_effect = lambda state: mock_inner_ast
            
            result = _parse_grouped_expression(parser_state)
            
            self.assertEqual(result["type"], "GROUPED_EXPRESSION")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 2)  # Column from LEFT_PAREN
            self.assertEqual(parser_state["pos"], 4)

    def test_preserves_filename_in_state(self):
        """Test that filename in parser_state is preserved."""
        tokens = [
            create_token("LEFT_PAREN", "(", 1, 1),
            create_token("NUMBER", "1", 1, 2),
            create_token("RIGHT_PAREN", ")", 1, 3),
        ]
        parser_state = create_parser_state(tokens, pos=0, filename="test_file.cc")
        
        mock_inner_ast = {
            "type": "NUMBER_LITERAL",
            "value": "1",
            "line": 1,
            "column": 2
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_expression_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_primary_expr_package._parse_array_literal_package._parse_expression_package._parse_grouped_expression_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.side_effect = lambda state: mock_inner_ast
            
            _parse_grouped_expression(parser_state)
            
            self.assertEqual(parser_state["filename"], "test_file.cc")


# === Test Runner ===
if __name__ == "__main__":
    unittest.main()

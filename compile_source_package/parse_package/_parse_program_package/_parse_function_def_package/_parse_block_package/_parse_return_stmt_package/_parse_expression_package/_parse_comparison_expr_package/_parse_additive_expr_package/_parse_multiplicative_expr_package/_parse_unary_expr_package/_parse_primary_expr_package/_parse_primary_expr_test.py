# === imports ===
import unittest
from unittest.mock import patch
from typing import Dict, Any

# === relative import for UUT ===
from ._parse_primary_expr_src import _parse_primary_expr


# === test helpers ===
def _create_token(ttype: str, value: str, line: int, column: int) -> Dict[str, Any]:
    """Helper to create a token dict."""
    return {"type": ttype, "value": value, "line": line, "column": column}


def _create_parser_state(tokens: list, pos: int = 0, filename: str = "test.src") -> Dict[str, Any]:
    """Helper to create a parser_state dict."""
    return {"tokens": tokens, "pos": pos, "filename": filename}


# === test cases ===
class TestParsePrimaryExpr(unittest.TestCase):
    """Test cases for _parse_primary_expr function."""
    
    def test_empty_tokens(self):
        """Test parsing with empty token list."""
        parser_state = _create_parser_state([])
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], "Unexpected end of file")
        self.assertEqual(result["line"], 0)
        self.assertEqual(result["column"], 0)
        self.assertEqual(parser_state["pos"], 0)
        self.assertEqual(parser_state["error"], "Unexpected end of file")
    
    def test_position_beyond_tokens(self):
        """Test parsing when position is beyond token list length."""
        parser_state = _create_parser_state(
            [_create_token("IDENTIFIER", "x", 1, 1)],
            pos=5
        )
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], "Unexpected end of file")
        self.assertEqual(parser_state["pos"], 5)
    
    def test_identifier_token(self):
        """Test IDENTIFIER token parsing."""
        parser_state = _create_parser_state([
            _create_token("IDENTIFIER", "x", 1, 1)
        ])
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "x")
        self.assertEqual(result["children"], [])
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 1)
        self.assertNotIn("error", parser_state)
    
    def test_number_literal(self):
        """Test NUMBER token parsing."""
        parser_state = _create_parser_state([
            _create_token("NUMBER", "42", 2, 5)
        ])
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "42")
        self.assertEqual(result["children"], [])
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 5)
        self.assertEqual(parser_state["pos"], 1)
    
    def test_string_literal_double_quotes(self):
        """Test STRING token parsing with double quotes."""
        parser_state = _create_parser_state([
            _create_token("STRING", '"hello"', 1, 1)
        ])
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "hello")
        self.assertEqual(result["children"], [])
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 1)
    
    def test_string_literal_single_quotes(self):
        """Test STRING token parsing with single quotes."""
        parser_state = _create_parser_state([
            _create_token("STRING", "'world'", 3, 10)
        ])
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "world")
        self.assertEqual(result["children"], [])
        self.assertEqual(result["line"], 3)
        self.assertEqual(result["column"], 10)
        self.assertEqual(parser_state["pos"], 1)
    
    def test_string_literal_mismatched_quotes(self):
        """Test STRING token with mismatched quotes (not stripped)."""
        parser_state = _create_parser_state([
            _create_token("STRING", '"mismatched\'', 1, 1)
        ])
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], '"mismatched\'')
        self.assertEqual(result["children"], [])
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 1)
    
    def test_true_literal(self):
        """Test TRUE token parsing."""
        parser_state = _create_parser_state([
            _create_token("TRUE", "true", 1, 1)
        ])
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertIs(result["value"], True)
        self.assertEqual(result["children"], [])
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 1)
    
    def test_false_literal(self):
        """Test FALSE token parsing."""
        parser_state = _create_parser_state([
            _create_token("FALSE", "false", 5, 20)
        ])
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertIs(result["value"], False)
        self.assertEqual(result["children"], [])
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 20)
        self.assertEqual(parser_state["pos"], 1)
    
    def test_null_literal(self):
        """Test NULL token parsing."""
        parser_state = _create_parser_state([
            _create_token("NULL", "null", 10, 3)
        ])
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertIsNone(result["value"])
        self.assertEqual(result["children"], [])
        self.assertEqual(result["line"], 10)
        self.assertEqual(result["column"], 3)
        self.assertEqual(parser_state["pos"], 1)
    
    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_comparison_expr_package._parse_additive_expr_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_unary_expr_src._parse_unary_expr')
    def test_paren_expr_success(self, mock_parse_unary):
        """Test LPAREN token with successful paren expression parsing."""
        inner_ast = {"type": "LITERAL", "value": "5", "children": [], "line": 1, "column": 2}
        mock_parse_unary.return_value = inner_ast
        
        parser_state = _create_parser_state([
            _create_token("LPAREN", "(", 1, 1),
            _create_token("NUMBER", "5", 1, 2),
            _create_token("RPAREN", ")", 1, 3)
        ])
        
        result = _parse_primary_expr(parser_state)
        
        mock_parse_unary.assert_called_once()
        self.assertEqual(result, inner_ast)
        self.assertEqual(parser_state["pos"], 3)
        self.assertNotIn("error", parser_state)
    
    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_comparison_expr_package._parse_additive_expr_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_unary_expr_src._parse_unary_expr')
    def test_paren_expr_missing_rparen_eof(self, mock_parse_unary):
        """Test LPAREN token with missing RPAREN (EOF)."""
        inner_ast = {"type": "LITERAL", "value": "5", "children": [], "line": 1, "column": 2}
        mock_parse_unary.return_value = inner_ast
        
        parser_state = _create_parser_state([
            _create_token("LPAREN", "(", 1, 1),
            _create_token("NUMBER", "5", 1, 2)
        ])
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertIn("Expected ')'", result["value"])
        self.assertIn("end of file", result["value"])
        self.assertEqual(result["line"], 0)
        self.assertEqual(result["column"], 0)
        self.assertEqual(parser_state["pos"], 2)
        self.assertIn("error", parser_state)
    
    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_comparison_expr_package._parse_additive_expr_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_unary_expr_src._parse_unary_expr')
    def test_paren_expr_missing_rparen_wrong_token(self, mock_parse_unary):
        """Test LPAREN token with missing RPAREN (wrong token type)."""
        inner_ast = {"type": "LITERAL", "value": "5", "children": [], "line": 1, "column": 2}
        mock_parse_unary.return_value = inner_ast
        
        parser_state = _create_parser_state([
            _create_token("LPAREN", "(", 1, 1),
            _create_token("NUMBER", "5", 1, 2),
            _create_token("PLUS", "+", 1, 3)
        ])
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertIn("Expected ')'", result["value"])
        self.assertIn("PLUS", result["value"])
        self.assertEqual(parser_state["pos"], 2)
    
    @patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_comparison_expr_package._parse_additive_expr_package._parse_multiplicative_expr_package._parse_unary_expr_package._parse_unary_expr_src._parse_unary_expr')
    def test_paren_expr_unary_error_propagation(self, mock_parse_unary):
        """Test LPAREN token when unary expression parsing fails."""
        error_ast = {"type": "ERROR", "value": "Some error", "children": [], "line": 0, "column": 0}
        mock_parse_unary.return_value = error_ast
        
        parser_state = _create_parser_state([
            _create_token("LPAREN", "(", 1, 1)
        ])
        parser_state["error"] = "Some error"
        
        result = _parse_primary_expr(parser_state)
        
        mock_parse_unary.assert_called_once()
        self.assertEqual(result, error_ast)
        self.assertEqual(parser_state["error"], "Some error")
    
    def test_unknown_token_type(self):
        """Test unknown token type."""
        parser_state = _create_parser_state([
            _create_token("UNKNOWN", "?", 7, 15)
        ])
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertIn("Unexpected token 'UNKNOWN'", result["value"])
        self.assertIn("line 7", result["value"])
        self.assertEqual(result["line"], 0)
        self.assertEqual(result["column"], 0)
        self.assertEqual(parser_state["pos"], 0)
        self.assertIn("error", parser_state)
    
    def test_operator_token(self):
        """Test operator token (should return ERROR)."""
        parser_state = _create_parser_state([
            _create_token("PLUS", "+", 4, 8)
        ])
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertIn("Unexpected token 'PLUS'", result["value"])
        self.assertEqual(parser_state["pos"], 0)
    
    def test_multiple_tokens_only_first_consumed(self):
        """Test that only the first token is consumed."""
        parser_state = _create_parser_state([
            _create_token("IDENTIFIER", "x", 1, 1),
            _create_token("PLUS", "+", 1, 2),
            _create_token("NUMBER", "5", 1, 3)
        ])
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "x")
        self.assertEqual(parser_state["pos"], 1)
    
    def test_position_not_at_start(self):
        """Test parsing when position is not at start of tokens."""
        parser_state = _create_parser_state([
            _create_token("PLUS", "+", 1, 1),
            _create_token("IDENTIFIER", "y", 1, 2),
            _create_token("NUMBER", "10", 1, 3)
        ], pos=1)
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "y")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 2)
        self.assertEqual(parser_state["pos"], 2)
    
    def test_float_number_literal(self):
        """Test NUMBER token with float value."""
        parser_state = _create_parser_state([
            _create_token("NUMBER", "3.14", 1, 1)
        ])
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "3.14")
        self.assertEqual(parser_state["pos"], 1)
    
    def test_negative_number_literal(self):
        """Test NUMBER token with negative value."""
        parser_state = _create_parser_state([
            _create_token("NUMBER", "-42", 2, 5)
        ])
        
        result = _parse_primary_expr(parser_state)
        
        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "-42")
        self.assertEqual(parser_state["pos"], 1)


# === test runner ===
if __name__ == "__main__":
    unittest.main()

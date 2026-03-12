# === imports ===
import unittest
from unittest.mock import patch

# === relative imports ===
from ._parse_return_stmt_src import _parse_return_stmt


# === test class ===
class TestParseReturnStmt(unittest.TestCase):
    """Test cases for _parse_return_stmt function."""

    def test_bare_return_statement(self):
        """Test parsing bare return statement (return;)."""
        tokens = [
            {"type": "RETURN", "value": "return", "line": 5, "column": 10},
            {"type": "SEMICOLON", "value": ";", "line": 5, "column": 16},
            {"type": "EOF", "value": "", "line": 5, "column": 17},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }
        
        result = _parse_return_stmt(parser_state)
        
        self.assertEqual(result["type"], "RETURN")
        self.assertIsNone(result["value"])
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 10)
        self.assertEqual(parser_state["pos"], 2)

    def test_return_with_expression(self):
        """Test parsing return statement with expression (return expr;)."""
        tokens = [
            {"type": "RETURN", "value": "return", "line": 3, "column": 5},
            {"type": "IDENTIFIER", "value": "x", "line": 3, "column": 12},
            {"type": "SEMICOLON", "value": ";", "line": 3, "column": 13},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }
        
        mock_expr_ast = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 3,
            "column": 12
        }
        
        def mock_parse_expression(state):
            state["pos"] = 2
            return mock_expr_ast
        
        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_for_stmt_package._parse_block_package._parse_return_stmt_package._parse_return_stmt_src._parse_expression', side_effect=mock_parse_expression):
            result = _parse_return_stmt(parser_state)
        
        self.assertEqual(result["type"], "RETURN")
        self.assertEqual(result["value"], mock_expr_ast)
        self.assertEqual(result["line"], 3)
        self.assertEqual(result["column"], 5)
        self.assertEqual(parser_state["pos"], 3)

    def test_missing_semicolon_after_return(self):
        """Test SyntaxError when semicolon is missing after return."""
        tokens = [
            {"type": "RETURN", "value": "return", "line": 7, "column": 1},
            {"type": "IDENTIFIER", "value": "x", "line": 7, "column": 8},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "error.c"
        }
        
        def mock_parse_expression(state):
            state["pos"] = 1
            return {"type": "IDENTIFIER", "value": "x", "line": 7, "column": 8}
        
        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_for_stmt_package._parse_block_package._parse_return_stmt_package._parse_return_stmt_src._parse_expression', side_effect=mock_parse_expression):
            with self.assertRaises(SyntaxError) as context:
                _parse_return_stmt(parser_state)
        
        self.assertIn("error.c:7:1", str(context.exception))
        self.assertIn("Expected ';' after return expression", str(context.exception))

    def test_missing_token_after_return(self):
        """Test SyntaxError when no token exists after return."""
        tokens = [
            {"type": "RETURN", "value": "return", "line": 10, "column": 3},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "error.c"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_return_stmt(parser_state)
        
        self.assertIn("error.c:10:3", str(context.exception))
        self.assertIn("Expected ';' or expression after 'return'", str(context.exception))

    def test_return_with_complex_expression(self):
        """Test parsing return with complex expression (return a + b;)."""
        tokens = [
            {"type": "RETURN", "value": "return", "line": 15, "column": 2},
            {"type": "IDENTIFIER", "value": "a", "line": 15, "column": 9},
            {"type": "OPERATOR", "value": "+", "line": 15, "column": 11},
            {"type": "IDENTIFIER", "value": "b", "line": 15, "column": 13},
            {"type": "SEMICOLON", "value": ";", "line": 15, "column": 14},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }
        
        mock_expr_ast = {
            "type": "BINARY_OP",
            "children": [
                {"type": "IDENTIFIER", "value": "a", "line": 15, "column": 9},
                {"type": "IDENTIFIER", "value": "b", "line": 15, "column": 13}
            ],
            "value": "+",
            "line": 15,
            "column": 9
        }
        
        def mock_parse_expression(state):
            state["pos"] = 4
            return mock_expr_ast
        
        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_for_stmt_package._parse_block_package._parse_return_stmt_package._parse_return_stmt_src._parse_expression', side_effect=mock_parse_expression):
            result = _parse_return_stmt(parser_state)
        
        self.assertEqual(result["type"], "RETURN")
        self.assertEqual(result["value"], mock_expr_ast)
        self.assertEqual(result["line"], 15)
        self.assertEqual(result["column"], 2)
        self.assertEqual(parser_state["pos"], 5)

    def test_return_without_filename(self):
        """Test parsing return when filename is not provided in parser_state."""
        tokens = [
            {"type": "RETURN", "value": "return", "line": 1, "column": 1},
            {"type": "SEMICOLON", "value": ";", "line": 1, "column": 7},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0
        }
        
        result = _parse_return_stmt(parser_state)
        
        self.assertEqual(result["type"], "RETURN")
        self.assertIsNone(result["value"])
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 2)

    def test_return_with_number_literal(self):
        """Test parsing return with number literal (return 42;)."""
        tokens = [
            {"type": "RETURN", "value": "return", "line": 20, "column": 5},
            {"type": "NUMBER", "value": "42", "line": 20, "column": 12},
            {"type": "SEMICOLON", "value": ";", "line": 20, "column": 14},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }
        
        mock_expr_ast = {
            "type": "NUMBER",
            "value": "42",
            "line": 20,
            "column": 12
        }
        
        def mock_parse_expression(state):
            state["pos"] = 2
            return mock_expr_ast
        
        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_for_stmt_package._parse_block_package._parse_return_stmt_package._parse_return_stmt_src._parse_expression', side_effect=mock_parse_expression):
            result = _parse_return_stmt(parser_state)
        
        self.assertEqual(result["type"], "RETURN")
        self.assertEqual(result["value"], mock_expr_ast)
        self.assertEqual(result["line"], 20)
        self.assertEqual(result["column"], 5)
        self.assertEqual(parser_state["pos"], 3)

    def test_return_with_function_call(self):
        """Test parsing return with function call (return foo();)."""
        tokens = [
            {"type": "RETURN", "value": "return", "line": 25, "column": 1},
            {"type": "IDENTIFIER", "value": "foo", "line": 25, "column": 8},
            {"type": "LPAREN", "value": "(", "line": 25, "column": 11},
            {"type": "RPAREN", "value": ")", "line": 25, "column": 12},
            {"type": "SEMICOLON", "value": ";", "line": 25, "column": 13},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.c"
        }
        
        mock_expr_ast = {
            "type": "CALL",
            "value": "foo",
            "children": [],
            "line": 25,
            "column": 8
        }
        
        def mock_parse_expression(state):
            state["pos"] = 4
            return mock_expr_ast
        
        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_for_stmt_package._parse_block_package._parse_return_stmt_package._parse_return_stmt_src._parse_expression', side_effect=mock_parse_expression):
            result = _parse_return_stmt(parser_state)
        
        self.assertEqual(result["type"], "RETURN")
        self.assertEqual(result["value"], mock_expr_ast)
        self.assertEqual(result["line"], 25)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 5)

    def test_wrong_token_after_expression(self):
        """Test SyntaxError when wrong token follows expression."""
        tokens = [
            {"type": "RETURN", "value": "return", "line": 30, "column": 1},
            {"type": "IDENTIFIER", "value": "x", "line": 30, "column": 8},
            {"type": "COMMA", "value": ",", "line": 30, "column": 9},
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "error.c"
        }
        
        def mock_parse_expression(state):
            state["pos"] = 1
            return {"type": "IDENTIFIER", "value": "x", "line": 30, "column": 8}
        
        with patch('main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_for_stmt_package._parse_block_package._parse_return_stmt_package._parse_return_stmt_src._parse_expression', side_effect=mock_parse_expression):
            with self.assertRaises(SyntaxError) as context:
                _parse_return_stmt(parser_state)
        
        self.assertIn("error.c:30:1", str(context.exception))
        self.assertIn("Expected ';' after return expression", str(context.exception))


# === main entry point ===
if __name__ == "__main__":
    unittest.main()

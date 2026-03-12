import unittest
from unittest.mock import patch

# Relative import for the function under test
from ._parse_expr_stmt_src import _parse_expr_stmt


class TestParseExprStmt(unittest.TestCase):
    """Test cases for _parse_expr_stmt function."""

    def test_happy_path_simple_literal_expression(self):
        """Test parsing a simple literal expression statement."""
        mock_expression_ast = {
            "type": "LITERAL",
            "value": 42,
            "line": 1,
            "column": 5
        }

        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "42", "line": 1, "column": 5}
            ],
            "filename": "test.py",
            "pos": 0
        }

        with patch('._parse_expression_package._parse_expression_src._parse_expression') as mock_parse_expr:
            mock_parse_expr.return_value = mock_expression_ast

            result = _parse_expr_stmt(parser_state)

            self.assertEqual(result["type"], "EXPR_STMT")
            self.assertEqual(result["expression"], mock_expression_ast)
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 5)
            mock_parse_expr.assert_called_once_with(parser_state)

    def test_happy_path_identifier_expression(self):
        """Test parsing an identifier expression statement."""
        mock_expression_ast = {
            "type": "IDENTIFIER",
            "name": "x",
            "line": 2,
            "column": 10
        }

        parser_state = {
            "tokens": [
                {"type": "IDENT", "value": "x", "line": 2, "column": 10}
            ],
            "filename": "test.py",
            "pos": 0
        }

        with patch('._parse_expression_package._parse_expression_src._parse_expression') as mock_parse_expr:
            mock_parse_expr.return_value = mock_expression_ast

            result = _parse_expr_stmt(parser_state)

            self.assertEqual(result["type"], "EXPR_STMT")
            self.assertEqual(result["expression"]["type"], "IDENTIFIER")
            self.assertEqual(result["line"], 2)
            self.assertEqual(result["column"], 10)

    def test_happy_path_binary_operation_expression(self):
        """Test parsing a binary operation expression statement."""
        mock_expression_ast = {
            "type": "BINARY_OP",
            "operator": "+",
            "left": {"type": "LITERAL", "value": 1},
            "right": {"type": "LITERAL", "value": 2},
            "line": 1,
            "column": 0
        }

        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 0},
                {"type": "PLUS", "value": "+", "line": 1, "column": 2},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 4}
            ],
            "filename": "test.py",
            "pos": 0
        }

        with patch('._parse_expression_package._parse_expression_src._parse_expression') as mock_parse_expr:
            mock_parse_expr.return_value = mock_expression_ast

            result = _parse_expr_stmt(parser_state)

            self.assertEqual(result["type"], "EXPR_STMT")
            self.assertEqual(result["expression"]["type"], "BINARY_OP")
            self.assertEqual(result["expression"]["operator"], "+")

    def test_happy_path_function_call_expression(self):
        """Test parsing a function call expression statement."""
        mock_expression_ast = {
            "type": "CALL",
            "callee": {"type": "IDENTIFIER", "name": "foo"},
            "arguments": [],
            "line": 3,
            "column": 0
        }

        parser_state = {
            "tokens": [
                {"type": "IDENT", "value": "foo", "line": 3, "column": 0},
                {"type": "LPAREN", "value": "(", "line": 3, "column": 3},
                {"type": "RPAREN", "value": ")", "line": 3, "column": 4}
            ],
            "filename": "test.py",
            "pos": 0
        }

        with patch('._parse_expression_package._parse_expression_src._parse_expression') as mock_parse_expr:
            mock_parse_expr.return_value = mock_expression_ast

            result = _parse_expr_stmt(parser_state)

            self.assertEqual(result["type"], "EXPR_STMT")
            self.assertEqual(result["expression"]["type"], "CALL")

    def test_happy_path_position_updated_by_expression_parser(self):
        """Test that parser_state position is updated by _parse_expression."""
        mock_expression_ast = {
            "type": "LITERAL",
            "value": 100,
            "line": 1,
            "column": 0
        }

        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "100", "line": 1, "column": 0},
                {"type": "SEMICOLON", "value": ";", "line": 1, "column": 4},
                {"type": "NUMBER", "value": "200", "line": 1, "column": 6}
            ],
            "filename": "test.py",
            "pos": 0
        }

        def update_pos(state):
            state["pos"] = 2
            return mock_expression_ast

        with patch('._parse_expression_package._parse_expression_src._parse_expression') as mock_parse_expr:
            mock_parse_expr.side_effect = update_pos

            result = _parse_expr_stmt(parser_state)

            self.assertEqual(parser_state["pos"], 2)
            self.assertEqual(result["type"], "EXPR_STMT")

    def test_edge_case_empty_tokens_raises_syntax_error(self):
        """Test that empty token list raises SyntaxError."""
        parser_state = {
            "tokens": [],
            "filename": "test.py",
            "pos": 0
        }

        with self.assertRaises(SyntaxError) as context:
            _parse_expr_stmt(parser_state)

        self.assertIn("Unexpected end of input", str(context.exception))
        self.assertIn("expected expression", str(context.exception))

    def test_edge_case_pos_at_end_raises_syntax_error(self):
        """Test that pos at end of tokens raises SyntaxError."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "42", "line": 1, "column": 0}
            ],
            "filename": "test.py",
            "pos": 1
        }

        with self.assertRaises(SyntaxError) as context:
            _parse_expr_stmt(parser_state)

        self.assertIn("Unexpected end of input", str(context.exception))

    def test_edge_case_pos_beyond_tokens_raises_syntax_error(self):
        """Test that pos beyond tokens raises SyntaxError."""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "42", "line": 1, "column": 0}
            ],
            "filename": "test.py",
            "pos": 5
        }

        with self.assertRaises(SyntaxError) as context:
            _parse_expr_stmt(parser_state)

        self.assertIn("Unexpected end of input", str(context.exception))

    def test_edge_case_missing_line_column_defaults_to_zero(self):
        """Test that missing line/column in token defaults to 0."""
        mock_expression_ast = {
            "type": "LITERAL",
            "value": 42
        }

        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "42"}
            ],
            "filename": "test.py",
            "pos": 0
        }

        with patch('._parse_expression_package._parse_expression_src._parse_expression') as mock_parse_expr:
            mock_parse_expr.return_value = mock_expression_ast

            result = _parse_expr_stmt(parser_state)

            self.assertEqual(result["line"], 0)
            self.assertEqual(result["column"], 0)

    def test_edge_case_empty_filename_in_error_message(self):
        """Test error message with empty filename."""
        parser_state = {
            "tokens": [],
            "filename": "",
            "pos": 0
        }

        with self.assertRaises(SyntaxError) as context:
            _parse_expr_stmt(parser_state)

        self.assertIn(":0:0: Unexpected end of input", str(context.exception))

    def test_ast_node_structure_complete(self):
        """Test that AST node has all required fields."""
        mock_expression_ast = {
            "type": "LITERAL",
            "value": 42,
            "line": 1,
            "column": 5
        }

        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "42", "line": 1, "column": 5}
            ],
            "filename": "test.py",
            "pos": 0
        }

        with patch('._parse_expression_package._parse_expression_src._parse_expression') as mock_parse_expr:
            mock_parse_expr.return_value = mock_expression_ast

            result = _parse_expr_stmt(parser_state)

            self.assertIn("type", result)
            self.assertIn("expression", result)
            self.assertIn("line", result)
            self.assertIn("column", result)
            self.assertEqual(result["type"], "EXPR_STMT")

    def test_dependency_parse_expression_called_with_correct_state(self):
        """Test that _parse_expression is called with the parser_state."""
        mock_expression_ast = {
            "type": "LITERAL",
            "value": 42,
            "line": 1,
            "column": 0
        }

        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "42", "line": 1, "column": 0}
            ],
            "filename": "test.py",
            "pos": 0
        }

        with patch('._parse_expression_package._parse_expression_src._parse_expression') as mock_parse_expr:
            mock_parse_expr.return_value = mock_expression_ast

            _parse_expr_stmt(parser_state)

            mock_parse_expr.assert_called_once()
            call_args = mock_parse_expr.call_args
            self.assertIs(call_args[0][0], parser_state)

    def test_dependency_parse_expression_called_once(self):
        """Test that _parse_expression is called exactly once."""
        mock_expression_ast = {
            "type": "LITERAL",
            "value": 42,
            "line": 1,
            "column": 0
        }

        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "42", "line": 1, "column": 0}
            ],
            "filename": "test.py",
            "pos": 0
        }

        with patch('._parse_expression_package._parse_expression_src._parse_expression') as mock_parse_expr:
            mock_parse_expr.return_value = mock_expression_ast

            _parse_expr_stmt(parser_state)

            self.assertEqual(mock_parse_expr.call_count, 1)

    def test_exception_propagation_from_parse_expression(self):
        """Test that SyntaxError from _parse_expression propagates."""
        parser_state = {
            "tokens": [
                {"type": "INVALID", "value": "?", "line": 1, "column": 0}
            ],
            "filename": "test.py",
            "pos": 0
        }

        with patch('._parse_expression_package._parse_expression_src._parse_expression') as mock_parse_expr:
            mock_parse_expr.side_effect = SyntaxError("test.py:1:0: Invalid expression")

            with self.assertRaises(SyntaxError) as context:
                _parse_expr_stmt(parser_state)

            self.assertIn("Invalid expression", str(context.exception))
            mock_parse_expr.assert_called_once()

    def test_boundary_single_token_expression(self):
        """Test parsing expression with single token."""
        mock_expression_ast = {
            "type": "IDENTIFIER",
            "name": "x",
            "line": 1,
            "column": 0
        }

        parser_state = {
            "tokens": [
                {"type": "IDENT", "value": "x", "line": 1, "column": 0}
            ],
            "filename": "test.py",
            "pos": 0
        }

        with patch('._parse_expression_package._parse_expression_src._parse_expression') as mock_parse_expr:
            mock_parse_expr.return_value = mock_expression_ast

            result = _parse_expr_stmt(parser_state)

            self.assertEqual(result["type"], "EXPR_STMT")
            self.assertEqual(result["expression"]["type"], "IDENTIFIER")

    def test_boundary_expression_at_last_token_position(self):
        """Test parsing expression when pos points to last token."""
        mock_expression_ast = {
            "type": "LITERAL",
            "value": 999,
            "line": 5,
            "column": 20
        }

        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 0},
                {"type": "NUMBER", "value": "2", "line": 2, "column": 0},
                {"type": "NUMBER", "value": "999", "line": 5, "column": 20}
            ],
            "filename": "test.py",
            "pos": 2
        }

        with patch('._parse_expression_package._parse_expression_src._parse_expression') as mock_parse_expr:
            mock_parse_expr.return_value = mock_expression_ast

            result = _parse_expr_stmt(parser_state)

            self.assertEqual(result["line"], 5)
            self.assertEqual(result["column"], 20)
            self.assertEqual(result["expression"]["value"], 999)


if __name__ == "__main__":
    unittest.main()

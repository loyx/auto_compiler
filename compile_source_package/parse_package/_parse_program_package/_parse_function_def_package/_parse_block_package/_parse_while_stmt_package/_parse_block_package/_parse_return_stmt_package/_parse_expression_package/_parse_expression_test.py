import unittest
from unittest.mock import patch, MagicMock

# Mock the dependency before importing _parse_expression
import sys
from unittest.mock import MagicMock

# Create a mock for the entire dependency chain
mock_parse_or_expression = MagicMock()

# Patch the module before importing
sys.modules['main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_or_expression_package._parse_or_expression_src'] = MagicMock()
sys.modules['main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_or_expression_package._parse_comparison_package._parse_comparison_src'] = MagicMock()
sys.modules['main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_or_expression_package._parse_comparison_package._parse_additive_package._parse_additive_src'] = MagicMock()

# Relative import from the same package
from ._parse_expression_src import _parse_expression


class TestParseExpression(unittest.TestCase):
    """Test cases for _parse_expression function."""

    def test_parse_expression_delegates_to_or_expression(self):
        """Test that _parse_expression delegates to _parse_or_expression."""
        mock_ast = {
            "type": "binary_op",
            "operator": "+",
            "left": {"type": "number", "value": 1},
            "right": {"type": "number", "value": 2},
            "line": 1,
            "column": 5
        }
        mock_parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "1", "line": 1, "column": 5},
                {"type": "PLUS", "value": "+", "line": 1, "column": 7},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 9}
            ],
            "pos": 0,
            "filename": "test.cc"
        }
        updated_parser_state = {
            "tokens": mock_parser_state["tokens"],
            "pos": 3,
            "filename": "test.cc"
        }

        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_or_expression_package._parse_or_expression_src._parse_or_expression"
        ) as mock_parse_or:
            mock_parse_or.return_value = (mock_ast, updated_parser_state)

            result = _parse_expression(mock_parser_state)

            self.assertEqual(result, mock_ast)
            mock_parse_or.assert_called_once_with(mock_parser_state)

    def test_parse_expression_with_number(self):
        """Test parsing a simple number expression."""
        mock_ast = {
            "type": "number",
            "value": 42,
            "line": 1,
            "column": 5
        }
        mock_parser_state = {
            "tokens": [{"type": "NUMBER", "value": "42", "line": 1, "column": 5}],
            "pos": 0,
            "filename": "test.cc"
        }

        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_or_expression_package._parse_or_expression_src._parse_or_expression"
        ) as mock_parse_or:
            mock_parse_or.return_value = (mock_ast, mock_parser_state)

            result = _parse_expression(mock_parser_state)

            self.assertEqual(result, mock_ast)
            mock_parse_or.assert_called_once_with(mock_parser_state)

    def test_parse_expression_with_variable(self):
        """Test parsing a variable expression."""
        mock_ast = {
            "type": "identifier",
            "value": "x",
            "line": 1,
            "column": 1
        }
        mock_parser_state = {
            "tokens": [{"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test.cc"
        }

        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_or_expression_package._parse_or_expression_src._parse_or_expression"
        ) as mock_parse_or:
            mock_parse_or.return_value = (mock_ast, mock_parser_state)

            result = _parse_expression(mock_parser_state)

            self.assertEqual(result, mock_ast)
            mock_parse_or.assert_called_once_with(mock_parser_state)

    def test_parse_expression_with_string(self):
        """Test parsing a string literal expression."""
        mock_ast = {
            "type": "string",
            "value": "hello",
            "line": 1,
            "column": 1
        }
        mock_parser_state = {
            "tokens": [{"type": "STRING", "value": '"hello"', "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test.cc"
        }

        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_or_expression_package._parse_or_expression_src._parse_or_expression"
        ) as mock_parse_or:
            mock_parse_or.return_value = (mock_ast, mock_parser_state)

            result = _parse_expression(mock_parser_state)

            self.assertEqual(result, mock_ast)
            mock_parse_or.assert_called_once_with(mock_parser_state)

    def test_parse_expression_with_logical_or(self):
        """Test parsing expression with logical OR operator."""
        mock_ast = {
            "type": "logical_op",
            "operator": "or",
            "left": {"type": "identifier", "value": "a"},
            "right": {"type": "identifier", "value": "b"},
            "line": 1,
            "column": 1
        }
        mock_parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "OR", "value": "or", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 6}
            ],
            "pos": 0,
            "filename": "test.cc"
        }

        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_or_expression_package._parse_or_expression_src._parse_or_expression"
        ) as mock_parse_or:
            mock_parse_or.return_value = (mock_ast, mock_parser_state)

            result = _parse_expression(mock_parser_state)

            self.assertEqual(result, mock_ast)
            mock_parse_or.assert_called_once_with(mock_parser_state)

    def test_parse_expression_with_logical_and(self):
        """Test parsing expression with logical AND operator."""
        mock_ast = {
            "type": "logical_op",
            "operator": "and",
            "left": {"type": "identifier", "value": "x"},
            "right": {"type": "identifier", "value": "y"},
            "line": 2,
            "column": 10
        }
        mock_parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 2, "column": 10},
                {"type": "AND", "value": "and", "line": 2, "column": 12},
                {"type": "IDENTIFIER", "value": "y", "line": 2, "column": 16}
            ],
            "pos": 0,
            "filename": "test.cc"
        }

        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_or_expression_package._parse_or_expression_src._parse_or_expression"
        ) as mock_parse_or:
            mock_parse_or.return_value = (mock_ast, mock_parser_state)

            result = _parse_expression(mock_parser_state)

            self.assertEqual(result, mock_ast)
            mock_parse_or.assert_called_once_with(mock_parser_state)

    def test_parse_expression_with_comparison(self):
        """Test parsing expression with comparison operator."""
        mock_ast = {
            "type": "comparison",
            "operator": ">",
            "left": {"type": "identifier", "value": "a"},
            "right": {"type": "number", "value": 10},
            "line": 1,
            "column": 1
        }
        mock_parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "GREATER", "value": ">", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "10", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.cc"
        }

        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_or_expression_package._parse_or_expression_src._parse_or_expression"
        ) as mock_parse_or:
            mock_parse_or.return_value = (mock_ast, mock_parser_state)

            result = _parse_expression(mock_parser_state)

            self.assertEqual(result, mock_ast)
            mock_parse_or.assert_called_once_with(mock_parser_state)

    def test_parse_expression_with_function_call(self):
        """Test parsing a function call expression."""
        mock_ast = {
            "type": "call",
            "function": {"type": "identifier", "value": "print"},
            "arguments": [
                {"type": "string", "value": "hello"}
            ],
            "line": 1,
            "column": 1
        }
        mock_parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "print", "line": 1, "column": 1},
                {"type": "LPAREN", "value": "(", "line": 1, "column": 6},
                {"type": "STRING", "value": '"hello"', "line": 1, "column": 7},
                {"type": "RPAREN", "value": ")", "line": 1, "column": 14}
            ],
            "pos": 0,
            "filename": "test.cc"
        }

        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_or_expression_package._parse_or_expression_src._parse_or_expression"
        ) as mock_parse_or:
            mock_parse_or.return_value = (mock_ast, mock_parser_state)

            result = _parse_expression(mock_parser_state)

            self.assertEqual(result, mock_ast)
            mock_parse_or.assert_called_once_with(mock_parser_state)

    def test_parse_expression_preserves_parser_state_update(self):
        """Test that parser state is properly updated after parsing."""
        mock_ast = {"type": "number", "value": 100, "line": 1, "column": 1}
        mock_parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "100", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.cc"
        }
        updated_parser_state = {
            "tokens": mock_parser_state["tokens"],
            "pos": 1,
            "filename": "test.cc"
        }

        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_or_expression_package._parse_or_expression_src._parse_or_expression"
        ) as mock_parse_or:
            mock_parse_or.return_value = (mock_ast, updated_parser_state)

            result = _parse_expression(mock_parser_state)

            self.assertEqual(result, mock_ast)
            mock_parse_or.assert_called_once_with(mock_parser_state)

    def test_parse_expression_with_complex_nested_expression(self):
        """Test parsing a complex nested expression."""
        mock_ast = {
            "type": "logical_op",
            "operator": "or",
            "left": {
                "type": "logical_op",
                "operator": "and",
                "left": {
                    "type": "comparison",
                    "operator": ">",
                    "left": {"type": "identifier", "value": "a"},
                    "right": {"type": "number", "value": 0}
                },
                "right": {
                    "type": "comparison",
                    "operator": "<",
                    "left": {"type": "identifier", "value": "a"},
                    "right": {"type": "number", "value": 100}
                }
            },
            "right": {
                "type": "identifier",
                "value": "default"
            },
            "line": 1,
            "column": 1
        }
        mock_parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "GREATER", "value": ">", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "0", "line": 1, "column": 5},
                {"type": "AND", "value": "and", "line": 1, "column": 7},
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 11},
                {"type": "LESS", "value": "<", "line": 1, "column": 13},
                {"type": "NUMBER", "value": "100", "line": 1, "column": 15},
                {"type": "OR", "value": "or", "line": 1, "column": 19},
                {"type": "IDENTIFIER", "value": "default", "line": 1, "column": 22}
            ],
            "pos": 0,
            "filename": "test.cc"
        }

        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_or_expression_package._parse_or_expression_src._parse_or_expression"
        ) as mock_parse_or:
            mock_parse_or.return_value = (mock_ast, mock_parser_state)

            result = _parse_expression(mock_parser_state)

            self.assertEqual(result, mock_ast)
            mock_parse_or.assert_called_once_with(mock_parser_state)

    def test_parse_expression_with_none_return(self):
        """Test parsing when expression can be None (e.g., return without value)."""
        mock_ast = {
            "type": "none",
            "line": 1,
            "column": 7
        }
        mock_parser_state = {
            "tokens": [
                {"type": "NEWLINE", "value": "\n", "line": 1, "column": 7}
            ],
            "pos": 0,
            "filename": "test.cc"
        }

        with patch(
            "main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_or_expression_package._parse_or_expression_src._parse_or_expression"
        ) as mock_parse_or:
            mock_parse_or.return_value = (mock_ast, mock_parser_state)

            result = _parse_expression(mock_parser_state)

            self.assertEqual(result, mock_ast)
            mock_parse_or.assert_called_once_with(mock_parser_state)


if __name__ == "__main__":
    unittest.main()

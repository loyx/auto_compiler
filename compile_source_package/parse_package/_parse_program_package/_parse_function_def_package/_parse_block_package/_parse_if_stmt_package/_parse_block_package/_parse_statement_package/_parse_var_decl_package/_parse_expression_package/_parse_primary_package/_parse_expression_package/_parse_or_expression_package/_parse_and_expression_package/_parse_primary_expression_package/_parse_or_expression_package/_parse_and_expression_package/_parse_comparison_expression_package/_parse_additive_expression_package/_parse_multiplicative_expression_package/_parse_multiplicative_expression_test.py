import unittest
from unittest.mock import patch
from typing import Any, Dict

# Relative import for the function under test
from ._parse_multiplicative_expression_package._parse_multiplicative_expression_src import _parse_multiplicative_expression

Token = Dict[str, Any]
AST = Dict[str, Any]
ParserState = Dict[str, Any]


class TestParseMultiplicativeExpression(unittest.TestCase):
    """Test cases for _parse_multiplicative_expression function."""

    def test_single_primary_expression(self):
        """Test parsing a single primary expression without operators."""
        parser_state = {
            "tokens": [{"type": "identifier", "value": "x", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test.src",
            "error": None
        }

        mock_primary = {"type": "identifier", "value": "x", "line": 1, "column": 1}

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_var_decl_package._parse_expression_package._parse_primary_package._parse_expression_package._parse_or_expression_package._parse_and_expression_package._parse_primary_expression_package._parse_or_expression_package._parse_and_expression_package._parse_comparison_expression_package._parse_additive_expression_package._parse_multiplicative_expression_package._parse_primary_expression_package._parse_primary_expression_src._parse_primary_expression") as mock_parse_primary:
            mock_parse_primary.return_value = mock_primary

            result = _parse_multiplicative_expression(parser_state)

            self.assertEqual(result, mock_primary)
            mock_parse_primary.assert_called_once()

    def test_multiplication_expression(self):
        """Test parsing a * b."""
        parser_state = {
            "tokens": [
                {"type": "identifier", "value": "a", "line": 1, "column": 1},
                {"type": "operator", "value": "*", "line": 1, "column": 3},
                {"type": "identifier", "value": "b", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.src",
            "error": None
        }

        call_count = [0]

        def primary_side_effect(state):
            call_count[0] += 1
            if call_count[0] == 1:
                state["pos"] = 1
                return {"type": "identifier", "value": "a", "line": 1, "column": 1}
            else:
                state["pos"] = 3
                return {"type": "identifier", "value": "b", "line": 1, "column": 5}

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_var_decl_package._parse_expression_package._parse_primary_package._parse_expression_package._parse_or_expression_package._parse_and_expression_package._parse_primary_expression_package._parse_or_expression_package._parse_and_expression_package._parse_comparison_expression_package._parse_additive_expression_package._parse_multiplicative_expression_package._parse_primary_expression_package._parse_primary_expression_src._parse_primary_expression") as mock_parse_primary:
            mock_parse_primary.side_effect = primary_side_effect

            result = _parse_multiplicative_expression(parser_state)

            self.assertEqual(result["type"], "binary_op")
            self.assertEqual(result["operator"], "mul")
            self.assertEqual(result["left"]["value"], "a")
            self.assertEqual(result["right"]["value"], "b")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 3)
            self.assertEqual(parser_state["pos"], 3)
            self.assertEqual(mock_parse_primary.call_count, 2)

    def test_division_expression(self):
        """Test parsing a / b."""
        parser_state = {
            "tokens": [
                {"type": "identifier", "value": "a", "line": 1, "column": 1},
                {"type": "operator", "value": "/", "line": 1, "column": 3},
                {"type": "identifier", "value": "b", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.src",
            "error": None
        }

        call_count = [0]

        def primary_side_effect(state):
            call_count[0] += 1
            if call_count[0] == 1:
                state["pos"] = 1
                return {"type": "identifier", "value": "a", "line": 1, "column": 1}
            else:
                state["pos"] = 3
                return {"type": "identifier", "value": "b", "line": 1, "column": 5}

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_var_decl_package._parse_expression_package._parse_primary_package._parse_expression_package._parse_or_expression_package._parse_and_expression_package._parse_primary_expression_package._parse_or_expression_package._parse_and_expression_package._parse_comparison_expression_package._parse_additive_expression_package._parse_multiplicative_expression_package._parse_primary_expression_package._parse_primary_expression_src._parse_primary_expression") as mock_parse_primary:
            mock_parse_primary.side_effect = primary_side_effect

            result = _parse_multiplicative_expression(parser_state)

            self.assertEqual(result["type"], "binary_op")
            self.assertEqual(result["operator"], "div")
            self.assertEqual(result["left"]["value"], "a")
            self.assertEqual(result["right"]["value"], "b")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 3)

    def test_chained_multiplicative_expression(self):
        """Test parsing a * b / c (left-associative)."""
        parser_state = {
            "tokens": [
                {"type": "identifier", "value": "a", "line": 1, "column": 1},
                {"type": "operator", "value": "*", "line": 1, "column": 3},
                {"type": "identifier", "value": "b", "line": 1, "column": 5},
                {"type": "operator", "value": "/", "line": 1, "column": 7},
                {"type": "identifier", "value": "c", "line": 1, "column": 9}
            ],
            "pos": 0,
            "filename": "test.src",
            "error": None
        }

        call_count = [0]

        def primary_side_effect(state):
            call_count[0] += 1
            if call_count[0] == 1:
                state["pos"] = 1
                return {"type": "identifier", "value": "a", "line": 1, "column": 1}
            elif call_count[0] == 2:
                state["pos"] = 3
                return {"type": "identifier", "value": "b", "line": 1, "column": 5}
            else:
                state["pos"] = 5
                return {"type": "identifier", "value": "c", "line": 1, "column": 9}

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_var_decl_package._parse_expression_package._parse_primary_package._parse_expression_package._parse_or_expression_package._parse_and_expression_package._parse_primary_expression_package._parse_or_expression_package._parse_and_expression_package._parse_comparison_expression_package._parse_additive_expression_package._parse_multiplicative_expression_package._parse_primary_expression_package._parse_primary_expression_src._parse_primary_expression") as mock_parse_primary:
            mock_parse_primary.side_effect = primary_side_effect

            result = _parse_multiplicative_expression(parser_state)

            # Should be left-associative: (a * b) / c
            self.assertEqual(result["type"], "binary_op")
            self.assertEqual(result["operator"], "div")
            self.assertEqual(result["left"]["operator"], "mul")
            self.assertEqual(result["left"]["left"]["value"], "a")
            self.assertEqual(result["left"]["right"]["value"], "b")
            self.assertEqual(result["right"]["value"], "c")
            self.assertEqual(mock_parse_primary.call_count, 3)

    def test_error_on_first_primary(self):
        """Test when error occurs on first primary expression."""
        parser_state = {
            "tokens": [{"type": "identifier", "value": "a", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test.src",
            "error": None
        }

        def primary_side_effect(state):
            state["error"] = "Parse error"
            return {"type": "error", "value": None}

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_var_decl_package._parse_expression_package._parse_primary_package._parse_expression_package._parse_or_expression_package._parse_and_expression_package._parse_primary_expression_package._parse_or_expression_package._parse_and_expression_package._parse_comparison_expression_package._parse_additive_expression_package._parse_multiplicative_expression_package._parse_primary_expression_package._parse_primary_expression_src._parse_primary_expression") as mock_parse_primary:
            mock_parse_primary.side_effect = primary_side_effect

            result = _parse_multiplicative_expression(parser_state)

            self.assertEqual(parser_state["error"], "Parse error")
            self.assertEqual(result["type"], "error")
            mock_parse_primary.assert_called_once()

    def test_error_on_second_primary(self):
        """Test when error occurs on second primary expression."""
        parser_state = {
            "tokens": [
                {"type": "identifier", "value": "a", "line": 1, "column": 1},
                {"type": "operator", "value": "*", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.src",
            "error": None
        }

        call_count = [0]

        def primary_side_effect(state):
            call_count[0] += 1
            if call_count[0] == 1:
                state["pos"] = 1
                return {"type": "identifier", "value": "a", "line": 1, "column": 1}
            else:
                state["error"] = "Parse error on right side"
                return {"type": "error", "value": None}

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_var_decl_package._parse_expression_package._parse_primary_package._parse_expression_package._parse_or_expression_package._parse_and_expression_package._parse_primary_expression_package._parse_or_expression_package._parse_and_expression_package._parse_comparison_expression_package._parse_additive_expression_package._parse_multiplicative_expression_package._parse_primary_expression_package._parse_primary_expression_src._parse_primary_expression") as mock_parse_primary:
            mock_parse_primary.side_effect = primary_side_effect

            result = _parse_multiplicative_expression(parser_state)

            self.assertEqual(parser_state["error"], "Parse error on right side")
            # Should return the left part that was already parsed
            self.assertEqual(result["value"], "a")
            self.assertEqual(mock_parse_primary.call_count, 2)

    def test_empty_tokens(self):
        """Test parsing with empty token list."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.src",
            "error": None
        }

        mock_primary = {"type": "empty", "value": None}

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_var_decl_package._parse_expression_package._parse_primary_package._parse_expression_package._parse_or_expression_package._parse_and_expression_package._parse_primary_expression_package._parse_or_expression_package._parse_and_expression_package._parse_comparison_expression_package._parse_additive_expression_package._parse_multiplicative_expression_package._parse_primary_expression_package._parse_primary_expression_src._parse_primary_expression") as mock_parse_primary:
            mock_parse_primary.return_value = mock_primary

            result = _parse_multiplicative_expression(parser_state)

            self.assertEqual(result, mock_primary)
            mock_parse_primary.assert_called_once()

    def test_non_multiplicative_operator(self):
        """Test that non-multiplicative operators stop parsing."""
        parser_state = {
            "tokens": [
                {"type": "identifier", "value": "a", "line": 1, "column": 1},
                {"type": "operator", "value": "+", "line": 1, "column": 3},
                {"type": "identifier", "value": "b", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.src",
            "error": None
        }

        call_count = [0]

        def primary_side_effect(state):
            call_count[0] += 1
            state["pos"] = call_count[0]
            return {"type": "identifier", "value": "a", "line": 1, "column": 1}

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_var_decl_package._parse_expression_package._parse_primary_package._parse_expression_package._parse_or_expression_package._parse_and_expression_package._parse_primary_expression_package._parse_or_expression_package._parse_and_expression_package._parse_comparison_expression_package._parse_additive_expression_package._parse_multiplicative_expression_package._parse_primary_expression_package._parse_primary_expression_src._parse_primary_expression") as mock_parse_primary:
            mock_parse_primary.side_effect = primary_side_effect

            result = _parse_multiplicative_expression(parser_state)

            # Should only parse the first primary, not consume the +
            self.assertEqual(result["value"], "a")
            self.assertEqual(parser_state["pos"], 1)
            # primary should only be called once
            self.assertEqual(mock_parse_primary.call_count, 1)

    def test_position_at_end(self):
        """Test when position is already at end of tokens."""
        parser_state = {
            "tokens": [{"type": "identifier", "value": "a", "line": 1, "column": 1}],
            "pos": 1,  # Already at end
            "filename": "test.src",
            "error": None
        }

        mock_primary = {"type": "identifier", "value": "a", "line": 1, "column": 1}

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_var_decl_package._parse_expression_package._parse_primary_package._parse_expression_package._parse_or_expression_package._parse_and_expression_package._parse_primary_expression_package._parse_or_expression_package._parse_and_expression_package._parse_comparison_expression_package._parse_additive_expression_package._parse_multiplicative_expression_package._parse_primary_expression_package._parse_primary_expression_src._parse_primary_expression") as mock_parse_primary:
            mock_parse_primary.return_value = mock_primary

            result = _parse_multiplicative_expression(parser_state)

            self.assertEqual(result, mock_primary)
            mock_parse_primary.assert_called_once()

    def test_multiple_same_operators(self):
        """Test parsing a * b * c."""
        parser_state = {
            "tokens": [
                {"type": "identifier", "value": "a", "line": 1, "column": 1},
                {"type": "operator", "value": "*", "line": 1, "column": 3},
                {"type": "identifier", "value": "b", "line": 1, "column": 5},
                {"type": "operator", "value": "*", "line": 1, "column": 7},
                {"type": "identifier", "value": "c", "line": 1, "column": 9}
            ],
            "pos": 0,
            "filename": "test.src",
            "error": None
        }

        call_count = [0]

        def primary_side_effect(state):
            call_count[0] += 1
            if call_count[0] == 1:
                state["pos"] = 1
                return {"type": "identifier", "value": "a", "line": 1, "column": 1}
            elif call_count[0] == 2:
                state["pos"] = 3
                return {"type": "identifier", "value": "b", "line": 1, "column": 5}
            else:
                state["pos"] = 5
                return {"type": "identifier", "value": "c", "line": 1, "column": 9}

        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_var_decl_package._parse_expression_package._parse_primary_package._parse_expression_package._parse_or_expression_package._parse_and_expression_package._parse_primary_expression_package._parse_or_expression_package._parse_and_expression_package._parse_comparison_expression_package._parse_additive_expression_package._parse_multiplicative_expression_package._parse_primary_expression_package._parse_primary_expression_src._parse_primary_expression") as mock_parse_primary:
            mock_parse_primary.side_effect = primary_side_effect

            result = _parse_multiplicative_expression(parser_state)

            # Should be left-associative: (a * b) * c
            self.assertEqual(result["type"], "binary_op")
            self.assertEqual(result["operator"], "mul")
            self.assertEqual(result["left"]["operator"], "mul")
            self.assertEqual(result["left"]["left"]["value"], "a")
            self.assertEqual(result["left"]["right"]["value"], "b")
            self.assertEqual(result["right"]["value"], "c")


if __name__ == "__main__":
    unittest.main()

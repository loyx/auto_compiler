import unittest
from unittest.mock import patch, MagicMock
from typing import Any, Dict

# Relative import for the function under test
from ._parse_additive_expr_src import _parse_additive_expr

# Type aliases
Token = Dict[str, Any]
AST = Dict[str, Any]
ParserState = Dict[str, Any]


class TestParseAdditiveExpr(unittest.TestCase):
    """Test cases for _parse_additive_expr function."""

    def _create_token(self, token_type: str, value: str, line: int = 1, column: int = 1) -> Token:
        """Helper to create a token."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def _create_ast_node(self, node_type: str, children: list = None, value: Any = None, line: int = 1, column: int = 1) -> AST:
        """Helper to create an AST node."""
        return {
            "type": node_type,
            "children": children if children is not None else [],
            "value": value,
            "line": line,
            "column": column
        }

    @patch("._parse_multiplicative_expr_package._parse_multiplicative_expr_src._parse_multiplicative_expr")
    def test_single_operand_no_operator(self, mock_parse_mult: MagicMock):
        """Test parsing a single operand with no additive operator."""
        # Arrange
        operand_ast = self._create_ast_node("IDENTIFIER", value="x")
        mock_parse_mult.return_value = operand_ast

        tokens = [self._create_token("IDENTIFIER", "x")]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }

        # Act
        result = _parse_additive_expr(parser_state)

        # Assert
        self.assertEqual(result, operand_ast)
        self.assertEqual(parser_state["pos"], 0)
        mock_parse_mult.assert_called_once_with(parser_state)

    @patch("._parse_multiplicative_expr_package._parse_multiplicative_expr_src._parse_multiplicative_expr")
    def test_simple_addition(self, mock_parse_mult: MagicMock):
        """Test parsing a simple addition expression: a + b."""
        # Arrange
        left_operand = self._create_ast_node("IDENTIFIER", value="a")
        right_operand = self._create_ast_node("IDENTIFIER", value="b")

        # First call returns left operand, second call returns right operand
        mock_parse_mult.side_effect = [left_operand, right_operand]

        tokens = [
            self._create_token("IDENTIFIER", "a", line=1, column=1),
            self._create_token("ADD", "+", line=1, column=3),
            self._create_token("IDENTIFIER", "b", line=1, column=5)
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }

        # Act
        result = _parse_additive_expr(parser_state)

        # Assert
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "+")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 3)
        self.assertEqual(len(result["children"]), 2)
        self.assertEqual(result["children"][0], left_operand)
        self.assertEqual(result["children"][1], right_operand)
        self.assertEqual(parser_state["pos"], 3)
        self.assertEqual(mock_parse_mult.call_count, 2)

    @patch("._parse_multiplicative_expr_package._parse_multiplicative_expr_src._parse_multiplicative_expr")
    def test_simple_subtraction(self, mock_parse_mult: MagicMock):
        """Test parsing a simple subtraction expression: a - b."""
        # Arrange
        left_operand = self._create_ast_node("IDENTIFIER", value="a")
        right_operand = self._create_ast_node("IDENTIFIER", value="b")

        mock_parse_mult.side_effect = [left_operand, right_operand]

        tokens = [
            self._create_token("IDENTIFIER", "a", line=1, column=1),
            self._create_token("SUB", "-", line=1, column=3),
            self._create_token("IDENTIFIER", "b", line=1, column=5)
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }

        # Act
        result = _parse_additive_expr(parser_state)

        # Assert
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "-")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 3)
        self.assertEqual(len(result["children"]), 2)
        self.assertEqual(result["children"][0], left_operand)
        self.assertEqual(result["children"][1], right_operand)
        self.assertEqual(parser_state["pos"], 3)

    @patch("._parse_multiplicative_expr_package._parse_multiplicative_expr_src._parse_multiplicative_expr")
    def test_left_associativity(self, mock_parse_mult: MagicMock):
        """Test left-associativity: a + b - c should parse as (a + b) - c."""
        # Arrange
        operand_a = self._create_ast_node("IDENTIFIER", value="a")
        operand_b = self._create_ast_node("IDENTIFIER", value="b")
        operand_c = self._create_ast_node("IDENTIFIER", value="c")

        mock_parse_mult.side_effect = [operand_a, operand_b, operand_c]

        tokens = [
            self._create_token("IDENTIFIER", "a", line=1, column=1),
            self._create_token("ADD", "+", line=1, column=3),
            self._create_token("IDENTIFIER", "b", line=1, column=5),
            self._create_token("SUB", "-", line=1, column=7),
            self._create_token("IDENTIFIER", "c", line=1, column=9)
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }

        # Act
        result = _parse_additive_expr(parser_state)

        # Assert: Should be (a + b) - c
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "-")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 7)
        self.assertEqual(len(result["children"]), 2)

        # Left child should be (a + b)
        left_child = result["children"][0]
        self.assertEqual(left_child["type"], "BINARY_OP")
        self.assertEqual(left_child["value"], "+")
        self.assertEqual(left_child["children"][0], operand_a)
        self.assertEqual(left_child["children"][1], operand_b)

        # Right child should be c
        self.assertEqual(result["children"][1], operand_c)
        self.assertEqual(parser_state["pos"], 5)
        self.assertEqual(mock_parse_mult.call_count, 3)

    @patch("._parse_multiplicative_expr_package._parse_multiplicative_expr_src._parse_multiplicative_expr")
    def test_multiple_additions(self, mock_parse_mult: MagicMock):
        """Test multiple additions: a + b + c."""
        # Arrange
        operand_a = self._create_ast_node("IDENTIFIER", value="a")
        operand_b = self._create_ast_node("IDENTIFIER", value="b")
        operand_c = self._create_ast_node("IDENTIFIER", value="c")

        mock_parse_mult.side_effect = [operand_a, operand_b, operand_c]

        tokens = [
            self._create_token("IDENTIFIER", "a", line=1, column=1),
            self._create_token("ADD", "+", line=1, column=3),
            self._create_token("IDENTIFIER", "b", line=1, column=5),
            self._create_token("ADD", "+", line=1, column=7),
            self._create_token("IDENTIFIER", "c", line=1, column=9)
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }

        # Act
        result = _parse_additive_expr(parser_state)

        # Assert: Should be (a + b) + c
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "+")
        self.assertEqual(result["column"], 7)

        left_child = result["children"][0]
        self.assertEqual(left_child["type"], "BINARY_OP")
        self.assertEqual(left_child["value"], "+")
        self.assertEqual(left_child["children"][0], operand_a)
        self.assertEqual(left_child["children"][1], operand_b)

        self.assertEqual(result["children"][1], operand_c)
        self.assertEqual(parser_state["pos"], 5)

    @patch("._parse_multiplicative_expr_package._parse_multiplicative_expr_src._parse_multiplicative_expr")
    def test_empty_tokens(self, mock_parse_mult: MagicMock):
        """Test with empty token list."""
        # Arrange
        empty_ast = self._create_ast_node("LITERAL", value=None)
        mock_parse_mult.return_value = empty_ast

        parser_state: ParserState = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }

        # Act
        result = _parse_additive_expr(parser_state)

        # Assert
        self.assertEqual(result, empty_ast)
        self.assertEqual(parser_state["pos"], 0)
        mock_parse_mult.assert_called_once_with(parser_state)

    @patch("._parse_multiplicative_expr_package._parse_multiplicative_expr_src._parse_multiplicative_expr")
    def test_error_from_multiplicative_expr(self, mock_parse_mult: MagicMock):
        """Test when _parse_multiplicative_expr sets an error."""
        # Arrange
        error_ast = self._create_ast_node("ERROR", value="parse error")
        mock_parse_mult.return_value = error_ast

        tokens = [
            self._create_token("IDENTIFIER", "a", line=1, column=1),
            self._create_token("ADD", "+", line=1, column=3)
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
            "error": "parse error"
        }

        # Act
        result = _parse_additive_expr(parser_state)

        # Assert
        self.assertEqual(result, error_ast)
        self.assertEqual(parser_state["pos"], 0)
        mock_parse_mult.assert_called_once_with(parser_state)

    @patch("._parse_multiplicative_expr_package._parse_multiplicative_expr_src._parse_multiplicative_expr")
    def test_error_after_first_operand(self, mock_parse_mult: MagicMock):
        """Test when error occurs after parsing first operand but before second."""
        # Arrange
        left_operand = self._create_ast_node("IDENTIFIER", value="a")
        right_operand = self._create_ast_node("ERROR", value="error")

        mock_parse_mult.side_effect = [left_operand, right_operand]

        tokens = [
            self._create_token("IDENTIFIER", "a", line=1, column=1),
            self._create_token("ADD", "+", line=1, column=3),
            self._create_token("IDENTIFIER", "b", line=1, column=5)
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }

        # Configure mock to set error on second call
        def side_effect(state):
            if mock_parse_mult.call_count == 2:
                state["error"] = "second operand error"
            return mock_parse_mult.side_effect[mock_parse_mult.call_count - 1]

        mock_parse_mult.side_effect = side_effect

        # Act
        result = _parse_additive_expr(parser_state)

        # Assert
        self.assertEqual(result, left_operand)
        self.assertEqual(parser_state["error"], "second operand error")

    @patch("._parse_multiplicative_expr_package._parse_multiplicative_expr_src._parse_multiplicative_expr")
    def test_non_additive_operator_after_operand(self, mock_parse_mult: MagicMock):
        """Test when next token is not an additive operator."""
        # Arrange
        left_operand = self._create_ast_node("IDENTIFIER", value="a")
        mock_parse_mult.return_value = left_operand

        tokens = [
            self._create_token("IDENTIFIER", "a", line=1, column=1),
            self._create_token("MUL", "*", line=1, column=3),
            self._create_token("IDENTIFIER", "b", line=1, column=5)
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }

        # Act
        result = _parse_additive_expr(parser_state)

        # Assert
        self.assertEqual(result, left_operand)
        self.assertEqual(parser_state["pos"], 0)
        mock_parse_mult.assert_called_once_with(parser_state)

    @patch("._parse_multiplicative_expr_package._parse_multiplicative_expr_src._parse_multiplicative_expr")
    def test_mixed_add_sub_operators(self, mock_parse_mult: MagicMock):
        """Test mixed + and - operators: a + b - c + d."""
        # Arrange
        operand_a = self._create_ast_node("IDENTIFIER", value="a")
        operand_b = self._create_ast_node("IDENTIFIER", value="b")
        operand_c = self._create_ast_node("IDENTIFIER", value="c")
        operand_d = self._create_ast_node("IDENTIFIER", value="d")

        mock_parse_mult.side_effect = [operand_a, operand_b, operand_c, operand_d]

        tokens = [
            self._create_token("IDENTIFIER", "a", line=1, column=1),
            self._create_token("ADD", "+", line=1, column=3),
            self._create_token("IDENTIFIER", "b", line=1, column=5),
            self._create_token("SUB", "-", line=1, column=7),
            self._create_token("IDENTIFIER", "c", line=1, column=9),
            self._create_token("ADD", "+", line=1, column=11),
            self._create_token("IDENTIFIER", "d", line=1, column=13)
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }

        # Act
        result = _parse_additive_expr(parser_state)

        # Assert: Should be ((a + b) - c) + d
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "+")
        self.assertEqual(result["column"], 11)

        # Left child: (a + b) - c
        left_child = result["children"][0]
        self.assertEqual(left_child["type"], "BINARY_OP")
        self.assertEqual(left_child["value"], "-")

        # Left-left: a + b
        left_left = left_child["children"][0]
        self.assertEqual(left_left["type"], "BINARY_OP")
        self.assertEqual(left_left["value"], "+")
        self.assertEqual(left_left["children"][0], operand_a)
        self.assertEqual(left_left["children"][1], operand_b)

        # Left-right: c
        self.assertEqual(left_child["children"][1], operand_c)

        # Right: d
        self.assertEqual(result["children"][1], operand_d)
        self.assertEqual(parser_state["pos"], 7)
        self.assertEqual(mock_parse_mult.call_count, 4)


if __name__ == "__main__":
    unittest.main()

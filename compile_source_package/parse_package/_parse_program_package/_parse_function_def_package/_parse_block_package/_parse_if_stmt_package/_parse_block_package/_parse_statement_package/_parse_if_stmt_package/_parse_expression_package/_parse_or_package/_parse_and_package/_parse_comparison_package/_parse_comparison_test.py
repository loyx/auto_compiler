# === std / third-party imports ===
import unittest
from unittest.mock import patch
from typing import Any, Dict

# === sub function imports ===
from ._parse_comparison_src import _parse_comparison


# === Test Class ===
class TestParseComparison(unittest.TestCase):
    """Test cases for _parse_comparison function."""

    def _create_parser_state(self, tokens: list, pos: int = 0) -> Dict[str, Any]:
        """Helper to create a parser state dictionary."""
        return {
            "tokens": tokens,
            "pos": pos,
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

    def test_single_comparison_gt(self):
        """Test parsing a single greater-than comparison."""
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("GT", ">", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 5),
        ]
        parser_state = self._create_parser_state(tokens)

        left_operand = {"type": "IDENTIFIER", "name": "a", "line": 1, "column": 1}
        right_operand = {"type": "IDENTIFIER", "name": "b", "line": 1, "column": 5}

        with patch("._parse_comparison_src._parse_additive") as mock_additive:
            mock_additive.side_effect = [left_operand, right_operand]
            result = _parse_comparison(parser_state)

        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["operator"], ">")
        self.assertEqual(result["left"], left_operand)
        self.assertEqual(result["right"], right_operand)
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 3)
        self.assertEqual(parser_state["pos"], 3)

    def test_single_comparison_lt(self):
        """Test parsing a single less-than comparison."""
        tokens = [
            self._create_token("IDENTIFIER", "x", 1, 1),
            self._create_token("LT", "<", 1, 3),
            self._create_token("NUMBER", "10", 1, 5),
        ]
        parser_state = self._create_parser_state(tokens)

        left_operand = {"type": "IDENTIFIER", "name": "x", "line": 1, "column": 1}
        right_operand = {"type": "NUMBER", "value": "10", "literal_type": "int", "line": 1, "column": 5}

        with patch("._parse_comparison_src._parse_additive") as mock_additive:
            mock_additive.side_effect = [left_operand, right_operand]
            result = _parse_comparison(parser_state)

        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["operator"], "<")
        self.assertEqual(parser_state["pos"], 3)

    def test_single_comparison_ge(self):
        """Test parsing a single greater-than-or-equal comparison."""
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("GE", ">=", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 6),
        ]
        parser_state = self._create_parser_state(tokens)

        left_operand = {"type": "IDENTIFIER", "name": "a", "line": 1, "column": 1}
        right_operand = {"type": "IDENTIFIER", "name": "b", "line": 1, "column": 6}

        with patch("._parse_comparison_src._parse_additive") as mock_additive:
            mock_additive.side_effect = [left_operand, right_operand]
            result = _parse_comparison(parser_state)

        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["operator"], ">=")

    def test_single_comparison_le(self):
        """Test parsing a single less-than-or-equal comparison."""
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("LE", "<=", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 6),
        ]
        parser_state = self._create_parser_state(tokens)

        left_operand = {"type": "IDENTIFIER", "name": "a", "line": 1, "column": 1}
        right_operand = {"type": "IDENTIFIER", "name": "b", "line": 1, "column": 6}

        with patch("._parse_comparison_src._parse_additive") as mock_additive:
            mock_additive.side_effect = [left_operand, right_operand]
            result = _parse_comparison(parser_state)

        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["operator"], "<=")

    def test_single_comparison_eq(self):
        """Test parsing a single equality comparison."""
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("EQ", "==", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 6),
        ]
        parser_state = self._create_parser_state(tokens)

        left_operand = {"type": "IDENTIFIER", "name": "a", "line": 1, "column": 1}
        right_operand = {"type": "IDENTIFIER", "name": "b", "line": 1, "column": 6}

        with patch("._parse_comparison_src._parse_additive") as mock_additive:
            mock_additive.side_effect = [left_operand, right_operand]
            result = _parse_comparison(parser_state)

        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["operator"], "==")

    def test_single_comparison_ne(self):
        """Test parsing a single not-equal comparison."""
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("NE", "!=", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 6),
        ]
        parser_state = self._create_parser_state(tokens)

        left_operand = {"type": "IDENTIFIER", "name": "a", "line": 1, "column": 1}
        right_operand = {"type": "IDENTIFIER", "name": "b", "line": 1, "column": 6}

        with patch("._parse_comparison_src._parse_additive") as mock_additive:
            mock_additive.side_effect = [left_operand, right_operand]
            result = _parse_comparison(parser_state)

        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["operator"], "!=")

    def test_chained_comparison_left_associative(self):
        """Test that chained comparisons are left-associative."""
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("GT", ">", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 5),
            self._create_token("LT", "<", 1, 7),
            self._create_token("IDENTIFIER", "c", 1, 9),
        ]
        parser_state = self._create_parser_state(tokens)

        operand_a = {"type": "IDENTIFIER", "name": "a", "line": 1, "column": 1}
        operand_b = {"type": "IDENTIFIER", "name": "b", "line": 1, "column": 5}
        operand_c = {"type": "IDENTIFIER", "name": "c", "line": 1, "column": 9}

        with patch("._parse_comparison_src._parse_additive") as mock_additive:
            mock_additive.side_effect = [operand_a, operand_b, operand_c]
            result = _parse_comparison(parser_state)

        # Should be ((a > b) < c)
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["operator"], "<")
        self.assertEqual(result["right"], operand_c)
        
        left_part = result["left"]
        self.assertEqual(left_part["type"], "BINARY_OP")
        self.assertEqual(left_part["operator"], ">")
        self.assertEqual(left_part["left"], operand_a)
        self.assertEqual(left_part["right"], operand_b)
        
        self.assertEqual(parser_state["pos"], 5)

    def test_no_comparison_operator(self):
        """Test when there is no comparison operator, just return additive result."""
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("SEMICOLON", ";", 1, 2),
        ]
        parser_state = self._create_parser_state(tokens)

        operand = {"type": "IDENTIFIER", "name": "a", "line": 1, "column": 1}

        with patch("._parse_comparison_src._parse_additive") as mock_additive:
            mock_additive.return_value = operand
            result = _parse_comparison(parser_state)

        self.assertEqual(result, operand)
        self.assertEqual(parser_state["pos"], 0)

    def test_left_operand_error(self):
        """Test when left operand (_parse_additive) returns error."""
        tokens = [
            self._create_token("GT", ">", 1, 1),
            self._create_token("IDENTIFIER", "b", 1, 3),
        ]
        parser_state = self._create_parser_state(tokens)
        parser_state["error"] = "Parse error in additive"

        error_ast = {"type": "ERROR", "line": 1, "column": 1}

        with patch("._parse_comparison_src._parse_additive") as mock_additive:
            mock_additive.return_value = error_ast
            result = _parse_comparison(parser_state)

        self.assertEqual(result, error_ast)
        self.assertEqual(parser_state["pos"], 0)

    def test_right_operand_error(self):
        """Test when right operand parsing fails."""
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
            self._create_token("GT", ">", 1, 3),
            self._create_token("IDENTIFIER", "b", 1, 5),
        ]
        parser_state = self._create_parser_state(tokens)

        left_operand = {"type": "IDENTIFIER", "name": "a", "line": 1, "column": 1}
        error_ast = {"type": "ERROR", "line": 1, "column": 5}

        with patch("._parse_comparison_src._parse_additive") as mock_additive:
            mock_additive.side_effect = [left_operand, error_ast]
            result = _parse_comparison(parser_state)

        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 3)

    def test_eof_handling(self):
        """Test handling when tokens are exhausted."""
        tokens = [
            self._create_token("IDENTIFIER", "a", 1, 1),
        ]
        parser_state = self._create_parser_state(tokens)

        operand = {"type": "IDENTIFIER", "name": "a", "line": 1, "column": 1}

        with patch("._parse_comparison_src._parse_additive") as mock_additive:
            mock_additive.return_value = operand
            result = _parse_comparison(parser_state)

        self.assertEqual(result, operand)
        self.assertEqual(parser_state["pos"], 0)

    def test_multiple_chained_comparisons(self):
        """Test multiple chained comparisons for left-associativity."""
        tokens = [
            self._create_token("NUMBER", "1", 1, 1),
            self._create_token("LT", "<", 1, 3),
            self._create_token("NUMBER", "2", 1, 5),
            self._create_token("LT", "<", 1, 7),
            self._create_token("NUMBER", "3", 1, 9),
            self._create_token("LT", "<", 1, 11),
            self._create_token("NUMBER", "4", 1, 13),
        ]
        parser_state = self._create_parser_state(tokens)

        num1 = {"type": "NUMBER", "value": "1", "literal_type": "int", "line": 1, "column": 1}
        num2 = {"type": "NUMBER", "value": "2", "literal_type": "int", "line": 1, "column": 5}
        num3 = {"type": "NUMBER", "value": "3", "literal_type": "int", "line": 1, "column": 9}
        num4 = {"type": "NUMBER", "value": "4", "literal_type": "int", "line": 1, "column": 13}

        with patch("._parse_comparison_src._parse_additive") as mock_additive:
            mock_additive.side_effect = [num1, num2, num3, num4]
            result = _parse_comparison(parser_state)

        # Should be (((1 < 2) < 3) < 4)
        self.assertEqual(result["operator"], "<")
        self.assertEqual(result["right"], num4)
        
        level2 = result["left"]
        self.assertEqual(level2["operator"], "<")
        self.assertEqual(level2["right"], num3)
        
        level1 = level2["left"]
        self.assertEqual(level1["operator"], "<")
        self.assertEqual(level1["left"], num1)
        self.assertEqual(level1["right"], num2)
        
        self.assertEqual(parser_state["pos"], 7)


# === Test Runner ===
if __name__ == "__main__":
    unittest.main()

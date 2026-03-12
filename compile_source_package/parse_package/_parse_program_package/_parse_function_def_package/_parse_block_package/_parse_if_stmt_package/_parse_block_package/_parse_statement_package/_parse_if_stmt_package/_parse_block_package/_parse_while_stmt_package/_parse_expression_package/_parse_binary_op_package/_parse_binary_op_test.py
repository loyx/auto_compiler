import unittest
from unittest.mock import patch
from ._parse_binary_op_src import _parse_binary_op


class TestParseBinaryOp(unittest.TestCase):
    """Test cases for _parse_binary_op function."""

    def _make_token(self, token_type: str, value: str, line: int, column: int) -> dict:
        """Helper to create a token dict."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def test_no_operator_returns_left(self):
        """Test when there's no operator, returns left operand as-is."""
        parser_state = {
            "tokens": [self._make_token("NUMBER", "42", 1, 1)],
            "filename": "test.py",
            "pos": 1  # Already past all tokens
        }
        left = {"type": "number", "value": "1", "line": 1, "column": 1}

        result = _parse_binary_op(parser_state, left, 0)

        self.assertEqual(result, left)
        self.assertEqual(parser_state["pos"], 1)

    def test_single_binary_operation(self):
        """Test parsing a single binary operation: 1 + 2."""
        tokens = [
            self._make_token("NUMBER", "1", 1, 1),
            self._make_token("PLUS", "+", 1, 3),
            self._make_token("NUMBER", "2", 1, 5)
        ]
        parser_state = {
            "tokens": tokens,
            "filename": "test.py",
            "pos": 1  # At PLUS operator
        }
        left = {"type": "number", "value": "1", "line": 1, "column": 1}

        with patch("._parse_unary_op_package._parse_unary_op_src._parse_unary_op") as mock_unary:
            mock_unary.return_value = {"type": "number", "value": "2", "line": 1, "column": 5}

            result = _parse_binary_op(parser_state, left, 0)

        self.assertEqual(result["type"], "binary_op")
        self.assertEqual(result["operator"], "+")
        self.assertEqual(result["left"]["value"], "1")
        self.assertEqual(result["right"]["value"], "2")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 3)
        self.assertEqual(parser_state["pos"], 3)

    def test_precedence_climbing(self):
        """Test precedence: 1 + 2 * 3 should be 1 + (2 * 3)."""
        tokens = [
            self._make_token("NUMBER", "1", 1, 1),
            self._make_token("PLUS", "+", 1, 3),
            self._make_token("NUMBER", "2", 1, 5),
            self._make_token("STAR", "*", 1, 7),
            self._make_token("NUMBER", "3", 1, 9)
        ]
        parser_state = {
            "tokens": tokens,
            "filename": "test.py",
            "pos": 1  # At PLUS
        }
        left = {"type": "number", "value": "1", "line": 1, "column": 1}

        call_count = [0]

        def mock_unary_side_effect(ps):
            call_count[0] += 1
            if call_count[0] == 1:
                return {"type": "number", "value": "2", "line": 1, "column": 5}
            else:
                return {"type": "number", "value": "3", "line": 1, "column": 9}

        with patch("._parse_unary_op_package._parse_unary_op_src._parse_unary_op", side_effect=mock_unary_side_effect):
            result = _parse_binary_op(parser_state, left, 0)

        # Should be: (1 + (2 * 3))
        # Top level should be +
        self.assertEqual(result["type"], "binary_op")
        self.assertEqual(result["operator"], "+")
        # Left should be 1
        self.assertEqual(result["left"]["value"], "1")
        # Right should be the * operation
        self.assertEqual(result["right"]["type"], "binary_op")
        self.assertEqual(result["right"]["operator"], "*")

    def test_right_associativity_doublestar(self):
        """Test right-associativity: 2 ** 3 ** 4 should be 2 ** (3 ** 4)."""
        tokens = [
            self._make_token("NUMBER", "2", 1, 1),
            self._make_token("DOUBLESTAR", "**", 1, 3),
            self._make_token("NUMBER", "3", 1, 6),
            self._make_token("DOUBLESTAR", "**", 1, 8),
            self._make_token("NUMBER", "4", 1, 11)
        ]
        parser_state = {
            "tokens": tokens,
            "filename": "test.py",
            "pos": 1  # At first **
        }
        left = {"type": "number", "value": "2", "line": 1, "column": 1}

        call_count = [0]

        def mock_unary_side_effect(ps):
            call_count[0] += 1
            if call_count[0] == 1:
                return {"type": "number", "value": "3", "line": 1, "column": 6}
            else:
                return {"type": "number", "value": "4", "line": 1, "column": 11}

        with patch("._parse_unary_op_package._parse_unary_op_src._parse_unary_op", side_effect=mock_unary_side_effect):
            result = _parse_binary_op(parser_state, left, 0)

        # Should be: 2 ** (3 ** 4)
        # Top level should be ** with left=2, right=(3 ** 4)
        self.assertEqual(result["type"], "binary_op")
        self.assertEqual(result["operator"], "**")
        self.assertEqual(result["left"]["value"], "2")
        # Right should be another ** operation
        self.assertEqual(result["right"]["type"], "binary_op")
        self.assertEqual(result["right"]["operator"], "**")
        self.assertEqual(result["right"]["left"]["value"], "3")
        self.assertEqual(result["right"]["right"]["value"], "4")

    def test_left_associativity_plus(self):
        """Test left-associativity: 1 + 2 + 3 should be (1 + 2) + 3."""
        tokens = [
            self._make_token("NUMBER", "1", 1, 1),
            self._make_token("PLUS", "+", 1, 3),
            self._make_token("NUMBER", "2", 1, 5),
            self._make_token("PLUS", "+", 1, 7),
            self._make_token("NUMBER", "3", 1, 9)
        ]
        parser_state = {
            "tokens": tokens,
            "filename": "test.py",
            "pos": 1  # At first +
        }
        left = {"type": "number", "value": "1", "line": 1, "column": 1}

        call_count = [0]

        def mock_unary_side_effect(ps):
            call_count[0] += 1
            if call_count[0] == 1:
                return {"type": "number", "value": "2", "line": 1, "column": 5}
            else:
                return {"type": "number", "value": "3", "line": 1, "column": 9}

        with patch("._parse_unary_op_package._parse_unary_op_src._parse_unary_op", side_effect=mock_unary_side_effect):
            result = _parse_binary_op(parser_state, left, 0)

        # Should be: (1 + 2) + 3
        # Top level should be + with left=(1 + 2), right=3
        self.assertEqual(result["type"], "binary_op")
        self.assertEqual(result["operator"], "+")
        # Left should be another + operation
        self.assertEqual(result["left"]["type"], "binary_op")
        self.assertEqual(result["left"]["operator"], "+")
        self.assertEqual(result["left"]["left"]["value"], "1")
        self.assertEqual(result["left"]["right"]["value"], "2")
        # Right should be 3
        self.assertEqual(result["right"]["value"], "3")

    def test_min_precedence_stops_parsing(self):
        """Test that operators below min_precedence are not parsed."""
        tokens = [
            self._make_token("NUMBER", "1", 1, 1),
            self._make_token("PLUS", "+", 1, 3),
            self._make_token("NUMBER", "2", 1, 5),
            self._make_token("STAR", "*", 1, 7),
            self._make_token("NUMBER", "3", 1, 9)
        ]
        parser_state = {
            "tokens": tokens,
            "filename": "test.py",
            "pos": 1  # At PLUS
        }
        left = {"type": "number", "value": "1", "line": 1, "column": 1}

        # Set min_precedence to 5 (STAR level), so PLUS (4) should not be parsed
        result = _parse_binary_op(parser_state, left, 5)

        # Should return left as-is since PLUS has precedence 4 < 5
        self.assertEqual(result, left)
        self.assertEqual(parser_state["pos"], 1)  # pos should not advance

    def test_error_on_unexpected_end(self):
        """Test SyntaxError when expression ends after operator."""
        tokens = [
            self._make_token("NUMBER", "1", 1, 1),
            self._make_token("PLUS", "+", 1, 3)
        ]
        parser_state = {
            "tokens": tokens,
            "filename": "test.py",
            "pos": 1  # At PLUS
        }
        left = {"type": "number", "value": "1", "line": 1, "column": 1}

        with self.assertRaises(SyntaxError) as context:
            _parse_binary_op(parser_state, left, 0)

        self.assertIn("Unexpected end", str(context.exception))

    def test_comparison_operators(self):
        """Test comparison operators with same precedence."""
        tokens = [
            self._make_token("NUMBER", "1", 1, 1),
            self._make_token("LT", "<", 1, 3),
            self._make_token("NUMBER", "2", 1, 5)
        ]
        parser_state = {
            "tokens": tokens,
            "filename": "test.py",
            "pos": 1  # At LT
        }
        left = {"type": "number", "value": "1", "line": 1, "column": 1}

        with patch("._parse_unary_op_package._parse_unary_op_src._parse_unary_op") as mock_unary:
            mock_unary.return_value = {"type": "number", "value": "2", "line": 1, "column": 5}

            result = _parse_binary_op(parser_state, left, 0)

        self.assertEqual(result["type"], "binary_op")
        self.assertEqual(result["operator"], "<")

    def test_logical_operators(self):
        """Test logical operators OR and AND with lowest precedence."""
        tokens = [
            self._make_token("BOOL", "True", 1, 1),
            self._make_token("OR", "or", 1, 6),
            self._make_token("BOOL", "False", 1, 9)
        ]
        parser_state = {
            "tokens": tokens,
            "filename": "test.py",
            "pos": 1  # At OR
        }
        left = {"type": "bool", "value": "True", "line": 1, "column": 1}

        with patch("._parse_unary_op_package._parse_unary_op_src._parse_unary_op") as mock_unary:
            mock_unary.return_value = {"type": "bool", "value": "False", "line": 1, "column": 9}

            result = _parse_binary_op(parser_state, left, 0)

        self.assertEqual(result["type"], "binary_op")
        self.assertEqual(result["operator"], "or")

    def test_position_tracking(self):
        """Test that parser position is correctly updated."""
        tokens = [
            self._make_token("NUMBER", "1", 1, 1),
            self._make_token("PLUS", "+", 1, 3),
            self._make_token("NUMBER", "2", 1, 5)
        ]
        parser_state = {
            "tokens": tokens,
            "filename": "test.py",
            "pos": 1
        }
        left = {"type": "number", "value": "1", "line": 1, "column": 1}

        with patch("._parse_unary_op_package._parse_unary_op_src._parse_unary_op") as mock_unary:
            mock_unary.return_value = {"type": "number", "value": "2", "line": 1, "column": 5}

            result = _parse_binary_op(parser_state, left, 0)

        # Position should advance past operator and right operand
        self.assertEqual(parser_state["pos"], 3)

    def test_mixed_precedence_complex(self):
        """Test complex expression: 1 + 2 * 3 - 4."""
        tokens = [
            self._make_token("NUMBER", "1", 1, 1),
            self._make_token("PLUS", "+", 1, 3),
            self._make_token("NUMBER", "2", 1, 5),
            self._make_token("STAR", "*", 1, 7),
            self._make_token("NUMBER", "3", 1, 9),
            self._make_token("MINUS", "-", 1, 11),
            self._make_token("NUMBER", "4", 1, 13)
        ]
        parser_state = {
            "tokens": tokens,
            "filename": "test.py",
            "pos": 1  # At PLUS
        }
        left = {"type": "number", "value": "1", "line": 1, "column": 1}

        call_count = [0]

        def mock_unary_side_effect(ps):
            call_count[0] += 1
            if call_count[0] == 1:
                return {"type": "number", "value": "2", "line": 1, "column": 5}
            elif call_count[0] == 2:
                return {"type": "number", "value": "3", "line": 1, "column": 9}
            else:
                return {"type": "number", "value": "4", "line": 1, "column": 13}

        with patch("._parse_unary_op_package._parse_unary_op_src._parse_unary_op", side_effect=mock_unary_side_effect):
            result = _parse_binary_op(parser_state, left, 0)

        # Should be: ((1 + (2 * 3)) - 4)
        # Top level should be -
        self.assertEqual(result["type"], "binary_op")
        self.assertEqual(result["operator"], "-")
        # Right should be 4
        self.assertEqual(result["right"]["value"], "4")
        # Left should be + operation
        self.assertEqual(result["left"]["type"], "binary_op")
        self.assertEqual(result["left"]["operator"], "+")

    def test_all_comparison_operators(self):
        """Test all comparison operators have same precedence."""
        comparison_ops = [
            ("EQ", "=="),
            ("NE", "!="),
            ("LT", "<"),
            ("LE", "<="),
            ("GT", ">"),
            ("GE", ">=")
        ]

        for op_type, op_value in comparison_ops:
            with self.subTest(op_type=op_type):
                tokens = [
                    self._make_token("NUMBER", "1", 1, 1),
                    self._make_token(op_type, op_value, 1, 3),
                    self._make_token("NUMBER", "2", 1, 5)
                ]
                parser_state = {
                    "tokens": tokens,
                    "filename": "test.py",
                    "pos": 1
                }
                left = {"type": "number", "value": "1", "line": 1, "column": 1}

                with patch("._parse_unary_op_package._parse_unary_op_src._parse_unary_op") as mock_unary:
                    mock_unary.return_value = {"type": "number", "value": "2", "line": 1, "column": 5}

                    result = _parse_binary_op(parser_state, left, 0)

                self.assertEqual(result["type"], "binary_op")
                self.assertEqual(result["operator"], op_value)

    def test_modulo_operator(self):
        """Test modulo operator with same precedence as multiply/divide."""
        tokens = [
            self._make_token("NUMBER", "10", 1, 1),
            self._make_token("PERCENT", "%", 1, 3),
            self._make_token("NUMBER", "3", 1, 5)
        ]
        parser_state = {
            "tokens": tokens,
            "filename": "test.py",
            "pos": 1
        }
        left = {"type": "number", "value": "10", "line": 1, "column": 1}

        with patch("._parse_unary_op_package._parse_unary_op_src._parse_unary_op") as mock_unary:
            mock_unary.return_value = {"type": "number", "value": "3", "line": 1, "column": 5}

            result = _parse_binary_op(parser_state, left, 0)

        self.assertEqual(result["type"], "binary_op")
        self.assertEqual(result["operator"], "%")

    def test_division_operator(self):
        """Test division operator."""
        tokens = [
            self._make_token("NUMBER", "10", 1, 1),
            self._make_token("SLASH", "/", 1, 3),
            self._make_token("NUMBER", "2", 1, 5)
        ]
        parser_state = {
            "tokens": tokens,
            "filename": "test.py",
            "pos": 1
        }
        left = {"type": "number", "value": "10", "line": 1, "column": 1}

        with patch("._parse_unary_op_package._parse_unary_op_src._parse_unary_op") as mock_unary:
            mock_unary.return_value = {"type": "number", "value": "2", "line": 1, "column": 5}

            result = _parse_binary_op(parser_state, left, 0)

        self.assertEqual(result["type"], "binary_op")
        self.assertEqual(result["operator"], "/")

    def test_and_operator_precedence(self):
        """Test AND operator has precedence 2 (higher than OR)."""
        tokens = [
            self._make_token("BOOL", "True", 1, 1),
            self._make_token("AND", "and", 1, 6),
            self._make_token("BOOL", "False", 1, 10),
            self._make_token("OR", "or", 1, 16),
            self._make_token("BOOL", "True", 1, 19)
        ]
        parser_state = {
            "tokens": tokens,
            "filename": "test.py",
            "pos": 1  # At AND
        }
        left = {"type": "bool", "value": "True", "line": 1, "column": 1}

        call_count = [0]

        def mock_unary_side_effect(ps):
            call_count[0] += 1
            if call_count[0] == 1:
                return {"type": "bool", "value": "False", "line": 1, "column": 10}
            else:
                return {"type": "bool", "value": "True", "line": 1, "column": 19}

        with patch("._parse_unary_op_package._parse_unary_op_src._parse_unary_op", side_effect=mock_unary_side_effect):
            result = _parse_binary_op(parser_state, left, 0)

        # Should be: (True and False) or True
        # Top level should be OR
        self.assertEqual(result["type"], "binary_op")
        self.assertEqual(result["operator"], "or")
        # Left should be AND operation
        self.assertEqual(result["left"]["type"], "binary_op")
        self.assertEqual(result["left"]["operator"], "and")


if __name__ == "__main__":
    unittest.main()
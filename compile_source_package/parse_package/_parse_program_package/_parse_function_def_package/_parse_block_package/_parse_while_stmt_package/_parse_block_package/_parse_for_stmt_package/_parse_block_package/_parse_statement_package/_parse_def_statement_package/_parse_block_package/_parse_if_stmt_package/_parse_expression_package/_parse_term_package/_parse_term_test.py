import unittest
from unittest.mock import patch

from ._parse_term_src import _parse_term


class TestParseTerm(unittest.TestCase):
    """Test cases for _parse_term function"""

    def test_single_factor_no_operators(self):
        """Test parsing a single factor without any operators"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "42", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }

        def mock_factor_side_effect(state):
            result = {
                "type": "NUMBER",
                "value": 42,
                "line": 1,
                "column": 1
            }
            state["pos"] = 1
            return result

        with patch("._parse_factor_package._parse_factor_src._parse_factor", side_effect=mock_factor_side_effect):
            result = _parse_term(parser_state)

            self.assertEqual(result["type"], "NUMBER")
            self.assertEqual(result["value"], 42)
            self.assertEqual(parser_state["pos"], 1)

    def test_multiplication_operator(self):
        """Test parsing factor * factor"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "10", "line": 1, "column": 1},
                {"type": "MUL", "value": "*", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "5", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.py"
        }

        call_count = [0]

        def mock_factor_side_effect(state):
            call_count[0] += 1
            if call_count[0] == 1:
                result = {"type": "NUMBER", "value": 10, "line": 1, "column": 1}
                state["pos"] = 1
            else:
                result = {"type": "NUMBER", "value": 5, "line": 1, "column": 5}
                state["pos"] = 3
            return result

        with patch("._parse_factor_package._parse_factor_src._parse_factor", side_effect=mock_factor_side_effect):
            result = _parse_term(parser_state)

            self.assertEqual(result["type"], "BINOP")
            self.assertEqual(result["operator"], "*")
            self.assertEqual(len(result["children"]), 2)
            self.assertEqual(parser_state["pos"], 3)

    def test_division_operator(self):
        """Test parsing factor / factor"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "20", "line": 1, "column": 1},
                {"type": "DIV", "value": "/", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "4", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.py"
        }

        call_count = [0]

        def mock_factor_side_effect(state):
            call_count[0] += 1
            if call_count[0] == 1:
                result = {"type": "NUMBER", "value": 20, "line": 1, "column": 1}
                state["pos"] = 1
            else:
                result = {"type": "NUMBER", "value": 4, "line": 1, "column": 5}
                state["pos"] = 3
            return result

        with patch("._parse_factor_package._parse_factor_src._parse_factor", side_effect=mock_factor_side_effect):
            result = _parse_term(parser_state)

            self.assertEqual(result["type"], "BINOP")
            self.assertEqual(result["operator"], "/")
            self.assertEqual(len(result["children"]), 2)
            self.assertEqual(parser_state["pos"], 3)

    def test_left_associative_multiple_operators(self):
        """Test left-associative parsing: factor * factor / factor"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "10", "line": 1, "column": 1},
                {"type": "MUL", "value": "*", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "5", "line": 1, "column": 5},
                {"type": "DIV", "value": "/", "line": 1, "column": 7},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 9}
            ],
            "pos": 0,
            "filename": "test.py"
        }

        call_count = [0]
        factor_values = [10, 5, 2]
        factor_positions = [1, 3, 5]

        def mock_factor_side_effect(state):
            idx = call_count[0]
            call_count[0] += 1
            result = {
                "type": "NUMBER",
                "value": factor_values[idx],
                "line": 1,
                "column": factor_positions[idx] * 2 - 1
            }
            state["pos"] = factor_positions[idx]
            return result

        with patch("._parse_factor_package._parse_factor_src._parse_factor", side_effect=mock_factor_side_effect):
            result = _parse_term(parser_state)

            # Should be left-associative: (10 * 5) / 2
            self.assertEqual(result["type"], "BINOP")
            self.assertEqual(result["operator"], "/")
            self.assertEqual(len(result["children"]), 2)

            # Left child should be the first BINOP (10 * 5)
            left_child = result["children"][0]
            self.assertEqual(left_child["type"], "BINOP")
            self.assertEqual(left_child["operator"], "*")

            # Right child should be the last factor (2)
            right_child = result["children"][1]
            self.assertEqual(right_child["type"], "NUMBER")
            self.assertEqual(right_child["value"], 2)

            self.assertEqual(parser_state["pos"], 5)

    def test_mixed_operators(self):
        """Test parsing with mixed * and / operators"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "8", "line": 1, "column": 1},
                {"type": "MUL", "value": "*", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "3", "line": 1, "column": 5},
                {"type": "DIV", "value": "/", "line": 1, "column": 7},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 9},
                {"type": "MUL", "value": "*", "line": 1, "column": 11},
                {"type": "NUMBER", "value": "4", "line": 1, "column": 13}
            ],
            "pos": 0,
            "filename": "test.py"
        }

        call_count = [0]
        factor_values = [8, 3, 2, 4]
        factor_positions = [1, 3, 5, 7]

        def mock_factor_side_effect(state):
            idx = call_count[0]
            call_count[0] += 1
            result = {
                "type": "NUMBER",
                "value": factor_values[idx],
                "line": 1,
                "column": factor_positions[idx] * 2 - 1
            }
            state["pos"] = factor_positions[idx]
            return result

        with patch("._parse_factor_package._parse_factor_src._parse_factor", side_effect=mock_factor_side_effect):
            result = _parse_term(parser_state)

            # Should be left-associative: ((8 * 3) / 2) * 4
            self.assertEqual(result["type"], "BINOP")
            self.assertEqual(result["operator"], "*")

            # Verify left-associative structure
            left_child = result["children"][0]
            self.assertEqual(left_child["type"], "BINOP")
            self.assertEqual(left_child["operator"], "/")

            self.assertEqual(parser_state["pos"], 7)

    def test_operator_at_end_raises_error(self):
        """Test that operator at end without right factor raises error from _parse_factor"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "10", "line": 1, "column": 1},
                {"type": "MUL", "value": "*", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.py"
        }

        call_count = [0]

        def mock_factor_side_effect(state):
            call_count[0] += 1
            if call_count[0] == 1:
                state["pos"] = 1
                return {"type": "NUMBER", "value": 10, "line": 1, "column": 1}
            else:
                raise SyntaxError("Unexpected end of input")

        with patch("._parse_factor_package._parse_factor_src._parse_factor", side_effect=mock_factor_side_effect):
            with self.assertRaises(SyntaxError):
                _parse_term(parser_state)

    def test_position_updated_correctly(self):
        """Test that parser_state position is updated correctly"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "5", "line": 1, "column": 1},
                {"type": "MUL", "value": "*", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "3", "line": 1, "column": 5},
                {"type": "NUMBER", "value": "2", "line": 1, "column": 7}
            ],
            "pos": 0,
            "filename": "test.py"
        }

        call_count = [0]

        def mock_factor_side_effect(state):
            result = {
                "type": "NUMBER",
                "value": int(state["tokens"][state["pos"]]["value"]),
                "line": state["tokens"][state["pos"]]["line"],
                "column": state["tokens"][state["pos"]]["column"]
            }
            state["pos"] += 1
            call_count[0] += 1
            return result

        with patch("._parse_factor_package._parse_factor_src._parse_factor", side_effect=mock_factor_side_effect):
            result = _parse_term(parser_state)

            # Should stop after consuming 5 * 3, not consume the last NUMBER
            self.assertEqual(parser_state["pos"], 3)
            self.assertEqual(result["type"], "BINOP")
            self.assertEqual(result["operator"], "*")

    def test_binop_node_structure(self):
        """Test that BINOP node has correct structure with all required fields"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "10", "line": 1, "column": 1},
                {"type": "MUL", "value": "*", "line": 1, "column": 3},
                {"type": "NUMBER", "value": "5", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.py"
        }

        call_count = [0]

        def mock_factor_side_effect(state):
            result = {
                "type": "NUMBER",
                "value": int(state["tokens"][state["pos"]]["value"]),
                "line": state["tokens"][state["pos"]]["line"],
                "column": state["tokens"][state["pos"]]["column"]
            }
            state["pos"] += 1
            call_count[0] += 1
            return result

        with patch("._parse_factor_package._parse_factor_src._parse_factor", side_effect=mock_factor_side_effect):
            result = _parse_term(parser_state)

            # Verify BINOP structure
            self.assertIn("type", result)
            self.assertIn("operator", result)
            self.assertIn("children", result)
            self.assertIn("line", result)
            self.assertIn("column", result)

            self.assertEqual(result["type"], "BINOP")
            self.assertEqual(result["operator"], "*")
            self.assertIsInstance(result["children"], list)
            self.assertEqual(len(result["children"]), 2)
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 3)

    def test_ident_factor(self):
        """Test parsing with identifier factors"""
        parser_state = {
            "tokens": [
                {"type": "IDENT", "value": "x", "line": 1, "column": 1},
                {"type": "MUL", "value": "*", "line": 1, "column": 3},
                {"type": "IDENT", "value": "y", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.py"
        }

        call_count = [0]
        ident_values = ["x", "y"]

        def mock_factor_side_effect(state):
            idx = call_count[0]
            call_count[0] += 1
            result = {
                "type": "IDENT",
                "value": ident_values[idx],
                "line": state["tokens"][state["pos"]]["line"],
                "column": state["tokens"][state["pos"]]["column"]
            }
            state["pos"] += 1
            return result

        with patch("._parse_factor_package._parse_factor_src._parse_factor", side_effect=mock_factor_side_effect):
            result = _parse_term(parser_state)

            self.assertEqual(result["type"], "BINOP")
            self.assertEqual(result["operator"], "*")
            self.assertEqual(result["children"][0]["type"], "IDENT")
            self.assertEqual(result["children"][0]["value"], "x")
            self.assertEqual(result["children"][1]["type"], "IDENT")
            self.assertEqual(result["children"][1]["value"], "y")


if __name__ == "__main__":
    unittest.main()

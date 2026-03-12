import unittest
from unittest.mock import Mock

from ._handle_unary_op_src import _handle_unary_op, VarOffsets


class TestHandleUnaryOp(unittest.TestCase):
    """Test cases for _handle_unary_op function."""

    def setUp(self):
        """Set up test fixtures."""
        self.var_offsets: VarOffsets = {"x": 0, "y": 1, "z": 2}
        self.next_offset = 3

    def test_unary_minus_operator(self):
        """Test unary minus operator '-'."""
        operand = {"type": "variable", "name": "x"}
        mock_recurse_fn = Mock(return_value=("LOAD_VAR x\n", 0, 3))

        code, result_offset, updated_offset = _handle_unary_op(
            "-", operand, self.var_offsets, self.next_offset, mock_recurse_fn
        )

        self.assertEqual(code, "LOAD_VAR x\nUNARY_OP -\n")
        self.assertEqual(result_offset, 0)
        self.assertEqual(updated_offset, 3)
        mock_recurse_fn.assert_called_once_with(operand, self.var_offsets, self.next_offset)

    def test_unary_not_operator(self):
        """Test logical not operator 'not'."""
        operand = {"type": "variable", "name": "flag"}
        mock_recurse_fn = Mock(return_value=("LOAD_VAR flag\n", 1, 2))

        code, result_offset, updated_offset = _handle_unary_op(
            "not", operand, self.var_offsets, self.next_offset, mock_recurse_fn
        )

        self.assertEqual(code, "LOAD_VAR flag\nUNARY_OP not\n")
        self.assertEqual(result_offset, 1)
        self.assertEqual(updated_offset, 2)

    def test_unary_bitwise_not_operator(self):
        """Test bitwise not operator '~'."""
        operand = {"type": "literal", "value": 42}
        mock_recurse_fn = Mock(return_value=("LOAD_CONST 42\n", 2, 3))

        code, result_offset, updated_offset = _handle_unary_op(
            "~", operand, self.var_offsets, self.next_offset, mock_recurse_fn
        )

        self.assertEqual(code, "LOAD_CONST 42\nUNARY_OP ~\n")
        self.assertEqual(result_offset, 2)
        self.assertEqual(updated_offset, 3)

    def test_unary_plus_operator(self):
        """Test unary plus operator '+'."""
        operand = {"type": "variable", "name": "y"}
        mock_recurse_fn = Mock(return_value=("LOAD_VAR y\n", 1, 3))

        code, result_offset, updated_offset = _handle_unary_op(
            "+", operand, self.var_offsets, self.next_offset, mock_recurse_fn
        )

        self.assertEqual(code, "LOAD_VAR y\nUNARY_OP +\n")
        self.assertEqual(result_offset, 1)
        self.assertEqual(updated_offset, 3)

    def test_nested_unary_operation(self):
        """Test nested unary operation as operand."""
        operand = {
            "type": "unary_op",
            "operator": "-",
            "operand": {"type": "variable", "name": "x"}
        }
        mock_recurse_fn = Mock(return_value=("LOAD_VAR x\nUNARY_OP -\n", 0, 3))

        code, result_offset, updated_offset = _handle_unary_op(
            "not", operand, self.var_offsets, self.next_offset, mock_recurse_fn
        )

        self.assertEqual(code, "LOAD_VAR x\nUNARY_OP -\nUNARY_OP not\n")
        self.assertEqual(result_offset, 0)
        self.assertEqual(updated_offset, 3)

    def test_binary_op_as_operand(self):
        """Test binary operation as operand."""
        operand = {
            "type": "binary_op",
            "operator": "+",
            "left": {"type": "variable", "name": "x"},
            "right": {"type": "variable", "name": "y"}
        }
        mock_recurse_fn = Mock(return_value=("LOAD_VAR x\nLOAD_VAR y\nBINARY_OP +\n", 0, 3))

        code, result_offset, updated_offset = _handle_unary_op(
            "-", operand, self.var_offsets, self.next_offset, mock_recurse_fn
        )

        self.assertEqual(code, "LOAD_VAR x\nLOAD_VAR y\nBINARY_OP +\nUNARY_OP -\n")
        self.assertEqual(result_offset, 0)
        self.assertEqual(updated_offset, 3)

    def test_zero_offset(self):
        """Test with zero starting offset."""
        operand = {"type": "literal", "value": 0}
        mock_recurse_fn = Mock(return_value=("LOAD_CONST 0\n", 0, 1))

        code, result_offset, updated_offset = _handle_unary_op(
            "-", operand, {}, 0, mock_recurse_fn
        )

        self.assertEqual(code, "LOAD_CONST 0\nUNARY_OP -\n")
        self.assertEqual(result_offset, 0)
        self.assertEqual(updated_offset, 1)

    def test_large_offset(self):
        """Test with large offset value."""
        operand = {"type": "variable", "name": "x"}
        mock_recurse_fn = Mock(return_value=("LOAD_VAR x\n", 100, 101))

        code, result_offset, updated_offset = _handle_unary_op(
            "-", operand, self.var_offsets, 100, mock_recurse_fn
        )

        self.assertEqual(code, "LOAD_VAR x\nUNARY_OP -\n")
        self.assertEqual(result_offset, 100)
        self.assertEqual(updated_offset, 101)

    def test_empty_var_offsets(self):
        """Test with empty variable offsets dictionary."""
        operand = {"type": "literal", "value": 5}
        mock_recurse_fn = Mock(return_value=("LOAD_CONST 5\n", 0, 1))

        code, result_offset, updated_offset = _handle_unary_op(
            "-", operand, {}, 0, mock_recurse_fn
        )

        self.assertEqual(code, "LOAD_CONST 5\nUNARY_OP -\n")
        self.assertEqual(result_offset, 0)
        self.assertEqual(updated_offset, 1)

    def test_recurse_fn_called_with_correct_params(self):
        """Verify recurse_fn receives the correct parameters."""
        operand = {"type": "variable", "name": "x"}
        mock_recurse_fn = Mock(return_value=("LOAD_VAR x\n", 0, 3))

        _handle_unary_op("-", operand, self.var_offsets, self.next_offset, mock_recurse_fn)

        mock_recurse_fn.assert_called_once_with(operand, self.var_offsets, self.next_offset)

    def test_result_offset_matches_operand_offset(self):
        """Verify result offset equals operand's result offset."""
        for expected_offset in [0, 1, 5, 100]:
            mock_recurse_fn = Mock(return_value=("LOAD_VAR x\n", expected_offset, expected_offset + 1))

            _, result_offset, _ = _handle_unary_op(
                "-", {"type": "variable", "name": "x"}, self.var_offsets, 0, mock_recurse_fn
            )

            self.assertEqual(result_offset, expected_offset)

    def test_updated_offset_matches_recurse_fn_output(self):
        """Verify updated offset matches what recurse_fn returns."""
        for next_off in [1, 5, 10, 50]:
            mock_recurse_fn = Mock(return_value=("LOAD_VAR x\n", 0, next_off))

            _, _, updated_offset = _handle_unary_op(
                "-", {"type": "variable", "name": "x"}, self.var_offsets, 0, mock_recurse_fn
            )

            self.assertEqual(updated_offset, next_off)

    def test_multiline_operand_code(self):
        """Test with multiline operand code."""
        operand = {
            "type": "binary_op",
            "operator": "+",
            "left": {"type": "variable", "name": "a"},
            "right": {"type": "variable", "name": "b"}
        }
        mock_recurse_fn = Mock(return_value=(
            "LOAD_VAR a\nLOAD_VAR b\nBINARY_OP +\n", 0, 3
        ))

        code, result_offset, updated_offset = _handle_unary_op(
            "-", operand, self.var_offsets, self.next_offset, mock_recurse_fn
        )

        self.assertEqual(
            code,
            "LOAD_VAR a\nLOAD_VAR b\nBINARY_OP +\nUNARY_OP -\n"
        )
        self.assertEqual(result_offset, 0)
        self.assertEqual(updated_offset, 3)

    def test_call_expression_as_operand(self):
        """Test function call expression as operand."""
        operand = {
            "type": "call",
            "function": "abs",
            "args": [{"type": "variable", "name": "x"}]
        }
        mock_recurse_fn = Mock(return_value=("CALL abs 1\n", 0, 2))

        code, result_offset, updated_offset = _handle_unary_op(
            "-", operand, self.var_offsets, self.next_offset, mock_recurse_fn
        )

        self.assertEqual(code, "CALL abs 1\nUNARY_OP -\n")
        self.assertEqual(result_offset, 0)
        self.assertEqual(updated_offset, 2)


if __name__ == "__main__":
    unittest.main()

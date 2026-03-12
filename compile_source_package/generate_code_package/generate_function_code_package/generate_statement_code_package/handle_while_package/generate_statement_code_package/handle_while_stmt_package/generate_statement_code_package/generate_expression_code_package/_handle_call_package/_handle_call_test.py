# test_handle_call.py
"""Unit tests for _handle_call function."""
import unittest
from unittest.mock import patch
from typing import Dict

from ._handle_call_src import _handle_call


class TestHandleCall(unittest.TestCase):
    """Test cases for _handle_call function."""

    def test_call_with_no_arguments(self):
        """Test function call with no arguments."""
        var_offsets: Dict[str, int] = {"x": 0}
        next_offset = 5

        assembly, result_offset, final_next_offset = _handle_call(
            function="print",
            args=[],
            var_offsets=var_offsets,
            next_offset=next_offset
        )

        self.assertEqual(assembly, "CALL print 0")
        self.assertEqual(result_offset, next_offset)
        self.assertEqual(final_next_offset, next_offset)

    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_stmt_package.generate_statement_code_package.generate_expression_code_package._handle_call_package._handle_call_src.generate_expression_code')
    def test_call_with_single_argument(self, mock_gen_expr):
        """Test function call with one argument."""
        mock_gen_expr.return_value = ("LOAD_CONST 42", 5, 6)

        var_offsets: Dict[str, int] = {"x": 0}
        next_offset = 5

        arg_expr = {"type": "literal", "value": 42}

        assembly, result_offset, final_next_offset = _handle_call(
            function="print",
            args=[arg_expr],
            var_offsets=var_offsets,
            next_offset=next_offset
        )

        self.assertEqual(assembly, "LOAD_CONST 42\nCALL print 1")
        self.assertEqual(result_offset, 5)
        self.assertEqual(final_next_offset, 6)
        mock_gen_expr.assert_called_once_with(arg_expr, var_offsets, next_offset)

    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_stmt_package.generate_statement_code_package.generate_expression_code_package._handle_call_package._handle_call_src.generate_expression_code')
    def test_call_with_multiple_arguments(self, mock_gen_expr):
        """Test function call with multiple arguments - left-to-right evaluation."""
        mock_gen_expr.side_effect = [
            ("LOAD_CONST 1", 5, 6),
            ("LOAD_CONST 2", 6, 7),
            ("LOAD_CONST 3", 7, 8),
        ]

        var_offsets: Dict[str, int] = {"x": 0}
        next_offset = 5

        args = [
            {"type": "literal", "value": 1},
            {"type": "literal", "value": 2},
            {"type": "literal", "value": 3},
        ]

        assembly, result_offset, final_next_offset = _handle_call(
            function="add",
            args=args,
            var_offsets=var_offsets,
            next_offset=next_offset
        )

        expected_assembly = "LOAD_CONST 1\nLOAD_CONST 2\nLOAD_CONST 3\nCALL add 3"
        self.assertEqual(assembly, expected_assembly)
        self.assertEqual(result_offset, 5)
        self.assertEqual(final_next_offset, 8)
        self.assertEqual(mock_gen_expr.call_count, 3)

    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_stmt_package.generate_statement_code_package.generate_expression_code_package._handle_call_package._handle_call_src.generate_expression_code')
    def test_call_with_variable_argument(self, mock_gen_expr):
        """Test function call with variable argument."""
        mock_gen_expr.return_value = ("LOAD_VAR x", 0, 1)

        var_offsets: Dict[str, int] = {"x": 0}
        next_offset = 5

        arg_expr = {"type": "variable", "name": "x"}

        assembly, result_offset, final_next_offset = _handle_call(
            function="print",
            args=[arg_expr],
            var_offsets=var_offsets,
            next_offset=next_offset
        )

        self.assertEqual(assembly, "LOAD_VAR x\nCALL print 1")
        self.assertEqual(result_offset, 0)
        mock_gen_expr.assert_called_once_with(arg_expr, var_offsets, next_offset)

    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_stmt_package.generate_statement_code_package.generate_expression_code_package._handle_call_package._handle_call_src.generate_expression_code')
    def test_call_with_nested_call_argument(self, mock_gen_expr):
        """Test function call with nested function call as argument."""
        mock_gen_expr.return_value = ("CALL inner 0", 5, 6)

        var_offsets: Dict[str, int] = {}
        next_offset = 5

        nested_call = {"type": "call", "function": "inner", "args": []}

        assembly, result_offset, final_next_offset = _handle_call(
            function="outer",
            args=[nested_call],
            var_offsets=var_offsets,
            next_offset=next_offset
        )

        self.assertEqual(assembly, "CALL inner 0\nCALL outer 1")
        self.assertEqual(result_offset, 5)
        self.assertEqual(final_next_offset, 6)

    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_stmt_package.generate_statement_code_package.generate_expression_code_package._handle_call_package._handle_call_src.generate_expression_code')
    def test_call_preserves_evaluation_order(self, mock_gen_expr):
        """Test that arguments are evaluated left-to-right."""
        mock_gen_expr.side_effect = [
            ("ARG1", 5, 6),
            ("ARG2", 6, 7),
            ("ARG3", 7, 8),
        ]

        var_offsets: Dict[str, int] = {}
        next_offset = 5

        args = [
            {"type": "literal", "value": "first"},
            {"type": "literal", "value": "second"},
            {"type": "literal", "value": "third"},
        ]

        _handle_call(
            function="test",
            args=args,
            var_offsets=var_offsets,
            next_offset=next_offset
        )

        calls = mock_gen_expr.call_args_list
        self.assertEqual(len(calls), 3)
        self.assertEqual(calls[0][0][0], args[0])
        self.assertEqual(calls[1][0][0], args[1])
        self.assertEqual(calls[2][0][0], args[2])

    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_stmt_package.generate_statement_code_package.generate_expression_code_package._handle_call_package._handle_call_src.generate_expression_code')
    def test_call_result_offset_is_first_arg_offset(self, mock_gen_expr):
        """Test that result offset is the first argument's offset when args exist."""
        mock_gen_expr.side_effect = [
            ("ARG1", 10, 11),
            ("ARG2", 11, 12),
        ]

        var_offsets: Dict[str, int] = {}
        next_offset = 10

        args = [
            {"type": "literal", "value": 1},
            {"type": "literal", "value": 2},
        ]

        assembly, result_offset, final_next_offset = _handle_call(
            function="test",
            args=args,
            var_offsets=var_offsets,
            next_offset=next_offset
        )

        self.assertEqual(result_offset, 10)

    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_stmt_package.generate_statement_code_package.generate_expression_code_package._handle_call_package._handle_call_src.generate_expression_code')
    def test_call_with_complex_expressions(self, mock_gen_expr):
        """Test function call with complex expression arguments."""
        mock_gen_expr.side_effect = [
            ("BINARY_ADD", 5, 6),
            ("UNARY_NEG", 6, 7),
        ]

        var_offsets: Dict[str, int] = {"x": 0, "y": 1}
        next_offset = 5

        args = [
            {"type": "binary_op", "operator": "+", "left": {"type": "variable", "name": "x"}, "right": {"type": "variable", "name": "y"}},
            {"type": "unary_op", "operator": "-", "operand": {"type": "literal", "value": 5}},
        ]

        assembly, result_offset, final_next_offset = _handle_call(
            function="process",
            args=args,
            var_offsets=var_offsets,
            next_offset=next_offset
        )

        self.assertEqual(assembly, "BINARY_ADD\nUNARY_NEG\nCALL process 2")
        self.assertEqual(result_offset, 5)
        self.assertEqual(final_next_offset, 7)


if __name__ == "__main__":
    unittest.main()

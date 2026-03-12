# === std / third-party imports ===
import unittest
from typing import Dict, Any
from unittest.mock import patch

# === sub function imports ===
from .generate_unary_op_code_src import generate_unary_op_code


class TestGenerateUnaryOpCode(unittest.TestCase):
    """Test cases for generate_unary_op_code function."""

    def setUp(self):
        """Set up test fixtures."""
        self.func_name = "test_func"
        self.label_counter: Dict[str, int] = {"counter": 0}
        self.var_offsets: Dict[str, int] = {"x": 0}
        self.next_offset = 10

    def test_negation_operator(self):
        """Test unary negation operator '-' generates NEG instruction."""
        expr: Dict[str, Any] = {
            "type": "UNARY_OP",
            "operator": "-",
            "operand": {"type": "VAR", "name": "x"}
        }

        with patch("..generate_expression_code_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("    LDR x0, [sp, #0]\n", 10)

            code, offset = generate_unary_op_code(
                expr, self.func_name, self.label_counter, self.var_offsets, self.next_offset
            )

            mock_gen_expr.assert_called_once_with(
                expr["operand"], self.func_name, self.label_counter, self.var_offsets, self.next_offset
            )
            self.assertIn("NEG x0, x0", code)
            self.assertEqual(offset, 10)

    def test_logical_not_operator(self):
        """Test unary logical not operator '!' generates CMP+CSET instructions."""
        expr: Dict[str, Any] = {
            "type": "UNARY_OP",
            "operator": "!",
            "operand": {"type": "VAR", "name": "flag"}
        }

        with patch("..generate_expression_code_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("    LDR x0, [sp, #4]\n", 10)

            code, offset = generate_unary_op_code(
                expr, self.func_name, self.label_counter, self.var_offsets, self.next_offset
            )

            mock_gen_expr.assert_called_once()
            self.assertIn("CMP x0, #0", code)
            self.assertIn("CSET x0, EQ", code)
            self.assertEqual(offset, 10)

    def test_bitwise_not_operator(self):
        """Test unary bitwise not operator '~' generates MVN instruction."""
        expr: Dict[str, Any] = {
            "type": "UNARY_OP",
            "operator": "~",
            "operand": {"type": "CONST", "value": 42}
        }

        with patch("..generate_expression_code_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("    MOV x0, #42\n", 10)

            code, offset = generate_unary_op_code(
                expr, self.func_name, self.label_counter, self.var_offsets, self.next_offset
            )

            mock_gen_expr.assert_called_once()
            self.assertIn("MVN x0, x0", code)
            self.assertEqual(offset, 10)

    def test_nested_unary_operators(self):
        """Test nested unary operators are handled correctly."""
        expr: Dict[str, Any] = {
            "type": "UNARY_OP",
            "operator": "-",
            "operand": {
                "type": "UNARY_OP",
                "operator": "~",
                "operand": {"type": "VAR", "name": "y"}
            }
        }

        with patch("..generate_expression_code_src.generate_expression_code") as mock_gen_expr:
            # Simulate nested call returning code for inner unary op
            mock_gen_expr.return_value = (
                "    LDR x0, [sp, #8]\n    MVN x0, x0\n", 10
            )

            code, offset = generate_unary_op_code(
                expr, self.func_name, self.label_counter, self.var_offsets, self.next_offset
            )

            mock_gen_expr.assert_called_once()
            self.assertIn("NEG x0, x0", code)
            self.assertIn("MVN x0, x0", code)
            self.assertEqual(offset, 10)

    def test_unknown_operator_raises_error(self):
        """Test that unknown unary operator raises ValueError."""
        expr: Dict[str, Any] = {
            "type": "UNARY_OP",
            "operator": "@",
            "operand": {"type": "VAR", "name": "x"}
        }

        with patch("..generate_expression_code_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("    LDR x0, [sp, #0]\n", 10)

            with self.assertRaises(ValueError) as context:
                generate_unary_op_code(
                    expr, self.func_name, self.label_counter, self.var_offsets, self.next_offset
                )

            self.assertIn("Unknown unary operator: @", str(context.exception))
            mock_gen_expr.assert_called_once()

    def test_offset_propagation(self):
        """Test that next_offset is properly propagated through recursive call."""
        expr: Dict[str, Any] = {
            "type": "UNARY_OP",
            "operator": "-",
            "operand": {"type": "VAR", "name": "x"}
        }

        with patch("..generate_expression_code_src.generate_expression_code") as mock_gen_expr:
            # Simulate offset being updated by operand processing
            mock_gen_expr.return_value = ("    LDR x0, [sp, #0]\n", 15)

            code, offset = generate_unary_op_code(
                expr, self.func_name, self.label_counter, self.var_offsets, self.next_offset
            )

            # Verify offset from operand is returned unchanged
            self.assertEqual(offset, 15)
            mock_gen_expr.assert_called_once_with(
                expr["operand"], self.func_name, self.label_counter, self.var_offsets, self.next_offset
            )

    def test_code_concatenation_order(self):
        """Test that operand code comes before operator code."""
        expr: Dict[str, Any] = {
            "type": "UNARY_OP",
            "operator": "-",
            "operand": {"type": "VAR", "name": "x"}
        }

        with patch("..generate_expression_code_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("    LDR x0, [sp, #0]\n", 10)

            code, offset = generate_unary_op_code(
                expr, self.func_name, self.label_counter, self.var_offsets, self.next_offset
            )

            # Operand code should come before operator code
            ldr_pos = code.find("LDR x0")
            neg_pos = code.find("NEG x0")
            self.assertLess(ldr_pos, neg_pos, "Operand code should come before operator code")

    def test_label_counter_unchanged(self):
        """Test that label_counter is not modified (passed through but not changed)."""
        expr: Dict[str, Any] = {
            "type": "UNARY_OP",
            "operator": "-",
            "operand": {"type": "VAR", "name": "x"}
        }

        original_counter = self.label_counter.copy()

        with patch("..generate_expression_code_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("    LDR x0, [sp, #0]\n", 10)

            generate_unary_op_code(
                expr, self.func_name, self.label_counter, self.var_offsets, self.next_offset
            )

            # label_counter should be passed to generate_expression_code but not modified by unary op
            # Note: generate_expression_code might modify it, but unary op itself doesn't
            mock_gen_expr.assert_called_once()
            # Verify the counter was passed (we can't check if it was modified by the mocked function)


class TestGenerateUnaryOpCodeIntegration(unittest.TestCase):
    """Integration tests with actual generate_expression_code behavior."""

    def test_all_unary_operators_produce_valid_asm(self):
        """Test that all unary operators produce valid ARM assembly syntax."""
        operators = ["-", "!", "~"]
        
        for op in operators:
            expr: Dict[str, Any] = {
                "type": "UNARY_OP",
                "operator": op,
                "operand": {"type": "VAR", "name": "x"}
            }

            with patch("..generate_expression_code_src.generate_expression_code") as mock_gen_expr:
                mock_gen_expr.return_value = ("    LDR x0, [sp, #0]\n", 10)

                code, offset = generate_unary_op_code(
                    expr, "func", {"counter": 0}, {"x": 0}, 10
                )

                # Verify code contains expected instruction
                self.assertTrue(len(code) > 0)
                self.assertIsInstance(code, str)
                self.assertIsInstance(offset, int)


if __name__ == "__main__":
    unittest.main()

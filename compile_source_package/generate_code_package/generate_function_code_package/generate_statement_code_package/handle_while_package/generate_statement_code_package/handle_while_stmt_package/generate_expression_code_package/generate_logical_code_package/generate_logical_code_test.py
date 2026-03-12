# === std / third-party imports ===
import unittest
from typing import Dict, Any
from unittest.mock import patch, MagicMock

# === sub function imports ===
from .generate_logical_code_src import generate_logical_code


class TestGenerateLogicalCode(unittest.TestCase):
    """Test cases for generate_logical_code function."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.var_offsets: Dict[str, int] = {"x": 0, "y": 8}
        self.next_offset: int = 16
        self.label_counter: int = 0
        
        # Sample expression nodes
        self.left_expr: Dict[str, Any] = {
            "type": "var",
            "var_name": "x"
        }
        self.right_expr: Dict[str, Any] = {
            "type": "var",
            "var_name": "y"
        }

    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_stmt_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code')
    def test_generate_and_code(self, mock_gen_expr: MagicMock) -> None:
        """Test AND logical operation code generation."""
        # Mock generate_expression_code to return simple code
        mock_gen_expr.side_effect = [
            ("    mov x0, #1\n", 24, 0),  # left operand
            ("    mov x0, #1\n", 32, 0),  # right operand
        ]
        
        code, updated_offset, updated_label_counter = generate_logical_code(
            self.left_expr,
            self.right_expr,
            "and",
            self.var_offsets,
            self.next_offset,
            self.label_counter
        )
        
        # Verify code contains expected AND branching structure
        self.assertIn("cbz x0, L_and_0", code)
        self.assertIn("b L_and_end_0", code)
        self.assertIn("L_and_0:", code)
        self.assertIn("L_and_end_0:", code)
        self.assertIn("mov x0, #0", code)  # false section
        
        # Verify offset and label counter updates
        self.assertEqual(updated_label_counter, 1)
        
        # Verify generate_expression_code was called twice (left and right)
        self.assertEqual(mock_gen_expr.call_count, 2)

    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_stmt_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code')
    def test_generate_or_code(self, mock_gen_expr: MagicMock) -> None:
        """Test OR logical operation code generation."""
        # Mock generate_expression_code to return simple code
        mock_gen_expr.side_effect = [
            ("    mov x0, #0\n", 24, 0),  # left operand
            ("    mov x0, #1\n", 32, 0),  # right operand
        ]
        
        code, updated_offset, updated_label_counter = generate_logical_code(
            self.left_expr,
            self.right_expr,
            "or",
            self.var_offsets,
            self.next_offset,
            self.label_counter
        )
        
        # Verify code contains expected OR branching structure
        self.assertIn("cbnz x0, L_or_0", code)
        self.assertIn("b L_or_end_0", code)
        self.assertIn("L_or_0:", code)
        self.assertIn("L_or_end_0:", code)
        self.assertIn("mov x0, #1", code)  # true section
        
        # Verify offset and label counter updates
        self.assertEqual(updated_label_counter, 1)
        
        # Verify generate_expression_code was called twice (left and right)
        self.assertEqual(mock_gen_expr.call_count, 2)

    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_stmt_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code')
    def test_generate_and_code_with_higher_label_counter(self, mock_gen_expr: MagicMock) -> None:
        """Test AND code generation with non-zero label counter."""
        mock_gen_expr.side_effect = [
            ("    ldr x0, [x19, #0]\n", 24, 0),
            ("    ldr x0, [x19, #8]\n", 32, 0),
        ]
        
        code, updated_offset, updated_label_counter = generate_logical_code(
            self.left_expr,
            self.right_expr,
            "and",
            self.var_offsets,
            self.next_offset,
            5  # Starting label counter
        )
        
        # Verify labels use the correct counter value
        self.assertIn("cbz x0, L_and_5", code)
        self.assertIn("b L_and_end_5", code)
        self.assertIn("L_and_5:", code)
        self.assertIn("L_and_end_5:", code)
        
        # Verify label counter is incremented
        self.assertEqual(updated_label_counter, 6)

    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_stmt_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code')
    def test_generate_or_code_with_higher_label_counter(self, mock_gen_expr: MagicMock) -> None:
        """Test OR code generation with non-zero label counter."""
        mock_gen_expr.side_effect = [
            ("    ldr x0, [x19, #0]\n", 24, 0),
            ("    ldr x0, [x19, #8]\n", 32, 0),
        ]
        
        code, updated_offset, updated_label_counter = generate_logical_code(
            self.left_expr,
            self.right_expr,
            "or",
            self.var_offsets,
            self.next_offset,
            10  # Starting label counter
        )
        
        # Verify labels use the correct counter value
        self.assertIn("cbnz x0, L_or_10", code)
        self.assertIn("b L_or_end_10", code)
        self.assertIn("L_or_10:", code)
        self.assertIn("L_or_end_10:", code)
        
        # Verify label counter is incremented
        self.assertEqual(updated_label_counter, 11)

    def test_invalid_operator_raises_value_error(self) -> None:
        """Test that invalid operator raises ValueError."""
        with self.assertRaises(ValueError) as context:
            generate_logical_code(
                self.left_expr,
                self.right_expr,
                "xor",  # Invalid operator
                self.var_offsets,
                self.next_offset,
                self.label_counter
            )
        
        self.assertIn("Unknown logical operator: xor", str(context.exception))

    def test_invalid_operator_not_raises(self) -> None:
        """Test that another invalid operator also raises ValueError."""
        with self.assertRaises(ValueError) as context:
            generate_logical_code(
                self.left_expr,
                self.right_expr,
                "not",  # Invalid operator
                self.var_offsets,
                self.next_offset,
                self.label_counter
            )
        
        self.assertIn("Unknown logical operator: not", str(context.exception))

    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_stmt_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code')
    def test_and_code_order_left_then_right(self, mock_gen_expr: MagicMock) -> None:
        """Test that AND code evaluates left operand before right operand."""
        mock_gen_expr.side_effect = [
            ("    ; left\n", 24, 0),
            ("    ; right\n", 32, 0),
        ]
        
        code, _, _ = generate_logical_code(
            self.left_expr,
            self.right_expr,
            "and",
            self.var_offsets,
            self.next_offset,
            self.label_counter
        )
        
        # Verify left code comes before branch
        left_pos = code.find("; left")
        branch_pos = code.find("cbz x0")
        right_pos = code.find("; right")
        
        self.assertLess(left_pos, branch_pos)
        self.assertLess(branch_pos, right_pos)

    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_stmt_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code')
    def test_or_code_order_left_then_right(self, mock_gen_expr: MagicMock) -> None:
        """Test that OR code evaluates left operand before right operand."""
        mock_gen_expr.side_effect = [
            ("    ; left\n", 24, 0),
            ("    ; right\n", 32, 0),
        ]
        
        code, _, _ = generate_logical_code(
            self.left_expr,
            self.right_expr,
            "or",
            self.var_offsets,
            self.next_offset,
            self.label_counter
        )
        
        # Verify left code comes before branch
        left_pos = code.find("; left")
        branch_pos = code.find("cbnz x0")
        right_pos = code.find("; right")
        
        self.assertLess(left_pos, branch_pos)
        self.assertLess(branch_pos, right_pos)

    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_stmt_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code')
    def test_and_short_circuit_structure(self, mock_gen_expr: MagicMock) -> None:
        """Test AND short-circuit structure: branch on false, skip right."""
        mock_gen_expr.side_effect = [
            ("    mov x0, #1\n", 24, 0),
            ("    mov x0, #1\n", 32, 0),
        ]
        
        code, _, _ = generate_logical_code(
            self.left_expr,
            self.right_expr,
            "and",
            self.var_offsets,
            self.next_offset,
            self.label_counter
        )
        
        # AND: cbz (branch if zero/false) to skip right operand evaluation
        self.assertIn("cbz x0", code)
        
        # Should have false section that sets result to 0
        self.assertIn("mov x0, #0", code)

    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_stmt_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code')
    def test_or_short_circuit_structure(self, mock_gen_expr: MagicMock) -> None:
        """Test OR short-circuit structure: branch on true, skip right."""
        mock_gen_expr.side_effect = [
            ("    mov x0, #1\n", 24, 0),
            ("    mov x0, #0\n", 32, 0),
        ]
        
        code, _, _ = generate_logical_code(
            self.left_expr,
            self.right_expr,
            "or",
            self.var_offsets,
            self.next_offset,
            self.label_counter
        )
        
        # OR: cbnz (branch if non-zero/true) to skip right operand evaluation
        self.assertIn("cbnz x0", code)
        
        # Should have true section that sets result to 1
        self.assertIn("mov x0, #1", code)

    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_stmt_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code')
    def test_empty_var_offsets(self, mock_gen_expr: MagicMock) -> None:
        """Test code generation with empty var_offsets."""
        mock_gen_expr.side_effect = [
            ("    mov x0, #1\n", 24, 0),
            ("    mov x0, #1\n", 32, 0),
        ]
        
        code, updated_offset, updated_label_counter = generate_logical_code(
            self.left_expr,
            self.right_expr,
            "and",
            {},  # Empty var_offsets
            self.next_offset,
            self.label_counter
        )
        
        # Should still generate valid code
        self.assertIn("cbz x0", code)
        self.assertEqual(updated_label_counter, 1)

    @patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_while_package.generate_statement_code_package.handle_while_stmt_package.generate_expression_code_package.generate_expression_code_src.generate_expression_code')
    def test_nested_expression_nodes(self, mock_gen_expr: MagicMock) -> None:
        """Test with nested expression nodes."""
        nested_left: Dict[str, Any] = {
            "type": "binary",
            "operator": "+",
            "left": {"type": "var", "var_name": "a"},
            "right": {"type": "const", "value": 1}
        }
        nested_right: Dict[str, Any] = {
            "type": "binary",
            "operator": "-",
            "left": {"type": "var", "var_name": "b"},
            "right": {"type": "const", "value": 2}
        }
        
        mock_gen_expr.side_effect = [
            ("    add x0, x1, x2\n", 24, 0),
            ("    sub x0, x3, x4\n", 32, 0),
        ]
        
        code, updated_offset, updated_label_counter = generate_logical_code(
            nested_left,
            nested_right,
            "and",
            self.var_offsets,
            self.next_offset,
            self.label_counter
        )
        
        # Should generate valid AND code regardless of expression complexity
        self.assertIn("cbz x0", code)
        self.assertIn("b L_and_end_0", code)
        self.assertEqual(updated_label_counter, 1)


if __name__ == "__main__":
    unittest.main()

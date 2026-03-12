# -*- coding: utf-8 -*-
"""Unit tests for handle_if function."""

from typing import Dict, Any
from unittest.mock import patch

from .handle_if_src import handle_if


class TestHandleIf:
    """Test cases for handle_if function."""

    def test_handle_if_with_then_and_else_bodies(self):
        """Test IF statement with both then_body and else_body."""
        stmt = {
            "type": "if",
            "condition": {"type": "binary", "op": ">", "left": {"type": "var", "name": "x"}, "right": {"type": "lit", "value": 0}},
            "then_body": [{"type": "assign", "var": "y", "expr": {"type": "lit", "value": 1}}],
            "else_body": [{"type": "assign", "var": "y", "expr": {"type": "lit", "value": -1}}],
        }
        func_name = "test_func"
        label_counter: Dict[str, int] = {"if_else": 0, "if_end": 0}
        var_offsets: Dict[str, int] = {"x": 0, "y": 1}
        next_offset = 2

        with patch("handle_if_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("LDR R0, [SP, #0]\nCMP R0, #0", "R0", 3)
            with patch("handle_if_src.generate_statement_code") as mock_gen_stmt:
                mock_gen_stmt.side_effect = [
                    ("STR R1, [SP, #1]", 4),
                    ("STR R2, [SP, #1]", 5),
                ]

                asm_code, offset = handle_if(stmt, func_name, label_counter, var_offsets, next_offset)

        # Verify label counter was mutated
        assert label_counter["if_else"] == 1
        assert label_counter["if_end"] == 1

        # Verify assembly structure
        assert "test_func_if_else_0:" in asm_code
        assert "test_func_if_end_0:" in asm_code
        assert "CMP R0, #0" in asm_code
        assert "B.EQ test_func_if_else_0" in asm_code
        assert "B test_func_if_end_0" in asm_code

        # Verify offset propagation
        assert offset == 5

        # Verify mock calls
        assert mock_gen_expr.call_count == 1
        assert mock_gen_stmt.call_count == 2

    def test_handle_if_with_empty_else_body(self):
        """Test IF statement with empty else_body."""
        stmt = {
            "type": "if",
            "condition": {"type": "lit", "value": 1},
            "then_body": [{"type": "assign", "var": "a", "expr": {"type": "lit", "value": 10}}],
            "else_body": [],
        }
        func_name = "my_func"
        label_counter: Dict[str, int] = {"if_else": 5, "if_end": 3}
        var_offsets: Dict[str, int] = {"a": 0}
        next_offset = 1

        with patch("handle_if_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("MOV R0, #1", "R0", 1)
            with patch("handle_if_src.generate_statement_code") as mock_gen_stmt:
                mock_gen_stmt.return_value = ("STR R0, [SP, #0]", 2)

                asm_code, offset = handle_if(stmt, func_name, label_counter, var_offsets, next_offset)

        # Verify label counter was mutated
        assert label_counter["if_else"] == 6
        assert label_counter["if_end"] == 4

        # Verify labels use correct numbers
        assert "my_func_if_else_5:" in asm_code
        assert "my_func_if_end_3:" in asm_code

        # Verify else_label exists but no else body statements
        assert "my_func_if_else_5:" in asm_code
        assert asm_code.count("STR R0, [SP, #0]") == 1  # Only then_body statement

        assert offset == 2

    def test_handle_if_with_empty_then_body(self):
        """Test IF statement with empty then_body."""
        stmt = {
            "type": "if",
            "condition": {"type": "lit", "value": 0},
            "then_body": [],
            "else_body": [{"type": "assign", "var": "b", "expr": {"type": "lit", "value": 20}}],
        }
        func_name = "func"
        label_counter: Dict[str, int] = {"if_else": 0, "if_end": 0}
        var_offsets: Dict[str, int] = {"b": 0}
        next_offset = 1

        with patch("handle_if_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("MOV R0, #0", "R0", 1)
            with patch("handle_if_src.generate_statement_code") as mock_gen_stmt:
                mock_gen_stmt.return_value = ("STR R0, [SP, #0]", 2)

                asm_code, offset = handle_if(stmt, func_name, label_counter, var_offsets, next_offset)

        # Verify label counter was mutated
        assert label_counter["if_else"] == 1
        assert label_counter["if_end"] == 1

        # Verify B instruction after then_body (even if empty)
        assert "B func_if_end_0" in asm_code
        assert "func_if_else_0:" in asm_code

        assert offset == 2

    def test_handle_if_with_multiple_then_statements(self):
        """Test IF statement with multiple statements in then_body."""
        stmt = {
            "type": "if",
            "condition": {"type": "binary", "op": "==", "left": {"type": "var", "name": "x"}, "right": {"type": "lit", "value": 5}},
            "then_body": [
                {"type": "assign", "var": "a", "expr": {"type": "lit", "value": 1}},
                {"type": "assign", "var": "b", "expr": {"type": "lit", "value": 2}},
                {"type": "assign", "var": "c", "expr": {"type": "lit", "value": 3}},
            ],
            "else_body": [],
        }
        func_name = "multi_stmt"
        label_counter: Dict[str, int] = {"if_else": 0, "if_end": 0}
        var_offsets: Dict[str, int] = {"x": 0, "a": 1, "b": 2, "c": 3}
        next_offset = 4

        with patch("handle_if_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("LDR R0, [SP, #0]", "R0", 5)
            with patch("handle_if_src.generate_statement_code") as mock_gen_stmt:
                mock_gen_stmt.side_effect = [
                    ("STR R1, [SP, #1]", 6),
                    ("STR R2, [SP, #2]", 7),
                    ("STR R3, [SP, #3]", 8),
                ]

                asm_code, offset = handle_if(stmt, func_name, label_counter, var_offsets, next_offset)

        assert mock_gen_stmt.call_count == 3
        assert offset == 8

    def test_handle_if_with_multiple_else_statements(self):
        """Test IF statement with multiple statements in else_body."""
        stmt = {
            "type": "if",
            "condition": {"type": "lit", "value": 0},
            "then_body": [],
            "else_body": [
                {"type": "assign", "var": "p", "expr": {"type": "lit", "value": 100}},
                {"type": "assign", "var": "q", "expr": {"type": "lit", "value": 200}},
            ],
        }
        func_name = "else_multi"
        label_counter: Dict[str, int] = {"if_else": 0, "if_end": 0}
        var_offsets: Dict[str, int] = {"p": 0, "q": 1}
        next_offset = 2

        with patch("handle_if_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("MOV R0, #0", "R0", 2)
            with patch("handle_if_src.generate_statement_code") as mock_gen_stmt:
                mock_gen_stmt.side_effect = [
                    ("STR R1, [SP, #0]", 3),
                    ("STR R2, [SP, #1]", 4),
                ]

                asm_code, offset = handle_if(stmt, func_name, label_counter, var_offsets, next_offset)

        assert mock_gen_stmt.call_count == 2
        assert offset == 4

    def test_handle_if_label_counter_mutation(self):
        """Test that label_counter is properly mutated with read-then-increment pattern."""
        stmt = {
            "type": "if",
            "condition": {"type": "lit", "value": 1},
            "then_body": [],
            "else_body": [],
        }
        func_name = "label_test"
        label_counter: Dict[str, int] = {"if_else": 10, "if_end": 20}
        var_offsets: Dict[str, int] = {}
        next_offset = 0

        with patch("handle_if_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("MOV R0, #1", "R0", 0)
            with patch("handle_if_src.generate_statement_code") as mock_gen_stmt:
                mock_gen_stmt.return_value = ("", 0)

                handle_if(stmt, func_name, label_counter, var_offsets, next_offset)

        # Verify read-then-increment: used 10, then set to 11; used 20, then set to 21
        assert label_counter["if_else"] == 11
        assert label_counter["if_end"] == 21

    def test_handle_if_missing_label_counter_keys(self):
        """Test handle_if when label_counter is missing expected keys."""
        stmt = {
            "type": "if",
            "condition": {"type": "lit", "value": 1},
            "then_body": [],
            "else_body": [],
        }
        func_name = "missing_keys"
        label_counter: Dict[str, int] = {}  # Empty, missing keys
        var_offsets: Dict[str, int] = {}
        next_offset = 0

        with patch("handle_if_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("MOV R0, #1", "R0", 0)
            with patch("handle_if_src.generate_statement_code") as mock_gen_stmt:
                mock_gen_stmt.return_value = ("", 0)

                asm_code, offset = handle_if(stmt, func_name, label_counter, var_offsets, next_offset)

        # Should default to 0 when keys are missing
        assert label_counter["if_else"] == 1
        assert label_counter["if_end"] == 1
        assert "missing_keys_if_else_0:" in asm_code
        assert "missing_keys_if_end_0:" in asm_code

    def test_handle_if_offset_propagation(self):
        """Test that offset is properly propagated through all operations."""
        stmt = {
            "type": "if",
            "condition": {"type": "lit", "value": 1},
            "then_body": [{"type": "assign", "var": "x", "expr": {"type": "lit", "value": 1}}],
            "else_body": [{"type": "assign", "var": "y", "expr": {"type": "lit", "value": 2}}],
        }
        func_name = "offset_test"
        label_counter: Dict[str, int] = {"if_else": 0, "if_end": 0}
        var_offsets: Dict[str, int] = {"x": 0, "y": 1}
        next_offset = 10

        with patch("handle_if_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("MOV R0, #1", "R0", 15)  # offset increases by 5
            with patch("handle_if_src.generate_statement_code") as mock_gen_stmt:
                mock_gen_stmt.side_effect = [
                    ("STR R1, [SP, #0]", 20),  # offset increases by 5
                    ("STR R2, [SP, #1]", 25),  # offset increases by 5
                ]

                asm_code, offset = handle_if(stmt, func_name, label_counter, var_offsets, next_offset)

        # Final offset should be 25 (10 -> 15 -> 20 -> 25)
        assert offset == 25

    def test_handle_if_default_empty_bodies(self):
        """Test handle_if when then_body or else_body keys are missing from stmt."""
        stmt: Dict[str, Any] = {
            "type": "if",
            "condition": {"type": "lit", "value": 1},
            # Missing then_body and else_body keys
        }
        func_name = "default_test"
        label_counter: Dict[str, int] = {"if_else": 0, "if_end": 0}
        var_offsets: Dict[str, int] = {}
        next_offset = 0

        with patch("handle_if_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("MOV R0, #1", "R0", 0)
            with patch("handle_if_src.generate_statement_code") as mock_gen_stmt:
                mock_gen_stmt.return_value = ("", 0)

                asm_code, offset = handle_if(stmt, func_name, label_counter, var_offsets, next_offset)

        # Should handle missing keys gracefully
        assert "default_if_else_0:" in asm_code
        assert "default_if_end_0:" in asm_code
        assert mock_gen_stmt.call_count == 0  # No statements to process

    def test_handle_if_default_missing_condition(self):
        """Test handle_if when condition key is missing from stmt."""
        stmt: Dict[str, Any] = {
            "type": "if",
            "then_body": [],
            "else_body": [],
            # Missing condition key
        }
        func_name = "no_cond"
        label_counter: Dict[str, int] = {"if_else": 0, "if_end": 0}
        var_offsets: Dict[str, int] = {}
        next_offset = 0

        with patch("handle_if_src.generate_expression_code") as mock_gen_expr:
            mock_gen_expr.return_value = ("", "R0", 0)
            with patch("handle_if_src.generate_statement_code") as mock_gen_stmt:
                mock_gen_stmt.return_value = ("", 0)

                asm_code, offset = handle_if(stmt, func_name, label_counter, var_offsets, next_offset)

        # Should handle missing condition gracefully (defaults to empty dict)
        assert mock_gen_expr.call_count == 1
        # Called with empty dict as condition
        mock_gen_expr.assert_called_with({}, var_offsets, next_offset)

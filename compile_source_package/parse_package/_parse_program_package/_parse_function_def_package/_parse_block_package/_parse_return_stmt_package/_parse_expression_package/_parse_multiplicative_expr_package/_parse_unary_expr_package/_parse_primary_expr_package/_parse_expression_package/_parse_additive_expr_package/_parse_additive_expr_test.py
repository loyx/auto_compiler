# === std / third-party imports ===
import unittest
from unittest.mock import patch
from typing import Dict, Any

# === relative imports ===
from ._parse_additive_expr_src import _parse_additive_expr

# === type aliases (matching source) ===
Token = Dict[str, Any]
AST = Dict[str, Any]
ParserState = Dict[str, Any]


class TestParseAdditiveExpr(unittest.TestCase):
    """Test cases for _parse_additive_expr function."""

    def _create_token(self, token_type: str, value: str, line: int = 1, column: int = 1) -> Token:
        """Helper to create a token dict."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def _create_ast_node(self, node_type: str, value: Any = None, 
                         children: list = None, line: int = 1, column: int = 1) -> AST:
        """Helper to create an AST node dict."""
        return {
            "type": node_type,
            "value": value,
            "children": children if children is not None else [],
            "line": line,
            "column": column
        }

    def test_single_multiplicative_expr_no_additive_operator(self):
        """Test parsing when there's no additive operator - should return single operand."""
        left_operand = self._create_ast_node("NUMBER", value=42, line=1, column=1)
        
        parser_state: ParserState = {
            "tokens": [self._create_token("NUMBER", "42")],
            "pos": 0,
            "filename": "test.cc",
            "error": ""
        }
        
        with patch("._parse_additive_expr_package._parse_multiplicative_expr_package._parse_multiplicative_expr_src._parse_multiplicative_expr") as mock_parse_mult:
            mock_parse_mult.return_value = left_operand
            
            result = _parse_additive_expr(parser_state)
            
            # Should return the single operand unchanged
            self.assertEqual(result, left_operand)
            # Should have called _parse_multiplicative_expr once
            mock_parse_mult.assert_called_once_with(parser_state)
            # Position should remain after first operand
            self.assertEqual(parser_state["pos"], 0)

    def test_single_addition_operator(self):
        """Test parsing a simple addition: a + b."""
        left_operand = self._create_ast_node("NUMBER", value=10, line=1, column=1)
        right_operand = self._create_ast_node("NUMBER", value=20, line=1, column=5)
        add_token = self._create_token("OPERATOR", "+", line=1, column=3)
        
        parser_state: ParserState = {
            "tokens": [
                self._create_token("NUMBER", "10", line=1, column=1),
                add_token,
                self._create_token("NUMBER", "20", line=1, column=5)
            ],
            "pos": 0,
            "filename": "test.cc",
            "error": ""
        }
        
        call_count = [0]
        def mock_parse_mult_side_effect(state):
            call_count[0] += 1
            if call_count[0] == 1:
                return left_operand
            else:
                return right_operand
        
        with patch("._parse_additive_expr_package._parse_multiplicative_expr_package._parse_multiplicative_expr_src._parse_multiplicative_expr") as mock_parse_mult:
            mock_parse_mult.side_effect = mock_parse_mult_side_effect
            
            result = _parse_additive_expr(parser_state)
            
            # Should build a BINARY_OP node
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["operator"], "+")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 3)
            self.assertEqual(len(result["children"]), 2)
            self.assertEqual(result["children"][0], left_operand)
            self.assertEqual(result["children"][1], right_operand)
            # Position should advance past the operator and right operand
            self.assertEqual(parser_state["pos"], 2)
            # Should have called _parse_multiplicative_expr twice
            self.assertEqual(mock_parse_mult.call_count, 2)

    def test_single_subtraction_operator(self):
        """Test parsing a simple subtraction: a - b."""
        left_operand = self._create_ast_node("NUMBER", value=100, line=1, column=1)
        right_operand = self._create_ast_node("NUMBER", value=50, line=1, column=5)
        sub_token = self._create_token("OPERATOR", "-", line=1, column=3)
        
        parser_state: ParserState = {
            "tokens": [
                self._create_token("NUMBER", "100", line=1, column=1),
                sub_token,
                self._create_token("NUMBER", "50", line=1, column=5)
            ],
            "pos": 0,
            "filename": "test.cc",
            "error": ""
        }
        
        call_count = [0]
        def mock_parse_mult_side_effect(state):
            call_count[0] += 1
            if call_count[0] == 1:
                return left_operand
            else:
                return right_operand
        
        with patch("._parse_additive_expr_package._parse_multiplicative_expr_package._parse_multiplicative_expr_src._parse_multiplicative_expr") as mock_parse_mult:
            mock_parse_mult.side_effect = mock_parse_mult_side_effect
            
            result = _parse_additive_expr(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["operator"], "-")
            self.assertEqual(result["children"][0], left_operand)
            self.assertEqual(result["children"][1], right_operand)

    def test_left_associativity_multiple_additions(self):
        """Test left-associativity: a + b + c should be ((a + b) + c)."""
        operand_a = self._create_ast_node("NUMBER", value=1, line=1, column=1)
        operand_b = self._create_ast_node("NUMBER", value=2, line=1, column=5)
        operand_c = self._create_ast_node("NUMBER", value=3, line=1, column=9)
        add_token1 = self._create_token("OPERATOR", "+", line=1, column=3)
        add_token2 = self._create_token("OPERATOR", "+", line=1, column=7)
        
        parser_state: ParserState = {
            "tokens": [
                self._create_token("NUMBER", "1", line=1, column=1),
                add_token1,
                self._create_token("NUMBER", "2", line=1, column=5),
                add_token2,
                self._create_token("NUMBER", "3", line=1, column=9)
            ],
            "pos": 0,
            "filename": "test.cc",
            "error": ""
        }
        
        call_count = [0]
        def mock_parse_mult_side_effect(state):
            call_count[0] += 1
            if call_count[0] == 1:
                return operand_a
            elif call_count[0] == 2:
                return operand_b
            else:
                return operand_c
        
        with patch("._parse_additive_expr_package._parse_multiplicative_expr_package._parse_multiplicative_expr_src._parse_multiplicative_expr") as mock_parse_mult:
            mock_parse_mult.side_effect = mock_parse_mult_side_effect
            
            result = _parse_additive_expr(parser_state)
            
            # Should be left-associative: ((a + b) + c)
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["operator"], "+")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 7)  # Second operator
            
            # Left child should be (a + b)
            left_child = result["children"][0]
            self.assertEqual(left_child["type"], "BINARY_OP")
            self.assertEqual(left_child["operator"], "+")
            self.assertEqual(left_child["line"], 1)
            self.assertEqual(left_child["column"], 3)  # First operator
            self.assertEqual(left_child["children"][0], operand_a)
            self.assertEqual(left_child["children"][1], operand_b)
            
            # Right child should be c
            self.assertEqual(result["children"][1], operand_c)

    def test_mixed_addition_and_subtraction(self):
        """Test mixed operators: a + b - c."""
        operand_a = self._create_ast_node("NUMBER", value=10, line=1, column=1)
        operand_b = self._create_ast_node("NUMBER", value=20, line=1, column=5)
        operand_c = self._create_ast_node("NUMBER", value=30, line=1, column=9)
        add_token = self._create_token("OPERATOR", "+", line=1, column=3)
        sub_token = self._create_token("OPERATOR", "-", line=1, column=7)
        
        parser_state: ParserState = {
            "tokens": [
                self._create_token("NUMBER", "10", line=1, column=1),
                add_token,
                self._create_token("NUMBER", "20", line=1, column=5),
                sub_token,
                self._create_token("NUMBER", "30", line=1, column=9)
            ],
            "pos": 0,
            "filename": "test.cc",
            "error": ""
        }
        
        call_count = [0]
        def mock_parse_mult_side_effect(state):
            call_count[0] += 1
            if call_count[0] == 1:
                return operand_a
            elif call_count[0] == 2:
                return operand_b
            else:
                return operand_c
        
        with patch("._parse_additive_expr_package._parse_multiplicative_expr_package._parse_multiplicative_expr_src._parse_multiplicative_expr") as mock_parse_mult:
            mock_parse_mult.side_effect = mock_parse_mult_side_effect
            
            result = _parse_additive_expr(parser_state)
            
            # Should be left-associative: ((a + b) - c)
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["operator"], "-")
            self.assertEqual(result["column"], 7)
            
            left_child = result["children"][0]
            self.assertEqual(left_child["operator"], "+")
            self.assertEqual(left_child["column"], 3)

    def test_non_operator_token_stops_parsing(self):
        """Test that non-operator tokens stop additive parsing."""
        left_operand = self._create_ast_node("NUMBER", value=42, line=1, column=1)
        right_operand = self._create_ast_node("NUMBER", value=100, line=1, column=5)
        
        parser_state: ParserState = {
            "tokens": [
                self._create_token("NUMBER", "42", line=1, column=1),
                self._create_token("SEMICOLON", ";", line=1, column=3),
                self._create_token("NUMBER", "100", line=1, column=5)
            ],
            "pos": 0,
            "filename": "test.cc",
            "error": ""
        }
        
        with patch("._parse_additive_expr_package._parse_multiplicative_expr_package._parse_multiplicative_expr_src._parse_multiplicative_expr") as mock_parse_mult:
            mock_parse_mult.return_value = left_operand
            
            result = _parse_additive_expr(parser_state)
            
            # Should return just the left operand, not consume the semicolon
            self.assertEqual(result, left_operand)
            mock_parse_mult.assert_called_once_with(parser_state)
            self.assertEqual(parser_state["pos"], 0)

    def test_other_operator_type_stops_parsing(self):
        """Test that non-additive operators (like *) stop additive parsing."""
        left_operand = self._create_ast_node("NUMBER", value=10, line=1, column=1)
        
        parser_state: ParserState = {
            "tokens": [
                self._create_token("NUMBER", "10", line=1, column=1),
                self._create_token("OPERATOR", "*", line=1, column=3),
                self._create_token("NUMBER", "5", line=1, column=5)
            ],
            "pos": 0,
            "filename": "test.cc",
            "error": ""
        }
        
        with patch("._parse_additive_expr_package._parse_multiplicative_expr_package._parse_multiplicative_expr_src._parse_multiplicative_expr") as mock_parse_mult:
            mock_parse_mult.return_value = left_operand
            
            result = _parse_additive_expr(parser_state)
            
            # Should not consume the * operator
            self.assertEqual(result, left_operand)
            self.assertEqual(parser_state["pos"], 0)

    def test_end_of_tokens_after_operator(self):
        """Test behavior when tokens end after an additive operator."""
        left_operand = self._create_ast_node("NUMBER", value=10, line=1, column=1)
        add_token = self._create_token("OPERATOR", "+", line=1, column=3)
        
        parser_state: ParserState = {
            "tokens": [
                self._create_token("NUMBER", "10", line=1, column=1),
                add_token
            ],
            "pos": 0,
            "filename": "test.cc",
            "error": ""
        }
        
        call_count = [0]
        def mock_parse_mult_side_effect(state):
            call_count[0] += 1
            if call_count[0] == 1:
                return left_operand
            else:
                # When called for right operand at end of tokens
                return self._create_ast_node("EMPTY", line=1, column=3)
        
        with patch("._parse_additive_expr_package._parse_multiplicative_expr_package._parse_multiplicative_expr_src._parse_multiplicative_expr") as mock_parse_mult:
            mock_parse_mult.side_effect = mock_parse_mult_side_effect
            
            result = _parse_additive_expr(parser_state)
            
            # Should still build the BINARY_OP node
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["operator"], "+")
            self.assertEqual(mock_parse_mult.call_count, 2)

    def test_position_advances_correctly(self):
        """Test that parser_state position advances correctly through multiple operators."""
        operand_a = self._create_ast_node("NUMBER", value=1, line=1, column=1)
        operand_b = self._create_ast_node("NUMBER", value=2, line=1, column=5)
        operand_c = self._create_ast_node("NUMBER", value=3, line=1, column=9)
        
        parser_state: ParserState = {
            "tokens": [
                self._create_token("NUMBER", "1", line=1, column=1),
                self._create_token("OPERATOR", "+", line=1, column=3),
                self._create_token("NUMBER", "2", line=1, column=5),
                self._create_token("OPERATOR", "-", line=1, column=7),
                self._create_token("NUMBER", "3", line=1, column=9)
            ],
            "pos": 0,
            "filename": "test.cc",
            "error": ""
        }
        
        call_count = [0]
        def mock_parse_mult_side_effect(state):
            call_count[0] += 1
            if call_count[0] == 1:
                return operand_a
            elif call_count[0] == 2:
                return operand_b
            else:
                return operand_c
        
        with patch("._parse_additive_expr_package._parse_multiplicative_expr_package._parse_multiplicative_expr_src._parse_multiplicative_expr") as mock_parse_mult:
            mock_parse_mult.side_effect = mock_parse_mult_side_effect
            
            result = _parse_additive_expr(parser_state)
            
            # Position should be at the end (after all tokens consumed)
            self.assertEqual(parser_state["pos"], 5)

    def test_starting_position_not_zero(self):
        """Test parsing when starting from a non-zero position."""
        left_operand = self._create_ast_node("NUMBER", value=42, line=2, column=1)
        right_operand = self._create_ast_node("NUMBER", value=100, line=2, column=5)
        
        parser_state: ParserState = {
            "tokens": [
                self._create_token("NUMBER", "10", line=1, column=1),
                self._create_token("NUMBER", "42", line=2, column=1),
                self._create_token("OPERATOR", "+", line=2, column=3),
                self._create_token("NUMBER", "100", line=2, column=5)
            ],
            "pos": 1,  # Start from second token
            "filename": "test.cc",
            "error": ""
        }
        
        call_count = [0]
        def mock_parse_mult_side_effect(state):
            call_count[0] += 1
            if call_count[0] == 1:
                return left_operand
            else:
                return right_operand
        
        with patch("._parse_additive_expr_package._parse_multiplicative_expr_package._parse_multiplicative_expr_src._parse_multiplicative_expr") as mock_parse_mult:
            mock_parse_mult.side_effect = mock_parse_mult_side_effect
            
            result = _parse_additive_expr(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["operator"], "+")
            # Position should advance from 1 to 3
            self.assertEqual(parser_state["pos"], 3)


if __name__ == "__main__":
    unittest.main()

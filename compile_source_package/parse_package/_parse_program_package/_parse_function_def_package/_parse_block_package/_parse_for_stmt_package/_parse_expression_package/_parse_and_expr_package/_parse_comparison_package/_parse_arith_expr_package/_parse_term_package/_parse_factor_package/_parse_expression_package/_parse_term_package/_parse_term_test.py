#!/usr/bin/env python3
"""Unit tests for _parse_term function."""

import unittest
from unittest.mock import patch, MagicMock
from typing import Dict, Any

# Mock the dependencies before importing _parse_term to prevent circular import issues
import sys

# Get the current package prefix
_current_package = __package__ or ''

# Create mock modules for the circular dependency chain
def _create_mock_module(module_path: str, return_func=None):
    """Create and register a mock module."""
    mock_module = MagicMock()
    if return_func:
        mock_module._parse_factor = return_func
    else:
        mock_module._parse_factor = MagicMock(return_value={"type": "ERROR", "value": "Mocked", "children": [], "line": 0, "column": 0})
    mock_module._parse_expression = MagicMock(return_value={"type": "ERROR", "value": "Mocked", "children": [], "line": 0, "column": 0})
    mock_module._parse_term = MagicMock(return_value={"type": "ERROR", "value": "Mocked", "children": [], "line": 0, "column": 0})
    sys.modules[module_path] = mock_module
    return mock_module

# Create a mock factory that can be configured later
class MockFactorFactory:
    def __init__(self):
        self.side_effect = None
        self.return_value = None
        self.call_count = 0
        self.calls = []
    
    def __call__(self, parser_state):
        self.call_count += 1
        self.calls.append(parser_state)
        if self.side_effect:
            if callable(self.side_effect):
                return self.side_effect(parser_state)
            elif isinstance(self.side_effect, list) and self.call_count <= len(self.side_effect):
                return self.side_effect[self.call_count - 1]
            else:
                return {"type": "ERROR", "value": "No more side effects", "children": [], "line": 0, "column": 0}
        elif self.return_value:
            return self.return_value
        else:
            return {"type": "ERROR", "value": "Mocked", "children": [], "line": 0, "column": 0}

# Create a shared mock factory
_mock_factor_factory = MockFactorFactory()

# Mock the entire circular dependency chain using relative paths
_factor_src_path = f'{_current_package}._parse_factor_package._parse_factor_src'
_expression_src_path = f'{_current_package}._parse_factor_package._parse_expression_package._parse_expression_src'
_term_src_path = f'{_current_package}._parse_term_src'

# Remove any existing modules to ensure clean import
for mod_path in [_factor_src_path, _expression_src_path, _term_src_path]:
    if mod_path in sys.modules:
        del sys.modules[mod_path]

# Also remove parent packages that might cache imports
_parent_pkg = f'{_current_package}._parse_factor_package'
if _parent_pkg in sys.modules:
    del sys.modules[_parent_pkg]

_create_mock_module(_factor_src_path, _mock_factor_factory)
_create_mock_module(_expression_src_path)

# Relative import for the function under test
from ._parse_term_src import _parse_term

# Type aliases for clarity
Token = Dict[str, Any]
AST = Dict[str, Any]
ParserState = Dict[str, Any]

# Type aliases for clarity
Token = Dict[str, Any]
AST = Dict[str, Any]
ParserState = Dict[str, Any]


class TestParseTerm(unittest.TestCase):
    """Test cases for _parse_term function."""

    def setUp(self):
        """Set up test fixtures."""
        self.maxDiff = None
        # Reset the mock factory before each test
        _mock_factor_factory.call_count = 0
        _mock_factor_factory.calls = []
        _mock_factor_factory.side_effect = None
        _mock_factor_factory.return_value = None

    def _create_token(self, token_type: str, value: str, line: int = 1, column: int = 1) -> Token:
        """Helper to create a token dict."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def _create_parser_state(self, tokens: list, pos: int = 0, filename: str = "test.py") -> ParserState:
        """Helper to create a parser state dict."""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename
        }

    def _create_ast_node(self, node_type: str, value: Any = None, children: list = None,
                         line: int = 0, column: int = 0) -> AST:
        """Helper to create an AST node dict."""
        return {
            "type": node_type,
            "value": value,
            "children": children if children is not None else [],
            "line": line,
            "column": column
        }

    def _setup_factor_mock(self, return_value=None, side_effect=None):
        """Helper to configure the _parse_factor mock."""
        _mock_factor_factory.return_value = return_value
        _mock_factor_factory.side_effect = side_effect
        return _mock_factor_factory

    # ==================== Happy Path Tests ====================

    def test_single_factor_no_operators(self):
        """Test parsing a single factor without any operators."""
        tokens = [self._create_token("IDENTIFIER", "x")]
        parser_state = self._create_parser_state(tokens)

        mock_factor_result = self._create_ast_node("IDENTIFIER", "x", line=1, column=1)

        mock_factory = self._setup_factor_mock(return_value=mock_factor_result)
        result = _parse_term(parser_state)

        self.assertEqual(result["type"], "IDENTIFIER")
        self.assertEqual(result["value"], "x")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(mock_factory.call_count, 1)
        self.assertEqual(parser_state["pos"], 1)

    def test_two_factors_with_multiply(self):
        """Test parsing two factors with MULTI operator."""
        tokens = [
            self._create_token("IDENTIFIER", "x", column=1),
            self._create_token("MULTI", "*", column=3),
            self._create_token("IDENTIFIER", "y", column=5)
        ]
        parser_state = self._create_parser_state(tokens)

        factor_results = [
            self._create_ast_node("IDENTIFIER", "x", line=1, column=1),
            self._create_ast_node("IDENTIFIER", "y", line=1, column=5)
        ]

        mock_factory = self._setup_factor_mock(side_effect=factor_results)
        result = _parse_term(parser_state)

        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "*")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 3)
        self.assertEqual(len(result["children"]), 2)
        self.assertEqual(result["children"][0]["type"], "IDENTIFIER")
        self.assertEqual(result["children"][0]["value"], "x")
        self.assertEqual(result["children"][1]["type"], "IDENTIFIER")
        self.assertEqual(result["children"][1]["value"], "y")
        self.assertEqual(mock_factory.call_count, 2)
        self.assertEqual(parser_state["pos"], 3)

    def test_two_factors_with_divide(self):
        """Test parsing two factors with DIV operator."""
        tokens = [
            self._create_token("LITERAL", "10", column=1),
            self._create_token("DIV", "/", column=4),
            self._create_token("LITERAL", "2", column=6)
        ]
        parser_state = self._create_parser_state(tokens)

        factor_results = [
            self._create_ast_node("LITERAL", "10", line=1, column=1),
            self._create_ast_node("LITERAL", "2", line=1, column=6)
        ]

        mock_factory = self._setup_factor_mock(side_effect=factor_results)
        result = _parse_term(parser_state)

        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "/")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 4)
        self.assertEqual(len(result["children"]), 2)
        self.assertEqual(mock_factory.call_count, 2)
        self.assertEqual(parser_state["pos"], 3)

    def test_two_factors_with_modulo(self):
        """Test parsing two factors with MOD operator."""
        tokens = [
            self._create_token("IDENTIFIER", "a", column=1),
            self._create_token("MOD", "%", column=3),
            self._create_token("IDENTIFIER", "b", column=5)
        ]
        parser_state = self._create_parser_state(tokens)

        factor_results = [
            self._create_ast_node("IDENTIFIER", "a", line=1, column=1),
            self._create_ast_node("IDENTIFIER", "b", line=1, column=5)
        ]

        mock_factory = self._setup_factor_mock(side_effect=factor_results)
        result = _parse_term(parser_state)

        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "%")
        self.assertEqual(mock_factory.call_count, 2)
        self.assertEqual(parser_state["pos"], 3)

    def test_multiple_factors_left_associative(self):
        """Test parsing multiple factors with left associativity: a * b / c."""
        tokens = [
            self._create_token("IDENTIFIER", "a", column=1),
            self._create_token("MULTI", "*", column=3),
            self._create_token("IDENTIFIER", "b", column=5),
            self._create_token("DIV", "/", column=7),
            self._create_token("IDENTIFIER", "c", column=9)
        ]
        parser_state = self._create_parser_state(tokens)

        factor_results = [
            self._create_ast_node("IDENTIFIER", "a", line=1, column=1),
            self._create_ast_node("IDENTIFIER", "b", line=1, column=5),
            self._create_ast_node("IDENTIFIER", "c", line=1, column=9)
        ]

        mock_factory = self._setup_factor_mock(side_effect=factor_results)
        result = _parse_term(parser_state)

        # Should be left associative: (a * b) / c
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "/")
        self.assertEqual(len(result["children"]), 2)

        # Left child should be (a * b)
        left_child = result["children"][0]
        self.assertEqual(left_child["type"], "BINARY_OP")
        self.assertEqual(left_child["value"], "*")
        self.assertEqual(left_child["children"][0]["value"], "a")
        self.assertEqual(left_child["children"][1]["value"], "b")

        # Right child should be c
        right_child = result["children"][1]
        self.assertEqual(right_child["type"], "IDENTIFIER")
        self.assertEqual(right_child["value"], "c")

        self.assertEqual(mock_factory.call_count, 3)
        self.assertEqual(parser_state["pos"], 5)

    def test_mixed_operators(self):
        """Test parsing with mixed operators: a * b % c / d."""
        tokens = [
            self._create_token("IDENTIFIER", "a", column=1),
            self._create_token("MULTI", "*", column=3),
            self._create_token("IDENTIFIER", "b", column=5),
            self._create_token("MOD", "%", column=7),
            self._create_token("IDENTIFIER", "c", column=9),
            self._create_token("DIV", "/", column=11),
            self._create_token("IDENTIFIER", "d", column=13)
        ]
        parser_state = self._create_parser_state(tokens)

        factor_results = [
            self._create_ast_node("IDENTIFIER", "a", line=1, column=1),
            self._create_ast_node("IDENTIFIER", "b", line=1, column=5),
            self._create_ast_node("IDENTIFIER", "c", line=1, column=9),
            self._create_ast_node("IDENTIFIER", "d", line=1, column=13)
        ]

        mock_factory = self._setup_factor_mock(side_effect=factor_results)
        result = _parse_term(parser_state)

        # Should be left associative: ((a * b) % c) / d
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "/")

        # Verify left associativity
        left_child = result["children"][0]
        self.assertEqual(left_child["type"], "BINARY_OP")
        self.assertEqual(left_child["value"], "%")

        left_left = left_child["children"][0]
        self.assertEqual(left_left["type"], "BINARY_OP")
        self.assertEqual(left_left["value"], "*")

        self.assertEqual(mock_factory.call_count, 4)
        self.assertEqual(parser_state["pos"], 7)

    # ==================== Boundary Value Tests ====================

    def test_empty_tokens(self):
        """Test parsing when tokens list is empty."""
        tokens = []
        parser_state = self._create_parser_state(tokens, pos=0)

        result = _parse_term(parser_state)

        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], "Unexpected end of input")
        self.assertEqual(parser_state.get("error"), "Unexpected end of input in term")
        self.assertEqual(parser_state["pos"], 0)

    def test_pos_at_end_of_tokens(self):
        """Test parsing when pos is already at end of tokens."""
        tokens = [self._create_token("IDENTIFIER", "x")]
        parser_state = self._create_parser_state(tokens, pos=1)

        result = _parse_term(parser_state)

        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], "Unexpected end of input")
        self.assertEqual(parser_state.get("error"), "Unexpected end of input in term")

    def test_pos_beyond_tokens(self):
        """Test parsing when pos is beyond tokens length."""
        tokens = [self._create_token("IDENTIFIER", "x")]
        parser_state = self._create_parser_state(tokens, pos=5)

        result = _parse_term(parser_state)

        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], "Unexpected end of input")
        self.assertEqual(parser_state.get("error"), "Unexpected end of input in term")

    def test_single_token_only(self):
        """Test parsing with only one token (single factor)."""
        tokens = [self._create_token("LITERAL", "42", column=1)]
        parser_state = self._create_parser_state(tokens)

        mock_factor_result = self._create_ast_node("LITERAL", "42", line=1, column=1)

        mock_factory = self._setup_factor_mock(return_value=mock_factor_result)
        result = _parse_term(parser_state)

        self.assertEqual(result["type"], "LITERAL")
        self.assertEqual(result["value"], "42")
        self.assertEqual(mock_factory.call_count, 1)
        self.assertEqual(parser_state["pos"], 1)

    # ==================== Error Propagation Tests ====================

    def test_first_factor_error(self):
        """Test error propagation when first factor parsing fails."""
        tokens = [self._create_token("IDENTIFIER", "x")]
        parser_state = self._create_parser_state(tokens)

        error_ast = self._create_ast_node("ERROR", "Factor parse error", line=1, column=1)

        def set_error(state):
            state["error"] = "Factor parse error"
            return error_ast

        mock_factory = self._setup_factor_mock(side_effect=set_error)
        result = _parse_term(parser_state)

        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(parser_state.get("error"), "Factor parse error")
        self.assertEqual(mock_factory.call_count, 1)

    def test_second_factor_error(self):
        """Test error propagation when second factor parsing fails."""
        tokens = [
            self._create_token("IDENTIFIER", "a", column=1),
            self._create_token("MULTI", "*", column=3),
            self._create_token("IDENTIFIER", "b", column=5)
        ]
        parser_state = self._create_parser_state(tokens)

        first_factor = self._create_ast_node("IDENTIFIER", "a", line=1, column=1)
        error_factor = self._create_ast_node("ERROR", "Second factor error", line=1, column=5)

        call_count = [0]

        def mock_factor_side_effect(state):
            call_count[0] += 1
            if call_count[0] == 1:
                return first_factor
            else:
                state["error"] = "Second factor error"
                return error_factor

        mock_factory = self._setup_factor_mock(side_effect=mock_factor_side_effect)
        result = _parse_term(parser_state)

        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], "Second factor error")
        self.assertEqual(parser_state.get("error"), "Second factor error")
        self.assertEqual(mock_factory.call_count, 2)

    def test_error_in_middle_of_chain(self):
        """Test error propagation in middle of operator chain."""
        tokens = [
            self._create_token("IDENTIFIER", "a", column=1),
            self._create_token("MULTI", "*", column=3),
            self._create_token("IDENTIFIER", "b", column=5),
            self._create_token("DIV", "/", column=7),
            self._create_token("IDENTIFIER", "c", column=9)
        ]
        parser_state = self._create_parser_state(tokens)

        factor_results = [
            self._create_ast_node("IDENTIFIER", "a", line=1, column=1),
            self._create_ast_node("IDENTIFIER", "b", line=1, column=5),
        ]
        error_result = self._create_ast_node("ERROR", "Third factor error", line=1, column=9)

        call_count = [0]

        def mock_factor_side_effect(state):
            call_count[0] += 1
            if call_count[0] <= 2:
                return factor_results[call_count[0] - 1]
            else:
                state["error"] = "Third factor error"
                return error_result

        mock_factory = self._setup_factor_mock(side_effect=mock_factor_side_effect)
        result = _parse_term(parser_state)

        # Should have built (a * b) before error
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(parser_state.get("error"), "Third factor error")
        self.assertEqual(mock_factory.call_count, 3)

    # ==================== Multi-Branch Logic Tests ====================

    def test_non_operator_stops_loop(self):
        """Test that non-operator token stops the operator loop."""
        tokens = [
            self._create_token("IDENTIFIER", "a", column=1),
            self._create_token("MULTI", "*", column=3),
            self._create_token("IDENTIFIER", "b", column=5),
            self._create_token("PLUS", "+", column=7),  # PLUS is not a term operator
            self._create_token("IDENTIFIER", "c", column=9)
        ]
        parser_state = self._create_parser_state(tokens)

        factor_results = [
            self._create_ast_node("IDENTIFIER", "a", line=1, column=1),
            self._create_ast_node("IDENTIFIER", "b", line=1, column=5)
        ]

        mock_factory = self._setup_factor_mock(side_effect=factor_results)
        result = _parse_term(parser_state)

        # Should only parse a * b, stopping at PLUS
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "*")
        self.assertEqual(mock_factory.call_count, 2)
        self.assertEqual(parser_state["pos"], 3)  # Should stop before PLUS

    def test_different_line_numbers(self):
        """Test parsing tokens on different lines."""
        tokens = [
            self._create_token("IDENTIFIER", "x", line=1, column=1),
            self._create_token("MULTI", "*", line=2, column=1),
            self._create_token("IDENTIFIER", "y", line=3, column=1)
        ]
        parser_state = self._create_parser_state(tokens)

        factor_results = [
            self._create_ast_node("IDENTIFIER", "x", line=1, column=1),
            self._create_ast_node("IDENTIFIER", "y", line=3, column=1)
        ]

        mock_factory = self._setup_factor_mock(side_effect=factor_results)
        result = _parse_term(parser_state)

        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "*")
        self.assertEqual(result["line"], 2)  # Operator line
        self.assertEqual(result["column"], 1)
        self.assertEqual(mock_factory.call_count, 2)

    # ==================== State Change Tests ====================

    def test_pos_updates_correctly(self):
        """Test that parser_state['pos'] updates correctly through parsing."""
        tokens = [
            self._create_token("IDENTIFIER", "a", column=1),
            self._create_token("MULTI", "*", column=3),
            self._create_token("IDENTIFIER", "b", column=5),
            self._create_token("DIV", "/", column=7),
            self._create_token("IDENTIFIER", "c", column=9)
        ]
        parser_state = self._create_parser_state(tokens)

        factor_results = [
            self._create_ast_node("IDENTIFIER", "a", line=1, column=1),
            self._create_ast_node("IDENTIFIER", "b", line=1, column=5),
            self._create_ast_node("IDENTIFIER", "c", line=1, column=9)
        ]

        mock_factory = self._setup_factor_mock(side_effect=factor_results)
        result = _parse_term(parser_state)

        # Should consume all 5 tokens
        self.assertEqual(parser_state["pos"], 5)

    def test_no_error_set_on_success(self):
        """Test that error is not set on successful parsing."""
        tokens = [
            self._create_token("IDENTIFIER", "x", column=1),
            self._create_token("MULTI", "*", column=3),
            self._create_token("IDENTIFIER", "y", column=5)
        ]
        parser_state = self._create_parser_state(tokens)

        factor_results = [
            self._create_ast_node("IDENTIFIER", "x", line=1, column=1),
            self._create_ast_node("IDENTIFIER", "y", line=1, column=5)
        ]

        mock_factory = self._setup_factor_mock(side_effect=factor_results)
        result = _parse_term(parser_state)

        self.assertNotIn("error", parser_state)
        self.assertEqual(result["type"], "BINARY_OP")

    # ==================== Additional Edge Cases ====================

    def test_consecutive_same_operators(self):
        """Test parsing with consecutive same operators: a * b * c * d."""
        tokens = [
            self._create_token("IDENTIFIER", "a", column=1),
            self._create_token("MULTI", "*", column=3),
            self._create_token("IDENTIFIER", "b", column=5),
            self._create_token("MULTI", "*", column=7),
            self._create_token("IDENTIFIER", "c", column=9),
            self._create_token("MULTI", "*", column=11),
            self._create_token("IDENTIFIER", "d", column=13)
        ]
        parser_state = self._create_parser_state(tokens)

        factor_results = [
            self._create_ast_node("IDENTIFIER", "a", line=1, column=1),
            self._create_ast_node("IDENTIFIER", "b", line=1, column=5),
            self._create_ast_node("IDENTIFIER", "c", line=1, column=9),
            self._create_ast_node("IDENTIFIER", "d", line=1, column=13)
        ]

        mock_factory = self._setup_factor_mock(side_effect=factor_results)
        result = _parse_term(parser_state)

        # Should be left associative: ((a * b) * c) * d
        self.assertEqual(result["type"], "BINARY_OP")
        self.assertEqual(result["value"], "*")
        self.assertEqual(mock_factory.call_count, 4)
        self.assertEqual(parser_state["pos"], 7)

    def test_token_missing_type_field(self):
        """Test handling of token without type field."""
        tokens = [
            {"value": "x", "line": 1, "column": 1},  # Missing type
            self._create_token("MULTI", "*", column=3),
            self._create_token("IDENTIFIER", "y", column=5)
        ]
        parser_state = self._create_parser_state(tokens)

        factor_results = [
            self._create_ast_node("IDENTIFIER", "x", line=1, column=1),
            self._create_ast_node("IDENTIFIER", "y", line=1, column=5)
        ]

        with patch("._parse_term_src._parse_factor", side_effect=factor_results) as mock_parse_factor:
            result = _parse_term(parser_state)

        # Should handle gracefully (type defaults to empty string, not in operator list)
        self.assertEqual(result["type"], "IDENTIFIER")
        mock_parse_factor.assert_called_once()


if __name__ == "__main__":
    unittest.main()

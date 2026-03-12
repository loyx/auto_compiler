#!/usr/bin/env python3
"""Unit tests for _parse_logical function."""

import unittest
from unittest.mock import patch, MagicMock
from typing import Dict, Any
import sys

# Define the base path for the package
BASE_PATH = 'main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_if_stmt_package._parse_block_package._parse_return_stmt_package._parse_expression_package._parse_primary_package._parse_expression_package._parse_logical_package'

# Mock the entire import chain before importing _parse_logical
# This prevents the import chain from failing due to missing sub-packages

# Create mock modules for the entire dependency chain
_parse_additive_mock = MagicMock()
_parse_additive_src_mock = MagicMock(_parse_additive=_parse_additive_mock)
_parse_additive_package_mock = MagicMock()
_parse_additive_package_mock._parse_additive_src = _parse_additive_src_mock

_parse_comparison_mock = MagicMock()
_parse_comparison_src_mock = MagicMock(_parse_comparison=_parse_comparison_mock)
_parse_comparison_package_mock = MagicMock()
_parse_comparison_package_mock._parse_comparison_src = _parse_comparison_src_mock

# Register mocks in sys.modules with absolute paths
mock_modules = {
    f'{BASE_PATH}._parse_comparison_package': _parse_comparison_package_mock,
    f'{BASE_PATH}._parse_comparison_package._parse_comparison_src': _parse_comparison_src_mock,
    f'{BASE_PATH}._parse_comparison_package._parse_additive_package': _parse_additive_package_mock,
    f'{BASE_PATH}._parse_comparison_package._parse_additive_package._parse_additive_src': _parse_additive_src_mock,
}

for name, mock_module in mock_modules.items():
    sys.modules[name] = mock_module

# Now import _parse_logical
from ._parse_logical_src import _parse_logical


class TestParseLogical(unittest.TestCase):
    """Test cases for _parse_logical function."""

    def _create_token(self, token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """Helper to create a token dict."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }

    def _create_ast_node(self, node_type: str, value: Any = None, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """Helper to create an AST node dict."""
        node = {
            "type": node_type,
            "line": line,
            "column": column
        }
        if value is not None:
            node["value"] = value
        return node

    def test_no_logical_operator(self):
        """Test parsing expression without logical operators."""
        parser_state = {
            "tokens": [self._create_token("NUMBER", "42")],
            "pos": 0,
            "filename": "test.py"
        }
        
        mock_comparison_ast = self._create_ast_node("Literal", 42)
        
        with patch(f"{BASE_PATH}._parse_logical_src._parse_comparison", return_value=mock_comparison_ast) as mock_parse_comp:
            result = _parse_logical(parser_state)
            
            self.assertEqual(result, mock_comparison_ast)
            mock_parse_comp.assert_called_once_with(parser_state)
            self.assertEqual(parser_state["pos"], 0)

    def test_single_and_operator(self):
        """Test parsing expression with single AND operator."""
        parser_state = {
            "tokens": [
                self._create_token("NUMBER", "1", line=1, column=1),
                self._create_token("KEYWORD", "AND", line=1, column=3),
                self._create_token("NUMBER", "0", line=1, column=7)
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        left_ast = self._create_ast_node("Literal", 1, line=1, column=1)
        right_ast = self._create_ast_node("Literal", 0, line=1, column=7)
        
        with patch(f"{BASE_PATH}._parse_logical_src._parse_comparison", side_effect=[left_ast, right_ast]) as mock_parse_comp:
            result = _parse_logical(parser_state)
            
            self.assertEqual(result["type"], "BinaryOp")
            self.assertEqual(result["op"], "AND")
            self.assertEqual(result["left"], left_ast)
            self.assertEqual(result["right"], right_ast)
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 3)
            self.assertEqual(parser_state["pos"], 3)
            self.assertEqual(mock_parse_comp.call_count, 2)

    def test_single_or_operator(self):
        """Test parsing expression with single OR operator."""
        parser_state = {
            "tokens": [
                self._create_token("NUMBER", "1", line=2, column=1),
                self._create_token("KEYWORD", "OR", line=2, column=3),
                self._create_token("NUMBER", "0", line=2, column=6)
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        left_ast = self._create_ast_node("Literal", 1, line=2, column=1)
        right_ast = self._create_ast_node("Literal", 0, line=2, column=6)
        
        with patch(f"{BASE_PATH}._parse_logical_src._parse_comparison", side_effect=[left_ast, right_ast]) as mock_parse_comp:
            result = _parse_logical(parser_state)
            
            self.assertEqual(result["type"], "BinaryOp")
            self.assertEqual(result["op"], "OR")
            self.assertEqual(result["left"], left_ast)
            self.assertEqual(result["right"], right_ast)
            self.assertEqual(result["line"], 2)
            self.assertEqual(result["column"], 3)
            self.assertEqual(parser_state["pos"], 3)

    def test_multiple_logical_operators_left_associative(self):
        """Test left-associativity of multiple logical operators."""
        parser_state = {
            "tokens": [
                self._create_token("NUMBER", "1", line=1, column=1),
                self._create_token("KEYWORD", "AND", line=1, column=3),
                self._create_token("NUMBER", "2", line=1, column=7),
                self._create_token("KEYWORD", "OR", line=1, column=9),
                self._create_token("NUMBER", "3", line=1, column=12)
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        ast1 = self._create_ast_node("Literal", 1, line=1, column=1)
        ast2 = self._create_ast_node("Literal", 2, line=1, column=7)
        ast3 = self._create_ast_node("Literal", 3, line=1, column=12)
        
        with patch(f"{BASE_PATH}._parse_logical_src._parse_comparison", side_effect=[ast1, ast2, ast3]) as mock_parse_comp:
            result = _parse_logical(parser_state)
            
            # Should be: (1 AND 2) OR 3
            self.assertEqual(result["type"], "BinaryOp")
            self.assertEqual(result["op"], "OR")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 9)
            
            # Left side should be (1 AND 2)
            left = result["left"]
            self.assertEqual(left["type"], "BinaryOp")
            self.assertEqual(left["op"], "AND")
            self.assertEqual(left["left"], ast1)
            self.assertEqual(left["right"], ast2)
            
            # Right side should be 3
            self.assertEqual(result["right"], ast3)
            
            self.assertEqual(parser_state["pos"], 5)
            self.assertEqual(mock_parse_comp.call_count, 3)

    def test_mixed_and_or_operators(self):
        """Test parsing with mixed AND and OR operators."""
        parser_state = {
            "tokens": [
                self._create_token("IDENTIFIER", "a", line=1, column=1),
                self._create_token("KEYWORD", "OR", line=1, column=3),
                self._create_token("IDENTIFIER", "b", line=1, column=6),
                self._create_token("KEYWORD", "AND", line=1, column=8),
                self._create_token("IDENTIFIER", "c", line=1, column=12)
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        ast_a = self._create_ast_node("Identifier", "a", line=1, column=1)
        ast_b = self._create_ast_node("Identifier", "b", line=1, column=6)
        ast_c = self._create_ast_node("Identifier", "c", line=1, column=12)
        
        with patch(f"{BASE_PATH}._parse_logical_src._parse_comparison", side_effect=[ast_a, ast_b, ast_c]) as mock_parse_comp:
            result = _parse_logical(parser_state)
            
            # Should be: (a OR b) AND c (left-associative)
            self.assertEqual(result["type"], "BinaryOp")
            self.assertEqual(result["op"], "AND")
            self.assertEqual(result["right"], ast_c)
            
            left = result["left"]
            self.assertEqual(left["type"], "BinaryOp")
            self.assertEqual(left["op"], "OR")
            self.assertEqual(left["left"], ast_a)
            self.assertEqual(left["right"], ast_b)

    def test_lowercase_and_or(self):
        """Test that lowercase and/or keywords are handled (case-insensitive)."""
        parser_state = {
            "tokens": [
                self._create_token("NUMBER", "1", line=1, column=1),
                self._create_token("KEYWORD", "and", line=1, column=3),
                self._create_token("NUMBER", "0", line=1, column=7)
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        left_ast = self._create_ast_node("Literal", 1, line=1, column=1)
        right_ast = self._create_ast_node("Literal", 0, line=1, column=7)
        
        with patch(f"{BASE_PATH}._parse_logical_src._parse_comparison", side_effect=[left_ast, right_ast]) as mock_parse_comp:
            result = _parse_logical(parser_state)
            
            self.assertEqual(result["type"], "BinaryOp")
            self.assertEqual(result["op"], "AND")  # Should be uppercase
            self.assertEqual(parser_state["pos"], 3)

    def test_empty_tokens(self):
        """Test parsing with empty token list."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }
        
        mock_ast = self._create_ast_node("Empty")
        
        with patch(f"{BASE_PATH}._parse_logical_src._parse_comparison", return_value=mock_ast) as mock_parse_comp:
            result = _parse_logical(parser_state)
            
            self.assertEqual(result, mock_ast)
            mock_parse_comp.assert_called_once()
            self.assertEqual(parser_state["pos"], 0)

    def test_pos_at_end(self):
        """Test when pos is already at end of tokens."""
        parser_state = {
            "tokens": [self._create_token("NUMBER", "42")],
            "pos": 1,
            "filename": "test.py"
        }
        
        mock_ast = self._create_ast_node("Literal", 42)
        
        with patch("._parse_logical_src._parse_comparison", return_value=mock_ast) as mock_parse_comp:
            result = _parse_logical(parser_state)
            
            self.assertEqual(result, mock_ast)
            self.assertEqual(parser_state["pos"], 1)

    def test_non_keyword_token(self):
        """Test that non-keyword tokens are not treated as logical operators."""
        parser_state = {
            "tokens": [
                self._create_token("NUMBER", "1", line=1, column=1),
                self._create_token("IDENTIFIER", "andx", line=1, column=3),  # Not a keyword
                self._create_token("NUMBER", "2", line=1, column=8)
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        ast1 = self._create_ast_node("Literal", 1, line=1, column=1)
        
        with patch(f"{BASE_PATH}._parse_logical_src._parse_comparison", return_value=ast1) as mock_parse_comp:
            result = _parse_logical(parser_state)
            
            # Should only parse once, not treat IDENTIFIER as operator
            self.assertEqual(result, ast1)
            mock_parse_comp.assert_called_once()
            self.assertEqual(parser_state["pos"], 0)

    def test_comparison_ast_with_children(self):
        """Test that comparison AST with children is properly wrapped."""
        parser_state = {
            "tokens": [
                self._create_token("IDENTIFIER", "x", line=1, column=1),
                self._create_token("KEYWORD", "AND", line=1, column=3),
                self._create_token("IDENTIFIER", "y", line=1, column=7)
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        left_ast = {
            "type": "Comparison",
            "op": "==",
            "left": self._create_ast_node("Identifier", "x"),
            "right": self._create_ast_node("Literal", 5),
            "line": 1,
            "column": 1
        }
        right_ast = self._create_ast_node("Identifier", "y", line=1, column=7)
        
        with patch(f"{BASE_PATH}._parse_logical_src._parse_comparison", side_effect=[left_ast, right_ast]) as mock_parse_comp:
            result = _parse_logical(parser_state)
            
            self.assertEqual(result["type"], "BinaryOp")
            self.assertEqual(result["op"], "AND")
            self.assertEqual(result["left"]["type"], "Comparison")
            self.assertEqual(result["right"], right_ast)


if __name__ == "__main__":
    unittest.main()

# -*- coding: utf-8 -*-
"""Unit tests for _handle_while_loop function."""

from unittest.mock import patch
from typing import Any, Dict

from ._handle_while_loop_src import _handle_while_loop

AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleWhileLoop:
    """Test cases for _handle_while_loop function."""

    def test_handle_while_loop_with_condition_and_body(self):
        """Test while loop node with both condition and body present."""
        node: AST = {
            "type": "while_loop",
            "condition": {"type": "binary_op", "op": "<", "left": {"type": "identifier", "name": "i"}, "right": {"type": "literal", "value": 10}},
            "body": {"type": "block", "statements": [{"type": "assignment", "target": "i", "value": {"type": "binary_op", "op": "+", "left": {"type": "identifier", "name": "i"}, "right": {"type": "literal", "value": 1}}}]}
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }

        with patch("._handle_while_loop_src._traverse_node") as mock_traverse:
            _handle_while_loop(node, symbol_table)

            assert mock_traverse.call_count == 2
            mock_traverse.assert_any_call(node["condition"], symbol_table)
            mock_traverse.assert_any_call(node["body"], symbol_table)

    def test_handle_while_loop_with_only_condition(self):
        """Test while loop node with only condition, body is None."""
        node: AST = {
            "type": "while_loop",
            "condition": {"type": "identifier", "name": "flag"},
            "body": None
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }

        with patch("._handle_while_loop_src._traverse_node") as mock_traverse:
            _handle_while_loop(node, symbol_table)

            mock_traverse.assert_called_once_with(node["condition"], symbol_table)

    def test_handle_while_loop_with_only_body(self):
        """Test while loop node with only body, condition is None."""
        node: AST = {
            "type": "while_loop",
            "condition": None,
            "body": {"type": "block", "statements": []}
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }

        with patch("._handle_while_loop_src._traverse_node") as mock_traverse:
            _handle_while_loop(node, symbol_table)

            mock_traverse.assert_called_once_with(node["body"], symbol_table)

    def test_handle_while_loop_with_both_none(self):
        """Test while loop node with both condition and body as None."""
        node: AST = {
            "type": "while_loop",
            "condition": None,
            "body": None
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }

        with patch("._handle_while_loop_src._traverse_node") as mock_traverse:
            _handle_while_loop(node, symbol_table)

            mock_traverse.assert_not_called()

    def test_handle_while_loop_missing_condition_key(self):
        """Test while loop node without condition key (uses .get())."""
        node: AST = {
            "type": "while_loop",
            "body": {"type": "block", "statements": []}
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }

        with patch("._handle_while_loop_src._traverse_node") as mock_traverse:
            _handle_while_loop(node, symbol_table)

            mock_traverse.assert_called_once_with(node["body"], symbol_table)

    def test_handle_while_loop_missing_body_key(self):
        """Test while loop node without body key (uses .get())."""
        node: AST = {
            "type": "while_loop",
            "condition": {"type": "literal", "value": True}
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }

        with patch("._handle_while_loop_src._traverse_node") as mock_traverse:
            _handle_while_loop(node, symbol_table)

            mock_traverse.assert_called_once_with(node["condition"], symbol_table)

    def test_handle_while_loop_empty_node(self):
        """Test while loop node with empty dict."""
        node: AST = {}
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }

        with patch("._handle_while_loop_src._traverse_node") as mock_traverse:
            _handle_while_loop(node, symbol_table)

            mock_traverse.assert_not_called()

    def test_handle_while_loop_symbol_table_modified(self):
        """Test that symbol_table can be modified through recursive traversal."""
        node: AST = {
            "type": "while_loop",
            "condition": {"type": "identifier", "name": "x"},
            "body": {"type": "assignment", "target": "y", "value": {"type": "literal", "value": 5}}
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": []
        }

        def side_effect(ast_node, sym_table):
            if ast_node.get("type") == "assignment":
                sym_table["variables"][ast_node["target"]] = {"value": ast_node["value"]}

        with patch("._handle_while_loop_src._traverse_node", side_effect=side_effect):
            _handle_while_loop(node, symbol_table)

            assert "y" in symbol_table["variables"]

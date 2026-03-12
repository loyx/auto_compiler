# === std / third-party imports ===
import unittest
from typing import Any, Dict
from copy import deepcopy

# === sub function imports ===
from ._handle_literal_src import _handle_literal

# === Type aliases (matching source) ===
AST = Dict[str, Any]
SymbolTable = Dict[str, Any]


class TestHandleLiteral(unittest.TestCase):
    """Test cases for _handle_literal function."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.base_symbol_table: SymbolTable = {
            "variables": {},
            "functions": {},
            "current_scope": 0,
            "scope_stack": [0]
        }

    def test_handle_literal_int_value(self) -> None:
        """Test handling literal node with integer value."""
        node: AST = {
            "type": "literal",
            "value": 42,
            "data_type": "int"
        }
        symbol_table: SymbolTable = deepcopy(self.base_symbol_table)
        
        result = _handle_literal(node, symbol_table)
        
        self.assertIsNone(result)
        self.assertEqual(symbol_table, self.base_symbol_table)

    def test_handle_literal_char_value(self) -> None:
        """Test handling literal node with character value."""
        node: AST = {
            "type": "literal",
            "value": "a",
            "data_type": "char"
        }
        symbol_table: SymbolTable = deepcopy(self.base_symbol_table)
        
        result = _handle_literal(node, symbol_table)
        
        self.assertIsNone(result)
        self.assertEqual(symbol_table, self.base_symbol_table)

    def test_handle_literal_string_value(self) -> None:
        """Test handling literal node with string value."""
        node: AST = {
            "type": "literal",
            "value": "hello",
            "data_type": "char"
        }
        symbol_table: SymbolTable = deepcopy(self.base_symbol_table)
        
        result = _handle_literal(node, symbol_table)
        
        self.assertIsNone(result)
        self.assertEqual(symbol_table, self.base_symbol_table)

    def test_handle_literal_zero_value(self) -> None:
        """Test handling literal node with zero value (boundary case)."""
        node: AST = {
            "type": "literal",
            "value": 0,
            "data_type": "int"
        }
        symbol_table: SymbolTable = deepcopy(self.base_symbol_table)
        
        result = _handle_literal(node, symbol_table)
        
        self.assertIsNone(result)
        self.assertEqual(symbol_table, self.base_symbol_table)

    def test_handle_literal_negative_value(self) -> None:
        """Test handling literal node with negative integer value."""
        node: AST = {
            "type": "literal",
            "value": -100,
            "data_type": "int"
        }
        symbol_table: SymbolTable = deepcopy(self.base_symbol_table)
        
        result = _handle_literal(node, symbol_table)
        
        self.assertIsNone(result)
        self.assertEqual(symbol_table, self.base_symbol_table)

    def test_handle_literal_empty_string(self) -> None:
        """Test handling literal node with empty string value (boundary case)."""
        node: AST = {
            "type": "literal",
            "value": "",
            "data_type": "char"
        }
        symbol_table: SymbolTable = deepcopy(self.base_symbol_table)
        
        result = _handle_literal(node, symbol_table)
        
        self.assertIsNone(result)
        self.assertEqual(symbol_table, self.base_symbol_table)

    def test_handle_literal_none_value(self) -> None:
        """Test handling literal node with None value."""
        node: AST = {
            "type": "literal",
            "value": None,
            "data_type": "int"
        }
        symbol_table: SymbolTable = deepcopy(self.base_symbol_table)
        
        result = _handle_literal(node, symbol_table)
        
        self.assertIsNone(result)
        self.assertEqual(symbol_table, self.base_symbol_table)

    def test_handle_literal_symbol_table_unchanged(self) -> None:
        """Test that symbol table remains unchanged after handling literal."""
        node: AST = {
            "type": "literal",
            "value": 123,
            "data_type": "int"
        }
        symbol_table: SymbolTable = {
            "variables": {"x": {"type": "int", "value": 10}},
            "functions": {"main": {"return_type": "int"}},
            "current_scope": 1,
            "scope_stack": [0, 1]
        }
        original_table = deepcopy(symbol_table)
        
        result = _handle_literal(node, symbol_table)
        
        self.assertIsNone(result)
        self.assertEqual(symbol_table, original_table)

    def test_handle_literal_minimal_node(self) -> None:
        """Test handling minimal literal node with only required fields."""
        node: AST = {
            "value": 999,
            "data_type": "int"
        }
        symbol_table: SymbolTable = deepcopy(self.base_symbol_table)
        
        result = _handle_literal(node, symbol_table)
        
        self.assertIsNone(result)
        self.assertEqual(symbol_table, self.base_symbol_table)

    def test_handle_literal_extra_fields(self) -> None:
        """Test handling literal node with extra fields."""
        node: AST = {
            "type": "literal",
            "value": 555,
            "data_type": "int",
            "line_number": 10,
            "column": 5
        }
        symbol_table: SymbolTable = deepcopy(self.base_symbol_table)
        
        result = _handle_literal(node, symbol_table)
        
        self.assertIsNone(result)
        self.assertEqual(symbol_table, self.base_symbol_table)

    def test_handle_literal_missing_value_field(self) -> None:
        """Test handling literal node with missing value field (uses .get, should not raise)."""
        node: AST = {
            "type": "literal",
            "data_type": "int"
        }
        symbol_table: SymbolTable = deepcopy(self.base_symbol_table)
        
        result = _handle_literal(node, symbol_table)
        
        self.assertIsNone(result)
        self.assertEqual(symbol_table, self.base_symbol_table)

    def test_handle_literal_missing_data_type_field(self) -> None:
        """Test handling literal node with missing data_type field (uses .get, should not raise)."""
        node: AST = {
            "type": "literal",
            "value": 42
        }
        symbol_table: SymbolTable = deepcopy(self.base_symbol_table)
        
        result = _handle_literal(node, symbol_table)
        
        self.assertIsNone(result)
        self.assertEqual(symbol_table, self.base_symbol_table)

    def test_handle_literal_empty_node(self) -> None:
        """Test handling empty node (uses .get, should not raise)."""
        node: AST = {}
        symbol_table: SymbolTable = deepcopy(self.base_symbol_table)
        
        result = _handle_literal(node, symbol_table)
        
        self.assertIsNone(result)
        self.assertEqual(symbol_table, self.base_symbol_table)

    def test_handle_literal_float_value(self) -> None:
        """Test handling literal node with float value."""
        node: AST = {
            "type": "literal",
            "value": 3.14,
            "data_type": "int"
        }
        symbol_table: SymbolTable = deepcopy(self.base_symbol_table)
        
        result = _handle_literal(node, symbol_table)
        
        self.assertIsNone(result)
        self.assertEqual(symbol_table, self.base_symbol_table)

    def test_handle_literal_boolean_value(self) -> None:
        """Test handling literal node with boolean value."""
        node: AST = {
            "type": "literal",
            "value": True,
            "data_type": "int"
        }
        symbol_table: SymbolTable = deepcopy(self.base_symbol_table)
        
        result = _handle_literal(node, symbol_table)
        
        self.assertIsNone(result)
        self.assertEqual(symbol_table, self.base_symbol_table)


if __name__ == "__main__":
    unittest.main()

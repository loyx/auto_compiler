# === std / third-party imports ===
import unittest
from typing import Any

# === relative imports ===
from _handle_literal_src import _handle_literal, AST, SymbolTable


# === test helper functions ===
def create_literal_node(
    value: Any = None,
    data_type: str = None,
    line: int = 1,
    column: int = 1
) -> AST:
    """Helper to create a literal AST node."""
    node: AST = {"type": "literal", "line": line, "column": column}
    if value is not None:
        node["value"] = value
    if data_type is not None:
        node["data_type"] = data_type
    return node


def create_symbol_table() -> SymbolTable:
    """Helper to create a fresh symbol table."""
    return {
        "variables": {},
        "functions": {},
        "current_scope": 0,
        "scope_stack": [],
        "errors": []
    }


# === test cases ===
class TestHandleLiteral(unittest.TestCase):
    """Test cases for _handle_literal function."""

    def test_valid_int_literal(self):
        """Test handling a valid integer literal."""
        node = create_literal_node(value=42, data_type="int")
        symbol_table = create_symbol_table()
        
        _handle_literal(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_valid_char_literal(self):
        """Test handling a valid character literal."""
        node = create_literal_node(value="a", data_type="char")
        symbol_table = create_symbol_table()
        
        _handle_literal(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_missing_data_type(self):
        """Test error when data_type field is missing."""
        node = create_literal_node(value=42)
        symbol_table = create_symbol_table()
        
        _handle_literal(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("missing data_type", symbol_table["errors"][0]["message"])
        self.assertEqual(symbol_table["errors"][0]["line"], 1)
        self.assertEqual(symbol_table["errors"][0]["column"], 1)

    def test_invalid_data_type(self):
        """Test error when data_type is not 'int' or 'char'."""
        node = create_literal_node(value=42, data_type="float")
        symbol_table = create_symbol_table()
        
        _handle_literal(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("Invalid data_type", symbol_table["errors"][0]["message"])
        self.assertIn("float", symbol_table["errors"][0]["message"])

    def test_missing_value(self):
        """Test error when value field is missing."""
        node = create_literal_node(data_type="int")
        symbol_table = create_symbol_table()
        
        _handle_literal(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("missing value", symbol_table["errors"][0]["message"])

    def test_int_type_with_string_value(self):
        """Test error when int type has string value."""
        node = create_literal_node(value="hello", data_type="int")
        symbol_table = create_symbol_table()
        
        _handle_literal(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("Expected int value", symbol_table["errors"][0]["message"])
        self.assertIn("str", symbol_table["errors"][0]["message"])

    def test_int_type_with_float_value(self):
        """Test error when int type has float value."""
        node = create_literal_node(value=3.14, data_type="int")
        symbol_table = create_symbol_table()
        
        _handle_literal(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("Expected int value", symbol_table["errors"][0]["message"])
        self.assertIn("float", symbol_table["errors"][0]["message"])

    def test_char_type_with_multichar_string(self):
        """Test error when char type has multi-character string."""
        node = create_literal_node(value="ab", data_type="char")
        symbol_table = create_symbol_table()
        
        _handle_literal(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("Expected single char value", symbol_table["errors"][0]["message"])

    def test_char_type_with_int_value(self):
        """Test error when char type has int value."""
        node = create_literal_node(value=97, data_type="char")
        symbol_table = create_symbol_table()
        
        _handle_literal(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("Expected single char value", symbol_table["errors"][0]["message"])

    def test_char_type_with_empty_string(self):
        """Test error when char type has empty string."""
        node = create_literal_node(value="", data_type="char")
        symbol_table = create_symbol_table()
        
        _handle_literal(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertIn("Expected single char value", symbol_table["errors"][0]["message"])

    def test_error_position_preserved(self):
        """Test that error position matches node position."""
        node = create_literal_node(value=42, data_type="invalid", line=10, column=25)
        symbol_table = create_symbol_table()
        
        _handle_literal(node, symbol_table)
        
        self.assertEqual(symbol_table["errors"][0]["line"], 10)
        self.assertEqual(symbol_table["errors"][0]["column"], 25)

    def test_symbol_table_without_errors_key(self):
        """Test that errors list is created if not present in symbol_table."""
        node = create_literal_node(value=42, data_type="invalid")
        symbol_table: SymbolTable = {
            "variables": {},
            "functions": {}
        }
        
        _handle_literal(node, symbol_table)
        
        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)

    def test_negative_int_literal(self):
        """Test handling a valid negative integer literal."""
        node = create_literal_node(value=-100, data_type="int")
        symbol_table = create_symbol_table()
        
        _handle_literal(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_zero_int_literal(self):
        """Test handling zero as integer literal."""
        node = create_literal_node(value=0, data_type="int")
        symbol_table = create_symbol_table()
        
        _handle_literal(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_special_char_literal(self):
        """Test handling special character literals."""
        for char in ["\n", "\t", " ", "!", "@", "1"]:
            with self.subTest(char=repr(char)):
                node = create_literal_node(value=char, data_type="char")
                symbol_table = create_symbol_table()
                
                _handle_literal(node, symbol_table)
                
                self.assertEqual(len(symbol_table["errors"]), 0)


# === test runner ===
if __name__ == "__main__":
    unittest.main()

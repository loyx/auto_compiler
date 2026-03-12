# === Test file for _handle_assignment ===
import unittest

# Relative import from the same package
from ._handle_assignment_src import _handle_assignment, AST, SymbolTable


class TestHandleAssignment(unittest.TestCase):
    """Test cases for _handle_assignment function."""

    def test_variable_declared_no_error(self):
        """Happy path: variable is declared, no error should be recorded."""
        node: AST = {
            "type": "assignment",
            "value": "x",
            "line": 10,
            "column": 5
        }
        symbol_table: SymbolTable = {
            "variables": {
                "x": {"data_type": "int", "is_declared": True, "line": 1, "column": 1, "scope_level": 0}
            },
            "errors": []
        }
        
        _handle_assignment(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_variable_not_declared_records_error(self):
        """Variable not declared - error should be recorded."""
        node: AST = {
            "type": "assignment",
            "value": "y",
            "line": 15,
            "column": 8
        }
        symbol_table: SymbolTable = {
            "variables": {
                "x": {"data_type": "int", "is_declared": True, "line": 1, "column": 1, "scope_level": 0}
            },
            "errors": []
        }
        
        _handle_assignment(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        error = symbol_table["errors"][0]
        self.assertEqual(error["line"], 15)
        self.assertEqual(error["column"], 8)
        self.assertEqual(error["message"], "use of undeclared variable: y")

    def test_variable_exists_but_not_declared(self):
        """Variable exists in table but is_declared is False - should record error."""
        node: AST = {
            "type": "assignment",
            "value": "z",
            "line": 20,
            "column": 3
        }
        symbol_table: SymbolTable = {
            "variables": {
                "z": {"data_type": "char", "is_declared": False, "line": 5, "column": 2, "scope_level": 0}
            },
            "errors": []
        }
        
        _handle_assignment(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertEqual(symbol_table["errors"][0]["message"], "use of undeclared variable: z")

    def test_var_name_from_children(self):
        """Variable name extracted from node["children"][0]["value"]."""
        node: AST = {
            "type": "assignment",
            "children": [
                {"type": "identifier", "value": "a"}
            ],
            "line": 25,
            "column": 10
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "errors": []
        }
        
        _handle_assignment(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertEqual(symbol_table["errors"][0]["message"], "use of undeclared variable: a")

    def test_var_name_priority_value_over_children(self):
        """Variable name from node["value"] takes priority over children."""
        node: AST = {
            "type": "assignment",
            "value": "priority_var",
            "children": [
                {"type": "identifier", "value": "ignored_var"}
            ],
            "line": 30,
            "column": 1
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "errors": []
        }
        
        _handle_assignment(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertEqual(symbol_table["errors"][0]["message"], "use of undeclared variable: priority_var")

    def test_no_variable_name_returns_early(self):
        """No extractable variable name - should return without error."""
        node: AST = {
            "type": "assignment",
            "children": [],
            "line": 35,
            "column": 5
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "errors": []
        }
        
        _handle_assignment(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_no_variable_name_no_value_key(self):
        """Node without value key and no children - should return without error."""
        node: AST = {
            "type": "assignment",
            "line": 40,
            "column": 2
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "errors": []
        }
        
        _handle_assignment(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_creates_errors_list_if_missing(self):
        """symbol_table without 'errors' key - should create it."""
        node: AST = {
            "type": "assignment",
            "value": "new_var",
            "line": 45,
            "column": 7
        }
        symbol_table: SymbolTable = {
            "variables": {}
        }
        
        _handle_assignment(node, symbol_table)
        
        self.assertIn("errors", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)

    def test_creates_variables_dict_if_missing(self):
        """symbol_table without 'variables' key - should create it."""
        node: AST = {
            "type": "assignment",
            "value": "another_var",
            "line": 50,
            "column": 4
        }
        symbol_table: SymbolTable = {
            "errors": []
        }
        
        _handle_assignment(node, symbol_table)
        
        self.assertIn("variables", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)

    def test_empty_symbol_table(self):
        """Completely empty symbol_table - should handle gracefully."""
        node: AST = {
            "type": "assignment",
            "value": "empty_test",
            "line": 55,
            "column": 9
        }
        symbol_table: SymbolTable = {}
        
        _handle_assignment(node, symbol_table)
        
        self.assertIn("errors", symbol_table)
        self.assertIn("variables", symbol_table)
        self.assertEqual(len(symbol_table["errors"]), 1)

    def test_default_line_column_when_missing(self):
        """Node without line/column - should default to 0."""
        node: AST = {
            "type": "assignment",
            "value": "no_location"
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "errors": []
        }
        
        _handle_assignment(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 1)
        self.assertEqual(symbol_table["errors"][0]["line"], 0)
        self.assertEqual(symbol_table["errors"][0]["column"], 0)

    def test_multiple_assignments_accumulate_errors(self):
        """Multiple assignment calls should accumulate errors."""
        symbol_table: SymbolTable = {
            "variables": {
                "declared": {"data_type": "int", "is_declared": True, "line": 1, "column": 1, "scope_level": 0}
            },
            "errors": []
        }
        
        node1: AST = {"type": "assignment", "value": "undeclared1", "line": 60, "column": 1}
        node2: AST = {"type": "assignment", "value": "declared", "line": 61, "column": 2}
        node3: AST = {"type": "assignment", "value": "undeclared2", "line": 62, "column": 3}
        
        _handle_assignment(node1, symbol_table)
        _handle_assignment(node2, symbol_table)
        _handle_assignment(node3, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 2)
        self.assertEqual(symbol_table["errors"][0]["message"], "use of undeclared variable: undeclared1")
        self.assertEqual(symbol_table["errors"][1]["message"], "use of undeclared variable: undeclared2")

    def test_children_not_dict(self):
        """Children[0] is not a dict - should return without error."""
        node: AST = {
            "type": "assignment",
            "children": ["not_a_dict"],
            "line": 70,
            "column": 5
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "errors": []
        }
        
        _handle_assignment(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 0)

    def test_children_dict_no_value(self):
        """Children[0] is dict but has no value key - should return without error."""
        node: AST = {
            "type": "assignment",
            "children": [{"type": "identifier"}],
            "line": 75,
            "column": 6
        }
        symbol_table: SymbolTable = {
            "variables": {},
            "errors": []
        }
        
        _handle_assignment(node, symbol_table)
        
        self.assertEqual(len(symbol_table["errors"]), 0)


if __name__ == "__main__":
    unittest.main()

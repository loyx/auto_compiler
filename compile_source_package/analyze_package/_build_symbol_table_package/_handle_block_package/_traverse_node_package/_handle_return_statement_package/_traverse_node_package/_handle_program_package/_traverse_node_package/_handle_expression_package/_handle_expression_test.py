import unittest
from unittest.mock import patch

# Relative import for the function under test
from ._handle_expression_src import _handle_expression


class TestHandleExpression(unittest.TestCase):
    """Test cases for _handle_expression function."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.symbol_table = {
            "variables": {
                "x": {"data_type": "int", "is_declared": True, "line": 1, "column": 1, "scope_level": 0},
                "y": {"data_type": "int", "is_declared": True, "line": 1, "column": 5, "scope_level": 0},
                "c": {"data_type": "char", "is_declared": True, "line": 2, "column": 1, "scope_level": 0}
            },
            "functions": {
                "foo": {"return_type": "int", "params": [], "line": 10, "column": 1}
            },
            "current_scope": 0,
            "scope_stack": [0],
            "errors": []
        }
    
    def test_expression_with_children(self):
        """Test expression node with children list."""
        node = {
            "type": "expression",
            "operator": "+",
            "children": [
                {"type": "variable", "value": "x", "line": 1, "column": 1},
                {"type": "variable", "value": "y", "line": 1, "column": 3}
            ],
            "line": 1,
            "column": 1
        }
        
        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_expression(node, self.symbol_table)
            
            self.assertEqual(mock_traverse.call_count, 2)
            self.assertEqual(len(self.symbol_table["errors"]), 0)
    
    def test_expression_with_operands(self):
        """Test expression node with operands list."""
        node = {
            "type": "expression",
            "operator": "*",
            "operands": [
                {"type": "literal", "value": 5, "data_type": "int", "line": 2, "column": 1},
                {"type": "literal", "value": 10, "data_type": "int", "line": 2, "column": 3}
            ],
            "line": 2,
            "column": 1
        }
        
        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_expression(node, self.symbol_table)
            
            self.assertEqual(mock_traverse.call_count, 2)
            self.assertEqual(len(self.symbol_table["errors"]), 0)
    
    def test_binary_operator_type_mismatch(self):
        """Test binary operator with mismatched operand types."""
        node = {
            "type": "expression",
            "operator": "+",
            "left": {"type": "variable", "value": "x", "data_type": "int", "line": 3, "column": 1},
            "right": {"type": "variable", "value": "c", "data_type": "char", "line": 3, "column": 3},
            "line": 3,
            "column": 1
        }
        
        with patch("._traverse_node_package._traverse_node_src._traverse_node"):
            _handle_expression(node, self.symbol_table)
            
            self.assertEqual(len(self.symbol_table["errors"]), 1)
            self.assertEqual(self.symbol_table["errors"][0]["type"], "operand_type_mismatch")
            self.assertIn("Operand type mismatch", self.symbol_table["errors"][0]["message"])
    
    def test_undeclared_variable(self):
        """Test reference to undeclared variable."""
        node = {
            "type": "expression",
            "operator": "identifier",
            "value": "undefined_var",
            "line": 4,
            "column": 1
        }
        
        with patch("._traverse_node_package._traverse_node_src._traverse_node"):
            _handle_expression(node, self.symbol_table)
            
            self.assertEqual(len(self.symbol_table["errors"]), 1)
            self.assertEqual(self.symbol_table["errors"][0]["type"], "undeclared_variable")
            self.assertIn("undefined_var", self.symbol_table["errors"][0]["message"])
    
    def test_undeclared_function(self):
        """Test call to undeclared function."""
        node = {
            "type": "expression",
            "operator": "call",
            "value": "unknown_func",
            "line": 5,
            "column": 1
        }
        
        with patch("._traverse_node_package._traverse_node_src._traverse_node"):
            _handle_expression(node, self.symbol_table)
            
            self.assertEqual(len(self.symbol_table["errors"]), 1)
            self.assertEqual(self.symbol_table["errors"][0]["type"], "undeclared_function")
            self.assertIn("unknown_func", self.symbol_table["errors"][0]["message"])
    
    def test_declared_function_call(self):
        """Test call to declared function - should not error."""
        node = {
            "type": "expression",
            "operator": "call",
            "value": "foo",
            "line": 6,
            "column": 1
        }
        
        with patch("._traverse_node_package._traverse_node_src._traverse_node"):
            _handle_expression(node, self.symbol_table)
            
            self.assertEqual(len(self.symbol_table["errors"]), 0)
    
    def test_variable_type_from_symbol_table(self):
        """Test variable type lookup from symbol table."""
        node = {
            "type": "expression",
            "operator": "+",
            "left": {"type": "variable", "value": "x", "line": 7, "column": 1},
            "right": {"type": "variable", "value": "y", "line": 7, "column": 3},
            "line": 7,
            "column": 1
        }
        
        with patch("._traverse_node_package._traverse_node_src._traverse_node"):
            _handle_expression(node, self.symbol_table)
            
            self.assertEqual(len(self.symbol_table["errors"]), 0)
    
    def test_empty_expression(self):
        """Test expression with no children or operands."""
        node = {
            "type": "expression",
            "operator": "+",
            "line": 8,
            "column": 1
        }
        
        with patch("._traverse_node_package._traverse_node_src._traverse_node") as mock_traverse:
            _handle_expression(node, self.symbol_table)
            
            mock_traverse.assert_not_called()
            self.assertEqual(len(self.symbol_table["errors"]), 0)
    
    def test_unary_operator(self):
        """Test unary operator (not binary)."""
        node = {
            "type": "expression",
            "operator": "-",
            "children": [{"type": "literal", "value": 5, "data_type": "int", "line": 9, "column": 1}],
            "line": 9,
            "column": 1
        }
        
        with patch("._traverse_node_package._traverse_node_src._traverse_node"):
            _handle_expression(node, self.symbol_table)
            
            self.assertEqual(len(self.symbol_table["errors"]), 0)
    
    def test_all_binary_operators(self):
        """Test all binary operators trigger type checking."""
        operators = ["+", "-", "*", "/", "==", "!=", "<", ">", "<=", ">=", "&&", "||"]
        
        for op in operators:
            symbol_table = {
                "variables": {
                    "a": {"data_type": "int", "is_declared": True},
                    "b": {"data_type": "char", "is_declared": True}
                },
                "functions": {},
                "errors": []
            }
            node = {
                "type": "expression",
                "operator": op,
                "left": {"type": "variable", "value": "a", "data_type": "int", "line": 1, "column": 1},
                "right": {"type": "variable", "value": "b", "data_type": "char", "line": 1, "column": 3},
                "line": 1,
                "column": 1
            }
            
            with patch("._traverse_node_package._traverse_node_src._traverse_node"):
                _handle_expression(node, symbol_table)
                
                self.assertEqual(len(symbol_table["errors"]), 1, f"Operator {op} should detect type mismatch")
    
    def test_variable_node_type(self):
        """Test node with type='variable' triggers declaration check."""
        node = {
            "type": "variable",
            "name": "missing_var",
            "line": 10,
            "column": 1
        }
        
        with patch("._traverse_node_package._traverse_node_src._traverse_node"):
            _handle_expression(node, self.symbol_table)
            
            self.assertEqual(len(self.symbol_table["errors"]), 1)
            self.assertEqual(self.symbol_table["errors"][0]["type"], "undeclared_variable")
    
    def test_function_call_node_type(self):
        """Test node with type='function_call' triggers declaration check."""
        node = {
            "type": "function_call",
            "name": "missing_func",
            "line": 11,
            "column": 1
        }
        
        with patch("._traverse_node_package._traverse_node_src._traverse_node"):
            _handle_expression(node, self.symbol_table)
            
            self.assertEqual(len(self.symbol_table["errors"]), 1)
            self.assertEqual(self.symbol_table["errors"][0]["type"], "undeclared_function")
    
    def test_error_initialization(self):
        """Test that errors list is initialized if not present."""
        symbol_table = {
            "variables": {},
            "functions": {}
        }
        node = {
            "type": "expression",
            "operator": "identifier",
            "value": "var",
            "line": 12,
            "column": 1
        }
        
        with patch("._traverse_node_package._traverse_node_src._traverse_node"):
            _handle_expression(node, symbol_table)
            
            self.assertIn("errors", symbol_table)
            self.assertEqual(len(symbol_table["errors"]), 1)
    
    def test_operator_from_op_field(self):
        """Test operator can be read from 'op' field."""
        node = {
            "type": "expression",
            "op": "+",
            "left": {"type": "literal", "value": 1, "data_type": "int", "line": 13, "column": 1},
            "right": {"type": "literal", "value": 2, "data_type": "int", "line": 13, "column": 3},
            "line": 13,
            "column": 1
        }
        
        with patch("._traverse_node_package._traverse_node_src._traverse_node"):
            _handle_expression(node, self.symbol_table)
            
            self.assertEqual(len(self.symbol_table["errors"]), 0)
    
    def test_default_line_column(self):
        """Test default line and column values when not provided."""
        node = {
            "type": "expression",
            "operator": "identifier",
            "value": "missing"
        }
        
        with patch("._traverse_node_package._traverse_node_src._traverse_node"):
            _handle_expression(node, self.symbol_table)
            
            self.assertEqual(len(self.symbol_table["errors"]), 1)
            self.assertEqual(self.symbol_table["errors"][0]["line"], 0)
            self.assertEqual(self.symbol_table["errors"][0]["column"], 0)


if __name__ == "__main__":
    unittest.main()

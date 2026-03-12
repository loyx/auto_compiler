import unittest

from ._create_ast_node_src import _create_ast_node


class TestCreateAstNode(unittest.TestCase):
    """Test cases for _create_ast_node function."""
    
    def test_basic_node_creation(self):
        """Test basic AST node creation with all parameters."""
        result = _create_ast_node(
            node_type="ObjectLiteral",
            value=None,
            children=[],
            line=1,
            column=0
        )
        
        self.assertEqual(result["type"], "ObjectLiteral")
        self.assertEqual(result["children"], [])
        self.assertIsNone(result["value"])
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 0)
    
    def test_node_with_string_value(self):
        """Test AST node creation with a string value."""
        result = _create_ast_node(
            node_type="StringLiteral",
            value="hello",
            children=[],
            line=5,
            column=10
        )
        
        self.assertEqual(result["type"], "StringLiteral")
        self.assertEqual(result["value"], "hello")
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 10)
    
    def test_node_with_numeric_value(self):
        """Test AST node creation with a numeric value."""
        result = _create_ast_node(
            node_type="NumberLiteral",
            value=42,
            children=[],
            line=3,
            column=5
        )
        
        self.assertEqual(result["type"], "NumberLiteral")
        self.assertEqual(result["value"], 42)
    
    def test_node_with_children(self):
        """Test AST node creation with child nodes."""
        child1 = _create_ast_node("Identifier", "x", [], 1, 0)
        child2 = _create_ast_node("Identifier", "y", [], 1, 5)
        
        result = _create_ast_node(
            node_type="BinaryExpression",
            value="+",
            children=[child1, child2],
            line=1,
            column=0
        )
        
        self.assertEqual(result["type"], "BinaryExpression")
        self.assertEqual(len(result["children"]), 2)
        self.assertEqual(result["children"][0]["type"], "Identifier")
        self.assertEqual(result["children"][0]["value"], "x")
        self.assertEqual(result["children"][1]["type"], "Identifier")
        self.assertEqual(result["children"][1]["value"], "y")
    
    def test_node_with_zero_line_column(self):
        """Test AST node creation with zero line and column."""
        result = _create_ast_node(
            node_type="Program",
            value=None,
            children=[],
            line=0,
            column=0
        )
        
        self.assertEqual(result["line"], 0)
        self.assertEqual(result["column"], 0)
    
    def test_node_with_boolean_value(self):
        """Test AST node creation with boolean value."""
        result = _create_ast_node(
            node_type="BooleanLiteral",
            value=True,
            children=[],
            line=1,
            column=0
        )
        
        self.assertEqual(result["value"], True)
        
        result_false = _create_ast_node(
            node_type="BooleanLiteral",
            value=False,
            children=[],
            line=1,
            column=0
        )
        
        self.assertEqual(result_false["value"], False)
    
    def test_node_with_dict_value(self):
        """Test AST node creation with dict value."""
        metadata = {"key": "value"}
        result = _create_ast_node(
            node_type="MetaNode",
            value=metadata,
            children=[],
            line=1,
            column=0
        )
        
        self.assertEqual(result["value"], metadata)
    
    def test_returns_dict_type(self):
        """Test that function returns a dictionary."""
        result = _create_ast_node("Test", None, [], 1, 1)
        self.assertIsInstance(result, dict)
    
    def test_all_required_fields_present(self):
        """Test that all required fields are present in result."""
        result = _create_ast_node("Test", "val", [], 10, 20)
        
        required_fields = ["type", "children", "value", "line", "column"]
        for field in required_fields:
            self.assertIn(field, result)
    
    def test_node_with_nested_children(self):
        """Test AST node creation with deeply nested children."""
        grandchild = _create_ast_node("Literal", 123, [], 2, 5)
        child = _create_ast_node("UnaryExpr", "-", [grandchild], 2, 4)
        
        result = _create_ast_node(
            node_type="Expression",
            value=None,
            children=[child],
            line=2,
            column=4
        )
        
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(len(result["children"][0]["children"]), 1)
        self.assertEqual(result["children"][0]["children"][0]["value"], 123)
    
    def test_node_with_empty_string_value(self):
        """Test AST node creation with empty string value."""
        result = _create_ast_node(
            node_type="StringLiteral",
            value="",
            children=[],
            line=1,
            column=0
        )
        
        self.assertEqual(result["value"], "")
    
    def test_node_with_large_line_column(self):
        """Test AST node creation with large line and column numbers."""
        result = _create_ast_node(
            node_type="Test",
            value=None,
            children=[],
            line=9999,
            column=8888
        )
        
        self.assertEqual(result["line"], 9999)
        self.assertEqual(result["column"], 8888)


if __name__ == "__main__":
    unittest.main()

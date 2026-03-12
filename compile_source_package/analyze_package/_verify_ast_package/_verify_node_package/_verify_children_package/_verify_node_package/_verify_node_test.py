import unittest
from unittest.mock import patch

from ._verify_node_src import _verify_node


class TestVerifyNode(unittest.TestCase):
    """Test cases for _verify_node function."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.filename = "test.py"
        self.default_symbol_table = {
            "variables": {"x": {"type": "int"}, "y": {"type": "str"}},
            "functions": {"foo": {"params_count": 2, "return_type": "int"}},
            "current_scope": 1
        }
        self.default_context_stack = []
    
    def test_valid_variable_ref(self):
        """Test valid variable reference."""
        node = {
            "type": "variable_ref",
            "name": "x",
            "line": 1,
            "column": 5
        }
        _verify_node(node, self.default_symbol_table, self.default_context_stack, self.filename)
    
    def test_undefined_variable(self):
        """Test undefined variable raises ValueError."""
        node = {
            "type": "variable_ref",
            "name": "undefined_var",
            "line": 10,
            "column": 20
        }
        with self.assertRaises(ValueError) as ctx:
            _verify_node(node, self.default_symbol_table, self.default_context_stack, self.filename)
        self.assertIn("undefined variable 'undefined_var'", str(ctx.exception))
        self.assertIn("test.py:10:20", str(ctx.exception))
    
    def test_valid_function_call(self):
        """Test valid function call with correct parameter count."""
        node = {
            "type": "function_call",
            "name": "foo",
            "args": [{"type": "literal", "value": 1}, {"type": "literal", "value": 2}],
            "line": 5,
            "column": 10
        }
        _verify_node(node, self.default_symbol_table, self.default_context_stack, self.filename)
    
    def test_undefined_function(self):
        """Test undefined function raises ValueError."""
        node = {
            "type": "function_call",
            "name": "bar",
            "args": [],
            "line": 7,
            "column": 15
        }
        with self.assertRaises(ValueError) as ctx:
            _verify_node(node, self.default_symbol_table, self.default_context_stack, self.filename)
        self.assertIn("undefined function 'bar'", str(ctx.exception))
        self.assertIn("test.py:7:15", str(ctx.exception))
    
    def test_wrong_parameter_count(self):
        """Test function call with wrong parameter count raises ValueError."""
        node = {
            "type": "function_call",
            "name": "foo",
            "args": [{"type": "literal", "value": 1}],
            "line": 8,
            "column": 12
        }
        with self.assertRaises(ValueError) as ctx:
            _verify_node(node, self.default_symbol_table, self.default_context_stack, self.filename)
        self.assertIn("function 'foo' expects 2 args, got 1", str(ctx.exception))
        self.assertIn("test.py:8:12", str(ctx.exception))
    
    def test_break_in_loop(self):
        """Test break statement inside loop context."""
        node = {
            "type": "break",
            "line": 15,
            "column": 8
        }
        context_stack = [{"type": "loop", "stmt_type": "while"}]
        _verify_node(node, self.default_symbol_table, context_stack, self.filename)
    
    def test_break_outside_loop(self):
        """Test break statement outside loop raises ValueError."""
        node = {
            "type": "break",
            "line": 3,
            "column": 5
        }
        with self.assertRaises(ValueError) as ctx:
            _verify_node(node, self.default_symbol_table, self.default_context_stack, self.filename)
        self.assertIn("'break' outside loop", str(ctx.exception))
        self.assertIn("test.py:3:5", str(ctx.exception))
    
    def test_continue_in_loop(self):
        """Test continue statement inside loop context."""
        node = {
            "type": "continue",
            "line": 16,
            "column": 8
        }
        context_stack = [{"type": "loop", "stmt_type": "for"}]
        _verify_node(node, self.default_symbol_table, context_stack, self.filename)
    
    def test_continue_outside_loop(self):
        """Test continue statement outside loop raises ValueError."""
        node = {
            "type": "continue",
            "line": 4,
            "column": 6
        }
        with self.assertRaises(ValueError) as ctx:
            _verify_node(node, self.default_symbol_table, self.default_context_stack, self.filename)
        self.assertIn("'continue' outside loop", str(ctx.exception))
        self.assertIn("test.py:4:6", str(ctx.exception))
    
    def test_return_in_function(self):
        """Test return statement inside function context."""
        node = {
            "type": "return",
            "line": 20,
            "column": 10
        }
        context_stack = [{"type": "function", "name": "main", "return_type": "int"}]
        _verify_node(node, self.default_symbol_table, context_stack, self.filename)
    
    def test_return_outside_function(self):
        """Test return statement outside function raises ValueError."""
        node = {
            "type": "return",
            "line": 2,
            "column": 3
        }
        with self.assertRaises(ValueError) as ctx:
            _verify_node(node, self.default_symbol_table, self.default_context_stack, self.filename)
        self.assertIn("'return' outside function", str(ctx.exception))
        self.assertIn("test.py:2:3", str(ctx.exception))
    
    @patch('main_package.compile_source_package.analyze_package._verify_ast_package._verify_node_package._verify_children_package._verify_children_src._verify_children')
    def test_block_node_verifies_children(self, mock_verify_children):
        """Test block node recursively verifies child nodes."""
        child1 = {"type": "variable_ref", "name": "x", "line": 1, "column": 1}
        child2 = {"type": "variable_ref", "name": "y", "line": 2, "column": 1}
        node = {
            "type": "block",
            "children": [child1, child2],
            "line": 0,
            "column": 0
        }
        _verify_node(node, self.default_symbol_table, self.default_context_stack, self.filename)
        self.assertEqual(mock_verify_children.call_count, 2)
        mock_verify_children.assert_any_call(child1, self.default_symbol_table, self.default_context_stack, self.filename)
        mock_verify_children.assert_any_call(child2, self.default_symbol_table, self.default_context_stack, self.filename)
    
    @patch('main_package.compile_source_package.analyze_package._verify_ast_package._verify_node_package._verify_children_package._verify_children_src._verify_children')
    def test_function_def_verifies_body_with_function_context(self, mock_verify_children):
        """Test function_def node verifies body with function context pushed."""
        body_node = {"type": "block", "children": [], "line": 10, "column": 5}
        node = {
            "type": "function_def",
            "name": "my_func",
            "body": body_node,
            "line": 9,
            "column": 0
        }
        _verify_node(node, self.default_symbol_table, self.default_context_stack, self.filename)
        mock_verify_children.assert_called_once()
        call_args = mock_verify_children.call_args
        self.assertEqual(call_args[0][0], body_node)
        new_context = call_args[0][2]
        self.assertEqual(len(new_context), 1)
        self.assertEqual(new_context[0]["type"], "function")
        self.assertEqual(new_context[0]["name"], "my_func")
        self.assertEqual(new_context[0]["return_type"], "any")
    
    def test_literal_node_no_validation(self):
        """Test literal node requires no semantic validation."""
        node = {
            "type": "literal",
            "value": 42,
            "line": 1,
            "column": 5
        }
        _verify_node(node, self.default_symbol_table, self.default_context_stack, self.filename)
    
    def test_binary_op_node_no_validation(self):
        """Test binary_op node requires no semantic validation."""
        node = {
            "type": "binary_op",
            "operator": "+",
            "left": {"type": "literal", "value": 1},
            "right": {"type": "literal", "value": 2},
            "line": 1,
            "column": 5
        }
        _verify_node(node, self.default_symbol_table, self.default_context_stack, self.filename)
    
    def test_unknown_node_type_no_validation(self):
        """Test unknown node type is silently skipped."""
        node = {
            "type": "unknown_type",
            "line": 1,
            "column": 5
        }
        _verify_node(node, self.default_symbol_table, self.default_context_stack, self.filename)
    
    def test_missing_name_in_variable_ref(self):
        """Test variable_ref with missing name field."""
        node = {
            "type": "variable_ref",
            "line": 1,
            "column": 5
        }
        with self.assertRaises(ValueError) as ctx:
            _verify_node(node, self.default_symbol_table, self.default_context_stack, self.filename)
        self.assertIn("undefined variable ''", str(ctx.exception))
    
    def test_missing_args_in_function_call(self):
        """Test function_call with missing args field."""
        node = {
            "type": "function_call",
            "name": "foo",
            "line": 1,
            "column": 5
        }
        _verify_node(node, self.default_symbol_table, self.default_context_stack, self.filename)
    
    def test_missing_line_column_defaults_to_zero(self):
        """Test node with missing line/column defaults to 0."""
        node = {
            "type": "variable_ref",
            "name": "undefined_var"
        }
        with self.assertRaises(ValueError) as ctx:
            _verify_node(node, self.default_symbol_table, self.default_context_stack, self.filename)
        self.assertIn("test.py:0:0", str(ctx.exception))
    
    def test_nested_loop_context(self):
        """Test break in nested loop context."""
        node = {
            "type": "break",
            "line": 25,
            "column": 12
        }
        context_stack = [
            {"type": "function", "name": "main", "return_type": "int"},
            {"type": "loop", "stmt_type": "for"},
            {"type": "loop", "stmt_type": "while"}
        ]
        _verify_node(node, self.default_symbol_table, context_stack, self.filename)
    
    def test_mixed_context_stack(self):
        """Test control flow with mixed context stack."""
        break_node = {"type": "break", "line": 30, "column": 8}
        return_node = {"type": "return", "line": 31, "column": 8}
        context_stack = [
            {"type": "function", "name": "outer", "return_type": "void"},
            {"type": "loop", "stmt_type": "for"}
        ]
        _verify_node(break_node, self.default_symbol_table, context_stack, self.filename)
        _verify_node(return_node, self.default_symbol_table, context_stack, self.filename)
    
    def test_empty_symbol_table_variable_ref(self):
        """Test variable_ref with empty symbol table."""
        node = {
            "type": "variable_ref",
            "name": "x",
            "line": 1,
            "column": 5
        }
        empty_symbol_table = {"variables": {}, "functions": {}, "current_scope": 0}
        with self.assertRaises(ValueError) as ctx:
            _verify_node(node, empty_symbol_table, self.default_context_stack, self.filename)
        self.assertIn("undefined variable 'x'", str(ctx.exception))
    
    def test_empty_symbol_table_function_call(self):
        """Test function_call with empty symbol table."""
        node = {
            "type": "function_call",
            "name": "foo",
            "args": [],
            "line": 1,
            "column": 5
        }
        empty_symbol_table = {"variables": {}, "functions": {}, "current_scope": 0}
        with self.assertRaises(ValueError) as ctx:
            _verify_node(node, empty_symbol_table, self.default_context_stack, self.filename)
        self.assertIn("undefined function 'foo'", str(ctx.exception))
    
    def test_function_with_zero_params(self):
        """Test function call with zero expected parameters."""
        symbol_table = {
            "variables": {},
            "functions": {"no_args": {"params_count": 0, "return_type": "void"}},
            "current_scope": 1
        }
        node = {
            "type": "function_call",
            "name": "no_args",
            "args": [],
            "line": 1,
            "column": 5
        }
        _verify_node(node, symbol_table, self.default_context_stack, self.filename)
    
    def test_function_with_zero_params_but_args_provided(self):
        """Test function call with zero expected parameters but args provided."""
        symbol_table = {
            "variables": {},
            "functions": {"no_args": {"params_count": 0, "return_type": "void"}},
            "current_scope": 1
        }
        node = {
            "type": "function_call",
            "name": "no_args",
            "args": [{"type": "literal", "value": 1}],
            "line": 1,
            "column": 5
        }
        with self.assertRaises(ValueError) as ctx:
            _verify_node(node, symbol_table, self.default_context_stack, self.filename)
        self.assertIn("function 'no_args' expects 0 args, got 1", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()

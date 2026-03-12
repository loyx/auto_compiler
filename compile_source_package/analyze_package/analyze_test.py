import unittest
from unittest.mock import patch

# Relative import from the same package
from .analyze_src import analyze


class TestAnalyze(unittest.TestCase):
    """Test cases for the analyze function."""

    def test_analyze_happy_path(self):
        """Test successful analysis with valid AST."""
        ast = {
            "type": "block",
            "children": [
                {
                    "type": "function_def",
                    "name": "main",
                    "children": []
                }
            ]
        }
        filename = "test.c"
        
        with patch("main_package.compile_source_package.analyze_package.analyze_src._build_symbol_table") as mock_build, \
             patch("main_package.compile_source_package.analyze_package.analyze_src._verify_ast") as mock_verify:
            
            result = analyze(ast, filename)
            
            # Verify both passes were called
            mock_build.assert_called_once()
            mock_verify.assert_called_once()
            
            # Verify result is the same AST object
            self.assertIs(result, ast)

    def test_analyze_with_empty_ast(self):
        """Test analysis with empty/minimal AST."""
        ast = {"type": "block", "children": []}
        filename = "empty.c"
        
        with patch("main_package.compile_source_package.analyze_package.analyze_src._build_symbol_table") as mock_build, \
             patch("main_package.compile_source_package.analyze_package.analyze_src._verify_ast") as mock_verify:
            
            result = analyze(ast, filename)
            
            mock_build.assert_called_once()
            mock_verify.assert_called_once()
            self.assertIs(result, ast)

    def test_analyze_raises_value_error(self):
        """Test that semantic errors raise ValueError with proper format."""
        ast = {
            "type": "variable_ref",
            "name": "undefined_var",
            "line": 10,
            "column": 5
        }
        filename = "error.c"
        
        with patch("main_package.compile_source_package.analyze_package.analyze_src._build_symbol_table"), \
             patch("main_package.compile_source_package.analyze_package.analyze_src._verify_ast") as mock_verify:
            
            mock_verify.side_effect = ValueError(f"{filename}:10:5: error: undefined variable 'undefined_var'")
            
            with self.assertRaises(ValueError) as context:
                analyze(ast, filename)
            
            self.assertIn("error.c:10:5: error:", str(context.exception))

    def test_analyze_symbol_table_initialization(self):
        """Test that symbol table is properly initialized."""
        ast = {"type": "block", "children": []}
        filename = "test.c"
        
        with patch("main_package.compile_source_package.analyze_package.analyze_src._build_symbol_table") as mock_build, \
             patch("main_package.compile_source_package.analyze_package.analyze_src._verify_ast"):
            
            analyze(ast, filename)
            
            # Check that symbol_table was passed to _build_symbol_table
            call_args = mock_build.call_args
            symbol_table = call_args[0][1]
            
            self.assertIn("variables", symbol_table)
            self.assertIn("functions", symbol_table)
            self.assertIn("current_scope", symbol_table)
            self.assertIn("scope_stack", symbol_table)
            
            self.assertEqual(symbol_table["current_scope"], 0)
            self.assertEqual(symbol_table["scope_stack"], [])

    def test_analyze_context_stack_initialization(self):
        """Test that context stack is properly initialized as empty list."""
        ast = {"type": "block", "children": []}
        filename = "test.c"
        
        with patch("main_package.compile_source_package.analyze_package.analyze_src._build_symbol_table"), \
             patch("main_package.compile_source_package.analyze_package.analyze_src._verify_ast") as mock_verify:
            
            analyze(ast, filename)
            
            # Check that context_stack was passed to _verify_ast
            call_args = mock_verify.call_args
            context_stack = call_args[0][2]
            
            self.assertEqual(context_stack, [])

    def test_analyze_preserves_ast_structure(self):
        """Test that analyze preserves AST structure."""
        ast = {
            "type": "function_def",
            "name": "test",
            "data_type": "int",
            "line": 1,
            "column": 1,
            "children": [
                {
                    "type": "variable_decl",
                    "name": "x",
                    "data_type": "int",
                    "line": 2,
                    "column": 5
                }
            ]
        }
        filename = "test.c"
        
        with patch("main_package.compile_source_package.analyze_package.analyze_src._build_symbol_table"), \
             patch("main_package.compile_source_package.analyze_package.analyze_src._verify_ast"):
            
            result = analyze(ast, filename)
            
            # Verify structure is preserved
            self.assertEqual(result["type"], "function_def")
            self.assertEqual(result["name"], "test")
            self.assertEqual(result["data_type"], "int")
            self.assertEqual(len(result["children"]), 1)

    def test_analyze_complex_ast(self):
        """Test analysis with complex nested AST."""
        ast = {
            "type": "block",
            "children": [
                {
                    "type": "function_def",
                    "name": "main",
                    "return_type": "int",
                    "params": [{"name": "argc", "type": "int"}],
                    "children": [
                        {
                            "type": "variable_decl",
                            "name": "x",
                            "data_type": "int",
                            "line": 1,
                            "column": 1
                        },
                        {
                            "type": "assignment",
                            "target": "x",
                            "value": {"type": "int_literal", "value": 10},
                            "line": 2,
                            "column": 1
                        },
                        {
                            "type": "return_stmt",
                            "value": {"type": "variable_ref", "name": "x"},
                            "line": 3,
                            "column": 1
                        }
                    ]
                }
            ]
        }
        filename = "complex.c"
        
        with patch("main_package.compile_source_package.analyze_package.analyze_src._build_symbol_table"), \
             patch("main_package.compile_source_package.analyze_package.analyze_src._verify_ast"):
            
            result = analyze(ast, filename)
            
            self.assertIs(result, ast)

    def test_analyze_multiple_function_calls(self):
        """Test that analyze calls sub-functions in correct order."""
        ast = {"type": "block", "children": []}
        filename = "test.c"
        call_order = []
        
        def mock_build_side_effect(*args, **kwargs):
            call_order.append("build")
        
        def mock_verify_side_effect(*args, **kwargs):
            call_order.append("verify")
        
        with patch("main_package.compile_source_package.analyze_package.analyze_src._build_symbol_table") as mock_build, \
             patch("main_package.compile_source_package.analyze_package.analyze_src._verify_ast") as mock_verify:
            
            mock_build.side_effect = mock_build_side_effect
            mock_verify.side_effect = mock_verify_side_effect
            
            analyze(ast, filename)
            
            # Verify order: build first, then verify
            self.assertEqual(call_order, ["build", "verify"])

    def test_analyze_build_symbol_table_receives_correct_args(self):
        """Test that _build_symbol_table receives ast and symbol_table."""
        ast = {"type": "block", "children": []}
        filename = "test.c"
        
        with patch("main_package.compile_source_package.analyze_package.analyze_src._build_symbol_table") as mock_build, \
             patch("main_package.compile_source_package.analyze_package.analyze_src._verify_ast"):
            
            analyze(ast, filename)
            
            # Verify _build_symbol_table was called with ast and symbol_table
            self.assertEqual(mock_build.call_count, 1)
            args = mock_build.call_args[0]
            self.assertEqual(len(args), 2)
            self.assertIs(args[0], ast)
            self.assertIsInstance(args[1], dict)

    def test_analyze_verify_ast_receives_correct_args(self):
        """Test that _verify_ast receives all four required arguments."""
        ast = {"type": "block", "children": []}
        filename = "test.c"
        
        with patch("main_package.compile_source_package.analyze_package.analyze_src._build_symbol_table"), \
             patch("main_package.compile_source_package.analyze_package.analyze_src._verify_ast") as mock_verify:
            
            analyze(ast, filename)
            
            # Verify _verify_ast was called with ast, symbol_table, context_stack, filename
            self.assertEqual(mock_verify.call_count, 1)
            args = mock_verify.call_args[0]
            self.assertEqual(len(args), 4)
            self.assertIs(args[0], ast)
            self.assertIsInstance(args[1], dict)  # symbol_table
            self.assertIsInstance(args[2], list)   # context_stack
            self.assertEqual(args[3], filename)

    def test_analyze_different_filenames(self):
        """Test analyze with different filename formats."""
        ast = {"type": "block", "children": []}
        filenames = ["test.c", "/path/to/file.c", "file_with_underscore.c", "File.C"]
        
        for filename in filenames:
            with patch("main_package.compile_source_package.analyze_package.analyze_src._build_symbol_table"), \
                 patch("main_package.compile_source_package.analyze_package.analyze_src._verify_ast"):
                
                result = analyze(ast, filename)
                self.assertIs(result, ast)

    def test_analyze_error_with_different_line_column(self):
        """Test error messages with different line and column numbers."""
        test_cases = [
            (1, 1, "error.c:1:1: error: test"),
            (100, 50, "error.c:100:50: error: test"),
            (999, 999, "error.c:999:999: error: test"),
        ]
        
        for line, column, expected_pattern in test_cases:
            ast = {
                "type": "variable_ref",
                "name": "x",
                "line": line,
                "column": column
            }
            filename = "error.c"
            
            with patch("main_package.compile_source_package.analyze_package.analyze_src._build_symbol_table"), \
                 patch("main_package.compile_source_package.analyze_package.analyze_src._verify_ast") as mock_verify:
                
                mock_verify.side_effect = ValueError(expected_pattern)
                
                with self.assertRaises(ValueError) as context:
                    analyze(ast, filename)
                
                self.assertIn(expected_pattern, str(context.exception))

    def test_analyze_ast_with_all_node_types(self):
        """Test analyze with AST containing various node types."""
        ast = {
            "type": "block",
            "children": [
                {"type": "function_def", "name": "func1", "children": []},
                {"type": "variable_decl", "name": "var1", "data_type": "int", "line": 1, "column": 1},
                {"type": "assignment", "target": "var1", "line": 2, "column": 1},
                {"type": "binary_op", "operator": "+", "line": 3, "column": 1},
                {"type": "function_call", "name": "func1", "line": 4, "column": 1},
                {"type": "variable_ref", "name": "var1", "line": 5, "column": 1},
                {"type": "int_literal", "value": 42, "line": 6, "column": 1},
                {"type": "char_literal", "value": "a", "line": 7, "column": 1},
                {"type": "if_stmt", "condition": {}, "then_branch": {}, "line": 8, "column": 1},
                {"type": "while_stmt", "condition": {}, "body": {}, "line": 9, "column": 1},
                {"type": "for_stmt", "init": {}, "condition": {}, "update": {}, "body": {}, "line": 10, "column": 1},
                {"type": "return_stmt", "value": {}, "line": 11, "column": 1},
                {"type": "break_stmt", "line": 12, "column": 1},
                {"type": "continue_stmt", "line": 13, "column": 1},
            ]
        }
        filename = "all_types.c"
        
        with patch("main_package.compile_source_package.analyze_package.analyze_src._build_symbol_table"), \
             patch("main_package.compile_source_package.analyze_package.analyze_src._verify_ast"):
            
            result = analyze(ast, filename)
            self.assertIs(result, ast)

    def test_analyze_returns_same_object_not_copy(self):
        """Test that analyze returns the same AST object, not a copy."""
        ast = {"type": "block", "children": [], "custom_field": "original"}
        filename = "test.c"
        
        with patch("main_package.compile_source_package.analyze_package.analyze_src._build_symbol_table"), \
             patch("main_package.compile_source_package.analyze_package.analyze_src._verify_ast"):
            
            result = analyze(ast, filename)
            
            # Modify result and check if original is also modified
            result["custom_field"] = "modified"
            self.assertEqual(ast["custom_field"], "modified")

    def test_analyze_with_nested_blocks(self):
        """Test analyze with deeply nested block structures."""
        ast = {
            "type": "block",
            "children": [
                {
                    "type": "block",
                    "children": [
                        {
                            "type": "block",
                            "children": [
                                {"type": "variable_decl", "name": "x", "data_type": "int", "line": 1, "column": 1}
                            ]
                        }
                    ]
                }
            ]
        }
        filename = "nested.c"
        
        with patch("main_package.compile_source_package.analyze_package.analyze_src._build_symbol_table"), \
             patch("main_package.compile_source_package.analyze_package.analyze_src._verify_ast"):
            
            result = analyze(ast, filename)
            self.assertIs(result, ast)

    def test_analyze_symbol_table_structure(self):
        """Test that symbol table has correct initial structure."""
        ast = {"type": "block", "children": []}
        filename = "test.c"
        
        with patch("main_package.compile_source_package.analyze_package.analyze_src._build_symbol_table") as mock_build, \
             patch("main_package.compile_source_package.analyze_package.analyze_src._verify_ast"):
            
            analyze(ast, filename)
            
            symbol_table = mock_build.call_args[0][1]
            
            # Verify structure
            self.assertIsInstance(symbol_table["variables"], dict)
            self.assertIsInstance(symbol_table["functions"], dict)
            self.assertIsInstance(symbol_table["scope_stack"], list)
            self.assertEqual(symbol_table["current_scope"], 0)
            self.assertEqual(len(symbol_table["variables"]), 0)
            self.assertEqual(len(symbol_table["functions"]), 0)


if __name__ == "__main__":
    unittest.main()

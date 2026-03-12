import unittest
from unittest.mock import patch

# Relative import from the same package
from ._parse_for_statement_src import _parse_for_statement


class TestParseForStatement(unittest.TestCase):
    """Test cases for _parse_for_statement function."""
    
    def test_happy_path_simple_for_loop(self):
        """Test parsing a simple for-loop statement."""
        tokens = [
            {"type": "FOR", "value": "for", "line": 1, "column": 1},
            {"type": "IDENT", "value": "i", "line": 1, "column": 5},
            {"type": "IN", "value": "in", "line": 1, "column": 7},
            {"type": "IDENT", "value": "items", "line": 1, "column": 10},
            {"type": "COLON", "value": ":", "line": 1, "column": 15},
            {"type": "INDENT", "value": "", "line": 2, "column": 1},
            {"type": "SEMICOLON", "value": ";", "line": 3, "column": 1},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.py"}
        
        with patch('._parse_for_statement_package._parse_expression_package._parse_expression_src._parse_expression') as mock_expr:
            def expr_side_effect(state):
                state["pos"] = 4
                return {"type": "IDENT", "value": "items"}
            mock_expr.side_effect = expr_side_effect
            
            with patch('._parse_for_statement_package._parse_block_package._parse_block_src._parse_block') as mock_block:
                def block_side_effect(state):
                    state["pos"] = 6
                    return {"type": "BLOCK", "children": []}
                mock_block.side_effect = block_side_effect
                
                result = _parse_for_statement(parser_state)
                
                self.assertEqual(result["type"], "FOR_STMT")
                self.assertEqual(result["line"], 1)
                self.assertEqual(result["column"], 1)
                self.assertEqual(len(result["children"]), 3)
                
                loop_var = result["children"][0]
                self.assertEqual(loop_var["type"], "LOOP_VAR")
                self.assertEqual(loop_var["value"], "i")
                self.assertEqual(loop_var["line"], 1)
                self.assertEqual(loop_var["column"], 5)
                
                iter_expr = result["children"][1]
                self.assertEqual(iter_expr["type"], "ITER_EXPR")
                
                body = result["children"][2]
                self.assertEqual(body["type"], "BODY")
                
                self.assertEqual(parser_state["pos"], 7)
    
    def test_parser_state_pos_updated(self):
        """Test that parser_state pos is correctly updated after parsing."""
        tokens = [
            {"type": "FOR", "value": "for", "line": 1, "column": 1},
            {"type": "IDENT", "value": "i", "line": 1, "column": 5},
            {"type": "IN", "value": "in", "line": 1, "column": 7},
            {"type": "IDENT", "value": "x", "line": 1, "column": 10},
            {"type": "COLON", "value": ":", "line": 1, "column": 12},
            {"type": "INDENT", "value": "", "line": 2, "column": 1},
            {"type": "SEMICOLON", "value": ";", "line": 3, "column": 1},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.py"}
        
        with patch('._parse_for_statement_package._parse_expression_package._parse_expression_src._parse_expression') as mock_expr:
            def expr_side_effect(state):
                state["pos"] = 4
                return {"type": "EXPR", "value": "x"}
            mock_expr.side_effect = expr_side_effect
            
            with patch('._parse_for_statement_package._parse_block_package._parse_block_src._parse_block') as mock_block:
                def block_side_effect(state):
                    state["pos"] = 6
                    return {"type": "BLOCK", "children": []}
                mock_block.side_effect = block_side_effect
                
                _parse_for_statement(parser_state)
                
                self.assertEqual(parser_state["pos"], 7)
    
    def test_missing_for_token(self):
        """Test SyntaxError when FOR token is missing."""
        tokens = [
            {"type": "IDENT", "value": "i", "line": 1, "column": 1},
            {"type": "IN", "value": "in", "line": 1, "column": 3},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.py"}
        
        with self.assertRaises(SyntaxError) as context:
            _parse_for_statement(parser_state)
        
        self.assertIn("Expected 'for' keyword", str(context.exception))
        self.assertIn("test.py:1", str(context.exception))
    
    def test_missing_loop_variable(self):
        """Test SyntaxError when loop variable is missing."""
        tokens = [
            {"type": "FOR", "value": "for", "line": 1, "column": 1},
            {"type": "IN", "value": "in", "line": 1, "column": 5},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.py"}
        
        with self.assertRaises(SyntaxError) as context:
            _parse_for_statement(parser_state)
        
        self.assertIn("Expected loop variable", str(context.exception))
        self.assertIn("test.py:1", str(context.exception))
    
    def test_missing_in_token(self):
        """Test SyntaxError when IN token is missing."""
        tokens = [
            {"type": "FOR", "value": "for", "line": 1, "column": 1},
            {"type": "IDENT", "value": "i", "line": 1, "column": 5},
            {"type": "COLON", "value": ":", "line": 1, "column": 7},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.py"}
        
        with patch('._parse_for_statement_package._parse_expression_package._parse_expression_src._parse_expression') as mock_expr:
            def expr_side_effect(state):
                state["pos"] = 2
                return {"type": "EXPR"}
            mock_expr.side_effect = expr_side_effect
            
            with self.assertRaises(SyntaxError) as context:
                _parse_for_statement(parser_state)
            
            self.assertIn("Expected 'in'", str(context.exception))
            self.assertIn("test.py:1", str(context.exception))
    
    def test_missing_colon(self):
        """Test SyntaxError when COLON token is missing."""
        tokens = [
            {"type": "FOR", "value": "for", "line": 1, "column": 1},
            {"type": "IDENT", "value": "i", "line": 1, "column": 5},
            {"type": "IN", "value": "in", "line": 1, "column": 7},
            {"type": "IDENT", "value": "x", "line": 1, "column": 10},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.py"}
        
        with patch('._parse_for_statement_package._parse_expression_package._parse_expression_src._parse_expression') as mock_expr:
            def expr_side_effect(state):
                state["pos"] = 4
                return {"type": "EXPR", "value": "x"}
            mock_expr.side_effect = expr_side_effect
            
            with self.assertRaises(SyntaxError) as context:
                _parse_for_statement(parser_state)
            
            self.assertIn("Expected ':'", str(context.exception))
            self.assertIn("test.py:1", str(context.exception))
    
    def test_missing_semicolon(self):
        """Test SyntaxError when SEMICOLON token is missing."""
        tokens = [
            {"type": "FOR", "value": "for", "line": 1, "column": 1},
            {"type": "IDENT", "value": "i", "line": 1, "column": 5},
            {"type": "IN", "value": "in", "line": 1, "column": 7},
            {"type": "IDENT", "value": "x", "line": 1, "column": 10},
            {"type": "COLON", "value": ":", "line": 1, "column": 12},
            {"type": "INDENT", "value": "", "line": 2, "column": 1},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.py"}
        
        with patch('._parse_for_statement_package._parse_expression_package._parse_expression_src._parse_expression') as mock_expr:
            def expr_side_effect(state):
                state["pos"] = 4
                return {"type": "EXPR", "value": "x"}
            mock_expr.side_effect = expr_side_effect
            
            with patch('._parse_for_statement_package._parse_block_package._parse_block_src._parse_block') as mock_block:
                def block_side_effect(state):
                    state["pos"] = 6
                    return {"type": "BLOCK", "children": []}
                mock_block.side_effect = block_side_effect
                
                with self.assertRaises(SyntaxError) as context:
                    _parse_for_statement(parser_state)
                
                self.assertIn("Expected ';'", str(context.exception))
                self.assertIn("test.py:2", str(context.exception))
    
    def test_eof_at_for_token(self):
        """Test SyntaxError when tokens are empty at FOR position."""
        tokens = []
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.py"}
        
        with self.assertRaises(SyntaxError) as context:
            _parse_for_statement(parser_state)
        
        self.assertIn("Expected 'for' keyword", str(context.exception))
        self.assertIn("EOF", str(context.exception))
    
    def test_eof_at_loop_variable(self):
        """Test SyntaxError when EOF occurs at loop variable position."""
        tokens = [
            {"type": "FOR", "value": "for", "line": 1, "column": 1},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.py"}
        
        with self.assertRaises(SyntaxError) as context:
            _parse_for_statement(parser_state)
        
        self.assertIn("Expected loop variable", str(context.exception))
        self.assertIn("EOF", str(context.exception))
    
    def test_eof_at_in_token(self):
        """Test SyntaxError when EOF occurs at IN token position."""
        tokens = [
            {"type": "FOR", "value": "for", "line": 1, "column": 1},
            {"type": "IDENT", "value": "i", "line": 1, "column": 5},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.py"}
        
        with self.assertRaises(SyntaxError) as context:
            _parse_for_statement(parser_state)
        
        self.assertIn("Expected 'in'", str(context.exception))
        self.assertIn("EOF", str(context.exception))
    
    def test_eof_at_colon(self):
        """Test SyntaxError when EOF occurs at COLON position."""
        tokens = [
            {"type": "FOR", "value": "for", "line": 1, "column": 1},
            {"type": "IDENT", "value": "i", "line": 1, "column": 5},
            {"type": "IN", "value": "in", "line": 1, "column": 7},
            {"type": "IDENT", "value": "x", "line": 1, "column": 10},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.py"}
        
        with patch('._parse_for_statement_package._parse_expression_package._parse_expression_src._parse_expression') as mock_expr:
            def expr_side_effect(state):
                state["pos"] = 4
                return {"type": "EXPR", "value": "x"}
            mock_expr.side_effect = expr_side_effect
            
            with self.assertRaises(SyntaxError) as context:
                _parse_for_statement(parser_state)
            
            self.assertIn("Expected ':'", str(context.exception))
            self.assertIn("EOF", str(context.exception))
    
    def test_eof_at_semicolon(self):
        """Test SyntaxError when EOF occurs at SEMICOLON position."""
        tokens = [
            {"type": "FOR", "value": "for", "line": 1, "column": 1},
            {"type": "IDENT", "value": "i", "line": 1, "column": 5},
            {"type": "IN", "value": "in", "line": 1, "column": 7},
            {"type": "IDENT", "value": "x", "line": 1, "column": 10},
            {"type": "COLON", "value": ":", "line": 1, "column": 12},
            {"type": "INDENT", "value": "", "line": 2, "column": 1},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.py"}
        
        with patch('._parse_for_statement_package._parse_expression_package._parse_expression_src._parse_expression') as mock_expr:
            def expr_side_effect(state):
                state["pos"] = 4
                return {"type": "EXPR", "value": "x"}
            mock_expr.side_effect = expr_side_effect
            
            with patch('._parse_for_statement_package._parse_block_package._parse_block_src._parse_block') as mock_block:
                def block_side_effect(state):
                    state["pos"] = 6
                    return {"type": "BLOCK", "children": []}
                mock_block.side_effect = block_side_effect
                
                with self.assertRaises(SyntaxError) as context:
                    _parse_for_statement(parser_state)
                
                self.assertIn("Expected ';'", str(context.exception))
                self.assertIn("EOF", str(context.exception))
    
    def test_default_filename_when_not_provided(self):
        """Test that default filename '<unknown>' is used when not provided."""
        tokens = [
            {"type": "IDENT", "value": "i", "line": 1, "column": 1},
        ]
        parser_state = {"tokens": tokens, "pos": 0}
        
        with self.assertRaises(SyntaxError) as context:
            _parse_for_statement(parser_state)
        
        self.assertIn("<unknown>:1", str(context.exception))
    
    def test_ast_preserves_line_column_info(self):
        """Test that AST node preserves line and column information from tokens."""
        tokens = [
            {"type": "FOR", "value": "for", "line": 5, "column": 10},
            {"type": "IDENT", "value": "item", "line": 5, "column": 14},
            {"type": "IN", "value": "in", "line": 5, "column": 19},
            {"type": "IDENT", "value": "data", "line": 5, "column": 22},
            {"type": "COLON", "value": ":", "line": 5, "column": 26},
            {"type": "INDENT", "value": "", "line": 6, "column": 1},
            {"type": "SEMICOLON", "value": ";", "line": 7, "column": 1},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.py"}
        
        with patch('._parse_for_statement_package._parse_expression_package._parse_expression_src._parse_expression') as mock_expr:
            def expr_side_effect(state):
                state["pos"] = 4
                return {"type": "IDENT", "value": "data", "line": 5, "column": 22}
            mock_expr.side_effect = expr_side_effect
            
            with patch('._parse_for_statement_package._parse_block_package._parse_block_src._parse_block') as mock_block:
                def block_side_effect(state):
                    state["pos"] = 6
                    return {"type": "BLOCK", "children": [], "line": 6, "column": 1}
                mock_block.side_effect = block_side_effect
                
                result = _parse_for_statement(parser_state)
                
                self.assertEqual(result["line"], 5)
                self.assertEqual(result["column"], 10)
                
                loop_var = result["children"][0]
                self.assertEqual(loop_var["line"], 5)
                self.assertEqual(loop_var["column"], 14)
                self.assertEqual(loop_var["value"], "item")
    
    def test_nested_for_loop_structure(self):
        """Test parsing for-loop with nested structure in body."""
        tokens = [
            {"type": "FOR", "value": "for", "line": 1, "column": 1},
            {"type": "IDENT", "value": "i", "line": 1, "column": 5},
            {"type": "IN", "value": "in", "line": 1, "column": 7},
            {"type": "IDENT", "value": "outer", "line": 1, "column": 10},
            {"type": "COLON", "value": ":", "line": 1, "column": 15},
            {"type": "INDENT", "value": "", "line": 2, "column": 1},
            {"type": "SEMICOLON", "value": ";", "line": 3, "column": 1},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.py"}
        
        with patch('._parse_for_statement_package._parse_expression_package._parse_expression_src._parse_expression') as mock_expr:
            def expr_side_effect(state):
                state["pos"] = 4
                return {"type": "IDENT", "value": "outer"}
            mock_expr.side_effect = expr_side_effect
            
            with patch('._parse_for_statement_package._parse_block_package._parse_block_src._parse_block') as mock_block:
                nested_for = {
                    "type": "FOR_STMT",
                    "children": [
                        {"type": "LOOP_VAR", "value": "j"},
                        {"type": "ITER_EXPR", "type": "IDENT", "value": "inner"},
                        {"type": "BODY", "children": []}
                    ]
                }
                def block_side_effect(state):
                    state["pos"] = 6
                    return {"type": "BLOCK", "children": [nested_for]}
                mock_block.side_effect = block_side_effect
                
                result = _parse_for_statement(parser_state)
                
                self.assertEqual(result["type"], "FOR_STMT")
                body = result["children"][2]
                self.assertEqual(body["type"], "BODY")
                self.assertEqual(len(body["children"]), 1)
    
    def test_expression_parser_called_with_correct_state(self):
        """Test that expression parser is called with updated parser_state."""
        tokens = [
            {"type": "FOR", "value": "for", "line": 1, "column": 1},
            {"type": "IDENT", "value": "i", "line": 1, "column": 5},
            {"type": "IN", "value": "in", "line": 1, "column": 7},
            {"type": "IDENT", "value": "x", "line": 1, "column": 10},
            {"type": "COLON", "value": ":", "line": 1, "column": 12},
            {"type": "INDENT", "value": "", "line": 2, "column": 1},
            {"type": "SEMICOLON", "value": ";", "line": 3, "column": 1},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.py"}
        
        with patch('._parse_for_statement_package._parse_expression_package._parse_expression_src._parse_expression') as mock_expr:
            def expr_side_effect(state):
                state["pos"] = 4
                return {"type": "EXPR"}
            mock_expr.side_effect = expr_side_effect
            
            with patch('._parse_for_statement_package._parse_block_package._parse_block_src._parse_block') as mock_block:
                def block_side_effect(state):
                    state["pos"] = 6
                    return {"type": "BLOCK", "children": []}
                mock_block.side_effect = block_side_effect
                
                _parse_for_statement(parser_state)
                
                mock_expr.assert_called_once()
                call_args = mock_expr.call_args
                self.assertEqual(call_args[0][0]["pos"], 3)
    
    def test_block_parser_called_with_correct_state(self):
        """Test that block parser is called with updated parser_state."""
        tokens = [
            {"type": "FOR", "value": "for", "line": 1, "column": 1},
            {"type": "IDENT", "value": "i", "line": 1, "column": 5},
            {"type": "IN", "value": "in", "line": 1, "column": 7},
            {"type": "IDENT", "value": "x", "line": 1, "column": 10},
            {"type": "COLON", "value": ":", "line": 1, "column": 12},
            {"type": "INDENT", "value": "", "line": 2, "column": 1},
            {"type": "SEMICOLON", "value": ";", "line": 3, "column": 1},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.py"}
        
        with patch('._parse_for_statement_package._parse_expression_package._parse_expression_src._parse_expression') as mock_expr:
            def expr_side_effect(state):
                state["pos"] = 4
                return {"type": "EXPR"}
            mock_expr.side_effect = expr_side_effect
            
            with patch('._parse_for_statement_package._parse_block_package._parse_block_src._parse_block') as mock_block:
                def block_side_effect(state):
                    state["pos"] = 6
                    return {"type": "BLOCK", "children": []}
                mock_block.side_effect = block_side_effect
                
                _parse_for_statement(parser_state)
                
                mock_block.assert_called_once()
                call_args = mock_block.call_args
                self.assertEqual(call_args[0][0]["pos"], 5)


if __name__ == "__main__":
    unittest.main()

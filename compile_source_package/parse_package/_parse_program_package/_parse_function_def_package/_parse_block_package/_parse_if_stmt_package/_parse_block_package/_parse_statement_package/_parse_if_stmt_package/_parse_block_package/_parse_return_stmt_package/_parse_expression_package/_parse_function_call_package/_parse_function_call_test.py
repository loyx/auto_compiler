import unittest
from unittest.mock import patch
from typing import Dict, Any

# Relative import for the function under test
from ._parse_function_call_src import _parse_function_call


class TestParseFunctionCall(unittest.TestCase):
    """Test cases for _parse_function_call function."""
    
    def _create_token(self, token_type: str, value: str = "", line: int = 1, column: int = 1) -> Dict[str, Any]:
        """Helper to create a token dict."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }
    
    def _create_parser_state(self, tokens: list, filename: str = "test.py", pos: int = 0) -> Dict[str, Any]:
        """Helper to create a parser state dict."""
        return {
            "tokens": tokens,
            "filename": filename,
            "pos": pos
        }
    
    def _create_callee_ast(self, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """Helper to create a callee AST node."""
        return {
            "type": "IDENTIFIER",
            "value": "func",
            "line": line,
            "column": column
        }
    
    def test_simple_function_call_no_args(self):
        """Test parsing a function call with no arguments: func()"""
        tokens = [
            self._create_token("LPAREN", "(", 1, 5),
            self._create_token("RPAREN", ")", 1, 6),
        ]
        parser_state = self._create_parser_state(tokens, "test.py", 0)
        callee = self._create_callee_ast(1, 1)
        
        # Mock _parse_expression - should not be called for no-arg function
        with patch("._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            result = _parse_function_call(parser_state, callee)
        
        # Verify no calls to _parse_expression (no arguments)
        mock_parse_expr.assert_not_called()
        
        # Verify result structure
        self.assertEqual(result["type"], "CALL")
        self.assertEqual(result["callee"], callee)
        self.assertEqual(result["arguments"], [])
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        
        # Verify pos is updated to after RPAREN
        self.assertEqual(parser_state["pos"], 2)
    
    def test_function_call_with_one_arg(self):
        """Test parsing a function call with one argument: func(arg1)"""
        tokens = [
            self._create_token("LPAREN", "(", 1, 5),
            self._create_token("IDENTIFIER", "arg1", 1, 6),
            self._create_token("RPAREN", ")", 1, 10),
        ]
        parser_state = self._create_parser_state(tokens, "test.py", 0)
        callee = self._create_callee_ast(1, 1)
        
        mock_arg_ast = {"type": "IDENTIFIER", "value": "arg1", "line": 1, "column": 6}
        
        def mock_parse_expr_side_effect(state):
            state["pos"] = 2  # Move past the identifier token
            return mock_arg_ast
        
        with patch("._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.side_effect = mock_parse_expr_side_effect
            result = _parse_function_call(parser_state, callee)
        
        # Verify _parse_expression was called once
        mock_parse_expr.assert_called_once()
        
        # Verify result structure
        self.assertEqual(result["type"], "CALL")
        self.assertEqual(result["callee"], callee)
        self.assertEqual(len(result["arguments"]), 1)
        self.assertEqual(result["arguments"][0], mock_arg_ast)
        
        # Verify pos is updated to after RPAREN
        self.assertEqual(parser_state["pos"], 3)
    
    def test_function_call_with_multiple_args(self):
        """Test parsing a function call with multiple arguments: func(arg1, arg2, arg3)"""
        tokens = [
            self._create_token("LPAREN", "(", 1, 5),
            self._create_token("IDENTIFIER", "arg1", 1, 6),
            self._create_token("COMMA", ",", 1, 10),
            self._create_token("IDENTIFIER", "arg2", 1, 12),
            self._create_token("COMMA", ",", 1, 16),
            self._create_token("IDENTIFIER", "arg3", 1, 18),
            self._create_token("RPAREN", ")", 1, 22),
        ]
        parser_state = self._create_parser_state(tokens, "test.py", 0)
        callee = self._create_callee_ast(1, 1)
        
        mock_arg1 = {"type": "IDENTIFIER", "value": "arg1", "line": 1, "column": 6}
        mock_arg2 = {"type": "IDENTIFIER", "value": "arg2", "line": 1, "column": 12}
        mock_arg3 = {"type": "IDENTIFIER", "value": "arg3", "line": 1, "column": 18}
        
        call_count = [0]
        def mock_parse_expr_side_effect(state):
            call_count[0] += 1
            # Move pos past the current identifier token
            state["pos"] = call_count[0] * 2 - 1
            if call_count[0] == 1:
                return mock_arg1
            elif call_count[0] == 2:
                return mock_arg2
            else:
                return mock_arg3
        
        with patch("._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.side_effect = mock_parse_expr_side_effect
            result = _parse_function_call(parser_state, callee)
        
        # Verify _parse_expression was called 3 times
        self.assertEqual(mock_parse_expr.call_count, 3)
        
        # Verify result structure
        self.assertEqual(result["type"], "CALL")
        self.assertEqual(result["callee"], callee)
        self.assertEqual(len(result["arguments"]), 3)
        self.assertEqual(result["arguments"], [mock_arg1, mock_arg2, mock_arg3])
        
        # Verify pos is updated to after RPAREN
        self.assertEqual(parser_state["pos"], 7)
    
    def test_missing_rparen_raises_error(self):
        """Test that missing RPAREN raises SyntaxError."""
        tokens = [
            self._create_token("LPAREN", "(", 1, 5),
            self._create_token("IDENTIFIER", "arg1", 1, 6),
        ]
        parser_state = self._create_parser_state(tokens, "test.py", 0)
        callee = self._create_callee_ast(1, 1)
        
        mock_arg_ast = {"type": "IDENTIFIER", "value": "arg1", "line": 1, "column": 6}
        
        def mock_parse_expr_side_effect(state):
            state["pos"] = 1  # Move past the identifier token
            return mock_arg_ast
        
        with patch("._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.side_effect = mock_parse_expr_side_effect
            
            with self.assertRaises(SyntaxError) as context:
                _parse_function_call(parser_state, callee)
            
            # Verify error message contains filename and expected ')'
            self.assertIn("test.py", str(context.exception))
            self.assertIn("')'", str(context.exception))
    
    def test_unexpected_token_after_arg_raises_error(self):
        """Test that unexpected token after argument raises SyntaxError."""
        tokens = [
            self._create_token("LPAREN", "(", 1, 5),
            self._create_token("IDENTIFIER", "arg1", 1, 6),
            self._create_token("SEMICOLON", ";", 1, 10),  # Unexpected token
        ]
        parser_state = self._create_parser_state(tokens, "test.py", 0)
        callee = self._create_callee_ast(1, 1)
        
        mock_arg_ast = {"type": "IDENTIFIER", "value": "arg1", "line": 1, "column": 6}
        
        def mock_parse_expr_side_effect(state):
            state["pos"] = 1  # Move past the identifier token
            return mock_arg_ast
        
        with patch("._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.side_effect = mock_parse_expr_side_effect
            
            with self.assertRaises(SyntaxError) as context:
                _parse_function_call(parser_state, callee)
            
            # Verify error message contains filename, line, column
            self.assertIn("test.py", str(context.exception))
            self.assertIn("1", str(context.exception))
            self.assertIn("10", str(context.exception))
            self.assertIn("','", str(context.exception))
            self.assertIn("')'", str(context.exception))
    
    def test_callee_line_column_preserved(self):
        """Test that callee line and column are preserved in result."""
        tokens = [
            self._create_token("LPAREN", "(", 2, 10),
            self._create_token("RPAREN", ")", 2, 11),
        ]
        parser_state = self._create_parser_state(tokens, "test.py", 0)
        callee = self._create_callee_ast(5, 3)  # Different line/column
        
        with patch("._parse_expression_package._parse_expression_src._parse_expression"):
            result = _parse_function_call(parser_state, callee)
        
        # Verify callee line/column are preserved
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 3)
    
    def test_empty_tokens_list_raises_error(self):
        """Test that empty tokens list raises SyntaxError."""
        tokens = []
        parser_state = self._create_parser_state(tokens, "empty.py", 0)
        callee = self._create_callee_ast(1, 1)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_function_call(parser_state, callee)
        
        # Verify error message
        self.assertIn("empty.py", str(context.exception))
        self.assertIn("'('", str(context.exception))
    
    def test_pos_not_at_lparen_raises_error(self):
        """Test that pos not pointing to LPAREN raises SyntaxError."""
        tokens = [
            self._create_token("IDENTIFIER", "func", 1, 1),
            self._create_token("LPAREN", "(", 1, 5),
            self._create_token("RPAREN", ")", 1, 6),
        ]
        parser_state = self._create_parser_state(tokens, "test.py", 1)  # pos at LPAREN
        callee = self._create_callee_ast(1, 1)
        
        # This should work since pos is at LPAREN
        with patch("._parse_expression_package._parse_expression_src._parse_expression"):
            result = _parse_function_call(parser_state, callee)
        
        self.assertEqual(result["type"], "CALL")
        
        # Now test with pos not at LPAREN
        parser_state2 = self._create_parser_state(tokens, "test.py", 0)  # pos at IDENTIFIER
        
        with self.assertRaises(SyntaxError) as context:
            _parse_function_call(parser_state2, callee)
        
        self.assertIn("test.py", str(context.exception))
        self.assertIn("'('", str(context.exception))
    
    def test_nested_function_call(self):
        """Test parsing nested function calls: func1(func2())"""
        tokens = [
            self._create_token("LPAREN", "(", 1, 6),
            self._create_token("IDENTIFIER", "func2", 1, 7),
            self._create_token("LPAREN", "(", 1, 12),
            self._create_token("RPAREN", ")", 1, 13),
            self._create_token("RPAREN", ")", 1, 14),
        ]
        parser_state = self._create_parser_state(tokens, "test.py", 0)
        callee = self._create_callee_ast(1, 1)
        
        # Inner call AST (returned by first _parse_expression call)
        inner_call_ast = {
            "type": "CALL",
            "callee": {"type": "IDENTIFIER", "value": "func2", "line": 1, "column": 7},
            "arguments": [],
            "line": 1,
            "column": 7
        }
        
        def mock_parse_expr_side_effect(state):
            # Simulate parsing the nested call
            # Move pos past the nested function call (tokens 1-4)
            state["pos"] = 4
            return inner_call_ast
        
        with patch("._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.side_effect = mock_parse_expr_side_effect
            result = _parse_function_call(parser_state, callee)
        
        # Verify result structure
        self.assertEqual(result["type"], "CALL")
        self.assertEqual(result["callee"], callee)
        self.assertEqual(len(result["arguments"]), 1)
        self.assertEqual(result["arguments"][0], inner_call_ast)
        
        # Verify pos is updated to after outer RPAREN
        self.assertEqual(parser_state["pos"], 5)


if __name__ == "__main__":
    unittest.main()

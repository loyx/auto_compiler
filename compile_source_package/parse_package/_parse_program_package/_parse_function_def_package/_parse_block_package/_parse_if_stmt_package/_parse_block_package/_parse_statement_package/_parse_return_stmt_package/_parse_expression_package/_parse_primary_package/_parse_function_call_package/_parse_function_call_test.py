# === imports ===
import unittest
from unittest.mock import patch
from typing import Any, Dict

# === relative import for UUT ===
from ._parse_function_call_src import _parse_function_call

# === type aliases ===
Token = Dict[str, Any]
AST = Dict[str, Any]
ParserState = Dict[str, Any]


class TestParseFunctionCall(unittest.TestCase):
    """Test cases for _parse_function_call function."""

    def test_empty_argument_list(self):
        """Test parsing function call with no arguments: func()"""
        tokens: list[Token] = [
            {"type": "LPAREN", "value": "(", "line": 1, "column": 5},
            {"type": "RPAREN", "value": ")", "line": 1, "column": 6},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_function_call(parser_state, "func", 1, 1)
        
        self.assertEqual(result["type"], "CALL")
        self.assertEqual(result["value"], "func")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(result["children"], [])
        self.assertEqual(parser_state["pos"], 2)

    def test_single_argument(self):
        """Test parsing function call with one argument: func(arg1)"""
        tokens: list[Token] = [
            {"type": "LPAREN", "value": "(", "line": 1, "column": 5},
            {"type": "IDENTIFIER", "value": "arg1", "line": 1, "column": 6},
            {"type": "RPAREN", "value": ")", "line": 1, "column": 10},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        mock_arg_ast: AST = {
            "type": "IDENTIFIER",
            "value": "arg1",
            "line": 1,
            "column": 6
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_return_stmt_package._parse_expression_package._parse_primary_package._parse_function_call_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = mock_arg_ast
            mock_parse_expr.side_effect = lambda state: state.update({"pos": 2}) or mock_arg_ast
            
            result = _parse_function_call(parser_state, "func", 1, 1)
        
        self.assertEqual(result["type"], "CALL")
        self.assertEqual(result["value"], "func")
        self.assertEqual(len(result["children"]), 1)
        self.assertEqual(result["children"][0]["value"], "arg1")
        self.assertEqual(parser_state["pos"], 3)

    def test_multiple_arguments(self):
        """Test parsing function call with multiple arguments: func(arg1, arg2, arg3)"""
        tokens: list[Token] = [
            {"type": "LPAREN", "value": "(", "line": 1, "column": 5},
            {"type": "IDENTIFIER", "value": "arg1", "line": 1, "column": 6},
            {"type": "COMMA", "value": ",", "line": 1, "column": 10},
            {"type": "IDENTIFIER", "value": "arg2", "line": 1, "column": 12},
            {"type": "COMMA", "value": ",", "line": 1, "column": 16},
            {"type": "IDENTIFIER", "value": "arg3", "line": 1, "column": 18},
            {"type": "RPAREN", "value": ")", "line": 1, "column": 22},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        call_count = [0]
        def mock_parse_expression(state: ParserState) -> AST:
            call_count[0] += 1
            pos = state["pos"]
            arg_name = f"arg{call_count[0]}"
            state["pos"] = pos + 2 if call_count[0] < 3 else pos + 1
            return {
                "type": "IDENTIFIER",
                "value": arg_name,
                "line": 1,
                "column": pos
            }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_return_stmt_package._parse_expression_package._parse_primary_package._parse_function_call_package._parse_expression_package._parse_expression_src._parse_expression", side_effect=mock_parse_expression):
            result = _parse_function_call(parser_state, "func", 1, 1)
        
        self.assertEqual(result["type"], "CALL")
        self.assertEqual(result["value"], "func")
        self.assertEqual(len(result["children"]), 3)
        self.assertEqual(result["children"][0]["value"], "arg1")
        self.assertEqual(result["children"][1]["value"], "arg2")
        self.assertEqual(result["children"][2]["value"], "arg3")
        self.assertEqual(parser_state["pos"], 7)

    def test_missing_open_paren_raises_error(self):
        """Test that missing '(' raises SyntaxError"""
        tokens: list[Token] = [
            {"type": "IDENTIFIER", "value": "arg1", "line": 1, "column": 6},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_function_call(parser_state, "func", 1, 1)
        
        self.assertIn("Expected '('", str(context.exception))
        self.assertIn("line 1", str(context.exception))
        self.assertIn("column 1", str(context.exception))

    def test_missing_close_paren_raises_error(self):
        """Test that missing ')' raises SyntaxError"""
        tokens: list[Token] = [
            {"type": "LPAREN", "value": "(", "line": 1, "column": 5},
            {"type": "IDENTIFIER", "value": "arg1", "line": 1, "column": 6},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        mock_arg_ast: AST = {
            "type": "IDENTIFIER",
            "value": "arg1",
            "line": 1,
            "column": 6
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_return_stmt_package._parse_expression_package._parse_primary_package._parse_function_call_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = mock_arg_ast
            mock_parse_expr.side_effect = lambda state: state.update({"pos": 2}) or mock_arg_ast
            
            with self.assertRaises(SyntaxError) as context:
                _parse_function_call(parser_state, "func", 1, 1)
        
        self.assertIn("Expected ')'", str(context.exception))

    def test_trailing_comma_raises_error(self):
        """Test that trailing comma raises SyntaxError: func(arg1,)"""
        tokens: list[Token] = [
            {"type": "LPAREN", "value": "(", "line": 1, "column": 5},
            {"type": "IDENTIFIER", "value": "arg1", "line": 1, "column": 6},
            {"type": "COMMA", "value": ",", "line": 1, "column": 10},
            {"type": "RPAREN", "value": ")", "line": 1, "column": 11},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        mock_arg_ast: AST = {
            "type": "IDENTIFIER",
            "value": "arg1",
            "line": 1,
            "column": 6
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_return_stmt_package._parse_expression_package._parse_primary_package._parse_function_call_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = mock_arg_ast
            mock_parse_expr.side_effect = lambda state: state.update({"pos": 2}) or mock_arg_ast
            
            with self.assertRaises(SyntaxError) as context:
                _parse_function_call(parser_state, "func", 1, 1)
        
        self.assertIn("Expected expression after ','", str(context.exception))

    def test_empty_argument_after_comma_raises_error(self):
        """Test that empty argument after comma raises SyntaxError: func(arg1, )"""
        tokens: list[Token] = [
            {"type": "LPAREN", "value": "(", "line": 1, "column": 5},
            {"type": "IDENTIFIER", "value": "arg1", "line": 1, "column": 6},
            {"type": "COMMA", "value": ",", "line": 1, "column": 10},
            {"type": "RPAREN", "value": ")", "line": 1, "column": 12},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        mock_arg_ast: AST = {
            "type": "IDENTIFIER",
            "value": "arg1",
            "line": 1,
            "column": 6
        }
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_if_stmt_package._parse_block_package._parse_statement_package._parse_return_stmt_package._parse_expression_package._parse_primary_package._parse_function_call_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.return_value = mock_arg_ast
            mock_parse_expr.side_effect = lambda state: state.update({"pos": 2}) or mock_arg_ast
            
            with self.assertRaises(SyntaxError) as context:
                _parse_function_call(parser_state, "func", 1, 1)
        
        self.assertIn("Expected expression after ','", str(context.exception))

    def test_position_updated_correctly(self):
        """Test that parser_state position is updated correctly"""
        tokens: list[Token] = [
            {"type": "LPAREN", "value": "(", "line": 1, "column": 5},
            {"type": "RPAREN", "value": ")", "line": 1, "column": 6},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        _parse_function_call(parser_state, "func", 1, 1)
        
        self.assertEqual(parser_state["pos"], 2)

    def test_ast_node_contains_correct_metadata(self):
        """Test that returned AST node contains correct line and column metadata"""
        tokens: list[Token] = [
            {"type": "LPAREN", "value": "(", "line": 5, "column": 10},
            {"type": "RPAREN", "value": ")", "line": 5, "column": 11},
        ]
        parser_state: ParserState = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_function_call(parser_state, "my_func", 5, 3)
        
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 3)
        self.assertEqual(result["value"], "my_func")


if __name__ == "__main__":
    unittest.main()

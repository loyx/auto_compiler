import unittest
from unittest.mock import patch
from typing import Dict, Any, List

from ._parse_function_def_src import _parse_function_def


class TestParseFunctionDef(unittest.TestCase):
    """Test cases for _parse_function_def function."""
    
    def _create_token(self, token_type: str, value: str, line: int = 1, column: int = 1) -> Dict[str, Any]:
        """Helper to create a token dict."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }
    
    def _create_parser_state(self, tokens: List[Dict], pos: int = 0, filename: str = "test.c") -> Dict[str, Any]:
        """Helper to create a parser state dict."""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename
        }
    
    def test_happy_path_simple_function(self):
        """Test parsing a simple function with no parameters."""
        tokens = [
            self._create_token("TYPE", "void", 1, 1),
            self._create_token("IDENTIFIER", "main", 1, 6),
            self._create_token("LPAREN", "(", 1, 10),
            self._create_token("RPAREN", ")", 1, 11),
            self._create_token("LBRACE", "{", 1, 13),
        ]
        
        parser_state = self._create_parser_state(tokens, 0)
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_function_def_src._parse_block") as mock_parse_block:
            mock_parse_block.return_value = {"type": "BLOCK", "children": []}
            
            result = _parse_function_def(parser_state)
            
            self.assertEqual(result["type"], "FUNCTION_DEF")
            self.assertEqual(result["value"], "main")
            self.assertEqual(result["return_type"], "void")
            self.assertEqual(result["params"], [])
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 6)
            mock_parse_block.assert_called_once()
    
    def test_happy_path_function_with_params(self):
        """Test parsing a function with parameters."""
        tokens = [
            self._create_token("TYPE", "int", 1, 1),
            self._create_token("IDENTIFIER", "add", 1, 5),
            self._create_token("LPAREN", "(", 1, 8),
            self._create_token("TYPE", "int", 1, 9),
            self._create_token("IDENTIFIER", "a", 1, 13),
            self._create_token("COMMA", ",", 1, 14),
            self._create_token("TYPE", "int", 1, 16),
            self._create_token("IDENTIFIER", "b", 1, 20),
            self._create_token("RPAREN", ")", 1, 21),
            self._create_token("LBRACE", "{", 1, 23),
        ]
        
        parser_state = self._create_parser_state(tokens, 0)
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_function_def_src._parse_block") as mock_parse_block:
            with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_function_def_src._parse_param_list") as mock_parse_param:
                mock_params = [
                    {"type": "PARAM", "value": "a", "param_type": "int"},
                    {"type": "PARAM", "value": "b", "param_type": "int"}
                ]
                mock_parse_param.return_value = (mock_params, 8)
                mock_parse_block.return_value = {"type": "BLOCK", "children": []}
                
                result = _parse_function_def(parser_state)
                
                self.assertEqual(result["type"], "FUNCTION_DEF")
                self.assertEqual(result["value"], "add")
                self.assertEqual(result["return_type"], "int")
                self.assertEqual(len(result["params"]), 2)
                mock_parse_param.assert_called_once()
                mock_parse_block.assert_called_once()
    
    def test_error_eof_at_return_type(self):
        """Test error when EOF encountered at return type."""
        tokens = []
        parser_state = self._create_parser_state(tokens, 0, "test.c")
        
        with self.assertRaises(SyntaxError) as context:
            _parse_function_def(parser_state)
        
        self.assertIn("expected return type", str(context.exception))
        self.assertIn("test.c", str(context.exception))
    
    def test_error_eof_at_function_name(self):
        """Test error when EOF encountered after return type."""
        tokens = [
            self._create_token("TYPE", "void", 1, 1),
        ]
        parser_state = self._create_parser_state(tokens, 0, "test.c")
        
        with self.assertRaises(SyntaxError) as context:
            _parse_function_def(parser_state)
        
        self.assertIn("expected function name", str(context.exception))
    
    def test_error_non_identifier_function_name(self):
        """Test error when function name is not an identifier."""
        tokens = [
            self._create_token("TYPE", "void", 1, 1),
            self._create_token("TYPE", "int", 1, 6),
        ]
        parser_state = self._create_parser_state(tokens, 0, "test.c")
        
        with self.assertRaises(SyntaxError) as context:
            _parse_function_def(parser_state)
        
        self.assertIn("expected function name", str(context.exception))
        self.assertIn("1", str(context.exception))
        self.assertIn("6", str(context.exception))
    
    def test_error_missing_left_paren(self):
        """Test error when '(' is missing after function name."""
        tokens = [
            self._create_token("TYPE", "void", 1, 1),
            self._create_token("IDENTIFIER", "main", 1, 6),
            self._create_token("LBRACE", "{", 1, 11),
        ]
        parser_state = self._create_parser_state(tokens, 0, "test.c")
        
        with self.assertRaises(SyntaxError) as context:
            _parse_function_def(parser_state)
        
        self.assertIn("expected '('", str(context.exception))
    
    def test_error_missing_right_paren(self):
        """Test error when ')' is missing after parameter list."""
        tokens = [
            self._create_token("TYPE", "void", 1, 1),
            self._create_token("IDENTIFIER", "main", 1, 6),
            self._create_token("LPAREN", "(", 1, 10),
            self._create_token("LBRACE", "{", 1, 11),
        ]
        parser_state = self._create_parser_state(tokens, 0, "test.c")
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_function_def_src._parse_param_list") as mock_parse_param:
            mock_parse_param.return_value = ([], 3)
            
            with self.assertRaises(SyntaxError) as context:
                _parse_function_def(parser_state)
            
            self.assertIn("expected ')'", str(context.exception))
    
    def test_error_missing_left_brace(self):
        """Test error when '{' is missing before function body."""
        tokens = [
            self._create_token("TYPE", "void", 1, 1),
            self._create_token("IDENTIFIER", "main", 1, 6),
            self._create_token("LPAREN", "(", 1, 10),
            self._create_token("RPAREN", ")", 1, 11),
        ]
        parser_state = self._create_parser_state(tokens, 0, "test.c")
        
        with self.assertRaises(SyntaxError) as context:
            _parse_function_def(parser_state)
        
        self.assertIn("expected '{'", str(context.exception))
    
    def test_parser_state_pos_updated(self):
        """Test that parser_state pos is updated before calling _parse_block."""
        tokens = [
            self._create_token("TYPE", "void", 1, 1),
            self._create_token("IDENTIFIER", "main", 1, 6),
            self._create_token("LPAREN", "(", 1, 10),
            self._create_token("RPAREN", ")", 1, 11),
            self._create_token("LBRACE", "{", 1, 13),
        ]
        parser_state = self._create_parser_state(tokens, 0, "test.c")
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_function_def_src._parse_block") as mock_parse_block:
            mock_parse_block.return_value = {"type": "BLOCK", "children": []}
            
            _parse_function_def(parser_state)
            
            self.assertEqual(parser_state["pos"], 5)
    
    def test_function_with_complex_return_type(self):
        """Test parsing function with complex return type like 'unsigned int'."""
        tokens = [
            self._create_token("TYPE", "unsigned", 1, 1),
            self._create_token("IDENTIFIER", "getValue", 1, 10),
            self._create_token("LPAREN", "(", 1, 18),
            self._create_token("RPAREN", ")", 1, 19),
            self._create_token("LBRACE", "{", 1, 21),
        ]
        
        parser_state = self._create_parser_state(tokens, 0, "test.c")
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_function_def_src._parse_block") as mock_parse_block:
            mock_parse_block.return_value = {"type": "BLOCK", "children": []}
            
            result = _parse_function_def(parser_state)
            
            self.assertEqual(result["return_type"], "unsigned")
            self.assertEqual(result["value"], "getValue")
    
    def test_error_custom_filename(self):
        """Test error messages include custom filename."""
        tokens = []
        parser_state = self._create_parser_state(tokens, 0, "my_custom_file.c")
        
        with self.assertRaises(SyntaxError) as context:
            _parse_function_def(parser_state)
        
        self.assertIn("my_custom_file.c", str(context.exception))
    
    def test_error_default_filename(self):
        """Test error messages include default filename when not provided."""
        tokens = []
        parser_state = {
            "tokens": tokens,
            "pos": 0
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_function_def(parser_state)
        
        self.assertIn("<unknown>", str(context.exception))


if __name__ == "__main__":
    unittest.main()

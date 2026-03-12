import unittest
from typing import Any, Dict

from ._parse_type_annotation_src import _parse_type_annotation


Token = Dict[str, Any]
ParserState = Dict[str, Any]


class TestParseTypeAnnotation(unittest.TestCase):
    """Test cases for _parse_type_annotation function."""
    
    def _create_parser_state(self, tokens: list, pos: int = 0) -> ParserState:
        """Helper to create parser state dict."""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": "test.py"
        }
    
    def _create_token(self, token_type: str, value: str, line: int = 1, column: int = 1) -> Token:
        """Helper to create a token dict."""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }
    
    def test_simple_type_int(self):
        """Test parsing simple type 'int'."""
        tokens = [
            self._create_token("IDENT", "int", line=1, column=5)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        result = _parse_type_annotation(parser_state)
        
        self.assertEqual(result["type"], "NAME")
        self.assertEqual(result["value"], "int")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 5)
        self.assertEqual(parser_state["pos"], 1)
    
    def test_simple_type_str(self):
        """Test parsing simple type 'str'."""
        tokens = [
            self._create_token("IDENT", "str", line=2, column=10)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        result = _parse_type_annotation(parser_state)
        
        self.assertEqual(result["type"], "NAME")
        self.assertEqual(result["value"], "str")
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 10)
        self.assertEqual(parser_state["pos"], 1)
    
    def test_simple_type_custom_class(self):
        """Test parsing simple custom type 'MyClass'."""
        tokens = [
            self._create_token("IDENT", "MyClass", line=3, column=15)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        result = _parse_type_annotation(parser_state)
        
        self.assertEqual(result["type"], "NAME")
        self.assertEqual(result["value"], "MyClass")
        self.assertEqual(result["line"], 3)
        self.assertEqual(result["column"], 15)
        self.assertEqual(parser_state["pos"], 1)
    
    def test_generic_type_single_arg(self):
        """Test parsing generic type 'List[int]'."""
        tokens = [
            self._create_token("IDENT", "List", line=1, column=5),
            self._create_token("LBRACKET", "[", line=1, column=9),
            self._create_token("IDENT", "int", line=1, column=10),
            self._create_token("RBRACKET", "]", line=1, column=13)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        result = _parse_type_annotation(parser_state)
        
        self.assertEqual(result["type"], "GENERIC")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 5)
        self.assertEqual(len(result["children"]), 2)
        self.assertEqual(result["children"][0]["type"], "NAME")
        self.assertEqual(result["children"][0]["value"], "List")
        self.assertEqual(result["children"][1]["type"], "TYPE_ARGS")
        self.assertEqual(len(result["children"][1]["children"]), 1)
        self.assertEqual(result["children"][1]["children"][0]["type"], "NAME")
        self.assertEqual(result["children"][1]["children"][0]["value"], "int")
        self.assertEqual(parser_state["pos"], 4)
    
    def test_generic_type_multiple_args(self):
        """Test parsing generic type 'Dict[str, int]'."""
        tokens = [
            self._create_token("IDENT", "Dict", line=1, column=5),
            self._create_token("LBRACKET", "[", line=1, column=9),
            self._create_token("IDENT", "str", line=1, column=10),
            self._create_token("COMMA", ",", line=1, column=13),
            self._create_token("IDENT", "int", line=1, column=15),
            self._create_token("RBRACKET", "]", line=1, column=16)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        result = _parse_type_annotation(parser_state)
        
        self.assertEqual(result["type"], "GENERIC")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 5)
        self.assertEqual(len(result["children"]), 2)
        self.assertEqual(result["children"][0]["type"], "NAME")
        self.assertEqual(result["children"][0]["value"], "Dict")
        self.assertEqual(result["children"][1]["type"], "TYPE_ARGS")
        self.assertEqual(len(result["children"][1]["children"]), 2)
        self.assertEqual(result["children"][1]["children"][0]["type"], "NAME")
        self.assertEqual(result["children"][1]["children"][0]["value"], "str")
        self.assertEqual(result["children"][1]["children"][1]["type"], "NAME")
        self.assertEqual(result["children"][1]["children"][1]["value"], "int")
        self.assertEqual(parser_state["pos"], 6)
    
    def test_generic_type_three_args(self):
        """Test parsing generic type 'Tuple[int, str, bool]'."""
        tokens = [
            self._create_token("IDENT", "Tuple", line=1, column=5),
            self._create_token("LBRACKET", "[", line=1, column=10),
            self._create_token("IDENT", "int", line=1, column=11),
            self._create_token("COMMA", ",", line=1, column=14),
            self._create_token("IDENT", "str", line=1, column=16),
            self._create_token("COMMA", ",", line=1, column=19),
            self._create_token("IDENT", "bool", line=1, column=21),
            self._create_token("RBRACKET", "]", line=1, column=25)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        result = _parse_type_annotation(parser_state)
        
        self.assertEqual(result["type"], "GENERIC")
        self.assertEqual(result["children"][0]["value"], "Tuple")
        type_args = result["children"][1]["children"]
        self.assertEqual(len(type_args), 3)
        self.assertEqual(type_args[0]["value"], "int")
        self.assertEqual(type_args[1]["value"], "str")
        self.assertEqual(type_args[2]["value"], "bool")
        self.assertEqual(parser_state["pos"], 8)
    
    def test_nested_generic_type(self):
        """Test parsing nested generic type 'List[List[int]]'."""
        tokens = [
            self._create_token("IDENT", "List", line=1, column=5),
            self._create_token("LBRACKET", "[", line=1, column=9),
            self._create_token("IDENT", "List", line=1, column=10),
            self._create_token("LBRACKET", "[", line=1, column=14),
            self._create_token("IDENT", "int", line=1, column=15),
            self._create_token("RBRACKET", "]", line=1, column=18),
            self._create_token("RBRACKET", "]", line=1, column=19)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        result = _parse_type_annotation(parser_state)
        
        self.assertEqual(result["type"], "GENERIC")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 5)
        self.assertEqual(len(result["children"]), 2)
        self.assertEqual(result["children"][0]["type"], "NAME")
        self.assertEqual(result["children"][0]["value"], "List")
        
        # Check TYPE_ARGS
        type_args = result["children"][1]
        self.assertEqual(type_args["type"], "TYPE_ARGS")
        self.assertEqual(len(type_args["children"]), 1)
        
        # Check nested generic
        nested_generic = type_args["children"][0]
        self.assertEqual(nested_generic["type"], "GENERIC")
        self.assertEqual(nested_generic["children"][0]["value"], "List")
        nested_type_args = nested_generic["children"][1]
        self.assertEqual(nested_type_args["children"][0]["value"], "int")
        
        self.assertEqual(parser_state["pos"], 7)
    
    def test_deeply_nested_generic_type(self):
        """Test parsing deeply nested generic type 'Optional[List[Dict[str, int]]]'."""
        tokens = [
            self._create_token("IDENT", "Optional", line=1, column=5),
            self._create_token("LBRACKET", "[", line=1, column=13),
            self._create_token("IDENT", "List", line=1, column=14),
            self._create_token("LBRACKET", "[", line=1, column=18),
            self._create_token("IDENT", "Dict", line=1, column=19),
            self._create_token("LBRACKET", "[", line=1, column=23),
            self._create_token("IDENT", "str", line=1, column=24),
            self._create_token("COMMA", ",", line=1, column=27),
            self._create_token("IDENT", "int", line=1, column=29),
            self._create_token("RBRACKET", "]", line=1, column=32),
            self._create_token("RBRACKET", "]", line=1, column=33),
            self._create_token("RBRACKET", "]", line=1, column=34)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        result = _parse_type_annotation(parser_state)
        
        self.assertEqual(result["type"], "GENERIC")
        self.assertEqual(result["children"][0]["value"], "Optional")
        self.assertEqual(parser_state["pos"], 12)
    
    def test_empty_generic_args(self):
        """Test parsing generic type with empty args 'List[]'."""
        tokens = [
            self._create_token("IDENT", "List", line=1, column=5),
            self._create_token("LBRACKET", "[", line=1, column=9),
            self._create_token("RBRACKET", "]", line=1, column=10)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        result = _parse_type_annotation(parser_state)
        
        self.assertEqual(result["type"], "GENERIC")
        self.assertEqual(result["children"][0]["value"], "List")
        self.assertEqual(result["children"][1]["children"], [])
        self.assertEqual(parser_state["pos"], 3)
    
    def test_empty_tokens_raises_error(self):
        """Test that empty token list raises SyntaxError."""
        parser_state = self._create_parser_state([], pos=0)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_type_annotation(parser_state)
        
        self.assertIn("Expected type name", str(context.exception))
    
    def test_non_ident_token_raises_error(self):
        """Test that non-IDENT token raises SyntaxError."""
        tokens = [
            self._create_token("LBRACKET", "[", line=1, column=5)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_type_annotation(parser_state)
        
        self.assertIn("Expected type name", str(context.exception))
    
    def test_missing_closing_bracket_raises_error(self):
        """Test that missing closing bracket raises SyntaxError."""
        tokens = [
            self._create_token("IDENT", "List", line=1, column=5),
            self._create_token("LBRACKET", "[", line=1, column=9),
            self._create_token("IDENT", "int", line=1, column=10)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_type_annotation(parser_state)
        
        self.assertIn("Expected ']'", str(context.exception))
    
    def test_missing_closing_bracket_after_comma_raises_error(self):
        """Test that missing closing bracket after comma raises SyntaxError."""
        tokens = [
            self._create_token("IDENT", "Dict", line=1, column=5),
            self._create_token("LBRACKET", "[", line=1, column=9),
            self._create_token("IDENT", "str", line=1, column=10),
            self._create_token("COMMA", ",", line=1, column=13),
            self._create_token("IDENT", "int", line=1, column=15)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_type_annotation(parser_state)
        
        self.assertIn("Expected ']'", str(context.exception))
    
    def test_pos_at_end_raises_error(self):
        """Test that pos at end of tokens raises SyntaxError."""
        tokens = [
            self._create_token("IDENT", "int", line=1, column=5)
        ]
        parser_state = self._create_parser_state(tokens, pos=1)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_type_annotation(parser_state)
        
        self.assertIn("Expected type name", str(context.exception))
    
    def test_pos_updated_correctly_simple_type(self):
        """Test that parser_state pos is updated correctly for simple type."""
        tokens = [
            self._create_token("IDENT", "int", line=1, column=5),
            self._create_token("COMMA", ",", line=1, column=8)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        result = _parse_type_annotation(parser_state)
        
        # Should only consume the IDENT token
        self.assertEqual(parser_state["pos"], 1)
        self.assertEqual(result["value"], "int")
    
    def test_pos_updated_correctly_generic_type(self):
        """Test that parser_state pos is updated correctly for generic type."""
        tokens = [
            self._create_token("IDENT", "List", line=1, column=5),
            self._create_token("LBRACKET", "[", line=1, column=9),
            self._create_token("IDENT", "int", line=1, column=10),
            self._create_token("RBRACKET", "]", line=1, column=13),
            self._create_token("COMMA", ",", line=1, column=14)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        result = _parse_type_annotation(parser_state)
        
        # Should consume all 4 tokens of List[int]
        self.assertEqual(parser_state["pos"], 4)
        self.assertEqual(result["type"], "GENERIC")
    
    def test_line_column_preserved(self):
        """Test that line and column information is preserved correctly."""
        tokens = [
            self._create_token("IDENT", "MyType", line=10, column=25)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        result = _parse_type_annotation(parser_state)
        
        self.assertEqual(result["line"], 10)
        self.assertEqual(result["column"], 25)
    
    def test_line_column_preserved_generic(self):
        """Test that line and column information is preserved for generic types."""
        tokens = [
            self._create_token("IDENT", "Generic", line=5, column=30),
            self._create_token("LBRACKET", "[", line=5, column=37),
            self._create_token("IDENT", "T", line=5, column=38),
            self._create_token("RBRACKET", "]", line=5, column=39)
        ]
        parser_state = self._create_parser_state(tokens, pos=0)
        
        result = _parse_type_annotation(parser_state)
        
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 30)


if __name__ == "__main__":
    unittest.main()

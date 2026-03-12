"""
Unit tests for _parse_param_list function.
"""
import unittest
from typing import Any, Dict, List

from ._parse_param_list_src import _parse_param_list


class TestParseParamList(unittest.TestCase):
    """Test cases for _parse_param_list function."""

    def _create_parser_state(self, tokens: List[Dict[str, Any]], filename: str = "test.py") -> Dict[str, Any]:
        """Helper to create parser state dictionary."""
        return {
            "tokens": tokens,
            "pos": 0,
            "filename": filename
        }

    def test_single_parameter(self):
        """Test parsing a single parameter."""
        tokens = [
            {"type": "TYPE", "value": "int", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 5},
            {"type": "RPAREN", "value": ")", "line": 1, "column": 6}
        ]
        parser_state = self._create_parser_state(tokens)
        
        params, new_pos = _parse_param_list(parser_state, 0)
        
        self.assertEqual(len(params), 1)
        self.assertEqual(params[0]["type"], "PARAM")
        self.assertEqual(params[0]["value"], "x")
        self.assertEqual(params[0]["param_type"], "int")
        self.assertEqual(params[0]["line"], 1)
        self.assertEqual(params[0]["column"], 1)
        self.assertEqual(new_pos, 2)

    def test_multiple_parameters(self):
        """Test parsing multiple comma-separated parameters."""
        tokens = [
            {"type": "TYPE", "value": "int", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 5},
            {"type": "COMMA", "value": ",", "line": 1, "column": 6},
            {"type": "TYPE", "value": "str", "line": 1, "column": 8},
            {"type": "IDENTIFIER", "value": "name", "line": 1, "column": 12},
            {"type": "RPAREN", "value": ")", "line": 1, "column": 16}
        ]
        parser_state = self._create_parser_state(tokens)
        
        params, new_pos = _parse_param_list(parser_state, 0)
        
        self.assertEqual(len(params), 2)
        self.assertEqual(params[0]["value"], "x")
        self.assertEqual(params[0]["param_type"], "int")
        self.assertEqual(params[1]["value"], "name")
        self.assertEqual(params[1]["param_type"], "str")
        self.assertEqual(new_pos, 5)

    def test_empty_parameter_list(self):
        """Test parsing empty parameter list (immediately RPAREN)."""
        tokens = [
            {"type": "RPAREN", "value": ")", "line": 1, "column": 1}
        ]
        parser_state = self._create_parser_state(tokens)
        
        params, new_pos = _parse_param_list(parser_state, 0)
        
        self.assertEqual(len(params), 0)
        self.assertEqual(new_pos, 0)

    def test_type_without_identifier_eof(self):
        """Test error when type is not followed by identifier (end of tokens)."""
        tokens = [
            {"type": "TYPE", "value": "int", "line": 1, "column": 1}
        ]
        parser_state = self._create_parser_state(tokens)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_param_list(parser_state, 0)
        
        self.assertIn("Expected identifier after type 'int'", str(context.exception))
        self.assertIn("test.py:1:1", str(context.exception))

    def test_type_without_identifier_wrong_token(self):
        """Test error when type is followed by non-identifier token."""
        tokens = [
            {"type": "TYPE", "value": "int", "line": 1, "column": 1},
            {"type": "COMMA", "value": ",", "line": 1, "column": 5}
        ]
        parser_state = self._create_parser_state(tokens)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_param_list(parser_state, 0)
        
        self.assertIn("Expected identifier after type 'int'", str(context.exception))
        self.assertIn("got ','", str(context.exception))

    def test_parameter_list_with_trailing_comma_stops(self):
        """Test that trailing comma without following param stops parsing."""
        tokens = [
            {"type": "TYPE", "value": "int", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 5},
            {"type": "COMMA", "value": ",", "line": 1, "column": 6}
        ]
        parser_state = self._create_parser_state(tokens)
        
        params, new_pos = _parse_param_list(parser_state, 0)
        
        self.assertEqual(len(params), 1)
        self.assertEqual(params[0]["value"], "x")
        self.assertEqual(new_pos, 3)

    def test_parameter_list_stops_at_unexpected_token(self):
        """Test that parameter list stops at unexpected token (not comma or RPAREN)."""
        tokens = [
            {"type": "TYPE", "value": "int", "line": 1, "column": 1},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 5},
            {"type": "TYPE", "value": "str", "line": 1, "column": 7}
        ]
        parser_state = self._create_parser_state(tokens)
        
        params, new_pos = _parse_param_list(parser_state, 0)
        
        self.assertEqual(len(params), 1)
        self.assertEqual(params[0]["value"], "x")
        self.assertEqual(new_pos, 2)

    def test_starts_at_non_type_token(self):
        """Test when starting position is not a TYPE token."""
        tokens = [
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1},
            {"type": "RPAREN", "value": ")", "line": 1, "column": 2}
        ]
        parser_state = self._create_parser_state(tokens)
        
        params, new_pos = _parse_param_list(parser_state, 0)
        
        self.assertEqual(len(params), 0)
        self.assertEqual(new_pos, 0)

    def test_custom_filename_in_error(self):
        """Test that custom filename appears in error message."""
        tokens = [
            {"type": "TYPE", "value": "int", "line": 5, "column": 10}
        ]
        parser_state = self._create_parser_state(tokens, filename="custom_file.py")
        
        with self.assertRaises(SyntaxError) as context:
            _parse_param_list(parser_state, 0)
        
        self.assertIn("custom_file.py:5:10", str(context.exception))

    def test_complex_parameter_types(self):
        """Test parsing parameters with complex type names."""
        tokens = [
            {"type": "TYPE", "value": "List[str]", "line": 2, "column": 1},
            {"type": "IDENTIFIER", "value": "items", "line": 2, "column": 11},
            {"type": "COMMA", "value": ",", "line": 2, "column": 16},
            {"type": "TYPE", "value": "Dict[str,Any]", "line": 2, "column": 18},
            {"type": "IDENTIFIER", "value": "mapping", "line": 2, "column": 32},
            {"type": "RPAREN", "value": ")", "line": 2, "column": 39}
        ]
        parser_state = self._create_parser_state(tokens)
        
        params, new_pos = _parse_param_list(parser_state, 0)
        
        self.assertEqual(len(params), 2)
        self.assertEqual(params[0]["param_type"], "List[str]")
        self.assertEqual(params[0]["value"], "items")
        self.assertEqual(params[1]["param_type"], "Dict[str,Any]")
        self.assertEqual(params[1]["value"], "mapping")


if __name__ == "__main__":
    unittest.main()

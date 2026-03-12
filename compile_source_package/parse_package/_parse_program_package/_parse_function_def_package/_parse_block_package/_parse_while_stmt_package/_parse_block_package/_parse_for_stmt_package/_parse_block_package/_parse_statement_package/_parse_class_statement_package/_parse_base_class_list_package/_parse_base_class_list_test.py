# -*- coding: utf-8 -*-
"""Unit tests for _parse_base_class_list function."""

import unittest
from ._parse_base_class_list_src import _parse_base_class_list


class TestParseBaseClassList(unittest.TestCase):
    """Test cases for _parse_base_class_list parser function."""

    def test_single_base_class(self):
        """Test parsing a single base class."""
        tokens = [
            {"type": "IDENT", "value": "BaseClass", "line": 1, "column": 10},
            {"type": "RPAREN", "value": ")", "line": 1, "column": 20},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.py"}
        
        result = _parse_base_class_list(parser_state)
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["type"], "BASE")
        self.assertEqual(result[0]["value"], "BaseClass")
        self.assertEqual(result[0]["line"], 1)
        self.assertEqual(result[0]["column"], 10)
        self.assertEqual(parser_state["pos"], 1)

    def test_multiple_base_classes(self):
        """Test parsing multiple base classes separated by commas."""
        tokens = [
            {"type": "IDENT", "value": "Base1", "line": 1, "column": 10},
            {"type": "COMMA", "value": ",", "line": 1, "column": 15},
            {"type": "IDENT", "value": "Base2", "line": 1, "column": 17},
            {"type": "COMMA", "value": ",", "line": 1, "column": 22},
            {"type": "IDENT", "value": "Base3", "line": 1, "column": 24},
            {"type": "RPAREN", "value": ")", "line": 1, "column": 30},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.py"}
        
        result = _parse_base_class_list(parser_state)
        
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]["value"], "Base1")
        self.assertEqual(result[1]["value"], "Base2")
        self.assertEqual(result[2]["value"], "Base3")
        self.assertEqual(parser_state["pos"], 5)

    def test_empty_base_class_list(self):
        """Test parsing when immediately encountering non-IDENT token."""
        tokens = [
            {"type": "RPAREN", "value": ")", "line": 1, "column": 10},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.py"}
        
        result = _parse_base_class_list(parser_state)
        
        self.assertEqual(len(result), 0)
        self.assertEqual(parser_state["pos"], 0)

    def test_no_trailing_comma(self):
        """Test parsing base classes without trailing comma."""
        tokens = [
            {"type": "IDENT", "value": "Base1", "line": 1, "column": 10},
            {"type": "COMMA", "value": ",", "line": 1, "column": 15},
            {"type": "IDENT", "value": "Base2", "line": 1, "column": 17},
            {"type": "RPAREN", "value": ")", "line": 1, "column": 22},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.py"}
        
        result = _parse_base_class_list(parser_state)
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["value"], "Base1")
        self.assertEqual(result[1]["value"], "Base2")
        self.assertEqual(parser_state["pos"], 3)

    def test_pos_at_end_of_tokens(self):
        """Test parsing when pos starts at end of token list."""
        tokens = [
            {"type": "IDENT", "value": "Base", "line": 1, "column": 10},
        ]
        parser_state = {"tokens": tokens, "pos": 1, "filename": "test.py"}
        
        result = _parse_base_class_list(parser_state)
        
        self.assertEqual(len(result), 0)
        self.assertEqual(parser_state["pos"], 1)

    def test_non_ident_token_stops_parsing(self):
        """Test that non-IDENT, non-COMMA token stops parsing."""
        tokens = [
            {"type": "IDENT", "value": "Base1", "line": 1, "column": 10},
            {"type": "COMMA", "value": ",", "line": 1, "column": 15},
            {"type": "KEYWORD", "value": "class", "line": 1, "column": 17},
            {"type": "IDENT", "value": "Base2", "line": 1, "column": 23},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.py"}
        
        result = _parse_base_class_list(parser_state)
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["value"], "Base1")
        self.assertEqual(parser_state["pos"], 2)

    def test_preserves_original_token_info(self):
        """Test that AST nodes preserve line and column from tokens."""
        tokens = [
            {"type": "IDENT", "value": "Base", "line": 5, "column": 25},
            {"type": "RPAREN", "value": ")", "line": 5, "column": 30},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.py"}
        
        result = _parse_base_class_list(parser_state)
        
        self.assertEqual(result[0]["line"], 5)
        self.assertEqual(result[0]["column"], 25)

    def test_modifies_parser_state_in_place(self):
        """Test that parser_state is modified in place."""
        tokens = [
            {"type": "IDENT", "value": "Base", "line": 1, "column": 10},
            {"type": "RPAREN", "value": ")", "line": 1, "column": 15},
        ]
        parser_state = {"tokens": tokens, "pos": 0, "filename": "test.py"}
        original_state_id = id(parser_state)
        
        result = _parse_base_class_list(parser_state)
        
        self.assertEqual(id(parser_state), original_state_id)
        self.assertEqual(parser_state["pos"], 1)
        self.assertIn("tokens", parser_state)
        self.assertIn("filename", parser_state)


if __name__ == "__main__":
    unittest.main()

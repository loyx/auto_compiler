import unittest
from .make_error_node_src import make_error_node


class TestMakeErrorNode(unittest.TestCase):
    """Test cases for make_error_node function."""

    def test_priority_1_last_consumed_token(self):
        """Test when pos > 0, should use tokens[pos - 1] (last consumed token)."""
        tokens = [
            {"type": "IDENT", "value": "x", "line": 1, "column": 5},
            {"type": "OP", "value": "+", "line": 1, "column": 7},
            {"type": "NUM", "value": "5", "line": 1, "column": 9},
        ]
        pos = 2  # Should use tokens[1]
        result = make_error_node(pos, tokens)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertIsNone(result["value"])
        self.assertEqual(result["children"], [])
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 7)

    def test_priority_1_pos_equals_len_tokens(self):
        """Test when pos == len(tokens), should use tokens[pos - 1]."""
        tokens = [
            {"type": "IDENT", "value": "x", "line": 3, "column": 10},
            {"type": "OP", "value": "=", "line": 3, "column": 12},
        ]
        pos = 2  # pos == len(tokens), should use tokens[1]
        result = make_error_node(pos, tokens)
        
        self.assertEqual(result["line"], 3)
        self.assertEqual(result["column"], 12)

    def test_priority_2_current_token_pos_zero(self):
        """Test when pos = 0, should use tokens[0] (current token)."""
        tokens = [
            {"type": "KEYWORD", "value": "if", "line": 5, "column": 1},
            {"type": "LPAREN", "value": "(", "line": 5, "column": 4},
        ]
        pos = 0
        result = make_error_node(pos, tokens)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["line"], 5)
        self.assertEqual(result["column"], 1)

    def test_priority_2_current_token_pos_within_bounds(self):
        """Test when pos < len(tokens) but pos > 0, should use tokens[pos]."""
        tokens = [
            {"type": "IDENT", "value": "a", "line": 2, "column": 3},
            {"type": "OP", "value": "*", "line": 2, "column": 5},
            {"type": "IDENT", "value": "b", "line": 2, "column": 7},
        ]
        pos = 1  # pos < len(tokens), should use tokens[1]
        result = make_error_node(pos, tokens)
        
        # Since pos > 0, priority 1 applies (tokens[pos-1])
        self.assertEqual(result["line"], 2)
        self.assertEqual(result["column"], 3)

    def test_priority_3_pos_beyond_tokens_length(self):
        """Test when pos > len(tokens), should use default line=0, column=0."""
        tokens = [
            {"type": "NUM", "value": "42", "line": 1, "column": 1},
        ]
        pos = 5  # pos > len(tokens)
        result = make_error_node(pos, tokens)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], None)
        self.assertEqual(result["children"], [])
        self.assertEqual(result["line"], 0)
        self.assertEqual(result["column"], 0)

    def test_empty_tokens_list(self):
        """Test with empty tokens list, should use default line=0, column=0."""
        tokens = []
        pos = 0
        result = make_error_node(pos, tokens)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["line"], 0)
        self.assertEqual(result["column"], 0)

    def test_token_missing_line_column_fields(self):
        """Test when token doesn't have line/column fields, should default to 0."""
        tokens = [
            {"type": "IDENT", "value": "x"},  # Missing line and column
            {"type": "OP", "value": "+"},
        ]
        pos = 1
        result = make_error_node(pos, tokens)
        
        self.assertEqual(result["line"], 0)
        self.assertEqual(result["column"], 0)

    def test_token_partial_fields_line_only(self):
        """Test when token has only line field, column should default to 0."""
        tokens = [
            {"type": "IDENT", "value": "x", "line": 10},
        ]
        pos = 1
        result = make_error_node(pos, tokens)
        
        self.assertEqual(result["line"], 10)
        self.assertEqual(result["column"], 0)

    def test_token_partial_fields_column_only(self):
        """Test when token has only column field, line should default to 0."""
        tokens = [
            {"type": "IDENT", "value": "x", "column": 25},
        ]
        pos = 1
        result = make_error_node(pos, tokens)
        
        self.assertEqual(result["line"], 0)
        self.assertEqual(result["column"], 25)

    def test_return_structure_consistency(self):
        """Test that return structure is always consistent."""
        tokens = [{"type": "TEST", "value": "val", "line": 7, "column": 14}]
        
        for pos in [0, 1, 2, 10]:
            result = make_error_node(pos, tokens)
            self.assertIn("type", result)
            self.assertIn("value", result)
            self.assertIn("children", result)
            self.assertIn("line", result)
            self.assertIn("column", result)
            self.assertEqual(result["type"], "ERROR")
            self.assertIsInstance(result["children"], list)


if __name__ == "__main__":
    unittest.main()

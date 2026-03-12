import unittest
from unittest.mock import patch

# Import the function under test using relative import
from ._parse_unary_src import _parse_unary

# Import path for mocking the dependency
_PARSE_PRIMARY_PATH = "._parse_primary_package._parse_primary_src._parse_primary"


class TestParseUnary(unittest.TestCase):
    """Test cases for _parse_unary function."""
    
    def test_single_minus_operator(self):
        """Test parsing a single minus unary operator."""
        parser_state = {
            "tokens": [
                {"type": "MINUS", "value": "-", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 2}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch(_PARSE_PRIMARY_PATH) as mock_parse_primary:
            mock_parse_primary.return_value = {
                "type": "IDENTIFIER",
                "value": "x",
                "children": [],
                "line": 1,
                "column": 2
            }
            
            result = _parse_unary(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "-")
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(result["children"][0]["type"], "IDENTIFIER")
            self.assertEqual(parser_state["pos"], 1)
    
    def test_single_plus_operator(self):
        """Test parsing a single plus unary operator."""
        parser_state = {
            "tokens": [
                {"type": "PLUS", "value": "+", "line": 1, "column": 1},
                {"type": "LITERAL", "value": "5", "line": 1, "column": 2}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch(_PARSE_PRIMARY_PATH) as mock_parse_primary:
            mock_parse_primary.return_value = {
                "type": "LITERAL",
                "value": "5",
                "children": [],
                "line": 1,
                "column": 2
            }
            
            result = _parse_unary(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "+")
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(result["children"][0]["type"], "LITERAL")
            self.assertEqual(parser_state["pos"], 1)
    
    def test_single_bang_operator(self):
        """Test parsing a single bang (logical NOT) unary operator."""
        parser_state = {
            "tokens": [
                {"type": "BANG", "value": "!", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "flag", "line": 1, "column": 2}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch(_PARSE_PRIMARY_PATH) as mock_parse_primary:
            mock_parse_primary.return_value = {
                "type": "IDENTIFIER",
                "value": "flag",
                "children": [],
                "line": 1,
                "column": 2
            }
            
            result = _parse_unary(parser_state)
            
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "!")
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(result["children"][0]["type"], "IDENTIFIER")
            self.assertEqual(parser_state["pos"], 1)
    
    def test_multiple_unary_operators_right_associative(self):
        """Test parsing multiple unary operators with right associativity."""
        parser_state = {
            "tokens": [
                {"type": "MINUS", "value": "-", "line": 1, "column": 1},
                {"type": "MINUS", "value": "-", "line": 1, "column": 2},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch(_PARSE_PRIMARY_PATH) as mock_parse_primary:
            mock_parse_primary.return_value = {
                "type": "IDENTIFIER",
                "value": "x",
                "children": [],
                "line": 1,
                "column": 3
            }
            
            result = _parse_unary(parser_state)
            
            # Should be: -(-x), outer minus at line 1, column 1
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "-")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            self.assertEqual(len(result["children"]), 1)
            
            # Inner should also be UNARY_OP
            inner = result["children"][0]
            self.assertEqual(inner["type"], "UNARY_OP")
            self.assertEqual(inner["value"], "-")
            self.assertEqual(inner["line"], 1)
            self.assertEqual(inner["column"], 2)
            
            # Innermost should be the identifier
            self.assertEqual(inner["children"][0]["type"], "IDENTIFIER")
            self.assertEqual(parser_state["pos"], 2)
    
    def test_mixed_unary_operators(self):
        """Test parsing mixed unary operators (!-+x)."""
        parser_state = {
            "tokens": [
                {"type": "BANG", "value": "!", "line": 1, "column": 1},
                {"type": "MINUS", "value": "-", "line": 1, "column": 2},
                {"type": "PLUS", "value": "+", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 4}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch(_PARSE_PRIMARY_PATH) as mock_parse_primary:
            mock_parse_primary.return_value = {
                "type": "IDENTIFIER",
                "value": "x",
                "children": [],
                "line": 1,
                "column": 4
            }
            
            result = _parse_unary(parser_state)
            
            # Should be: !(-(+x))
            # Outer: BANG at column 1
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "!")
            self.assertEqual(result["column"], 1)
            
            # Middle: MINUS at column 2
            middle = result["children"][0]
            self.assertEqual(middle["type"], "UNARY_OP")
            self.assertEqual(middle["value"], "-")
            self.assertEqual(middle["column"], 2)
            
            # Inner: PLUS at column 3
            inner = middle["children"][0]
            self.assertEqual(inner["type"], "UNARY_OP")
            self.assertEqual(inner["value"], "+")
            self.assertEqual(inner["column"], 3)
            
            # Innermost: IDENTIFIER
            self.assertEqual(inner["children"][0]["type"], "IDENTIFIER")
            self.assertEqual(parser_state["pos"], 3)
    
    def test_no_unary_operator(self):
        """Test parsing when there's no unary operator, just primary expression."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch(_PARSE_PRIMARY_PATH) as mock_parse_primary:
            mock_parse_primary.return_value = {
                "type": "IDENTIFIER",
                "value": "x",
                "children": [],
                "line": 1,
                "column": 1
            }
            
            result = _parse_unary(parser_state)
            
            # Should return the primary expression directly
            self.assertEqual(result["type"], "IDENTIFIER")
            self.assertEqual(result["value"], "x")
            self.assertEqual(parser_state["pos"], 0)
    
    def test_error_in_parser_state(self):
        """Test that function returns ERROR when parser_state already has error."""
        parser_state = {
            "tokens": [
                {"type": "MINUS", "value": "-", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.c",
            "error": "Previous error"
        }
        
        result = _parse_unary(parser_state)
        
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["value"], None)
        # Position should not be updated when there's an error
        self.assertEqual(parser_state["pos"], 0)
    
    def test_error_from_parse_primary(self):
        """Test error propagation when _parse_primary sets an error."""
        parser_state = {
            "tokens": [
                {"type": "MINUS", "value": "-", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch(_PARSE_PRIMARY_PATH) as mock_parse_primary:
            def set_error(state):
                state["error"] = "Primary parse failed"
                return {"type": "ERROR", "children": [], "value": None, "line": 0, "column": 0}
            
            mock_parse_primary.side_effect = set_error
            
            result = _parse_unary(parser_state)
            
            self.assertEqual(result["type"], "ERROR")
            self.assertEqual(parser_state.get("error"), "Primary parse failed")
    
    def test_empty_tokens(self):
        """Test parsing with empty token list."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch(_PARSE_PRIMARY_PATH) as mock_parse_primary:
            mock_parse_primary.return_value = {
                "type": "ERROR",
                "value": None,
                "children": [],
                "line": 0,
                "column": 0
            }
            
            result = _parse_unary(parser_state)
            
            # No unary ops, should return what _parse_primary returns
            self.assertEqual(result["type"], "ERROR")
            self.assertEqual(parser_state["pos"], 0)
    
    def test_position_at_end(self):
        """Test parsing when position is already at end of tokens."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 1,  # Already at end
            "filename": "test.c"
        }
        
        with patch(_PARSE_PRIMARY_PATH) as mock_parse_primary:
            mock_parse_primary.return_value = {
                "type": "ERROR",
                "value": None,
                "children": [],
                "line": 0,
                "column": 0
            }
            
            result = _parse_unary(parser_state)
            
            self.assertEqual(parser_state["pos"], 1)
    
    def test_position_updated_after_unary_ops(self):
        """Test that position is correctly updated after consuming unary operators."""
        parser_state = {
            "tokens": [
                {"type": "MINUS", "value": "-", "line": 1, "column": 1},
                {"type": "PLUS", "value": "+", "line": 1, "column": 2},
                {"type": "BANG", "value": "!", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 4}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch(_PARSE_PRIMARY_PATH) as mock_parse_primary:
            mock_parse_primary.return_value = {
                "type": "IDENTIFIER",
                "value": "x",
                "children": [],
                "line": 1,
                "column": 4
            }
            
            result = _parse_unary(parser_state)
            
            # Position should be updated to point to the identifier (after all unary ops)
            self.assertEqual(parser_state["pos"], 3)
            # _parse_primary should have been called
            mock_parse_primary.assert_called_once()
    
    def test_line_column_preserved(self):
        """Test that line and column information is preserved in AST nodes."""
        parser_state = {
            "tokens": [
                {"type": "MINUS", "value": "-", "line": 5, "column": 10},
                {"type": "IDENTIFIER", "value": "x", "line": 5, "column": 11}
            ],
            "pos": 0,
            "filename": "test.c"
        }
        
        with patch(_PARSE_PRIMARY_PATH) as mock_parse_primary:
            mock_parse_primary.return_value = {
                "type": "IDENTIFIER",
                "value": "x",
                "children": [],
                "line": 5,
                "column": 11
            }
            
            result = _parse_unary(parser_state)
            
            self.assertEqual(result["line"], 5)
            self.assertEqual(result["column"], 10)
            self.assertEqual(result["children"][0]["line"], 5)
            self.assertEqual(result["children"][0]["column"], 11)


if __name__ == "__main__":
    unittest.main()

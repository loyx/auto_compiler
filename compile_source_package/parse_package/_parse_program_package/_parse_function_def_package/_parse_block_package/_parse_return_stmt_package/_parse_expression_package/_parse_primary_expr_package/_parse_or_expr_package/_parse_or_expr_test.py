import unittest
from unittest.mock import patch

# Import the function under test using relative import
from ._parse_or_expr_src import _parse_or_expr


class TestParseOrExpr(unittest.TestCase):
    """Test cases for _parse_or_expr function."""
    
    def test_no_or_operator(self):
        """Test parsing expression without OR operator."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        with patch("_parse_or_expr_package._parse_or_expr_src._parse_and_expr") as mock_and_expr:
            mock_and_expr.return_value = {
                "type": "IDENTIFIER",
                "value": "a",
                "children": [],
                "line": 1,
                "column": 1
            }
            
            result = _parse_or_expr(parser_state)
            
            # Should return the result from _parse_and_expr without modification
            self.assertEqual(result["type"], "IDENTIFIER")
            self.assertEqual(result["value"], "a")
            mock_and_expr.assert_called_once_with(parser_state)
    
    def test_single_or_operator(self):
        """Test parsing expression with single OR operator."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "OR", "value": "||", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        with patch("_parse_or_expr_package._parse_or_expr_src._parse_and_expr") as mock_and_expr:
            # First call returns left operand
            # Second call returns right operand
            mock_and_expr.side_effect = [
                {
                    "type": "IDENTIFIER",
                    "value": "a",
                    "children": [],
                    "line": 1,
                    "column": 1
                },
                {
                    "type": "IDENTIFIER",
                    "value": "b",
                    "children": [],
                    "line": 1,
                    "column": 5
                }
            ]
            
            result = _parse_or_expr(parser_state)
            
            # Should build BINARY_OP node
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["operator"], "||")
            self.assertEqual(len(result["children"]), 2)
            self.assertEqual(result["children"][0]["value"], "a")
            self.assertEqual(result["children"][1]["value"], "b")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 3)
            
            # _parse_and_expr should be called twice
            self.assertEqual(mock_and_expr.call_count, 2)
    
    def test_multiple_or_operators(self):
        """Test parsing expression with multiple OR operators (left-associative)."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "OR", "value": "||", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5},
                {"type": "OR", "value": "||", "line": 1, "column": 7},
                {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 9}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        with patch("_parse_or_expr_package._parse_or_expr_src._parse_and_expr") as mock_and_expr:
            mock_and_expr.side_effect = [
                {"type": "IDENTIFIER", "value": "a", "children": [], "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "b", "children": [], "line": 1, "column": 5},
                {"type": "IDENTIFIER", "value": "c", "children": [], "line": 1, "column": 9}
            ]
            
            result = _parse_or_expr(parser_state)
            
            # Should be left-associative: (a || b) || c
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["operator"], "||")
            # Left child should be another BINARY_OP (a || b)
            self.assertEqual(result["children"][0]["type"], "BINARY_OP")
            self.assertEqual(result["children"][0]["operator"], "||")
            self.assertEqual(result["children"][0]["children"][0]["value"], "a")
            self.assertEqual(result["children"][0]["children"][1]["value"], "b")
            # Right child should be c
            self.assertEqual(result["children"][1]["value"], "c")
    
    def test_existing_error_in_parser_state(self):
        """Test that existing error in parser_state is handled."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.src",
            "error": "Previous error"
        }
        
        result = _parse_or_expr(parser_state)
        
        # Should return ERROR node immediately
        self.assertEqual(result["type"], "ERROR")
        self.assertEqual(result["children"], [])
        self.assertIsNone(result["value"])
    
    def test_error_from_and_expr_left(self):
        """Test error propagation when left operand parsing fails."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        def side_effect(ps):
            ps["error"] = "Left operand parse error"
            return {
                "type": "ERROR",
                "children": [],
                "value": None,
                "line": 0,
                "column": 0
            }
        
        with patch("_parse_or_expr_package._parse_or_expr_src._parse_and_expr") as mock_and_expr:
            mock_and_expr.side_effect = side_effect
            
            result = _parse_or_expr(parser_state)
            
            # Should return error result
            self.assertEqual(result["type"], "ERROR")
            self.assertIn("error", parser_state)
    
    def test_error_from_and_expr_right(self):
        """Test error propagation when right operand parsing fails."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "OR", "value": "||", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        call_count = [0]
        
        def side_effect(ps):
            call_count[0] += 1
            if call_count[0] == 1:
                # First call (left operand)
                return {
                    "type": "IDENTIFIER",
                    "value": "a",
                    "children": [],
                    "line": 1,
                    "column": 1
                }
            else:
                # Second call (right operand) - set error
                ps["error"] = "Right operand parse error"
                return {
                    "type": "ERROR",
                    "children": [],
                    "value": None,
                    "line": 0,
                    "column": 0
                }
        
        with patch("_parse_or_expr_package._parse_or_expr_src._parse_and_expr") as mock_and_expr:
            mock_and_expr.side_effect = side_effect
            
            result = _parse_or_expr(parser_state)
            
            # Should return error result from right operand
            self.assertEqual(result["type"], "ERROR")
            self.assertIn("error", parser_state)
    
    def test_empty_tokens(self):
        """Test parsing with empty token list."""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.src"
        }
        
        with patch("_parse_or_expr_package._parse_or_expr_src._parse_and_expr") as mock_and_expr:
            mock_and_expr.return_value = {
                "type": "ERROR",
                "children": [],
                "value": None,
                "line": 0,
                "column": 0
            }
            
            result = _parse_or_expr(parser_state)
            
            # Should handle empty tokens gracefully
            mock_and_expr.assert_called_once_with(parser_state)
    
    def test_or_token_by_value(self):
        """Test OR detection by value '||' when type is not OR."""
        parser_state = {
            "tokens": [
                {"type": "OPERATOR", "value": "||", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        with patch("_parse_or_expr_package._parse_or_expr_src._parse_and_expr") as mock_and_expr:
            mock_and_expr.side_effect = [
                {"type": "IDENTIFIER", "value": "a", "children": [], "line": 1, "column": 0},
                {"type": "IDENTIFIER", "value": "b", "children": [], "line": 1, "column": 3}
            ]
            
            result = _parse_or_expr(parser_state)
            
            # Should detect OR by value
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["operator"], "||")
    
    def test_non_or_token_stops_loop(self):
        """Test that non-OR token stops the OR parsing loop."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "AND", "value": "&&", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        with patch("_parse_or_expr_package._parse_or_expr_src._parse_and_expr") as mock_and_expr:
            mock_and_expr.return_value = {
                "type": "IDENTIFIER",
                "value": "a",
                "children": [],
                "line": 1,
                "column": 1
            }
            
            result = _parse_or_expr(parser_state)
            
            # Should not process AND as OR, return single identifier
            self.assertEqual(result["type"], "IDENTIFIER")
            self.assertEqual(result["value"], "a")
            # _parse_and_expr called only once since no OR found
            mock_and_expr.assert_called_once_with(parser_state)
    
    def test_pos_updated_after_or(self):
        """Test that parser_state pos is updated after consuming OR token."""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "OR", "value": "||", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.src"
        }
        
        with patch("_parse_or_expr_package._parse_or_expr_src._parse_and_expr") as mock_and_expr:
            mock_and_expr.side_effect = [
                {"type": "IDENTIFIER", "value": "a", "children": [], "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "b", "children": [], "line": 1, "column": 5}
            ]
            
            result = _parse_or_expr(parser_state)
            
            # pos should be updated to 2 (after OR token at index 1)
            self.assertEqual(parser_state["pos"], 2)


if __name__ == "__main__":
    unittest.main()

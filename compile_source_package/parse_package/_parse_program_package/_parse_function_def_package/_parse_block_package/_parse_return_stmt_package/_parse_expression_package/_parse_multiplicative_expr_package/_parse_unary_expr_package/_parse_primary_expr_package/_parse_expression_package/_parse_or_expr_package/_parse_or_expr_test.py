import unittest
from unittest.mock import patch
from typing import Any, Dict

# Import the function under test using relative import
from ._parse_or_expr_src import _parse_or_expr

# Type aliases for clarity
Token = Dict[str, Any]
AST = Dict[str, Any]
ParserState = Dict[str, Any]


class TestParseOrExpr(unittest.TestCase):
    """Test cases for _parse_or_expr function."""

    def test_single_expression_no_or(self):
        """Test parsing a single expression without OR operator."""
        mock_and_expr = {
            "type": "IDENTIFIER",
            "value": "x",
            "line": 1,
            "column": 1
        }
        
        parser_state: ParserState = {
            "tokens": [mock_and_expr],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("._parse_and_expr_package._parse_and_expr_src._parse_and_expr") as mock_parse_and:
            mock_parse_and.return_value = mock_and_expr
            
            result = _parse_or_expr(parser_state)
            
            self.assertEqual(result["type"], "IDENTIFIER")
            self.assertEqual(result["value"], "x")
            self.assertEqual(parser_state["pos"], 0)

    def test_single_or_operation(self):
        """Test parsing a single OR operation."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "KEYWORD", "value": "OR", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 6},
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        call_count = [0]
        def mock_and_impl(state):
            idx = min(call_count[0], len(state["tokens"]) - 1)
            token = state["tokens"][idx]
            call_count[0] += 1
            return token
        
        with patch("._parse_and_expr_package._parse_and_expr_src._parse_and_expr", side_effect=mock_and_impl):
            result = _parse_or_expr(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["operator"], "OR")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 3)
            self.assertEqual(len(result["children"]), 2)
            self.assertEqual(result["children"][0]["value"], "a")
            self.assertEqual(result["children"][1]["value"], "b")
            self.assertEqual(parser_state["pos"], 3)

    def test_multiple_or_operations_left_associative(self):
        """Test parsing multiple OR operations with left-associativity."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "KEYWORD", "value": "OR", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 6},
                {"type": "KEYWORD", "value": "OR", "line": 1, "column": 8},
                {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 11},
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        call_count = [0]
        def mock_and_impl(state):
            idx = min(call_count[0], len(state["tokens"]) - 1)
            token = state["tokens"][idx]
            call_count[0] += 1
            return token
        
        with patch("._parse_and_expr_package._parse_and_expr_src._parse_and_expr", side_effect=mock_and_impl):
            result = _parse_or_expr(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["operator"], "OR")
            
            inner_left = result["children"][0]
            self.assertEqual(inner_left["type"], "BINARY_OP")
            self.assertEqual(inner_left["operator"], "OR")
            self.assertEqual(inner_left["children"][0]["value"], "a")
            self.assertEqual(inner_left["children"][1]["value"], "b")
            
            self.assertEqual(result["children"][1]["value"], "c")
            self.assertEqual(parser_state["pos"], 5)

    def test_or_with_non_or_token_stops(self):
        """Test that parsing stops when encountering non-OR token."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "KEYWORD", "value": "OR", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 6},
                {"type": "KEYWORD", "value": "AND", "line": 1, "column": 8},
                {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 12},
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        call_count = [0]
        def mock_and_impl(state):
            idx = min(call_count[0], len(state["tokens"]) - 1)
            token = state["tokens"][idx]
            call_count[0] += 1
            return token
        
        with patch("._parse_and_expr_package._parse_and_expr_src._parse_and_expr", side_effect=mock_and_impl):
            result = _parse_or_expr(parser_state)
            
            self.assertEqual(result["type"], "BINARY_OP")
            self.assertEqual(result["operator"], "OR")
            self.assertEqual(result["children"][0]["value"], "a")
            self.assertEqual(result["children"][1]["value"], "b")
            self.assertEqual(parser_state["pos"], 3)

    def test_empty_tokens_raises_error(self):
        """Test that empty token list raises SyntaxError when consuming token."""
        parser_state: ParserState = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("._parse_and_expr_package._parse_and_expr_src._parse_and_expr") as mock_parse_and:
            mock_parse_and.return_value = {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            
            with self.assertRaises(SyntaxError) as context:
                _parse_or_expr(parser_state)
            
            self.assertIn("Unexpected end of input", str(context.exception))
            self.assertIn("test.py", str(context.exception))

    def test_or_at_end_raises_error(self):
        """Test that OR keyword at end of tokens raises SyntaxError."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "KEYWORD", "value": "OR", "line": 1, "column": 3},
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        call_count = [0]
        def mock_and_impl(state):
            idx = min(call_count[0], len(state["tokens"]) - 1)
            token = state["tokens"][idx]
            call_count[0] += 1
            return token
        
        with patch("._parse_and_expr_package._parse_and_expr_src._parse_and_expr", side_effect=mock_and_impl):
            with self.assertRaises(SyntaxError) as context:
                _parse_or_expr(parser_state)
            
            self.assertIn("Unexpected end of input", str(context.exception))

    def test_case_sensitive_or_keyword(self):
        """Test that 'or' (lowercase) is not treated as OR keyword."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "KEYWORD", "value": "or", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 6},
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("._parse_and_expr_package._parse_and_expr_src._parse_and_expr") as mock_parse_and:
            mock_parse_and.return_value = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
            
            result = _parse_or_expr(parser_state)
            
            self.assertEqual(result["type"], "IDENTIFIER")
            self.assertEqual(result["value"], "a")
            self.assertEqual(parser_state["pos"], 0)

    def test_or_wrong_type_not_matched(self):
        """Test that token with value 'OR' but wrong type is not matched."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "OR", "line": 1, "column": 3},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 6},
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch("._parse_and_expr_package._parse_and_expr_src._parse_and_expr") as mock_parse_and:
            mock_parse_and.return_value = {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 1}
            
            result = _parse_or_expr(parser_state)
            
            self.assertEqual(result["type"], "IDENTIFIER")
            self.assertEqual(result["value"], "a")
            self.assertEqual(parser_state["pos"], 0)

    def test_preserves_line_column_info(self):
        """Test that line and column information is preserved from OR token."""
        parser_state: ParserState = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 5, "column": 10},
                {"type": "KEYWORD", "value": "OR", "line": 5, "column": 12},
                {"type": "IDENTIFIER", "value": "b", "line": 5, "column": 15},
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        call_count = [0]
        def mock_and_impl(state):
            idx = min(call_count[0], len(state["tokens"]) - 1)
            token = state["tokens"][idx]
            call_count[0] += 1
            return token
        
        with patch("._parse_and_expr_package._parse_and_expr_src._parse_and_expr", side_effect=mock_and_impl):
            result = _parse_or_expr(parser_state)
            
            self.assertEqual(result["line"], 5)
            self.assertEqual(result["column"], 12)


if __name__ == "__main__":
    unittest.main()

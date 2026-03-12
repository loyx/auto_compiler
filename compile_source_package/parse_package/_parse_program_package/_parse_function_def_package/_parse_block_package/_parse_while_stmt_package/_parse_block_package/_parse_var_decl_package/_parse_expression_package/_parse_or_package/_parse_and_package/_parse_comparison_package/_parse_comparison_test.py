import unittest
from unittest.mock import patch

from ._parse_comparison_src import _parse_comparison


class TestParseComparison(unittest.TestCase):
    """Test cases for _parse_comparison function."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.eq_token = {
            "type": "OPERATOR",
            "value": "==",
            "line": 1,
            "column": 5
        }
        
        self.ne_token = {
            "type": "OPERATOR",
            "value": "!=",
            "line": 1,
            "column": 5
        }
        
        self.lt_token = {
            "type": "OPERATOR",
            "value": "<",
            "line": 1,
            "column": 5
        }
        
        self.gt_token = {
            "type": "OPERATOR",
            "value": ">",
            "line": 1,
            "column": 5
        }
        
        self.le_token = {
            "type": "OPERATOR",
            "value": "<=",
            "line": 1,
            "column": 5
        }
        
        self.ge_token = {
            "type": "OPERATOR",
            "value": ">=",
            "line": 1,
            "column": 5
        }
        
        self.semicolon_token = {
            "type": "PUNCTUATION",
            "value": ";",
            "line": 1,
            "column": 10
        }
    
    @patch('._consume_token_package._consume_token_src._consume_token')
    @patch('._parse_additive_package._parse_additive_src._parse_additive')
    def test_parse_comparison_equals(self, mock_parse_additive, mock_consume_token):
        """Test parsing comparison with == operator."""
        left_ast = {"type": "IDENTIFIER", "value": "x", "children": [], "line": 1, "column": 1}
        right_ast = {"type": "NUMBER", "value": "5", "children": [], "line": 1, "column": 7}
        
        mock_parse_additive.side_effect = [
            (left_ast, {"tokens": [self.eq_token], "pos": 0, "filename": "test.c"}),
            (right_ast, {"tokens": [self.eq_token], "pos": 1, "filename": "test.c"})
        ]
        
        mock_consume_token.return_value = (self.eq_token, {"tokens": [self.eq_token], "pos": 1, "filename": "test.c"})
        
        parser_state = {
            "tokens": [self.eq_token],
            "pos": 0,
            "filename": "test.c"
        }
        
        result_ast, result_state = _parse_comparison(parser_state)
        
        self.assertEqual(result_ast["type"], "BINARY_OP")
        self.assertEqual(result_ast["value"], "==")
        self.assertEqual(result_ast["children"], [left_ast, right_ast])
        self.assertEqual(result_ast["line"], 1)
        self.assertEqual(result_ast["column"], 5)
        
        mock_parse_additive.assert_called()
        self.assertEqual(mock_parse_additive.call_count, 2)
        mock_consume_token.assert_called_once()
    
    @patch('._consume_token_package._consume_token_src._consume_token')
    @patch('._parse_additive_package._parse_additive_src._parse_additive')
    def test_parse_comparison_not_equals(self, mock_parse_additive, mock_consume_token):
        """Test parsing comparison with != operator."""
        left_ast = {"type": "IDENTIFIER", "value": "a", "children": [], "line": 2, "column": 1}
        right_ast = {"type": "IDENTIFIER", "value": "b", "children": [], "line": 2, "column": 5}
        
        mock_parse_additive.side_effect = [
            (left_ast, {"tokens": [self.ne_token], "pos": 0, "filename": "test.c"}),
            (right_ast, {"tokens": [self.ne_token], "pos": 1, "filename": "test.c"})
        ]
        
        mock_consume_token.return_value = (self.ne_token, {"tokens": [self.ne_token], "pos": 1, "filename": "test.c"})
        
        parser_state = {
            "tokens": [self.ne_token],
            "pos": 0,
            "filename": "test.c"
        }
        
        result_ast, result_state = _parse_comparison(parser_state)
        
        self.assertEqual(result_ast["type"], "BINARY_OP")
        self.assertEqual(result_ast["value"], "!=")
        self.assertEqual(result_ast["children"], [left_ast, right_ast])
    
    @patch('._consume_token_package._consume_token_src._consume_token')
    @patch('._parse_additive_package._parse_additive_src._parse_additive')
    def test_parse_comparison_less_than(self, mock_parse_additive, mock_consume_token):
        """Test parsing comparison with < operator."""
        left_ast = {"type": "IDENTIFIER", "value": "i", "children": [], "line": 3, "column": 1}
        right_ast = {"type": "NUMBER", "value": "10", "children": [], "line": 3, "column": 5}
        
        mock_parse_additive.side_effect = [
            (left_ast, {"tokens": [self.lt_token], "pos": 0, "filename": "test.c"}),
            (right_ast, {"tokens": [self.lt_token], "pos": 1, "filename": "test.c"})
        ]
        
        mock_consume_token.return_value = (self.lt_token, {"tokens": [self.lt_token], "pos": 1, "filename": "test.c"})
        
        parser_state = {
            "tokens": [self.lt_token],
            "pos": 0,
            "filename": "test.c"
        }
        
        result_ast, result_state = _parse_comparison(parser_state)
        
        self.assertEqual(result_ast["type"], "BINARY_OP")
        self.assertEqual(result_ast["value"], "<")
        self.assertEqual(result_ast["children"], [left_ast, right_ast])
    
    @patch('._consume_token_package._consume_token_src._consume_token')
    @patch('._parse_additive_package._parse_additive_src._parse_additive')
    def test_parse_comparison_greater_than(self, mock_parse_additive, mock_consume_token):
        """Test parsing comparison with > operator."""
        left_ast = {"type": "IDENTIFIER", "value": "x", "children": [], "line": 4, "column": 1}
        right_ast = {"type": "NUMBER", "value": "0", "children": [], "line": 4, "column": 5}
        
        mock_parse_additive.side_effect = [
            (left_ast, {"tokens": [self.gt_token], "pos": 0, "filename": "test.c"}),
            (right_ast, {"tokens": [self.gt_token], "pos": 1, "filename": "test.c"})
        ]
        
        mock_consume_token.return_value = (self.gt_token, {"tokens": [self.gt_token], "pos": 1, "filename": "test.c"})
        
        parser_state = {
            "tokens": [self.gt_token],
            "pos": 0,
            "filename": "test.c"
        }
        
        result_ast, result_state = _parse_comparison(parser_state)
        
        self.assertEqual(result_ast["type"], "BINARY_OP")
        self.assertEqual(result_ast["value"], ">")
        self.assertEqual(result_ast["children"], [left_ast, right_ast])
    
    @patch('._consume_token_package._consume_token_src._consume_token')
    @patch('._parse_additive_package._parse_additive_src._parse_additive')
    def test_parse_comparison_less_than_or_equal(self, mock_parse_additive, mock_consume_token):
        """Test parsing comparison with <= operator."""
        left_ast = {"type": "IDENTIFIER", "value": "age", "children": [], "line": 5, "column": 1}
        right_ast = {"type": "NUMBER", "value": "100", "children": [], "line": 5, "column": 7}
        
        mock_parse_additive.side_effect = [
            (left_ast, {"tokens": [self.le_token], "pos": 0, "filename": "test.c"}),
            (right_ast, {"tokens": [self.le_token], "pos": 1, "filename": "test.c"})
        ]
        
        mock_consume_token.return_value = (self.le_token, {"tokens": [self.le_token], "pos": 1, "filename": "test.c"})
        
        parser_state = {
            "tokens": [self.le_token],
            "pos": 0,
            "filename": "test.c"
        }
        
        result_ast, result_state = _parse_comparison(parser_state)
        
        self.assertEqual(result_ast["type"], "BINARY_OP")
        self.assertEqual(result_ast["value"], "<=")
        self.assertEqual(result_ast["children"], [left_ast, right_ast])
    
    @patch('._consume_token_package._consume_token_src._consume_token')
    @patch('._parse_additive_package._parse_additive_src._parse_additive')
    def test_parse_comparison_greater_than_or_equal(self, mock_parse_additive, mock_consume_token):
        """Test parsing comparison with >= operator."""
        left_ast = {"type": "IDENTIFIER", "value": "score", "children": [], "line": 6, "column": 1}
        right_ast = {"type": "NUMBER", "value": "60", "children": [], "line": 6, "column": 8}
        
        mock_parse_additive.side_effect = [
            (left_ast, {"tokens": [self.ge_token], "pos": 0, "filename": "test.c"}),
            (right_ast, {"tokens": [self.ge_token], "pos": 1, "filename": "test.c"})
        ]
        
        mock_consume_token.return_value = (self.ge_token, {"tokens": [self.ge_token], "pos": 1, "filename": "test.c"})
        
        parser_state = {
            "tokens": [self.ge_token],
            "pos": 0,
            "filename": "test.c"
        }
        
        result_ast, result_state = _parse_comparison(parser_state)
        
        self.assertEqual(result_ast["type"], "BINARY_OP")
        self.assertEqual(result_ast["value"], ">=")
        self.assertEqual(result_ast["children"], [left_ast, right_ast])
    
    @patch('._parse_additive_package._parse_additive_src._parse_additive')
    def test_no_comparison_operator(self, mock_parse_additive):
        """Test when there's no comparison operator - should return left operand as-is."""
        left_ast = {"type": "IDENTIFIER", "value": "x", "children": [], "line": 1, "column": 1}
        
        mock_parse_additive.return_value = (left_ast, {"tokens": [self.semicolon_token], "pos": 0, "filename": "test.c"})
        
        parser_state = {
            "tokens": [self.semicolon_token],
            "pos": 0,
            "filename": "test.c"
        }
        
        result_ast, result_state = _parse_comparison(parser_state)
        
        self.assertEqual(result_ast, left_ast)
        self.assertEqual(result_state["pos"], 0)
        
        mock_parse_additive.assert_called_once()
    
    @patch('._parse_additive_package._parse_additive_src._parse_additive')
    def test_end_of_tokens(self, mock_parse_additive):
        """Test boundary case: end of tokens after parsing left operand."""
        left_ast = {"type": "IDENTIFIER", "value": "x", "children": [], "line": 1, "column": 1}
        
        mock_parse_additive.return_value = (left_ast, {"tokens": [], "pos": 0, "filename": "test.c"})
        
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.c"
        }
        
        result_ast, result_state = _parse_comparison(parser_state)
        
        self.assertEqual(result_ast, left_ast)
        
        mock_parse_additive.assert_called_once()
    
    @patch('._consume_token_package._consume_token_src._consume_token')
    @patch('._parse_additive_package._parse_additive_src._parse_additive')
    def test_chained_comparison_single_op(self, mock_parse_additive, mock_consume_token):
        """Test that only one comparison operator is consumed (chaining handled by higher level)."""
        left_ast = {"type": "IDENTIFIER", "value": "x", "children": [], "line": 1, "column": 1}
        right_ast = {"type": "NUMBER", "value": "5", "children": [], "line": 1, "column": 7}
        
        mock_parse_additive.side_effect = [
            (left_ast, {"tokens": [self.eq_token, self.lt_token], "pos": 1, "filename": "test.c"}),
            (right_ast, {"tokens": [self.eq_token, self.lt_token], "pos": 2, "filename": "test.c"})
        ]
        
        mock_consume_token.return_value = (self.eq_token, {"tokens": [self.eq_token, self.lt_token], "pos": 2, "filename": "test.c"})
        
        parser_state = {
            "tokens": [self.eq_token, self.lt_token],
            "pos": 0,
            "filename": "test.c"
        }
        
        result_ast, result_state = _parse_comparison(parser_state)
        
        self.assertEqual(result_ast["type"], "BINARY_OP")
        self.assertEqual(result_ast["value"], "==")
        self.assertEqual(len(result_ast["children"]), 2)
        self.assertEqual(result_state["pos"], 2)
        
        mock_parse_additive.assert_called()
        self.assertEqual(mock_parse_additive.call_count, 2)
        mock_consume_token.assert_called_once()
    
    @patch('._consume_token_package._consume_token_src._consume_token')
    @patch('._parse_additive_package._parse_additive_src._parse_additive')
    def test_ast_node_structure(self, mock_parse_additive, mock_consume_token):
        """Test that the BINARY_OP AST node has correct structure with line/column info."""
        left_ast = {"type": "IDENTIFIER", "value": "a", "children": [], "line": 10, "column": 5}
        right_ast = {"type": "NUMBER", "value": "42", "children": [], "line": 10, "column": 12}
        
        op_token = {
            "type": "OPERATOR",
            "value": "==",
            "line": 10,
            "column": 9
        }
        
        mock_parse_additive.side_effect = [
            (left_ast, {"tokens": [op_token], "pos": 0, "filename": "test.c"}),
            (right_ast, {"tokens": [op_token], "pos": 1, "filename": "test.c"})
        ]
        
        mock_consume_token.return_value = (op_token, {"tokens": [op_token], "pos": 1, "filename": "test.c"})
        
        parser_state = {
            "tokens": [op_token],
            "pos": 0,
            "filename": "test.c"
        }
        
        result_ast, result_state = _parse_comparison(parser_state)
        
        self.assertEqual(result_ast["type"], "BINARY_OP")
        self.assertEqual(result_ast["value"], "==")
        self.assertEqual(result_ast["line"], 10)
        self.assertEqual(result_ast["column"], 9)
        self.assertEqual(result_ast["children"], [left_ast, right_ast])


if __name__ == "__main__":
    unittest.main()

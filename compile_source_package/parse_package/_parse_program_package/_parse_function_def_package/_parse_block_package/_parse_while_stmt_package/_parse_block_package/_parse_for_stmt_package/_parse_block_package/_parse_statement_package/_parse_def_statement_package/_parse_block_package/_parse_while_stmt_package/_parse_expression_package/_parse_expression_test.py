import unittest
from unittest.mock import patch

from ._parse_expression_src import _parse_expression


class TestParseExpression(unittest.TestCase):
    """Test cases for _parse_expression function."""
    
    def test_single_term_no_operators(self):
        """Test parsing a single term without any PLUS/MINUS operators."""
        tokens = [
            {"type": "NUMBER", "value": "42", "line": 1, "column": 1}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        term_ast = {"type": "NUMBER", "value": "42", "line": 1, "column": 1}
        
        def parse_term_side_effect(state):
            state["pos"] = 1
            return term_ast
        
        with patch("._parse_term_package._parse_term_src._parse_term") as mock_parse_term:
            mock_parse_term.side_effect = parse_term_side_effect
            
            result = _parse_expression(parser_state)
            
            self.assertEqual(result, term_ast)
            self.assertEqual(parser_state["pos"], 1)
            mock_parse_term.assert_called_once()
    
    def test_expression_with_plus(self):
        """Test parsing expression with PLUS operator."""
        tokens = [
            {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
            {"type": "PLUS", "value": "+", "line": 1, "column": 2},
            {"type": "NUMBER", "value": "2", "line": 1, "column": 3}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        term1_ast = {"type": "NUMBER", "value": "1", "line": 1, "column": 1}
        term2_ast = {"type": "NUMBER", "value": "2", "line": 1, "column": 3}
        
        call_count = [0]
        def parse_term_side_effect(state):
            call_count[0] += 1
            if call_count[0] == 1:
                state["pos"] = 1
                return term1_ast
            else:
                state["pos"] = 3
                return term2_ast
        
        with patch("._parse_term_package._parse_term_src._parse_term") as mock_parse_term:
            mock_parse_term.side_effect = parse_term_side_effect
            
            result = _parse_expression(parser_state)
            
            self.assertEqual(result["type"], "BINOP")
            self.assertEqual(result["op"], "PLUS")
            self.assertEqual(result["left"], term1_ast)
            self.assertEqual(result["right"], term2_ast)
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 2)
            self.assertEqual(parser_state["pos"], 3)
            self.assertEqual(mock_parse_term.call_count, 2)
    
    def test_expression_with_minus(self):
        """Test parsing expression with MINUS operator."""
        tokens = [
            {"type": "NUMBER", "value": "10", "line": 1, "column": 1},
            {"type": "MINUS", "value": "-", "line": 1, "column": 2},
            {"type": "NUMBER", "value": "5", "line": 1, "column": 3}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        term1_ast = {"type": "NUMBER", "value": "10", "line": 1, "column": 1}
        term2_ast = {"type": "NUMBER", "value": "5", "line": 1, "column": 3}
        
        call_count = [0]
        def parse_term_side_effect(state):
            call_count[0] += 1
            if call_count[0] == 1:
                state["pos"] = 1
                return term1_ast
            else:
                state["pos"] = 3
                return term2_ast
        
        with patch("._parse_term_package._parse_term_src._parse_term") as mock_parse_term:
            mock_parse_term.side_effect = parse_term_side_effect
            
            result = _parse_expression(parser_state)
            
            self.assertEqual(result["type"], "BINOP")
            self.assertEqual(result["op"], "MINUS")
            self.assertEqual(result["left"], term1_ast)
            self.assertEqual(result["right"], term2_ast)
            self.assertEqual(parser_state["pos"], 3)
            self.assertEqual(mock_parse_term.call_count, 2)
    
    def test_multiple_operators_left_associative(self):
        """Test parsing expression with multiple operators (left-associative)."""
        tokens = [
            {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
            {"type": "PLUS", "value": "+", "line": 1, "column": 2},
            {"type": "NUMBER", "value": "2", "line": 1, "column": 3},
            {"type": "MINUS", "value": "-", "line": 1, "column": 4},
            {"type": "NUMBER", "value": "3", "line": 1, "column": 5}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        term1_ast = {"type": "NUMBER", "value": "1", "line": 1, "column": 1}
        term2_ast = {"type": "NUMBER", "value": "2", "line": 1, "column": 3}
        term3_ast = {"type": "NUMBER", "value": "3", "line": 1, "column": 5}
        
        call_count = [0]
        def parse_term_side_effect(state):
            call_count[0] += 1
            if call_count[0] == 1:
                state["pos"] = 1
                return term1_ast
            elif call_count[0] == 2:
                state["pos"] = 3
                return term2_ast
            else:
                state["pos"] = 5
                return term3_ast
        
        with patch("._parse_term_package._parse_term_src._parse_term") as mock_parse_term:
            mock_parse_term.side_effect = parse_term_side_effect
            
            result = _parse_expression(parser_state)
            
            self.assertEqual(result["type"], "BINOP")
            self.assertEqual(result["op"], "MINUS")
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 4)
            
            left = result["left"]
            self.assertEqual(left["type"], "BINOP")
            self.assertEqual(left["op"], "PLUS")
            self.assertEqual(left["left"], term1_ast)
            self.assertEqual(left["right"], term2_ast)
            
            self.assertEqual(result["right"], term3_ast)
            self.assertEqual(parser_state["pos"], 5)
            self.assertEqual(mock_parse_term.call_count, 3)
    
    def test_stops_at_non_operator_token(self):
        """Test that parsing stops when encountering non-PLUS/MINUS token."""
        tokens = [
            {"type": "NUMBER", "value": "1", "line": 1, "column": 1},
            {"type": "PLUS", "value": "+", "line": 1, "column": 2},
            {"type": "NUMBER", "value": "2", "line": 1, "column": 3},
            {"type": "MUL", "value": "*", "line": 1, "column": 4},
            {"type": "NUMBER", "value": "3", "line": 1, "column": 5}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        term1_ast = {"type": "NUMBER", "value": "1", "line": 1, "column": 1}
        term2_ast = {"type": "NUMBER", "value": "2", "line": 1, "column": 3}
        
        call_count = [0]
        def parse_term_side_effect(state):
            call_count[0] += 1
            if call_count[0] == 1:
                state["pos"] = 1
                return term1_ast
            else:
                state["pos"] = 3
                return term2_ast
        
        with patch("._parse_term_package._parse_term_src._parse_term") as mock_parse_term:
            mock_parse_term.side_effect = parse_term_side_effect
            
            result = _parse_expression(parser_state)
            
            self.assertEqual(result["type"], "BINOP")
            self.assertEqual(result["op"], "PLUS")
            self.assertEqual(parser_state["pos"], 3)
            self.assertEqual(mock_parse_term.call_count, 2)
    
    def test_end_of_tokens_after_expression(self):
        """Test parsing when tokens end right after expression."""
        tokens = [
            {"type": "NUMBER", "value": "42", "line": 1, "column": 1}
        ]
        parser_state = {
            "tokens": tokens,
            "pos": 0,
            "filename": "test.py",
            "error": ""
        }
        
        term_ast = {"type": "NUMBER", "value": "42", "line": 1, "column": 1}
        
        def parse_term_side_effect(state):
            state["pos"] = 1
            return term_ast
        
        with patch("._parse_term_package._parse_term_src._parse_term") as mock_parse_term:
            mock_parse_term.side_effect = parse_term_side_effect
            
            result = _parse_expression(parser_state)
            
            self.assertEqual(result, term_ast)
            self.assertEqual(parser_state["pos"], 1)
            mock_parse_term.assert_called_once()


if __name__ == "__main__":
    unittest.main()

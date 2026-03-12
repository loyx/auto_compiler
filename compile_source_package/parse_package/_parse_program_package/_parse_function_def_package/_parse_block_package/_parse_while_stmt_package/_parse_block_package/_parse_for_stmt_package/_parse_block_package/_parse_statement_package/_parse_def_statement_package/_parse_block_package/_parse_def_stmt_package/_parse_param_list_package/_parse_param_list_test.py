import unittest

# Relative import from the same package
from ._parse_param_list_src import _parse_param_list


class TestParseParamList(unittest.TestCase):
    """Test cases for _parse_param_list function"""
    
    def test_empty_param_list(self):
        """Test parsing empty parameter list (immediately RPAREN)"""
        parser_state = {
            "tokens": [
                {"type": "RPAREN", "value": ")", "line": 1, "column": 10}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_param_list(parser_state)
        
        self.assertEqual(result, [])
        self.assertEqual(parser_state["pos"], 0)
    
    def test_single_parameter(self):
        """Test parsing single parameter"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 5},
                {"type": "RPAREN", "value": ")", "line": 1, "column": 6}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_param_list(parser_state)
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["type"], "PARAM")
        self.assertEqual(result[0]["value"], "x")
        self.assertEqual(result[0]["line"], 1)
        self.assertEqual(result[0]["column"], 5)
        self.assertEqual(parser_state["pos"], 1)
    
    def test_multiple_parameters(self):
        """Test parsing multiple parameters with commas"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "a", "line": 1, "column": 5},
                {"type": "COMMA", "value": ",", "line": 1, "column": 6},
                {"type": "IDENTIFIER", "value": "b", "line": 1, "column": 7},
                {"type": "COMMA", "value": ",", "line": 1, "column": 8},
                {"type": "IDENTIFIER", "value": "c", "line": 1, "column": 9},
                {"type": "RPAREN", "value": ")", "line": 1, "column": 10}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_param_list(parser_state)
        
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]["value"], "a")
        self.assertEqual(result[1]["value"], "b")
        self.assertEqual(result[2]["value"], "c")
        self.assertEqual(parser_state["pos"], 5)
    
    def test_trailing_comma_raises_error(self):
        """Test that trailing comma raises SyntaxError"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 5},
                {"type": "COMMA", "value": ",", "line": 1, "column": 6},
                {"type": "RPAREN", "value": ")", "line": 1, "column": 7}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with self.assertRaises(SyntaxError) as context:
            _parse_param_list(parser_state)
        
        self.assertIn("Expected IDENTIFIER after COMMA", str(context.exception))
    
    def test_comma_without_identifier_at_end(self):
        """Test that comma at end without following identifier raises SyntaxError"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 5},
                {"type": "COMMA", "value": ",", "line": 1, "column": 6}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with self.assertRaises(SyntaxError):
            _parse_param_list(parser_state)
    
    def test_non_identifier_at_start(self):
        """Test parsing when first token is not an identifier"""
        parser_state = {
            "tokens": [
                {"type": "NUMBER", "value": "42", "line": 1, "column": 5},
                {"type": "RPAREN", "value": ")", "line": 1, "column": 7}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_param_list(parser_state)
        
        self.assertEqual(result, [])
        self.assertEqual(parser_state["pos"], 0)
    
    def test_pos_at_end_of_tokens(self):
        """Test when pos is at end of tokens list"""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_param_list(parser_state)
        
        self.assertEqual(result, [])
        self.assertEqual(parser_state["pos"], 0)
    
    def test_pos_updated_correctly(self):
        """Test that parser_state pos is updated correctly"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "param1", "line": 2, "column": 10},
                {"type": "COMMA", "value": ",", "line": 2, "column": 16},
                {"type": "IDENTIFIER", "value": "param2", "line": 2, "column": 18},
                {"type": "RPAREN", "value": ")", "line": 2, "column": 24}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_param_list(parser_state)
        
        self.assertEqual(len(result), 2)
        self.assertEqual(parser_state["pos"], 3)
    
    def test_param_nodes_have_correct_structure(self):
        """Test that parameter AST nodes have correct structure"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 3, "column": 15},
                {"type": "RPAREN", "value": ")", "line": 3, "column": 16}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_param_list(parser_state)
        
        self.assertEqual(len(result), 1)
        param_node = result[0]
        self.assertIn("type", param_node)
        self.assertIn("value", param_node)
        self.assertIn("line", param_node)
        self.assertIn("column", param_node)
        self.assertEqual(param_node["type"], "PARAM")
    
    def test_starting_from_nonzero_pos(self):
        """Test parsing when starting from non-zero position"""
        parser_state = {
            "tokens": [
                {"type": "LPAREN", "value": "(", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 2},
                {"type": "RPAREN", "value": ")", "line": 1, "column": 3}
            ],
            "pos": 1,
            "filename": "test.py"
        }
        
        result = _parse_param_list(parser_state)
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["value"], "x")
        self.assertEqual(parser_state["pos"], 2)


if __name__ == "__main__":
    unittest.main()

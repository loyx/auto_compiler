import unittest
from unittest.mock import patch

from ._parse_assignment_src import _parse_assignment


class TestParseAssignment(unittest.TestCase):
    """Test cases for _parse_assignment function."""
    
    @patch('._parse_comparison_package._parse_comparison_src._parse_comparison')
    @patch('._get_current_token_package._get_current_token_src._get_current_token')
    @patch('._advance_package._advance_src._advance')
    @patch('._syntax_error_package._syntax_error_src._syntax_error')
    def test_valid_assignment(self, mock_syntax_error, mock_advance, mock_get_token, mock_parse_comp):
        """Test valid assignment: identifier = expression"""
        mock_parse_comp.return_value = {"type": "identifier", "value": "x", "line": 1, "column": 1}
        mock_get_token.return_value = {"type": "operator", "value": "=", "line": 1, "column": 5}
        
        parser_state = {
            "tokens": [
                {"type": "identifier", "value": "x", "line": 1, "column": 1},
                {"type": "operator", "value": "=", "line": 1, "column": 5},
                {"type": "number", "value": "5", "line": 1, "column": 7}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_assignment(parser_state)
        
        self.assertEqual(result["type"], "assignment")
        self.assertEqual(result["value"], "=")
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 5)
        self.assertEqual(len(result["children"]), 2)
        self.assertEqual(result["children"][0]["type"], "identifier")
        mock_syntax_error.assert_not_called()
        mock_advance.assert_called_once()
    
    @patch('._parse_comparison_package._parse_comparison_src._parse_comparison')
    @patch('._get_current_token_package._get_current_token_src._get_current_token')
    @patch('._advance_package._advance_src._advance')
    @patch('._syntax_error_package._syntax_error_src._syntax_error')
    def test_no_assignment_operator(self, mock_syntax_error, mock_advance, mock_get_token, mock_parse_comp):
        """Test when there is no '=' operator - should return comparison result"""
        comparison_result = {"type": "number", "value": "5", "line": 1, "column": 1}
        mock_parse_comp.return_value = comparison_result
        mock_get_token.return_value = {"type": "operator", "value": "+", "line": 1, "column": 3}
        
        parser_state = {
            "tokens": [
                {"type": "number", "value": "5", "line": 1, "column": 1},
                {"type": "operator", "value": "+", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_assignment(parser_state)
        
        self.assertEqual(result, comparison_result)
        mock_syntax_error.assert_not_called()
        mock_advance.assert_not_called()
    
    @patch('._parse_comparison_package._parse_comparison_src._parse_comparison')
    @patch('._get_current_token_package._get_current_token_src._get_current_token')
    @patch('._advance_package._advance_src._advance')
    @patch('._syntax_error_package._syntax_error_src._syntax_error')
    def test_invalid_left_side(self, mock_syntax_error, mock_advance, mock_get_token, mock_parse_comp):
        """Test invalid left side: non-identifier = expression"""
        mock_parse_comp.return_value = {"type": "number", "value": "5", "line": 1, "column": 1}
        mock_get_token.return_value = {"type": "operator", "value": "=", "line": 1, "column": 3}
        
        parser_state = {
            "tokens": [
                {"type": "number", "value": "5", "line": 1, "column": 1},
                {"type": "operator", "value": "=", "line": 1, "column": 3}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_assignment(parser_state)
        
        mock_syntax_error.assert_called_once_with(
            parser_state,
            "Left side of assignment must be an identifier"
        )
        mock_advance.assert_not_called()
        self.assertEqual(result["type"], "number")
    
    @patch('._parse_comparison_package._parse_comparison_src._parse_comparison')
    @patch('._get_current_token_package._get_current_token_src._get_current_token')
    @patch('._advance_package._advance_src._advance')
    @patch('._syntax_error_package._syntax_error_src._syntax_error')
    def test_chained_assignment(self, mock_syntax_error, mock_advance, mock_get_token, mock_parse_comp):
        """Test right-associative chained assignment: a = b = 5"""
        def parse_comp_side_effect(state):
            if state.get("pos", 0) == 0:
                return {"type": "identifier", "value": "a", "line": 1, "column": 1}
            else:
                return {"type": "identifier", "value": "b", "line": 1, "column": 5}
        
        mock_parse_comp.side_effect = parse_comp_side_effect
        
        token_queue = [
            {"type": "identifier", "value": "a", "line": 1, "column": 1},
            {"type": "operator", "value": "=", "line": 1, "column": 3},
            {"type": "identifier", "value": "b", "line": 1, "column": 5},
            {"type": "operator", "value": "=", "line": 1, "column": 7},
            {"type": "number", "value": "5", "line": 1, "column": 9}
        ]
        
        def get_token_side_effect(state):
            pos = state.get("pos", 0)
            if pos < len(token_queue):
                return token_queue[pos]
            return None
        
        mock_get_token.side_effect = get_token_side_effect
        
        advance_calls = []
        def advance_side_effect(state):
            advance_calls.append(state.get("pos", 0))
            state["pos"] = state.get("pos", 0) + 1
        
        mock_advance.side_effect = advance_side_effect
        
        parser_state = {
            "tokens": token_queue,
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_assignment(parser_state)
        
        self.assertEqual(result["type"], "assignment")
        self.assertEqual(result["value"], "=")
        self.assertEqual(len(result["children"]), 2)
        
        left_child = result["children"][0]
        self.assertEqual(left_child["type"], "identifier")
        self.assertEqual(left_child["value"], "a")
        
        right_child = result["children"][1]
        self.assertEqual(right_child["type"], "assignment")
        self.assertEqual(right_child["value"], "=")
        self.assertEqual(len(right_child["children"]), 2)
        self.assertEqual(right_child["children"][0]["value"], "b")
        self.assertEqual(right_child["children"][1]["value"], "5")
        
        self.assertEqual(mock_parse_comp.call_count, 2)
        mock_syntax_error.assert_not_called()
    
    @patch('._parse_comparison_package._parse_comparison_src._parse_comparison')
    @patch('._get_current_token_package._get_current_token_src._get_current_token')
    @patch('._advance_package._advance_src._advance')
    @patch('._syntax_error_package._syntax_error_src._syntax_error')
    def test_none_token(self, mock_syntax_error, mock_advance, mock_get_token, mock_parse_comp):
        """Test when current token is None (EOF)"""
        mock_parse_comp.return_value = {"type": "number", "value": "5", "line": 1, "column": 1}
        mock_get_token.return_value = None
        
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_assignment(parser_state)
        
        self.assertEqual(result["type"], "number")
        mock_syntax_error.assert_not_called()
        mock_advance.assert_not_called()
    
    @patch('._parse_comparison_package._parse_comparison_src._parse_comparison')
    @patch('._get_current_token_package._get_current_token_src._get_current_token')
    @patch('._advance_package._advance_src._advance')
    @patch('._syntax_error_package._syntax_error_src._syntax_error')
    def test_token_missing_value_field(self, mock_syntax_error, mock_advance, mock_get_token, mock_parse_comp):
        """Test when token doesn't have 'value' field"""
        mock_parse_comp.return_value = {"type": "identifier", "value": "x", "line": 1, "column": 1}
        mock_get_token.return_value = {"type": "operator", "line": 1, "column": 5}
        
        parser_state = {
            "tokens": [{"type": "identifier", "value": "x", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_assignment(parser_state)
        
        self.assertEqual(result["type"], "identifier")
        mock_syntax_error.assert_not_called()
        mock_advance.assert_not_called()
    
    @patch('._parse_comparison_package._parse_comparison_src._parse_comparison')
    @patch('._get_current_token_package._get_current_token_src._get_current_token')
    @patch('._advance_package._advance_src._advance')
    @patch('._syntax_error_package._syntax_error_src._syntax_error')
    def test_token_empty_value(self, mock_syntax_error, mock_advance, mock_get_token, mock_parse_comp):
        """Test when token has empty 'value' field"""
        mock_parse_comp.return_value = {"type": "identifier", "value": "x", "line": 1, "column": 1}
        mock_get_token.return_value = {"type": "operator", "value": "", "line": 1, "column": 5}
        
        parser_state = {
            "tokens": [{"type": "identifier", "value": "x", "line": 1, "column": 1}],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_assignment(parser_state)
        
        self.assertEqual(result["type"], "identifier")
        mock_syntax_error.assert_not_called()
        mock_advance.assert_not_called()
    
    @patch('._parse_comparison_package._parse_comparison_src._parse_comparison')
    @patch('._get_current_token_package._get_current_token_src._get_current_token')
    @patch('._advance_package._advance_src._advance')
    @patch('._syntax_error_package._syntax_error_src._syntax_error')
    def test_assignment_with_complex_expression(self, mock_syntax_error, mock_advance, mock_get_token, mock_parse_comp):
        """Test assignment with complex right-hand side expression"""
        mock_parse_comp.return_value = {"type": "identifier", "value": "result", "line": 1, "column": 1}
        mock_get_token.return_value = {"type": "operator", "value": "=", "line": 1, "column": 8}
        
        rhs_expression = {
            "type": "addition",
            "children": [
                {"type": "number", "value": "3", "line": 1, "column": 10},
                {"type": "number", "value": "4", "line": 1, "column": 12}
            ],
            "value": "+",
            "line": 1,
            "column": 11
        }
        
        def parse_comp_side_effect(state):
            if state.get("pos", 0) == 0:
                return {"type": "identifier", "value": "result", "line": 1, "column": 1}
            return rhs_expression
        
        mock_parse_comp.side_effect = parse_comp_side_effect
        
        parser_state = {
            "tokens": [
                {"type": "identifier", "value": "result", "line": 1, "column": 1},
                {"type": "operator", "value": "=", "line": 1, "column": 8},
                {"type": "number", "value": "3", "line": 1, "column": 10},
                {"type": "operator", "value": "+", "line": 1, "column": 11},
                {"type": "number", "value": "4", "line": 1, "column": 12}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        result = _parse_assignment(parser_state)
        
        self.assertEqual(result["type"], "assignment")
        self.assertEqual(result["children"][0]["value"], "result")
        self.assertEqual(result["children"][1]["type"], "addition")
        mock_syntax_error.assert_not_called()


if __name__ == '__main__':
    unittest.main()

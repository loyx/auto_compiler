import unittest
from unittest.mock import patch
from typing import Dict, Any

from ._parse_array_literal_src import _parse_array_literal


class TestParseArrayLiteral(unittest.TestCase):
    
    def _create_parser_state(self, tokens: list, pos: int = 0, filename: str = "<test>") -> Dict[str, Any]:
        """Helper to create parser state"""
        return {
            "tokens": tokens,
            "pos": pos,
            "filename": filename
        }
    
    def _create_token(self, token_type: str, value: str = "", line: int = 1, column: int = 1) -> Dict[str, Any]:
        """Helper to create a token"""
        return {
            "type": token_type,
            "value": value,
            "line": line,
            "column": column
        }
    
    def test_empty_array(self):
        """Test parsing empty array []"""
        tokens = [
            self._create_token("LBRACKET", "[", 1, 1),
            self._create_token("RBRACKET", "]", 1, 2)
        ]
        parser_state = self._create_parser_state(tokens)
        
        result = _parse_array_literal(parser_state)
        
        self.assertEqual(result["type"], "ArrayLiteral")
        self.assertEqual(result["elements"], [])
        self.assertEqual(result["line"], 1)
        self.assertEqual(result["column"], 1)
        self.assertEqual(parser_state["pos"], 2)
    
    def test_single_element_array(self):
        """Test parsing single element array [expr]"""
        tokens = [
            self._create_token("LBRACKET", "[", 1, 1),
            self._create_token("NUMBER", "1", 1, 2),
            self._create_token("RBRACKET", "]", 1, 3)
        ]
        parser_state = self._create_parser_state(tokens)
        
        mock_element = {"type": "NumberLiteral", "value": "1", "line": 1, "column": 2}
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_def_statement_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_array_literal_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.side_effect = lambda state: (state.update({"pos": 2}), mock_element)[1]
            
            result = _parse_array_literal(parser_state)
        
        self.assertEqual(result["type"], "ArrayLiteral")
        self.assertEqual(len(result["elements"]), 1)
        self.assertEqual(result["elements"][0], mock_element)
        self.assertEqual(parser_state["pos"], 3)
    
    def test_multiple_elements_array(self):
        """Test parsing multiple elements array [expr1, expr2]"""
        tokens = [
            self._create_token("LBRACKET", "[", 1, 1),
            self._create_token("NUMBER", "1", 1, 2),
            self._create_token("COMMA", ",", 1, 3),
            self._create_token("NUMBER", "2", 1, 4),
            self._create_token("RBRACKET", "]", 1, 5)
        ]
        parser_state = self._create_parser_state(tokens)
        
        mock_element1 = {"type": "NumberLiteral", "value": "1", "line": 1, "column": 2}
        mock_element2 = {"type": "NumberLiteral", "value": "2", "line": 1, "column": 4}
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_def_statement_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_array_literal_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            call_count = [0]
            def side_effect(state):
                call_count[0] += 1
                if call_count[0] == 1:
                    state["pos"] = 2
                    return mock_element1
                else:
                    state["pos"] = 4
                    return mock_element2
            
            mock_parse_expr.side_effect = side_effect
            
            result = _parse_array_literal(parser_state)
        
        self.assertEqual(result["type"], "ArrayLiteral")
        self.assertEqual(len(result["elements"]), 2)
        self.assertEqual(result["elements"][0], mock_element1)
        self.assertEqual(result["elements"][1], mock_element2)
        self.assertEqual(parser_state["pos"], 5)
    
    def test_nested_array(self):
        """Test parsing nested array [[inner]]"""
        tokens = [
            self._create_token("LBRACKET", "[", 1, 1),
            self._create_token("LBRACKET", "[", 1, 2),
            self._create_token("NUMBER", "1", 1, 3),
            self._create_token("RBRACKET", "]", 1, 4),
            self._create_token("RBRACKET", "]", 1, 5)
        ]
        parser_state = self._create_parser_state(tokens)
        
        mock_inner_array = {"type": "ArrayLiteral", "elements": [], "line": 1, "column": 2}
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_def_statement_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_array_literal_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.side_effect = lambda state: (state.update({"pos": 4}), mock_inner_array)[1]
            
            result = _parse_array_literal(parser_state)
        
        self.assertEqual(result["type"], "ArrayLiteral")
        self.assertEqual(len(result["elements"]), 1)
        self.assertEqual(result["elements"][0], mock_inner_array)
        self.assertEqual(parser_state["pos"], 5)
    
    def test_missing_opening_bracket(self):
        """Test error when first token is not LBRACKET"""
        tokens = [
            self._create_token("NUMBER", "1", 1, 1)
        ]
        parser_state = self._create_parser_state(tokens)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_array_literal(parser_state)
        
        self.assertIn("Expected '['", str(context.exception))
    
    def test_unexpected_end_of_input_before_opening(self):
        """Test error when tokens are exhausted before LBRACKET"""
        tokens = []
        parser_state = self._create_parser_state(tokens)
        
        with self.assertRaises(SyntaxError) as context:
            _parse_array_literal(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))
    
    def test_missing_closing_bracket(self):
        """Test error when closing bracket is missing"""
        tokens = [
            self._create_token("LBRACKET", "[", 1, 1),
            self._create_token("NUMBER", "1", 1, 2)
        ]
        parser_state = self._create_parser_state(tokens)
        
        mock_element = {"type": "NumberLiteral", "value": "1", "line": 1, "column": 2}
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_def_statement_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_array_literal_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.side_effect = lambda state: (state.update({"pos": 2}), mock_element)[1]
            
            with self.assertRaises(SyntaxError) as context:
                _parse_array_literal(parser_state)
        
        self.assertIn("Expected ',' or ']'", str(context.exception))
    
    def test_unexpected_token_instead_of_comma_or_bracket(self):
        """Test error when unexpected token appears after element"""
        tokens = [
            self._create_token("LBRACKET", "[", 1, 1),
            self._create_token("NUMBER", "1", 1, 2),
            self._create_token("SEMICOLON", ";", 1, 3)
        ]
        parser_state = self._create_parser_state(tokens)
        
        mock_element = {"type": "NumberLiteral", "value": "1", "line": 1, "column": 2}
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_def_statement_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_array_literal_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.side_effect = lambda state: (state.update({"pos": 2}), mock_element)[1]
            
            with self.assertRaises(SyntaxError) as context:
                _parse_array_literal(parser_state)
        
        self.assertIn("Expected ',' or ']'", str(context.exception))
    
    def test_missing_closing_bracket_after_comma(self):
        """Test error when array ends with comma and no closing bracket"""
        tokens = [
            self._create_token("LBRACKET", "[", 1, 1),
            self._create_token("NUMBER", "1", 1, 2),
            self._create_token("COMMA", ",", 1, 3)
        ]
        parser_state = self._create_parser_state(tokens)
        
        mock_element = {"type": "NumberLiteral", "value": "1", "line": 1, "column": 2}
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_def_statement_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_array_literal_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.side_effect = lambda state: (state.update({"pos": 2}), mock_element)[1]
            
            with self.assertRaises(SyntaxError) as context:
                _parse_array_literal(parser_state)
        
        self.assertIn("Unexpected end of input", str(context.exception))
    
    def test_parse_expression_propagates_error(self):
        """Test that SyntaxError from _parse_expression is propagated"""
        tokens = [
            self._create_token("LBRACKET", "[", 1, 1),
            self._create_token("INVALID", "x", 1, 2)
        ]
        parser_state = self._create_parser_state(tokens)
        
        with patch("main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_for_stmt_package._parse_block_package._parse_statement_package._parse_def_statement_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_array_literal_package._parse_expression_package._parse_expression_src._parse_expression") as mock_parse_expr:
            mock_parse_expr.side_effect = SyntaxError("Invalid expression")
            
            with self.assertRaises(SyntaxError) as context:
                _parse_array_literal(parser_state)
        
        self.assertEqual(str(context.exception), "Invalid expression")
    
    def test_custom_filename_in_error(self):
        """Test that custom filename appears in error messages"""
        tokens = [
            self._create_token("NUMBER", "1", 1, 1)
        ]
        parser_state = self._create_parser_state(tokens, filename="test.txt")
        
        with self.assertRaises(SyntaxError) as context:
            _parse_array_literal(parser_state)
        
        self.assertIn("test.txt", str(context.exception))


if __name__ == "__main__":
    unittest.main()

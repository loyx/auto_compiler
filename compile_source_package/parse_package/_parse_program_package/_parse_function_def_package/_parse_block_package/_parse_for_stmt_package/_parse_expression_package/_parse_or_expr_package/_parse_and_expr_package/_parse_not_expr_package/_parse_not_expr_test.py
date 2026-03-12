import unittest
from unittest.mock import patch, MagicMock
import sys
from types import ModuleType

# Define the base package path
BASE_PKG = 'main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_for_stmt_package._parse_expression_package._parse_or_expr_package._parse_and_expr_package._parse_not_expr_package'

# Mock all dependencies before any imports
# This prevents the actual modules from being loaded

# Mock _build_error_node_package
mock_build_error_node_src = ModuleType(f'{BASE_PKG}._parse_primary_expr_package._build_error_node_package._build_error_node_src')
mock_build_error_node_src._build_error_node = MagicMock(return_value={"type": "ERROR", "value": "mocked", "children": [], "line": 0, "column": 0})
sys.modules[f'{BASE_PKG}._parse_primary_expr_package._build_error_node_package._build_error_node_src'] = mock_build_error_node_src

mock_build_error_node_pkg = ModuleType(f'{BASE_PKG}._parse_primary_expr_package._build_error_node_package')
sys.modules[f'{BASE_PKG}._parse_primary_expr_package._build_error_node_package'] = mock_build_error_node_pkg

# Mock _handle_identifier_package
mock_handle_identifier_src = ModuleType(f'{BASE_PKG}._parse_primary_expr_package._handle_identifier_package._handle_identifier_src')
mock_handle_identifier_src._handle_identifier = MagicMock(return_value={"type": "IDENTIFIER", "value": "mocked", "children": [], "line": 0, "column": 0})
sys.modules[f'{BASE_PKG}._parse_primary_expr_package._handle_identifier_package._handle_identifier_src'] = mock_handle_identifier_src

mock_handle_identifier_pkg = ModuleType(f'{BASE_PKG}._parse_primary_expr_package._handle_identifier_package')
sys.modules[f'{BASE_PKG}._parse_primary_expr_package._handle_identifier_package'] = mock_handle_identifier_pkg

# Mock _parse_argument_list_package (dependency of _handle_identifier)
mock_parse_argument_list_src = ModuleType(f'{BASE_PKG}._parse_primary_expr_package._handle_identifier_package._parse_argument_list_package._parse_argument_list_src')
mock_parse_argument_list_src._parse_argument_list = MagicMock(return_value=[])
sys.modules[f'{BASE_PKG}._parse_primary_expr_package._handle_identifier_package._parse_argument_list_package._parse_argument_list_src'] = mock_parse_argument_list_src

mock_parse_argument_list_pkg = ModuleType(f'{BASE_PKG}._parse_primary_expr_package._handle_identifier_package._parse_argument_list_package')
sys.modules[f'{BASE_PKG}._parse_primary_expr_package._handle_identifier_package._parse_argument_list_package'] = mock_parse_argument_list_pkg

# Mock _handle_paren_expr_package
mock_handle_paren_expr_src = ModuleType(f'{BASE_PKG}._parse_primary_expr_package._handle_paren_expr_package._handle_paren_expr_src')
mock_handle_paren_expr_src._handle_paren_expr = MagicMock(return_value={"type": "IDENTIFIER", "value": "mocked", "children": [], "line": 0, "column": 0})
sys.modules[f'{BASE_PKG}._parse_primary_expr_package._handle_paren_expr_package._handle_paren_expr_src'] = mock_handle_paren_expr_src

mock_handle_paren_expr_pkg = ModuleType(f'{BASE_PKG}._parse_primary_expr_package._handle_paren_expr_package')
sys.modules[f'{BASE_PKG}._parse_primary_expr_package._handle_paren_expr_package'] = mock_handle_paren_expr_pkg

# Mock _parse_primary_expr_package
mock_primary_expr_module = ModuleType(f'{BASE_PKG}._parse_primary_expr_package._parse_primary_expr_src')
mock_primary_expr_module._parse_primary_expr = MagicMock(return_value={"type": "IDENTIFIER", "value": "mocked", "children": [], "line": 0, "column": 0})
sys.modules[f'{BASE_PKG}._parse_primary_expr_package._parse_primary_expr_src'] = mock_primary_expr_module

mock_parent_module = ModuleType(f'{BASE_PKG}._parse_primary_expr_package')
sys.modules[f'{BASE_PKG}._parse_primary_expr_package'] = mock_parent_module

# Relative import for the function being tested
from ._parse_not_expr_src import _parse_not_expr

# Define the correct patch path for _parse_primary_expr
PARSE_PRIMARY_EXPR_PATH = f'{BASE_PKG}._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr'


class TestParseNotExpr(unittest.TestCase):
    
    def test_parse_not_expression(self):
        """Test parsing a simple 'not' expression"""
        parser_state = {
            "tokens": [
                {"type": "NOT", "value": "not", "line": 1, "column": 1},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 5}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        # Mock _parse_primary_expr to return a simple AST node
        with patch('._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr') as mock_primary:
            mock_primary.return_value = {
                "type": "IDENTIFIER",
                "value": "x",
                "children": [],
                "line": 1,
                "column": 5
            }
            
            result = _parse_not_expr(parser_state)
            
            # Verify the result structure
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "not")
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(result["line"], 1)
            self.assertEqual(result["column"], 1)
            
            # Verify pos was updated
            self.assertEqual(parser_state["pos"], 1)
            
            # Verify _parse_primary_expr was called
            mock_primary.assert_called_once()
    
    def test_parse_primary_expression(self):
        """Test parsing a primary expression (no NOT token)"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch('._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr') as mock_primary:
            mock_primary.return_value = {
                "type": "IDENTIFIER",
                "value": "x",
                "children": [],
                "line": 1,
                "column": 1
            }
            
            result = _parse_not_expr(parser_state)
            
            # Should return the primary expression directly
            self.assertEqual(result["type"], "IDENTIFIER")
            self.assertEqual(result["value"], "x")
            
            # Verify _parse_primary_expr was called
            mock_primary.assert_called_once()
    
    def test_empty_tokens(self):
        """Test parsing when tokens list is empty"""
        parser_state = {
            "tokens": [],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch('._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr') as mock_primary:
            mock_primary.return_value = {
                "type": "LITERAL",
                "value": None,
                "children": [],
                "line": 0,
                "column": 0
            }
            
            result = _parse_not_expr(parser_state)
            
            # Should call _parse_primary_expr when pos >= len(tokens)
            mock_primary.assert_called_once()
    
    def test_nested_not_expressions(self):
        """Test parsing nested 'not' expressions (not not x)"""
        parser_state = {
            "tokens": [
                {"type": "NOT", "value": "not", "line": 1, "column": 1},
                {"type": "NOT", "value": "not", "line": 1, "column": 5},
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 10}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        # First call returns another UNARY_OP (for the inner 'not')
        # Second call returns the identifier
        primary_result = {
            "type": "IDENTIFIER",
            "value": "x",
            "children": [],
            "line": 1,
            "column": 10
        }
        
        inner_not_result = {
            "type": "UNARY_OP",
            "value": "not",
            "children": [primary_result],
            "line": 1,
            "column": 5
        }
        
        with patch('._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr') as mock_primary:
            # First call (for inner not) returns inner_not_result
            # Second call (for outer not) returns primary_result
            mock_primary.side_effect = [inner_not_result, primary_result]
            
            result = _parse_not_expr(parser_state)
            
            # Verify nested structure
            self.assertEqual(result["type"], "UNARY_OP")
            self.assertEqual(result["value"], "not")
            self.assertEqual(len(result["children"]), 1)
            self.assertEqual(result["children"][0]["type"], "UNARY_OP")
    
    def test_pos_out_of_bounds(self):
        """Test when pos is beyond tokens length"""
        parser_state = {
            "tokens": [
                {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 1}
            ],
            "pos": 5,  # Beyond tokens length
            "filename": "test.py"
        }
        
        with patch('._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr') as mock_primary:
            mock_primary.return_value = {
                "type": "IDENTIFIER",
                "value": "x",
                "children": [],
                "line": 1,
                "column": 1
            }
            
            result = _parse_not_expr(parser_state)
            
            # Should call _parse_primary_expr when pos >= len(tokens)
            mock_primary.assert_called_once()
    
    def test_not_token_position_tracking(self):
        """Test that line and column are correctly tracked from NOT token"""
        parser_state = {
            "tokens": [
                {"type": "NOT", "value": "not", "line": 5, "column": 10},
                {"type": "IDENTIFIER", "value": "x", "line": 5, "column": 15}
            ],
            "pos": 0,
            "filename": "test.py"
        }
        
        with patch('._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr') as mock_primary:
            mock_primary.return_value = {
                "type": "IDENTIFIER",
                "value": "x",
                "children": [],
                "line": 5,
                "column": 15
            }
            
            result = _parse_not_expr(parser_state)
            
            # Verify line and column come from NOT token
            self.assertEqual(result["line"], 5)
            self.assertEqual(result["column"], 10)
    
    def test_not_with_different_token_types(self):
        """Test 'not' with different primary expression types"""
        test_cases = [
            ("IDENTIFIER", "x"),
            ("LITERAL", 42),
            ("LITERAL", True),
            ("LITERAL", "string"),
        ]
        
        for token_type, token_value in test_cases:
            with self.subTest(token_type=token_type, token_value=token_value):
                parser_state = {
                    "tokens": [
                        {"type": "NOT", "value": "not", "line": 1, "column": 1},
                        {"type": token_type, "value": token_value, "line": 1, "column": 5}
                    ],
                    "pos": 0,
                    "filename": "test.py"
                }
                
                with patch('._parse_primary_expr_package._parse_primary_expr_src._parse_primary_expr') as mock_primary:
                    mock_primary.return_value = {
                        "type": token_type,
                        "value": token_value,
                        "children": [],
                        "line": 1,
                        "column": 5
                    }
                    
                    result = _parse_not_expr(parser_state)
                    
                    self.assertEqual(result["type"], "UNARY_OP")
                    self.assertEqual(result["value"], "not")
                    self.assertEqual(len(result["children"]), 1)
                    self.assertEqual(result["children"][0]["type"], token_type)


if __name__ == '__main__':
    unittest.main()

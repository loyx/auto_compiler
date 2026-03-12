#!/usr/bin/env python3
"""Integration test for handle_return function."""

import sys
import os

# Add project root to path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', '..'))
sys.path.insert(0, project_root)

from unittest.mock import patch
from main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_return_package.handle_return_src import handle_return


def test_handle_return_with_value_expression():
    """Test RETURN statement with a value expression."""
    stmt = {"type": "RETURN", "value": {"op": "const", "value": 42}}
    func_name = "test_func"
    var_offsets = {"x": 0}
    
    with patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_return_package.handle_return_src.generate_expression_code') as mock_gen_expr:
        mock_gen_expr.return_value = "mov x0, #42"
        
        result = handle_return(stmt, func_name, var_offsets)
        
        mock_gen_expr.assert_called_once_with({"op": "const", "value": 42}, "test_func", {"x": 0})
        assert "mov x0, #42" in result
        assert "b test_func_exit" in result


def test_handle_return_without_value():
    """Test RETURN statement without a value (None)."""
    stmt = {"type": "RETURN", "value": None}
    func_name = "void_func"
    var_offsets = {}
    
    with patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_return_package.handle_return_src.generate_expression_code') as mock_gen_expr:
        result = handle_return(stmt, func_name, var_offsets)
        
        mock_gen_expr.assert_not_called()
        assert result == "b void_func_exit"


def test_handle_return_with_empty_dict_value():
    """Test RETURN statement with empty dict value."""
    stmt = {"type": "RETURN", "value": {}}
    func_name = "empty_func"
    var_offsets = {}
    
    with patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_return_package.handle_return_src.generate_expression_code') as mock_gen_expr:
        result = handle_return(stmt, func_name, var_offsets)
        
        mock_gen_expr.assert_not_called()
        assert result == "b empty_func_exit"


def test_handle_return_with_multiline_expression():
    """Test RETURN statement with expression that generates multi-line code."""
    stmt = {"type": "RETURN", "value": {"op": "add", "left": {"op": "const", "value": 1}, "right": {"op": "const", "value": 2}}}
    func_name = "calc_func"
    var_offsets = {}
    
    with patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_return_package.handle_return_src.generate_expression_code') as mock_gen_expr:
        mock_gen_expr.return_value = "mov x0, #1\nmov x1, #2\nadd x0, x0, x1"
        
        result = handle_return(stmt, func_name, var_offsets)
        
        expected = "mov x0, #1\nmov x1, #2\nadd x0, x0, x1\nb calc_func_exit"
        assert result == expected


def test_handle_return_when_expression_code_empty():
    """Test RETURN when expression code generation returns empty string."""
    stmt = {"type": "RETURN", "value": {"op": "const", "value": 0}}
    func_name = "zero_func"
    var_offsets = {}
    
    with patch('main_package.compile_source_package.generate_code_package.generate_function_code_package.generate_statement_code_package.handle_return_package.handle_return_src.generate_expression_code') as mock_gen_expr:
        mock_gen_expr.return_value = ""
        
        result = handle_return(stmt, func_name, var_offsets)
        
        mock_gen_expr.assert_called_once()
        assert result == "b zero_func_exit"


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])

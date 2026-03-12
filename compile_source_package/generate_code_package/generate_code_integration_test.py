#!/usr/bin/env python3
"""Integration test for generate_code function."""

import pytest
from unittest.mock import patch
import sys
import os

# Adjust path for import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from generate_code_package.generate_code_src import generate_code


class TestGenerateCodeIntegration:
    """Integration tests for generate_code function."""

    def test_generate_code_single_function(self):
        """Test code generation with a single function definition."""
        ast = {
            "type": "PROGRAM",
            "children": [
                {
                    "type": "FUNCTION_DEF",
                    "name": "main",
                    "params": [],
                    "return_type": "int",
                    "body": []
                }
            ]
        }
        
        with patch('generate_code_package.generate_code_src.generate_function_code') as mock_gen_func:
            mock_gen_func.return_value = "main:\n    ret"
            
            result = generate_code(ast)
            
            mock_gen_func.assert_called_once()
            call_args = mock_gen_func.call_args
            assert call_args[0][0]["name"] == "main"
            assert call_args[0][1] == {"if_else": 0, "if_end": 0, "while_cond": 0, 
                                        "while_end": 0, "for_cond": 0, "for_end": 0, "for_update": 0}
            assert result == "main:\n    ret"

    def test_generate_code_multiple_functions(self):
        """Test code generation with multiple function definitions."""
        ast = {
            "type": "PROGRAM",
            "children": [
                {
                    "type": "FUNCTION_DEF",
                    "name": "func1",
                    "params": [],
                    "return_type": "void",
                    "body": []
                },
                {
                    "type": "FUNCTION_DEF",
                    "name": "func2",
                    "params": [],
                    "return_type": "int",
                    "body": []
                }
            ]
        }
        
        with patch('generate_code_package.generate_code_src.generate_function_code') as mock_gen_func:
            mock_gen_func.side_effect = ["func1:\n    ret", "func2:\n    ret"]
            
            result = generate_code(ast)
            
            assert mock_gen_func.call_count == 2
            assert result == "func1:\n    ret\nfunc2:\n    ret"

    def test_generate_code_empty_children(self):
        """Test code generation with empty children list."""
        ast = {
            "type": "PROGRAM",
            "children": []
        }
        
        result = generate_code(ast)
        
        assert result == ""

    def test_generate_code_missing_children(self):
        """Test code generation when children key is missing."""
        ast = {
            "type": "PROGRAM"
        }
        
        result = generate_code(ast)
        
        assert result == ""

    def test_generate_code_non_program_root(self):
        """Test that non-PROGRAM root raises ValueError."""
        ast = {
            "type": "MODULE",
            "children": []
        }
        
        with pytest.raises(ValueError, match="Root node must be PROGRAM"):
            generate_code(ast)

    def test_generate_code_label_counter_initialization(self):
        """Test that label_counter is properly initialized for each call."""
        ast = {
            "type": "PROGRAM",
            "children": [
                {
                    "type": "FUNCTION_DEF",
                    "name": "test",
                    "params": [],
                    "return_type": "void",
                    "body": []
                }
            ]
        }
        
        with patch('generate_code_package.generate_code_src.generate_function_code') as mock_gen_func:
            mock_gen_func.return_value = "test:\n    ret"
            
            generate_code(ast)
            
            call_args = mock_gen_func.call_args
            label_counter = call_args[0][1]
            assert label_counter == {
                "if_else": 0,
                "if_end": 0,
                "while_cond": 0,
                "while_end": 0,
                "for_cond": 0,
                "for_end": 0,
                "for_update": 0
            }

    def test_generate_code_output_format(self):
        """Test that function codes are joined with newlines."""
        ast = {
            "type": "PROGRAM",
            "children": [
                {"type": "FUNCTION_DEF", "name": "f1", "params": [], "return_type": "void", "body": []},
                {"type": "FUNCTION_DEF", "name": "f2", "params": [], "return_type": "void", "body": []},
                {"type": "FUNCTION_DEF", "name": "f3", "params": [], "return_type": "void", "body": []}
            ]
        }
        
        with patch('generate_code_package.generate_code_src.generate_function_code') as mock_gen_func:
            mock_gen_func.side_effect = ["code1", "code2", "code3"]
            
            result = generate_code(ast)
            
            assert result == "code1\ncode2\ncode3"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

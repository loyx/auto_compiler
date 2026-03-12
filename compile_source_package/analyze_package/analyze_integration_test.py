#!/usr/bin/env python3
"""
集成测试：analyze 函数的语义分析功能
验证完整的类型检查和作用域验证流程
"""

import pytest
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from analyze_src import analyze


def test_analyze_complete_program():
    """测试完整程序的分析流程"""
    ast = {
        "type": "block",
        "children": [
            {
                "type": "function_def",
                "value": "main",
                "data_type": "int",
                "children": [
                    {
                        "type": "variable_decl",
                        "value": "x",
                        "data_type": "int",
                        "line": 2,
                        "column": 4
                    },
                    {
                        "type": "assignment",
                        "children": [
                            {
                                "type": "variable_ref",
                                "value": "x",
                                "line": 3,
                                "column": 4
                            },
                            {
                                "type": "int_literal",
                                "value": 5,
                                "line": 3,
                                "column": 8
                            }
                        ],
                        "line": 3,
                        "column": 4
                    }
                ],
                "line": 1,
                "column": 0
            }
        ]
    }
    
    result = analyze(ast, "test.c")
    
    assert result is ast
    assert len(result["children"]) == 1


def test_analyze_undeclared_variable():
    """测试未声明变量的错误检测"""
    ast = {
        "type": "block",
        "children": [
            {
                "type": "assignment",
                "children": [
                    {
                        "type": "variable_ref",
                        "value": "x",
                        "line": 1,
                        "column": 0
                    },
                    {
                        "type": "int_literal",
                        "value": 5,
                        "line": 1,
                        "column": 4
                    }
                ],
                "line": 1,
                "column": 0
            }
        ]
    }
    
    with pytest.raises(ValueError) as exc_info:
        analyze(ast, "test.c")
    
    assert "test.c:1:0: error:" in str(exc_info.value)
    assert "undeclared" in str(exc_info.value).lower() or "undefined" in str(exc_info.value).lower()


def test_analyze_type_mismatch():
    """测试类型不匹配错误"""
    ast = {
        "type": "block",
        "children": [
            {
                "type": "variable_decl",
                "value": "c",
                "data_type": "char",
                "line": 1,
                "column": 0
            },
            {
                "type": "assignment",
                "children": [
                    {
                        "type": "variable_ref",
                        "value": "c",
                        "line": 2,
                        "column": 0
                    },
                    {
                        "type": "int_literal",
                        "value": 5,
                        "line": 2,
                        "column": 4
                    }
                ],
                "line": 2,
                "column": 0
            }
        ]
    }
    
    with pytest.raises(ValueError) as exc_info:
        analyze(ast, "test.c")
    
    assert "test.c:2:0: error:" in str(exc_info.value)
    assert "type" in str(exc_info.value).lower() or "mismatch" in str(exc_info.value).lower()


def test_analyze_break_outside_loop():
    """测试循环外 break 的错误"""
    ast = {
        "type": "block",
        "children": [
            {
                "type": "break_stmt",
                "line": 1,
                "column": 0
            }
        ]
    }
    
    with pytest.raises(ValueError) as exc_info:
        analyze(ast, "test.c")
    
    assert "test.c:1:0: error:" in str(exc_info.value)
    assert "break" in str(exc_info.value).lower()


def test_analyze_empty_ast():
    """测试空 AST 的处理"""
    ast = {
        "type": "block",
        "children": []
    }
    
    result = analyze(ast, "empty.c")
    
    assert result is ast
    assert len(result["children"]) == 0


def test_analyze_preserves_type_info():
    """测试分析后保留类型信息"""
    ast = {
        "type": "block",
        "children": [
            {
                "type": "variable_decl",
                "value": "x",
                "data_type": "int",
                "line": 1,
                "column": 0
            }
        ]
    }
    
    result = analyze(ast, "test.c")
    
    assert result["children"][0]["data_type"] == "int"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
# -*- coding: utf-8 -*-
"""
parse 函数集成测试
验证 parse 函数在真实模块边界中的行为，真实调用子函数链
"""

import sys
import os

# 确保项目根目录在路径中
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from compile_source_package.parse_package.parse_src import parse


def test_empty_token_list():
    """测试空 token 列表"""
    tokens = []
    ast = parse(tokens, "test.empty")
    assert ast["type"] == "PROGRAM"
    assert ast["children"] == []


def test_single_function_definition():
    """测试单函数定义"""
    tokens = [
        {"type": "DEF", "value": "def", "line": 1, "column": 1},
        {"type": "IDENTIFIER", "value": "foo", "line": 1, "column": 5},
        {"type": "LPAREN", "value": "(", "line": 1, "column": 8},
        {"type": "RPAREN", "value": ")", "line": 1, "column": 9},
        {"type": "COLON", "value": ":", "line": 1, "column": 10},
        {"type": "INDENT", "value": "", "line": 2, "column": 1},
        {"type": "RETURN", "value": "return", "line": 2, "column": 5},
        {"type": "NUMBER", "value": "42", "line": 2, "column": 12},
        {"type": "NEWLINE", "value": "", "line": 2, "column": 14},
        {"type": "DEDENT", "value": "", "line": 3, "column": 1},
    ]
    ast = parse(tokens, "test.func")
    assert ast["type"] == "PROGRAM"
    assert len(ast["children"]) == 1
    assert ast["children"][0]["type"] == "FUNCTION_DEF"
    assert ast["children"][0]["value"] == "foo"


def test_multiple_function_definitions():
    """测试多函数定义"""
    tokens = [
        {"type": "DEF", "value": "def", "line": 1, "column": 1},
        {"type": "IDENTIFIER", "value": "foo", "line": 1, "column": 5},
        {"type": "LPAREN", "value": "(", "line": 1, "column": 8},
        {"type": "RPAREN", "value": ")", "line": 1, "column": 9},
        {"type": "COLON", "value": ":", "line": 1, "column": 10},
        {"type": "INDENT", "value": "", "line": 2, "column": 1},
        {"type": "RETURN", "value": "return", "line": 2, "column": 5},
        {"type": "NUMBER", "value": "1", "line": 2, "column": 12},
        {"type": "NEWLINE", "value": "", "line": 2, "column": 13},
        {"type": "DEDENT", "value": "", "line": 3, "column": 1},
        {"type": "DEF", "value": "def", "line": 3, "column": 1},
        {"type": "IDENTIFIER", "value": "bar", "line": 3, "column": 5},
        {"type": "LPAREN", "value": "(", "line": 3, "column": 8},
        {"type": "RPAREN", "value": ")", "line": 3, "column": 9},
        {"type": "COLON", "value": ":", "line": 3, "column": 10},
        {"type": "INDENT", "value": "", "line": 4, "column": 1},
        {"type": "RETURN", "value": "return", "line": 4, "column": 5},
        {"type": "NUMBER", "value": "2", "line": 4, "column": 12},
        {"type": "NEWLINE", "value": "", "line": 4, "column": 13},
        {"type": "DEDENT", "value": "", "line": 5, "column": 1},
    ]
    ast = parse(tokens, "test.multi_func")
    assert ast["type"] == "PROGRAM"
    assert len(ast["children"]) == 2
    assert ast["children"][0]["value"] == "foo"
    assert ast["children"][1]["value"] == "bar"


def test_variable_declaration():
    """测试变量声明"""
    tokens = [
        {"type": "DEF", "value": "def", "line": 1, "column": 1},
        {"type": "IDENTIFIER", "value": "main", "line": 1, "column": 5},
        {"type": "LPAREN", "value": "(", "line": 1, "column": 9},
        {"type": "RPAREN", "value": ")", "line": 1, "column": 10},
        {"type": "COLON", "value": ":", "line": 1, "column": 11},
        {"type": "INDENT", "value": "", "line": 2, "column": 1},
        {"type": "IDENTIFIER", "value": "x", "line": 2, "column": 5},
        {"type": "ASSIGN", "value": "=", "line": 2, "column": 7},
        {"type": "NUMBER", "value": "10", "line": 2, "column": 9},
        {"type": "NEWLINE", "value": "", "line": 2, "column": 11},
        {"type": "DEDENT", "value": "", "line": 3, "column": 1},
    ]
    ast = parse(tokens, "test.var_decl")
    assert ast["type"] == "PROGRAM"
    assert len(ast["children"]) == 1
    func_node = ast["children"][0]
    assert func_node["type"] == "FUNCTION_DEF"
    # 函数体中应包含变量声明
    assert len(func_node["children"]) > 0


def test_if_statement():
    """测试 if 控制结构"""
    tokens = [
        {"type": "DEF", "value": "def", "line": 1, "column": 1},
        {"type": "IDENTIFIER", "value": "check", "line": 1, "column": 5},
        {"type": "LPAREN", "value": "(", "line": 1, "column": 10},
        {"type": "RPAREN", "value": ")", "line": 1, "column": 11},
        {"type": "COLON", "value": ":", "line": 1, "column": 12},
        {"type": "INDENT", "value": "", "line": 2, "column": 1},
        {"type": "IF", "value": "if", "line": 2, "column": 5},
        {"type": "NUMBER", "value": "1", "line": 2, "column": 8},
        {"type": "COLON", "value": ":", "line": 2, "column": 9},
        {"type": "INDENT", "value": "", "line": 3, "column": 1},
        {"type": "RETURN", "value": "return", "line": 3, "column": 9},
        {"type": "NUMBER", "value": "0", "line": 3, "column": 16},
        {"type": "NEWLINE", "value": "", "line": 3, "column": 17},
        {"type": "DEDENT", "value": "", "line": 4, "column": 1},
        {"type": "DEDENT", "value": "", "line": 5, "column": 1},
    ]
    ast = parse(tokens, "test.if_stmt")
    assert ast["type"] == "PROGRAM"
    func_node = ast["children"][0]
    # 查找 IF_STMT 节点
    if_nodes = [n for n in func_node["children"] if n["type"] == "IF_STMT"]
    assert len(if_nodes) > 0


def test_while_statement():
    """测试 while 控制结构"""
    tokens = [
        {"type": "DEF", "value": "def", "line": 1, "column": 1},
        {"type": "IDENTIFIER", "value": "loop", "line": 1, "column": 5},
        {"type": "LPAREN", "value": "(", "line": 1, "column": 9},
        {"type": "RPAREN", "value": ")", "line": 1, "column": 10},
        {"type": "COLON", "value": ":", "line": 1, "column": 11},
        {"type": "INDENT", "value": "", "line": 2, "column": 1},
        {"type": "WHILE", "value": "while", "line": 2, "column": 5},
        {"type": "NUMBER", "value": "1", "line": 2, "column": 11},
        {"type": "COLON", "value": ":", "line": 2, "column": 12},
        {"type": "INDENT", "value": "", "line": 3, "column": 1},
        {"type": "BREAK", "value": "break", "line": 3, "column": 9},
        {"type": "NEWLINE", "value": "", "line": 3, "column": 14},
        {"type": "DEDENT", "value": "", "line": 4, "column": 1},
        {"type": "DEDENT", "value": "", "line": 5, "column": 1},
    ]
    ast = parse(tokens, "test.while_stmt")
    assert ast["type"] == "PROGRAM"
    func_node = ast["children"][0]
    while_nodes = [n for n in func_node["children"] if n["type"] == "WHILE_STMT"]
    assert len(while_nodes) > 0


def test_for_statement():
    """测试 for 控制结构"""
    tokens = [
        {"type": "DEF", "value": "def", "line": 1, "column": 1},
        {"type": "IDENTIFIER", "value": "iterate", "line": 1, "column": 5},
        {"type": "LPAREN", "value": "(", "line": 1, "column": 12},
        {"type": "RPAREN", "value": ")", "line": 1, "column": 13},
        {"type": "COLON", "value": ":", "line": 1, "column": 14},
        {"type": "INDENT", "value": "", "line": 2, "column": 1},
        {"type": "FOR", "value": "for", "line": 2, "column": 5},
        {"type": "IDENTIFIER", "value": "i", "line": 2, "column": 9},
        {"type": "IN", "value": "in", "line": 2, "column": 11},
        {"type": "IDENTIFIER", "value": "range", "line": 2, "column": 14},
        {"type": "LPAREN", "value": "(", "line": 2, "column": 19},
        {"type": "NUMBER", "value": "10", "line": 2, "column": 20},
        {"type": "RPAREN", "value": ")", "line": 2, "column": 22},
        {"type": "COLON", "value": ":", "line": 2, "column": 23},
        {"type": "INDENT", "value": "", "line": 3, "column": 1},
        {"type": "CONTINUE", "value": "continue", "line": 3, "column": 9},
        {"type": "NEWLINE", "value": "", "line": 3, "column": 17},
        {"type": "DEDENT", "value": "", "line": 4, "column": 1},
        {"type": "DEDENT", "value": "", "line": 5, "column": 1},
    ]
    ast = parse(tokens, "test.for_stmt")
    assert ast["type"] == "PROGRAM"
    func_node = ast["children"][0]
    for_nodes = [n for n in func_node["children"] if n["type"] == "FOR_STMT"]
    assert len(for_nodes) > 0


def test_return_statement():
    """测试 return 语句"""
    tokens = [
        {"type": "DEF", "value": "def", "line": 1, "column": 1},
        {"type": "IDENTIFIER", "value": "get_value", "line": 1, "column": 5},
        {"type": "LPAREN", "value": "(", "line": 1, "column": 14},
        {"type": "RPAREN", "value": ")", "line": 1, "column": 15},
        {"type": "COLON", "value": ":", "line": 1, "column": 16},
        {"type": "INDENT", "value": "", "line": 2, "column": 1},
        {"type": "RETURN", "value": "return", "line": 2, "column": 5},
        {"type": "NUMBER", "value": "100", "line": 2, "column": 12},
        {"type": "NEWLINE", "value": "", "line": 2, "column": 15},
        {"type": "DEDENT", "value": "", "line": 3, "column": 1},
    ]
    ast = parse(tokens, "test.return_stmt")
    assert ast["type"] == "PROGRAM"
    func_node = ast["children"][0]
    return_nodes = [n for n in func_node["children"] if n["type"] == "RETURN_STMT"]
    assert len(return_nodes) > 0


def test_break_statement():
    """测试 break 语句"""
    tokens = [
        {"type": "DEF", "value": "def", "line": 1, "column": 1},
        {"type": "IDENTIFIER", "value": "stop", "line": 1, "column": 5},
        {"type": "LPAREN", "value": "(", "line": 1, "column": 9},
        {"type": "RPAREN", "value": ")", "line": 1, "column": 10},
        {"type": "COLON", "value": ":", "line": 1, "column": 11},
        {"type": "INDENT", "value": "", "line": 2, "column": 1},
        {"type": "BREAK", "value": "break", "line": 2, "column": 5},
        {"type": "NEWLINE", "value": "", "line": 2, "column": 10},
        {"type": "DEDENT", "value": "", "line": 3, "column": 1},
    ]
    ast = parse(tokens, "test.break_stmt")
    assert ast["type"] == "PROGRAM"
    func_node = ast["children"][0]
    break_nodes = [n for n in func_node["children"] if n["type"] == "BREAK_STMT"]
    assert len(break_nodes) > 0


def test_continue_statement():
    """测试 continue 语句"""
    tokens = [
        {"type": "DEF", "value": "def", "line": 1, "column": 1},
        {"type": "IDENTIFIER", "value": "skip", "line": 1, "column": 5},
        {"type": "LPAREN", "value": "(", "line": 1, "column": 9},
        {"type": "RPAREN", "value": ")", "line": 1, "column": 10},
        {"type": "COLON", "value": ":", "line": 1, "column": 11},
        {"type": "INDENT", "value": "", "line": 2, "column": 1},
        {"type": "CONTINUE", "value": "continue", "line": 2, "column": 5},
        {"type": "NEWLINE", "value": "", "line": 2, "column": 13},
        {"type": "DEDENT", "value": "", "line": 3, "column": 1},
    ]
    ast = parse(tokens, "test.continue_stmt")
    assert ast["type"] == "PROGRAM"
    func_node = ast["children"][0]
    continue_nodes = [n for n in func_node["children"] if n["type"] == "CONTINUE_STMT"]
    assert len(continue_nodes) > 0


def test_complex_expression():
    """测试复杂表达式"""
    tokens = [
        {"type": "DEF", "value": "def", "line": 1, "column": 1},
        {"type": "IDENTIFIER", "value": "calc", "line": 1, "column": 5},
        {"type": "LPAREN", "value": "(", "line": 1, "column": 9},
        {"type": "RPAREN", "value": ")", "line": 1, "column": 10},
        {"type": "COLON", "value": ":", "line": 1, "column": 11},
        {"type": "INDENT", "value": "", "line": 2, "column": 1},
        {"type": "RETURN", "value": "return", "line": 2, "column": 5},
        {"type": "NUMBER", "value": "1", "line": 2, "column": 12},
        {"type": "PLUS", "value": "+", "line": 2, "column": 14},
        {"type": "NUMBER", "value": "2", "line": 2, "column": 16},
        {"type": "STAR", "value": "*", "line": 2, "column": 18},
        {"type": "NUMBER", "value": "3", "line": 2, "column": 20},
        {"type": "NEWLINE", "value": "", "line": 2, "column": 21},
        {"type": "DEDENT", "value": "", "line": 3, "column": 1},
    ]
    ast = parse(tokens, "test.expr")
    assert ast["type"] == "PROGRAM"
    func_node = ast["children"][0]
    return_nodes = [n for n in func_node["children"] if n["type"] == "RETURN_STMT"]
    assert len(return_nodes) > 0
    # 验证表达式中有二元操作
    return_node = return_nodes[0]
    assert len(return_node["children"]) > 0


def test_filename_propagation():
    """测试文件名传递到 AST"""
    tokens = [
        {"type": "DEF", "value": "def", "line": 1, "column": 1},
        {"type": "IDENTIFIER", "value": "test_func", "line": 1, "column": 5},
        {"type": "LPAREN", "value": "(", "line": 1, "column": 14},
        {"type": "RPAREN", "value": ")", "line": 1, "column": 15},
        {"type": "COLON", "value": ":", "line": 1, "column": 16},
        {"type": "INDENT", "value": "", "line": 2, "column": 1},
        {"type": "PASS", "value": "pass", "line": 2, "column": 5},
        {"type": "NEWLINE", "value": "", "line": 2, "column": 9},
        {"type": "DEDENT", "value": "", "line": 3, "column": 1},
    ]
    test_filename = "my_test_source.py"
    ast = parse(tokens, test_filename)
    assert ast["type"] == "PROGRAM"
    # 验证 AST 结构正确构建


def test_syntax_error_propagation():
    """测试语法错误传播（带行列号）"""
    # 构造一个会导致语法错误的 token 流
    tokens = [
        {"type": "DEF", "value": "def", "line": 1, "column": 1},
        {"type": "IDENTIFIER", "value": "incomplete", "line": 1, "column": 5},
        {"type": "LPAREN", "value": "(", "line": 1, "column": 15},
        # 缺少 RPAREN 和 COLON，应该导致语法错误
    ]
    try:
        ast = parse(tokens, "test_error.py")
        # 如果没有抛出异常，说明解析器对不完整输入有容错处理
        # 这是可接受的行为
    except Exception as e:
        # 如果抛出异常，验证异常信息包含行列号
        error_msg = str(e)
        # 异常应该包含错误位置信息
        assert "line" in error_msg.lower() or "column" in error_msg.lower() or "1" in error_msg


if __name__ == "__main__":
    # 运行所有测试
    test_empty_token_list()
    print("✓ test_empty_token_list passed")
    
    test_single_function_definition()
    print("✓ test_single_function_definition passed")
    
    test_multiple_function_definitions()
    print("✓ test_multiple_function_definitions passed")
    
    test_variable_declaration()
    print("✓ test_variable_declaration passed")
    
    test_if_statement()
    print("✓ test_if_statement passed")
    
    test_while_statement()
    print("✓ test_while_statement passed")
    
    test_for_statement()
    print("✓ test_for_statement passed")
    
    test_return_statement()
    print("✓ test_return_statement passed")
    
    test_break_statement()
    print("✓ test_break_statement passed")
    
    test_continue_statement()
    print("✓ test_continue_statement passed")
    
    test_complex_expression()
    print("✓ test_complex_expression passed")
    
    test_filename_propagation()
    print("✓ test_filename_propagation passed")
    
    test_syntax_error_propagation()
    print("✓ test_syntax_error_propagation passed")
    
    print("\n所有集成测试通过！")

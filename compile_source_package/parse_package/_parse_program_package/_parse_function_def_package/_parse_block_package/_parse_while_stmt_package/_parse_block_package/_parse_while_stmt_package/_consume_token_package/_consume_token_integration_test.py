#!/usr/bin/env python3
"""
集成测试：_consume_token 函数

验证 _consume_token 在真实模块边界中的行为，使用真实的 _peek_token 子函数。
"""

import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from main_package.compile_source_package.parse_package._parse_program_package._parse_function_def_package._parse_block_package._parse_while_stmt_package._parse_block_package._parse_while_stmt_package._consume_token_package._consume_token_src import _consume_token


def test_consume_matching_token():
    """测试成功消费匹配的 token"""
    parser_state = {
        "tokens": [
            {"type": "WHILE", "value": "while", "line": 1, "column": 1},
            {"type": "LPAREN", "value": "(", "line": 1, "column": 7},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 8},
        ],
        "pos": 0,
        "filename": "test.py",
        "error": None
    }
    
    new_state = _consume_token(parser_state, "WHILE")
    
    assert new_state["pos"] == 1, f"Expected pos=1, got {new_state['pos']}"
    assert new_state["filename"] == "test.py", "filename should be preserved"
    assert new_state["error"] is None, "error should be preserved"
    assert parser_state["pos"] == 0, "Original state should not be modified"
    print("✓ test_consume_matching_token passed")


def test_consume_token_at_middle_position():
    """测试在中间位置消费 token"""
    parser_state = {
        "tokens": [
            {"type": "WHILE", "value": "while", "line": 1, "column": 1},
            {"type": "LPAREN", "value": "(", "line": 1, "column": 7},
            {"type": "IDENTIFIER", "value": "x", "line": 1, "column": 8},
        ],
        "pos": 1,
        "filename": "test.py",
        "error": None
    }
    
    new_state = _consume_token(parser_state, "LPAREN")
    
    assert new_state["pos"] == 2, f"Expected pos=2, got {new_state['pos']}"
    assert parser_state["pos"] == 1, "Original state should not be modified"
    print("✓ test_consume_token_at_middle_position passed")


def test_consume_last_token():
    """测试消费最后一个 token"""
    parser_state = {
        "tokens": [
            {"type": "RPAREN", "value": ")", "line": 1, "column": 10},
        ],
        "pos": 0,
        "filename": "test.py",
        "error": None
    }
    
    new_state = _consume_token(parser_state, "RPAREN")
    
    assert new_state["pos"] == 1, f"Expected pos=1, got {new_state['pos']}"
    print("✓ test_consume_last_token passed")


def test_consume_token_end_of_input():
    """测试在输入结束时消费 token 应抛出异常"""
    parser_state = {
        "tokens": [
            {"type": "WHILE", "value": "while", "line": 1, "column": 1},
        ],
        "pos": 1,
        "filename": "test.py",
        "error": None
    }
    
    try:
        _consume_token(parser_state, "RPAREN")
        assert False, "Should have raised SyntaxError"
    except SyntaxError as e:
        assert "Unexpected end of input" in str(e), f"Wrong error message: {e}"
    print("✓ test_consume_token_end_of_input passed")


def test_consume_token_type_mismatch():
    """测试 token 类型不匹配时应抛出异常"""
    parser_state = {
        "tokens": [
            {"type": "WHILE", "value": "while", "line": 1, "column": 1},
            {"type": "LPAREN", "value": "(", "line": 1, "column": 7},
        ],
        "pos": 0,
        "filename": "test.py",
        "error": None
    }
    
    try:
        _consume_token(parser_state, "RPAREN")
        assert False, "Should have raised SyntaxError"
    except SyntaxError as e:
        assert "Expected RPAREN but got WHILE" in str(e), f"Wrong error message: {e}"
    print("✓ test_consume_token_type_mismatch passed")


def test_consume_multiple_tokens_sequentially():
    """测试连续消费多个 token"""
    parser_state = {
        "tokens": [
            {"type": "WHILE", "value": "while", "line": 1, "column": 1},
            {"type": "LPAREN", "value": "(", "line": 1, "column": 7},
            {"type": "RPAREN", "value": ")", "line": 1, "column": 10},
        ],
        "pos": 0,
        "filename": "test.py",
        "error": None
    }
    
    state1 = _consume_token(parser_state, "WHILE")
    assert state1["pos"] == 1
    
    state2 = _consume_token(state1, "LPAREN")
    assert state2["pos"] == 2
    
    state3 = _consume_token(state2, "RPAREN")
    assert state3["pos"] == 3
    
    print("✓ test_consume_multiple_tokens_sequentially passed")


def test_empty_token_list():
    """测试空 token 列表"""
    parser_state = {
        "tokens": [],
        "pos": 0,
        "filename": "test.py",
        "error": None
    }
    
    try:
        _consume_token(parser_state, "WHILE")
        assert False, "Should have raised SyntaxError"
    except SyntaxError as e:
        assert "Unexpected end of input" in str(e), f"Wrong error message: {e}"
    print("✓ test_empty_token_list passed")


def test_state_fields_preserved():
    """测试所有状态字段在消费后保持不变（除了 pos）"""
    parser_state = {
        "tokens": [
            {"type": "WHILE", "value": "while", "line": 1, "column": 1},
        ],
        "pos": 0,
        "filename": "complex/path/to/file.py",
        "error": "some previous error"
    }
    
    new_state = _consume_token(parser_state, "WHILE")
    
    assert new_state["filename"] == "complex/path/to/file.py", "filename should be preserved"
    assert new_state["error"] == "some previous error", "error should be preserved"
    assert new_state["tokens"] is parser_state["tokens"], "tokens list should be the same reference"
    print("✓ test_state_fields_preserved passed")


if __name__ == "__main__":
    test_consume_matching_token()
    test_consume_token_at_middle_position()
    test_consume_last_token()
    test_consume_token_end_of_input()
    test_consume_token_type_mismatch()
    test_consume_multiple_tokens_sequentially()
    test_empty_token_list()
    test_state_fields_preserved()
    print("\n✅ All integration tests passed!")

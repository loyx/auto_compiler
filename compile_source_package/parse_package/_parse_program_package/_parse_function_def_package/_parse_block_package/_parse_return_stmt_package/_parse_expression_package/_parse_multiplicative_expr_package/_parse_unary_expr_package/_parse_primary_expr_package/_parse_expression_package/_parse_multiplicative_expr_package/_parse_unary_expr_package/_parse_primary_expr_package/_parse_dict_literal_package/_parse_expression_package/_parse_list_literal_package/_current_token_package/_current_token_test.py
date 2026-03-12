# === imports ===
from typing import Any, Dict
from ._current_token_src import _current_token

# === type aliases (matching source) ===
Token = Dict[str, Any]
ParserState = Dict[str, Any]

# === test cases ===

def test_current_token_valid_position():
    """测试 pos 在有效范围内时返回对应 token"""
    tokens = [
        {"type": "IDENT", "value": "x", "line": 1, "column": 1},
        {"type": "OP", "value": "+", "line": 1, "column": 2},
        {"type": "NUMBER", "value": "5", "line": 1, "column": 3},
    ]
    parser_state: ParserState = {
        "tokens": tokens,
        "filename": "test.py",
        "pos": 1,
    }
    
    result = _current_token(parser_state)
    
    assert result is not None
    assert result == tokens[1]
    assert result["type"] == "OP"
    assert result["value"] == "+"


def test_current_token_position_zero():
    """测试 pos 为 0 时返回第一个 token"""
    tokens = [
        {"type": "IDENT", "value": "x", "line": 1, "column": 1},
    ]
    parser_state: ParserState = {
        "tokens": tokens,
        "filename": "test.py",
        "pos": 0,
    }
    
    result = _current_token(parser_state)
    
    assert result is not None
    assert result == tokens[0]
    assert result["type"] == "IDENT"


def test_current_token_position_last():
    """测试 pos 在最后一个位置时返回最后一个 token"""
    tokens = [
        {"type": "IDENT", "value": "x", "line": 1, "column": 1},
        {"type": "OP", "value": "+", "line": 1, "column": 2},
        {"type": "NUMBER", "value": "5", "line": 1, "column": 3},
    ]
    parser_state: ParserState = {
        "tokens": tokens,
        "filename": "test.py",
        "pos": 2,
    }
    
    result = _current_token(parser_state)
    
    assert result is not None
    assert result == tokens[2]
    assert result["value"] == "5"


def test_current_token_position_out_of_bounds_high():
    """测试 pos 大于等于 tokens 长度时返回 None"""
    tokens = [
        {"type": "IDENT", "value": "x", "line": 1, "column": 1},
    ]
    parser_state: ParserState = {
        "tokens": tokens,
        "filename": "test.py",
        "pos": 1,
    }
    
    result = _current_token(parser_state)
    
    assert result is None


def test_current_token_position_out_of_bounds_far():
    """测试 pos 远大于 tokens 长度时返回 None"""
    tokens = [
        {"type": "IDENT", "value": "x", "line": 1, "column": 1},
    ]
    parser_state: ParserState = {
        "tokens": tokens,
        "filename": "test.py",
        "pos": 100,
    }
    
    result = _current_token(parser_state)
    
    assert result is None


def test_current_token_negative_position():
    """测试 pos 为负数时返回 None"""
    tokens = [
        {"type": "IDENT", "value": "x", "line": 1, "column": 1},
        {"type": "OP", "value": "+", "line": 1, "column": 2},
    ]
    parser_state: ParserState = {
        "tokens": tokens,
        "filename": "test.py",
        "pos": -1,
    }
    
    result = _current_token(parser_state)
    
    assert result is None


def test_current_token_empty_tokens():
    """测试 tokens 为空列表时返回 None"""
    parser_state: ParserState = {
        "tokens": [],
        "filename": "test.py",
        "pos": 0,
    }
    
    result = _current_token(parser_state)
    
    assert result is None


def test_current_token_missing_tokens_key():
    """测试 parser_state 缺少 tokens 键时返回 None"""
    parser_state: ParserState = {
        "filename": "test.py",
        "pos": 0,
    }
    
    result = _current_token(parser_state)
    
    assert result is None


def test_current_token_missing_pos_key():
    """测试 parser_state 缺少 pos 键时使用默认值 0"""
    tokens = [
        {"type": "IDENT", "value": "x", "line": 1, "column": 1},
    ]
    parser_state: ParserState = {
        "tokens": tokens,
        "filename": "test.py",
    }
    
    result = _current_token(parser_state)
    
    assert result is not None
    assert result == tokens[0]


def test_current_token_empty_parser_state():
    """测试 parser_state 为空字典时返回 None"""
    parser_state: ParserState = {}
    
    result = _current_token(parser_state)
    
    assert result is None


def test_current_token_token_with_all_fields():
    """测试返回的 token 包含所有字段"""
    tokens = [
        {
            "type": "STRING",
            "value": "hello",
            "line": 5,
            "column": 10,
        },
    ]
    parser_state: ParserState = {
        "tokens": tokens,
        "filename": "test.py",
        "pos": 0,
    }
    
    result = _current_token(parser_state)
    
    assert result is not None
    assert result["type"] == "STRING"
    assert result["value"] == "hello"
    assert result["line"] == 5
    assert result["column"] == 10


# === test runner ===
if __name__ == "__main__":
    test_current_token_valid_position()
    test_current_token_position_zero()
    test_current_token_position_last()
    test_current_token_position_out_of_bounds_high()
    test_current_token_position_out_of_bounds_far()
    test_current_token_negative_position()
    test_current_token_empty_tokens()
    test_current_token_missing_tokens_key()
    test_current_token_missing_pos_key()
    test_current_token_empty_parser_state()
    test_current_token_token_with_all_fields()
    print("All tests passed!")

#!/usr/bin/env python3
"""Integration test for _parse_program function.

Tests the _parse_program function through real module boundaries,
minimizing mocks and validating behavior through actual call chains.
"""

import sys

# Add project root to path
project_root = "/Users/loyx/projects/autoapp_workspace/workspace/projects/cc/files"
sys.path.insert(0, project_root)

from main_package.compile_source_package.parse_package._parse_program_package._parse_program_src import (
    _parse_program,
    _parse_block,
)
from main_package.compile_source_package.parse_package._parse_program_package._is_at_end_package._is_at_end_src import (
    _is_at_end,
)


def create_token(type_name: str, value: str = None, line: int = 1, column: int = 1) -> dict:
    """Helper to create a token dict."""
    return {
        "type": type_name,
        "value": value,
        "line": line,
        "column": column
    }


def test_empty_program():
    """Test parsing an empty program (no functions)."""
    tokens = []
    parser_state = {
        "tokens": tokens,
        "pos": 0,
        "filename": "test.c"
    }
    
    result = _parse_program(parser_state)
    
    assert result["type"] == "PROGRAM", f"Expected PROGRAM type, got {result['type']}"
    assert result["children"] == [], f"Expected empty children, got {result['children']}"
    assert result["value"] is None
    assert parser_state["pos"] == 0, "Position should not advance for empty program"
    print("✓ test_empty_program passed")


def test_single_function():
    """Test parsing a program with a single function."""
    # Tokens for: int foo() { }
    tokens = [
        create_token("INT", "int", 1, 1),
        create_token("IDENTIFIER", "foo", 1, 5),
        create_token("LPAREN", "(", 1, 8),
        create_token("RPAREN", ")", 1, 9),
        create_token("LBRACE", "{", 1, 11),
        create_token("RBRACE", "}", 1, 13),
    ]
    
    parser_state = {
        "tokens": tokens,
        "pos": 0,
        "filename": "test.c"
    }
    
    result = _parse_program(parser_state)
    
    assert result["type"] == "PROGRAM", f"Expected PROGRAM type, got {result['type']}"
    assert len(result["children"]) == 1, f"Expected 1 child, got {len(result['children'])}"
    
    func_def = result["children"][0]
    assert func_def["type"] == "FUNCTION_DEF", f"Expected FUNCTION_DEF, got {func_def['type']}"
    assert func_def["value"] == "foo", f"Expected function name 'foo', got {func_def['value']}"
    assert func_def["return_type"] == "int", f"Expected return_type 'int', got {func_def.get('return_type')}"
    
    print("✓ test_single_function passed")


def test_multiple_functions():
    """Test parsing a program with multiple functions."""
    # Tokens for: int foo() { } void bar() { }
    tokens = [
        create_token("INT", "int", 1, 1),
        create_token("IDENTIFIER", "foo", 1, 5),
        create_token("LPAREN", "(", 1, 8),
        create_token("RPAREN", ")", 1, 9),
        create_token("LBRACE", "{", 1, 11),
        create_token("RBRACE", "}", 1, 13),
        create_token("VOID", "void", 2, 1),
        create_token("IDENTIFIER", "bar", 2, 6),
        create_token("LPAREN", "(", 2, 9),
        create_token("RPAREN", ")", 2, 10),
        create_token("LBRACE", "{", 2, 12),
        create_token("RBRACE", "}", 2, 14),
    ]
    
    parser_state = {
        "tokens": tokens,
        "pos": 0,
        "filename": "test.c"
    }
    
    result = _parse_program(parser_state)
    
    assert result["type"] == "PROGRAM", f"Expected PROGRAM type, got {result['type']}"
    assert len(result["children"]) == 2, f"Expected 2 children, got {len(result['children'])}"
    
    func1 = result["children"][0]
    assert func1["type"] == "FUNCTION_DEF"
    assert func1["value"] == "foo"
    assert func1["return_type"] == "int"
    
    func2 = result["children"][1]
    assert func2["type"] == "FUNCTION_DEF"
    assert func2["value"] == "bar"
    assert func2["return_type"] == "void"
    
    print("✓ test_multiple_functions passed")


def test_function_with_parameters():
    """Test parsing a function with parameters."""
    # Tokens for: int add(int a, int b) { }
    tokens = [
        create_token("INT", "int", 1, 1),
        create_token("IDENTIFIER", "add", 1, 5),
        create_token("LPAREN", "(", 1, 8),
        create_token("INT", "int", 1, 9),
        create_token("IDENTIFIER", "a", 1, 13),
        create_token("COMMA", ",", 1, 14),
        create_token("INT", "int", 1, 16),
        create_token("IDENTIFIER", "b", 1, 20),
        create_token("RPAREN", ")", 1, 21),
        create_token("LBRACE", "{", 1, 23),
        create_token("RBRACE", "}", 1, 25),
    ]
    
    parser_state = {
        "tokens": tokens,
        "pos": 0,
        "filename": "test.c"
    }
    
    result = _parse_program(parser_state)
    
    assert result["type"] == "PROGRAM"
    assert len(result["children"]) == 1
    
    func_def = result["children"][0]
    assert func_def["type"] == "FUNCTION_DEF"
    assert func_def["value"] == "add"
    assert func_def["return_type"] == "int"
    assert "params" in func_def
    assert len(func_def["params"]) == 2
    
    param1 = func_def["params"][0]
    assert param1["type"] == "PARAM"
    assert param1["value"] == "a"
    assert param1["param_type"] == "int"
    
    param2 = func_def["params"][1]
    assert param2["type"] == "PARAM"
    assert param2["value"] == "b"
    assert param2["param_type"] == "int"
    
    print("✓ test_function_with_parameters passed")


def test_function_with_body_statements():
    """Test parsing a function with statements in the body."""
    # Tokens for: int foo() { x = 1; }
    tokens = [
        create_token("INT", "int", 1, 1),
        create_token("IDENTIFIER", "foo", 1, 5),
        create_token("LPAREN", "(", 1, 8),
        create_token("RPAREN", ")", 1, 9),
        create_token("LBRACE", "{", 1, 11),
        create_token("IDENTIFIER", "x", 1, 13),
        create_token("ASSIGN", "=", 1, 15),
        create_token("NUMBER", "1", 1, 17),
        create_token("SEMICOLON", ";", 1, 18),
        create_token("RBRACE", "}", 1, 20),
    ]
    
    parser_state = {
        "tokens": tokens,
        "pos": 0,
        "filename": "test.c"
    }
    
    result = _parse_program(parser_state)
    
    assert result["type"] == "PROGRAM"
    assert len(result["children"]) == 1
    
    func_def = result["children"][0]
    assert func_def["type"] == "FUNCTION_DEF"
    assert "body" in func_def
    
    body = func_def["body"]
    assert body["type"] == "BLOCK"
    assert len(body["children"]) >= 1, "Body should contain at least one statement"
    
    print("✓ test_function_with_body_statements passed")


def test_parser_state_position_update():
    """Test that parser_state position is correctly updated after parsing."""
    # Tokens for: int foo() { }
    tokens = [
        create_token("INT", "int", 1, 1),
        create_token("IDENTIFIER", "foo", 1, 5),
        create_token("LPAREN", "(", 1, 8),
        create_token("RPAREN", ")", 1, 9),
        create_token("LBRACE", "{", 1, 11),
        create_token("RBRACE", "}", 1, 13),
    ]
    
    parser_state = {
        "tokens": tokens,
        "pos": 0,
        "filename": "test.c"
    }
    
    result = _parse_program(parser_state)
    
    # Position should be at the end of tokens
    assert parser_state["pos"] == len(tokens), f"Expected pos={len(tokens)}, got {parser_state['pos']}"
    
    print("✓ test_parser_state_position_update passed")


def test_is_at_end_integration():
    """Test _is_at_end helper in integration context."""
    tokens = [create_token("INT", "int", 1, 1)]
    
    # Not at end
    parser_state = {"tokens": tokens, "pos": 0, "filename": "test.c"}
    assert _is_at_end(parser_state) == False, "Should not be at end when pos=0"
    
    # At end
    parser_state = {"tokens": tokens, "pos": 1, "filename": "test.c"}
    assert _is_at_end(parser_state) == True, "Should be at end when pos=len(tokens)"
    
    print("✓ test_is_at_end_integration passed")


def test_parse_block_integration():
    """Test _parse_block helper in integration context."""
    # Tokens for: { }
    tokens = [
        create_token("LBRACE", "{", 1, 1),
        create_token("RBRACE", "}", 1, 2),
    ]
    
    parser_state = {
        "tokens": tokens,
        "pos": 1,  # Start after LBRACE
        "filename": "test.c"
    }
    
    result = _parse_block(parser_state)
    
    assert result["type"] == "BLOCK", f"Expected BLOCK type, got {result['type']}"
    assert parser_state["pos"] == 2, f"Expected pos=2 after parsing block, got {parser_state['pos']}"
    
    print("✓ test_parse_block_integration passed")


def test_program_ast_structure():
    """Test that PROGRAM AST node has correct structure."""
    tokens = []
    parser_state = {
        "tokens": tokens,
        "pos": 0,
        "filename": "test.c"
    }
    
    result = _parse_program(parser_state)
    
    # Verify all required fields exist
    assert "type" in result, "PROGRAM node must have 'type' field"
    assert "children" in result, "PROGRAM node must have 'children' field"
    assert "value" in result, "PROGRAM node must have 'value' field"
    assert "line" in result, "PROGRAM node must have 'line' field"
    assert "column" in result, "PROGRAM node must have 'column' field"
    
    # Verify types
    assert isinstance(result["children"], list), "children must be a list"
    assert result["value"] is None, "PROGRAM value should be None"
    
    print("✓ test_program_ast_structure passed")


def main():
    """Run all integration tests."""
    print("Running _parse_program integration tests...\n")
    
    test_empty_program()
    test_single_function()
    test_multiple_functions()
    test_function_with_parameters()
    test_function_with_body_statements()
    test_parser_state_position_update()
    test_is_at_end_integration()
    test_parse_block_integration()
    test_program_ast_structure()
    
    print("\n✅ All integration tests passed!")


if __name__ == "__main__":
    main()

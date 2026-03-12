# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_expression_package._parse_expression_src import _parse_expression
from ._parse_block_package._parse_block_src import _parse_block

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,
#   "value": str,
#   "line": int,
#   "column": int
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,
#   "children": list,
#   "value": Any,
#   "line": int,
#   "column": int
# }

ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,
#   "pos": int,
#   "filename": str,
#   "error": str
# }

# === main function ===
def _parse_for_stmt(parser_state: dict) -> dict:
    """解析 FOR 语句，返回 FOR AST 节点。"""
    tokens = parser_state["tokens"]
    filename = parser_state["filename"]
    
    # 获取 FOR token 的位置信息
    for_token = tokens[parser_state["pos"]]
    for_line = for_token["line"]
    for_column = for_token["column"]
    
    # 1. 消费 FOR token
    parser_state["pos"] += 1
    
    # 2. 消费 LPAREN
    token = _current_token(parser_state)
    if token["type"] != "LPAREN":
        raise SyntaxError(f"{filename}:{token['line']}:{token['column']}: FOR 语句期望 LPAREN")
    parser_state["pos"] += 1
    
    # 3. 解析 initializer（可为空）
    token = _current_token(parser_state)
    if token["type"] == "SEMICOLON":
        initializer_ast = None
    else:
        initializer_ast = _parse_expression(parser_state)
    
    # 4. 消费 SEMICOLON
    token = _current_token(parser_state)
    if token["type"] != "SEMICOLON":
        raise SyntaxError(f"{filename}:{token['line']}:{token['column']}: FOR 语句期望 SEMICOLON")
    parser_state["pos"] += 1
    
    # 5. 解析 condition（可为空）
    token = _current_token(parser_state)
    if token["type"] == "SEMICOLON":
        condition_ast = None
    else:
        condition_ast = _parse_expression(parser_state)
    
    # 6. 消费 SEMICOLON
    token = _current_token(parser_state)
    if token["type"] != "SEMICOLON":
        raise SyntaxError(f"{filename}:{token['line']}:{token['column']}: FOR 语句期望 SEMICOLON")
    parser_state["pos"] += 1
    
    # 7. 解析 increment（可为空）
    token = _current_token(parser_state)
    if token["type"] == "RPAREN":
        increment_ast = None
    else:
        increment_ast = _parse_expression(parser_state)
    
    # 8. 消费 RPAREN
    token = _current_token(parser_state)
    if token["type"] != "RPAREN":
        raise SyntaxError(f"{filename}:{token['line']}:{token['column']}: FOR 语句期望 RPAREN")
    parser_state["pos"] += 1
    
    # 9. 解析循环体块
    body_ast = _parse_block(parser_state)
    
    # 10. 返回 FOR AST 节点
    return {
        "type": "FOR",
        "initializer": initializer_ast,
        "condition": condition_ast,
        "increment": increment_ast,
        "body": body_ast,
        "line": for_line,
        "column": for_column
    }

# === helper functions ===
def _current_token(parser_state: ParserState) -> Token:
    """获取当前位置的 token，若越界则返回 EOF token。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    if pos < len(tokens):
        return tokens[pos]
    # 返回 EOF token
    return {"type": "EOF", "value": "", "line": -1, "column": -1}

# === OOP compatibility layer ===

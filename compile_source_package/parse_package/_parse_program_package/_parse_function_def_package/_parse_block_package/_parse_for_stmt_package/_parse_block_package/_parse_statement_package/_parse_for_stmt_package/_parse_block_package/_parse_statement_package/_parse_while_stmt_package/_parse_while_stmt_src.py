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
def _parse_while_stmt(parser_state: ParserState) -> AST:
    """解析 while 语句，语法：while (condition) { ... }"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state["filename"]
    
    # 1. 消耗 WHILE token
    if pos >= len(tokens) or tokens[pos]["type"] != "WHILE":
        raise SyntaxError(f"{filename}:{tokens[pos]['line'] if pos < len(tokens) else 0}:{tokens[pos]['column'] if pos < len(tokens) else 0}: Expected WHILE token")
    
    while_token = tokens[pos]
    pos += 1
    
    # 2. 期望并消耗 LPAREN
    if pos >= len(tokens) or tokens[pos]["type"] != "LPAREN":
        raise SyntaxError(f"{filename}:{tokens[pos]['line'] if pos < len(tokens) else while_token['line']}:{tokens[pos]['column'] if pos < len(tokens) else while_token['column']}: Expected '(' after while")
    
    pos += 1
    
    # 3. 解析条件表达式
    parser_state["pos"] = pos
    condition_ast = _parse_expression(parser_state)
    pos = parser_state["pos"]
    
    # 4. 期望并消耗 RPAREN
    if pos >= len(tokens) or tokens[pos]["type"] != "RPAREN":
        raise SyntaxError(f"{filename}:{tokens[pos]['line'] if pos < len(tokens) else condition_ast['line']}:{tokens[pos]['column'] if pos < len(tokens) else condition_ast['column']}: Expected ')' after condition")
    
    pos += 1
    
    # 5. 解析循环体块
    parser_state["pos"] = pos
    body_ast = _parse_block(parser_state)
    pos = parser_state["pos"]
    
    # 6. 返回 WHILE_STMT AST 节点
    result: AST = {
        "type": "WHILE_STMT",
        "condition": condition_ast,
        "body": body_ast,
        "line": while_token["line"],
        "column": while_token["column"]
    }
    
    parser_state["pos"] = pos
    return result

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for parser function node

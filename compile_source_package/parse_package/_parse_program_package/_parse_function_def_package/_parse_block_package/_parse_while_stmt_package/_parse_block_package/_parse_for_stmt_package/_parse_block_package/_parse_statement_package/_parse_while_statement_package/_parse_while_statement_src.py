# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ..expression_package._parse_expression_src import _parse_expression
from ..block_package._parse_block_src import _parse_block

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
def _parse_while_statement(parser_state: ParserState) -> AST:
    """解析 while 循环语句。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "<unknown>")
    
    # 1. 获取 WHILE token 信息
    while_token = tokens[pos]
    start_line = while_token["line"]
    start_column = while_token["column"]
    
    # 2. 消费 WHILE token
    parser_state["pos"] += 1
    
    # 3. 解析条件表达式
    if parser_state["pos"] >= len(tokens):
        raise SyntaxError(f"Expected condition expression after 'while' at {filename}:{start_line}")
    
    condition_ast = _parse_expression(parser_state)
    
    # 4. 消费 COLON token
    if parser_state["pos"] >= len(tokens):
        raise SyntaxError(f"Expected ':' after while condition at {filename}:{start_line}")
    
    colon_token = tokens[parser_state["pos"]]
    if colon_token["type"] != "COLON":
        raise SyntaxError(f"Expected ':' after while condition at {filename}:{start_line}")
    parser_state["pos"] += 1
    
    # 5. 解析循环体 block
    if parser_state["pos"] >= len(tokens):
        raise SyntaxError(f"Expected block after ':' at {filename}:{start_line}")
    
    body_ast = _parse_block(parser_state)
    
    # 6. 消费结束分号
    if parser_state["pos"] >= len(tokens):
        raise SyntaxError(f"Expected ';' after while loop at {filename}:{start_line}")
    
    semicolon_token = tokens[parser_state["pos"]]
    if semicolon_token["type"] != "SEMICOLON":
        raise SyntaxError(f"Expected ';' after while loop at {filename}:{start_line}")
    parser_state["pos"] += 1
    
    # 7. 构建并返回 AST
    return {
        "type": "WHILE_STMT",
        "line": start_line,
        "column": start_column,
        "children": [condition_ast, body_ast]
    }

# === helper functions ===
# No helper functions needed for this implementation

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function nodes

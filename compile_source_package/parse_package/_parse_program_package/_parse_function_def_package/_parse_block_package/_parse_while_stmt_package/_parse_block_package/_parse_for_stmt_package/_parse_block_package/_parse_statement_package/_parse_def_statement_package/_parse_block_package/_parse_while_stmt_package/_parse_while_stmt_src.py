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
    """解析 while 语句。输入：parser_state（pos 指向 WHILE 关键字）。输出：WHILE AST 节点。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 消费 WHILE 关键字
    while_token = tokens[pos]
    parser_state["pos"] += 1
    
    # 解析条件表达式
    if parser_state["pos"] >= len(tokens) or tokens[parser_state["pos"]]["type"] == "COLON":
        raise SyntaxError(
            f"Expected expression after WHILE at {parser_state['filename']}:"
            f"{while_token['line']}:{while_token['column']}"
        )
    
    condition_ast = _parse_expression(parser_state)
    
    # 期望 COLON
    pos = parser_state["pos"]
    if pos >= len(tokens) or tokens[pos]["type"] != "COLON":
        raise SyntaxError(
            f"Expected COLON after while condition at {parser_state['filename']}:"
            f"{tokens[pos]['line']}:{tokens[pos]['column']}"
        )
    parser_state["pos"] += 1
    
    # 解析块
    body_ast = _parse_block(parser_state)
    
    # 消费 SEMICOLON（_parse_block 停在 SEMICOLON 位置）
    if parser_state["pos"] < len(tokens):
        parser_state["pos"] += 1
    
    return {
        "type": "WHILE",
        "line": while_token["line"],
        "column": while_token["column"],
        "children": [condition_ast, body_ast]
    }

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function
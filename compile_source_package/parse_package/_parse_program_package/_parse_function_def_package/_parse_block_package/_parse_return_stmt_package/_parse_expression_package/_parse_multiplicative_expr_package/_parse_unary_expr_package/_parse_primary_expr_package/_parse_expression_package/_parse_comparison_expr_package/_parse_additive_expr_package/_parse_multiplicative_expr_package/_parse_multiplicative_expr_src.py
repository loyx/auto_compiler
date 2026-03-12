# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_primary_expr_package._parse_primary_expr_src import _parse_primary_expr

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
def _parse_multiplicative_expr(parser_state: ParserState) -> AST:
    """解析乘法表达式（*、/）。左结合性，返回 AST 节点。"""
    left = _parse_primary_expr(parser_state)
    
    while _is_multiplicative_op(parser_state):
        op_token = _consume_token(parser_state)
        right = _parse_primary_expr(parser_state)
        left = {
            "type": "BINARY_OP",
            "value": op_token["value"],
            "children": [left, right],
            "line": op_token["line"],
            "column": op_token["column"]
        }
    
    return left

# === helper functions ===
def _is_multiplicative_op(parser_state: ParserState) -> bool:
    """检查当前 token 是否为乘法运算符（* 或 /）。"""
    pos = parser_state["pos"]
    tokens = parser_state["tokens"]
    if pos >= len(tokens):
        return False
    token = tokens[pos]
    return token["type"] == "OPERATOR" and token["value"] in ["*", "/"]

def _consume_token(parser_state: ParserState) -> Token:
    """消费当前 token 并返回，同时推进 pos。"""
    pos = parser_state["pos"]
    tokens = parser_state["tokens"]
    if pos >= len(tokens):
        raise SyntaxError(f"Unexpected end of input in {parser_state.get('filename', 'unknown')}")
    token = tokens[pos]
    parser_state["pos"] = pos + 1
    return token

# === OOP compatibility layer ===

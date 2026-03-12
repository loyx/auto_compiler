# === std / third-party imports ===
from typing import Any, Dict, List

# === sub function imports ===
from ._parse_additive_expr_package._parse_additive_expr_src import _parse_additive_expr

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
def _parse_comparison(parser_state: ParserState) -> AST:
    """解析比较表达式（较高优先级），左结合性。"""
    left = _parse_additive_expr(parser_state)
    
    while _is_comparison_op(parser_state):
        op_token = _consume_current_token(parser_state)
        right = _parse_additive_expr(parser_state)
        left = {
            "type": "BINARY_OP",
            "operator": op_token["value"],
            "children": [left, right],
            "line": op_token["line"],
            "column": op_token["column"]
        }
    
    return left

# === helper functions ===
def _is_comparison_op(parser_state: ParserState) -> bool:
    """检查当前 token 是否为比较运算符。"""
    tokens: List[Token] = parser_state["tokens"]
    pos: int = parser_state["pos"]
    if pos >= len(tokens):
        return False
    current_token = tokens[pos]
    return current_token.get("value") in ("==", "!=", "<", "<=", ">", ">=")

def _consume_current_token(parser_state: ParserState) -> Token:
    """消费并返回当前 token。"""
    tokens: List[Token] = parser_state["tokens"]
    pos: int = parser_state["pos"]
    if pos >= len(tokens):
        raise SyntaxError(f"Unexpected end of input in {parser_state.get('filename', '<unknown>')}")
    token = tokens[pos]
    parser_state["pos"] = pos + 1
    return token

# === OOP compatibility layer ===

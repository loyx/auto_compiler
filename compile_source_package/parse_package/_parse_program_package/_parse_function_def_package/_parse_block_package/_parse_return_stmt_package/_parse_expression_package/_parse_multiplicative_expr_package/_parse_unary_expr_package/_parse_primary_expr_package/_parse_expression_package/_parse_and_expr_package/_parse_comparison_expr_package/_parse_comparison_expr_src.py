# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_primary_expr_package._parse_primary_expr_src import _parse_primary_expr
from ._consume_token_package._consume_token_src import _consume_token
from ._build_binary_op_package._build_binary_op_src import _build_binary_op

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
def _parse_comparison_expr(parser_state: ParserState) -> AST:
    """解析比较表达式，构建左结合的 BINARY_OP AST 节点。"""
    left = _parse_primary_expr(parser_state)
    
    while _is_comparison_operator(parser_state):
        op_token = _consume_token(parser_state)
        right = _parse_primary_expr(parser_state)
        left = _build_binary_op(op_token["value"], left, right, op_token)
    
    return left

# === helper functions ===
def _current_token(parser_state: ParserState) -> Token:
    """返回当前 token 但不消费。"""
    pos = parser_state["pos"]
    tokens = parser_state["tokens"]
    if pos < len(tokens):
        return tokens[pos]
    # 返回 EOF token
    return {"type": "EOF", "value": "", "line": 0, "column": 0}


def _is_comparison_operator(parser_state: ParserState) -> bool:
    """检查当前 token 是否为比较运算符。"""
    token = _current_token(parser_state)
    if token["type"] != "OPERATOR":
        return False
    return token["value"] in ("<", ">", "<=", ">=", "==", "!=")

# === OOP compatibility layer ===

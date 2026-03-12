# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_multiplicative_expr_package._parse_multiplicative_expr_src import _parse_multiplicative_expr

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
#   "filename": str,
#   "pos": int,
#   "error": str
# }


# === main function ===
def _parse_additive_expr(parser_state: ParserState) -> AST:
    """
    解析加法表达式（较低优先级，处理 + 和 - 运算符）。
    左结合性，调用 _parse_multiplicative_expr 获取操作数。
    """
    left = _parse_multiplicative_expr(parser_state)
    
    while _is_additive_operator(parser_state):
        op_token = _consume_current_token(parser_state)
        right = _parse_multiplicative_expr(parser_state)
        left = _build_binary_op(op_token, left, right)
    
    return left


# === helper functions ===
def _is_additive_operator(parser_state: ParserState) -> bool:
    """检查当前 token 是否为加法运算符 (+ 或 -)。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    if pos >= len(tokens):
        return False
    token = tokens[pos]
    return token["type"] == "OPERATOR" and token["value"] in ("+", "-")


def _consume_current_token(parser_state: ParserState) -> Token:
    """消费当前 token 并返回，同时推进 pos。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    if pos >= len(tokens):
        raise SyntaxError(f"Unexpected end of input in {parser_state.get('filename', '<unknown>')}")
    token = tokens[pos]
    parser_state["pos"] = pos + 1
    return token


def _build_binary_op(op_token: Token, left: AST, right: AST) -> AST:
    """构建二元操作符 AST 节点。"""
    return {
        "type": "BINARY_OP",
        "operator": op_token["value"],
        "children": [left, right],
        "line": op_token["line"],
        "column": op_token["column"]
    }


# === OOP compatibility layer ===
# Not required for this parser function node
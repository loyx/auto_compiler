# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_comparison_package._parse_comparison_src import _parse_comparison

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
def _parse_and_expr(parser_state: ParserState) -> AST:
    """
    解析 AND 表达式（中等优先级）。
    左结合性，构建 BINARY_OP 节点。
    """
    left = _parse_comparison(parser_state)
    
    while _is_and_keyword(parser_state):
        op_token = _consume_token(parser_state)
        right = _parse_comparison(parser_state)
        left = {
            "type": "BINARY_OP",
            "operator": "AND",
            "children": [left, right],
            "line": op_token["line"],
            "column": op_token["column"]
        }
    
    return left


# === helper functions ===
def _is_and_keyword(parser_state: ParserState) -> bool:
    """检查当前 token 是否为 AND 关键字。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    if pos >= len(tokens):
        return False
    token = tokens[pos]
    return token["type"] == "KEYWORD" and token["value"] == "AND"


def _consume_token(parser_state: ParserState) -> Token:
    """消费当前 token 并返回。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    if pos >= len(tokens):
        raise SyntaxError(f"Unexpected end of input in {parser_state['filename']}")
    token = tokens[pos]
    parser_state["pos"] = pos + 1
    return token


# === OOP compatibility layer ===
# Not needed for parser function nodes

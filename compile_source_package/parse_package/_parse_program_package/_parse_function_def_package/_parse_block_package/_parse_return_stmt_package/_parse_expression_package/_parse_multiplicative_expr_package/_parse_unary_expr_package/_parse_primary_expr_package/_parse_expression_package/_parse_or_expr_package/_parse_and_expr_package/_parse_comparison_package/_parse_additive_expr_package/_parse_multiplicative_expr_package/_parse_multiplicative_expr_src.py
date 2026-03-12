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
    """
    解析乘法表达式（较高优先级，处理 * 和 / 运算符）。
    左结合性，调用 _parse_primary_expr 获取操作数。
    """
    # Step 1: 获取左侧操作数
    left = _parse_primary_expr(parser_state)
    
    # Step 2: 循环处理乘法运算符
    while _is_multiplicative_operator(parser_state):
        op_token = _consume_token(parser_state)
        right = _parse_primary_expr(parser_state)
        
        # Step 3: 构建 BINARY_OP 节点
        left = {
            "type": "BINARY_OP",
            "operator": op_token["value"],
            "children": [left, right],
            "line": op_token["line"],
            "column": op_token["column"]
        }
    
    return left


# === helper functions ===
def _is_multiplicative_operator(parser_state: ParserState) -> bool:
    """检查当前 token 是否为乘法运算符 (* 或 /)。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        return False
    
    current_token = tokens[pos]
    return current_token["type"] == "OPERATOR" and current_token["value"] in ("*", "/")


def _consume_token(parser_state: ParserState) -> Token:
    """消费当前 token 并返回，同时推进 pos。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input")
    
    token = tokens[pos]
    parser_state["pos"] = pos + 1
    return token


# === OOP compatibility layer ===
# Not needed for parser function nodes

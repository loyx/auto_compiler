# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_primary_expr_package._parse_primary_expr_src import _parse_primary_expr

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,             # token 类型
#   "value": str,            # token 值
#   "line": int,             # 行号
#   "column": int            # 列号
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (BINARY_OP, UNARY_OP, IDENTIFIER, LITERAL, etc.)
#   "children": list,        # 子节点列表
#   "value": Any,            # 节点值
#   "line": int,             # 行号
#   "column": int            # 列号
# }

ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,          # token 列表
#   "pos": int,              # 当前位置
#   "filename": str,         # 源文件名
#   "error": str             # 错误信息（可选）
# }

# === main function ===
def _parse_multiplicative_expr(parser_state: ParserState) -> AST:
    """解析乘法/除法表达式（* 和 / 运算符），实现左结合。"""
    left = _parse_primary_expr(parser_state)
    if parser_state.get("error"):
        return left

    while _is_multiplicative_operator(parser_state):
        op_token = _current_token(parser_state)
        parser_state["pos"] += 1
        op_symbol = op_token["value"]
        line = op_token.get("line", 0)
        column = op_token.get("column", 0)

        right = _parse_primary_expr(parser_state)
        if parser_state.get("error"):
            return left

        left = {
            "type": "BINARY_OP",
            "value": op_symbol,
            "children": [left, right],
            "line": line,
            "column": column
        }

    return left

# === helper functions ===
def _is_multiplicative_operator(parser_state: ParserState) -> bool:
    """检查当前 token 是否为乘除运算符（STAR 或 SLASH）。"""
    token = _current_token(parser_state)
    if token is None:
        return False
    return token.get("type") in ("STAR", "SLASH")

def _current_token(parser_state: ParserState) -> Token:
    """获取当前位置的 token，若越界则返回 None。"""
    pos = parser_state.get("pos", 0)
    tokens = parser_state.get("tokens", [])
    if pos < 0 or pos >= len(tokens):
        return None
    return tokens[pos]

# === OOP compatibility layer ===
# No OOP wrapper needed for this parser function node.

# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._consume_token_package._consume_token_src import _consume_token
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
def _parse_and(parser_state: ParserState) -> AST:
    """
    解析逻辑与表达式（&& 运算符），优先级高于 ||。
    使用 while 循环实现左结合：a && b && c 解析为 ((a && b) && c)。
    """
    # 首先解析左侧操作数（更高优先级的比较表达式）
    left = _parse_comparison(parser_state)

    # while 循环实现左结合
    while _current_token_is_and(parser_state):
        and_token = _consume_token(parser_state, "AND")
        right = _parse_comparison(parser_state)
        left = _build_binary_op_node(left, right, and_token)

    return left


# === helper functions ===
def _current_token_is_and(parser_state: ParserState) -> bool:
    """检查当前 token 是否为 AND 类型。"""
    pos = parser_state.get("pos", 0)
    tokens = parser_state.get("tokens", [])
    if pos >= len(tokens):
        return False
    current_token = tokens[pos]
    return current_token.get("type") == "AND"


def _build_binary_op_node(left: AST, right: AST, and_token: Token) -> AST:
    """
    构建 BINARY_OP AST 节点。
    line 和 column 取自 AND token 本身。
    """
    return {
        "type": "BINARY_OP",
        "children": [left, right],
        "value": "&&",
        "line": and_token.get("line"),
        "column": and_token.get("column")
    }

# === OOP compatibility layer ===
# Not required for this parser function node

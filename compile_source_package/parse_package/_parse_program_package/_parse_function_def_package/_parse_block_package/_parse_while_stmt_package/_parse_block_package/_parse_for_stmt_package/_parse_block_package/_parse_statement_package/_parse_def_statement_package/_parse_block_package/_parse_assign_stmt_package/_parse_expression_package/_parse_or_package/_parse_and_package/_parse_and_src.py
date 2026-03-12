# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_not_package._parse_not_src import _parse_not
from ._expect_token_package._expect_token_src import _expect_token

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
#   "op": str,
#   "left": AST,
#   "right": AST,
#   "operand": AST,
#   "name": AST,
#   "args": list,
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
    解析 AND 表达式（中等优先级）。
    输入：parser_state（pos 指向 AND 表达式起始）。
    输出：AST 节点。
    处理逻辑：调用 _parse_not 解析左操作数，循环消费 AND token 并构建 BINOP 节点。
    """
    left_ast = _parse_not(parser_state)

    while _current_token_is_and(parser_state):
        and_token = _expect_token(parser_state, "AND")
        right_ast = _parse_not(parser_state)

        left_ast = {
            "type": "BINOP",
            "op": "and",
            "left": left_ast,
            "right": right_ast,
            "line": and_token["line"],
            "column": and_token["column"],
            "children": [left_ast, right_ast]
        }

    return left_ast


# === helper functions ===
def _current_token_is_and(parser_state: ParserState) -> bool:
    """检查当前 token 是否为 AND 类型。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    if pos >= len(tokens):
        return False
    return tokens[pos]["type"] == "AND"


# === OOP compatibility layer ===
# Not required for this parser function node.

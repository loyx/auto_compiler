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
# For BINARY nodes:
# {
#   "type": "BINARY",
#   "operator": str,
#   "left": AST,
#   "right": AST,
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
def _parse_equality(parser_state: ParserState) -> AST:
    """解析相等性表达式（优先级 Level 4：EQ, NE）。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "<unknown>")

    left = _parse_comparison(parser_state)

    while pos < len(tokens):
        token = tokens[pos]
        if token["type"] not in ("EQ", "NE"):
            break

        op = token["value"]
        line = token["line"]
        column = token["column"]
        parser_state["pos"] = pos + 1
        pos = parser_state["pos"]

        right = _parse_comparison(parser_state)

        left = {
            "type": "BINARY",
            "operator": op,
            "left": left,
            "right": right,
            "line": line,
            "column": column,
        }

    return left


# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function
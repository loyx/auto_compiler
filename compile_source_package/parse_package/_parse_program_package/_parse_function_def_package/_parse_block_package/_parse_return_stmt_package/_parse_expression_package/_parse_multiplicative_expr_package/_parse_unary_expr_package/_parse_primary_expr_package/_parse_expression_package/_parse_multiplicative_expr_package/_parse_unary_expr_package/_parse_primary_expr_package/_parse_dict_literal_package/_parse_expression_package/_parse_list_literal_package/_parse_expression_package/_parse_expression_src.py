# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_or_expression_package._parse_or_expression_src import _parse_or_expression

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
def _parse_expression(parser_state: ParserState) -> AST:
    """
    表达式解析入口函数。
    解析任意表达式，从最低优先级的 or 运算开始。
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        filename = parser_state.get("filename", "<unknown>")
        raise SyntaxError(
            f"SyntaxError at {filename}:0:0: Empty expression is not allowed"
        )
    
    ast = _parse_or_expression(parser_state)
    return ast


# === helper functions ===


# === OOP compatibility layer ===

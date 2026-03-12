# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_equality_package._parse_equality_src import _parse_equality

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
def _parse_expression(parser_state: ParserState) -> AST:
    """
    解析完整表达式的主入口函数。
    这是递归下降解析器的顶层入口，用于处理括号内的表达式或作为顶层解析入口。
    语法：expression := equality
    """
    # 调用 equality 层级解析函数
    result = _parse_equality(parser_state)
    return result

# === helper functions ===
# No helper functions needed for this simple delegation

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function node

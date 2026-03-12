# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_assignment_package._parse_assignment_src import _parse_assignment

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
def _parse_expression(parser_state: dict) -> dict:
    """
    解析表达式入口函数。
    从最低优先级（赋值表达式）开始递归下降解析。
    """
    return _parse_assignment(parser_state)

# === helper functions ===
# Helper functions are delegated to child modules

# === OOP compatibility layer ===
# Not required for parser function nodes

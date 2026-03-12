# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_logical_or_package._parse_logical_or_src import _parse_logical_or

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
#   "operator": str,
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
    解析完整表达式的入口函数。
    调用 _parse_logical_or 开始递归下降解析。
    """
    if parser_state.get("error"):
        return _make_error_node(parser_state)
    
    result = _parse_logical_or(parser_state)
    return result

# === helper functions ===
def _make_error_node(parser_state: ParserState) -> AST:
    """创建 ERROR 节点。"""
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    line = 1
    column = 1
    if pos < len(tokens):
        token = tokens[pos]
        line = token.get("line", 1)
        column = token.get("column", 1)
    
    return {
        "type": "ERROR",
        "value": None,
        "line": line,
        "column": column
    }

# === OOP compatibility layer ===

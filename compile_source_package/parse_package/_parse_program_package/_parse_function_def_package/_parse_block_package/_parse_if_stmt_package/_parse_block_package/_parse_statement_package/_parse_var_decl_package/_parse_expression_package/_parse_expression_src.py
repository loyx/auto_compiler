# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_primary_package._parse_primary_src import _parse_primary
from ._parse_binary_op_package._parse_binary_op_src import _parse_binary_op

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
    """解析表达式。支持算术表达式、字面量、标识符、二元运算、括号表达式。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        _raise_error(parser_state, "Unexpected end of expression")
    
    # 解析左侧操作数（基础单元）
    left = _parse_primary(parser_state)
    
    # 解析二元运算（如果有）
    result = _parse_binary_op(parser_state, left, 0)
    
    return result

# === helper functions ===
def _raise_error(parser_state: ParserState, message: str) -> None:
    """抛出 SyntaxError，包含文件名、行号、列号信息。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "<unknown>")
    
    if pos < len(tokens):
        token = tokens[pos]
        line = token.get("line", 1)
        column = token.get("column", 1)
    else:
        line = 1
        column = 1
    
    raise SyntaxError(f"{filename}:{line}:{column}: {message}")

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node

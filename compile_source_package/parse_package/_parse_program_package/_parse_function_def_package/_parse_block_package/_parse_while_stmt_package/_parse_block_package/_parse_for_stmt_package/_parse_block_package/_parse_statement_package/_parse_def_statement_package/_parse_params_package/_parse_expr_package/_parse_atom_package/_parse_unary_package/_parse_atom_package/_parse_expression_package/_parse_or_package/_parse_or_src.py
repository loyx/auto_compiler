# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_and_package._parse_and_src import _parse_and
from ._consume_token_package._consume_token_src import _consume_token
from ._current_token_type_package._current_token_type_src import _current_token_type

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
#   "column": int,
#   "op": str,
#   "left": AST,
#   "right": AST,
#   "operand": AST
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
def _parse_or(parser_state: ParserState) -> AST:
    """解析逻辑或表达式（最低优先级），构建左结合 AST。"""
    left = _parse_and(parser_state)
    
    while _current_token_type(parser_state) == "OR":
        op_line = parser_state["tokens"][parser_state["pos"]].get("line", 0)
        op_column = parser_state["tokens"][parser_state["pos"]].get("column", 0)
        
        _consume_token(parser_state, "OR")
        
        right = _parse_and(parser_state)
        
        left = {
            "type": "BINOP",
            "op": "||",
            "left": left,
            "right": right,
            "line": op_line,
            "column": op_column
        }
    
    return left

# === helper functions ===
# No helper functions needed; all logic delegated to child functions.

# === OOP compatibility layer ===
# Not needed for this parser function node.

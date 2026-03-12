# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_multiplicative_package._parse_multiplicative_src import _parse_multiplicative
from ._peek_token_package._peek_token_src import _peek_token
from ._consume_token_package._consume_token_src import _consume_token

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
def _parse_additive(state: ParserState) -> AST:
    """解析加法/减法表达式（+、- 运算符），使用左结合性。"""
    left = _parse_multiplicative(state)
    
    while True:
        token = _peek_token(state)
        if token is None:
            break
        
        if token["type"] not in ("PLUS", "MINUS"):
            break
        
        op_token = _consume_token(state)
        right = _parse_multiplicative(state)
        
        left = {
            "type": "BinaryOp",
            "value": op_token["value"],
            "children": [left, right],
            "line": op_token.get("line", 0),
            "column": op_token.get("column", 0)
        }
    
    return left

# === helper functions ===

# === OOP compatibility layer ===

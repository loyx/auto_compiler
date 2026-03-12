# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._get_current_token_package._get_current_token_src import _get_current_token
from ._advance_package._advance_src import _advance
from ._parse_primary_package._parse_primary_src import _parse_primary

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
def _parse_unary(parser_state: ParserState) -> AST:
    """解析一元表达式（负号、正号等）。"""
    token = _get_current_token(parser_state)
    
    if token is None:
        parser_state["error"] = "Unexpected end of input in unary expression"
        return {"type": "error", "value": None, "line": 0, "column": 0}
    
    if token["value"] in ("-", "+"):
        op = token["value"]
        line = token["line"]
        column = token["column"]
        _advance(parser_state)
        
        operand = _parse_unary(parser_state)
        
        return {
            "type": "unary",
            "children": [operand],
            "value": op,
            "line": line,
            "column": column
        }
    else:
        return _parse_primary(parser_state)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for parser function node
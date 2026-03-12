# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_multiplicative_package._parse_multiplicative_src import _parse_multiplicative
from ._expect_token_package._expect_token_src import _expect_token
from ._current_token_package._current_token_src import _current_token

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
def _parse_additive(parser_state: ParserState) -> AST:
    """Parse additive expressions (+, -). Left-associative."""
    left = _parse_multiplicative(parser_state)
    
    while True:
        token = _current_token(parser_state)
        if token is None or token["type"] not in ("PLUS", "MINUS"):
            break
        
        op_token = _expect_token(parser_state, token["type"])
        right = _parse_multiplicative(parser_state)
        
        left = {
            "type": "BINOP",
            "op": op_token["value"],
            "left": left,
            "right": right,
            "line": op_token["line"],
            "column": op_token["column"]
        }
    
    return left

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for parser function
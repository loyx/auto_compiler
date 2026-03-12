# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_and_package._parse_and_src import _parse_and
from ._match_package._match_src import _match
from ._previous_package._previous_src import _previous

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,             # token type (uppercase string)
#   "value": str,            # token value
#   "line": int,             # line number
#   "column": int            # column number
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # node type (BINARY_OP, UNARY_OP, ASSIGNMENT, etc.)
#   "children": list,        # child nodes (for GROUPING)
#   "value": Any,            # node value (for literals, identifiers)
#   "op": str,               # operator (for BINARY_OP, UNARY_OP)
#   "left": AST,             # left operand (for BINARY_OP)
#   "right": AST,            # right operand (for BINARY_OP)
#   "operand": AST,          # operand (for UNARY_OP)
#   "name": str,             # variable name (for ASSIGNMENT)
#   "line": int,             # line number
#   "column": int            # column number
# }

ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,          # list of Token
#   "pos": int,              # current position
#   "filename": str,         # source filename
#   "error": str             # error message (optional)
# }

# === main function ===
def _parse_or(parser_state: ParserState) -> AST:
    """Parse OR expression with left-associativity."""
    left = _parse_and(parser_state)
    
    # Propagate error from child parsing
    if parser_state.get("error"):
        return left
    
    while _match(parser_state, "OR"):
        op_token = _previous(parser_state)
        right = _parse_and(parser_state)
        
        # Propagate error from right operand parsing
        if parser_state.get("error"):
            return left
        
        left = {
            "type": "BINARY_OP",
            "op": "||",
            "left": left,
            "right": right,
            "line": op_token["line"],
            "column": op_token["column"]
        }
    
    return left

# === helper functions ===
# No helper functions - all logic delegated to child functions

# === OOP compatibility layer ===
# Not required - this is a parser function, not a framework adapter

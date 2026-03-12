# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_factor_package._parse_factor_src import _parse_factor

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
def _parse_term(parser_state: ParserState) -> AST:
    """
    Parse term expression.
    
    Grammar: term := factor ((MUL | DIV) factor)*
    
    Builds left-associative AST for term expressions.
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        raise SyntaxError(f"Expected factor, got EOF at end of file")
    
    # Parse first factor
    left = _parse_factor(parser_state)
    
    # Loop through MUL/DIV operators
    while parser_state["pos"] < len(tokens):
        current_token = tokens[parser_state["pos"]]
        token_type = current_token.get("type", "")
        
        if token_type not in ("MUL", "DIV"):
            break
        
        # Consume operator
        op_token = tokens[parser_state["pos"]]
        parser_state["pos"] += 1
        
        # Parse next factor
        right = _parse_factor(parser_state)
        
        # Build left-associative AST node
        left = {
            "type": op_token["type"],
            "line": op_token.get("line", 0),
            "column": op_token.get("column", 0),
            "children": [left, right]
        }
    
    return left

# === helper functions ===
# No helper functions needed; logic is simple enough

# === OOP compatibility layer ===
# Not needed for parser module; omit entirely
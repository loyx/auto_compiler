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
#   "pos": int,
#   "filename": str,
#   "error": str
# }

# === main function ===
def _parse_additive(parser_state: dict) -> tuple:
    """Parse additive expressions (+ and -). Returns (AST, ParserState)."""
    # Parse left side
    left_ast, state = _parse_multiplicative(parser_state)
    
    # Check for errors from multiplicative parsing
    if state.get("error"):
        return (left_ast, state)
    
    result_ast = left_ast
    current_state = state
    
    while True:
        token = _peek_token(current_state)
        
        # Check if current token is additive operator
        if token and token.get("type") == "OPERATOR" and token.get("value") in ("+", "-"):
            op_token = token
            # Consume the operator
            _, new_state = _consume_token(current_state)
            
            # Parse right side
            right_ast, next_state = _parse_multiplicative(new_state)
            
            # Check for errors
            if next_state.get("error"):
                return (right_ast, next_state)
            
            # Build binary operation AST node
            result_ast = {
                "type": "BINARY_OP",
                "operator": op_token.get("value"),
                "left": result_ast,
                "right": right_ast,
                "line": op_token.get("line"),
                "column": op_token.get("column")
            }
            
            current_state = next_state
        else:
            break
    
    return (result_ast, current_state)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for parser function
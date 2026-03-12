# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from ._parse_and_package._parse_and_src import _parse_and
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
def _parse_or(parser_state: ParserState) -> Tuple[AST, ParserState]:
    """Parse logical OR expressions (||) with left-associative chaining."""
    # Parse left operand using _parse_and
    left_ast, parser_state = _parse_and(parser_state)
    
    # Loop to handle left-associative OR chaining (a || b || c)
    while _is_current_token_or(parser_state):
        # Record position for AST node
        line = parser_state["tokens"][parser_state["pos"]].get("line", 0)
        column = parser_state["tokens"][parser_state["pos"]].get("column", 0)
        
        # Consume the OR token
        _, parser_state = _consume_token(parser_state, "OR")
        
        # Parse right operand
        right_ast, parser_state = _parse_and(parser_state)
        
        # Build BINARY_OP node
        left_ast = {
            "type": "BINARY_OP",
            "value": "||",
            "children": [left_ast, right_ast],
            "line": line,
            "column": column
        }
    
    return left_ast, parser_state

# === helper functions ===
def _is_current_token_or(parser_state: ParserState) -> bool:
    """Check if current token is OR (||) without consuming it."""
    pos = parser_state.get("pos", 0)
    tokens = parser_state.get("tokens", [])
    
    if pos >= len(tokens):
        return False
    
    current_token = tokens[pos]
    return current_token.get("type") == "OR"

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function node

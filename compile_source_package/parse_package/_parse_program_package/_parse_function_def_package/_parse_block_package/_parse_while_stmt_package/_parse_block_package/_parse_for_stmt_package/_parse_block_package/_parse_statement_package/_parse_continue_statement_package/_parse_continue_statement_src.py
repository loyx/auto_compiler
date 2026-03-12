# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No subfunctions needed

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
def _parse_continue_statement(parser_state: ParserState) -> AST:
    """Parse a continue statement."""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # Get CONTINUE token
    continue_token = tokens[pos]
    line = continue_token["line"]
    column = continue_token["column"]
    
    # Consume CONTINUE token
    pos += 1
    
    # Check for SEMICOLON
    if pos >= len(tokens) or tokens[pos]["type"] != "SEMICOLON":
        raise SyntaxError("Expected ';' after continue statement")
    
    # Consume SEMICOLON
    pos += 1
    
    # Update parser state
    parser_state["pos"] = pos
    
    # Build AST node
    ast_node: AST = {
        "type": "CONTINUE_STMT",
        "line": line,
        "column": column,
        "children": []
    }
    
    return ast_node

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for parser helper function

# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No subfunctions needed for this simple statement parser

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
def _parse_continue_stmt(parser_state: ParserState) -> AST:
    """
    Parse CONTINUE statement.
    
    Input: parser_state with pos pointing to CONTINUE token
    Output: CONTINUE AST node
    Side effect: advances parser_state["pos"] past the statement
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state["filename"]
    
    # Get CONTINUE token info for AST node
    continue_token = tokens[pos]
    line = continue_token["line"]
    column = continue_token["column"]
    
    # Consume CONTINUE token
    parser_state["pos"] += 1
    
    # Check for SEMICOLON
    if parser_state["pos"] >= len(tokens):
        raise SyntaxError(f"{filename}:{line}:{column}: missing ';' after 'continue'")
    
    semicolon_token = tokens[parser_state["pos"]]
    if semicolon_token["type"] != "SEMICOLON":
        raise SyntaxError(f"{filename}:{line}:{column}: expected ';' after 'continue'")
    
    # Consume SEMICOLON
    parser_state["pos"] += 1
    
    # Return CONTINUE AST node
    return {
        "type": "CONTINUE",
        "line": line,
        "column": column
    }

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for parser function node

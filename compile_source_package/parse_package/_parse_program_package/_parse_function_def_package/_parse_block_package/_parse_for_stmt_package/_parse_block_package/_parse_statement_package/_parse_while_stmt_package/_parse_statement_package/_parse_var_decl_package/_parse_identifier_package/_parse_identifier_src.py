# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed for this simple parser node

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
def _parse_identifier(parser_state: ParserState) -> AST:
    """
    Parse an identifier token from the parser state.
    
    Expects parser_state["pos"] to point to an IDENTIFIER token.
    Consumes the token and returns an AST node.
    Raises SyntaxError if current token is not IDENTIFIER.
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "<unknown>")
    
    # Check if current token exists and is IDENTIFIER
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}:1:1: expected identifier")
    
    current_token = tokens[pos]
    
    if current_token.get("type") != "IDENTIFIER":
        line = current_token.get("line", 1)
        column = current_token.get("column", 1)
        raise SyntaxError(f"{filename}:{line}:{column}: expected identifier")
    
    # Record token location
    line = current_token["line"]
    column = current_token["column"]
    value = current_token["value"]
    
    # Consume the token
    parser_state["pos"] = pos + 1
    
    # Return AST node
    return {
        "type": "IDENTIFIER",
        "value": value,
        "line": line,
        "column": column,
        "children": []
    }

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this parser function node

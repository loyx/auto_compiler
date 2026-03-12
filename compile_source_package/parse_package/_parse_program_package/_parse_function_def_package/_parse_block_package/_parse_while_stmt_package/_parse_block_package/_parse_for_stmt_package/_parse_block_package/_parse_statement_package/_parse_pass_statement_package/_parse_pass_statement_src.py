# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# (none - no child functions needed)

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
def _parse_pass_statement(parser_state: ParserState) -> AST:
    """Parse pass statement.
    
    pass statement syntax:
        PASS SEMICOLON
    
    Args:
        parser_state: Parser state with pos pointing to PASS token
    
    Returns:
        AST node with type "PASS_STMT"
    
    Raises:
        SyntaxError: If semicolon is missing after pass
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # Get PASS token info
    pass_token = tokens[pos]
    line = pass_token["line"]
    column = pass_token["column"]
    
    # Move past PASS token
    pos += 1
    
    # Check for semicolon
    if pos >= len(tokens) or tokens[pos]["type"] != "SEMICOLON":
        raise SyntaxError("Expected ';' after pass statement")
    
    # Move past semicolon
    pos += 1
    
    # Update parser state
    parser_state["pos"] = pos
    
    # Return AST node
    return {
        "type": "PASS_STMT",
        "line": line,
        "column": column,
        "children": []
    }

# === helper functions ===
# (none needed)

# === OOP compatibility layer ===
# (not needed - this is a parser helper function)

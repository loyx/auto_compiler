# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions needed for this simple parser

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
def _parse_break_statement(parser_state: ParserState) -> AST:
    """
    Parse break statement.
    
    Syntax: BREAK SEMICOLON
    
    Args:
        parser_state: ParserState with pos pointing to BREAK token
    
    Returns:
        AST node with type="BREAK_STMT"
    
    Raises:
        SyntaxError: If semicolon is missing after break
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # Get BREAK token and record position
    break_token = tokens[pos]
    line = break_token["line"]
    column = break_token["column"]
    
    # Consume BREAK token
    parser_state["pos"] = pos + 1
    
    # Check for semicolon
    new_pos = parser_state["pos"]
    if new_pos >= len(tokens):
        raise SyntaxError("Expected ';' after break statement")
    
    semicolon_token = tokens[new_pos]
    if semicolon_token["type"] != "SEMICOLON":
        raise SyntaxError("Expected ';' after break statement")
    
    # Consume semicolon
    parser_state["pos"] = new_pos + 1
    
    # Return BREAK_STMT AST node
    return {
        "type": "BREAK_STMT",
        "line": line,
        "column": column,
        "children": []
    }

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for parser function
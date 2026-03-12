# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed for this simple parser

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
    Parse an identifier token and return an IDENTIFIER AST node.
    
    Args:
        parser_state: Current parser state with tokens, pos, filename
        
    Returns:
        AST node with type "IDENTIFIER"
        
    Raises:
        SyntaxError: If current token is not an identifier
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # Check if current position has a token
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input: expected identifier")
    
    current_token = tokens[pos]
    
    # Verify token type is IDENTIFIER
    if current_token["type"] != "IDENTIFIER":
        raise SyntaxError(
            f"Expected identifier at line {current_token['line']}, "
            f"column {current_token['column']}, got {current_token['type']}"
        )
    
    # Consume the token (advance position)
    parser_state["pos"] = pos + 1
    
    # Build and return AST node
    return {
        "type": "IDENTIFIER",
        "value": current_token["value"],
        "line": current_token["line"],
        "column": current_token["column"]
    }

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this parser function
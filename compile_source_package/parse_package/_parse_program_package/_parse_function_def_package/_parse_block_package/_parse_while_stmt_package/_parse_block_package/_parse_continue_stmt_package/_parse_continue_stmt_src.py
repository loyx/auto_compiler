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
def _parse_continue_stmt(parser_state: ParserState) -> AST:
    """
    Parse a continue statement.
    
    Grammar: continue;
    
    Args:
        parser_state: Parser state with current position at CONTINUE keyword
        
    Returns:
        AST node with type "CONTINUE_STMT"
        
    Raises:
        SyntaxError: If syntax is invalid (missing semicolon, etc.)
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # Check we have a token at current position
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input, expected 'continue;'")
    
    # Current token should be CONTINUE
    current_token = tokens[pos]
    if current_token["type"] != "CONTINUE":
        raise SyntaxError(
            f"Expected CONTINUE keyword, got {current_token['type']} "
            f"at line {current_token['line']}, column {current_token['column']}"
        )
    
    # Record position info from CONTINUE token
    line = current_token["line"]
    column = current_token["column"]
    
    # Consume CONTINUE token
    pos += 1
    
    # Check for semicolon
    if pos >= len(tokens):
        raise SyntaxError(
            f"Expected ';' after 'continue' at line {line}, column {column}"
        )
    
    next_token = tokens[pos]
    if next_token["type"] != "SEMICOLON":
        raise SyntaxError(
            f"Expected ';' after 'continue', got {next_token['type']} "
            f"at line {next_token['line']}, column {next_token['column']}"
        )
    
    # Consume semicolon
    pos += 1
    
    # Update parser state position
    parser_state["pos"] = pos
    
    # Build and return AST node
    return {
        "type": "CONTINUE_STMT",
        "children": [],
        "line": line,
        "column": column
    }

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this parser function
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
def _parse_break_stmt(parser_state: ParserState) -> AST:
    """
    Parse a break statement.
    
    Syntax: break;
    
    Input: parser_state with current position pointing to BREAK keyword
    Output: BREAK_STMT AST node
    Raises: SyntaxError on syntax errors
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # Check if we have a BREAK token at current position
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input, expected 'break'")
    
    current_token = tokens[pos]
    if current_token.get("type") != "BREAK" or current_token.get("value") != "break":
        raise SyntaxError(f"Expected 'break' keyword, got '{current_token.get('value')}'")
    
    break_line = current_token.get("line", 0)
    break_column = current_token.get("column", 0)
    
    # Consume BREAK token
    parser_state["pos"] = pos + 1
    
    # Move to next token and check for semicolon
    pos = parser_state["pos"]
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input, expected ';'")
    
    next_token = tokens[pos]
    if next_token.get("type") != "SEMICOLON" or next_token.get("value") != ";":
        raise SyntaxError(f"Expected ';', got '{next_token.get('value')}'")
    
    # Consume SEMICOLON token
    parser_state["pos"] = pos + 1
    
    # Build and return BREAK_STMT AST node
    ast_node: AST = {
        "type": "BREAK_STMT",
        "children": [],
        "line": break_line,
        "column": break_column
    }
    
    return ast_node

# === helper functions ===
# No helper functions needed for this simple parser

# === OOP compatibility layer ===
# Not needed for this parser function
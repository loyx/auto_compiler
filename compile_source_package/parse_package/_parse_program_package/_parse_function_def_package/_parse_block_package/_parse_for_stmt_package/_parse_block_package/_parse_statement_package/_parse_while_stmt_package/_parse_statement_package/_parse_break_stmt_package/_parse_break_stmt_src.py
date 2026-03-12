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
def _parse_break_stmt(parser_state: ParserState) -> AST:
    """Parse break statement. Syntax: break ;"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "<unknown>")
    
    # Step 1: Current token must be BREAK
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}:0:0: Unexpected end of input, expected 'break'")
    
    token = tokens[pos]
    if token["type"] != "BREAK":
        raise SyntaxError(
            f"{filename}:{token['line']}:{token['column']}: "
            f"Expected 'break', got '{token['value']}'"
        )
    
    break_line = token["line"]
    break_column = token["column"]
    
    # Step 2: Consume BREAK token
    pos += 1
    
    # Step 3: Next token must be SEMICOLON
    if pos >= len(tokens):
        raise SyntaxError(
            f"{filename}:{break_line}:{break_column}: "
            f"Expected ';' after 'break'"
        )
    
    semicolon_token = tokens[pos]
    if semicolon_token["type"] != "SEMICOLON":
        raise SyntaxError(
            f"{filename}:{semicolon_token['line']}:{semicolon_token['column']}: "
            f"Expected ';', got '{semicolon_token['value']}'"
        )
    
    # Step 4: Consume SEMICOLON token
    pos += 1
    
    # Update parser state position
    parser_state["pos"] = pos
    
    # Step 5: Return BREAK_STMT AST node
    return {
        "type": "BREAK_STMT",
        "children": [],
        "line": break_line,
        "column": break_column
    }

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for parser helper function
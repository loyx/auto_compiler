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
def _parse_continue_stmt(parser_state: ParserState) -> AST:
    """
    Parse continue statement: continue;
    
    Input: parser_state with pos pointing to CONTINUE keyword
    Output: CONTINUE_STMT AST node
    Side effect: modifies parser_state["pos"]
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state["filename"]
    
    # Record CONTINUE keyword position
    continue_token = tokens[pos]
    line = continue_token["line"]
    column = continue_token["column"]
    
    # Consume CONTINUE keyword
    pos += 1
    
    # Check for SEMICOLON
    if pos >= len(tokens) or tokens[pos]["type"] != "SEMICOLON":
        raise SyntaxError(f"{filename}:{line}:{column}: Expected ';' after continue")
    
    # Consume SEMICOLON
    pos += 1
    
    # Update parser state position
    parser_state["pos"] = pos
    
    # Build CONTINUE_STMT AST node
    ast_node: AST = {
        "type": "CONTINUE_STMT",
        "children": [],
        "line": line,
        "column": column
    }
    
    return ast_node

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for parser function node

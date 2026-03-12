# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No subfunctions required for this parser node

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
    Parse break statement (break;).
    
    Input: parser_state with pos pointing to BREAK keyword token.
    Output: BREAK_STMT AST node.
    Side effect: modifies parser_state["pos"] to consume BREAK and SEMICOLON.
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state["filename"]
    
    # Step 1: Record BREAK token position
    break_token = tokens[pos]
    line = break_token["line"]
    column = break_token["column"]
    
    # Step 2: Consume BREAK keyword
    parser_state["pos"] += 1
    pos = parser_state["pos"]
    
    # Step 3: Check and consume SEMICOLON
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}:{line}:{column}: expected ';' after break")
    
    semicolon_token = tokens[pos]
    if semicolon_token["type"] != "SEMICOLON":
        raise SyntaxError(f"{filename}:{line}:{column}: expected ';' after break, got '{semicolon_token['value']}'")
    
    # Consume SEMICOLON
    parser_state["pos"] += 1
    
    # Step 4: Build BREAK_STMT AST node
    ast_node: AST = {
        "type": "BREAK_STMT",
        "children": [],
        "line": line,
        "column": column
    }
    
    return ast_node

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not required for parser function nodes

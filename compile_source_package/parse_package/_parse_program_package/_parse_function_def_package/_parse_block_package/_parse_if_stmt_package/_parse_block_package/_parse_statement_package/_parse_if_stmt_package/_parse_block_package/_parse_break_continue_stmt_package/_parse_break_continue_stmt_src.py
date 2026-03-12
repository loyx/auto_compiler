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
#   "filename": str,
#   "pos": int,
#   "error": str
# }

# === main function ===
def _parse_break_continue_stmt(parser_state: ParserState) -> AST:
    """
    Parse break or continue statement.
    
    Input: parser_state with pos pointing to BREAK or CONTINUE token
    Output: AST node for BREAK or CONTINUE
    Side effect: modifies parser_state["pos"] to consume the token
    Raises: SyntaxError if token is not BREAK or CONTINUE
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state["filename"]
    
    # Get current token
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}:0:0: Unexpected end of input, expected BREAK or CONTINUE")
    
    current_token = tokens[pos]
    token_type = current_token.get("type", "")
    line = current_token.get("line", 0)
    column = current_token.get("column", 0)
    
    # Validate token type
    if token_type not in ("BREAK", "CONTINUE"):
        raise SyntaxError(f"{filename}:{line}:{column}: Expected BREAK or CONTINUE, got {token_type}")
    
    # Consume the token
    parser_state["pos"] = pos + 1
    
    # Build AST node
    ast_node: AST = {
        "type": token_type,
        "line": line,
        "column": column
    }
    
    return ast_node

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for parser internal function
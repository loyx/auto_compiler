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
    Parse break statement.
    
    Consumes BREAK token and returns BREAK_STMT AST node.
    Side effect: updates parser_state["pos"].
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # Get current BREAK token
    break_token = tokens[pos]
    
    # Build AST node
    ast_node: AST = {
        "type": "BREAK_STMT",
        "line": break_token["line"],
        "column": break_token["column"],
        "children": []
    }
    
    # Consume BREAK token (side effect)
    parser_state["pos"] = pos + 1
    
    return ast_node

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for parser function node

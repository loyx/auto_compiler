# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._expect_token_package._expect_token_src import _expect_token

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
#   "type": str,             # BREAK_STMT
#   "children": list,        # 空列表
#   "value": str,            # "break"
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
    Parse break statement (break ;) and return BREAK_STMT AST node.
    
    Input: parser_state with pos pointing to BREAK token
    Output: BREAK_STMT AST node
    Side effect: Consumes BREAK and SEMICOLON tokens, updates pos
    Exception: Raises SyntaxError on syntax error
    """
    current_pos = parser_state["pos"]
    token = parser_state["tokens"][current_pos]
    
    # Consume BREAK token
    _expect_token(parser_state, "BREAK")
    
    # Consume SEMICOLON token
    _expect_token(parser_state, "SEMICOLON")
    
    # Build and return BREAK_STMT AST node
    return {
        "type": "BREAK_STMT",
        "children": [],
        "value": "break",
        "line": token["line"],
        "column": token["column"]
    }

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function node

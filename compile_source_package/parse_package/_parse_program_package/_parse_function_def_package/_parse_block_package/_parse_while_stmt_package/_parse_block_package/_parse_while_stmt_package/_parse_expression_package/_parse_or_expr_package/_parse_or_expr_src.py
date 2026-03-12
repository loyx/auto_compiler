# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from ._parse_and_expr_package._parse_and_expr_src import _parse_and_expr
from ._peek_token_package._peek_token_src import _peek_token
from ._consume_token_package._consume_token_src import _consume_token

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
def _parse_or_expr(parser_state: ParserState) -> Tuple[AST, ParserState]:
    """Parse 'or' expressions (lowest precedence)."""
    left_ast, parser_state = _parse_and_expr(parser_state)
    
    while True:
        token = _peek_token(parser_state)
        if token is None or token.get("type") != "OR":
            break
        
        parser_state = _consume_token(parser_state)
        right_ast, parser_state = _parse_and_expr(parser_state)
        
        left_ast = {
            "type": "BINARY_OP",
            "operator": "or",
            "children": [left_ast, right_ast],
            "line": token.get("line", 0),
            "column": token.get("column", 0)
        }
    
    return left_ast, parser_state

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for parser function node
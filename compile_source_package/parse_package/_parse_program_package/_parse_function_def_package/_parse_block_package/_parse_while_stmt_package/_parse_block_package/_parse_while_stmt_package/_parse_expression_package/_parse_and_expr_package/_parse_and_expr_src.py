# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from .._peek_token_package._peek_token_src import _peek_token
from ._consume_token_package._consume_token_src import _consume_token
from ._parse_comparison_package._parse_comparison_src import _parse_comparison

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
def _parse_and_expr(parser_state: ParserState) -> tuple[AST, ParserState]:
    """Parse 'and' expressions with left associativity."""
    # Parse left side
    left_ast, parser_state = _parse_comparison(parser_state)
    
    # Loop to handle consecutive 'and' operators
    while True:
        token = _peek_token(parser_state)
        if token is None or token["type"] != "AND":
            break
        
        # Consume the AND token
        _, parser_state = _consume_token(parser_state, "AND")
        
        # Parse right side
        right_ast, parser_state = _parse_comparison(parser_state)
        
        # Build BINARY_OP node with left associativity
        left_ast = {
            "type": "BINARY_OP",
            "operator": "and",
            "children": [left_ast, right_ast],
            "line": left_ast.get("line", token["line"]),
            "column": left_ast.get("column", token["column"])
        }
    
    return left_ast, parser_state

# === helper functions ===
# No helper functions needed for this simple logic

# === OOP compatibility layer ===
# Not needed for parser function nodes
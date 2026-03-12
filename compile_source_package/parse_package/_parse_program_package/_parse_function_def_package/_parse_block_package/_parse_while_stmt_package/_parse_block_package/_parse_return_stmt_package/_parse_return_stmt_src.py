# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._peek_token_package._peek_token_src import _peek_token
from ._consume_token_package._consume_token_src import _consume_token
from ._parse_expression_package._parse_expression_src import _parse_expression

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
def _parse_return_stmt(parser_state: dict) -> dict:
    """Parse a return statement and return an AST node."""
    token = _peek_token(parser_state)
    line = token.get("line", 0)
    column = token.get("column", 0)
    
    # Consume RETURN keyword
    parser_state = _consume_token(parser_state, "RETURN")
    
    # Check if there's a return expression or just semicolon
    token = _peek_token(parser_state)
    children = []
    
    if token is not None and token.get("type") != "SEMICOLON":
        # Parse the return expression
        expr_ast = _parse_expression(parser_state)
        children.append(expr_ast)
    
    # Consume semicolon
    parser_state = _consume_token(parser_state, "SEMICOLON")
    
    return {
        "type": "RETURN_STMT",
        "children": children,
        "line": line,
        "column": column
    }

# === helper functions ===
# No helper functions needed; all logic delegated to child functions.

# === OOP compatibility layer ===
# No OOP wrapper needed for this parser function node.

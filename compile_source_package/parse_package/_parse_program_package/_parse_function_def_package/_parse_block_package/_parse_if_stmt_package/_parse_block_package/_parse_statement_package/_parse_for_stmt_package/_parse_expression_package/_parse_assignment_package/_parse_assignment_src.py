# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_comparison_package._parse_comparison_src import _parse_comparison
from ._get_current_token_package._get_current_token_src import _get_current_token
from ._advance_package._advance_src import _advance
from ._syntax_error_package._syntax_error_src import _syntax_error

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
def _parse_assignment(parser_state: dict) -> dict:
    """Parse assignment expression (right-associative '=' operator)."""
    # Step 1: Parse left side as comparison expression
    left = _parse_comparison(parser_state)
    
    # Step 2: Check if current token is '='
    current_token = _get_current_token(parser_state)
    
    if current_token is None or current_token.get("value") != "=":
        # Not an assignment, return comparison result
        return left
    
    # Step 3: Validate left side is assignable (must be identifier)
    if left.get("type") != "identifier":
        _syntax_error(parser_state, "Left side of assignment must be an identifier")
        return left
    
    # Step 4: Consume '=' token and record position
    line = current_token.get("line", 0)
    column = current_token.get("column", 0)
    _advance(parser_state)
    
    # Step 5: Recursively parse right side (right-associative)
    right = _parse_assignment(parser_state)
    
    # Step 6: Build assignment AST node
    return {
        "type": "assignment",
        "children": [left, right],
        "value": "=",
        "line": line,
        "column": column
    }

# === helper functions ===
# No helper functions needed; all logic is in main function

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function node

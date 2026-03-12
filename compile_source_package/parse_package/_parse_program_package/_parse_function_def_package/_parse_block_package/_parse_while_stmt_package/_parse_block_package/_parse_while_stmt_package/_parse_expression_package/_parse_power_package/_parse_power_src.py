# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_unary_package._parse_unary_src import _parse_unary
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
def _parse_power(parser_state: dict) -> tuple:
    """
    Parse power expressions (**). Right-associative.
    Input: parser_state dict
    Output: (AST node, updated_parser_state)
    """
    # Parse the base (right-hand side expression)
    base_ast, parser_state = _parse_unary(parser_state)
    
    # Check if current token is DOUBLESTAR
    current_token = _peek_token(parser_state)
    
    if current_token is not None and current_token.get("type") == "DOUBLESTAR":
        # Record position for error reporting
        line = current_token.get("line", 0)
        column = current_token.get("column", 0)
        
        # Consume the DOUBLESTAR token
        _consume_token(parser_state, "DOUBLESTAR")
        
        # Recursively call _parse_power to parse the exponent (right-associative)
        exponent_ast, parser_state = _parse_power(parser_state)
        
        # Build BINARY_OP AST node
        result_ast = {
            "type": "BINARY_OP",
            "operator": "**",
            "children": [base_ast, exponent_ast],
            "line": line,
            "column": column
        }
        
        return (result_ast, parser_state)
    
    # No power operator, return the base as-is
    return (base_ast, parser_state)

# === helper functions ===
# No helper functions needed - all logic is in main function

# === OOP compatibility layer ===
# Not needed for this parser function node

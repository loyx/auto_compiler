# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from ._parse_multiplicative_package._parse_multiplicative_src import _parse_multiplicative
from ._get_current_token_package._get_current_token_src import _get_current_token
from ._consume_token_package._consume_token_src import _consume_token
from ._is_operator_token_package._is_operator_token_src import _is_operator_token

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
def _parse_additive(parser_state: ParserState) -> Tuple[AST, ParserState]:
    """Parse additive expressions (+, -) with left associativity."""
    # Parse left operand (higher precedence: multiplicative)
    left_ast, parser_state = _parse_multiplicative(parser_state)
    
    # Loop for consecutive + or - operators (left-associative)
    while True:
        current_token = _get_current_token(parser_state)
        if not _is_operator_token(current_token, ['+', '-']):
            break
        
        op_token = current_token
        parser_state = _consume_token(parser_state)
        
        # Parse right operand (higher precedence: multiplicative)
        right_ast, parser_state = _parse_multiplicative(parser_state)
        
        # Build BINARY_OP AST node (left-associative: accumulate into left_ast)
        left_ast = {
            "type": "BINARY_OP",
            "value": op_token["value"],
            "children": [left_ast, right_ast],
            "line": op_token.get("line", 0),
            "column": op_token.get("column", 0)
        }
    
    return left_ast, parser_state

# === helper functions ===
# No helper functions needed - all logic delegated to sub-functions

# === OOP compatibility layer ===
# Not needed for parser function node

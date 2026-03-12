# === std / third-party imports ===
from typing import Any, Dict, Tuple

# === sub function imports ===
from ._parse_additive_package._parse_additive_src import _parse_additive
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
def _parse_comparison(parser_state: ParserState) -> Tuple[AST, ParserState]:
    """Parse comparison expressions (==, !=, <, >, <=, >=).
    
    Returns:
        Tuple[AST, ParserState]: AST node and updated parser state.
        If comparison operator found: returns BINARY_OP node.
        If no comparison operator: returns left operand directly.
    """
    # Parse left operand
    left_ast, state = _parse_additive(parser_state)
    if state.get("error"):
        return left_ast, state
    
    # Check for comparison operators
    current_token = _peek_token(state)
    if current_token is None:
        return left_ast, state
    
    # Check if current token is a comparison operator
    operator_value = current_token.get("value")
    if operator_value not in {"==", "!=", "<", ">", "<=", ">="}:
        return left_ast, state
    
    # Consume the comparison operator
    operator_token, state_after_op = _consume_token(state, "OPERATOR")
    if state_after_op.get("error"):
        return left_ast, state_after_op
    
    # Parse right operand
    right_ast, state_after_right = _parse_additive(state_after_op)
    if state_after_right.get("error"):
        return right_ast, state_after_right
    
    # Build BINARY_OP AST node
    ast_node = {
        "type": "BINARY_OP",
        "operator": operator_value,
        "left": left_ast,
        "right": right_ast,
        "line": operator_token.get("line", 0),
        "column": operator_token.get("column", 0)
    }
    
    return ast_node, state_after_right

# === helper functions ===
# No helper functions needed for this module

# === OOP compatibility layer ===
# Not needed for parser function
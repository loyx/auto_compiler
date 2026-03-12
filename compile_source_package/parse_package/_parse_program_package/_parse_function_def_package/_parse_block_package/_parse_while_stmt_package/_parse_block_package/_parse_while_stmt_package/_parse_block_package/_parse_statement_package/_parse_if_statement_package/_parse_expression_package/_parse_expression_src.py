# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_primary_package._parse_primary_src import _parse_primary
from ._get_precedence_package._get_precedence_src import _get_precedence

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
def _parse_expression(parser_state: dict) -> dict:
    """
    Parse expression using precedence climbing algorithm.
    Handles binary operators with proper precedence.
    Modifies parser_state in-place by advancing pos.
    Returns expression AST node.
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of expression")
    
    # Parse left side (primary expression)
    left = _parse_primary(parser_state)
    
    # Handle binary operators with precedence climbing
    while parser_state["pos"] < len(tokens):
        current_token = tokens[parser_state["pos"]]
        op_type = current_token.get("type", "")
        
        # Check if current token is a binary operator
        precedence = _get_precedence(op_type)
        if precedence == 0:
            break
        
        # Consume operator token
        parser_state["pos"] += 1
        operator = current_token.get("value", op_type)
        op_line = current_token.get("line", 0)
        op_column = current_token.get("column", 0)
        
        # Parse right side with precedence handling
        right = _parse_primary(parser_state)
        
        # Continue binding while next operator has higher or equal precedence
        while parser_state["pos"] < len(tokens):
            next_token = tokens[parser_state["pos"]]
            next_op_type = next_token.get("type", "")
            next_precedence = _get_precedence(next_op_type)
            
            if next_precedence <= precedence:
                break
            
            # Consume next operator
            parser_state["pos"] += 1
            next_op = next_token.get("value", next_op_type)
            
            # Build right-associative tree
            right = {
                "type": "BINARY_OP",
                "left": right,
                "operator": next_op,
                "right": _parse_primary(parser_state),
                "line": next_token.get("line", 0),
                "column": next_token.get("column", 0)
            }
        
        # Build AST node for this operation
        left = {
            "type": "BINARY_OP",
            "left": left,
            "operator": operator,
            "right": right,
            "line": op_line,
            "column": op_column
        }
    
    return left

# === helper functions ===
def _expect_token(parser_state: dict, expected_type: str) -> dict:
    """
    Helper to expect and consume a specific token type.
    Raises SyntaxError if token doesn't match.
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        raise SyntaxError(f"Expected {expected_type}, got end of input")
    
    token = tokens[pos]
    if token.get("type") != expected_type:
        raise SyntaxError(f"Expected {expected_type}, got {token.get('type')}")
    
    parser_state["pos"] += 1
    return token

# === OOP compatibility layer ===
# Not needed for parser helper function

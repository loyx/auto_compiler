# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_primary_package._parse_primary_src import _parse_primary

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
#   "filename": str,
#   "pos": int,
#   "error": str
# }

# === main function ===
def _parse_binary_op(parser_state: ParserState, min_precedence: int, left: AST) -> AST:
    """
    Parse binary operations with precedence climbing algorithm.
    Modifies parser_state['pos'] as operators and operands are consumed.
    """
    # Operator precedence table
    OPERATOR_PRECEDENCE = {
        "PLUS": 1,
        "MINUS": 1,
        "STAR": 2,
        "SLASH": 2,
    }
    
    while True:
        tokens = parser_state["tokens"]
        pos = parser_state["pos"]
        
        # Check if we have a token to examine
        if pos >= len(tokens):
            return left
        
        current_token = tokens[pos]
        op_type = current_token.get("type")
        
        # Check if current token is a binary operator
        if op_type not in OPERATOR_PRECEDENCE:
            return left
        
        op_precedence = OPERATOR_PRECEDENCE[op_type]
        
        # Check if operator precedence meets minimum threshold
        if op_precedence < min_precedence:
            return left
        
        # Record operator info
        op = current_token.get("value", op_type)
        line = current_token.get("line", 0)
        column = current_token.get("column", 0)
        
        # Consume operator token
        parser_state["pos"] = pos + 1
        
        # Parse right operand
        right = _parse_primary(parser_state)
        
        # Check for next operator to determine precedence for recursion
        next_pos = parser_state["pos"]
        next_precedence = 0
        if next_pos < len(tokens):
            next_token = tokens[next_pos]
            next_op_type = next_token.get("type")
            if next_op_type in OPERATOR_PRECEDENCE:
                next_precedence = OPERATOR_PRECEDENCE[next_op_type]
        
        # For left-associative operators, use precedence + 1
        # For right-associative, would use precedence (all arithmetic ops are left-assoc)
        right_min_precedence = op_precedence + 1
        
        # If next operator has lower or equal precedence, don't recurse deeper
        if next_precedence <= op_precedence:
            right_min_precedence = op_precedence + 1
        
        # Recursively parse any higher-precedence operators on the right
        right = _parse_binary_op(parser_state, right_min_precedence, right)
        
        # Build binary operation AST node
        left = {
            "type": "BINARY_OP",
            "operator": op,
            "children": [left, right],
            "line": line,
            "column": column,
        }
    
    return left

# === helper functions ===
# No helper functions needed - logic is contained in main function

# === OOP compatibility layer ===
# Not needed - this is a parser helper function, not a framework entry point

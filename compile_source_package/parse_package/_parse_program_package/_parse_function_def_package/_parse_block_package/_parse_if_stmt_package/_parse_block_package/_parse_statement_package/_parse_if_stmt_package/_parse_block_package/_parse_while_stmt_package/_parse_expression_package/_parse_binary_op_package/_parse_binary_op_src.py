# === std / third-party imports ===
from typing import Any, Dict

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

# Operator precedence table (from low to high)
OPERATOR_PRECEDENCE = {
    "OR": 1,
    "AND": 2,
    "EQ": 3, "NE": 3, "LT": 3, "LE": 3, "GT": 3, "GE": 3,
    "PLUS": 4, "MINUS": 4,
    "STAR": 5, "SLASH": 5, "PERCENT": 5,
    "DOUBLESTAR": 6,
}

# Right-associative operators
RIGHT_ASSOCIATIVE = {"DOUBLESTAR"}

# === main function ===
def _parse_binary_op(parser_state: dict, left: dict, min_precedence: int) -> dict:
    """
    Parse binary operator expressions using precedence climbing algorithm.
    Input: parser_state (pos at left operand), left AST node, min_precedence.
    Output: complete expression AST node.
    Side effect: modifies parser_state["pos"] to end of expression.
    """
    # Lazy import to avoid circular dependency
    from ._parse_unary_op_package._parse_unary_op_src import _parse_unary_op
    
    tokens = parser_state["tokens"]
    
    while True:
        if parser_state["pos"] >= len(tokens):
            break
        
        current_token = tokens[parser_state["pos"]]
        op_type = current_token.get("type")
        
        # Check if current token is a binary operator
        if op_type not in OPERATOR_PRECEDENCE:
            break
        
        precedence = OPERATOR_PRECEDENCE[op_type]
        
        # If operator precedence < min_precedence, return current left
        if precedence < min_precedence:
            break
        
        # Record operator and advance pos
        operator = current_token.get("value", op_type)
        op_line = current_token.get("line", 0)
        op_column = current_token.get("column", 0)
        parser_state["pos"] += 1
        
        # Parse right operand
        if parser_state["pos"] >= len(tokens):
            raise SyntaxError(f"Unexpected end of expression after operator '{operator}'")
        
        right = _parse_unary_op(parser_state)
        
        # Determine next min_precedence based on associativity
        if op_type in RIGHT_ASSOCIATIVE:
            next_min_precedence = precedence
        else:
            next_min_precedence = precedence + 1
        
        # Recursively parse right side binary operations
        right = _parse_binary_op(parser_state, right, next_min_precedence)
        
        # Build binary operation AST node
        left = {
            "type": "binary_op",
            "operator": operator,
            "left": left,
            "right": right,
            "line": op_line,
            "column": op_column
        }
    
    return left

# === helper functions ===
def _get_token_precedence(token_type: str) -> int:
    """Get precedence level for a token type. Returns 0 if not an operator."""
    return OPERATOR_PRECEDENCE.get(token_type, 0)

# === OOP compatibility layer ===
# Not needed for this parser function node

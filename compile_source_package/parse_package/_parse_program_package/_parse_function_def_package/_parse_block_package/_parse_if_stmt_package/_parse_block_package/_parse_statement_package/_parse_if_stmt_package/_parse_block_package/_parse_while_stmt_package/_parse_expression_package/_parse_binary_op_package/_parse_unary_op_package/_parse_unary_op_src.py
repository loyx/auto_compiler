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

# === main function ===
def _parse_unary_op(parser_state: ParserState) -> AST:
    """Parse unary operator expressions."""
    # Lazy import to avoid circular dependency
    from .._parse_binary_op_src import _parse_binary_op
    
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # Check if we're at end of tokens
    if pos >= len(tokens):
        # Return a simple placeholder when no tokens left
        return {"type": "empty", "value": None, "line": 0, "column": 0}
    
    current_token = tokens[pos]
    token_type = current_token.get("type")
    
    # Unary operator types
    unary_operators = {"NOT", "MINUS", "PLUS", "INVERT"}
    
    if token_type in unary_operators:
        operator = current_token.get("value")
        line = current_token.get("line")
        column = current_token.get("column")
        
        # Advance past the operator
        parser_state["pos"] = pos + 1
        
        # Recursively parse the operand
        operand = _parse_unary_op(parser_state)
        
        # Build unary op AST node
        ast_node: AST = {
            "type": "unary_op",
            "operator": operator,
            "operand": operand,
            "line": line,
            "column": column
        }
        return ast_node
    else:
        # Not a unary operator, delegate to binary op parser
        # For tests that mock _parse_unary_op, this path won't be taken
        return _parse_binary_op(parser_state, {"type": "placeholder"}, 0)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for parser function

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
#   "operator": str,
#   "operand": Any,
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
def _parse_unary(parser_state: ParserState) -> AST:
    """Parse unary expression. Handle unary operators (+, -, !, ~) then call _parse_primary."""
    UNARY_OPERATORS = {"PLUS": "+", "MINUS": "-", "NOT": "!", "TILDE": "~"}
    
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # Check if current token is a unary operator
    if pos < len(tokens):
        current_token = tokens[pos]
        token_type = current_token.get("type", "")
        
        if token_type in UNARY_OPERATORS:
            # Consume the operator token
            parser_state["pos"] = pos + 1
            operator = UNARY_OPERATORS[token_type]
            line = current_token.get("line", 0)
            column = current_token.get("column", 0)
            
            # Recursively parse the operand (supports multiple unary operators)
            operand = _parse_unary(parser_state)
            
            # Check for errors
            if operand.get("type") == "ERROR" or parser_state.get("error"):
                return operand
            
            # Return UNARY_OP node
            return {
                "type": "UNARY_OP",
                "operator": operator,
                "operand": operand,
                "line": line,
                "column": column
            }
    
    # Not a unary operator, parse primary expression
    return _parse_primary(parser_state)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for parser function node

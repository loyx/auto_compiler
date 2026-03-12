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
#   "pos": int,
#   "filename": str,
#   "error": str
# }

# === main function ===
def _parse_unary(parser_state: ParserState) -> AST:
    """Parse unary expressions (- and ! operators)."""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input while parsing unary expression")
    
    current_token = tokens[pos]
    token_type = current_token.get("type", "")
    token_value = current_token.get("value", "")
    line = current_token.get("line", 0)
    column = current_token.get("column", 0)
    
    # Check if current token is a unary operator
    if token_type == "OPERATOR" and token_value in ("-", "!"):
        operator = token_value
        operator_line = line
        operator_column = column
        
        # Advance position
        parser_state["pos"] = pos + 1
        
        # Recursively parse the operand (supports chained unary ops like --x, !!x)
        operand = _parse_unary(parser_state)
        
        # Build UNARY_OP AST node
        return {
            "type": "UNARY_OP",
            "children": [operand],
            "value": operator,
            "line": operator_line,
            "column": operator_column
        }
    else:
        # Not a unary operator, parse primary expression
        return _parse_primary(parser_state)

# === helper functions ===
# No helper functions needed for this module

# === OOP compatibility layer ===
# Not needed for parser function nodes

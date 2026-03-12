# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_additive_expression_package._parse_additive_expression_src import _parse_additive_expression

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
def _parse_comparison(parser_state: ParserState) -> AST:
    """Parse comparison expressions (<, >, <=, >=, ==, !=)."""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # Parse left operand using additive expression
    left = _parse_additive_expression(parser_state)
    
    # Check for comparison operators
    comparison_ops = {"<", ">", "<=", ">=", "==", "!="}
    
    while parser_state["pos"] < len(tokens):
        current_token = tokens[parser_state["pos"]]
        
        if current_token.get("value") not in comparison_ops:
            break
        
        # Record operator
        op_token = current_token
        op_line = op_token.get("line", 0)
        op_column = op_token.get("column", 0)
        
        # Advance position
        parser_state["pos"] += 1
        
        # Parse right operand
        if parser_state["pos"] >= len(tokens):
            raise SyntaxError(
                f"Expected right operand after '{op_token['value']}' "
                f"at line {op_line}, column {op_column}"
            )
        
        right = _parse_additive_expression(parser_state)
        
        # Build BINARY_OP node
        left = {
            "type": "BINARY_OP",
            "value": op_token["value"],
            "children": [left, right],
            "line": op_line,
            "column": op_column
        }
    
    return left

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for parser function
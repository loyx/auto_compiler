# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_term_package._parse_term_src import _parse_term

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
#   "column": int,
#   "operator": str,
#   "left": AST,
#   "right": AST,
#   "operand": AST
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
    """
    Parse comparison (<, >, <=, >=) expressions.
    Priority: higher than term, lower than equality.
    Supports left-to-right chaining: a < b < c
    """
    left = _parse_term(parser_state)
    
    comparison_ops = {"<", ">", "<=", ">="}
    
    while True:
        tokens = parser_state["tokens"]
        pos = parser_state["pos"]
        
        if pos >= len(tokens):
            break
        
        current_token = tokens[pos]
        op_value = current_token.get("value", "")
        
        if op_value not in comparison_ops:
            break
        
        parser_state["pos"] += 1
        op_line = current_token.get("line", 0)
        op_column = current_token.get("column", 0)
        
        right = _parse_term(parser_state)
        
        left = {
            "type": "BINARY",
            "operator": op_value,
            "left": left,
            "right": right,
            "line": op_line,
            "column": op_column
        }
    
    return left

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not required for parser function nodes

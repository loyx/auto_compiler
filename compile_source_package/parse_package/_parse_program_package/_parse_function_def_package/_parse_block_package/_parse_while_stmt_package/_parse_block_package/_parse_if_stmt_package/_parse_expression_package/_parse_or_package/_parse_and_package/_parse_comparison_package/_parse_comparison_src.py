# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._consume_token_package._consume_token_src import _consume_token
from ._parse_additive_package._parse_additive_src import _parse_additive

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
    """
    Parse comparison expressions (==, !=, <, >, <=, >=).
    Priority is higher than && and ||, lower than additive expressions.
    """
    # Parse left operand using higher-precedence parser
    left = _parse_additive(parser_state)
    
    # Check if current token is a comparison operator
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    comparison_types = {"EQ", "NE", "LT", "GT", "LE", "GE"}
    
    if pos < len(tokens) and tokens[pos]["type"] in comparison_types:
        op_token = tokens[pos]
        op_type = op_token["type"]
        
        # Map token type to actual operator string
        op_map = {
            "EQ": "==",
            "NE": "!=",
            "LT": "<",
            "GT": ">",
            "LE": "<=",
            "GE": ">="
        }
        operator = op_map[op_type]
        
        # Consume the operator token
        _consume_token(parser_state, op_type)
        
        # Parse right operand
        right = _parse_additive(parser_state)
        
        # Build BINARY_OP AST node
        return {
            "type": "BINARY_OP",
            "children": [left, right],
            "value": operator,
            "line": op_token["line"],
            "column": op_token["column"]
        }
    
    # No comparison operator, return left operand as-is
    return left

# === helper functions ===
# No helper functions needed for this simple parsing logic

# === OOP compatibility layer ===
# Not needed for parser function nodes

# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
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
#   "line": int,
#   "column": int,
#   "value": Any,
#   "literal_type": str,
#   "name": str,
#   "operator": str,
#   "left": AST,
#   "right": AST,
#   "operand": AST,
#   "callee": AST,
#   "arguments": list
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
    Parse comparison expressions (>, <, >=, <=, ==, !=).
    Priority: higher than AND, lower than additive.
    Left-associative.
    """
    # Parse left operand (higher priority: additive)
    left = _parse_additive(parser_state)
    
    # Check if there's an error from _parse_additive
    if parser_state.get("error"):
        return left
    
    # Loop for left-associative comparison operators
    while _is_comparison_operator(parser_state):
        token = _current_token(parser_state)
        op = token["value"]
        line = token["line"]
        column = token["column"]
        
        # Advance past the operator
        _advance(parser_state)
        
        # Parse right operand
        right = _parse_additive(parser_state)
        
        # Check if right operand parsing failed
        if parser_state.get("error"):
            return {"type": "ERROR", "line": line, "column": column}
        
        # Build binary op node
        left = {
            "type": "BINARY_OP",
            "operator": op,
            "left": left,
            "right": right,
            "line": line,
            "column": column
        }
    
    return left

# === helper functions ===
def _current_token(parser_state: ParserState) -> Token:
    """Get current token without advancing."""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    if pos < len(tokens):
        return tokens[pos]
    # Return EOF token
    return {"type": "EOF", "value": "", "line": 0, "column": 0}

def _advance(parser_state: ParserState) -> Token:
    """Advance position and return the token that was at current position."""
    token = _current_token(parser_state)
    parser_state["pos"] = parser_state["pos"] + 1
    return token

def _is_comparison_operator(parser_state: ParserState) -> bool:
    """Check if current token is a comparison operator."""
    token = _current_token(parser_state)
    return token["type"] in ("GT", "LT", "GE", "LE", "EQ", "NE")

# === OOP compatibility layer ===

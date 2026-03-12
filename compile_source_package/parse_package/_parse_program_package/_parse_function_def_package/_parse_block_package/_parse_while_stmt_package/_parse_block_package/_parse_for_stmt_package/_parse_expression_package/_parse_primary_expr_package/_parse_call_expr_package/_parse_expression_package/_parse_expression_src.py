# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_call_expr_package._parse_call_expr_src import _parse_call_expr

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,        # e.g., "NUMBER", "STRING", "IDENTIFIER", "LPAREN", "PLUS", etc.
#   "value": str,       # token value string
#   "line": int,        # source line number
#   "column": int       # source column number
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,        # node type: "LITERAL", "IDENT", "CALL", "BINOP", "ERROR"
#   "value": Any,       # node value (literal value, identifier name, operator, function name)
#   "line": int,        # source line number
#   "column": int,      # source column number
#   "children": list    # child AST nodes (for CALL: args; for BINOP: [left, right])
# }

ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,     # list of Token
#   "pos": int,         # current position in tokens
#   "filename": str,    # source filename
#   "error": str        # error message if any
# }

# === main function ===
def _parse_expression(parser_state: ParserState) -> AST:
    """Parse a single expression and return its AST node."""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        parser_state["error"] = "Unexpected end of input while parsing expression"
        return {"type": "ERROR", "value": "Unexpected EOF", "line": 0, "column": 0, "children": []}
    
    token = tokens[pos]
    primary = _parse_primary(parser_state)
    
    if parser_state.get("error"):
        return primary
    
    return _parse_binary_op(parser_state, primary, 0)

# === helper functions ===
def _parse_primary(parser_state: ParserState) -> AST:
    """Parse primary expression: literal, identifier, call, or parenthesized expression."""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    token = tokens[pos]
    ttype = token["type"]
    
    if ttype == "NUMBER" or ttype == "STRING":
        parser_state["pos"] += 1
        return {"type": "LITERAL", "value": token["value"], "line": token["line"], "column": token["column"], "children": []}
    
    if ttype == "IDENTIFIER":
        parser_state["pos"] += 1
        if pos + 1 < len(tokens) and tokens[pos]["type"] == "LPAREN":
            return _parse_call_expr(parser_state, token)
        return {"type": "IDENT", "value": token["value"], "line": token["line"], "column": token["column"], "children": []}
    
    if ttype == "LPAREN":
        parser_state["pos"] += 1
        expr = _parse_expression(parser_state)
        if parser_state.get("error"):
            return expr
        if parser_state["pos"] >= len(tokens) or tokens[parser_state["pos"]]["type"] != "RPAREN":
            parser_state["error"] = "Expected ')' after expression"
            return {"type": "ERROR", "value": "Missing ')'", "line": token["line"], "column": token["column"], "children": [expr]}
        parser_state["pos"] += 1
        return expr
    
    parser_state["error"] = f"Unexpected token '{token['value']}' of type {ttype}"
    return {"type": "ERROR", "value": "Unexpected token", "line": token["line"], "column": token["column"], "children": []}

def _get_precedence(op_type: str) -> int:
    """Return operator precedence level (higher = tighter binding)."""
    if op_type in ("PLUS", "MINUS"):
        return 2
    if op_type in ("STAR", "SLASH"):
        return 3
    if op_type in ("EQ", "NEQ", "LT", "GT", "LTE", "GTE"):
        return 1
    return 0

def _parse_binary_op(parser_state: ParserState, left: AST, min_prec: int) -> AST:
    """Parse binary operators with precedence climbing."""
    tokens = parser_state["tokens"]
    
    while parser_state["pos"] < len(tokens):
        op_token = tokens[parser_state["pos"]]
        prec = _get_precedence(op_token["type"])
        if prec < min_prec:
            break
        
        parser_state["pos"] += 1
        right = _parse_primary(parser_state)
        if parser_state.get("error"):
            return right
        
        while parser_state["pos"] < len(tokens):
            next_op = tokens[parser_state["pos"]]
            next_prec = _get_precedence(next_op["type"])
            if next_prec <= prec:
                break
            right = _parse_binary_op(parser_state, right, next_prec)
            if parser_state.get("error"):
                return right
        
        left = {"type": "BINOP", "value": op_token["value"], "line": op_token["line"], "column": op_token["column"], "children": [left, right]}
    
    return left

# === OOP compatibility layer ===
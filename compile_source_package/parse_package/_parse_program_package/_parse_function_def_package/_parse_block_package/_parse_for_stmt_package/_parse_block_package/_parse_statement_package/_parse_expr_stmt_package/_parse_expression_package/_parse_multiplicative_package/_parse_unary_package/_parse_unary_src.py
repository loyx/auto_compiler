# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_atom_package._parse_atom_src import _parse_atom
from ._parse_expression_package._parse_expression_src import _parse_expression

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

PREFIX_OPERATORS = {"+", "-", "!", "~", "not"}

# === main function ===
def _parse_unary(parser_state: ParserState) -> AST:
    """解析一元表达式（前缀运算符、括号、原子值）。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        raise SyntaxError(f"Unexpected end of input at {parser_state.get('filename', 'unknown')}")
    
    token = tokens[pos]
    token_type = token.get("type", "")
    token_value = token.get("value", "")
    line = token.get("line", 0)
    column = token.get("column", 0)
    
    # Case 1: Prefix operator
    if token_type == "OPERATOR" and token_value in PREFIX_OPERATORS:
        parser_state["pos"] += 1
        operand = _parse_unary(parser_state)
        return {
            "type": "UNARY_OP",
            "children": [operand],
            "value": token_value,
            "line": line,
            "column": column
        }
    
    # Case 2: Left parenthesis
    if token_type == "PAREN" and token_value == "(":
        parser_state["pos"] += 1
        expr = _parse_expression(parser_state)
        
        if parser_state["pos"] >= len(tokens):
            raise SyntaxError(f"Unclosed parenthesis at line {line}")
        
        close_token = tokens[parser_state["pos"]]
        if not (close_token.get("type") == "PAREN" and close_token.get("value") == ")"):
            raise SyntaxError(f"Expected ')' but got '{close_token.get('value')}' at line {close_token.get('line')}")
        
        parser_state["pos"] += 1
        return expr
    
    # Case 3: Atomic value
    return _parse_atom(parser_state)

# === helper functions ===
# No helper functions needed - logic delegated to sub-functions

# === OOP compatibility layer ===
# Not needed for parser function node
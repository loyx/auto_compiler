# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ..._parse_expression_package._parse_expression_src import _parse_expression

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,             # token type (uppercase string)
#   "value": str,            # token value
#   "line": int,             # line number
#   "column": int            # column number
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # node type (IDENTIFIER, LITERAL, GROUPING, ERROR)
#   "children": list,        # child nodes (for GROUPING)
#   "value": Any,            # node value (Python native types)
#   "line": int,             # line number
#   "column": int            # column number
# }

ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,          # list of Token
#   "pos": int,              # current position in tokens
#   "filename": str,         # source filename
#   "error": str             # error message (optional)
# }

# === main function ===
def _parse_primary(parser_state: dict) -> dict:
    """Parse primary expressions (identifiers, literals, parenthesized expressions)."""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # Boundary check
    if pos >= len(tokens):
        current_line = tokens[-1].get("line", 0) if tokens else 0
        current_column = tokens[-1].get("column", 0) if tokens else 0
        parser_state["error"] = f"Unexpected end of input at line {current_line}"
        return {"type": "ERROR", "value": "unexpected_eof", "line": current_line, "column": current_column}
    
    current_token = tokens[pos]
    token_type = current_token.get("type", "")
    token_value = current_token.get("value", "")
    token_line = current_token.get("line", 0)
    token_column = current_token.get("column", 0)
    
    # Identifier
    if token_type == "IDENTIFIER":
        parser_state["pos"] = pos + 1
        return {"type": "IDENTIFIER", "value": token_value, "line": token_line, "column": token_column}
    
    # Number literal
    if token_type == "NUMBER":
        parser_state["pos"] = pos + 1
        parsed_value = float(token_value) if '.' in token_value else int(token_value)
        return {"type": "LITERAL", "value": parsed_value, "line": token_line, "column": token_column}
    
    # String literal
    if token_type == "STRING":
        parser_state["pos"] = pos + 1
        return {"type": "LITERAL", "value": token_value, "line": token_line, "column": token_column}
    
    # Boolean true
    if token_type == "TRUE":
        parser_state["pos"] = pos + 1
        return {"type": "LITERAL", "value": True, "line": token_line, "column": token_column}
    
    # Boolean false
    if token_type == "FALSE":
        parser_state["pos"] = pos + 1
        return {"type": "LITERAL", "value": False, "line": token_line, "column": token_column}
    
    # Nil (null)
    if token_type == "NIL":
        parser_state["pos"] = pos + 1
        return {"type": "LITERAL", "value": None, "line": token_line, "column": token_column}
    
    # Parenthesized expression: '(' expression ')'
    if token_type == "LEFT_PAREN":
        parser_state["pos"] = pos + 1  # consume left paren
        inner_expr = _parse_expression(parser_state)
        
        # Check and consume right paren
        new_pos = parser_state["pos"]
        if new_pos >= len(tokens) or tokens[new_pos].get("type") != "RIGHT_PAREN":
            parser_state["error"] = f"Expected ')' after expression at line {token_line}"
            return {"type": "ERROR", "value": "missing_right_paren", "line": token_line, "column": token_column}
        
        parser_state["pos"] = new_pos + 1  # consume right paren
        return {"type": "GROUPING", "children": [inner_expr], "line": token_line, "column": token_column}
    
    # Unexpected token
    parser_state["error"] = f"Unexpected token '{token_value}' at line {token_line}, column {token_column}"
    return {"type": "ERROR", "value": "unexpected_token", "line": token_line, "column": token_column}

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_function_call_package._parse_function_call_src import _parse_function_call

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
def _parse_expression(parser_state: ParserState) -> AST:
    """Parse a single expression from token stream and return AST node."""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        raise SyntaxError(f"Unexpected end of input in {parser_state.get('filename', '<unknown>')}")
    
    token = tokens[pos]
    token_type = token["type"]
    token_value = token["value"]
    line = token.get("line", 0)
    column = token.get("column", 0)
    
    # Handle literals (numbers, strings)
    if token_type in ("NUMBER", "STRING"):
        parser_state["pos"] = pos + 1
        return {
            "type": "LITERAL",
            "value": token_value,
            "line": line,
            "column": column,
            "children": []
        }
    
    # Handle identifiers (may be function calls)
    if token_type == "IDENT":
        parser_state["pos"] = pos + 1
        # Check if followed by '(' for function call
        if parser_state["pos"] < len(tokens) and tokens[parser_state["pos"]]["type"] == "LPAREN":
            return _parse_function_call(parser_state, token_value)
        return {
            "type": "IDENT",
            "value": token_value,
            "line": line,
            "column": column,
            "children": []
        }
    
    # Handle parenthesized expressions
    if token_type == "LPAREN":
        parser_state["pos"] = pos + 1
        expr = _parse_expression(parser_state)
        # Expect closing paren
        if parser_state["pos"] >= len(tokens) or tokens[parser_state["pos"]]["type"] != "RPAREN":
            raise SyntaxError(f"Expected ')' at line {line}, column {column}")
        parser_state["pos"] += 1
        return expr
    
    # Handle unary operators
    if token_type in ("MINUS", "NOT"):
        parser_state["pos"] = pos + 1
        operand = _parse_expression(parser_state)
        return {
            "type": "UNARY",
            "value": token_value,
            "line": line,
            "column": column,
            "children": [operand]
        }
    
    # Handle binary operators
    if token_type in ("PLUS", "MINUS", "STAR", "SLASH", "EQ", "NE", "LT", "GT", "LE", "GE", "AND", "OR"):
        parser_state["pos"] = pos + 1
        left = _parse_expression(parser_state)
        right = _parse_expression(parser_state)
        return {
            "type": "BINARY",
            "value": token_value,
            "line": line,
            "column": column,
            "children": [left, right]
        }
    
    raise SyntaxError(f"Unexpected token '{token_value}' at line {line}, column {column}")


# === helper functions ===
def _consume_token(parser_state: ParserState, expected_type: str) -> Token:
    """Consume current token if it matches expected type."""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    if pos >= len(tokens):
        raise SyntaxError(f"Unexpected end of input")
    token = tokens[pos]
    if token["type"] != expected_type:
        raise SyntaxError(f"Expected {expected_type}, got {token['type']}")
    parser_state["pos"] = pos + 1
    return token


# === OOP compatibility layer ===
# Not needed for this parser function node

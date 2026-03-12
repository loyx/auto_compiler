# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
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

# === main function ===
def _parse_list_literal(parser_state: ParserState, lbracket_token: Token) -> AST:
    """Parse list literal: [elem1, elem2, ...]"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    elements = []
    
    # Check for empty list []
    if pos < len(tokens) and tokens[pos]["type"] == "RBRACKET":
        parser_state["pos"] = pos + 1
        return {
            "type": "LIST",
            "value": None,
            "line": lbracket_token["line"],
            "column": lbracket_token["column"],
            "children": elements
        }
    
    # Parse elements
    while pos < len(tokens):
        elem = _parse_expression(parser_state)
        if elem["type"] == "ERROR":
            return elem
        elements.append(elem)
        
        pos = parser_state["pos"]
        if pos >= len(tokens):
            parser_state["error"] = "Unexpected end of input in list literal"
            return _make_error_node(parser_state["error"], lbracket_token["line"], lbracket_token["column"])
        
        next_token = tokens[pos]
        if next_token["type"] == "COMMA":
            parser_state["pos"] = pos + 1
            pos = parser_state["pos"]
        elif next_token["type"] == "RBRACKET":
            parser_state["pos"] = pos + 1
            break
        else:
            parser_state["error"] = f"Expected COMMA or RBRACKET, got {next_token['type']}"
            return _make_error_node(parser_state["error"], next_token["line"], next_token["column"])
    
    return {
        "type": "LIST",
        "value": None,
        "line": lbracket_token["line"],
        "column": lbracket_token["column"],
        "children": elements
    }

# === helper functions ===
def _make_error_node(message: str, line: int, column: int) -> AST:
    """Create an ERROR AST node."""
    return {
        "type": "ERROR",
        "value": message,
        "line": line,
        "column": column,
        "children": []
    }

# === OOP compatibility layer ===

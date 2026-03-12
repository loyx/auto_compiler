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
def _parse_array_literal(parser_state: ParserState) -> AST:
    """Parse array literal starting from LEFT_BRACKET token."""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # Check bounds and get current token
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input, expected '['")
    
    current_token = tokens[pos]
    start_line = current_token["line"]
    start_column = current_token["column"]
    
    # Consume LEFT_BRACKET '['
    if current_token["type"] != "LEFT_BRACKET":
        raise SyntaxError(f"Expected '[', got {current_token['type']}")
    pos += 1
    
    # Parse elements
    children = []
    while pos < len(tokens):
        current_token = tokens[pos]
        
        # Check for RIGHT_BRACKET ']'
        if current_token["type"] == "RIGHT_BRACKET":
            break
        
        # Parse expression element
        element_ast = _parse_expression(parser_state)
        children.append(element_ast)
        
        # Check what comes after the expression
        pos = parser_state["pos"]
        if pos >= len(tokens):
            raise SyntaxError("Unexpected end of input in array literal")
        
        current_token = tokens[pos]
        
        # Handle comma or closing bracket
        if current_token["type"] == "COMMA":
            pos += 1
            parser_state["pos"] = pos
        elif current_token["type"] == "RIGHT_BRACKET":
            break
        else:
            raise SyntaxError(f"Expected ',' or ']', got {current_token['type']}")
    
    # Consume RIGHT_BRACKET ']'
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input, expected ']'")
    
    if tokens[pos]["type"] != "RIGHT_BRACKET":
        raise SyntaxError(f"Expected ']', got {tokens[pos]['type']}")
    pos += 1
    parser_state["pos"] = pos
    
    # Return AST node
    return {
        "type": "ArrayLiteral",
        "children": children,
        "value": None,
        "line": start_line,
        "column": start_column
    }

# === helper functions ===

# === OOP compatibility layer ===

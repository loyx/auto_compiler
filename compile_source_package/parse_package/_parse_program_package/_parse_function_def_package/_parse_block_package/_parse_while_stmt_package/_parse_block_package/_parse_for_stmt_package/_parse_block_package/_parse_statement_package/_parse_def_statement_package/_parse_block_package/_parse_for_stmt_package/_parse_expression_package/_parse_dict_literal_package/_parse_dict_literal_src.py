# === std / third-party imports ===
from typing import Dict, Any

# === sub function imports ===
from ._parse_primary_package._parse_primary_src import _parse_primary
from ._parse_expression_package._parse_expression_src import _parse_expression

# === ADT defines ===
ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,
#   "pos": int,
#   "filename": str,
#   "error": str
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

Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,
#   "value": str,
#   "line": int,
#   "column": int
# }

# === main function ===
def _parse_dict_literal(parser_state: ParserState) -> AST:
    """Parse dictionary literal syntax: {key: value, ...}"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # Current token must be LBRACE
    if pos >= len(tokens):
        raise SyntaxError(f"Unexpected end of input, expected '{{' in {parser_state['filename']}")
    
    lbrace_token = tokens[pos]
    if lbrace_token["type"] != "LBRACE":
        raise SyntaxError(f"Expected '{{' but got {lbrace_token['type']} in {parser_state['filename']}")
    
    # Record position info from LBRACE
    line = lbrace_token["line"]
    column = lbrace_token["column"]
    
    # Consume LBRACE
    parser_state["pos"] = pos + 1
    pos = parser_state["pos"]
    
    pairs = []
    
    # Check for empty dictionary
    if pos < len(tokens) and tokens[pos]["type"] == "RBRACE":
        # Empty dict: {}
        parser_state["pos"] = pos + 1
        return {
            "type": "DictLiteral",
            "pairs": [],
            "line": line,
            "column": column
        }
    
    # Parse key-value pairs
    while True:
        # Parse key (must be primary expression: identifier or string)
        key_ast = _parse_primary(parser_state)
        pos = parser_state["pos"]
        
        # Expect COLON
        if pos >= len(tokens):
            raise SyntaxError(f"Unexpected end of input, expected ':' in {parser_state['filename']}")
        
        colon_token = tokens[pos]
        if colon_token["type"] != "COLON":
            raise SyntaxError(f"Expected ':' after key in {parser_state['filename']}")
        
        # Consume COLON
        parser_state["pos"] = pos + 1
        pos = parser_state["pos"]
        
        # Parse value (any expression)
        value_ast = _parse_expression(parser_state)
        pos = parser_state["pos"]
        
        # Add key-value pair
        pairs.append({
            "key": key_ast,
            "value": value_ast
        })
        
        # Check for COMMA or RBRACE
        if pos >= len(tokens):
            raise SyntaxError(f"Unexpected end of input, expected ',' or '}}' in {parser_state['filename']}")
        
        current_token = tokens[pos]
        
        if current_token["type"] == "RBRACE":
            # End of dictionary
            parser_state["pos"] = pos + 1
            break
        elif current_token["type"] == "COMMA":
            # Consume COMMA and continue
            parser_state["pos"] = pos + 1
            pos = parser_state["pos"]
            
            # After comma, check if we have RBRACE (trailing comma case)
            if pos < len(tokens) and tokens[pos]["type"] == "RBRACE":
                parser_state["pos"] = pos + 1
                break
        else:
            raise SyntaxError(f"Expected ',' or '}}' after value in {parser_state['filename']}")
    
    return {
        "type": "DictLiteral",
        "pairs": pairs,
        "line": line,
        "column": column
    }

# === helper functions ===

# === OOP compatibility layer ===

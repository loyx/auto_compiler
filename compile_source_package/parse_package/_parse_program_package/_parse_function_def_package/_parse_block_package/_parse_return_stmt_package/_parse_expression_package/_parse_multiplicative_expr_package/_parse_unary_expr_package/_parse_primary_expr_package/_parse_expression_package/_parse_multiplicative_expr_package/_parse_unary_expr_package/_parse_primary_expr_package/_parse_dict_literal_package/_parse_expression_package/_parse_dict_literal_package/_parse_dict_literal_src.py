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
#   "column": int,
#   "key": AST,
#   "value": AST
# }

ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,
#   "filename": str,
#   "pos": int,
#   "error": str
# }

# === main function ===
def _parse_dict_literal(parser_state: ParserState) -> AST:
    """Parse dictionary literal syntax."""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # Check and consume LEFT_BRACE
    if pos >= len(tokens) or tokens[pos]["type"] != "LEFT_BRACE":
        raise SyntaxError(f"Expected '{{' at line {parser_state.get('filename', 'unknown')}")
    
    left_brace = tokens[pos]
    parser_state["pos"] += 1
    pos = parser_state["pos"]
    
    # Initialize dictionary AST node
    dict_node: AST = {
        "type": "DICT_LITERAL",
        "children": [],
        "line": left_brace["line"],
        "column": left_brace["column"]
    }
    
    # Parse key-value pairs
    while pos < len(tokens):
        token = tokens[pos]
        
        # Check for RIGHT_BRACE (empty dict or end of dict)
        if token["type"] == "RIGHT_BRACE":
            parser_state["pos"] += 1
            return dict_node
        
        # Parse key expression
        key_node = _parse_expression(parser_state)
        pos = parser_state["pos"]
        
        # Check and consume COLON
        if pos >= len(tokens) or tokens[pos]["type"] != "COLON":
            line = key_node.get("line", "unknown")
            column = key_node.get("column", "unknown")
            filename = parser_state.get("filename", "unknown")
            raise SyntaxError(f"Expected ':' after dictionary key at line {line}, column {column} in {filename}")
        
        parser_state["pos"] += 1
        pos = parser_state["pos"]
        
        # Parse value expression
        value_node = _parse_expression(parser_state)
        pos = parser_state["pos"]
        
        # Create key-value pair node
        kv_pair: AST = {
            "type": "KEY_VALUE_PAIR",
            "key": key_node,
            "value": value_node,
            "line": key_node.get("line", 0),
            "column": key_node.get("column", 0)
        }
        dict_node["children"].append(kv_pair)
        
        # Check for COMMA or RIGHT_BRACE
        if pos >= len(tokens):
            filename = parser_state.get("filename", "unknown")
            raise SyntaxError(f"Expected '}}' to close dictionary at line {left_brace['line']}, column {left_brace['column']} in {filename}")
        
        token = tokens[pos]
        if token["type"] == "COMMA":
            parser_state["pos"] += 1
            pos = parser_state["pos"]
            
            # Support trailing comma: check if next is RIGHT_BRACE
            if pos < len(tokens) and tokens[pos]["type"] == "RIGHT_BRACE":
                parser_state["pos"] += 1
                return dict_node
        elif token["type"] == "RIGHT_BRACE":
            parser_state["pos"] += 1
            return dict_node
        else:
            # Unexpected token - should be COMMA or RIGHT_BRACE
            filename = parser_state.get("filename", "unknown")
            raise SyntaxError(f"Expected ',' or '}}' at line {token['line']}, column {token['column']} in {filename}")
    
    # Reached end of tokens without closing brace
    filename = parser_state.get("filename", "unknown")
    raise SyntaxError(f"Expected '}}' to close dictionary at line {left_brace['line']}, column {left_brace['column']} in {filename}")

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for parser function node

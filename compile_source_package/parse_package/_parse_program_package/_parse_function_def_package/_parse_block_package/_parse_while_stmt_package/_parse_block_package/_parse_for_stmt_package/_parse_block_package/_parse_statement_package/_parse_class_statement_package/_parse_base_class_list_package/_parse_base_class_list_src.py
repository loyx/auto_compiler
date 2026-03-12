# === std / third-party imports ===
from typing import Any, Dict, List

# === sub function imports ===
# No sub functions needed for this simple parsing logic

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
def _parse_base_class_list(parser_state: ParserState) -> List[AST]:
    """
    Parse base class list from token stream.
    
    Grammar: IDENT (COMMA IDENT)*
    
    Input: parser_state with pos pointing to first token after LPAREN
    Output: List of base class AST nodes
    Side effect: Updates parser_state["pos"] to position after last consumed token
    """
    base_classes = []
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    while pos < len(tokens):
        token = tokens[pos]
        
        # Expect IDENT token for base class name
        if token["type"] != "IDENT":
            # Stop parsing when encountering non-IDENT token
            # (RPAREN or other token will be handled by caller)
            break
        
        # Create AST node for this base class
        base_node = {
            "type": "BASE",
            "value": token["value"],
            "line": token["line"],
            "column": token["column"]
        }
        base_classes.append(base_node)
        
        # Move past the IDENT token
        pos += 1
        
        # Check for comma
        if pos < len(tokens) and tokens[pos]["type"] == "COMMA":
            # Consume the comma and continue to next IDENT
            pos += 1
        else:
            # No comma, end of base class list
            break
    
    # Update parser state position
    parser_state["pos"] = pos
    
    return base_classes

# === helper functions ===
# No helper functions needed for this simple logic

# === OOP compatibility layer ===
# Not needed for this parser function
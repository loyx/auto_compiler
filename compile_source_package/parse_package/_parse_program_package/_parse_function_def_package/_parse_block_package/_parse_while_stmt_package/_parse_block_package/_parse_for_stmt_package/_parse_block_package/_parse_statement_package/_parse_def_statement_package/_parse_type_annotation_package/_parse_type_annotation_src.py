# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions - inline implementation

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
def _parse_type_annotation(parser_state: ParserState) -> AST:
    """Parse a type annotation from the token stream.
    
    Grammar: type_annotation := IDENT (generic_args)?
    generic_args := LBRACKET type_annotation (COMMA type_annotation)* RBRACKET
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # Check for type name (IDENT)
    if pos >= len(tokens):
        raise SyntaxError("Expected type name")
    
    current_token = tokens[pos]
    if current_token["type"] != "IDENT":
        raise SyntaxError("Expected type name")
    
    type_name = current_token["value"]
    start_line = current_token["line"]
    start_column = current_token["column"]
    pos += 1
    
    # Check for generic arguments
    if pos < len(tokens) and tokens[pos]["type"] == "LBRACKET":
        pos += 1  # consume LBRACKET
        type_args = []
        
        # Parse first type argument
        if pos >= len(tokens):
            raise SyntaxError("Expected ']' after generic arguments")
        
        if tokens[pos]["type"] != "RBRACKET":
            parser_state["pos"] = pos
            type_args.append(_parse_type_annotation(parser_state))
            pos = parser_state["pos"]
            
            # Parse remaining type arguments
            while pos < len(tokens) and tokens[pos]["type"] == "COMMA":
                pos += 1  # consume COMMA
                parser_state["pos"] = pos
                type_args.append(_parse_type_annotation(parser_state))
                pos = parser_state["pos"]
        
        # Expect RBRACKET
        if pos >= len(tokens) or tokens[pos]["type"] != "RBRACKET":
            raise SyntaxError("Expected ']' after generic arguments")
        pos += 1  # consume RBRACKET
        
        # Update parser_state pos before returning
        parser_state["pos"] = pos
        
        # Build GENERIC AST node
        return {
            "type": "GENERIC",
            "line": start_line,
            "column": start_column,
            "children": [
                {"type": "NAME", "value": type_name, "line": start_line, "column": start_column},
                {"type": "TYPE_ARGS", "children": type_args}
            ]
        }
    else:
        # Simple type - no generic arguments
        parser_state["pos"] = pos
        return {
            "type": "NAME",
            "value": type_name,
            "line": start_line,
            "column": start_column
        }

# === helper functions ===
# No helper functions - all logic in main function

# === OOP compatibility layer ===
# Not required - this is a parser helper function

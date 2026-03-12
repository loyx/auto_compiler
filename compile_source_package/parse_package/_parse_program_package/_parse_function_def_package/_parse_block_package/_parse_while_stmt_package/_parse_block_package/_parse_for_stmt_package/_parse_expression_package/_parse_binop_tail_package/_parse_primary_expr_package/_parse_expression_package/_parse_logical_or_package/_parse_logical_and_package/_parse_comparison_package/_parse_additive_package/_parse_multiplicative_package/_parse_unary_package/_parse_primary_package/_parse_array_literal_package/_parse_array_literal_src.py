# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_unary_package._parse_unary_src import _parse_unary

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
#   "operator": str,
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
def _parse_array_literal(parser_state: ParserState, start_line: int, start_column: int) -> AST:
    """Parse array literal from LEFT_BRACKET onwards."""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # Check for empty array: immediate RIGHT_BRACKET
    if pos < len(tokens) and tokens[pos]["type"] == "RIGHT_BRACKET":
        parser_state["pos"] = pos + 1
        return {
            "type": "ARRAY_LITERAL",
            "elements": [],
            "line": start_line,
            "column": start_column
        }
    
    elements = []
    
    while pos < len(tokens):
        # Parse element using _parse_unary
        element = _parse_unary(parser_state)
        
        # Check if parsing failed
        if element["type"] == "ERROR":
            return {
                "type": "ERROR",
                "value": parser_state.get("error", "Array element parse failed"),
                "line": start_line,
                "column": start_column
            }
        
        elements.append(element)
        pos = parser_state["pos"]
        
        # Check what comes after the element
        if pos >= len(tokens):
            parser_state["error"] = "Unexpected end of input in array literal"
            return {
                "type": "ERROR",
                "value": "Unexpected end of input in array literal",
                "line": start_line,
                "column": start_column
            }
        
        current_token = tokens[pos]
        
        if current_token["type"] == "RIGHT_BRACKET":
            # End of array
            parser_state["pos"] = pos + 1
            return {
                "type": "ARRAY_LITERAL",
                "elements": elements,
                "line": start_line,
                "column": start_column
            }
        elif current_token["type"] == "COMMA":
            # Continue to next element
            parser_state["pos"] = pos + 1
            pos = parser_state["pos"]
        else:
            # Invalid token after element
            parser_state["error"] = f"Expected COMMA or RIGHT_BRACKET, got {current_token['type']}"
            return {
                "type": "ERROR",
                "value": f"Expected COMMA or RIGHT_BRACKET, got {current_token['type']}",
                "line": start_line,
                "column": start_column
            }
    
    # Should not reach here, but handle anyway
    parser_state["error"] = "Unexpected end of input in array literal"
    return {
        "type": "ERROR",
        "value": "Unexpected end of input in array literal",
        "line": start_line,
        "column": start_column
    }

# === helper functions ===

# === OOP compatibility layer ===

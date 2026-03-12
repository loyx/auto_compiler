# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# only import child functions
from ._parse_expression_package._parse_expression_src import _parse_expression

# === ADT defines ===
# define the data structures used between parent and child functions
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
def _parse_return_stmt(parser_state: ParserState) -> AST:
    """Parse a return statement. Input parser_state with pos pointing to RETURN token."""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "<unknown>")
    
    # 1. Check current token is RETURN
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}:0:0: Unexpected EOF, expected RETURN")
    
    current_token = tokens[pos]
    if current_token["type"] != "RETURN":
        raise SyntaxError(
            f"{filename}:{current_token['line']}:{current_token['column']}: "
            f"Expected RETURN, got {current_token['type']}"
        )
    
    # Save line/column for AST
    line = current_token["line"]
    column = current_token["column"]
    
    # 2. Consume RETURN token
    parser_state["pos"] = pos + 1
    pos = parser_state["pos"]
    
    # 3. Check next token
    value_node = None
    if pos < len(tokens):
        next_token = tokens[pos]
        if next_token["type"] != "SEMICOLON":
            # Parse expression
            value_node = _parse_expression(parser_state)
            pos = parser_state["pos"]
    
    # 4. Check and consume SEMICOLON
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}:{line}:{column}: Expected SEMICOLON after return")
    
    semi_token = tokens[pos]
    if semi_token["type"] != "SEMICOLON":
        raise SyntaxError(
            f"{filename}:{semi_token['line']}:{semi_token['column']}: "
            f"Expected SEMICOLON, got {semi_token['type']}"
        )
    
    # Consume SEMICOLON
    parser_state["pos"] = pos + 1
    
    # 5. Build AST
    children = []
    if value_node is not None:
        children = [value_node]
    
    return {
        "type": "RETURN_STMT",
        "children": children,
        "value": None,
        "line": line,
        "column": column,
    }

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for parsing function
# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_primary_package._parse_primary_src import _parse_primary
from ._parse_binary_op_package._parse_binary_op_src import _parse_binary_op

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
def _parse_assignment(parser_state: ParserState, left: AST) -> AST:
    """
    Parse assignment expression.
    
    Input: parser_state with pos at ASSIGN token, left AST node (identifier).
    Output: ASSIGNMENT AST node with left and right children.
    Modifies parser_state['pos'] to point after the assigned value.
    Raises SyntaxError on invalid tokens.
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state["filename"]
    
    # Record ASSIGN token position for error reporting
    assign_token = tokens[pos]
    line = assign_token["line"]
    column = assign_token["column"]
    
    # Consume ASSIGN token
    parser_state["pos"] = pos + 1
    
    # Check if there's a valid expression after ASSIGN
    if parser_state["pos"] >= len(tokens):
        raise SyntaxError(f"{filename}:{line}:{column}: Expected expression after '='")
    
    # Parse right-hand side: primary + binary ops
    rhs = _parse_primary(parser_state)
    rhs = _parse_binary_op(parser_state, 0, rhs)
    
    # Build ASSIGNMENT AST node
    return {
        "type": "ASSIGNMENT",
        "children": [left, rhs],
        "line": line,
        "column": column
    }

# === helper functions ===
# No helper functions needed; logic is straightforward.

# === OOP compatibility layer ===
# Not required for this function node (parser utility function).

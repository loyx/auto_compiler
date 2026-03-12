# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_primary_package._parse_primary_src import _parse_primary
from ._parse_binary_op_package._parse_binary_op_src import _parse_binary_op
from ._parse_assignment_package._parse_assignment_src import _parse_assignment
from ._parse_call_args_package._parse_call_args_src import _parse_call_args

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
def _parse_expression(parser_state: dict) -> dict:
    """Parse an expression and return AST node. Modifies parser_state['pos'] in-place."""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "<unknown>")
    
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}:0:0: Unexpected end of input")
    
    token = tokens[pos]
    line, column = token["line"], token["column"]
    
    # Parse left-hand side (primary expression)
    left = _parse_primary(parser_state)
    
    # Check for function call: IDENTIFIER followed by LPAREN
    if left["type"] == "IDENTIFIER" and parser_state["pos"] < len(tokens):
        current = tokens[parser_state["pos"]]
        if current["type"] == "LPAREN":
            parser_state["pos"] += 1  # consume LPAREN
            args = _parse_call_args(parser_state)
            # consume RPAREN if present
            if parser_state["pos"] < len(tokens) and tokens[parser_state["pos"]]["type"] == "RPAREN":
                parser_state["pos"] += 1
            else:
                raise SyntaxError(f"{filename}:{line}:{column}: Expected ')' after function arguments")
            return {
                "type": "CALL",
                "value": left["value"],
                "children": args,
                "line": line,
                "column": column
            }
    
    # Check for assignment (lowest precedence)
    if parser_state["pos"] < len(tokens):
        current = tokens[parser_state["pos"]]
        if current["type"] == "ASSIGN":
            return _parse_assignment(parser_state, left)
    
    # Parse binary operations with precedence climbing
    return _parse_binary_op(parser_state, 0, left)

# === helper functions ===
def _get_precedence(op_type: str) -> int:
    """Return operator precedence level. Higher = binds tighter."""
    precedence_map = {
        "PLUS": 1,
        "MINUS": 1,
        "STAR": 2,
        "SLASH": 2,
    }
    return precedence_map.get(op_type, 0)

# === OOP compatibility layer ===

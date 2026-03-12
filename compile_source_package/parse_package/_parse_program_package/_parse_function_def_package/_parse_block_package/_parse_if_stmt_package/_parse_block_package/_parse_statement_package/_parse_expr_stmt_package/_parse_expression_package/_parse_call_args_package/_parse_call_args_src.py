# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from .._parse_primary_package._parse_primary_src import _parse_primary
from .._parse_binary_op_package._parse_binary_op_src import _parse_binary_op

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
def _parse_call_args(parser_state: dict) -> list:
    """Parse function call arguments inside parentheses."""
    args = []
    tokens = parser_state["tokens"]
    
    # Check for empty argument list: func()
    if parser_state["pos"] < len(tokens) and tokens[parser_state["pos"]]["type"] == "RPAREN":
        return args
    
    # Parse arguments until RPAREN
    while parser_state["pos"] < len(tokens):
        current_token = tokens[parser_state["pos"]]
        
        # Check for end of argument list
        if current_token["type"] == "RPAREN":
            break
        
        # Parse argument expression: primary + binary ops
        arg_expr = _parse_primary(parser_state)
        arg_expr = _parse_binary_op(parser_state, 0, arg_expr)
        args.append(arg_expr)
        
        # Check separator or end
        if parser_state["pos"] >= len(tokens):
            raise SyntaxError("Unexpected end of file while parsing function arguments")
        
        next_token = tokens[parser_state["pos"]]
        if next_token["type"] == "COMMA":
            parser_state["pos"] += 1  # consume comma
        elif next_token["type"] == "RPAREN":
            break  # end of arguments, don't consume RPAREN
        else:
            raise SyntaxError(f"Expected COMMA or RPAREN, got {next_token['type']}")
    
    return args

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for parser sub-function

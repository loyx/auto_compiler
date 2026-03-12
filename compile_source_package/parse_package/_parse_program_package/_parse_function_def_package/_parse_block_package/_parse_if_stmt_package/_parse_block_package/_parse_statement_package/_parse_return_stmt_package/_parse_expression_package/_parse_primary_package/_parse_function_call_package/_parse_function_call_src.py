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
def _parse_function_call(parser_state: ParserState, func_name: str, line: int, column: int) -> AST:
    """Parse function call: function_name(args). Returns CALL AST node."""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # Consume '(' token
    if pos >= len(tokens) or tokens[pos]["value"] != "(":
        raise SyntaxError(f"Expected '(' after function name at line {line}, column {column}")
    pos += 1
    
    args = []
    
    # Check for empty parameter list
    if pos < len(tokens) and tokens[pos]["value"] == ")":
        pos += 1
        parser_state["pos"] = pos
        return {
            "type": "CALL",
            "children": args,
            "value": func_name,
            "line": line,
            "column": column
        }
    
    # Parse first argument
    arg_ast = _parse_expression(parser_state)
    args.append(arg_ast)
    pos = parser_state["pos"]
    
    # Parse remaining arguments
    while pos < len(tokens):
        token = tokens[pos]
        if token["value"] == ")":
            pos += 1
            break
        elif token["value"] == ",":
            pos += 1
            if pos >= len(tokens) or tokens[pos]["value"] == ")":
                raise SyntaxError(f"Expected expression after ',' at line {token['line']}, column {token['column']}")
            arg_ast = _parse_expression(parser_state)
            args.append(arg_ast)
            pos = parser_state["pos"]
        else:
            break
    
    parser_state["pos"] = pos
    
    if pos > len(tokens) or (pos < len(tokens) and tokens[pos - 1]["value"] != ")"):
        raise SyntaxError(f"Expected ')' to close function call at line {line}, column {column}")
    
    return {
        "type": "CALL",
        "children": args,
        "value": func_name,
        "line": line,
        "column": column
    }

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for parser function
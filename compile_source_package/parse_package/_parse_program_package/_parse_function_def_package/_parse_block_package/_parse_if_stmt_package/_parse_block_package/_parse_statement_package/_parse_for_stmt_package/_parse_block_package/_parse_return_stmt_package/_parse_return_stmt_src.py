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
def _parse_return_stmt(parser_state: ParserState) -> AST:
    """Parse RETURN statement and return AST node."""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "<unknown>")
    
    return_token = tokens[pos]
    line = return_token["line"]
    column = return_token["column"]
    
    # Consume RETURN token
    parser_state["pos"] = pos + 1
    
    # Check if next token exists
    if pos + 1 >= len(tokens):
        raise SyntaxError(f"{filename}:{line}:{column}: Expected ';' or expression after 'return'")
    
    next_token = tokens[pos + 1]
    
    # Check if it's a bare return (return;)
    if next_token["type"] == "SEMICOLON":
        parser_state["pos"] = pos + 2
        return {
            "type": "RETURN",
            "value": None,
            "line": line,
            "column": column
        }
    else:
        # Parse expression
        expr_ast = _parse_expression(parser_state)
        
        # Expect SEMICOLON after expression
        if parser_state["pos"] >= len(tokens):
            raise SyntaxError(f"{filename}:{line}:{column}: Expected ';' after return expression")
        
        if tokens[parser_state["pos"]]["type"] != "SEMICOLON":
            raise SyntaxError(f"{filename}:{line}:{column}: Expected ';' after return expression")
        
        parser_state["pos"] += 1
        
        return {
            "type": "RETURN",
            "value": expr_ast,
            "line": line,
            "column": column
        }

# === helper functions ===

# === OOP compatibility layer ===

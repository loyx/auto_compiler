# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_and_package._parse_and_src import _parse_and

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
#   "operator": str,
#   "left": AST,
#   "right": AST,
#   "operand": AST
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
def _parse_or(parser_state: ParserState) -> AST:
    """Parse logical OR (||) expressions."""
    tokens = parser_state["tokens"]
    
    # Parse left operand using _parse_and
    left_ast = _parse_and(parser_state)
    
    # Loop to handle chained || operators
    while parser_state["pos"] < len(tokens):
        current_token = tokens[parser_state["pos"]]
        
        # Check if current token is "||"
        if current_token.get("value") != "||":
            break
        
        # Consume the "||" operator
        op_line = current_token.get("line", 0)
        op_column = current_token.get("column", 0)
        parser_state["pos"] += 1
        
        # Check bounds before parsing right operand
        if parser_state["pos"] >= len(tokens):
            raise SyntaxError(
                f"Unexpected end of input after '||' at line {op_line}, column {op_column}"
            )
        
        # Parse right operand
        right_ast = _parse_and(parser_state)
        
        # Build binary AST node
        left_ast = {
            "type": "BINARY",
            "operator": "||",
            "left": left_ast,
            "right": right_ast,
            "line": op_line,
            "column": op_column
        }
    
    return left_ast

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for parser function
# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_comparison_package._parse_comparison_src import _parse_comparison

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
def _parse_not(parser_state: ParserState) -> AST:
    """
    Parse 'not' unary operator expression (higher precedence than 'and').
    
    If current token is NOT: consume it and recursively parse not expression.
    Otherwise: delegate to _parse_comparison for next precedence level.
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "<unknown>")
    
    # Check if current token is NOT
    if pos < len(tokens) and tokens[pos]["type"] == "NOT":
        not_token = tokens[pos]
        line = not_token["line"]
        column = not_token["column"]
        
        # Consume NOT token
        parser_state["pos"] = pos + 1
        
        # Recursively parse the operand (allows chained 'not not x')
        operand = _parse_not(parser_state)
        
        # Build UNARY_OP AST node
        return {
            "type": "UNARY_OP",
            "operator": "not",
            "children": [operand],
            "line": line,
            "column": column
        }
    else:
        # No NOT token, delegate to next precedence level
        return _parse_comparison(parser_state)

# === helper functions ===
def _raise_syntax_error(filename: str, line: int, column: int, message: str) -> None:
    """Raise SyntaxError with standardized format."""
    raise SyntaxError(f"{filename}:{line}:{column}: {message}")

# === OOP compatibility layer ===
# Not needed for this parser function node

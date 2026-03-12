# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_argument_list_package._parse_argument_list_src import _parse_argument_list

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
#   "value": Any,
#   "line": int,
#   "column": int,
#   "children": list
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
def _parse_call_expr(parser_state: ParserState, identifier_token: Token) -> AST:
    """Parse a function call expression.
    
    Assumes parser_state['pos'] points to LPAREN token.
    Returns CALL AST node with function name and argument children.
    Sets parser_state['error'] on failure.
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # Check for LPAREN
    if pos >= len(tokens) or tokens[pos]["type"] != "LPAREN":
        parser_state["error"] = f"Expected '(' after function name '{identifier_token['value']}'"
        return {
            "type": "ERROR",
            "value": parser_state["error"],
            "line": identifier_token["line"],
            "column": identifier_token["column"],
            "children": []
        }
    
    # Consume LPAREN
    parser_state["pos"] += 1
    
    # Parse argument list
    args = _parse_argument_list(parser_state, identifier_token)
    
    # Check if argument list parsing set an error
    if parser_state["error"]:
        return {
            "type": "ERROR",
            "value": parser_state["error"],
            "line": identifier_token["line"],
            "column": identifier_token["column"],
            "children": []
        }
    
    return {
        "type": "CALL",
        "value": identifier_token["value"],
        "line": identifier_token["line"],
        "column": identifier_token["column"],
        "children": args
    }

# === helper functions ===

# === OOP compatibility layer ===

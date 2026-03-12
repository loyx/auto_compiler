# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions needed for this implementation

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
def _parse_primary(parser_state: ParserState) -> AST:
    """Parse primary expression (literal, identifier, parenthesized expr, function call)."""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        parser_state["error"] = "Unexpected end of input"
        return {"type": "ERROR", "value": None, "line": 0, "column": 0, "children": []}
    
    token = tokens[pos]
    token_type = token["type"]
    
    if token_type in ("INTEGER", "FLOAT", "STRING"):
        parser_state["pos"] = pos + 1
        return {
            "type": "LITERAL",
            "value": token["value"],
            "line": token["line"],
            "column": token["column"],
            "children": []
        }
    
    elif token_type == "IDENTIFIER":
        if pos + 1 < len(tokens) and tokens[pos + 1]["type"] == "LPAREN":
            parser_state["pos"] = pos + 2
            return {
                "type": "CALL",
                "value": token["value"],
                "line": token["line"],
                "column": token["column"],
                "children": []
            }
        else:
            parser_state["pos"] = pos + 1
            return {
                "type": "IDENTIFIER",
                "value": token["value"],
                "line": token["line"],
                "column": token["column"],
                "children": []
            }
    
    elif token_type == "LPAREN":
        parser_state["pos"] = pos + 1
        return {
            "type": "PAREN",
            "value": None,
            "line": token["line"],
            "column": token["column"],
            "children": []
        }
    
    else:
        parser_state["error"] = f"Unexpected token: {token_type}"
        return {
            "type": "ERROR",
            "value": None,
            "line": token["line"],
            "column": token["column"],
            "children": []
        }

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this parsing function

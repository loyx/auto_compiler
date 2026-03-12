# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed for this atom parser

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,        # Token type: "NUMBER", "STRING", "IDENTIFIER", "KEYWORD", etc.
#   "value": str,       # Token value as string
#   "line": int,        # Line number in source
#   "column": int       # Column number in source
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,        # AST node type: "NUMBER_LITERAL", "STRING_LITERAL", etc.
#   "children": list,   # Child nodes (empty for atom literals)
#   "value": Any,       # Literal value (int, float, str, bool, None)
#   "line": int,        # Line number in source
#   "column": int       # Column number in source
# }

ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,     # List of Token dicts
#   "pos": int,         # Current position in tokens list
#   "filename": str,    # Source filename for error messages
#   "error": str        # Error message (if any)
# }

# === main function ===
def _parse_atom(parser_state: ParserState) -> AST:
    """Parse atomic value (number, string, identifier, boolean, null)."""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        raise SyntaxError(f"Unexpected end of input in {parser_state.get('filename', 'unknown')}")
    
    token = tokens[pos]
    token_type = token["type"]
    token_value = token["value"]
    line = token["line"]
    column = token["column"]
    
    # Parse based on token type
    if token_type == "NUMBER":
        # Convert to int or float
        if "." in token_value or "e" in token_value.lower():
            value = float(token_value)
        else:
            value = int(token_value)
        ast_node = {
            "type": "NUMBER_LITERAL",
            "children": [],
            "value": value,
            "line": line,
            "column": column
        }
    elif token_type == "STRING":
        # Remove quotes from string value
        if (token_value.startswith('"') and token_value.endswith('"')) or \
           (token_value.startswith("'") and token_value.endswith("'")):
            value = token_value[1:-1]
        else:
            value = token_value
        ast_node = {
            "type": "STRING_LITERAL",
            "children": [],
            "value": value,
            "line": line,
            "column": column
        }
    elif token_type == "IDENTIFIER":
        ast_node = {
            "type": "IDENTIFIER",
            "children": [],
            "value": token_value,
            "line": line,
            "column": column
        }
    elif token_type == "KEYWORD":
        if token_value.lower() == "true":
            ast_node = {
                "type": "BOOLEAN_LITERAL",
                "children": [],
                "value": True,
                "line": line,
                "column": column
            }
        elif token_value.lower() == "false":
            ast_node = {
                "type": "BOOLEAN_LITERAL",
                "children": [],
                "value": False,
                "line": line,
                "column": column
            }
        elif token_value.lower() in ("null", "none"):
            ast_node = {
                "type": "NULL_LITERAL",
                "children": [],
                "value": None,
                "line": line,
                "column": column
            }
        else:
            raise SyntaxError(f"Invalid keyword as atom: {token_value} at {line}:{column}")
    else:
        raise SyntaxError(f"Invalid atom token type: {token_type} at {line}:{column}")
    
    # Advance position
    parser_state["pos"] = pos + 1
    
    return ast_node

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for parser helper function

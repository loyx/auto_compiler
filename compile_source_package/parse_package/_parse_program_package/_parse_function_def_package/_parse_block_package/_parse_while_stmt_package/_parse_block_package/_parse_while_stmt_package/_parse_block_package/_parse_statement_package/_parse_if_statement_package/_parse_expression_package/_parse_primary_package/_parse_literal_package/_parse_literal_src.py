# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions needed

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
#   "name": str,
#   "callee": AST,
#   "arguments": list,
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
def _parse_literal(parser_state: ParserState, token: Token) -> AST:
    """
    Parse literal token (NUMBER, STRING, BOOLEAN) and return AST node.
    
    Args:
        parser_state: Parser state dictionary, current pos points to literal token
        token: Current literal token with type NUMBER/STRING/BOOLEAN
    
    Returns:
        AST node with type, value, line, and column fields
    
    Side effects:
        Advances parser_state["pos"] by 1
    
    Raises:
        ValueError: On unexpected token type
    """
    token_type = token["type"]
    line = token["line"]
    column = token["column"]
    value_str = token["value"]
    
    # Consume the token
    parser_state["pos"] += 1
    
    if token_type == "NUMBER":
        # Try to convert to int or float
        try:
            if "." in value_str:
                value = float(value_str)
            else:
                value = int(value_str)
        except ValueError:
            # On conversion failure, keep original string
            value = value_str
        
        return {
            "type": "NUMBER",
            "value": value,
            "line": line,
            "column": column
        }
    
    elif token_type == "STRING":
        # Remove surrounding quotes (double or single)
        if (value_str.startswith('"') and value_str.endswith('"')) or \
           (value_str.startswith("'") and value_str.endswith("'")):
            value = value_str[1:-1]
        else:
            value = value_str
        
        return {
            "type": "STRING",
            "value": value,
            "line": line,
            "column": column
        }
    
    elif token_type == "BOOLEAN":
        # Convert to bool (case-insensitive)
        value = value_str.lower() == "true"
        
        return {
            "type": "BOOLEAN",
            "value": value,
            "line": line,
            "column": column
        }
    
    else:
        # Should not reach here based on contract
        raise ValueError(f"Unexpected token type: {token_type}")

# === helper functions ===
# No helper functions needed for this simple logic

# === OOP compatibility layer ===
# Not needed for this helper function

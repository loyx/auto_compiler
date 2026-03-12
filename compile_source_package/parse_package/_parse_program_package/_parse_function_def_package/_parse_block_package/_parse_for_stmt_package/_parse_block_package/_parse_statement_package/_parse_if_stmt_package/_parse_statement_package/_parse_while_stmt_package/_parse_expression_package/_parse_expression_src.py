# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions - inline implementation

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
#   "value": str,
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
def _parse_expression(parser_state: ParserState) -> AST:
    """
    Parse an expression from the current token position.
    Handles: identifiers, literals (number/string), binary operations, parenthesized expressions.
    Updates parser_state['pos'] as tokens are consumed.
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of expression")
    
    token = tokens[pos]
    token_type = token.get("type", "")
    
    # Parse based on token type
    if token_type == "NUMBER":
        parser_state["pos"] = pos + 1
        return {
            "type": "NUMBER",
            "value": token["value"],
            "line": token.get("line", 0),
            "column": token.get("column", 0)
        }
    
    elif token_type == "STRING":
        parser_state["pos"] = pos + 1
        return {
            "type": "STRING",
            "value": token["value"],
            "line": token.get("line", 0),
            "column": token.get("column", 0)
        }
    
    elif token_type == "IDENT":
        parser_state["pos"] = pos + 1
        return {
            "type": "IDENT",
            "value": token["value"],
            "line": token.get("line", 0),
            "column": token.get("column", 0)
        }
    
    elif token_type == "LPAREN":
        # Parenthesized expression: ( expr )
        parser_state["pos"] = pos + 1
        inner_expr = _parse_expression(parser_state)
        
        # Expect RPAREN
        new_pos = parser_state["pos"]
        if new_pos >= len(tokens) or tokens[new_pos].get("type") != "RPAREN":
            raise SyntaxError("Expected closing parenthesis")
        parser_state["pos"] = new_pos + 1
        
        return {
            "type": "PAREN_EXPR",
            "children": [inner_expr],
            "line": token.get("line", 0),
            "column": token.get("column", 0)
        }
    
    elif token_type == "MINUS":
        # Unary minus: -expr
        parser_state["pos"] = pos + 1
        operand = _parse_expression(parser_state)
        return {
            "type": "UNARY_MINUS",
            "children": [operand],
            "line": token.get("line", 0),
            "column": token.get("column", 0)
        }
    
    else:
        raise SyntaxError(f"Unexpected token in expression: {token_type}")

# === helper functions ===
# No helper functions needed - logic is inline

# === OOP compatibility layer ===
# Not needed - this is a helper parser function, not a framework entry point

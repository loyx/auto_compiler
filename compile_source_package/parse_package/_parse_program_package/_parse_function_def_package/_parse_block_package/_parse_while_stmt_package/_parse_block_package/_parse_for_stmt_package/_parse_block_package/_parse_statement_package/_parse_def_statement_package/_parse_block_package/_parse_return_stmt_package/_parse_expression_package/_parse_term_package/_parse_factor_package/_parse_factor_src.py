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
def _parse_factor(parser_state: ParserState) -> AST:
    """
    Parse a factor from the token stream.
    
    Factor grammar:
        factor := IDENTIFIER | NUMBER | LPAREN expression RPAREN
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # Check for end of input
    if pos >= len(tokens):
        raise SyntaxError(f"Expected factor, got end of input")
    
    token = tokens[pos]
    token_type = token["type"]
    
    # Case 1: IDENTIFIER
    if token_type == "IDENTIFIER":
        parser_state["pos"] = pos + 1
        return {
            "type": "IDENTIFIER",
            "value": token["value"],
            "line": token["line"],
            "column": token["column"]
        }
    
    # Case 2: NUMBER
    elif token_type == "NUMBER":
        parser_state["pos"] = pos + 1
        return {
            "type": "NUMBER",
            "value": token["value"],
            "line": token["line"],
            "column": token["column"]
        }
    
    # Case 3: LPAREN (parenthesized expression)
    elif token_type == "LPAREN":
        parser_state["pos"] = pos + 1
        expr_ast = _parse_expression(parser_state)
        
        # Expect RPAREN
        pos = parser_state["pos"]
        if pos >= len(tokens):
            raise SyntaxError(f"Expected RPAREN, got end of input at line {token['line']}, column {token['column']}")
        
        next_token = tokens[pos]
        if next_token["type"] != "RPAREN":
            raise SyntaxError(f"Expected RPAREN, got {next_token['type']} at line {next_token['line']}, column {next_token['column']}")
        
        parser_state["pos"] = pos + 1
        return {
            "type": "GROUP",
            "children": [expr_ast],
            "line": token["line"],
            "column": token["column"]
        }
    
    # Invalid token type
    else:
        raise SyntaxError(f"Expected factor, got {token_type} at line {token['line']}, column {token['column']}")

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for internal parser function

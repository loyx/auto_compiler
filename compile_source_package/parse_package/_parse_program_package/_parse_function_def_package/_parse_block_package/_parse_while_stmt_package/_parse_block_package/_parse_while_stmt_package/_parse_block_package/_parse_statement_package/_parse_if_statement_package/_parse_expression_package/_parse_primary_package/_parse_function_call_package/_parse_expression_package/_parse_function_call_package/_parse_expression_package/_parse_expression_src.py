# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_function_call_package._parse_function_call_src import _parse_function_call

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
#   "filename": str,
#   "pos": int,
#   "error": str
# }


# === main function ===
def _parse_expression(parser_state: ParserState) -> AST:
    """Parse a single expression and return AST node."""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # Check bounds
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input while parsing expression")
    
    token = tokens[pos]
    token_type = token["type"]
    
    # Dispatch based on token type
    if token_type == "NUMBER":
        parser_state["pos"] += 1
        return {
            "type": "NUMBER",
            "value": token["value"],
            "line": token["line"],
            "column": token["column"]
        }
    
    elif token_type == "STRING":
        parser_state["pos"] += 1
        return {
            "type": "STRING",
            "value": token["value"],
            "line": token["line"],
            "column": token["column"]
        }
    
    elif token_type == "IDENTIFIER":
        parser_state["pos"] += 1
        # Check if next token is LPAREN (function call)
        next_pos = parser_state["pos"]
        if next_pos < len(tokens) and tokens[next_pos]["type"] == "LPAREN":
            return _parse_function_call(parser_state, token["value"])
        else:
            return {
                "type": "IDENTIFIER",
                "name": token["value"],
                "line": token["line"],
                "column": token["column"]
            }
    
    elif token_type == "LPAREN":
        parser_state["pos"] += 1
        # Parse inner expression
        inner_ast = _parse_expression(parser_state)
        # Expect RPAREN
        if parser_state["pos"] >= len(tokens):
            raise SyntaxError("Unexpected end of input, expected ')'")
        if tokens[parser_state["pos"]]["type"] != "RPAREN":
            raise SyntaxError(f"Expected ')' but got {tokens[parser_state['pos']]['type']}")
        parser_state["pos"] += 1
        return inner_ast
    
    else:
        raise SyntaxError(f"Unexpected token type '{token_type}' while parsing expression")


# === helper functions ===
# No helper functions needed - logic delegated to sub-functions

# === OOP compatibility layer ===
# Not needed - this is a parser utility function

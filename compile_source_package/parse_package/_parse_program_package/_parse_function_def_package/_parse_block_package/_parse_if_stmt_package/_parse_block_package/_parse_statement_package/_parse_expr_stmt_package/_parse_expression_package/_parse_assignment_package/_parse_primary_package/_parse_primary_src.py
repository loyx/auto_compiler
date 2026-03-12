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
def _parse_primary(parser_state: ParserState) -> AST:
    """
    Parse primary expressions (literals, identifiers, parenthesized expressions).
    Input: parser_state with pos at start of primary.
    Output: AST node for the primary.
    Raises SyntaxError on invalid tokens.
    Modifies parser_state['pos'] to point after the consumed token.
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "<unknown>")
    
    # Check for end of input
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}:0:0: Unexpected end of input while parsing primary expression")
    
    token = tokens[pos]
    token_type = token["type"]
    token_value = token["value"]
    line = token["line"]
    column = token["column"]
    
    if token_type == "IDENTIFIER":
        parser_state["pos"] = pos + 1
        return {
            "type": "IDENTIFIER",
            "value": token_value,
            "line": line,
            "column": column
        }
    
    elif token_type == "NUMBER":
        parser_state["pos"] = pos + 1
        return {
            "type": "NUMBER",
            "value": token_value,
            "line": line,
            "column": column
        }
    
    elif token_type == "STRING":
        parser_state["pos"] = pos + 1
        return {
            "type": "STRING",
            "value": token_value,
            "line": line,
            "column": column
        }
    
    elif token_type == "LPAREN":
        # Consume LPAREN
        parser_state["pos"] = pos + 1
        
        # Parse inner expression
        inner_ast = _parse_expression(parser_state)
        
        # Expect and consume RPAREN
        new_pos = parser_state["pos"]
        if new_pos >= len(tokens):
            raise SyntaxError(f"{filename}:{line}:{column}: Expected ')' but found end of input")
        
        next_token = tokens[new_pos]
        if next_token["type"] != "RPAREN":
            raise SyntaxError(
                f"{filename}:{next_token['line']}:{next_token['column']}: "
                f"Expected ')' but found '{next_token['value']}'"
            )
        
        parser_state["pos"] = new_pos + 1
        return inner_ast
    
    else:
        raise SyntaxError(
            f"{filename}:{line}:{column}: Unexpected token '{token_value}' of type '{token_type}'"
        )

# === helper functions ===
# No helper functions needed for this simple parsing logic

# === OOP compatibility layer ===
# Not needed for parser function nodes
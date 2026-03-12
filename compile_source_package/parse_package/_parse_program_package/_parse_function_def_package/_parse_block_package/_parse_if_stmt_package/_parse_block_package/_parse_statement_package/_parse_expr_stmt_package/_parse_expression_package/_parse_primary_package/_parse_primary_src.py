# === std / third-party imports ===
from typing import Any, Dict, Callable, Optional

# === sub function imports ===
# No child functions; _parse_expression is passed as callback parameter

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
def _parse_primary(parser_state: ParserState, expression_parser: Optional[Callable[[ParserState], AST]] = None) -> AST:
    """
    Parse primary expressions (literals, identifiers, parenthesized expressions).
    Input: parser_state with pos at primary expression start.
    Output: AST node for the primary expression.
    Modifies parser_state['pos'] to point after the primary expression.
    Raises SyntaxError on invalid tokens.
    """
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state.get("filename", "<unknown>")
    
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}:0:0: Unexpected end of input")
    
    token = tokens[pos]
    token_type = token["type"]
    token_value = token["value"]
    line = token["line"]
    column = token["column"]
    
    if token_type == "NUMBER":
        # Convert to Python numeric value (int or float)
        try:
            if "." in token_value:
                numeric_value = float(token_value)
            else:
                numeric_value = int(token_value)
        except ValueError:
            raise SyntaxError(f"{filename}:{line}:{column}: Invalid number '{token_value}'")
        parser_state["pos"] += 1
        return {
            "type": "LITERAL",
            "value": numeric_value,
            "line": line,
            "column": column
        }
    
    elif token_type == "STRING":
        # Remove quotes from string literal
        if len(token_value) >= 2 and token_value[0] in ('"', "'") and token_value[-1] == token_value[0]:
            string_value = token_value[1:-1]
        else:
            raise SyntaxError(f"{filename}:{line}:{column}: Invalid string literal '{token_value}'")
        parser_state["pos"] += 1
        return {
            "type": "LITERAL",
            "value": string_value,
            "line": line,
            "column": column
        }
    
    elif token_type == "IDENTIFIER":
        parser_state["pos"] += 1
        return {
            "type": "IDENTIFIER",
            "value": token_value,
            "line": line,
            "column": column
        }
    
    elif token_type == "LPAREN":
        if expression_parser is None:
            raise SyntaxError(f"{filename}:{line}:{column}: Internal error: expression_parser not provided for parenthesized expression")
        parser_state["pos"] += 1  # consume LPAREN
        inner_expr = expression_parser(parser_state)
        
        # Check and consume RPAREN
        new_pos = parser_state["pos"]
        if new_pos >= len(tokens) or tokens[new_pos]["type"] != "RPAREN":
            raise SyntaxError(f"{filename}:{line}:{column}: Expected ')'")
        parser_state["pos"] += 1  # consume RPAREN
        
        return inner_expr
    
    else:
        raise SyntaxError(f"{filename}:{line}:{column}: Unexpected token '{token_value}'")

# === helper functions ===
# No helper functions needed; logic is self-contained

# === OOP compatibility layer ===
# Not needed; this is a parser helper function, not a framework entry point

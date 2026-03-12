# === std / third-party imports ===
from typing import Any, Dict, List

# === sub function imports ===
from ._parse_function_call_package._parse_function_call_src import _parse_function_call
from ._parse_literal_package._parse_literal_src import _parse_literal

# _parse_expression is in the parent package, imported at module level
from .._parse_expression_src import _parse_expression

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
def _parse_primary(parser_state: ParserState) -> AST:
    """
    Parse primary expression (identifier, literal, parenthesized expr, or function call).
    Input: parser_state at primary token.
    Behavior: consume tokens for primary expr, advance pos.
    Output: AST node for primary.
    Side effect: modifies parser_state['pos'].
    Raises SyntaxError on invalid primary.
    """
    tokens: List[Token] = parser_state["tokens"]
    pos: int = parser_state["pos"]
    
    if pos >= len(tokens):
        raise SyntaxError("Unexpected end of input")
    
    token: Token = tokens[pos]
    token_type: str = token["type"]
    token_value: str = token["value"]
    line: int = token["line"]
    column: int = token["column"]
    
    # Case 1: Identifier (could be variable or function call)
    if token_type == "IDENTIFIER":
        parser_state["pos"] += 1
        identifier_ast: AST = {
            "type": "IDENTIFIER",
            "name": token_value,
            "line": line,
            "column": column
        }
        
        # Check if this is a function call (next token is LPAREN)
        next_pos: int = parser_state["pos"]
        if next_pos < len(tokens) and tokens[next_pos]["type"] == "LPAREN":
            return _parse_function_call(parser_state, identifier_ast, tokens[next_pos])
        else:
            return identifier_ast
    
    # Case 2: Literals (NUMBER, STRING, BOOLEAN)
    elif token_type in ("NUMBER", "STRING", "BOOLEAN"):
        return _parse_literal(parser_state, token)
    
    # Case 3: Parenthesized expression
    elif token_type == "LPAREN":
        parser_state["pos"] += 1  # consume LPAREN
        inner_expr: AST = _parse_expression._parse_expression(parser_state)
        
        # Expect RPAREN
        if parser_state["pos"] >= len(tokens):
            raise SyntaxError(f"Expected ')' to close parenthesis at line {line}, column {column}")
        
        rparen_token: Token = tokens[parser_state["pos"]]
        if rparen_token["type"] != "RPAREN":
            raise SyntaxError(
                f"Expected ')' but got '{rparen_token['value']}' at line {rparen_token['line']}, "
                f"column {rparen_token['column']}"
            )
        
        parser_state["pos"] += 1  # consume RPAREN
        return inner_expr
    
    # Case 4: Invalid token for primary expression
    else:
        raise SyntaxError(
            f"Unexpected token '{token_value}' of type {token_type} at line {line}, column {column}"
        )

# === helper functions ===
# No helper functions - delegated to subfunctions

# === OOP compatibility layer ===
# No OOP wrapper needed - this is a parser helper function

# === std / third-party imports ===
from typing import Any, Dict, List

# === sub function imports ===
from ._parse_expression_package._parse_expression_src import _parse_expression
from ._parse_unary_expr_package._parse_unary_expr_src import _parse_unary_expr
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
    """Parse atomic expression (identifier, literal, unary op, parentheses, function call)."""
    tokens: List[Token] = parser_state["tokens"]
    pos: int = parser_state["pos"]
    filename: str = parser_state.get("filename", "<unknown>")
    
    if pos >= len(tokens):
        raise SyntaxError(f"{filename}:0:0: Unexpected end of input")
    
    token = tokens[pos]
    token_type = token.get("type", "")
    token_value = token.get("value", "")
    line = token.get("line", 0)
    column = token.get("column", 0)
    
    # 1. Unary operators: -, !, ~
    if token_type == "OPERATOR" and token_value in ("-", "!", "~"):
        return _parse_unary_expr(parser_state)
    
    # 2. Parenthesized expression
    if token_type == "LPAREN":
        parser_state["pos"] += 1  # consume '('
        expr_ast = _parse_expression(parser_state)
        if parser_state["pos"] >= len(tokens):
            raise SyntaxError(f"{filename}:{line}:{column}: Expected ')'")
        close_token = tokens[parser_state["pos"]]
        if close_token.get("type") != "RPAREN":
            raise SyntaxError(f"{filename}:{line}:{column}: Expected ')'")
        parser_state["pos"] += 1  # consume ')'
        return expr_ast
    
    # 3. Identifier or function call
    if token_type == "IDENTIFIER":
        parser_state["pos"] += 1  # consume identifier
        if parser_state["pos"] < len(tokens) and tokens[parser_state["pos"]].get("type") == "LPAREN":
            return _parse_function_call(parser_state, token_value, line, column)
        return {"type": "IDENTIFIER", "children": [], "value": token_value, "line": line, "column": column}
    
    # 4. Literals
    if token_type == "NUMBER_INT":
        parser_state["pos"] += 1
        return {"type": "LITERAL", "children": [], "value": int(token_value), "line": line, "column": column}
    
    if token_type == "NUMBER_FLOAT":
        parser_state["pos"] += 1
        return {"type": "LITERAL", "children": [], "value": float(token_value), "line": line, "column": column}
    
    if token_type == "STRING":
        parser_state["pos"] += 1
        return {"type": "LITERAL", "children": [], "value": token_value, "line": line, "column": column}
    
    if token_type == "BOOL":
        parser_state["pos"] += 1
        bool_value = token_value.lower() == "true"
        return {"type": "LITERAL", "children": [], "value": bool_value, "line": line, "column": column}
    
    if token_type == "NULL":
        parser_state["pos"] += 1
        return {"type": "LITERAL", "children": [], "value": None, "line": line, "column": column}
    
    raise SyntaxError(f"{filename}:{line}:{column}: Unexpected token '{token_value}'")

# === helper functions ===
# All helpers delegated to sub-functions

# === OOP compatibility layer ===
# No OOP wrapper needed for parser helper function

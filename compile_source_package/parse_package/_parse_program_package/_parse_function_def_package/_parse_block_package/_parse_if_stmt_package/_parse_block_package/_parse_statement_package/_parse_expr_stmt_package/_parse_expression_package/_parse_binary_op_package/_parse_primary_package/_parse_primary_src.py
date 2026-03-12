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
def _parse_primary(parser_state: dict) -> dict:
    """Parses a primary expression (literal, identifier, or parenthesized expression)."""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    filename = parser_state["filename"]
    
    # Check bounds
    if pos >= len(tokens):
        last_token = tokens[-1] if tokens else {"line": 1, "column": 1}
        raise SyntaxError(f"{filename}:{last_token['line']}:{last_token['column']}: 意外的表达式结束")
    
    token = tokens[pos]
    token_type = token["type"]
    token_value = token["value"]
    line = token["line"]
    column = token["column"]
    
    if token_type == "NUMBER":
        parser_state["pos"] += 1
        return {"type": "NUM_LITERAL", "value": token_value, "line": line, "column": column}
    
    elif token_type == "STRING":
        parser_state["pos"] += 1
        # Strip quotes from string value
        stripped_value = _strip_quotes(token_value)
        return {"type": "STR_LITERAL", "value": stripped_value, "line": line, "column": column}
    
    elif token_type == "IDENTIFIER":
        parser_state["pos"] += 1
        return {"type": "IDENTIFIER", "value": token_value, "line": line, "column": column}
    
    elif token_type == "LPAREN":
        # Consume LPAREN
        parser_state["pos"] += 1
        # Parse inner expression
        inner_ast = _parse_expression(parser_state)
        # Check for RPAREN
        new_pos = parser_state["pos"]
        if new_pos >= len(tokens):
            raise SyntaxError(f"{filename}:{line}:{column}: 期望右括号 ')'")
        current_token = tokens[new_pos]
        if current_token["type"] != "RPAREN":
            raise SyntaxError(f"{filename}:{current_token['line']}:{current_token['column']}: 期望右括号 ')'")
        # Consume RPAREN
        parser_state["pos"] += 1
        return {"type": "PAREN_EXPR", "children": [inner_ast], "line": line, "column": column}
    
    else:
        raise SyntaxError(f"{filename}:{line}:{column}: 无效的主表达式")

# === helper functions ===
def _strip_quotes(s: str) -> str:
    """Remove surrounding quotes from a string literal."""
    if len(s) >= 2:
        if (s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'"):
            return s[1:-1]
    return s

# === OOP compatibility layer ===

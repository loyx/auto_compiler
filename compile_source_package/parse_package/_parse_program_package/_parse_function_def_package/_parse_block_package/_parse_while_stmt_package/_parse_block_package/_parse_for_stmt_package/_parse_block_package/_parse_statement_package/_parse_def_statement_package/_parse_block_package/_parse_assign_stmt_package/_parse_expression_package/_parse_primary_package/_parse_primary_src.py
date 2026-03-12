# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_or_package._parse_or_src import _parse_or
from ._expect_token_package._expect_token_src import _expect_token
from ._parse_argument_list_package._parse_argument_list_src import _parse_argument_list

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
#   "op": str,
#   "left": AST,
#   "right": AST,
#   "operand": AST,
#   "name": AST,
#   "args": list,
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
    """解析原子表达式（字面量、标识符、括号、函数调用）。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        raise SyntaxError(f"Unexpected end of input at {parser_state.get('filename', 'unknown')}")
    
    token = tokens[pos]
    token_type = token["type"]
    token_value = token["value"]
    line = token.get("line", 0)
    column = token.get("column", 0)
    
    if token_type == "INTEGER":
        parser_state["pos"] = pos + 1
        return {"type": "LITERAL", "value": int(token_value), "line": line, "column": column}
    
    if token_type == "FLOAT":
        parser_state["pos"] = pos + 1
        return {"type": "LITERAL", "value": float(token_value), "line": line, "column": column}
    
    if token_type == "STRING":
        parser_state["pos"] = pos + 1
        stripped = token_value[1:-1] if len(token_value) >= 2 else token_value
        return {"type": "LITERAL", "value": stripped, "line": line, "column": column}
    
    if token_type == "TRUE":
        parser_state["pos"] = pos + 1
        return {"type": "LITERAL", "value": True, "line": line, "column": column}
    
    if token_type == "FALSE":
        parser_state["pos"] = pos + 1
        return {"type": "LITERAL", "value": False, "line": line, "column": column}
    
    if token_type == "IDENTIFIER":
        parser_state["pos"] = pos + 1
        next_pos = parser_state["pos"]
        if next_pos < len(tokens) and tokens[next_pos]["type"] == "LPAREN":
            parser_state["pos"] = next_pos + 1
            args = _parse_argument_list(parser_state)
            _expect_token(parser_state, "RPAREN")
            return {
                "type": "CALL",
                "name": {"type": "IDENTIFIER", "value": token_value, "line": line, "column": column},
                "args": args,
                "line": line,
                "column": column
            }
        return {"type": "IDENTIFIER", "value": token_value, "line": line, "column": column}
    
    if token_type == "LPAREN":
        parser_state["pos"] = pos + 1
        expr = _parse_or(parser_state)
        _expect_token(parser_state, "RPAREN")
        return expr
    
    raise SyntaxError(f"Unexpected token '{token_value}' at line {line}, column {column}")


# === helper functions ===
# No helper functions - all logic delegated to child functions

# === OOP compatibility layer ===
# No OOP wrapper needed for parser helper function

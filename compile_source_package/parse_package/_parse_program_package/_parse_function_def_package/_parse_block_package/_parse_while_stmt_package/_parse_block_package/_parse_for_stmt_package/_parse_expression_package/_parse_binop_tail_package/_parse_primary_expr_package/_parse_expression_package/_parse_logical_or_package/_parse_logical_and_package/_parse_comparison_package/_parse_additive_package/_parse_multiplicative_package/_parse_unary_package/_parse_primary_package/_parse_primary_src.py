# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_unary_package._parse_unary_src import _parse_unary
from ._parse_array_literal_package._parse_array_literal_src import _parse_array_literal
from ._parse_dict_literal_package._parse_dict_literal_src import _parse_dict_literal

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
#   "operator": str,
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


def _make_error_node(parser_state: ParserState, message: str, line: int = -1, column: int = -1) -> AST:
    """Helper to create ERROR node and set parser_state error."""
    parser_state["error"] = message
    return {"type": "ERROR", "value": None, "line": line, "column": column}


def _parse_primary(parser_state: ParserState) -> AST:
    """解析初级表达式（字面量、标识符、括号表达式、数组/字典字面量）。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        return _make_error_node(parser_state, "Unexpected end of input", -1, -1)
    
    token = tokens[pos]
    token_type = token.get("type")
    token_value = token.get("value")
    line = token.get("line", -1)
    column = token.get("column", -1)
    
    # NUMBER 字面量
    if token_type == "NUMBER":
        parser_state["pos"] = pos + 1
        return {"type": "LITERAL", "value": token_value, "literal_type": "NUMBER", "line": line, "column": column}
    
    # STRING 字面量（去除引号）
    if token_type == "STRING":
        parser_state["pos"] = pos + 1
        value = token_value
        if len(value) >= 2 and ((value[0] == '"' and value[-1] == '"') or (value[0] == "'" and value[-1] == "'")):
            value = value[1:-1]
        return {"type": "LITERAL", "value": value, "literal_type": "STRING", "line": line, "column": column}
    
    # IDENTIFIER
    if token_type == "IDENTIFIER":
        parser_state["pos"] = pos + 1
        return {"type": "IDENTIFIER", "name": token_value, "line": line, "column": column}
    
    # TRUE / FALSE / NULL
    if token_type == "TRUE":
        parser_state["pos"] = pos + 1
        return {"type": "LITERAL", "value": True, "literal_type": "BOOLEAN", "line": line, "column": column}
    if token_type == "FALSE":
        parser_state["pos"] = pos + 1
        return {"type": "LITERAL", "value": False, "literal_type": "BOOLEAN", "line": line, "column": column}
    if token_type == "NULL":
        parser_state["pos"] = pos + 1
        return {"type": "LITERAL", "value": None, "literal_type": "NULL", "line": line, "column": column}
    
    # LEFT_PAREN - 括号表达式
    if token_type == "LEFT_PAREN":
        parser_state["pos"] = pos + 1
        inner_expr = _parse_unary(parser_state)
        if parser_state["error"]:
            return inner_expr
        new_pos = parser_state["pos"]
        if new_pos < len(tokens) and tokens[new_pos].get("type") == "RIGHT_PAREN":
            parser_state["pos"] = new_pos + 1
            return inner_expr
        else:
            return _make_error_node(parser_state, "Missing closing parenthesis", line, column)
    
    # LEFT_BRACKET - 数组字面量
    if token_type == "LEFT_BRACKET":
        parser_state["pos"] = pos + 1
        return _parse_array_literal(parser_state, line, column)
    
    # LEFT_BRACE - 字典字面量
    if token_type == "LEFT_BRACE":
        parser_state["pos"] = pos + 1
        return _parse_dict_literal(parser_state, line, column)
    
    # 无法识别的 token
    return _make_error_node(parser_state, f"Unexpected token: {token_type}", line, column)


# === helper functions ===
# _make_error_node is defined above main function


# === OOP compatibility layer ===
# Not needed for this parser function node

# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_expression_package._parse_expression_src import _parse_expression
from ._create_error_node_package._create_error_node_src import _create_error_node
from ._parse_number_package._parse_number_src import _parse_number
from ._parse_string_package._parse_string_src import _parse_string
from ._create_literal_node_package._create_literal_node_src import _create_literal_node

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,             # token 类型
#   "value": str,            # token 值
#   "line": int,             # 行号
#   "column": int            # 列号
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型
#   "children": list,        # 子节点列表
#   "value": Any,            # 节点值
#   "line": int,             # 行号
#   "column": int            # 列号
# }

ParserState = Dict[str, Any]
# ParserState possible fields:
# {
#   "tokens": list,          # token 列表
#   "pos": int,              # 当前位置
#   "filename": str,         # 源文件名
#   "error": str             # 错误信息
# }


# === main function ===
def _parse_primary(parser_state: dict) -> dict:
    """解析基础表达式（primary expression）。"""
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    if pos >= len(tokens):
        parser_state["error"] = "Unexpected end of input"
        return _create_error_node("Unexpected end of input", 0, 0)
    
    current_token = tokens[pos]
    token_type = current_token.get("type", "")
    token_value = current_token.get("value", "")
    token_line = current_token.get("line", 0)
    token_column = current_token.get("column", 0)
    
    if token_type == "IDENTIFIER":
        parser_state["pos"] = pos + 1
        return {
            "type": "IDENTIFIER",
            "value": token_value,
            "children": [],
            "line": token_line,
            "column": token_column
        }
    
    if token_type == "NUMBER":
        parser_state["pos"] = pos + 1
        return _parse_number(token_value, token_line, token_column)
    
    if token_type == "STRING":
        parser_state["pos"] = pos + 1
        return _parse_string(token_value, token_line, token_column)
    
    if token_type == "TRUE":
        parser_state["pos"] = pos + 1
        return _create_literal_node(True, token_line, token_column)
    
    if token_type == "FALSE":
        parser_state["pos"] = pos + 1
        return _create_literal_node(False, token_line, token_column)
    
    if token_type == "NIL":
        parser_state["pos"] = pos + 1
        return _create_literal_node(None, token_line, token_column)
    
    if token_type == "LEFT_PAREN":
        parser_state["pos"] = pos + 1
        expr_ast = _parse_expression(parser_state)
        if parser_state.get("error"):
            return expr_ast
        new_pos = parser_state.get("pos", 0)
        if new_pos >= len(tokens):
            parser_state["error"] = "Expected ')' but found end of input"
            return _create_error_node("Expected ')' but found end of input", token_line, token_column)
        next_token = tokens[new_pos]
        if next_token.get("type") != "RIGHT_PAREN":
            parser_state["error"] = f"Expected ')' but found '{next_token.get('value', '')}'"
            return _create_error_node(f"Expected ')' but found '{next_token.get('value', '')}'", token_line, token_column)
        parser_state["pos"] = new_pos + 1
        return expr_ast
    
    parser_state["error"] = f"Unexpected token: {token_value}"
    return _create_error_node(f"Unexpected token: {token_value}", token_line, token_column)


# === helper functions ===
# No helper functions; all logic delegated

# === OOP compatibility layer ===
# No OOP wrapper needed

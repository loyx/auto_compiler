# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_unary_expr_package._parse_unary_expr_src import _parse_unary_expr
from ._create_error_node_package._create_error_node_src import _create_error_node

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
#   "type": str,             # 节点类型 (BINARY_OP, UNARY_OP, IDENTIFIER, LITERAL, PAREN_EXPR, etc.)
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
#   "error": str             # 错误信息（可选）
# }


# === main function ===
def _parse_primary_expr(parser_state: ParserState) -> AST:
    """
    解析基本表达式（标识符、字面量、括号表达式）。
    
    处理以下 token 类型：
    - IDENTIFIER: 返回 IDENTIFIER 节点
    - NUMBER: 返回 LITERAL 节点（数值）
    - STRING: 返回 LITERAL 节点（字符串）
    - TRUE/FALSE: 返回 LITERAL 节点（布尔值）
    - NULL: 返回 LITERAL 节点（None）
    - LPAREN: 解析括号内表达式，返回 PAREN_EXPR 节点
    """
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    # 检查位置是否超出范围
    if pos >= len(tokens):
        parser_state["error"] = "Unexpected end of input"
        return _create_error_node(pos, tokens)
    
    current_token = tokens[pos]
    token_type = current_token.get("type", "")
    token_value = current_token.get("value", "")
    line = current_token.get("line", 0)
    column = current_token.get("column", 0)
    
    # 根据 token 类型处理
    if token_type == "IDENTIFIER":
        parser_state["pos"] = pos + 1
        return {"type": "IDENTIFIER", "value": token_value, "line": line, "column": column, "children": []}
    
    elif token_type == "NUMBER":
        parser_state["pos"] = pos + 1
        parsed_value = _parse_number_value(token_value)
        return {"type": "LITERAL", "value": parsed_value, "line": line, "column": column, "children": []}
    
    elif token_type == "STRING":
        parser_state["pos"] = pos + 1
        return {"type": "LITERAL", "value": token_value, "line": line, "column": column, "children": []}
    
    elif token_type == "TRUE":
        parser_state["pos"] = pos + 1
        return {"type": "LITERAL", "value": True, "line": line, "column": column, "children": []}
    
    elif token_type == "FALSE":
        parser_state["pos"] = pos + 1
        return {"type": "LITERAL", "value": False, "line": line, "column": column, "children": []}
    
    elif token_type == "NULL":
        parser_state["pos"] = pos + 1
        return {"type": "LITERAL", "value": None, "line": line, "column": column, "children": []}
    
    elif token_type == "LPAREN":
        return _handle_paren_expr(parser_state, pos, line, column, tokens)
    
    else:
        parser_state["error"] = f"Unexpected token: {token_type}"
        return _create_error_node(pos, tokens)


# === helper functions ===
def _parse_number_value(token_value: str) -> Any:
    """将 token 值解析为 int 或 float。"""
    try:
        if "." in token_value:
            return float(token_value)
        else:
            return int(token_value)
    except ValueError:
        return token_value


def _handle_paren_expr(parser_state: ParserState, pos: int, line: int, column: int, tokens: list) -> AST:
    """处理括号表达式。"""
    # 消费左括号
    parser_state["pos"] = pos + 1
    
    # 解析括号内的表达式
    inner_ast = _parse_unary_expr(parser_state)
    
    # 检查是否有错误
    if parser_state.get("error"):
        return inner_ast
    
    # 消费右括号
    new_pos = parser_state.get("pos", 0)
    if new_pos >= len(tokens):
        parser_state["error"] = "Missing closing parenthesis"
        return {"type": "PAREN_EXPR", "value": None, "line": line, "column": column, "children": [inner_ast]}
    
    next_token = tokens[new_pos]
    if next_token.get("type") != "RPAREN":
        parser_state["error"] = f"Expected RPAREN, got {next_token.get('type')}"
        return {"type": "PAREN_EXPR", "value": None, "line": line, "column": column, "children": [inner_ast]}
    
    # 消费右括号
    parser_state["pos"] = new_pos + 1
    
    return {"type": "PAREN_EXPR", "value": None, "line": line, "column": column, "children": [inner_ast]}

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node.

# === std / third-party imports ===
from typing import Any, Dict, List

# === sub function imports ===
from ._parse_identifier_package._parse_identifier_src import _parse_identifier

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
def _parse_expression(parser_state: ParserState) -> AST:
    """解析单个表达式节点。"""
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    # 边界检查：pos 越界
    if pos >= len(tokens):
        parser_state["error"] = "Unexpected end of expression"
        return _create_ast_node("ERROR", value=None, line=-1, column=-1)
    
    token = tokens[pos]
    token_type = token.get("type", "")
    token_value = token.get("value", "")
    token_line = token.get("line", 0)
    token_column = token.get("column", 0)
    
    # 根据 token 类型分发
    if token_type == "NUMBER":
        return _create_ast_node("NUMBER_LITERAL", value=token_value, line=token_line, column=token_column)
    
    elif token_type == "STRING":
        return _create_ast_node("STRING_LITERAL", value=token_value, line=token_line, column=token_column)
    
    elif token_type == "IDENTIFIER":
        return _parse_identifier(parser_state)
    
    elif token_type == "LEFT_PAREN":
        return _parse_paren_expression(parser_state)
    
    elif token_type in ["PLUS", "MINUS", "STAR", "SLASH", "PERCENT", "EQ", "NE", "LT", "GT", "LE", "GE", "AND", "OR"]:
        return _create_ast_node("OPERATOR", value=token_value, line=token_line, column=token_column)
    
    else:
        parser_state["error"] = f"Unexpected token type: {token_type}"
        return _create_ast_node("ERROR", value=token_value, line=token_line, column=token_column)

# === helper functions ===
def _create_ast_node(node_type: str, value: Any = None, children: List = None, line: int = 0, column: int = 0) -> AST:
    """创建 AST 节点的辅助函数。"""
    return {
        "type": node_type,
        "children": children if children is not None else [],
        "value": value,
        "line": line,
        "column": column
    }

def _parse_paren_expression(parser_state: ParserState) -> AST:
    """解析括号表达式 (...)。"""
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    if pos >= len(tokens) or tokens[pos].get("type") != "LEFT_PAREN":
        parser_state["error"] = "Expected LEFT_PAREN"
        return _create_ast_node("ERROR", value=None, line=-1, column=-1)
    
    # 跳过 LEFT_PAREN
    parser_state["pos"] = pos + 1
    
    # 解析内部表达式
    inner_ast = _parse_expression(parser_state)
    
    # 检查 RIGHT_PAREN
    new_pos = parser_state.get("pos", 0)
    if new_pos >= len(tokens) or tokens[new_pos].get("type") != "RIGHT_PAREN":
        parser_state["error"] = "Expected RIGHT_PAREN"
        return _create_ast_node("ERROR", value=None, line=-1, column=-1)
    
    # 跳过 RIGHT_PAREN
    parser_state["pos"] = new_pos + 1
    
    return _create_ast_node(
        "PAREN_EXPR",
        value=None,
        children=[inner_ast],
        line=tokens[pos].get("line", 0),
        column=tokens[pos].get("column", 0)
    )

# === OOP compatibility layer ===
# No OOP wrapper needed for this parser function node
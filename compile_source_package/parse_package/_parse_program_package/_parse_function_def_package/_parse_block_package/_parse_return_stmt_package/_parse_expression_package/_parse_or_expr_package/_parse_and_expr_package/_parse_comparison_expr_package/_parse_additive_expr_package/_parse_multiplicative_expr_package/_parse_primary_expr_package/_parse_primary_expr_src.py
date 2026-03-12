# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_additive_expr_package._parse_additive_expr_src import _parse_additive_expr

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
#   "type": str,             # 节点类型 (BINARY_OP, UNARY_OP, IDENTIFIER, LITERAL, etc.)
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
    """解析 primary 表达式（标识符、字面量、括号表达式等）。"""
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 检查是否还有 token
    if pos >= len(tokens):
        parser_state["error"] = "Expected primary expression"
        return {"type": "ERROR", "value": None, "line": 0, "column": 0}
    
    current_token = tokens[pos]
    token_type = current_token["type"]
    token_value = current_token["value"]
    line = current_token["line"]
    column = current_token["column"]
    
    # 处理标识符
    if token_type == "IDENTIFIER":
        parser_state["pos"] = pos + 1
        return {"type": "IDENTIFIER", "value": token_value, "line": line, "column": column}
    
    # 处理数字字面量
    elif token_type == "NUMBER":
        parser_state["pos"] = pos + 1
        return {"type": "LITERAL", "value": token_value, "line": line, "column": column}
    
    # 处理字符串字面量
    elif token_type == "STRING":
        parser_state["pos"] = pos + 1
        return {"type": "LITERAL", "value": token_value, "line": line, "column": column}
    
    # 处理括号表达式
    elif token_type == "LPAREN":
        parser_state["pos"] = pos + 1  # 消费 LPAREN
        expr_ast = _parse_additive_expr(parser_state)
        
        # 检查是否有错误
        if parser_state.get("error"):
            return expr_ast
        
        # 消费 RPAREN
        new_pos = parser_state["pos"]
        if new_pos >= len(tokens) or tokens[new_pos]["type"] != "RPAREN":
            parser_state["error"] = "Expected RPAREN"
            return {"type": "ERROR", "value": None, "line": line, "column": column}
        
        parser_state["pos"] = new_pos + 1
        return expr_ast
    
    # 无效的 primary 起始 token
    else:
        parser_state["error"] = "Expected primary expression"
        return {"type": "ERROR", "value": None, "line": line, "column": column}

# === helper functions ===

# === OOP compatibility layer ===

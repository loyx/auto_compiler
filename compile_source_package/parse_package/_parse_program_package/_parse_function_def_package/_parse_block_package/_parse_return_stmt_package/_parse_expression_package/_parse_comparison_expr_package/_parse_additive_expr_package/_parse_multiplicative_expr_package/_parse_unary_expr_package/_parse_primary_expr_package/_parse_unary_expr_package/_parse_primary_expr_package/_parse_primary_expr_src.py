# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_unary_expr_package._parse_unary_expr_src import _parse_unary_expr

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,             # token 类型 (IDENTIFIER, NUMBER, STRING, LPAREN, RPAREN, OPERATOR, etc.)
#   "value": str,            # token 值
#   "line": int,             # 行号
#   "column": int            # 列号
# }

AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (UNARY_OP, IDENTIFIER, LITERAL, ERROR, etc.)
#   "children": list,        # 子节点列表
#   "value": Any,            # 节点值（operator 符号或字面量值）
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
def _parse_primary_expr(parser_state: ParserState) -> AST:
    """解析基本表达式（标识符、字面量、括号表达式等）。"""
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    filename = parser_state.get("filename", "")
    
    # 检查是否已到 token 末尾
    if pos >= len(tokens):
        parser_state["error"] = "Unexpected end of input"
        return {"type": "ERROR", "children": [], "value": None, "line": -1, "column": -1}
    
    current_token = tokens[pos]
    token_type = current_token.get("type", "")
    token_value = current_token.get("value", "")
    token_line = current_token.get("line", -1)
    token_column = current_token.get("column", -1)
    
    # 处理标识符
    if token_type == "IDENTIFIER":
        parser_state["pos"] = pos + 1
        return {
            "type": "IDENTIFIER",
            "children": [],
            "value": token_value,
            "line": token_line,
            "column": token_column
        }
    
    # 处理字面量
    if token_type in ("NUMBER", "STRING", "BOOLEAN", "NULL"):
        parser_state["pos"] = pos + 1
        return {
            "type": "LITERAL",
            "children": [],
            "value": token_value,
            "line": token_line,
            "column": token_column
        }
    
    # 处理括号表达式
    if token_type == "LPAREN":
        parser_state["pos"] = pos + 1  # 消费 LPAREN
        
        # 解析括号内的表达式
        inner_expr = _parse_unary_expr(parser_state)
        
        # 检查是否有错误
        if parser_state.get("error"):
            return inner_expr
        
        # 期望 RPAREN
        new_pos = parser_state.get("pos", 0)
        if new_pos >= len(tokens):
            parser_state["error"] = "Expected ')' but found end of input"
            return {"type": "ERROR", "children": [], "value": None, "line": token_line, "column": token_column}
        
        next_token = tokens[new_pos]
        if next_token.get("type") != "RPAREN":
            parser_state["error"] = f"Expected ')' but found '{next_token.get('value')}'"
            return {"type": "ERROR", "children": [], "value": None, "line": token_line, "column": token_column}
        
        # 消费 RPAREN
        parser_state["pos"] = new_pos + 1
        return inner_expr
    
    # 其他类型：错误
    parser_state["error"] = f"Unexpected token '{token_value}' of type '{token_type}'"
    return {"type": "ERROR", "children": [], "value": None, "line": token_line, "column": token_column}

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for parser functions
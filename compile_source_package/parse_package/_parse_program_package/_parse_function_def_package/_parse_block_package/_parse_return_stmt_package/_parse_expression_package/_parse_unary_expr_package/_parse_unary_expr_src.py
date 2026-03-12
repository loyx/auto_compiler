# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# Note: Import is done inside the function to avoid circular dependency

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
def _parse_unary_expr(parser_state: ParserState) -> AST:
    """解析一元表达式（处理 -, ! 运算符，右结合）。"""
    # Lazy import to avoid circular dependency
    from ._parse_primary_expr_package._parse_primary_expr_src import _parse_primary_expr
    
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 检查是否还有 token
    if pos >= len(tokens):
        return _parse_primary_expr(parser_state)
    
    current_token = tokens[pos]
    token_type = current_token.get("type", "")
    
    # 检查是否为一元运算符
    if token_type in ("MINUS", "NOT"):
        # 消费运算符 token
        operator_str = "-" if token_type == "MINUS" else "!"
        line = current_token.get("line", 0)
        column = current_token.get("column", 0)
        parser_state["pos"] = pos + 1
        
        # 递归解析操作数（支持连续一元运算符）
        operand = _parse_unary_expr(parser_state)
        
        # 构建 UNARY_OP 节点
        return {
            "type": "UNARY_OP",
            "value": operator_str,
            "children": [operand],
            "line": line,
            "column": column
        }
    else:
        # 不是运算符，解析基本表达式
        return _parse_primary_expr(parser_state)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for parser helper function

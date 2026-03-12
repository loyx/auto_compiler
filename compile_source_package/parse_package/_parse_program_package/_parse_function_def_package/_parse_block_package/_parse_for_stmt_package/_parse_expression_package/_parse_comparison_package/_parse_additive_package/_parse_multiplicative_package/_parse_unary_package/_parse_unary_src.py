# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_primary_package._parse_primary_src import _parse_primary

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
def _parse_unary(parser_state: ParserState) -> AST:
    """
    解析一元表达式（前缀运算符）。
    
    语法：unary_expr := (unary_op)* primary_expr
    一元运算符：PLUS (+), MINUS (-), BANG (!)
    """
    if parser_state.get("error"):
        return {"type": "ERROR", "children": [], "value": None, "line": 0, "column": 0}
    
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    # 收集所有一元运算符
    unary_ops = []
    while pos < len(tokens):
        token = tokens[pos]
        token_type = token.get("type", "")
        
        if token_type in ("PLUS", "MINUS", "BANG"):
            op_value = token.get("value", "")
            line = token.get("line", 0)
            column = token.get("column", 0)
            unary_ops.append({"op": op_value, "line": line, "column": column})
            pos += 1
        else:
            break
    
    parser_state["pos"] = pos
    
    # 解析基础表达式
    operand = _parse_primary(parser_state)
    
    if parser_state.get("error"):
        return {"type": "ERROR", "children": [], "value": None, "line": 0, "column": 0}
    
    # 从内到外构建一元运算符节点（右结合）
    result = operand
    for op_info in reversed(unary_ops):
        result = {
            "type": "UNARY_OP",
            "value": op_info["op"],
            "children": [result],
            "line": op_info["line"],
            "column": op_info["column"]
        }
    
    return result

# === helper functions ===
def _get_current_token(parser_state: ParserState) -> Token:
    """获取当前位置的 token，若越界则返回 None。"""
    pos = parser_state.get("pos", 0)
    tokens = parser_state.get("tokens", [])
    if pos < len(tokens):
        return tokens[pos]
    return None

# === OOP compatibility layer ===
# Not needed for parser helper function

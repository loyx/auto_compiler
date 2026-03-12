# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_unary_expr_package._parse_unary_expr_src import _parse_unary_expr

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
def _parse_multiplicative_expr(parser_state: ParserState) -> AST:
    """解析乘除表达式（更高优先级的二元运算符表达式）。"""
    # 解析左侧操作数
    left_ast = _parse_unary_expr(parser_state)
    
    # 检查是否出错
    if parser_state.get("error"):
        return left_ast
    
    # 检查当前 token 是否为乘法运算符
    tokens = parser_state["tokens"]
    pos = parser_state["pos"]
    
    if pos >= len(tokens):
        return left_ast
    
    current_token = tokens[pos]
    operator = current_token.get("value", "")
    
    if operator not in ("*", "/"):
        return left_ast
    
    # 记录运算符信息
    op_line = current_token.get("line", 0)
    op_column = current_token.get("column", 0)
    
    # 消费运算符 token
    parser_state["pos"] = pos + 1
    
    # 解析右侧操作数
    right_ast = _parse_unary_expr(parser_state)
    
    # 检查是否出错
    if parser_state.get("error"):
        return right_ast
    
    # 构建 BINARY_OP AST 节点
    result = {
        "type": "BINARY_OP",
        "children": [left_ast, right_ast],
        "value": operator,
        "line": op_line,
        "column": op_column
    }
    
    return result

# === helper functions ===

# === OOP compatibility layer ===

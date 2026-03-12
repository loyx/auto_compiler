# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._parse_and_expr_package._parse_and_expr_src import _parse_and_expr

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
def _parse_or_expr(parser_state: ParserState) -> AST:
    """
    解析 OR 表达式（|| 运算符），是表达式解析的入口函数（最低优先级）。
    """
    # 检查是否已有错误
    if parser_state.get("error"):
        return {"type": "ERROR", "children": [], "value": None, "line": 0, "column": 0}
    
    # 解析左侧操作数
    left_ast = _parse_and_expr(parser_state)
    
    # 若左侧解析出错，直接返回
    if parser_state.get("error"):
        return left_ast
    
    # 循环处理 || 运算符
    tokens = parser_state.get("tokens", [])
    pos = parser_state.get("pos", 0)
    
    while pos < len(tokens):
        token = tokens[pos]
        
        # 检查是否为 OR 运算符
        if token.get("type") == "OR" or token.get("value") == "||":
            # 消费 OR token
            or_line = token.get("line", 0)
            or_column = token.get("column", 0)
            parser_state["pos"] = pos + 1
            
            # 解析右侧操作数
            right_ast = _parse_and_expr(parser_state)
            
            # 若右侧解析出错，返回
            if parser_state.get("error"):
                return right_ast
            
            # 构建 BINARY_OP 节点
            left_ast = {
                "type": "BINARY_OP",
                "operator": "||",
                "children": [left_ast, right_ast],
                "line": or_line,
                "column": or_column
            }
            
            # 更新位置
            pos = parser_state.get("pos", 0)
        else:
            # 不是 OR 运算符，结束循环
            break
    
    return left_ast


# === helper functions ===
# No helper functions needed


# === OOP compatibility layer ===
# No OOP wrapper needed for parser function
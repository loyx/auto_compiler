# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions needed for this simple utility

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
#   "type": str,             # 节点类型 (BINARY_OP, UNARY_OP, IDENTIFIER, LITERAL, ERROR, etc.)
#   "children": list,        # 子节点列表
#   "value": Any,            # 节点值
#   "line": int,             # 行号
#   "column": int            # 列号
# }

# === main function ===
def _create_error_node(pos: int, tokens: list) -> AST:
    """
    创建错误 AST 节点。
    
    从 tokens 中提取位置信息，返回 ERROR 类型的 AST 节点。
    纯函数，不修改任何输入参数。
    """
    if pos < len(tokens):
        line = tokens[pos].get("line", 0)
        column = tokens[pos].get("column", 0)
    else:
        line = 0
        column = 0
    
    return {
        "type": "ERROR",
        "value": None,
        "line": line,
        "column": column,
        "children": []
    }

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed - this is a utility function, not a framework entry point

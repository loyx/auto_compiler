# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed for this simple builder

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

# === main function ===
def _build_binary_op(left: AST, right: AST, op_token: Token) -> AST:
    """
    构建二元操作 AST 节点。
    
    Args:
        left: 左操作数的 AST 节点
        right: 右操作数的 AST 节点
        op_token: 运算符 token
    
    Returns:
        BINARY_OP 类型的 AST 节点
    """
    return {
        "type": "BINARY_OP",
        "value": op_token["value"],
        "children": [left, right],
        "line": left["line"],
        "column": left["column"]
    }

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this pure function node

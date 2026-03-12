# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed for this simple builder

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,
#   "children": list,
#   "value": Any,
#   "line": int,
#   "column": int,
#   "operator": str,
#   "left": AST,
#   "right": AST
# }

# === main function ===
def _make_binary_op(operator: str, left: AST, right: AST, line: int, column: int) -> AST:
    """
    构建二元操作 AST 节点。
    
    创建一个新的 AST 字典，设置 type 为 "binary_op"，
    并填充 operator、left、right、line、column 字段。
    """
    return {
        "type": "binary_op",
        "operator": operator,
        "left": left,
        "right": right,
        "line": line,
        "column": column
    }

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed - this is a pure function node, no framework requires class wrapper

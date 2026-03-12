# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No subfunctions needed for this simple helper

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型
#   "children": list,        # 子节点列表
#   "value": Any,            # 节点值
#   "line": int,             # 行号
#   "column": int            # 列号
# }

# === main function ===
def _create_error_node(error_message: str, line: int, column: int) -> AST:
    """
    Create an ERROR node in the AST.
    
    Args:
        error_message: Error description message string
        line: Line number where error occurred
        column: Column number where error occurred
    
    Returns:
        AST node dictionary with type="ERROR"
    """
    return {
        "type": "ERROR",
        "value": error_message,
        "children": [],
        "line": line,
        "column": column
    }

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this helper function
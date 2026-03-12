# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed for this simple implementation

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 ("block")
#   "children": list,        # 子节点列表
#   "line": int,             # 行号
#   "column": int            # 列号
#   "data_type": str         # 可选：节点的数据类型
# }

SymbolTable = Dict[str, Any]
# SymbolTable possible fields:
# {
#   "variables": Dict[str, Dict],
#   "functions": Dict[str, Dict],
#   "current_scope": int,
#   "scope_stack": list,
#   "current_function": str,
#   "errors": list
# }

# === main function ===
def _handle_block(node: AST, symbol_table: SymbolTable) -> str:
    """
    Handle block node, return the type of the last expression.
    
    Processing logic:
    1. Get children from node
    2. If children is empty, return "void"
    3. Return the data_type of the last child, or "void" if not available
    
    Note: Cannot call _traverse_node directly (circular dependency).
    Parent function coordinates recursion.
    """
    children = node.get("children", [])
    
    if not children:
        return "void"
    
    # Get the last child and check for data_type field
    last_child = children[-1]
    return last_child.get("data_type", "void")

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this function

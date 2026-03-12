# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ... import _traverse_node

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,
#   "children": list,
#   "value": Any,
#   "data_type": str,
#   "line": int,
#   "column": int
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
def _handle_block(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理 block 类型节点（代码块）。
    
    遍历块内所有子节点，对每个子节点递归调用 _traverse_node。
    所有错误通过 symbol_table["errors"] 收集。
    block 本身不创建新作用域。
    """
    children = node.get("children", [])
    
    if not isinstance(children, list):
        symbol_table.setdefault("errors", []).append({
            "type": "warning",
            "message": f"Block node has invalid children type: {type(children).__name__}",
            "line": node.get("line", "?"),
            "column": node.get("column", "?")
        })
        return
    
    for child_node in children:
        _traverse_node(child_node, symbol_table)

# === helper functions ===
# No helper functions needed for this simple traversal logic

# === OOP compatibility layer ===
# No OOP wrapper needed for internal AST traversal function

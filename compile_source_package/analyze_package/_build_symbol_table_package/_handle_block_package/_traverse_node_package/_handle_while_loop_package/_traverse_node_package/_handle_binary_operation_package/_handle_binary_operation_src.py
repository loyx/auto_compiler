# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# Note: _traverse_node is a parent dispatcher function for tree traversal
# This is a special case for mutual recursion in AST traversal systems
# Using lazy import to avoid circular import issues

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,
#   "left": AST,             # 左操作数
#   "right": AST,            # 右操作数
#   "operator": str,         # 运算符（如 "+", "-", "*", "/" 等）
# }

SymbolTable = Dict[str, Any]
# SymbolTable possible fields:
# {
#   "variables": Dict[str, Dict],
#   "functions": Dict[str, Dict],
#   "current_scope": int,
#   "scope_stack": list
# }

# === main function ===
def _handle_binary_operation(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理 binary_operation 节点，递归遍历 left 和 right 子节点。
    
    Args:
        node: AST node，包含 "left"、"right"、"operator" 字段
        symbol_table: 符号表，在遍历过程中可能被修改
    """
    # Lazy import to avoid circular import
    from .._traverse_node_src import _traverse_node
    
    left = node.get("left")
    right = node.get("right")
    
    if left is not None:
        _traverse_node(left, symbol_table)
    
    if right is not None:
        _traverse_node(right, symbol_table)

# === helper functions ===
# No helper functions needed for this simple traversal logic

# === OOP compatibility layer ===
# No OOP wrapper needed - this is a handler function in a traversal system

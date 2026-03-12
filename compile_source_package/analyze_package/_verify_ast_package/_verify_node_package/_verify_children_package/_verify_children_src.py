# === std / third-party imports ===
from typing import Any, Dict, List

# === sub function imports ===
# Delayed import for _verify_node as specified in requirements
# This will be imported at runtime to avoid circular dependencies

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型
#   "children": list,        # 子节点列表（AST 节点列表）
#   "line": int,             # 行号
#   "column": int            # 列号
# }

SymbolTable = Dict[str, Any]
# SymbolTable possible fields:
# {
#   "variables": Dict[str, Dict],
#   "functions": Dict[str, Dict],
#   "current_scope": int,
# }

ContextStack = List[Dict[str, Any]]
# ContextStack possible fields:
# [
#   {"type": "function", "name": str, "return_type": str},
#   {"type": "loop", "stmt_type": "while"|"for"}
# ]

# === main function ===
def _verify_children(node: AST, symbol_table: SymbolTable, context_stack: ContextStack, filename: str) -> None:
    """
    递归验证 node['children'] 列表中的所有子节点。
    
    对每个子节点调用 _verify_node 进行验证。
    若 node['children'] 不存在或为空列表，直接返回。
    """
    children = node.get('children', [])
    
    if not children:
        return
    
    # Delayed import to avoid circular dependencies
    from ._verify_node_package import _verify_node_src
    
    for child in children:
        _verify_node_src._verify_node(child, symbol_table, context_stack, filename)

# === helper functions ===
# No helper functions needed for this simple iteration logic

# === OOP compatibility layer ===
# Not needed - this is a verification helper function, not a framework entry point

# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No direct child functions; _verify_node is imported lazily inside the function
# to avoid circular dependency (parent -> child -> parent cycle)

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 ("if_stmt")
#   "condition": dict,       # 条件表达式
#   "then_branch": dict,     # then 分支（语句块）
#   "else_branch": dict,     # else 分支（可选，可能为 None）
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

ContextStack = list
# ContextStack possible fields:
# [
#   {"type": "function", "name": str, "return_type": str},
#   {"type": "loop", "stmt_type": "while"|"for"}
# ]

# === main function ===
def _verify_if_stmt(node: dict, symbol_table: dict, context_stack: list, filename: str) -> None:
    """
    验证 if_stmt 节点。
    
    递归验证条件表达式、then_branch，若有 else_branch 也递归验证。
    验证失败时抛出 ValueError 异常。
    """
    # Lazy import to avoid circular dependency
    from ..._verify_node_package._verify_node_src import _verify_node
    
    # 验证条件表达式
    _verify_node(node['condition'], symbol_table, context_stack, filename)
    
    # 验证 then 分支
    _verify_node(node['then_branch'], symbol_table, context_stack, filename)
    
    # 验证 else 分支（如果存在）
    else_branch = node.get('else_branch')
    if else_branch is not None:
        _verify_node(else_branch, symbol_table, context_stack, filename)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this verification function

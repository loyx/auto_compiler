# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# Import parent dispatcher for recursive traversal
# Use lazy import inside function to avoid circular dependency

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,
#   "condition": AST,        # 条件表达式
#   "then_body": AST,        # then 分支
#   "else_body": AST,        # else 分支（可选）
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
def _handle_if_statement(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理 if_statement 节点。
    
    递归遍历 condition、then_body 和 else_body 节点。
    本函数不直接修改 symbol_table，而是通过递归调用触发其他 handler。
    """
    # Lazy import to avoid circular dependency
    from .._traverse_node_src import _traverse_node
    
    condition = node.get("condition")
    then_body = node.get("then_body")
    else_body = node.get("else_body")
    
    if condition is not None:
        _traverse_node(condition, symbol_table)
    
    if then_body is not None:
        _traverse_node(then_body, symbol_table)
    
    if else_body is not None:
        _traverse_node(else_body, symbol_table)

# === helper functions ===
# No helper functions needed for this simple handler

# === OOP compatibility layer ===
# Not needed - this is a handler function, not a framework entry point

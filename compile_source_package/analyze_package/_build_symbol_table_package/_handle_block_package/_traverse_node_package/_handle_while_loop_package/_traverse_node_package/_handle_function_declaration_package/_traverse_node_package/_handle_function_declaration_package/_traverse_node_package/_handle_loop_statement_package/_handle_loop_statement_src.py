# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from .._traverse_node_src import _traverse_node

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,
#   "condition": AST,
#   "body": AST,
#   "loop_type": str,
#   "line": int,
#   "column": int
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
def _handle_loop_statement(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理循环语句节点。
    
    输入：loop_statement 类型的 AST 节点和符号表
    处理：递归遍历循环条件和循环体
    副作用：不修改符号表，仅递归遍历子节点
    """
    condition = node.get("condition")
    body = node.get("body")
    
    if condition is not None:
        _traverse_node(condition, symbol_table)
    
    if body is not None:
        _traverse_node(body, symbol_table)

# === helper functions ===

# === OOP compatibility layer ===

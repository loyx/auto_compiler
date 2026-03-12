# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from .._traverse_node_package._traverse_node_src import _traverse_node

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
    """处理代码块节点，管理作用域的进入和退出。"""
    # 初始化 scope_stack 如果不存在
    if "scope_stack" not in symbol_table:
        symbol_table["scope_stack"] = []
    
    # 初始化 current_scope 如果不存在
    if "current_scope" not in symbol_table:
        symbol_table["current_scope"] = 0
    
    # 进入 block：增加 current_scope，压入 scope_stack
    symbol_table["current_scope"] += 1
    symbol_table["scope_stack"].append(symbol_table["current_scope"])
    
    # 遍历 block 的所有 children，对每个 child 调用 _traverse_node
    children = node.get("children", [])
    for child in children:
        _traverse_node(child, symbol_table)
    
    # 退出 block：从 scope_stack 弹出，恢复 current_scope
    symbol_table["scope_stack"].pop()
    if symbol_table["scope_stack"]:
        symbol_table["current_scope"] = symbol_table["scope_stack"][-1]
    else:
        symbol_table["current_scope"] = 0

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this function node

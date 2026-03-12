# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._traverse_node_package._traverse_node_src import _traverse_node

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (必填，永不为空)
#   "children": list,        # 子节点列表 (可选，默认 [])
#   "value": Any,            # 节点值 (可选)
#   "data_type": str,        # 类型信息 "int" 或 "char" (可选)
#   "line": int,             # 行号 (必填，最小为 0)
#   "column": int            # 列号 (必填，最小为 0)
# }

SymbolTable = Dict[str, Any]
# SymbolTable possible fields:
# {
#   "variables": Dict[str, Dict],  # var_name -> {data_type, is_declared, line, column, scope_level}
#   "functions": Dict[str, Dict],  # func_name -> {return_type, params, line, column}
#   "current_scope": int,          # 当前作用域层级
#   "scope_stack": list,           # 作用域栈 (存储旧 scope 值)
#   "current_function": str,       # 当前函数名 (可选)
#   "errors": list                 # 错误列表 (可选)
# }

# === main function ===
def _handle_block(node: AST, symbol_table: SymbolTable) -> None:
    """处理 block 代码块节点，管理作用域。"""
    # 进入 block：current_scope + 1 并压栈
    scope_stack = symbol_table.setdefault("scope_stack", [])
    scope_stack.append(symbol_table.get("current_scope", 0))
    symbol_table["current_scope"] = symbol_table.get("current_scope", 0) + 1
    
    # 递归遍历 block 的所有 children 节点
    for child in node.get("children", []):
        _traverse_node(child, symbol_table)
    
    # 退出 block：弹栈恢复之前的 current_scope
    if scope_stack:
        symbol_table["current_scope"] = scope_stack.pop()

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this function node

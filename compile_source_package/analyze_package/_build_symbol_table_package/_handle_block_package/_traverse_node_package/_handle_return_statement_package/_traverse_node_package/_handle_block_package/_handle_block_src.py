# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._traverse_node_package._traverse_node_src import _traverse_node

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "block")
#   "children": list,        # 子节点列表 (可选，默认 [])
#   "value": Any,            # 节点值
#   "data_type": str,        # 类型信息 ("int" 或 "char")
#   "line": int,             # 行号
#   "column": int            # 列号
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
    """
    处理 block 类型节点（代码块）。
    
    管理作用域：进入 block 时压栈并递增 current_scope，
    退出 block 时弹栈恢复。遍历子节点并委托给 _traverse_node。
    """
    # 进入 block：保存旧 scope 并递增
    old_scope = symbol_table.get("current_scope", 0)
    scope_stack = symbol_table.setdefault("scope_stack", [])
    scope_stack.append(old_scope)
    symbol_table["current_scope"] = old_scope + 1
    
    try:
        # 遍历子节点
        children = node.get("children", [])
        for child in children:
            _traverse_node(child, symbol_table)
    finally:
        # 退出 block：恢复旧 scope
        symbol_table["current_scope"] = scope_stack.pop()

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node

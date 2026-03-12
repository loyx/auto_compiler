# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# Deferred import to avoid circular dependency
# from ._traverse_node_package._traverse_node_src import _traverse_node

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "program", "function_declaration", "block" 等)
#   "children": list,        # 子节点列表
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
#   "scope_stack": list,           # 作用域栈
#   "current_function": str,       # 当前函数名 (可选)
#   "errors": list                 # 错误列表 (可选)
# }

# === main function ===
def _handle_program(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理 program 类型节点（AST 根节点）。
    
    遍历 program 的 children 并递归调用 _traverse_node 处理每个子节点。
    program 节点本身不修改 symbol_table，仅作为遍历入口。
    """
    # Deferred import to avoid circular dependency
    from ._traverse_node_package._traverse_node_src import _traverse_node
    
    children = node.get("children", [])
    for child in children:
        _traverse_node(child, symbol_table)

# === helper functions ===
# No helper functions needed for this simple traversal logic

# === OOP compatibility layer ===
# No OOP wrapper needed - this is a pure function node in the dependency tree

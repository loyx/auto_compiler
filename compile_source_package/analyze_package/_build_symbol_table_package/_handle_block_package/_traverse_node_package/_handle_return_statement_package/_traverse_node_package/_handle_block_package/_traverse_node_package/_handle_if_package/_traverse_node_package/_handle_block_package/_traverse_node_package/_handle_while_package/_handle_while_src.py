# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._traverse_node_package._traverse_node_src import _traverse_node

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 ("while", "if", "block", etc.)
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
def _handle_while(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理 while 循环节点。
    
    遍历 while 节点的所有子节点（condition 和 body），
    递归调用 _traverse_node 进行处理。
    
    注意：while 节点本身不创建新作用域，block 节点才会创建。
    """
    children = node.get("children", [])
    
    for child in children:
        _traverse_node(child, symbol_table)

# === helper functions ===
# No helper functions needed for this simple traversal logic

# === OOP compatibility layer ===
# Not needed - this is a helper function node, not a framework entry point

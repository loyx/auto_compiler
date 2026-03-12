# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# _traverse_node is the parent dispatcher function, import from parent module
# Import _traverse_node lazily to avoid circular import
# It will be imported inside the function when needed

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型
#   "children": list,        # 子节点列表
#   "value": Any,            # 节点值
#   "data_type": str,        # 类型信息 ("int" 或 "char")
#   "line": int,             # 行号
#   "column": int            # 列号
#   "condition": AST,        # while_loop 条件节点
#   "body": AST              # while_loop 循环体节点
# }

SymbolTable = Dict[str, Any]
# SymbolTable possible fields:
# {
#   "variables": Dict[str, Dict],  # var_name -> {data_type, is_declared, line, column, scope_level}
#   "functions": Dict[str, Dict],  # func_name -> {return_type, params, line, column}
#   "current_scope": int,          # 当前作用域层级
#   "scope_stack": list            # 作用域栈
# }

# === main function ===
def _handle_while_loop(node: AST, symbol_table: SymbolTable) -> None:
    """处理 while_loop 类型节点。遍历条件和循环体子节点。"""
    # Import _traverse_node lazily to avoid circular import
    from .._traverse_node_src import _traverse_node
    
    condition = node.get("condition")
    body = node.get("body")
    
    if condition is not None:
        _traverse_node(condition, symbol_table)
    
    if body is not None:
        _traverse_node(body, symbol_table)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node

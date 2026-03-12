# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._traverse_node_package._traverse_node_src import _traverse_node

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "while_loop")
#   "children": list,        # 子节点列表
#   "value": Any,            # 节点值
#   "data_type": str,        # 类型信息 ("int" 或 "char")
#   "line": int,             # 行号
#   "column": int            # 列号
#   "condition": Any,        # 循环条件表达式
#   "body": Any              # 循环体代码块
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
def _handle_while_loop(node: AST, symbol_table: SymbolTable) -> None:
    """处理 while_loop 类型节点（while 循环）。"""
    condition = node.get("condition")
    body = node.get("body")
    
    if condition is not None:
        _traverse_node(condition, symbol_table)
    
    if body is not None:
        _traverse_node(body, symbol_table)

# === helper functions ===

# === OOP compatibility layer ===

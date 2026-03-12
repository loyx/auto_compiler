# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._traverse_node_package._traverse_node_src import _traverse_node

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "block", "var_decl", "assignment", "if", "while", "function_call", etc.)
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
    
    管理作用域层级：进入 block 时提升 scope，退出时恢复。
    遍历 block 内所有子节点并递归处理。
    """
    # 初始化作用域相关字段（如果不存在）
    if "current_scope" not in symbol_table:
        symbol_table["current_scope"] = 0
    if "scope_stack" not in symbol_table:
        symbol_table["scope_stack"] = []
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    # 进入 block：提升作用域层级
    old_scope = symbol_table["current_scope"]
    symbol_table["scope_stack"].append(old_scope)
    symbol_table["current_scope"] += 1
    
    # 遍历并处理所有子节点
    children = node.get("children", [])
    for child in children:
        _traverse_node(child, symbol_table)
    
    # 退出 block：恢复作用域层级
    if symbol_table["scope_stack"]:
        symbol_table["current_scope"] = symbol_table["scope_stack"].pop()
    else:
        symbol_table["current_scope"] = 0

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not required for this function node

# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._traverse_node_package._traverse_node_src import _traverse_node

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "block", "var_decl", "assignment", "if", "while", etc.)
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
    """处理代码块节点：管理作用域并遍历块内所有语句。"""
    # 1. 进入新作用域
    old_scope = symbol_table.get("current_scope", 0)
    symbol_table["current_scope"] = old_scope + 1
    if "scope_stack" not in symbol_table:
        symbol_table["scope_stack"] = []
    symbol_table["scope_stack"].append(old_scope)
    
    # 2. 遍历并处理块内所有子节点
    children = node.get("children", [])
    for child_node in children:
        _traverse_node(child_node, symbol_table)
    
    # 3. 退出作用域（恢复之前的 scope）
    if symbol_table["scope_stack"]:
        previous_scope = symbol_table["scope_stack"].pop()
        symbol_table["current_scope"] = previous_scope

# === helper functions ===
# No helper functions needed; all logic is in main function

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node

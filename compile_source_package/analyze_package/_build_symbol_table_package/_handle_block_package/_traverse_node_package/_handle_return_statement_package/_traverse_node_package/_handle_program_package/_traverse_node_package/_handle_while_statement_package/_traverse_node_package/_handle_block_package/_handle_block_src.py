# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._traverse_node_package._traverse_node_src import _traverse_node

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
def _handle_block(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理 block 类型节点，管理作用域层级。
    
    处理逻辑：
    1. 进入新作用域：current_scope += 1，压入 scope_stack
    2. 遍历 block 的 children，递归处理每个语句
    3. 离开作用域：弹出 scope_stack，current_scope -= 1
    """
    # 进入新作用域
    symbol_table["current_scope"] += 1
    symbol_table["scope_stack"].append(symbol_table["current_scope"])
    
    # 遍历 block 中的所有子节点（语句）
    children = node.get("children", [])
    for child in children:
        _traverse_node(child, symbol_table)
    
    # 离开作用域
    symbol_table["scope_stack"].pop()
    symbol_table["current_scope"] -= 1

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
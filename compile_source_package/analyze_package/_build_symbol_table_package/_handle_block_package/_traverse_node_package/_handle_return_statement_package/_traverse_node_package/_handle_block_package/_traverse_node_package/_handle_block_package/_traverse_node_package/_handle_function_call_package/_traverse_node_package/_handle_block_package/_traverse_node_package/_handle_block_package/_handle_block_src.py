# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._dispatch_node_package._dispatch_node_src import _dispatch_node

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
    """处理 block 节点：进入新作用域，遍历子节点，退出作用域。"""
    # 1. 保存当前作用域层级
    old_scope = symbol_table.get("current_scope", 0)
    
    # 2. 进入新作用域（scope + 1）
    symbol_table["current_scope"] = old_scope + 1
    
    # 3. 初始化 scope_stack（如果不存在）
    if "scope_stack" not in symbol_table:
        symbol_table["scope_stack"] = []
    symbol_table["scope_stack"].append(old_scope)
    
    # 4. 遍历子节点并调用调度器
    children = node.get("children", [])
    for child in children:
        _dispatch_node(child, symbol_table)
    
    # 5. 退出作用域（恢复旧 scope）
    symbol_table["current_scope"] = symbol_table["scope_stack"].pop()

# === helper functions ===
# No helper functions needed for this simple scope management logic

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
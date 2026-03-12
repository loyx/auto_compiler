# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions needed for this module

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
    """
    处理 block 类型节点，管理作用域的进入和退出。
    
    处理步骤：
    1. 进入 block 时，将当前 scope 压入 scope_stack
    2. 增加 current_scope 层级（+1）
    3. block 处理完成后，恢复之前的 scope 层级
    
    副作用：
    - 修改 symbol_table["current_scope"]
    - 修改 symbol_table["scope_stack"]
    
    注意：
    - block 节点本身不直接处理子节点，子节点由 _traverse_node 递归处理
    - 此函数只负责作用域管理
    """
    # 进入 block：保存当前作用域层级
    current_scope = symbol_table.get("current_scope", 0)
    scope_stack = symbol_table.get("scope_stack", [])
    
    # 将当前 scope 压入栈
    scope_stack.append(current_scope)
    symbol_table["scope_stack"] = scope_stack
    
    # 增加作用域层级
    symbol_table["current_scope"] = current_scope + 1

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this function node
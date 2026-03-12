# === std / third-party imports ===
from typing import Any, Callable, Dict

# === sub function imports ===
# No sub functions - traverse_fn is passed as parameter

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
def _handle_block(node: AST, symbol_table: SymbolTable, traverse_fn: Callable[[AST, SymbolTable], None]) -> None:
    """
    处理 block 类型节点。
    
    遍历 block 内所有子节点并递归调用 traverse_fn。
    block 本身不改变作用域，作用域管理由 if/while/function_decl 等节点处理。
    错误由子节点处理并记录到 symbol_table['errors']。
    """
    children = node.get("children", [])
    for child_node in children:
        traverse_fn(child_node, symbol_table)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not required for this function node

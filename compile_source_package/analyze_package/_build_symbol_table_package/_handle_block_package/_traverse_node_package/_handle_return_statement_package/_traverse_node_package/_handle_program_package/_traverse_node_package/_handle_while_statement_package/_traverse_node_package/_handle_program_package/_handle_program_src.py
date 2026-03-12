# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed

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
    处理 program 类型节点（AST 的根节点）。
    
    负责初始化符号表的基本结构，作为 AST 遍历的入口点。
    不直接递归子节点，由 _traverse_node 负责遍历。
    """
    # 初始化符号表作用域
    symbol_table["current_scope"] = 0
    symbol_table["scope_stack"] = [0]
    
    # 初始化 variables 和 functions 字典（如果不存在）
    if "variables" not in symbol_table:
        symbol_table["variables"] = {}
    
    if "functions" not in symbol_table:
        symbol_table["functions"] = {}
    
    # 初始化 errors 列表（如果不存在）
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    # 注意：不在此处遍历 children，由 _traverse_node 负责


# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this function node

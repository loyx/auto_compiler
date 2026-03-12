# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub-functions needed for this initialization logic

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型
#   "children": list,        # 子节点列表
#   "value": Any,            # 节点值
#   "data_type": str,        # 类型信息
#   "line": int,             # 行号
#   "column": int            # 列号
# }

SymbolTable = Dict[str, Any]
# SymbolTable possible fields:
# {
#   "variables": Dict[str, Dict],
#   "functions": Dict[str, Dict],
#   "current_scope": int,
#   "scope_stack": list,
#   "current_function": str,
#   "errors": list
# }

# === main function ===
def _handle_program(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理 program 根节点，初始化符号表。
    
    初始化 symbol_table 的作用域栈和基础字段，为后续 AST 遍历做准备。
    不递归处理子节点，由 _traverse_node 自动处理。
    """
    # 初始化作用域栈
    symbol_table["scope_stack"] = [0]
    symbol_table["current_scope"] = 0
    
    # 初始化 variables（如果未存在）
    if "variables" not in symbol_table:
        symbol_table["variables"] = {}
    
    # 初始化 functions（如果未存在）
    if "functions" not in symbol_table:
        symbol_table["functions"] = {}
    
    # 初始化 errors（如果未存在）
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    # 初始化 current_function（如果未存在）
    if "current_function" not in symbol_table:
        symbol_table["current_function"] = ""

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for internal AST traversal function

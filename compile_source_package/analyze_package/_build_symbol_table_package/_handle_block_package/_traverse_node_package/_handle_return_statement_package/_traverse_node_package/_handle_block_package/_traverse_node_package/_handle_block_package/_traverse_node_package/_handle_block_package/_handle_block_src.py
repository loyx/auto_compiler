# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from .._traverse_node import _traverse_node

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
    """处理 block 类型节点（代码块）。
    
    处理逻辑：
    1. 初始化作用域字段（如果不存在）
    2. 进入新作用域：保存当前 scope 到 stack，current_scope + 1
    3. 遍历子节点，调用 _traverse_node 递归处理
    4. 退出作用域：从 stack 恢复 current_scope
    
    副作用：修改 symbol_table 中的作用域信息，可能添加错误记录
    """
    # 初始化作用域字段（如果不存在）
    if "current_scope" not in symbol_table:
        symbol_table["current_scope"] = 0
    if "scope_stack" not in symbol_table:
        symbol_table["scope_stack"] = []
    
    # 初始化 errors 列表（如果不存在）
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    # Enter scope: 保存旧 scope，进入新层级
    old_scope = symbol_table["current_scope"]
    symbol_table["scope_stack"].append(old_scope)
    symbol_table["current_scope"] = old_scope + 1
    
    try:
        # 遍历子节点
        children = node.get("children", [])
        for child in children:
            _traverse_node(child, symbol_table)
    finally:
        # Exit scope: 恢复旧 scope（即使有错误也要执行）
        if symbol_table["scope_stack"]:
            symbol_table["current_scope"] = symbol_table["scope_stack"].pop()

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
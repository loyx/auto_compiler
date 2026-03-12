# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub function imports at module level to avoid circular dependency.
# _traverse_node will be imported inside the function.

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
def _handle_while(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理 while 循环节点。
    
    处理行为：
    1. 进入新的作用域（循环体作用域）
    2. 递归处理条件表达式
    3. 递归处理循环体
    4. 退出作用域
    """
    # 函数内部 import，避免循环依赖
    from ._traverse_node_src import _traverse_node
    
    # 初始化 symbol_table 必要字段（如果不存在）
    if "scope_stack" not in symbol_table:
        symbol_table["scope_stack"] = []
    if "current_scope" not in symbol_table:
        symbol_table["current_scope"] = 0
    
    # 进入作用域：保存当前 scope 到栈中，并递增
    symbol_table["scope_stack"].append(symbol_table["current_scope"])
    symbol_table["current_scope"] += 1
    
    # 处理子节点
    children = node.get("children", [])
    
    # children[0] = 条件表达式
    if len(children) >= 1:
        _traverse_node(children[0], symbol_table)
    
    # children[1] = 循环体
    if len(children) >= 2:
        _traverse_node(children[1], symbol_table)
    
    # 退出作用域：从栈中恢复上一个 scope 值
    if symbol_table["scope_stack"]:
        symbol_table["current_scope"] = symbol_table["scope_stack"].pop()

# === helper functions ===
# No helper functions needed.

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node.

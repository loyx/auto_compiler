# === std / third-party imports ===
from typing import Any, Dict

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
    处理 block 节点：管理作用域的进入和退出。
    
    处理逻辑：
    1. 进入 block 作用域：current_scope + 1, push scope_stack
    2. 递归遍历子节点
    3. 退出 block 作用域：current_scope - 1, pop scope_stack
    """
    # 延迟导入以避免循环依赖
    from ._traverse_node_package._traverse_node_src import _traverse_node
    
    # 进入 block 作用域
    symbol_table["current_scope"] += 1
    line = node.get("line", 0)
    scope_id = f"block_{line}"
    symbol_table["scope_stack"].append(scope_id)
    
    try:
        # 递归遍历 block 中的所有子节点
        children = node.get("children", [])
        for child in children:
            _traverse_node(child, symbol_table)
    finally:
        # 退出 block 作用域（确保一定执行）
        symbol_table["current_scope"] -= 1
        symbol_table["scope_stack"].pop()

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this function node
# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# Note: Import _traverse_node inside the function to avoid circular import

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
    处理代码块节点。管理作用域（进入/退出），遍历子节点。
    
    输入：block 类型 AST 节点和符号表。
    副作用：修改 symbol_table['current_scope'] 和 scope_stack，可能记录错误。
    不抛出异常。
    """
    # 进入新作用域
    old_scope = symbol_table.get("current_scope", 0)
    symbol_table.setdefault("scope_stack", []).append(old_scope)
    symbol_table["current_scope"] = old_scope + 1
    
    # 遍历 block 的所有子节点（语句列表）
    # Import here to avoid circular import
    from ._traverse_node_package._traverse_node_src import _traverse_node
    
    children = node.get("children", [])
    for child_node in children:
        _traverse_node(child_node, symbol_table)
    
    # 退出作用域：从 scope_stack 弹出并恢复 current_scope
    scope_stack = symbol_table.get("scope_stack", [])
    if scope_stack:
        symbol_table["current_scope"] = scope_stack.pop()


# === helper functions ===
# No helper functions needed for this simple scope management logic

# === OOP compatibility layer ===
# No OOP wrapper needed - this is a helper function, not a framework entry point

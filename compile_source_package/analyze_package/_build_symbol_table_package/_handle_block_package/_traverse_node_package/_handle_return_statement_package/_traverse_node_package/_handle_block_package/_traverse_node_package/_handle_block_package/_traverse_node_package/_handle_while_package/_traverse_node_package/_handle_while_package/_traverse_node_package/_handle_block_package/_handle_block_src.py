# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._traverse_node_package._traverse_node_src import _traverse_node

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
    Handle block-type AST node with scope management.
    
    Process:
    1. Enter new scope: push current_scope to stack, increment current_scope
    2. Traverse all children nodes
    3. Exit scope: pop from stack, restore current_scope
    """
    # Enter new scope
    old_scope = symbol_table.get("current_scope", 0)
    scope_stack = symbol_table.setdefault("scope_stack", [])
    scope_stack.append(old_scope)
    symbol_table["current_scope"] = old_scope + 1
    
    # Process all children statements
    children = node.get("children", [])
    for child in children:
        _traverse_node(child, symbol_table)
    
    # Exit scope: restore previous scope level
    if scope_stack:
        symbol_table["current_scope"] = scope_stack.pop()

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this internal compiler function

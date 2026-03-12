# === std / third-party imports ===
from typing import Any, Callable, Dict

# === sub function imports ===
# No child functions - traverse_fn is injected via dependency injection

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
def _handle_if(node: AST, symbol_table: SymbolTable, traverse_fn: Callable[[AST, SymbolTable], None]) -> None:
    """
    Handle if-type AST nodes with scope management.
    
    Enters a new scope, traverses all child nodes (condition, then-branch, else-branch),
    then exits the scope. Errors are recorded to symbol_table['errors'] by child handlers.
    """
    # Enter new scope
    old_scope = symbol_table.get("current_scope", 0)
    if "scope_stack" not in symbol_table:
        symbol_table["scope_stack"] = []
    symbol_table["scope_stack"].append(old_scope)
    symbol_table["current_scope"] = old_scope + 1
    
    # Traverse all child nodes (condition, then-block, else-block if present)
    children = node.get("children", [])
    for child_node in children:
        traverse_fn(child_node, symbol_table)
    
    # Exit scope, restore previous scope level
    if symbol_table["scope_stack"]:
        symbol_table["current_scope"] = symbol_table["scope_stack"].pop()

# === helper functions ===
# No helper functions needed - logic is straightforward

# === OOP compatibility layer ===
# Not required - this is a handler function, not a framework entry point

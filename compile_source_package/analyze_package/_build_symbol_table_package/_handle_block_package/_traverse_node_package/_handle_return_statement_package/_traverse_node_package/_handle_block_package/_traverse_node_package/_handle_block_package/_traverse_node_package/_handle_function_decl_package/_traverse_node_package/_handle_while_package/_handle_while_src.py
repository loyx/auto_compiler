# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._inline_traverse_package._inline_traverse_src import _inline_traverse

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
    Handle while loop AST node.
    Manages scope and recursively processes condition and body.
    All errors are recorded in symbol_table["errors"].
    """
    # 1. Initialize errors list if not present
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    # 2. Enter new scope for while loop
    symbol_table["current_scope"] = symbol_table.get("current_scope", 0) + 1
    
    # 3. Get children
    children = node.get("children", [])
    
    # 4. Validate children structure (must have condition and body)
    if len(children) < 2:
        symbol_table["errors"].append({
            "message": "While node must have condition and body",
            "line": node.get("line", 0),
            "column": node.get("column", 0),
            "severity": "error"
        })
        # Exit scope
        symbol_table["current_scope"] -= 1
        return
    
    # 5. Process condition expression (children[0])
    _inline_traverse(children[0], symbol_table)
    
    # 6. Process loop body (children[1])
    _inline_traverse(children[1], symbol_table)
    
    # 7. Exit scope
    symbol_table["current_scope"] -= 1

# === helper functions ===
# No helper functions in this file; delegated to _inline_traverse

# === OOP compatibility layer ===
# No OOP wrapper needed; this is a helper function node

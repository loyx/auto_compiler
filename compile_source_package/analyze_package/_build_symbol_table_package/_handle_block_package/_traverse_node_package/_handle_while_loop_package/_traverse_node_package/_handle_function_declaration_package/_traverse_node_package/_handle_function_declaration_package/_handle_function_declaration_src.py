# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# Note: Import _traverse_node inside the function to avoid circular import

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,
#   "name": str,
#   "params": list,
#   "body": AST,
#   "return_type": str,
#   "line": int,
#   "column": int
# }

SymbolTable = Dict[str, Any]
# SymbolTable possible fields:
# {
#   "variables": Dict[str, Dict],
#   "functions": Dict[str, Dict],
#   "current_scope": int,
#   "scope_stack": list
# }

# === main function ===
def _handle_function_declaration(node: AST, symbol_table: SymbolTable) -> None:
    """处理函数声明节点，将函数信息注册到符号表中。"""
    func_name = node["name"]
    params = node["params"]
    return_type = node["return_type"]
    line = node["line"]
    column = node["column"]
    
    symbol_table["functions"][func_name] = {
        "return_type": return_type,
        "params": params,
        "line": line,
        "column": column
    }
    
    if "body" in node and node["body"] is not None:
        _traverse_node(node["body"], symbol_table)

# === helper functions ===

# === OOP compatibility layer ===

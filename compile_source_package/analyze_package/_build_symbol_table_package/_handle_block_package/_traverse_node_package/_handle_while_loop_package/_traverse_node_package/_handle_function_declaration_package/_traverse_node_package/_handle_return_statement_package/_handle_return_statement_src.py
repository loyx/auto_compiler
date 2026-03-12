# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._traverse_node_package._traverse_node_src import _traverse_node

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,
#   "name": str,             # 函数名
#   "params": list,          # 参数列表
#   "body": AST,             # 函数体
#   "return_type": str,      # 返回类型
#   "line": int,
#   "column": int
# }

SymbolTable = Dict[str, Any]
# SymbolTable possible fields:
# {
#   "variables": Dict[str, Dict],
#   "functions": Dict[str, Dict],  # func_name -> {return_type, params, line, column}
#   "current_scope": int,
#   "scope_stack": list
# }

# === main function ===
def _handle_return_statement(node: AST, symbol_table: SymbolTable) -> None:
    """
    Handle return statement node by traversing the return value expression.
    
    Args:
        node: AST node of type return_statement, contains "value" (optional), "line", "column"
        symbol_table: Symbol table that may be modified during traversal
    """
    value = node.get("value")
    if value is not None:
        _traverse_node(value, symbol_table)

# === helper functions ===
# (none needed)

# === OOP compatibility layer ===
# (not needed for this function node)

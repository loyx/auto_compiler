# === std / third-party imports ===
from typing import Any, Dict

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,
#   "children": list,
#   "value": Any,
#   "data_type": str,
#   "line": int,
#   "column": int
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
def _handle_expression(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理 expression 节点：递归遍历表达式子节点，进行类型检查。
    """
    # 延迟导入以避免循环导入
    from ._traverse_node_package._traverse_node_src import _traverse_node
    from ._check_expression_types_package._check_expression_types_src import _check_expression_types
    
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    children = node.get("children", [])
    
    for child in children:
        _traverse_node(child, symbol_table)
    
    _check_expression_types(node, symbol_table)

# === helper functions ===
# No helper functions - delegated to sub functions

# === OOP compatibility layer ===
# No OOP wrapper needed

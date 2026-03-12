# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# Lazy import to avoid circular dependency
_traverse_node = None

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
def _handle_function_declaration(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理 function_declaration 节点，在 symbol_table 中注册函数信息。
    
    副作用：修改 symbol_table["functions"] 和 symbol_table（通过递归遍历）
    """
    # 从 node 中提取字段
    func_name = node.get("name")
    return_type = node.get("return_type")
    params = node.get("params")
    line = node.get("line")
    column = node.get("column")
    body = node.get("body")
    
    # 如果 func_name 不为 None 且 symbol_table 包含 "functions" 键，注册函数信息
    if func_name is not None and "functions" in symbol_table:
        symbol_table["functions"][func_name] = {
            "return_type": return_type,
            "params": params,
            "line": line,
            "column": column
        }
    
    # 如果 body 字段不为 None，递归遍历函数体
    if body is not None:
        # Lazy import to avoid circular dependency
        from .._traverse_node_src import _traverse_node
        _traverse_node(body, symbol_table)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this function node
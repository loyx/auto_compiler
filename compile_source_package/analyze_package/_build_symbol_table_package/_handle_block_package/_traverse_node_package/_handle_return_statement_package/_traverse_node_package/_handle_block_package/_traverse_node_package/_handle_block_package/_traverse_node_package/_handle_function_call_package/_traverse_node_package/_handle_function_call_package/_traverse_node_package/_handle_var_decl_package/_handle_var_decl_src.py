# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions needed for this simple logic

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
#   "variables": Dict[str, Dict],  # var_name -> {data_type, is_declared, line, column, scope_level}
#   "functions": Dict[str, Dict],
#   "current_scope": int,
#   "scope_stack": list,
#   "current_function": str,
#   "errors": list
# }


# === main function ===
def _handle_var_decl(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理变量声明节点。验证变量未在当前作用域重复声明，然后添加到 symbol_table["variables"]。
    
    副作用：
    - 修改 symbol_table["variables"]
    - 可能向 symbol_table["errors"] 添加错误
    """
    var_name = node.get("value")
    data_type = node.get("data_type")
    line = node.get("line", 0)
    column = node.get("column", 0)
    current_scope = symbol_table.get("current_scope", 0)
    
    # 检查变量是否已存在
    if var_name in symbol_table.get("variables", {}):
        existing_var = symbol_table["variables"][var_name]
        # 如果在同一作用域已声明，记录错误
        if existing_var.get("scope_level") == current_scope:
            error_msg = f"Variable '{var_name}' already declared"
            symbol_table.setdefault("errors", []).append({
                "message": error_msg,
                "line": line,
                "column": column
            })
            return
    
    # 添加变量到符号表
    symbol_table.setdefault("variables", {})[var_name] = {
        "data_type": data_type,
        "is_declared": True,
        "line": line,
        "column": column,
        "scope_level": current_scope
    }


# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this function node

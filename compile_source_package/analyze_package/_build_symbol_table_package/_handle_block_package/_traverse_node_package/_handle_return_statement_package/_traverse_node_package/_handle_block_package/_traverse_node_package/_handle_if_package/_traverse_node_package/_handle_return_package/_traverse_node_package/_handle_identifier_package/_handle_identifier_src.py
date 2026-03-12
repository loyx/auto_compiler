# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 ("identifier" 或 "variable")
#   "name": str,             # 变量名
#   "line": int,             # 行号
#   "column": int            # 列号
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
def _handle_identifier(node: AST, symbol_table: SymbolTable) -> str:
    """
    处理标识符/变量节点，查找变量类型。
    
    在 symbol_table["variables"] 中查找变量：
    - 如果找到，返回变量的 data_type
    - 如果未找到，记录错误并返回 "void"
    """
    var_name = node["name"]
    variables = symbol_table.get("variables", {})
    
    if var_name in variables:
        var_info = variables[var_name]
        return var_info.get("data_type", "void")
    else:
        # 变量未定义，记录错误
        line = node.get("line", 0)
        error_msg = f"undefined variable '{var_name}' at line {line}"
        
        # 确保 errors 列表存在
        if "errors" not in symbol_table:
            symbol_table["errors"] = []
        symbol_table["errors"].append(error_msg)
        
        return "void"


# === helper functions ===

# === OOP compatibility layer ===

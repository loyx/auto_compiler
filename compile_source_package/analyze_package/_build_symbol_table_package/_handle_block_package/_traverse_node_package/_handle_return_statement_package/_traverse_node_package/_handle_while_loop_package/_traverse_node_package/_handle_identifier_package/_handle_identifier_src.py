# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions delegated

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型，值为 "identifier"
#   "name": str,             # 变量名
#   "line": int,             # 行号
#   "column": int,           # 列号
# }

SymbolTable = Dict[str, Any]
# SymbolTable possible fields:
# {
#   "variables": Dict[str, Dict],  # var_name -> {data_type, is_declared, line, column, scope_level}
#   "functions": Dict[str, Dict],
#   "current_scope": int,
#   "scope_stack": list,
#   "current_function": str,
#   "errors": list                 # 错误列表
# }

# === main function ===
def _handle_identifier(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理 identifier 类型节点，检查变量是否已在符号表中声明。
    
    如果变量未声明，记录错误到 symbol_table["errors"]。
    如果变量已声明，不做任何操作。
    不抛异常，不自动添加变量。
    """
    var_name = node.get("name")
    line = node.get("line")
    column = node.get("column")
    
    variables = symbol_table.get("variables", {})
    
    if var_name not in variables:
        errors = symbol_table.get("errors")
        if errors is None:
            errors = []
            symbol_table["errors"] = errors
        
        errors.append({
            "error_type": "undeclared_variable",
            "var_name": var_name,
            "line": line,
            "column": column,
            "message": f"Variable '{var_name}' used before declaration"
        })

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not required for this function node
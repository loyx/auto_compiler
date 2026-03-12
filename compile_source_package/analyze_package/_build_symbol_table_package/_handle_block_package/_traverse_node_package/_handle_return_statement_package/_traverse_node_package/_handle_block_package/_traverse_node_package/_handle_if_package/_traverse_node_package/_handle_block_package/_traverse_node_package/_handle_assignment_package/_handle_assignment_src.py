# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed for this simple validation logic

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 ("assignment")
#   "children": list,        # 子节点列表 (可选，默认 [])
#   "value": Any,            # 节点值（变量名）
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
def _handle_assignment(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理赋值语句节点：检查变量是否已声明，验证类型匹配。
    副作用：可能修改 symbol_table['errors']。
    """
    # 从 node 提取信息
    var_name = node.get("value")
    data_type = node.get("data_type")
    line = node.get("line", 0)
    column = node.get("column", 0)
    
    # 确保 symbol_table["variables"] 存在
    if "variables" not in symbol_table:
        symbol_table["variables"] = {}
    
    # 确保 symbol_table["errors"] 存在
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    variables = symbol_table["variables"]
    errors = symbol_table["errors"]
    
    # 检查变量是否已声明
    if var_name not in variables:
        errors.append({
            "type": "undefined_variable",
            "line": line,
            "column": column,
            "message": f"Variable '{var_name}' used before declaration"
        })
        return
    
    # 变量已声明，验证类型匹配
    declared_type = variables[var_name].get("data_type")
    if declared_type != data_type:
        errors.append({
            "type": "type_mismatch",
            "line": line,
            "column": column,
            "message": f"Type mismatch for variable '{var_name}': expected {declared_type}, got {data_type}"
        })

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this function node
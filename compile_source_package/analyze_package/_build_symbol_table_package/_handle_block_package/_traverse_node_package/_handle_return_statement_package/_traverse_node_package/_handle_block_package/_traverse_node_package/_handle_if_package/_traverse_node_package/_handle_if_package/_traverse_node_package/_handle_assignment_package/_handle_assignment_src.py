# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No subfunctions required for this module

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (必填，永不为空)
#   "children": list,        # 子节点列表 (可选，默认 [])
#   "value": Any,            # 节点值 (可选)
#   "data_type": str,        # 类型信息 "int" 或 "char" (可选)
#   "line": int,             # 行号 (必填，最小为 0)
#   "column": int            # 列号 (必填，最小为 0)
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
    处理变量赋值节点。检查变量是否已声明，记录赋值信息。
    副作用：可能修改 symbol_table 中的 errors 列表。
    """
    var_name = node.get("value")
    line = node.get("line", 0)
    column = node.get("column", 0)
    variables = symbol_table.get("variables", {})
    
    # 检查变量是否已声明
    if var_name not in variables:
        symbol_table.setdefault("errors", []).append({
            "type": "undeclared_variable",
            "message": f"变量 '{var_name}' 未声明",
            "line": line,
            "column": column
        })
        return
    
    # 可选：类型检查
    declared_type = variables[var_name].get("data_type")
    assigned_type = node.get("data_type")
    if assigned_type and declared_type and assigned_type != declared_type:
        symbol_table.setdefault("errors", []).append({
            "type": "type_mismatch",
            "message": f"类型不匹配：'{var_name}' 声明为 {declared_type}，赋值为 {assigned_type}",
            "line": line,
            "column": column
        })

# === helper functions ===
# No helper functions required

# === OOP compatibility layer ===
# Not required for this function node
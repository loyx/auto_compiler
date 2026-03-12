# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No subfunctions delegated

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "block", "var_decl", "assignment", "if", "while", "function_call", etc.)
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
def _handle_assignment(node: AST, symbol_table: SymbolTable) -> None:
    """
    处理赋值语句节点，验证变量是否已声明并检查类型匹配。
    
    副作用：可能向 symbol_table["errors"] 添加错误信息
    """
    var_name = node.get("value")
    line = node.get("line", 0)
    column = node.get("column", 0)
    assigned_type = node.get("data_type")
    
    variables = symbol_table.get("variables", {})
    errors = symbol_table.setdefault("errors", [])
    
    if var_name not in variables:
        errors.append(f"Variable '{var_name}' not declared at line {line}, column {column}")
        return
    
    var_info = variables[var_name]
    declared_type = var_info.get("data_type")
    
    if declared_type and assigned_type and declared_type != assigned_type:
        errors.append(f"Type mismatch for '{var_name}' at line {line}, column {column}")

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not required for this semantic analysis function
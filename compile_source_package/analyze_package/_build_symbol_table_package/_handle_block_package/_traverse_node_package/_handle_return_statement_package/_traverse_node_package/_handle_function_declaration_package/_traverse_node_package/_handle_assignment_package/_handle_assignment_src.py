# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions needed for this simple validation logic

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型
#   "children": list,        # 子节点列表
#   "value": Any,            # 节点值
#   "data_type": str,        # 类型信息 ("int" 或 "char")
#   "line": int,             # 行号
#   "column": int            # 列号
#   "name": str,             # 变量名或函数名
# }

SymbolTable = Dict[str, Any]
# SymbolTable possible fields:
# {
#   "variables": Dict[str, Dict],  # var_name -> {data_type, is_declared, line, column, scope_level}
#   "functions": Dict[str, Dict],  # func_name -> {return_type, params, line, column}
#   "current_scope": int,          # 当前作用域层级
#   "scope_stack": list,           # 作用域栈
#   "current_function": str,       # 当前函数名 (可选)
#   "errors": list                 # 错误列表 (List[str])
# }


# === main function ===
def _handle_assignment(node: AST, symbol_table: SymbolTable) -> None:
    """
    Handle assignment nodes by validating that the variable being assigned has been declared.
    
    Modifies symbol_table in-place by appending errors if variable is undeclared.
    """
    # Extract variable name from node
    var_name = node.get("value") or node.get("name")
    
    # Extract location information
    line = node.get("line", 0)
    column = node.get("column", 0)
    
    # Ensure variables dict exists in symbol_table
    if "variables" not in symbol_table:
        symbol_table["variables"] = {}
    
    # Ensure errors list exists in symbol_table
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    # Check if variable is declared
    variables = symbol_table["variables"]
    if var_name not in variables:
        # Variable not declared, add error
        error_msg = f"Error: Variable '{var_name}' used without declaration at line {line}, column {column}"
        symbol_table["errors"].append(error_msg)
    # If variable exists, it's already declared - no action needed


# === helper functions ===
# No helper functions needed for this simple logic

# === OOP compatibility layer ===
# No OOP wrapper needed - this is a helper function node, not a framework entry point

# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions needed for this simple validation logic

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "block", "var_decl", "assignment", "if", "while", etc.)
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
    Handle assignment statement node.
    
    Validates that the variable being assigned to has been declared.
    Records errors to symbol_table['errors'] if variable is undeclared.
    Does not throw exceptions; all errors are collected in the symbol table.
    """
    # Extract variable name from node value
    var_name = node.get("value")
    line = node.get("line", -1)
    column = node.get("column", -1)
    
    # Ensure variables dict exists in symbol_table
    if "variables" not in symbol_table:
        symbol_table["variables"] = {}
    
    # Ensure errors list exists in symbol_table
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    # Check if variable is declared
    variables = symbol_table["variables"]
    
    if var_name not in variables:
        # Variable not declared - record error
        error = {
            "type": "error",
            "message": f"Variable '{var_name}' used before declaration",
            "line": line,
            "column": column
        }
        symbol_table["errors"].append(error)
    else:
        # Variable is declared - optionally update assignment position
        # This can track where the variable was last assigned
        variables[var_name]["last_assignment_line"] = line
        variables[var_name]["last_assignment_column"] = column

# === helper functions ===
# No helper functions needed for this straightforward logic

# === OOP compatibility layer ===
# Not needed - this is a helper function for semantic analysis, not a framework entry point

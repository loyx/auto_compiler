# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed

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
def _handle_var_decl(node: AST, symbol_table: SymbolTable) -> None:
    """
    Handle variable declaration nodes.
    
    Process var_decl type nodes by extracting variable name, data type,
    and position information, then record in symbol table or report
    duplicate declaration errors.
    
    Side effects:
    - Modifies symbol_table["variables"]
    - May append errors to symbol_table["errors"]
    """
    # Extract variable info from node
    var_name = node.get("value")
    data_type = node.get("data_type")
    line = node.get("line", 0)
    column = node.get("column", 0)
    
    # Ensure symbol_table["variables"] exists
    if "variables" not in symbol_table:
        symbol_table["variables"] = {}
    
    # Ensure symbol_table["errors"] exists
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    # Get current scope level
    current_scope = symbol_table.get("current_scope", 0)
    
    # Check for duplicate declaration
    if var_name in symbol_table["variables"]:
        # Record duplicate declaration error
        error = {
            "line": line,
            "column": column,
            "message": f"duplicate variable declaration: {var_name}"
        }
        symbol_table["errors"].append(error)
    else:
        # Add new variable to symbol table
        symbol_table["variables"][var_name] = {
            "data_type": data_type,
            "is_declared": True,
            "line": line,
            "column": column,
            "scope_level": current_scope
        }

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this helper function
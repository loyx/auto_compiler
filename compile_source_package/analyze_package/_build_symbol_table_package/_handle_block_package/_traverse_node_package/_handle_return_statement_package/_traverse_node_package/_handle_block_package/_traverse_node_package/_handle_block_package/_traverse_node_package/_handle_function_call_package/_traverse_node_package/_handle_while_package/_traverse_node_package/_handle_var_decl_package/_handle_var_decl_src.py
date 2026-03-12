# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed for this simple logic

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
def _handle_var_decl(node: AST, symbol_table: SymbolTable) -> None:
    """
    Handle variable declaration node: check for duplicate declaration and record to symbol table.
    
    Side effects:
    - Modifies symbol_table["variables"]
    - May append error to symbol_table["errors"]
    """
    # Extract information from node
    var_name = node.get("value")
    data_type = node.get("data_type")
    line = node.get("line")
    column = node.get("column")
    current_scope = symbol_table.get("current_scope", 0)
    
    # Initialize errors list if not present
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    # Check if variable already exists
    if "variables" not in symbol_table:
        symbol_table["variables"] = {}
    
    existing_var = symbol_table["variables"].get(var_name)
    
    if existing_var is not None and existing_var.get("is_declared", False):
        # Same scope duplicate declaration is an error
        if existing_var.get("scope_level") == current_scope:
            error_msg = f"Variable '{var_name}' already declared"
            symbol_table["errors"].append({
                "message": error_msg,
                "line": line,
                "column": column,
                "var_name": var_name
            })
        # Different scope: allow shadowing, will be handled by scope management
        # Just update the variable entry for the new scope
        symbol_table["variables"][var_name] = {
            "data_type": data_type,
            "is_declared": True,
            "line": line,
            "column": column,
            "scope_level": current_scope
        }
    else:
        # Variable doesn't exist or not yet declared, add it
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
# Not needed for this function node
# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # 节点类型 (如 "program", "function_declaration", "block" 等)
#   "children": list,        # 子节点列表
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
#   "scope_stack": list,           # 作用域栈
#   "current_function": str,       # 当前函数名 (可选)
#   "errors": list                 # 错误列表 (可选)
# }

# === main function ===
def _handle_variable_declaration(node: AST, symbol_table: SymbolTable) -> None:
    """
    Handle variable_declaration AST nodes and register variables in the symbol table.
    
    Args:
        node: AST node with type='variable_declaration'
        symbol_table: Symbol table to register the variable
    
    Side effects:
        - Updates symbol_table['variables'] with new variable info
        - May append errors to symbol_table['errors'] if duplicate declaration
    """
    # Extract variable information from the node
    var_name = node.get("value") or node.get("name")
    data_type = node.get("data_type")
    line = node.get("line", 0)
    column = node.get("column", 0)
    current_scope = symbol_table.get("current_scope", 0)
    
    # Validate variable name
    if not var_name:
        _add_error(symbol_table, line, "Variable name missing in declaration")
        return
    
    # Validate data type
    if data_type not in ("int", "char"):
        _add_error(symbol_table, line, f"Invalid data type '{data_type}' for variable '{var_name}'")
        return
    
    # Initialize variables dict if not exists
    if "variables" not in symbol_table:
        symbol_table["variables"] = {}
    
    # Check for duplicate declaration in current scope
    if var_name in symbol_table["variables"]:
        existing_var = symbol_table["variables"][var_name]
        if existing_var.get("scope_level") == current_scope:
            _add_error(symbol_table, line, f"Variable '{var_name}' already declared in current scope")
            return
    
    # Register variable in symbol table
    symbol_table["variables"][var_name] = {
        "data_type": data_type,
        "is_declared": True,
        "line": line,
        "column": column,
        "scope_level": current_scope
    }

# === helper functions ===
def _add_error(symbol_table: SymbolTable, line: int, message: str) -> None:
    """
    Add an error message to the symbol table's errors list.
    
    Args:
        symbol_table: Symbol table to add error to
        line: Line number where error occurred
        message: Error message description
    """
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    symbol_table["errors"].append(f"Line {line}: {message}")

# === OOP compatibility layer ===
# Not needed for this helper function

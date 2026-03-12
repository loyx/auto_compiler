# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,
#   "children": list,
#   "value": Any,
#   "data_type": str,
#   "line": int,
#   "column": int,
#   "name": str,
#   "return_type": str,
#   "params": list
# }

SymbolTable = Dict[str, Any]
# SymbolTable possible fields:
# {
#   "variables": Dict[str, Dict],
#   "functions": Dict[str, Dict],
#   "current_scope": int,
#   "scope_stack": list,
#   "current_function": str,
#   "errors": list
# }

# === main function ===
def _handle_variable_declaration(node: AST, symbol_table: SymbolTable) -> None:
    """Handle variable_declaration nodes by registering variables in the symbol table."""
    # Ensure required fields exist in symbol_table
    if "variables" not in symbol_table:
        symbol_table["variables"] = {}
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    
    # Extract variable information from node
    var_name = node.get("name") or node.get("value")
    data_type = node.get("data_type")
    line = node.get("line", 0)
    column = node.get("column", 0)
    
    # Get current scope level
    scope_level = symbol_table.get("current_scope", 0)
    
    # Check for duplicate declaration at same scope level
    if var_name in symbol_table["variables"]:
        existing = symbol_table["variables"][var_name]
        if existing.get("scope_level") == scope_level:
            error_msg = f"Error: Variable '{var_name}' already declared at line {existing['line']}, column {existing['column']}"
            symbol_table["errors"].append(error_msg)
            return
    
    # Register variable in symbol table
    symbol_table["variables"][var_name] = {
        "data_type": data_type,
        "is_declared": True,
        "line": line,
        "column": column,
        "scope_level": scope_level
    }

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this function
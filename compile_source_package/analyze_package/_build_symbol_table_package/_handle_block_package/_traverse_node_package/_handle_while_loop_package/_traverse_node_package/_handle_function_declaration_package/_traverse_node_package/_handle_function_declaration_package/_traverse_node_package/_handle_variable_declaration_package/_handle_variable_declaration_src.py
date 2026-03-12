# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed for this simple handler

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,
#   "name": str,
#   "value": Any,
#   "var_type": str,
#   "line": int,
#   "column": int
# }

SymbolTable = Dict[str, Any]
# SymbolTable possible fields:
# {
#   "variables": Dict[str, Dict],
#   "functions": Dict[str, Dict],
#   "current_scope": int,
#   "scope_stack": list
# }

# === main function ===
def _handle_variable_declaration(node: AST, symbol_table: SymbolTable) -> None:
    """
    Handle variable declaration node and register variable info to symbol table.
    
    Args:
        node: AST node of type variable_declaration
        symbol_table: Symbol table to be modified
    
    Side Effects:
        Modifies symbol_table["variables"] dictionary
    """
    # Extract variable information from node
    var_name = node.get("name")
    var_type = node.get("var_type", "any")
    var_value = node.get("value")
    line = node.get("line", 0)
    column = node.get("column", 0)
    
    # Get current scope from symbol table
    current_scope = symbol_table.get("current_scope", 0)
    
    # Build variable entry
    variable_entry = {
        "name": var_name,
        "var_type": var_type,
        "scope": current_scope,
        "line": line,
        "column": column
    }
    
    # Add value if present
    if var_value is not None:
        variable_entry["value"] = var_value
    
    # Register variable to symbol table
    if "variables" not in symbol_table:
        symbol_table["variables"] = {}
    
    symbol_table["variables"][var_name] = variable_entry

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# No OOP wrapper needed for this helper function

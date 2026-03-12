# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,
#   "name": str,
#   "data_type": str,
#   "line": int,
#   "column": int
# }

SymbolTable = Dict[str, Any]
# SymbolTable possible fields:
# {
#   "variables": Dict[str, Dict],
#   "current_scope": int,
# }

# === main function ===
def _verify_variable_ref(node: dict, symbol_table: dict, filename: str) -> None:
    """Verify variable reference node against symbol table."""
    var_name = node['name']
    variables = symbol_table['variables']
    current_scope = symbol_table['current_scope']
    
    # Check if variable exists
    if var_name not in variables:
        raise ValueError(
            f"{filename}:{node['line']}:{node['column']}: "
            f"error: variable '{var_name}' was not declared in this scope"
        )
    
    var_info = variables[var_name]
    
    # Check if variable is declared
    if not var_info.get('is_declared', False):
        raise ValueError(
            f"{filename}:{node['line']}:{node['column']}: "
            f"error: variable '{var_name}' was not declared in this scope"
        )
    
    # Check scope visibility
    if var_info['scope_level'] > current_scope:
        raise ValueError(
            f"{filename}:{node['line']}:{node['column']}: "
            f"error: variable '{var_name}' was not declared in this scope"
        )
    
    # Set the data type on the node
    node['data_type'] = var_info['data_type']

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this function node

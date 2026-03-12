# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No child functions needed for this validation logic

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,
#   "children": list,
#   "value": Any,
#   "data_type": str,
#   "line": int,
#   "column": int
# }

SymbolTable = Dict[str, Any]
# SymbolTable possible fields:
# {
#   "variables": Dict[str, Dict],
#   "functions": Dict[str, Dict],  # func_name -> {return_type, params, line, column}
#   "current_scope": int,
#   "scope_stack": list,
#   "current_function": str,
#   "errors": list
# }

# === main function ===
def _handle_function_call(node: AST, symbol_table: SymbolTable) -> None:
    """
    Handle function_call type AST node.
    Validate: 1) function declared, 2) argument count, 3) argument types.
    Side effect: may add errors to symbol_table["errors"].
    """
    func_name = node.get("value")
    args = node.get("children", [])
    
    # Check if function is declared
    functions = symbol_table.get("functions", {})
    if func_name not in functions:
        symbol_table.setdefault("errors", []).append(f"Function '{func_name}' not declared")
        return
    
    func_decl = functions[func_name]
    declared_params = func_decl.get("params", [])
    
    # Check argument count
    if len(args) != len(declared_params):
        symbol_table.setdefault("errors", []).append("Argument count mismatch")
        return
    
    # Check argument types
    for i, arg_node in enumerate(args):
        arg_type = arg_node.get("data_type")
        expected_type = declared_params[i].get("data_type") if isinstance(declared_params[i], dict) else declared_params[i]
        if arg_type != expected_type:
            symbol_table.setdefault("errors", []).append("Type mismatch")
            return

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this validation function
# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed for this implementation

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
def _handle_return(node: AST, symbol_table: SymbolTable) -> None:
    """
    Handle return statement nodes by validating they're inside functions
    and return types match function declarations.
    """
    line = node.get("line", 0)
    column = node.get("column", 0)
    
    # Check if we're inside a function
    current_function = symbol_table.get("current_function")
    if not current_function:
        symbol_table["errors"].append({
            "type": "error",
            "message": "return statement outside function",
            "line": line,
            "column": column
        })
        return
    
    # Get function declaration from symbol table
    functions = symbol_table.get("functions", {})
    func_decl = functions.get(current_function)
    
    if not func_decl:
        symbol_table["errors"].append({
            "type": "error",
            "message": "return statement outside function",
            "line": line,
            "column": column
        })
        return
    
    # Extract return value data_type from node
    return_type = node.get("data_type")
    declared_return_type = func_decl.get("return_type")
    
    # Validate return type matches function declaration
    if return_type is not None and declared_return_type is not None:
        if return_type != declared_return_type:
            symbol_table["errors"].append({
                "type": "error",
                "message": "Return type mismatch",
                "line": line,
                "column": column
            })

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this function node
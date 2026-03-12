# === std / third-party imports ===
from typing import Any, Dict

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,
#   "name": str,             # function name being called
#   "arguments": list,       # argument list, each element is an AST node
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
def _handle_function_call(node: AST, symbol_table: SymbolTable) -> None:
    """
    Handle function_call AST node by recursively traversing all arguments.
    
    Input:
      - node: AST node containing "name" (function name) and "arguments" (parameter list)
      - symbol_table: Symbol table for tracking variables and functions
    
    Processing:
      1. Extract "arguments" field from node (a list)
      2. Iterate through each argument node in the list
      3. For each non-None argument, call _traverse_node for recursive traversal
    
    Side effects:
      - May modify symbol_table through recursive _traverse_node calls
    """
    # Lazy import to avoid circular dependency with _traverse_node_src
    from .._traverse_node_src import _traverse_node
    
    arguments = node.get("arguments", [])
    
    for arg_node in arguments:
        if arg_node is not None:
            _traverse_node(arg_node, symbol_table)

# === helper functions ===
# No helper functions needed for this simple traversal logic

# === OOP compatibility layer ===
# No OOP wrapper needed - this is a handler function, not a framework entry point

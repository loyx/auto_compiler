# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
from ._traverse_node_package._traverse_node_src import _traverse_node

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
#   "functions": Dict[str, Dict],
#   "current_scope": int,
#   "scope_stack": list,
#   "current_function": str,
#   "errors": list
# }

# === main function ===
def _handle_if(node: AST, symbol_table: SymbolTable) -> None:
    """Handle if-statement node in AST traversal."""
    # Save current scope level
    old_scope = symbol_table.get("current_scope", 0)
    
    # Enter new scope
    symbol_table["current_scope"] = old_scope + 1
    
    # Push old scope to stack
    scope_stack = symbol_table.setdefault("scope_stack", [])
    scope_stack.append(old_scope)
    
    try:
        # Process each child node (condition, then_block, optional else_block)
        children = node.get("children", [])
        for child in children:
            _traverse_node(child, symbol_table)
    except Exception as e:
        # Collect errors
        errors = symbol_table.setdefault("errors", [])
        errors.append({
            "type": "if_handling_error",
            "message": str(e),
            "line": node.get("line"),
            "column": node.get("column")
        })
    finally:
        # Exit scope: restore from stack
        if scope_stack:
            symbol_table["current_scope"] = scope_stack.pop()

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this function node

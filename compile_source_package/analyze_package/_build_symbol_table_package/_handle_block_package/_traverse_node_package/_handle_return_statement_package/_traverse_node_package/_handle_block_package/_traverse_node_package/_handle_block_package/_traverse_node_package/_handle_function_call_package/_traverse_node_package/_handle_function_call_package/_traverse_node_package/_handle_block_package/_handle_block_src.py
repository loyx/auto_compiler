# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# Import parent function for recursive traversal of child nodes
from .._traverse_node_src import _traverse_node

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
def _handle_block(node: AST, symbol_table: SymbolTable) -> None:
    """
    Handle block-type AST nodes.
    
    Manages scope: enters new scope on entry, traverses children, exits scope on exit.
    """
    # Enter new scope
    old_scope = symbol_table.get("current_scope", 0)
    symbol_table["current_scope"] = old_scope + 1
    symbol_table.setdefault("scope_stack", []).append(old_scope)
    
    try:
        # Traverse child nodes
        for child in node.get("children", []):
            _traverse_node(child, symbol_table)
    finally:
        # Exit scope (guaranteed restoration)
        if symbol_table.get("scope_stack"):
            symbol_table["current_scope"] = symbol_table["scope_stack"].pop()
        else:
            symbol_table["current_scope"] = old_scope

# === helper functions ===
# No helper functions needed for this simple logic

# === OOP compatibility layer ===
# Not needed for this function node

# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions; _traverse_node is imported from parent module

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,             # Node type
#   "children": list,        # Child nodes list
#   "value": Any,            # Node value
#   "line": int,             # Line number
#   "column": int            # Column number
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
def _handle_if_statement(node: AST, symbol_table: SymbolTable) -> None:
    """
    Handle if_statement nodes: process condition and manually traverse then/else blocks.
    
    Input: AST node of type 'if_statement', symbol_table
    Processing: Extract condition, then-block, else-block; manually traverse children with scope handling
    Side effects: May modify symbol_table through child traversal
    Exception: None
    """
    # Deferred import to avoid circular dependency
    from .. import _traverse_node
    
    # Ensure required fields exist in symbol_table
    if "errors" not in symbol_table:
        symbol_table["errors"] = []
    if "scope_stack" not in symbol_table:
        symbol_table["scope_stack"] = []
    if "current_scope" not in symbol_table:
        symbol_table["current_scope"] = 0
    
    # Validate children structure
    children = node.get("children", [])
    if len(children) < 2:
        symbol_table["errors"].append(
            f"Error: if_statement at line {node.get('line', 0)}, column {node.get('column', 0)} "
            f"requires at least condition and then-block"
        )
        return
    
    # Extract nodes
    condition_node = children[0]
    then_block_node = children[1]
    else_block_node = children[2] if len(children) > 2 else None
    
    # Traverse condition expression (no new scope)
    _traverse_node(condition_node, symbol_table)
    
    # Handle then-block (create new scope)
    symbol_table["scope_stack"].append(symbol_table["current_scope"])
    symbol_table["current_scope"] += 1
    
    then_children = then_block_node.get("children", [])
    for child in then_children:
        _traverse_node(child, symbol_table)
    
    # Exit then-block scope
    if symbol_table["scope_stack"]:
        symbol_table["current_scope"] = symbol_table["scope_stack"].pop()
    
    # Handle else-block if exists (create new scope)
    if else_block_node is not None:
        symbol_table["scope_stack"].append(symbol_table["current_scope"])
        symbol_table["current_scope"] += 1
        
        else_children = else_block_node.get("children", [])
        for child in else_children:
            _traverse_node(child, symbol_table)
        
        # Exit else-block scope
        if symbol_table["scope_stack"]:
            symbol_table["current_scope"] = symbol_table["scope_stack"].pop()

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not required for this function node

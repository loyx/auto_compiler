# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# Import parent function for recursive traversal (controlled back-call pattern)
from main_package.compile_source_package.analyze_package._build_symbol_table_package._handle_block_package._traverse_node_package._handle_while_loop_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._handle_function_declaration_package._traverse_node_package._traverse_node_src import _traverse_node

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,
#   "condition": AST,
#   "then_branch": AST,
#   "else_branch": AST,
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
def _handle_if_statement(node: AST, symbol_table: SymbolTable) -> None:
    """
    Handle if_statement AST node by recursively traversing its condition and branches.
    
    Args:
        node: if_statement type AST node containing condition, then_branch, else_branch
        symbol_table: Symbol table passed down for child nodes (read-only)
    """
    condition = node.get("condition")
    then_branch = node.get("then_branch")
    else_branch = node.get("else_branch")
    
    # Recursively traverse condition
    if condition is not None:
        _traverse_node(condition, symbol_table)
    
    # Recursively traverse then branch
    if then_branch is not None:
        _traverse_node(then_branch, symbol_table)
    
    # Recursively traverse else branch if exists
    if else_branch is not None:
        _traverse_node(else_branch, symbol_table)

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not required for this function node

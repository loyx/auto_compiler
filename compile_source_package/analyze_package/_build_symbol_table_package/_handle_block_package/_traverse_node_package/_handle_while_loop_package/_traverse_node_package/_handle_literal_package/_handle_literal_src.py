# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed for this stub

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,
#   "value": Any,            # 字面量值
#   "data_type": str,        # 数据类型 ("int" 或 "char")
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
def _handle_literal(node: AST, symbol_table: SymbolTable) -> None:
    """
    Handle literal AST node.
    
    Literal nodes represent self-contained values (integers, characters).
    They do not require symbol table registration or special processing.
    This function validates the node structure and returns immediately.
    
    Args:
        node: AST node with "value" and "data_type" fields
        symbol_table: Symbol table (not modified by this function)
    """
    # Validate node has required fields for literal type
    _ = node.get("value")
    _ = node.get("data_type")
    # Literals are self-contained; no symbol table operation needed
    return

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this function node

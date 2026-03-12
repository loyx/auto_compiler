# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No subfunctions needed for this simple constructor

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,
#   "children": list,
#   "value": Any,
#   "line": int,
#   "column": int
# }

# === main function ===
def _create_ast_node(node_type: str, value: Any, children: list, line: int, column: int) -> AST:
    """
    Create a standard AST node dictionary.
    
    Args:
        node_type: AST node type string (e.g., "ObjectLiteral", "Property")
        value: Node value (string, number, or None for container nodes)
        children: List of child AST node dictionaries
        line: Starting line number
        column: Starting column number
    
    Returns:
        AST node dictionary with type, children, value, line, column fields
    """
    return {
        "type": node_type,
        "children": children,
        "value": value,
        "line": line,
        "column": column
    }

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this helper function
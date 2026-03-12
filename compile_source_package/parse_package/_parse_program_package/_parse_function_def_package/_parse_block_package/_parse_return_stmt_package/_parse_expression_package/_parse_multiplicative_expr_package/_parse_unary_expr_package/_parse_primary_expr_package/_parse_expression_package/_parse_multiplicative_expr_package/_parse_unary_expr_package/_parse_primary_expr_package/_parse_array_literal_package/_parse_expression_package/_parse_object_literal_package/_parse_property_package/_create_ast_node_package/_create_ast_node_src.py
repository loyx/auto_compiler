# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed for this utility constructor

# === ADT defines ===
AST = Dict[str, Any]
# AST possible fields:
# {
#   "type": str,
#   "value": Any,
#   "children": list,
#   "line": int,
#   "column": int
# }

# === main function ===
def _create_ast_node(node_type: str, value: Any, children: list, line: int, column: int) -> AST:
    """
    Create an AST node dictionary.
    
    This is a pure constructor function used by all parser functions.
    No side effects, does not modify input parameters.
    
    Args:
        node_type: Node type string (e.g., "Property", "ObjectLiteral", "StringLiteral", "Identifier")
        value: Node value (None, str, int, float, bool, etc.). Usually None for container nodes.
        children: List of child AST nodes. Empty list [] for leaf nodes.
        line: Starting line number (1-indexed)
        column: Starting column number (1-indexed)
    
    Returns:
        AST dictionary with type/value/children/line/column fields
    """
    return {
        "type": node_type,
        "value": value,
        "children": children,
        "line": line,
        "column": column
    }

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this utility function

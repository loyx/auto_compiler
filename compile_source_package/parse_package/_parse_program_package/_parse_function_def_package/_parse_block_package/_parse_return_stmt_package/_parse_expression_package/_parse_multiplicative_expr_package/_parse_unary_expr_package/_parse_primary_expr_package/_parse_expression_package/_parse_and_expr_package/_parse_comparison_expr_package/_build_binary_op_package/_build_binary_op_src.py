# === std / third-party imports ===
from typing import Any, Dict

# === sub function imports ===
# No sub functions needed for this simple builder

# === ADT defines ===
Token = Dict[str, Any]
# Token possible fields:
# {
#   "type": str,
#   "value": str,
#   "line": int,
#   "column": int
# }

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
def _build_binary_op(operator: str, left: AST, right: AST, op_token: Token) -> AST:
    """
    Build a BINARY_OP AST node.
    
    Args:
        operator: Operator string (e.g., "AND", "<", "==")
        left: Left operand AST node
        right: Right operand AST node
        op_token: Operator token for line/column information
    
    Returns:
        BINARY_OP AST node with structure:
        {
            "type": "BINARY_OP",
            "operator": operator,
            "children": [left, right],
            "line": op_token["line"],
            "column": op_token["column"]
        }
    """
    return {
        "type": "BINARY_OP",
        "operator": operator,
        "children": [left, right],
        "line": op_token["line"],
        "column": op_token["column"]
    }

# === helper functions ===
# No helper functions needed

# === OOP compatibility layer ===
# Not needed for this utility function
